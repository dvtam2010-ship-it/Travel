#!/usr/bin/env python3
"""Assemble travel-vox-combo scene clips into final.mp4.

Muse video clips last ~10 seconds each (not exactly), so this script measures
every clip's real duration with ffprobe and trims the final clip so the total
runtime matches total_duration_seconds (tolerance +/-0.5s by default).

Usage:
  python3 scripts/assemble_clips.py project.json clips_dir final.mp4 [--voiceover-dir DIR] [--tolerance 0.5]

--voiceover-dir: directory with voiceover_001.mp3, voiceover_002.mp3, ... and
  manifest.json (see scripts/make_voiceover.py). Each voiceover is mixed over
  its scene's audio: the clip ambience is first cleaned (highpass + FFT
  denoise, because Muse video ambience is often noisy broadband hiss) and
  then deep-ducked under the voice with a sidechain compressor. Scenes
  without a voiceover file keep their original audio. A
  voiceover overflowing its scene by more than +0.5s triggers a loud warning
  instead of being cut silently.

Temp files honor the TMPDIR env var; set TMPDIR to a roomy path if /tmp is small.
"""
import argparse, json, shutil, subprocess, sys, tempfile
from pathlib import Path

UNIT = 10  # nominal Muse video clip length in seconds


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def has_audio(path: Path) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    return bool(out.stdout.strip())


# Seconds a voiceover may overflow its scene before it is treated as a problem.
VO_OVERFLOW_ALLOW = 0.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("clips_dir")
    ap.add_argument("output")
    ap.add_argument("--voiceover-dir", default=None)
    ap.add_argument("--tolerance", type=float, default=0.5)
    args = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg and ffprobe are required (both missing or not on PATH)")

    project_path = Path(args.project)
    clips_dir = Path(args.clips_dir).resolve()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    vo_dir = Path(args.voiceover_dir).resolve() if args.voiceover_dir else None
    if vo_dir and not vo_dir.is_dir():
        raise SystemExit(f"voiceover dir not found: {vo_dir}")

    doc = json.loads(project_path.read_text(encoding="utf-8"))
    scenes = doc["scenes"]
    aspect = doc.get("aspect_ratio", "9:16")
    requested = float(doc.get("total_duration_seconds", 0))
    if requested <= 0:
        raise SystemExit("total_duration_seconds must be positive")
    canvas = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080)}.get(aspect, (1080, 1920))
    w, h = canvas

    # Measure real durations; clips are only ~10s, never assume exactly 10.
    actuals = []
    for scene in scenes:
        n = int(scene["scene"])
        src = clips_dir / f"scene_{n:03d}.mp4"
        if not src.exists():
            raise SystemExit(f"missing clip: {src}")
        d = probe_duration(src)
        if d <= 0:
            raise SystemExit(f"clip has no measurable duration: {src}")
        actuals.append(d)

    # Per-scene trim plan: non-final scenes use at most UNIT seconds; the final
    # clip is trimmed so the total hits the requested duration.
    trims = []
    for idx, d in enumerate(actuals):
        if idx < len(scenes) - 1:
            trims.append(min(d, UNIT))
        else:
            remaining = requested - sum(trims)
            trims.append(max(0.1, min(d, remaining)))

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        normalized = []
        vo_warnings = []
        for scene, d, t in zip(scenes, actuals, trims):
            n = int(scene["scene"])
            src = clips_dir / f"scene_{n:03d}.mp4"
            dst = td / f"scene_{n:03d}.mp4"
            vf = (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                  f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30")
            vo = vo_dir / f"voiceover_{n:03d}.mp3" if vo_dir else None
            cmd = ["ffmpeg", "-y", "-i", str(src)]
            audio_args = ["-map", "0"]
            if vo and vo.exists():
                vd = probe_duration(vo)
                vo_use = min(vd, t + VO_OVERFLOW_ALLOW)
                if vd > t + VO_OVERFLOW_ALLOW:
                    vo_warnings.append(
                        f"scene {n}: voiceover {vd:.2f}s is {vd - t:.2f}s longer than "
                        f"the scene segment ({t:.2f}s) -- it will fade out at the scene "
                        f"end instead of being cut silently. Consider shortening the "
                        f"narration and re-running make_voiceover.py.")
                elif vd > t:
                    print(f"scene {n}: voiceover {vd:.2f}s slightly overflows the "
                          f"{t:.2f}s segment; allowing up to +{VO_OVERFLOW_ALLOW}s with fade-out")
                fade_st = max(0.0, vo_use - 0.4)
                cmd += ["-i", str(vo)]
                # Ducking: the voiceover keys a sidechain compressor on the clip's
                # ambience, so background audio drops while the voice speaks.
                if has_audio(src):
                    fc = (
                        f"[1:a]asplit=2[vo][key];"
                        # Denoise first: Muse video ambience is often loud
                        # broadband hiss; then duck it hard under the voice.
                        f"[0:a]highpass=f=70,afftdn=nr=14:nf=-45[dn];"
                        f"[dn][key]sidechaincompress=threshold=0.015:ratio=20:"
                        f"attack=10:release=400[bg];"
                        f"[vo]volume=1.3,atrim=0:{vo_use:.3f},asetpts=PTS-STARTPTS,"
                        f"afade=t=out:st={fade_st:.3f}:d=0.4[vo2];"
                        f"[bg][vo2]amix=inputs=2:duration=first:dropout_transition=0[a]"
                    )
                else:
                    fc = (
                        f"anullsrc=r=48000:cl=stereo:d={t:.3f}[bg];"
                        f"[1:a]volume=1.3,atrim=0:{vo_use:.3f},asetpts=PTS-STARTPTS,"
                        f"afade=t=out:st={fade_st:.3f}:d=0.4[vo2];"
                        f"[bg][vo2]amix=inputs=2:duration=first:dropout_transition=0[a]"
                    )
                audio_args = ["-filter_complex", fc, "-map", "0:v", "-map", "[a]"]
            cmd += ["-t", f"{t:.3f}", "-vf", vf,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30"] + audio_args + \
                   ["-c:a", "aac", "-ar", "48000", "-ac", "2", str(dst)]
            run(cmd)
            normalized.append(dst)
        concat = td / "concat.txt"
        concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in normalized), encoding="utf-8")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(output)])

    final = probe_duration(output)
    for w in vo_warnings:
        print("WARNING: " + w)
    if abs(final - requested) > args.tolerance:
        print(f"WARNING: final {final:.2f}s vs requested {requested:.2f}s "
              f"(tolerance +/-{args.tolerance}s); clips may have run short")
    print(output)


if __name__ == "__main__":
    main()
