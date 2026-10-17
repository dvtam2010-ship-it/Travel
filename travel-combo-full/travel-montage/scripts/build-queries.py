#!/usr/bin/env python3
"""Draft English stock-footage search queries from beats.json.

Usage:
    python3 scripts/build-queries.py out/<slug>/beats.json [--out queries.json]

Reads each beat's visual_note (falls back to narration_en keywords) and emits
2 draft queries per shot into queries.json. The agent MUST review/refine every
query before hunting footage (see references/footage-sourcing.md).
"""
import argparse
import json
import os
import re

STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "at", "to", "for",
    "with", "from", "by", "is", "are", "was", "were", "be", "it", "its",
    "this", "that", "these", "those", "you", "your", "we", "our", "i",
    "as", "so", "but", "not", "no", "if", "what", "when", "where", "how",
    "can", "will", "just", "like", "more", "most", "than", "then", "there",
    "their", "they", "them", "he", "she", "his", "her", "into", "over",
    "under", "about", "up", "out", "all", "one", "also", "very", "much",
}


def keywords(text: str, n: int = 6):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    seen, out = set(), []
    for w in words:
        w = w.strip("'")
        if len(w) < 3 or w in STOPWORDS or w in seen:
            continue
        seen.add(w)
        out.append(w)
        if len(out) >= n:
            break
    return out


def draft_queries(beat: dict):
    visual = (beat.get("visual_note") or "").strip()
    narration = (beat.get("narration_en") or "").strip()
    queries = []
    if visual:
        queries.append(visual)
        kw = keywords(narration, 4)
        if kw:
            queries.append(" ".join(kw))
    elif narration:
        kw = keywords(narration, 6)
        if kw:
            queries.append(" ".join(kw[:4]))
            if len(kw) > 4:
                queries.append(" ".join(kw[2:]))
    # de-dup, keep max 3
    uniq = []
    for q in queries:
        if q and q not in uniq:
            uniq.append(q)
    return uniq[:3]


def main() -> None:
    ap = argparse.ArgumentParser(description="beats.json -> queries.json drafts")
    ap.add_argument("beats", help="Path to beats.json")
    ap.add_argument("--out", default=None, help="Output path (default: alongside beats)")
    args = ap.parse_args()

    with open(args.beats, encoding="utf-8") as f:
        beats = json.load(f)

    result = [
        {"shot_id": b.get("id", f"shot_{i+1:02d}"), "queries": draft_queries(b)}
        for i, b in enumerate(beats)
    ]

    out_path = args.out or os.path.join(os.path.dirname(args.beats), "queries.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    empty = sum(1 for r in result if not r["queries"])
    print(f"OK: {out_path} ({len(result)} shots, {empty} without draft queries)")
    print("LƯU Ý: agent phải hiệu đính từng query theo references/footage-sourcing.md trước khi săn.")


if __name__ == "__main__":
    main()
