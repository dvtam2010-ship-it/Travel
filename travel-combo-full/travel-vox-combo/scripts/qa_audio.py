#!/usr/bin/env python3
"""Audio QA for travel-vox-combo background beds and final mixes.

Muse video clips often ship with loud broadband hiss as their "ambience",
sometimes only ~5 dB under the voiceover, which survives light ducking and
sounds like noise over the narration. This script measures every scene's bed
against its voiceover and checks the final mix for sane loudness and clipping.

Usage:
  python3 scripts/qa_audio.py project.json clips_dir qa_dir \
      [--voiceover-dir DIR] [--final final.mp4]

Writes qa_dir/audio_report.json and prints a per-scene table.
Exit 0 unless a FAIL is found (bed masks voice, or final clips).

Thresholds (see references/audio-qa.md):
  bed_vs_voice_gap = vo_I - bed_I (integrated LUFS)
    gap >= 10 dB            -> pass
    4 dB <= gap < 10 dB     -> warn  (assembly denoise+duck should handle it)
    gap < 4 dB              -> FAIL  (bed will mask the voice)
  hiss: bed high-frequency loudness (highpass 6 kHz) within 15 dB of the
    bed's full loudness     -> warn  ("hissy bed", informational)
  final mix: true peak > -1.0 dBFS -> FAIL (clipping);
    integrated outside [-30, -12] LUFS -> warn.
"""
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def has_audio(path: Path) -> bool:
    r = run(["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=index", "-of", "csv=p=0", str(path)])
    return bool(r.stdout.strip())


def loudness(path: Path, af: str = "ebur128=peak=true"):
    """Return (integrated_lufs, lra_lu, true_peak_dbfs) or (None, None, None)."""
    r = run(["ffmpeg", "-hide_banner", "-i", str(path),
             "-af", af, "-f", "null", "-"])
    out = r.stderr
    i_vals = re.findall(r"I:\s+(-?\d+(?:\.\d+)?)\s+LUFS", out)
    lra_vals = re.findall(r"LRA:\s+(-?\d+(?:\.\d+)?)\s+LU", out)
    peak_vals = re.findall(r"Peak:\s+(-?\d+(?:\.\d+)?)\s+dBFS", out)
    try:
        return (float(i_vals[-1]), float(lra_vals[-1]),
                max(float(p) for p in peak_vals) if peak_vals else None)
    except (IndexError, ValueError):
        return (None, None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_json")
    ap.add_argument("clips_dir")
    ap.add_argument("qa_dir")
    ap.add_argument("--voiceover-dir", default=None)
    ap.add_argument("--final", default=None)
    args = ap.parse_args()

    proj = json.loads(Path(args.project_json).read_text(encoding="utf-8"))
    clips_dir = Path(args.clips_dir)
    qa_dir = Path(args.qa_dir)
    qa_dir.mkdir(parents=True, exist_ok=True)
    vo_dir = Path(args.voiceover_dir) if args.voiceover_dir else None

    scenes_out = []
    any_fail = False
    print(f"{'scene':>5} {'bed_I':>8} {'vo_I':>8} {'gap':>6}  verdict  notes")
    for s in proj.get("scenes", []):
        n = int(s["scene"])
        clip = clips_dir / f"scene_{n:03d}.mp4"
        entry = {"scene": n, "verdict": "pass", "notes": []}
        if not clip.exists() or not has_audio(clip):
            entry["notes"].append("no audio track in clip")
            scenes_out.append(entry)
            print(f"{n:>5} {'--':>8} {'--':>8} {'--':>6}  pass     no audio track")
            continue
        bed_i, _, _ = loudness(clip)
        bed_hf_i, _, _ = loudness(clip, "highpass=f=6000,ebur128")
        entry["bed_lufs"] = bed_i
        entry["bed_hf_lufs"] = bed_hf_i
        vo_i = None
        if vo_dir:
            vo = vo_dir / f"voiceover_{n:03d}.mp3"
            if vo.exists():
                vo_i, _, _ = loudness(vo)
        entry["vo_lufs"] = vo_i
        notes = []
        verdict = "pass"
        if bed_i is not None and bed_hf_i is not None:
            if bed_hf_i - bed_i > -15:
                notes.append("hissy bed (strong high-frequency noise)")
                verdict = "warn"
        if bed_i is not None and vo_i is not None:
            gap = vo_i - bed_i
            entry["bed_voice_gap_db"] = round(gap, 1)
            if gap < 4:
                verdict = "fail"
                notes.append(f"bed only {gap:.1f} dB under voice: will mask narration")
            elif gap < 10:
                verdict = "warn" if verdict == "pass" else verdict
                notes.append(f"bed {gap:.1f} dB under voice: denoise+duck required")
        else:
            entry["bed_voice_gap_db"] = None
        entry["verdict"] = verdict
        entry["notes"] = notes
        if verdict == "fail":
            any_fail = True
        gap_s = f"{entry['bed_voice_gap_db']:>6.1f}" if entry.get("bed_voice_gap_db") is not None else f"{'--':>6}"
        bed_s = f"{bed_i:>8.1f}" if bed_i is not None else f"{'--':>8}"
        vo_s = f"{vo_i:>8.1f}" if vo_i is not None else f"{'--':>8}"
        print(f"{n:>5} {bed_s} {vo_s} {gap_s}  {verdict:<6} {'; '.join(notes)}")
        scenes_out.append(entry)

    final_out = None
    if args.final:
        fp = Path(args.final)
        if fp.exists():
            i, lra, peak = loudness(fp)
            final_out = {"path": str(fp), "integrated_lufs": i, "lra_lu": lra,
                         "true_peak_dbfs": peak, "verdict": "pass", "notes": []}
            if peak is not None and peak > -1.0:
                final_out["verdict"] = "fail"
                final_out["notes"].append(f"true peak {peak:.1f} dBFS: clipping")
                any_fail = True
            if i is not None and (i < -30 or i > -12):
                if final_out["verdict"] == "pass":
                    final_out["verdict"] = "warn"
                final_out["notes"].append(f"integrated {i:.1f} LUFS outside [-30,-12]")
            print(f"\nfinal: I={i} LUFS  LRA={lra} LU  peak={peak} dBFS  "
                  f"-> {final_out['verdict']} {'; '.join(final_out['notes'])}")
        else:
            print(f"\nfinal: {fp} not found, skipped")

    verdict = "fail" if any_fail else (
        "pass_with_warnings" if any(e["verdict"] == "warn" for e in scenes_out)
        or (final_out and final_out["verdict"] == "warn") else "pass")
    report = {"generated_at": datetime.now(timezone.utc).isoformat(),
              "verdict": verdict, "scenes": scenes_out, "final": final_out}
    (qa_dir / "audio_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nAUDIO QA {verdict.upper()} -> {qa_dir / 'audio_report.json'}")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
