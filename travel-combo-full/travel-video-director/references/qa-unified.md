# Khung QA thống nhất — không chồng chéo

Nguyên tắc: **mỗi hạng mục QA có đúng một chủ, kiểm đúng một lần, ở đúng một
thời điểm.** Asset đã pass cổng QA của pipeline nào thì không chấm lại bằng
cổng QA của pipeline kia.

## Bảng phân công QA

| # | Hạng mục | Chủ (file chuẩn) | Kiểm khi nào | Áp dụng |
|---|---|---|---|---|
| 1 | Fact check: số liệu, giá, giờ mở cửa — phải kiểm chứng được, không bịa | Script (M: `script-writing-travel-en.md`, V: Step 3) | Viết kịch bản; duyệt 1 lần ở GATE 1 (M) / review JSON (V) | M, V, H |
| 2 | Khớp hình–lời (anchor: named entity, thời gian, hành động, quy mô) | M: `qa-visual-match.md` → verdict match/partial/mismatch; V: `frame-qa.md` checklist → accept/regenerate | Chọn asset (M: B3 eye-check; V: Step 9 frame review) | Mỗi asset chỉ chấm **1 lần** bằng cổng của pipeline đã sinh ra nó |
| 3 | Địa danh đúng vị trí thật (tỉnh/vùng + đặc trưng nhận diện) | Một chuẩn: M `qa-geo-travel.md` §1 = V `realistic-travel-scenes.md` place check | Viết query/prompt (M: B2, V: Step 5) | M, V, H |
| 4 | Bản đồ Việt Nam: đủ Hoàng Sa + Trường Sa, đúng vị trí tương đối | **Một chuẩn duy nhất** (nội dung = V `vietnam-map.md`): mainland + Hoang Sa (Paracel) ~16.5°N 112°E + Truong Sa (Spratly) ~7–12°N 111–117°E; cấm đường lưỡi bò | Scene/shot nào có bản đồ: kiểm 1 lần trên frame/thumbnail; không kiểm lại nếu visual không đổi | M, V, H |
| 5 | Tiền tệ — số liệu: VND chuẩn, quy đổi USD theo tỷ giá hiện hành + "about" | M `qa-geo-travel.md` §3 | Viết kịch bản | M, V, H |
| 6 | Tiền tệ — hình ảnh: không close-up tiền; portrait Hồ Chí Minh dignified, không méo/móp; không tiền giả mạo | V `vietnam-currency.md` (+ `shows_currency`/`currency_detail`) | Thiết kế scene (V: Step 4–5) / chọn footage (M: B3) → frame QA | M, V, H (khi có cảnh tiền) |
| 7 | Món ăn: đúng món thật (tên, vùng miền, đặc trưng nhận diện); không footage → reference photo thật trước, image-to-video từ ref thật; cấm bịa món "gần giống" | M `qa-food-travel.md` | Chọn asset / viết prompt món ăn | M, V, H (V documentary food scenes phải reference-grounded) |
| 8 | Narrator nhất quán: một video = một voice id, xuyên suốt mọi scene/beat | V `voiceover.md` (one narrator identity) | Chốt voice id khi khởi tạo project; không đổi giữa chừng | M, V, H |
| 9 | Audio — chuẩn pass/fail duy nhất | **Một chuẩn:** bed ≥4 dB dưới voice (fail nếu <4 dB); tuyệt đối không duck ngược; master **-14 LUFS**; true peak ≤ **-1 dBFS**; spot-listen final | Ráp final | M: chain nhẹ (voice -20 LUFS, nhạc royalty-free -40 LUFS, duck ≤6 dB). V: denoise (highpass + afftdn) + deep duck vì bed AI hissy. Cùng chuẩn pass/fail |
| 10 | Gate người | M: GATE 1 (kịch bản + phân loại beat) + GATE 2 (contact sheet có cột narration) bắt buộc. V: review 5 frames/scene, accept/regenerate; gọi user review khi frames inconclusive | Theo pipeline | Giữ nguyên mỗi pipeline |
| 11 | Final verification — một checklist duy nhất | runtime đúng (±0.5s), thứ tự scene/shot đúng, không trùng/thiếu, map integrity đã pass, audio không clip, subtitle khớp lời, không watermark/logo | Trước khi giao | M, V, H |
| 12 | Chất lượng footage đầu vào (chỉ pipeline M) | Ưu tiên ≥1080p; 3 frame không mờ/nhòe; cảnh đẹp (sáng đủ, bố cục rõ); thực tế với thời điểm hiện tại (không dùng footage vài năm trước cho nội dung "hiện tại") — không đạt sau 2 lần viết lại query → `needs_ai` → render AI video | B3 chọn clip (M) | M |
| 13 | Phương án R cho `[GEN]` | Tìm ảnh bối cảnh thật (ghi provenance) → tạo ảnh AI bám sát thật nhất (kiểm side-by-side, không bịa chi tiết) → image-to-video; ảnh thật đủ đẹp thì animate trực tiếp từ ảnh thật | B4 (M) / Steps 4–9 (V) | M, V |

## Các cặp QA từng chồng chéo — nay đã gộp

- **Bản đồ:** trước đây M (`qa-geo-travel.md` §2) và V (`vietnam-map.md`) mỗi
  bên một cách viết → nay **một chuẩn duy nhất** (mục 4), kiểm một lần.
- **Tiền:** M lo "giá bao nhiêu" (mục 5), V lo "tiền trông thế nào" (mục 6) —
  hai nửa bổ sung nhau, không trùng; gom chung một mục tiền tệ.
- **Khớp hình–lời:** M chấm footage (match/partial/mismatch), V chấm scene
  gen (accept/regenerate) — cùng khái niệm anchor, khác công cụ vì khác loại
  asset; quy tắc "mỗi asset chấm 1 lần" ngăn chấm trùng.
- **Món ăn:** chỉ M có file QA riêng → nay thành chuẩn chung cho cả V (mục 7).
- **Audio:** hai chain khác nhau (nhạc royalty-free vs bed AI hissy) nhưng
  **một chuẩn pass/fail** (mục 9) — không còn hai bộ ngưỡng riêng.
- **Narrator:** chỉ V quy định chặt → nay áp dụng cho cả M (mục 8).

## Quy tắc chống trùng lặp khi chạy

1. Asset đã `accept` ở frame QA (V) thì không đem chấm lại match/partial/
   mismatch (M), và ngược lại.
2. Map đã pass kiểm frame/thumbnail thì B5/final verification chỉ xác nhận
   "không đổi", không kiểm lại từ đầu.
3. Số liệu/giá đã duyệt ở GATE 1 thì final chỉ kiểm "script không đổi".
4. Mọi video đều chạy chế độ kết hợp mặc định: beat `[FOOTAGE]` qua QA của M,
   scene `[EXPLAIN]`/`[GEN]` qua QA của V — không asset nào qua cả hai cổng.
