# Frame-Based Image QA (V1)

The assistant cannot watch video playback. Image QA therefore runs on **extracted frames**: 5 stills per scene at 10 / 30 / 50 / 70 / 90% of the clip's real duration, reviewed against a generated checklist.

## Running it

After clips are generated (and before assembly):

```sh
python3 scripts/qa_frames.py out/<project-slug>/project.json \
  out/<project-slug>/clips out/<project-slug>/qa
```

Output:
- `qa/frames/scene_NNN_f1..f5.jpg` — the frames (`-q:v 3`)
- `qa/scene_NNN_checklist.md` — per-scene checklist built from the project JSON: scene type, location/behavior/evidence (documentary) or information goal/subject (collage), negative prompt list, continuity notes, map requirements, accept/reject criteria
- `qa/qa_report.json` — skeleton with one entry per scene: `{status: "pending", frames: [...], checklist: path, verdict: null, notes: ""}`

## Review procedure

The assistant **can** read images, so review each scene's 5 frames directly:

1. Open the frames (in order f1 → f5) and read `scene_NNN_checklist.md`.
2. Check against the list:
   - **Location cues:** is the named place recognizable (not a generic backdrop)?
   - **Behavior:** is the cultural behavior actually visible, not just implied?
   - **Hands and contact:** do hands and hand-object contact look physically normal in every frame?
   - **Stability:** same face, clothing, and props across all 5 frames? No morphing storefronts or duplicated people?
   - **Negatives:** does anything from the scene's `negative_prompt` list appear?
   - **Map scenes:** mainland Vietnam + Hoang Sa (Paracel) + Truong Sa (Spratly) in plausible positions (see `references/vietnam-map.md`).
   - **Currency scenes** (`shows_currency: true`): note color matches the stated denomination; no garbled text/numerals; **the portrait of Hồ Chí Minh is dignified and undistorted** (see `references/vietnam-currency.md`).
3. **Cross-scene continuity:** when a scene's `continuity_notes` require it, compare the last frame of scene N with the first frame of scene N+1 (same person, clothes, props, position, time of day).
4. Write the verdict into `qa_report.json` for that scene: `verdict: "accept"` or `"regenerate"`, with the concrete reason in `notes`. Set `status: "done"`.

## When to regenerate

Regenerate **only on material defects**:

- wrong place or wrong behavior
- broken hands or impossible hand-object contact
- identity/clothing/prop change mid-scene
- materially wrong map (missing archipelagos, wrong country shape)
- **currency: distorted or disrespectful portrait of Hồ Chí Minh**, garbled denomination text, or a close-up that reads as a counterfeit prop

**Never regenerate** for minor aesthetic differences (slightly different lighting, background extra, framing taste). Avoid repeated retries chasing perfection.

If a scene repeatedly fails after 2 regenerations, keep the best take, log it as an unresolved limitation in `qa_report.json`, and move on — do not loop forever.

## Honesty limits

- Frames are stills. **Motion smoothness cannot be judged** — a clip can look fine frame-by-frame and still have jittery motion.
- **Audio cannot be judged** — narration intelligibility, ambience level, and the voiceover mix must be checked by listening to the voiceover MP3s and (after assembly) the final MP4.
- The checklist's narration line is context only, not something frames can prove.
