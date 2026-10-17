---
name: travel-vox-combo
description: >
  Travel vox combo V1.2: create English-narrated Vox-inspired short-form travel explainers about Vietnam
  for foreign visitors, generating video with Muse video (media.generate_video) instead of Google Flow.
  Use when the user wants a Vietnam travel guide video, TikTok, YouTube Short, or similar explainer
  produced end to end. Combine editorial paper-collage explanation with realistic, culturally specific
  everyday travel footage. Enforce one consistent English narrator, practical traveler guidance, and
  strict Vietnam map integrity: whenever Vietnam is mapped, include Hoang Sa (Paracel Islands) and
  Truong Sa (Spratly Islands) in geographically appropriate South China Sea positions.
---

# Travel Vox Combo Director — V1.2

Turn two required inputs — **title/topic** and **total duration** — into a finished short-form production workflow:

`title + duration -> timed English script -> ~10s scene blocks -> video_prompt JSON -> TTS voiceover -> Muse video generation -> frame QA -> clips -> final MP4`

Video generation uses the `media.generate_video` tool. Each generated clip lasts **approximately 10 seconds** — duration is not a parameter — so assembly measures real durations with ffprobe and trims the final clip to hit the requested total.

## Non-negotiable rules

1. **English explanatory language.** Narration, generated headlines, captions, map labels, prompt instructions, and JSON prose are in English. Authentic incidental Vietnamese speech and storefront signage may appear in documentary footage when appropriate; do not present Vietnamese as explanatory subtitles or fabricate legible signage.
2. **One narrator identity.** Keep the same narrator gender, accent family, age range, energy, pacing, and documentary tone for every scene — and the same TTS voice id (`narrator_voice`) for the voiceover on every scene.
3. **One editorial identity, two scene types.** Use `editorial_collage` to explain maps, routes, comparisons, costs, or concepts; use `real_life_documentary` to show people, places, food, transport, and everyday behavior. Keep palette, pacing, narration, and transitions coherent across both. Do not impose paper textures or graphics on documentary footage.
4. **Each generated clip is ~10 seconds, not exactly.** Plan scenes as ~10-second units. Assembly measures each clip's real duration and trims the final scene so total runtime lands within ±0.5 s of the requested duration.
5. **Vietnam map integrity.** Whenever a scene contains a map of Vietnam, include mainland Vietnam plus both archipelagos and apply `references/vietnam-map.md` exactly. Be honest: rendered text/labels from a video model are unreliable — verify map scenes on extracted frames and re-generate or fix labels in post if wrong.
6. **Tourist utility first.** Optimize for foreign visitors: where, why, when, cost, logistics, etiquette, transport, risks, and memorable takeaways.
7. **Do not copy Vox logos, title cards, or proprietary templates.** Use only an editorial paper-collage aesthetic inspired by explanatory journalism.
8. **Honesty about generation.** Never claim a clip was generated, accepted, or downloaded unless the `media.generate_video` tool actually returned a finished result. There is no preflight check; rollout gating is possible; the tool result is the only signal of success.
9. **You cannot watch clips back.** The assistant has no video playback. Accept a scene only after ffmpeg frame extraction or explicit user review.
10. **Specificity before spectacle.** Documentary scenes must show evidence of the named Vietnamese place and the particular behavior being explained. Avoid generic Southeast Asian backdrops, staged advertising cues, and unsupported claims that one local example represents all of Vietnam.

## Inputs

Required:
- `title`
- `duration`

Optional:
- audience segment
- platform
- aspect ratio
- destination/region
- season
- budget level
- narrator profile
- CTA

Defaults:
- audience: first-time international visitors
- platform: TikTok / YouTube Shorts
- aspect: `9:16`
- narrator: neutral international English, warm documentary-explainer
- ending: useful takeaway or soft save/follow CTA

## Workflow

### Step 1 — Normalize duration

Convert duration to seconds.

Set:
- `scene_count = ceil(total_duration_seconds / 10)`
- all non-final scenes: `usable_duration_seconds = 10`
- final scene: remainder; if remainder is `0`, use `10`

### Step 2 — Choose the travel narrative arc

Read `references/travel-story.md` and select automatically.

