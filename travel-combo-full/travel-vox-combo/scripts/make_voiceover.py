#!/usr/bin/env python3
"""Generate per-scene TTS voiceover files for a travel-vox-combo project (V1).

Reads project.json, synthesizes each scene's `narration` (spoken form) with the
TTS CLI, and writes voiceover_NNN.mp3 + manifest.json into a voiceover dir.

Usage:
  python3 scripts/make_voiceover.py project.json [--out-dir DIR]

Default out dir: <project.json's parent>/voiceover.

Each MP3 must fit its scene: duration <= usable_duration_seconds + 0.5s,
otherwise the script exits nonzero and names the offending scenes (shorten the
narration text and re-run; do not raise TTS speed above 105).

TTS is called via subprocess with the narration piped through stdin -- the text
never appears in a shell command. On TTS failure the script prints the exact
failing command for a later identical retry (see references/voiceover.md for
the retry ladder) and exits nonzero.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

TTS_CLI = "/opt/hatch/bin/tts"
DEFAULT_VOICE = "avocado_v2:MAI_01"
TOLERANCE = 0.5  # seconds a voiceover may exceed usable_duration_seconds


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def synth_scene(voice: str, text: str, output: Path) -> None:
    """Run one tts speak call. Raises RuntimeError with the exact failing command."""
    cmd = [TTS_CLI, "speak", "--voice", voice,
           "--output", str(output), "--text-stdin"]
    try:
        proc = subprocess.run(cmd, input=text, capture_output=True, text=True)
    except FileNotFoundError:
        raise RuntimeError(f"TTS CLI not found at {TTS_CLI}")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "unknown error").strip()
        raise RuntimeError(
            f"TTS failed for {output.name}: {err}\n"
            f"Retry the identical request later (see references/voiceover.md):\n"
            f"  {' '.join(cmd)}  # with the scene narration via stdin")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    project_path = Path(args.project)
    doc = json.loads(project_path.read_text(encoding="utf-8"))

    if not doc.get("voiceover", True):
        print("voiceover disabled in project JSON; nothing to generate")
        return 0

    voice = doc.get("narrator_voice") or DEFAULT_VOICE
    if not isinstance(voice, str) or not voice.strip():
        raise SystemExit("narrator_voice must be a nonempty voice id")

    if not shutil.which("ffprobe"):
        raise SystemExit("ffprobe is required to verify voiceover durations")

    out_dir = Path(args.out_dir) if args.out_dir else project_path.parent / "voiceover"
    out_dir.mkdir(parents=True, exist_ok=True)

    scenes = doc.get("scenes", [])
    if not scenes:
        raise SystemExit("project has no scenes")

    manifest = {"voice": voice, "scenes": {}}
    overlong = []
    for scene in scenes:
        n = int(scene["scene"])
        text = scene.get("narration", "")
        if not isinstance(text, str) or not text.strip():
            raise SystemExit(f"scene {n}: narration must be nonempty text for voiceover")
        usable = float(scene.get("usable_duration_seconds", 10))
        dest = out_dir / f"voiceover_{n:03d}.mp3"
        print(f"scene {n}: synthesizing ({len(text)} chars) -> {dest.name}")
        synth_scene(voice, text, dest)
        dur = probe_duration(dest)
        ok = dur <= usable + TOLERANCE
        manifest["scenes"][str(n)] = {
            "file": dest.name,
            "duration_secs": round(dur, 3),
            "usable_duration_seconds": usable,
            "ok": ok,
        }
        print(f"scene {n}: {dur:.2f}s vs usable {usable:.2f}s -> {'OK' if ok else 'TOO LONG'}")
        if not ok:
            overlong.append(n)

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False),
                             encoding="utf-8")
    print(f"manifest: {manifest_path}")

    if overlong:
        print("VOICEOVER TOO LONG for scenes: " + ", ".join(map(str, overlong)))
        print("Shorten those scenes' narration text and re-run; "
              "do not raise TTS speed above 105.")
        return 1
    print("VOICEOVER COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
