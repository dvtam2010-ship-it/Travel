#!/usr/bin/env python3
"""Scaffold a new travel-montage project.

Usage:
    python3 scripts/new-project.py --title "Ha Giang Loop" --format 16:9 --duration 4
    python3 scripts/new-project.py   # interactive mode

Creates out/<slug>/ with PROJECT.md, beats.json, seo.json, queries.json,
asset_manifest.json scaffolds + clips/raw/ + audio/ dirs.
"""
import argparse
import json
import os
import re
import unicodedata

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(SKILL_DIR, "out")
SHOT_SECONDS = 10  # default seconds per shot


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return text or "untitled"


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold travel-montage project")
    ap.add_argument("--title", help="Video topic/title")
    ap.add_argument("--format", default="16:9", choices=["16:9", "9:16"])
    ap.add_argument("--duration", type=float, default=4.0,
                    help="Duration in minutes (default 4)")
    args = ap.parse_args()

    title = args.title or input("Chủ đề video: ").strip()
    fmt = args.format
    if not args.title:
        f = input("Định dạng [16:9]: ").strip()
        if f in ("16:9", "9:16"):
            fmt = f
        d = input("Thời lượng phút [4]: ").strip()
        if d:
            args.duration = float(d)

    slug = slugify(title)
    total_s = int(args.duration * 60)
    n_shots = max(1, round(total_s / SHOT_SECONDS))

    proj = os.path.join(OUT_DIR, slug)
    os.makedirs(os.path.join(proj, "clips", "raw"), exist_ok=True)
    os.makedirs(os.path.join(proj, "audio"), exist_ok=True)

    beats = [
        {
            "id": f"shot_{i+1:02d}",
            "narration_en": "",
            "duration_s": SHOT_SECONDS,
            "visual_note": "",
        }
        for i in range(n_shots)
    ]
    with open(os.path.join(proj, "beats.json"), "w", encoding="utf-8") as f:
        json.dump(beats, f, ensure_ascii=False, indent=2)

    seo = {
        "title": "",
        "description": "",
        "tags": [],
        "hashtags": ["#WondersOfVietnam"],
    }
    with open(os.path.join(proj, "seo.json"), "w", encoding="utf-8") as f:
        json.dump(seo, f, ensure_ascii=False, indent=2)

    with open(os.path.join(proj, "queries.json"), "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

    manifest = {"project": slug, "assets": []}
    with open(os.path.join(proj, "asset_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    project_md = (
        f"# {title}\n\n"
        f"- Slug: `{slug}`\n"
        f"- Format: {fmt}\n"
        f"- Duration: ~{args.duration:g} min ({total_s}s)\n"
        f"- Shots: {n_shots} (~{SHOT_SECONDS}s/shot)\n"
        f"- Language: English (narration, subtitles, SEO)\n"
        f"- Channel: Wonders of Vietnam\n\n"
        f"## Next\n"
        f"1. Viết kịch bản: đọc `references/script-writing-travel-en.md`, "
        f"điền `beats.json` + `seo.json` → **GATE 1: user duyệt**\n"
        f"2. `python3 scripts/build-queries.py out/{slug}/beats.json` → "
        f"`queries.json`\n"
    )
    with open(os.path.join(proj, "PROJECT.md"), "w", encoding="utf-8") as f:
        f.write(project_md)

    print(f"OK: {proj} ({n_shots} shots, {fmt}, ~{args.duration:g} min)")
    print("Tiếp theo: viết kịch bản theo references/script-writing-travel-en.md (GATE 1).")


if __name__ == "__main__":
    main()