Defaults:
- destination guide -> `hook_orient_plan`
- mistakes/scams/warnings -> `warning_fix`
- food guide -> `taste_route`
- itinerary -> `timeboxed_route`
- etiquette -> `myth_context_behavior`
- transport -> `problem_options_choice`
- best-of list -> `ranked_utility`

### Step 3 — Write timed narration

Target spoken English per ~10-second scene:
- normal: 21–28 words
- dense fact: maximum about 30 words
- trimmed final scene: scale word count proportionally

Scene 1 must hook immediately. Avoid generic greetings and tourism-brochure filler.

### Step 4 — Design the scene sequence

Assign `scene_type` to every scene. Choose `editorial_collage` when a graphic makes a fact or relationship clearer. Choose `real_life_documentary` when viewers need to see what an experience actually looks and feels like. Alternate for the story's needs; no fixed ratio is required.

For collage scenes, read `references/vox-travel-style.md`. Include:
- one information goal
- one dominant visual subject/metaphor
- one 2–6 word English headline
- one camera move
- 2–5 paper-native element motions
- consistent palette/print texture
- restrained text density

For documentary scenes, read `references/realistic-travel-scenes.md` and follow its 11-step framework in order. Establish location, observable cultural behavior, environmental evidence, human action and feasible micro-actions. Specify context-appropriate clothing, camera, lighting, natural sound, cultural/geographic QA, continuity, and a scene-specific negative prompt. A `headline` may be kept as JSON planning metadata without appearing in the generated footage; use `overlay_text: []` unless on-screen explanation is needed.

If any scene visibly depicts Vietnamese money, read `references/vietnam-currency.md` first: avoid banknote close-ups, set `shows_currency: true` with an exact `currency_detail`, and add currency negatives to the prompt. The portrait of Hồ Chí Minh must never be distorted or disrespected.

### Step 5 — Build the project JSON

Read `references/muse-video-schema.md` and emit one project object with ordered `scenes`.

Each scene is one ~10-second generation unit. Build `video_prompt` from the guidance for its `scene_type`. `video_prompt` is verbatim text sent to `media.generate_video` — the tool may expand it, so every factual requirement (place, behavior, map anchors, key negatives) must live inside the text itself. Collage prompts specify subject, action, composition, one camera move, paper-layer motion, lighting/palette, stable English explanatory text, and a single continuous shot. Documentary prompts follow the ordered framework in `references/realistic-travel-scenes.md`; keep the visible action achievable in ~10 seconds and make the physical setting and behavior observable.

For map scenes append the required map integrity block from `references/vietnam-map.md`. Apply place and culture QA to documentary scenes even when no map appears.

### Step 6 — Validate the production JSON

Write the JSON to a project file and run:

`python3 scripts/validate_output.py <project.json>`

Fix all errors before generating anything.

### Step 7 — Generate the TTS voiceover

Read `references/voiceover.md` first. Voiceover runs right after validation because it does not depend on the video.

Run:

`python3 scripts/make_voiceover.py out/<project-slug>/project.json`

This synthesizes each scene's `narration` (spoken form) with the TTS CLI using the project's `narrator_voice` (default `avocado_v2:MAI_01`, Warm), writes `voiceover_001.mp3`, `voiceover_002.mp3`, … plus `manifest.json` into `out/<project-slug>/voiceover/`, and verifies each file fits its scene (`duration <= usable_duration_seconds + 0.5 s`).

If a voiceover is too long: shorten that scene's narration text and re-run. Do not raise TTS speed above 105. On TTS failure, retry the identical request on the bounded ladder (~5m / ~10m / ~30m / ~1h); never switch voices or engines. After the ~1h retry still fails, stop and report.

If the project sets `voiceover: false`, skip this step; assembly will keep the clips' original audio.

### Step 8 — Generate every scene with Muse video

Read `references/muse-production.md` first.

For each scene in ascending scene order, call `media.generate_video` with the scene's `video_prompt` as the text entry, `output_dir` set to `out/<project-slug>/clips`, and `name` set to the zero-padded `scene_NNN`. Use `resume_from_snapshot_id` for direct continuity where the scene's continuity notes require it. Record the returned clip path and snapshot id per scene before moving on. Do not reorder scenes.

