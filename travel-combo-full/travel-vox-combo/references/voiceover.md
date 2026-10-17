# Voiceover Pipeline (V1)

Default voiceover is **on** (`voiceover: true` in project JSON). The voiceover is exact word-for-word English narration, synthesized per scene with TTS and mixed over the clip audio at assembly time with ducking.

## Voice selection

- Default voice: `avocado_v2:MAI_01` (Warm, Meta AI voice) — fits the warm documentary-explainer tone.
- The user may override by naming a voice or giving a voice id. Resolve it **only** from the two authoritative sources:
  - `/opt/hatch/skills/voice-selector/voice_source.json` — copy the `id` verbatim
  - `~/workspace/user/voices.json` — copy the `voice_id` verbatim (never `saved_voice_id`)
- **Never invent a voice id.** If the requested name is ambiguous or absent from both sources, ask the user instead of guessing.
- Store the resolved id in the project's `narrator_voice` field. One narrator identity means the **same voice id for every scene**.

## Narration text in spoken form

The `narration` field of each scene **is** the voiceover script. Write it in spoken form before generating audio — TTS reads text literally:

- numbers as words: "forty-two", not "42"
- abbreviations spelled out: "A P I", not "API"
- times as words: "three thirty P M", not "3:30 PM"
- no stage directions, markup, URLs, or visual formatting

## Generating per-scene audio

Run after the project JSON is validated, before video generation (voiceover does not depend on the video):

```sh
python3 scripts/make_voiceover.py out/<project-slug>/project.json
```

What the script does per scene:
1. Reads `narration` from the scene in `project.json`.
2. Synthesizes with the TTS CLI, text via **stdin** (never embedded in the shell command):
   ```sh
   /opt/hatch/bin/tts speak --voice avocado_v2:MAI_01 \
     --output out/<slug>/voiceover/voiceover_001.mp3 --text-stdin
   ```
   with the scene's narration piped through stdin.
3. Measures each MP3 with ffprobe. The file **must** fit the scene: `duration <= usable_duration_seconds + 0.5 s`.
4. If a file is too long: **shorten the narration text** (cut filler words, split the idea across scenes) and regenerate that scene. Do not raise `--speed` above 105.
5. Writes `out/<slug>/voiceover/manifest.json` mapping each scene to its file and measured duration.

If `voiceover` is `false` in the project JSON, the script exits cleanly without generating anything and assembly keeps the clips' original audio.

## Handling TTS failures

Follow `/opt/hatch/skills/tts/SKILL.md` exactly:

- The TTS CLI already retries transient errors internally. A failure that reaches you is either exhausted retries or a permanent error.
- **Retry the exact same request later** — same text, same voice id, same engine. Never switch voices or engines because of a failure.
- Back off on a bounded ladder: **~5 minutes, then ~10 minutes, then ~30 minutes, then ~1 hour.** Schedule each retry (delayed wakeup or short cron) instead of blocking; tell the user the voiceover will arrive once synthesis recovers.
- **After the ~1-hour retry still fails: stop.** Cancel any scheduled retry, report the actual error, suggest trying again later. Do not keep rescheduling.
- Report immediately without running the ladder: auth failures and clear request errors (bad `--format`, over-long request).
- `HTTP 500 ... THERE WAS AN ERROR` is opaque: first verify every voice id character-for-character against the two authoritative sources above. If the id matches and it still fails, run the ladder with the request completely unchanged.

## Mixing at assembly

`scripts/assemble_clips.py --voiceover-dir out/<slug>/voiceover` mixes each scene's voiceover over its clip audio with **ducking** (background ambience drops to ~25% while the voice speaks). Scenes without a voiceover file keep their original audio. A voiceover slightly longer than its scene is allowed to overflow up to +0.5 s with a fade-out; anything longer produces a loud warning naming the scene instead of being cut silently.

**Audio cleanup (lesson 2026-10-05):** Muse video clip ambience is often loud broadband hiss that sits only ~5 dB under the voice and survives light ducking. The assembler therefore cleans the ambience first (`highpass=f=70` + `afftdn` FFT denoise) and then ducks it hard (sidechain ratio 20) under the voiceover. If a final mix still sounds noisy, check a spectrogram of a raw clip: persistent full-spectrum brightness means the hiss fix is working as intended and the remaining issue is likely the voice level — raise the voiceover `volume` gain rather than denoising harder.
