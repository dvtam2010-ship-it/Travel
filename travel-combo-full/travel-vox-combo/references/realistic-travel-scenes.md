# Realistic Everyday Vietnam Travel Scenes

Use for `real_life_documentary` scenes that let an international viewer see a specific travel experience. The target is observational footage with cultural and geographic evidence, not a polished food advertisement or a generic Asian street. Keep the English narrator and the overall editorial pacing of the video; let the footage itself look real.

## Prompt framework

Write the `video_prompt` in this order. Be concrete, but fit the action into one continuous generated shot of about 10 seconds.

1. **LOCATION:** Named place, venue type, time of day, and weather or season only when relevant. Use details supportable for that place; verify uncertain regional facts before treating them as requirements.
2. **CULTURAL BEHAVIOR:** The particular practice the viewer should understand. Describe one observed instance, not a universal rule about all Vietnamese people or shops.
3. **ENVIRONMENTAL EVIDENCE:** Two or three visible details that make the place and activity recognizable: layout, seating, streetscape, food, utensils, vehicles, architecture, or natural setting. Use the details that matter to the scene rather than filling the frame with stereotypes.
4. **HUMAN ACTION:** One main action with a clear beginning and result. State who does it and what physical objects they touch.
5. **MICRO-ACTIONS:** Two or three feasible gestures or reactions that support the main action. Prioritize accurate hand-object contact, posture, and natural behavior over a long list of effects.
6. **CAMERA:** One documentary camera move or a locked shot; specify framing that first proves the context and then reveals the action. Use subtle handheld motion only if it helps. Avoid dramatic or physically impossible moves.
7. **LIGHTING:** Natural light consistent with the place and time; ordinary exposure variations are acceptable. Avoid studio or fantasy lighting unless the real venue plausibly uses it.
8. **SOUND:** Keep the same English narrator profile across scenes. Describe location sound at a plausible level: traffic, conversation, utensils, weather, or other scene-specific sources. Incidental Vietnamese speech can be present without becoming an explanatory voice track. Keep music subordinate to speech and the useful ambience.
9. **CULTURAL/GEOGRAPHIC QA:** Check that clothing suits the actual activity, place, and weather; that the food, tools, service, posture, transport, buildings, terrain, season, and signage fit the named location. Do not assign ethnic or ceremonial clothing by default. For a map, also apply `vietnam-map.md`; street footage without a map does not need archipelago labels.
10. **CONTINUITY:** Specify any returning person's face, clothing, props, position, time of day, and action endpoint needed for the next scene. If there is no recurring subject, say what visual element links the cut. When a scene must pick up exactly where the previous one ended, note that generation should use `resume_from_snapshot_id` from the previous accepted scene.
11. **NEGATIVE PROMPT:** List only scene-relevant failure modes: generic or wrong regional cues, staged reactions, incorrect tools/food, broken anatomy or contact, changing identity/props, artificial lighting, text artifacts, or watermarks. Do not use negatives to erase normal local life. Remember the tool may expand the prompt: put only the most load-bearing negatives here.

Informational overlays and subtitles should be English. For documentary footage, use no generated overlay unless essential; add exact typography in post when accuracy matters. Natural Vietnamese signs may remain in the environment if credible and legible; avoid invented readable words.

## Place, clothing, and culture check

Before writing a prompt and again when reviewing its output, check the details that the scene actually claims:

- **Place:** Match the named region and venue to visible terrain, street scale, architecture, transport, and weather. A real street view needs place cues; it does not need a map or island labels.
- **Clothing:** Match ordinary clothing and footwear to the person's activity, weather, and venue. Use a helmet for a rider, suitable rainwear when rain matters, and respectful clothing where a site requires it. Do not dress contemporary people in folk or ceremonial clothing just to signal "Vietnam."
- **Food and tools:** Check ingredients, serving vessels, table height, utensils, and how the person handles them. When regional preparation varies, depict the specific stall or traveler choice instead of presenting it as a rule for every shop.
- **People:** Make the named behavior visible through posture, timing, and contact with real objects. Background people should continue their own activity without synchronized or camera-facing reactions.
- **Signage and language:** Explanatory text stays English. Incidental Vietnamese storefront text must not be a fabricated claim; if generated lettering is unstable, frame it away or add verified text later in post.
- **Continuity and sound:** Hold face, clothing, props, shop layout, daylight, and ambient sound steady within the shot. Match the end action to the next scene and keep narration intelligible.

