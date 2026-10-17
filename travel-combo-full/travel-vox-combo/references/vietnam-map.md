# Vietnam Map Integrity

Whenever a Vietnam map appears, include all of the following in the visual prompt:

- Mainland Vietnam with a recognizable north-south S-shaped coastline.
- `Hoang Sa (Paracel Islands)` in the South China Sea, east of central Vietnam, visually anchored around approximately 16.5°N, 112°E.
- `Truong Sa (Spratly Islands)` as a dispersed archipelago farther south and southeast, broadly around approximately 7–12°N, 111–117°E; a label anchor near 9°N, 114°E is acceptable.

Never swap the two archipelagos, merge them into the mainland, place them in the Gulf of Thailand, or show them as one single island.

Use English labels exactly as written above.

## Honesty note for Muse video

A generative video model does not reliably render exact on-screen text or label positions. Treat map labels as a best-effort direction in the prompt, then verify on extracted frames (see `muse-production.md`). If an archipelago is mislabeled, misplaced, or missing, re-generate with simpler map direction, or accept the footage and add verified English labels in post-production. Never deliver a map with wrong islands as if it were correct.

## Quy tắc dựng bản đồ bằng code (bắt buộc, mọi pipeline)

Bài học 12/10/2026 (video Ninh Bình, shot_02): đem bản đồ vẽ bằng code cho AI
image-to-video animate → model bịa thêm địa hình "bản đồ cổ" xung quanh và bóp
méo hình Việt Nam thành khối không nhận ra ở các frame close-up. TÂM đánh giá
"vẽ sai bản đồ hoàn toàn".

- **Bản đồ phải render từ dữ liệu biên giới thật** — Natural Earth 50m qua
  world-atlas TopoJSON (`https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json`,
  decode arcs delta-encoded trong Python, ISO id `704`). **Cấm vẽ polygon tay.**
- **Cấm AI animate bản đồ code-drawn** dưới mọi hình thức (image-to-video,
  text-to-video). Animation chỉ bằng **ffmpeg zoompan** (deterministic, không
  hallucination).
- **QA clip đã animate, không chỉ frame tĩnh:** trích frame ở đầu/giữa/cuối
  clip animation, đối chiếu với PNG nguồn — hình dạng đất liền, vị trí
  Hoàng Sa/Trường Sa, label, không đường lưỡi bò, không địa hình bịa thêm.
  Frame close-up (zoom sâu nhất) vẫn phải nhận ra được Việt Nam.