If the tool reports unavailability or gating, stop cleanly after producing validated JSON and explain that generation could not run. Do not pretend to have generated anything.

### Step 9 — Accept clips via frame QA

Run the frame QA system:

`python3 scripts/qa_frames.py out/<project-slug>/project.json out/<project-slug>/clips out/<project-slug>/qa`

Review per `references/frame-qa.md`: 5 frames per scene against the generated checklist (location cues, visible behavior, hands/contact, identity stability, negatives, map correctness), cross-scene continuity where required, verdict `accept`/`regenerate` recorded in `qa/qa_report.json`. Re-generate only on material defects. Frames cannot judge motion smoothness — check that separately.

Then run the audio QA system (background beds are often noisy hiss):

`python3 scripts/qa_audio.py out/<project-slug>/project.json out/<project-slug>/clips out/<project-slug>/qa --voiceover-dir out/<project-slug>/voiceover`

Review per `references/audio-qa.md`: any scene with `fail` (bed < 4 dB under the voice) must be re-generated with a calmer ambience prompt or have its bed muted before assembly — do not just mix it. `warn` scenes are handled by the assembler's denoise + deep ducking. Results land in `qa/audio_report.json`.

### Step 10 — Assemble the final clip

`python3 scripts/assemble_clips.py out/<project-slug>/project.json out/<project-slug>/clips out/<project-slug>/final.mp4 --voiceover-dir out/<project-slug>/voiceover`

Assembly requirements:
- sort by scene number, never filesystem creation time
- measure each clip's real duration with ffprobe (they are only ~10 s)
- trim the final clip so total runtime matches the requested duration (±0.5 s)
- normalize all clips to the project aspect and consistent frame rate
- mix the voiceover over each scene's audio: the clip ambience is first cleaned (highpass + FFT denoise — Muse video beds are often noisy hiss) and then deep-ducked under the voice with a sidechain compressor; scenes without a voiceover file keep their original audio
- a voiceover overflowing its scene by more than +0.5 s produces a loud warning naming the scene — never cut silently
- concatenate with no unintended gaps
- encode final output as H.264 video + AAC audio in MP4

Tip: if `/tmp` is small, set `TMPDIR` to a workspace path before running the script.

### Step 11 — Final verification

Before delivery verify:
- final runtime
- scene order
- no duplicated or missing scene
- English narration and explanatory text; credible incidental Vietnamese speech/signage may appear in documentary scenes
- consistent narrator identity
- visual continuity
- map integrity wherever maps appear (verified on frames, not assumed)
- documentary location, clothing, food/props, behavior, camera, and sound when those scenes appear
- audio QA: `qa/audio_report.json` shows no `fail` (re-run with `--final` on the assembled file: no clipping, sane loudness); spot-listen to the final mix
- no generation-tool UI overlays or artifacts

Deliver:
1. `SCRIPT PLAN`
2. `PROJECT JSON`
3. generation status per scene
4. path/link to the assembled `final.mp4` if generation and assembly actually completed

## Canonical map labels

Use:
- `Hoang Sa (Paracel Islands)`
- `Truong Sa (Spratly Islands)`

Rendered labels are not guaranteed by the video model — verify visually.

## Quality bar

The result should feel like a retention-focused editorial travel explainer, not a tourism advertisement: fast hook, useful specificity, strong visual evidence, practical friction points, contextual advice, and a crisp payoff.

## Version history

- V1 (2026-10-05): TTS voiceover pipeline (`scripts/make_voiceover.py` + `references/voiceover.md`, mix with ducking in `scripts/assemble_clips.py`) + frame-based image QA system (`scripts/qa_frames.py` + `references/frame-qa.md`).
- V1.1 (2026-10-05): audio cleanup in assembler (highpass + FFT denoise on hissy Muse video beds, deep sidechain ducking ratio 20) + audio QA system for background beds and final mix (`scripts/qa_audio.py` + `references/audio-qa.md`, wired into Steps 9 and 11).
- V1.2 (2026-10-05): Vietnamese currency QA (`references/vietnam-currency.md`): `shows_currency` + `currency_detail` schema fields, validator requirement, currency checklist in `qa_frames.py`, portrait-dignity rules for Hồ Chí Minh in `frame-qa.md` (no close-ups, never distorted/disrespected).
