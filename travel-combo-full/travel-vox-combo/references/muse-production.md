# Muse Video Production Runbook

Use this reference only for the generation stage. Generation uses the `media.generate_video` tool. There is no browser step and no Google Flow.

## Facts about the tool (do not work around them)

- Each clip lasts **approximately 10 seconds**. Duration and aspect ratio are not parameters.
- The prompt is a list of ordered entries `{kind: "text" | "image", value}`. You may pass a reference image (e.g. a style frame or a map layout sketch) as an image entry alongside the text.
- `resume_from_snapshot_id` continues generation from a previous clip's end state — use it for direct continuity when a scene must pick up exactly where the last one ended.
- `output_dir` accepts an absolute or home-relative path; `name` sets the file stem (no extension).
- Clips carry synthesized audio; describe mood, ambience, and voiceover in text. The tool takes no audio input.
- Text supplied in the prompt is copied verbatim into the generation request, but the tool may expand the prompt with its own detail. Keep every factual requirement inside your own text.
- There is no preflight check and rollout gating is possible. The tool result is the only signal of success.
- The assistant cannot view video playback.

## Preconditions

- `media.generate_video` is available in this session. If a call reports the tool as unavailable or gated, stop generation cleanly after producing validated JSON, report which scenes are still missing, and explain that generation could not run. Do not retry in a loop and do not pretend anything was generated.

## Generation procedure

For each scene in `project.json`, in ascending scene order:

1. Build the prompt entries: `[{kind: "text", value: <scene's video_prompt>}]`, plus any reference image entries the scene needs.
2. Call `media.generate_video` with:
   - `output_dir`: `out/<project-slug>/clips` (home-relative)
   - `name`: `scene_NNN` (zero-padded scene number, e.g. `scene_001`)
3. When the scene's `continuity_notes` require the same subject or setting to continue from the previous scene, pass the previous scene's returned snapshot id as `resume_from_snapshot_id`.
4. Wait for the tool result. Record the returned clip path and snapshot id for the scene before moving on.
5. Do not reorder scenes during generation.
6. Never claim a scene was generated, accepted, or downloaded unless the tool returned a finished result for it.

## Acceptance: frame-based image QA (V1)

Because you cannot watch clips back, every scene goes through the frame QA system in `references/frame-qa.md`:

```sh
python3 scripts/qa_frames.py out/<project-slug>/project.json \
  out/<project-slug>/clips out/<project-slug>/qa
```

This extracts 5 frames per scene (at 10/30/50/70/90% of real duration), builds a per-scene checklist from the project JSON, and starts `qa/qa_report.json`. Review the frames against the checklist (location cues, visible behavior, hands/contact, identity stability, negatives, map correctness), compare last-frame/first-frame across scenes where `continuity_notes` require it, and record `accept` or `regenerate` with a concrete reason per scene. Re-generate only on material defects; never for minor aesthetic differences.

**Map labels:** rendered on-screen text from a video model is unreliable. Verify archipelago positions on extracted frames against `references/vietnam-map.md`. If labels or positions are wrong, re-generate with simpler map direction, or accept the clip and add verified English labels in post.

Honesty limits: frames are stills — motion smoothness and audio quality cannot be judged from them. Listen to the voiceover MP3s and the final MP4 separately.

## Voiceover (V1 default)

Voiceover is generated **before** this stage with `scripts/make_voiceover.py` (see `references/voiceover.md`): exact word-for-word narration per scene, synthesized with TTS in the project's `narrator_voice`, mixed over clip audio with ducking at assembly time via `scripts/assemble_clips.py --voiceover-dir`.

If the project sets `voiceover: false`, no voiceover exists: the prompt's SOUND block is the only audio direction and assembly preserves the clips' original audio. This does not guarantee exact narration wording.

## Failure handling

- If the tool is unavailable or gated: stop and report the access limitation with scenes completed vs. missing.
- If a scene repeatedly fails: preserve its prompt and scene number, report it as unresolved, and do not silently skip it.
- Never fabricate a clip path or snapshot id.
- If a clip's actual duration makes the total overshoot badly, assembly trims the final clip; see the assemble script.