## Ten-second production example: Hanoi sidewalk pho

This adapts the original 8-second Flow example to the skill's ~10-second Muse video unit. The key visual lesson is low sidewalk seating and the order of adding lime and fresh chili before eating. Do not require every Hanoi pho shop to look identical.

```text
Create one continuous ~10-second real-life travel documentary shot, 9:16 unless the project specifies another aspect. Natural, observational footage in contemporary Hanoi, Vietnam; no paper collage or graphic overlay.

LOCATION: Early morning at one modest sidewalk pho shop on a narrow Hanoi street. The traveler sits at a low plastic table on a low plastic stool. Nearby customers eat normally; parked motorbikes and an ordinary shopfront remain visible in the background.

CULTURAL BEHAVIOR: Show this traveler preparing a bowl of pho at low sidewalk seating: lime and sliced fresh chili go into the bowl before the first bite.

ENVIRONMENTAL EVIDENCE: Steaming ceramic bowl with rice noodles and beef, chopsticks, a small plate of lime wedges and fresh red chili, practical condiment containers, slightly worn pavement, and everyday street activity. Keep the visual clutter plausible and restrained.

HUMAN ACTION AND MICRO-ACTIONS: Start wide enough to establish the low seating and street. The traveler leans toward the bowl, squeezes one lime wedge into it, places a little fresh chili in the broth, stirs once with chopsticks, then lifts noodles at the end. Natural blinking, finger contact, posture, and irregular steam; nearby diners do not acknowledge the camera. Keep each gesture brief enough for about ten seconds.

CAMERA: Eye-level from beside the table, one slow push from a medium-wide view toward the bowl. Subtle handheld feel; no cut, orbit, drone, or excessive slow motion.

LIGHTING: Soft morning daylight; the sidewalk is slightly shaded and the road brighter. No studio lighting.

SOUND: Same warm English documentary narrator as the other scenes. Voiceover: "At this Hanoi stall, breakfast starts on a low plastic stool. Squeeze lime over the steaming bowl, add fresh chili, then lift the noodles with chopsticks." Keep low traffic, utensils, and indistinct Vietnamese conversation audible beneath the voice. No dramatic music.

CULTURAL/GEOGRAPHIC QA: Seat and table height support the traveler's posture; bowl, chopsticks, lime, and chili look usable and consistent from frame to frame. Casual clothes suit the morning weather. The street reads as contemporary Hanoi without relying on fabricated signs or generic market props.

CONTINUITY: Keep the same traveler, clothes, bowl, table, and shopfront through the shot. End on chopsticks lifting noodles to cut into a later tasting shot.

NEGATIVE PROMPT: luxury restaurant, cafe-height table, staged food commercial, people staring at camera, wrong utensils, oversized bowl, theatrical reaction, generic Southeast Asian market, malformed hands, incorrect hand-object contact, duplicated people or motorbikes, changing storefront or clothing, unstable face, CGI skin, unrealistic steam, excessive bokeh, cinematic rays, flicker, warped frames, text artifacts, watermark, logo.
```

## Acceptance check

The assistant cannot watch video playback. On extracted frames, confirm the location cues and the behavior are actually visible, the gestures are physically plausible, the subject and props stay stable, and the sound description does not promise narration the frames contradict. Reject materially wrong food, seating, clothing, geography, or hand-object interaction even when the shot looks attractive. Log the accepted asset and any unresolved limitation per scene. When frames are inconclusive, ask the user to review the clip before accepting it.
