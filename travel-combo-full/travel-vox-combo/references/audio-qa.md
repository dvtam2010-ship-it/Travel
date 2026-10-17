# Audio QA: background beds and final mix

Muse video clips ship with synthesized ambience that is often loud broadband
hiss — sometimes only ~5 dB under the voiceover — which survives light ducking
and sounds like noise over the narration. Run audio QA at two points:

## 1. After generation, before assembly (per-scene bed check)

```sh
python3 scripts/qa_audio.py out/<slug>/project.json out/<slug>/clips out/<slug>/qa \
    --voiceover-dir out/<slug>/voiceover
```

For each scene it measures:
- **bed loudness** (integrated LUFS of the clip's audio)
- **hiss**: high-frequency (highpass 6 kHz) loudness vs full loudness — a bed
  whose HF energy sits within 15 dB of the total is flagged "hissy bed"
- **bed-vs-voice gap**: voiceover LUFS minus bed LUFS

Verdicts per scene:
- `pass` — gap ≥ 10 dB, no strong hiss. Safe to mix as-is.
- `warn` — gap 4–10 dB, or hissy bed. The assembler's denoise + deep ducking
  (see `references/voiceover.md`) is designed to handle exactly this; proceed,
  but listen to the final mix.
- `fail` — gap < 4 dB: the bed will mask the narration. Do not just mix it —
  either re-generate the clip (prompt for calmer ambience, e.g. "soft distant
  water, very quiet") or mute that scene's bed before assembly.

Results land in `qa/audio_report.json`. Exit code is 1 on any `fail`.

## 2. After assembly (final mix check)

```sh
python3 scripts/qa_audio.py out/<slug>/project.json out/<slug>/clips out/<slug>/qa \
    --voiceover-dir out/<slug>/voiceover --final out/<slug>/final.mp4
```

Checks the final mix:
- **true peak ≤ −1.0 dBFS** — above that is clipping → `fail`.
- **integrated loudness in [−30, −12] LUFS** — outside that range → `warn`
  (too quiet or too hot for web video).

## Reading the report

`qa/audio_report.json`:

```json
{
  "verdict": "pass | pass_with_warnings | fail",
  "scenes": [
    {"scene": 1, "bed_lufs": -28.1, "bed_hf_lufs": -26.0, "vo_lufs": -22.8,
     "bed_voice_gap_db": 5.3, "verdict": "warn",
     "notes": ["hissy bed (strong high-frequency noise)",
               "bed 5.3 dB under voice: denoise+duck required"]}
  ],
  "final": {"integrated_lufs": -19.4, "lra_lu": 6.1,
            "true_peak_dbfs": -2.3, "verdict": "pass", "notes": []}
}
```

## Remediation ladder

1. `warn` on beds → no action needed; the assembler already denoises
   (`highpass` + `afftdn`) and deep-ducks (sidechain ratio 20).
2. `warn` on the final mix → listen to the flagged passage; usually fixed by
   re-running assembly (deterministic) or trimming a loud bed.
3. `fail` on a bed → re-generate that scene's clip with a calmer ambience
   prompt, then re-run frame QA + audio QA for the scene.
4. `fail` on clipping → lower the voiceover `volume` gain in
   `scripts/assemble_clips.py` and re-assemble; never ship a clipping mix.

## Limits (honest)

- Numbers cannot hear: a `pass` means levels and spectra are sane, not that
  the bed sounds pleasant. Always spot-listen to the final mix.
- The hiss heuristic catches constant broadband noise; it will not catch
  garbled pseudo-speech or musical artifacts — those are caught by listening
  or, partially, by frame QA notes.
