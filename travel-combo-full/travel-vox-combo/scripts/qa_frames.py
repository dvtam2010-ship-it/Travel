#!/usr/bin/env python3
"""Extract QA frames and build per-scene checklists for travel-vox-combo (V1).

Usage:
  python3 scripts/qa_frames.py project.json clips_dir qa_dir

For each scene_NNN.mp4 in clips_dir:
  - probes real duration with ffprobe
  - extracts 5 frames at 10/30/50/70/90% of duration to
    qa_dir/frames/scene_NNN_f1..f5.jpg (quality -q:v 3)
  - writes qa_dir/scene_NNN_checklist.md from the project JSON
  - adds a skeleton entry to qa_dir/qa_report.json
    (status "pending", verdict null -- the human/model review fills these in)

Requires ffmpeg and ffprobe on PATH.
"""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

FRAME_FRACTIONS = [0.10, 0.30, 0.50, 0.70, 0.90]


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def extract_frames(clip: Path, duration: float, frames_dir: Path, n: int) -> list:
    frames_dir.mkdir(parents=True, exist_ok=True)
    names = []
    for idx, frac in enumerate(FRAME_FRACTIONS, 1):
        ts = max(0.0, duration * frac)
        name = f"scene_{n:03d}_f{idx}.jpg"
        dest = frames_dir / name
        # -ss after -i for accurate seek on short clips
        run(["ffmpeg", "-y", "-i", str(clip), "-ss", f"{ts:.3f}",
             "-frames:v", "1", "-q:v", "3", str(dest)])
        names.append(name)
    return names


def bullet_list(items):
    return "\n".join(f"- {x}" for x in items) if items else "- (none)"


def build_checklist(scene: dict) -> str:
    n = int(scene["scene"])
    stype = scene.get("scene_type", "?")
    lines = [
        f"# Scene {n:03d} QA checklist",
        "",
        f"- scene_type: `{stype}`",
        f"- timeline: {scene.get('timeline', '?')}",
        f"- narration (for context, not graded on frames): {scene.get('narration', '')}",
        "",
        "## Check on the frames",
    ]
    if stype == "real_life_documentary":
        lines += [
            f"- location: {scene.get('location', '')}",
            f"- cultural_behavior: {scene.get('cultural_behavior', '')}",
            f"- environmental_evidence:\n{bullet_list(scene.get('environmental_evidence', []))}",
            f"- human_action: {scene.get('human_action', '')}",
            f"- micro_actions:\n{bullet_list(scene.get('micro_actions', []))}",
            f"- wardrobe_context: {scene.get('wardrobe_context', '')}",
            f"- lighting: {scene.get('lighting', '')}",
            "",
            "### Accept / reject",
            "- [ ] location cues recognizable as the named place",
            "- [ ] the cultural behavior is actually visible",
            "- [ ] hands and hand-object contact look physically normal",
            "- [ ] face, clothing, props stable across all 5 frames",
            "- [ ] no staged/camera-facing reactions in background people",
        ]
    else:
        lines += [
            f"- information_goal: {scene.get('information_goal', '')}",
            f"- visual_subject: {scene.get('visual_subject', '')}",
            f"- headline: {scene.get('headline', '')}",
            f"- camera_move: {scene.get('camera_move', '')}",
            "",
            "### Accept / reject",
            "- [ ] paper-collage look consistent (no photorealistic bleed)",
            "- [ ] English explanatory text readable and spelled correctly",
            "- [ ] layout stable across all 5 frames",
        ]
    lines += [
        "",
        "### Negative prompt (must NOT appear)",
        bullet_list(scene.get("negative_prompt", [])),
        "",
        "### Continuity",
        scene.get("continuity_notes", "(none)"),
        "",
        "### Map integrity",
        f"map_integrity_required: {bool(scene.get('map_integrity_required', False))}",
    ]
    if scene.get("map_integrity_required"):
        lines += [
            "- [ ] mainland Vietnam present",
            "- [ ] Hoang Sa (Paracel Islands) present in a plausible position",
            "- [ ] Truong Sa (Spratly Islands) present in a plausible position",
        ]
    if scene.get("shows_currency"):
        lines += [
            "",
            "### Currency QA (Vietnamese dong — see references/vietnam-currency.md)",
            f"currency_detail: {scene.get('currency_detail', '')}",
            "- [ ] note color/size matches the stated denomination family",
            "- [ ] no readable text or numerals are garbled or wrong",
            "- [ ] **the portrait of Ho Chi Minh is dignified and undistorted** —",
            "  ANY warp, cartoonish distortion, or disrespectful context = regenerate",
            "- [ ] no close-up makes the note look like a counterfeit prop",
        ]
    lines += [
        "",
        "### Verdict",
        "- accept / regenerate (copy into qa_report.json with reason)",
        "- regenerate ONLY on material defects: wrong place/behavior, broken hands,",
        "  identity change, materially wrong map, distorted/disrespectful currency",
        "  portrait. Never for minor aesthetic differences.",
        "",
        "### Honesty limits",
        "- Frames are stills: motion smoothness and audio quality CANNOT be judged here.",
        "- Narration/audio must be checked separately (listen to the voiceover files).",
    ]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("clips_dir")
    ap.add_argument("qa_dir")
    args = ap.parse_args()

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg and ffprobe are required (both missing or not on PATH)")

    project_path = Path(args.project)
    clips_dir = Path(args.clips_dir)
    qa_dir = Path(args.qa_dir)
    frames_dir = qa_dir / "frames"
    qa_dir.mkdir(parents=True, exist_ok=True)

    doc = json.loads(project_path.read_text(encoding="utf-8"))
    scenes = doc.get("scenes", [])
    if not scenes:
        raise SystemExit("project has no scenes")

    report = {"project": doc.get("title", ""), "scenes": []}
    for scene in scenes:
        n = int(scene["scene"])
        clip = clips_dir / f"scene_{n:03d}.mp4"
        if not clip.exists():
            raise SystemExit(f"missing clip: {clip}")
        dur = probe_duration(clip)
        if dur <= 0:
            raise SystemExit(f"clip has no measurable duration: {clip}")
        frames = extract_frames(clip, dur, frames_dir, n)
        checklist_name = f"scene_{n:03d}_checklist.md"
        (qa_dir / checklist_name).write_text(build_checklist(scene), encoding="utf-8")
        report["scenes"].append({
            "scene": n,
            "status": "pending",
            "frames": frames,
            "checklist": checklist_name,
            "verdict": None,
            "notes": "",
        })
        print(f"scene {n:03d}: {dur:.2f}s -> 5 frames + checklist")

    report_path = qa_dir / "qa_report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"qa report skeleton: {report_path}")
    print("QA FRAMES READY")


if __name__ == "__main__":
    sys.exit(main())
