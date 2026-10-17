#!/usr/bin/env python3
"""Validate a travel-vox-combo project JSON against references/muse-video-schema.md.

Usage:
  python3 scripts/validate_output.py project.json [--check-voiceover VOICEOVER_DIR]

--check-voiceover: additionally verify the voiceover manifest and audio files
  (voiceover_NNN.mp3 exist, manifest.json consistent, durations fit their scenes).
  Voiceover files are generated after JSON validation, so this check is optional
  and off by default.
"""
import argparse, json, math, re, subprocess, sys
from pathlib import Path

UNIT = 10  # nominal Muse video clip length in seconds
VO_TOLERANCE = 0.5  # seconds a voiceover may exceed usable_duration_seconds


def probe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def check_voiceover(doc, vo_dir: Path, errors: list) -> None:
    if not vo_dir.is_dir():
        errors.append(f"voiceover dir not found: {vo_dir}")
        return
    manifest_path = vo_dir / "manifest.json"
    if not manifest_path.exists():
        errors.append(f"voiceover manifest missing: {manifest_path}")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        errors.append(f"voiceover manifest unreadable: {e}")
        return
    entries = manifest.get("scenes", {})
    for scene in doc.get("scenes", []):
        n = int(scene["scene"])
        key = str(n)
        if key not in entries:
            errors.append(f"scene {n}: missing from voiceover manifest")
            continue
        entry = entries[key]
        audio = vo_dir / entry.get("file", f"voiceover_{n:03d}.mp3")
        if not audio.exists():
            errors.append(f"scene {n}: voiceover file missing: {audio.name}")
            continue
        try:
            dur = probe_duration(audio)
        except (subprocess.CalledProcessError, ValueError):
            errors.append(f"scene {n}: cannot probe voiceover duration: {audio.name}")
            continue
        usable = float(scene.get("usable_duration_seconds", UNIT))
        if dur > usable + VO_TOLERANCE:
            errors.append(f"scene {n}: voiceover {dur:.2f}s exceeds usable {usable:.2f}s "
                          f"(+{VO_TOLERANCE}s tolerance)")
        manifest_dur = entry.get("duration_secs")
        if isinstance(manifest_dur, (int, float)) and abs(manifest_dur - dur) > 0.05:
            errors.append(f"scene {n}: manifest duration {manifest_dur}s != "
                          f"measured {dur:.2f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--check-voiceover", default=None,
                    help="voiceover dir to verify against manifest")
    args = ap.parse_args()

    doc = json.loads(Path(args.project).read_text(encoding="utf-8"))
    errors = []
    total = float(doc.get("total_duration_seconds", 0))
    scenes = doc.get("scenes", [])
    expected = int(math.ceil(total / UNIT)) if total > 0 else 0
    if total <= 0:
        errors.append("total_duration_seconds must be positive")
    if len(scenes) != expected:
        errors.append(f"scene count {len(scenes)} != expected {expected} (ceil({total}/{UNIT}))")

    # V1 voiceover fields
    voiceover_on = doc.get("voiceover", True)
    if voiceover_on:
        voice = doc.get("narrator_voice", "avocado_v2:MAI_01")
        if not isinstance(voice, str) or not voice.strip():
            errors.append("narrator_voice must be a nonempty voice id when voiceover is true")

    documentary_text_fields = (
        "location", "cultural_behavior", "human_action", "wardrobe_context",
        "lighting", "sound_design", "continuity_notes"
    )
    documentary_list_fields = (
        "environmental_evidence", "micro_actions", "cultural_geographic_qa",
        "negative_prompt"
    )

    for i, s in enumerate(scenes, 1):
        if not isinstance(s, dict):
            errors.append(f"scene {i}: must be an object")
            continue
        if s.get("scene") != i:
            errors.append(f"scene index mismatch at position {i}")
        if s.get("generation_duration_seconds") != UNIT:
            errors.append(f"scene {i}: generation duration must be {UNIT}")
        expected_usable = UNIT if i < expected or total % UNIT == 0 else total - UNIT * (expected - 1)
        try:
            usable = float(s.get("usable_duration_seconds", -1))
        except (TypeError, ValueError):
            usable = -1
        if abs(usable - expected_usable) > 1e-6:
            errors.append(f"scene {i}: wrong usable duration (want {expected_usable})")
        scene_type = s.get("scene_type")
        if scene_type not in ("editorial_collage", "real_life_documentary"):
            errors.append(f"scene {i}: scene_type must be editorial_collage or real_life_documentary, got {scene_type!r}")
        if not isinstance(s.get("video_prompt"), str) or not s["video_prompt"].strip():
            errors.append(f"scene {i}: video_prompt must be nonempty text")
        if s.get("shows_currency"):
            detail = s.get("currency_detail", "")
            if not isinstance(detail, str) or not detail.strip():
                errors.append(f"scene {i}: currency_detail must be nonempty text when shows_currency is true "
                              f"(see references/vietnam-currency.md)")
        if voiceover_on:
            narration = s.get("narration", "")
            if not isinstance(narration, str) or not narration.strip():
                errors.append(f"scene {i}: narration must be nonempty text when voiceover is true")
        if scene_type == "real_life_documentary":
            for field in documentary_text_fields:
                if not isinstance(s.get(field), str) or not s[field].strip():
                    errors.append(f"scene {i}: {field} must be nonempty text")
            for field in documentary_list_fields:
                items = s.get(field)
                if not isinstance(items, list) or not items or any(not isinstance(x, str) or not x.strip() for x in items):
                    errors.append(f"scene {i}: {field} must be a nonempty list of text")
        if s.get("map_integrity_required"):
            text = " ".join(str(s.get(k, "")) for k in ["video_prompt", "headline", "visual_subject"])
            for term in ["Hoang Sa (Paracel Islands)", "Truong Sa (Spratly Islands)"]:
                if term not in text:
                    errors.append(f"scene {i}: map prompt missing {term}")
            if not re.search(r"16\.5|112", text):
                errors.append(f"scene {i}: Hoang Sa geographic anchor missing")
            if not re.search(r"7.?12|111.?117|9.?N|114", text):
                errors.append(f"scene {i}: Truong Sa geographic anchor missing")

    if args.check_voiceover and voiceover_on:
        check_voiceover(doc, Path(args.check_voiceover), errors)

    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print("-", e)
        raise SystemExit(1)
    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
