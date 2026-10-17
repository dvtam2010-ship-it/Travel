# Muse Video Project JSON Schema

Required project fields:

```json
{
  "title": "...",
  "total_duration_seconds": 60,
  "aspect_ratio": "9:16",
  "narrator_profile": "...",
  "narrator_voice": "avocado_v2:MAI_01",
  "voiceover": true,
  "scenes": []
}
```

`total_duration_seconds` must be positive. Scene count must equal `ceil(total_duration_seconds / 10)`.

**Voiceover fields (V1):**

- `narrator_voice`: TTS voice id for the voiceover, copied verbatim from an authoritative voice source (see `references/voiceover.md`). Default `avocado_v2:MAI_01` (Warm, Meta AI voice). Required (nonempty) when `voiceover` is true.
- `voiceover`: boolean, default `true`. When `true`, each scene's `narration` is the exact spoken text synthesized by `scripts/make_voiceover.py` and mixed over the clip audio at assembly time. When `false`, no voiceover is generated and assembly keeps the clips' original audio.
- `narration` (per scene) is the voiceover script: write it in spoken form — numbers as words ("forty-two" not "42"), abbreviations spelled out ("A P I" not "API"), times as words ("three thirty P M" not "3:30 PM"). TTS reads the text literally.

Required scene fields:

```json
{
  "scene": 1,
  "scene_type": "editorial_collage",
  "timeline": "00:00-00:10",
  "generation_duration_seconds": 10,
  "usable_duration_seconds": 10,
  "narration": "...",
  "headline": "...",
  "overlay_text": [],
  "information_goal": "...",
  "visual_subject": "...",
  "camera_move": "slow_push_in",
  "element_motion": ["..."],
  "video_prompt": "...",
  "map_integrity_required": false
}
```

`generation_duration_seconds` is the nominal 10-second Muse video unit. Actual generated clips last approximately 10 seconds — not exactly — and are measured with ffprobe at assembly time; the final clip is trimmed so the total runtime matches `total_duration_seconds` (±0.5 s).

`video_prompt` is the verbatim text sent to `media.generate_video` as the `{kind: "text"}` prompt entry. The tool may expand it, so every factual requirement (place, behavior, map anchors, load-bearing negatives) must live inside this text. The validator only checks that it is nonempty; the production runbook governs its content.

`scene_type` is `editorial_collage` or `real_life_documentary` and must be stated on every scene. There is no legacy default: a missing value fails validation.

For `editorial_collage`, keep `element_motion` as 2–5 paper-native motions and follow `vox-travel-style.md`.

For `real_life_documentary`, retain the common fields above and add:

```json
{
  "location": "Hanoi, Vietnam; morning sidewalk pho shop",
  "cultural_behavior": "A traveler seasons one bowl of pho while seated on a low sidewalk stool.",
  "environmental_evidence": ["low plastic stools and tables", "ordinary Hanoi sidewalk shopfront", "parked motorbikes"],
  "human_action": "The traveler squeezes a lime wedge into the bowl and adds fresh chili.",
  "micro_actions": ["leans toward the low table", "squeezes lime", "adds chili"],
  "wardrobe_context": "Practical casual travel clothes suited to the weather; no ceremonial costume.",
  "lighting": "Soft natural morning light with a brighter street beyond the shade.",
  "sound_design": "English narrator over restrained traffic, utensils, and indistinct Vietnamese conversation.",
  "cultural_geographic_qa": ["stool and table height support the posture", "condiments and bowl look plausible for this shop", "street details fit contemporary Hanoi"],
  "continuity_notes": "Keep the same traveler, clothes, bowl, and table position; end with chopsticks lifting noodles.",
  "negative_prompt": ["generic Southeast Asian market", "luxury restaurant", "malformed hands", "changing storefront"]
}
```

These are planning and validation fields; `video_prompt` must still contain the concrete visual and audio instructions. `headline` can be planning metadata for documentary scenes; it need not appear on screen. Prefer `overlay_text: []` for documentary footage. `element_motion` can be `[]` for documentary scenes. Keep one continuous shot and one camera move. Pace the visible action for ~10 seconds.

**Currency fields (optional, any scene type):**

```json
{
  "shows_currency": false,
  "currency_detail": ""
}
```

- `shows_currency`: boolean, default `false`. Set `true` when Vietnamese
  banknotes or coins are visibly depicted.
- `currency_detail`: required when `shows_currency` is true — name the exact
  note(s) by denomination and color, e.g. "traveler pays with a blue 20,000₫
  polymer note at a street-food stall; mid shot, note recognizable by color,
  text not legible".
- Read `references/vietnam-currency.md` before writing these: avoid close-ups
  of banknotes, and the portrait of Hồ Chí Minh must never be distorted or
  disrespected. The validator requires `currency_detail` when `shows_currency`
  is true, and `qa_frames.py` adds a currency checklist section.
