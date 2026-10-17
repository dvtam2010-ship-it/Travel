# travel-montage — VERSION

**Phiên bản hiện tại: V1.5** — chốt ngày 12/10/2026 (DINH yêu cầu thêm phương án R).

## Patch 17/10/2026 — quy tắc license Mixkit (video)

- `references/footage-sourcing.md`: tách Mixkit khỏi Coverr trong thứ tự nguồn
  (Coverr giữ vị trí 3, Mixkit xuống 4); Mixkit chỉ dùng clip nhãn "Stock Video
  Free License" — nút "Free Download" bản 720p là Restricted License (personal
  use only), cấm YouTube/monetized (xác minh live 12/10/2026; 8 clip đã bị loại
  khỏi video Tràng An vs Tam Cốc; 12 clip video Ninh Bình unlisted chờ TÂM
  quyết định xử lý).
- Thêm bước kiểm license vào "Quy trình săn" (bước 2: đọc nhãn license trên
  trang video trước khi tải bản full, ghi đúng tên license vào manifest) +
  quy tắc cứng trong mục "Quy tắc".
- Phạm vi patch: chỉ license VIDEO Mixkit (đã xác minh). Nhạc Mixkit trong
  SKILL.md rule 7 không thuộc patch này.

## V1.5 (12/10/2026) — phương án R: ảnh thật → ảnh AI giống thật → video

- Chính thức hóa phương án R (reference-grounded) trong `references/ai-fallback.md`,
  áp dụng cho mọi slot `[GEN]` (mở rộng quy trình vốn chỉ dùng cho món ăn):
  1. tìm 1–3 ảnh bối cảnh thật (Wikimedia/Flickr CC/blog uy tín, ghi provenance);
  2. tạo ảnh AI bám sát ảnh thật nhất có thể (kiểm side-by-side, không bịa chi tiết);
  3. upscale → image-to-video; ảnh thật đủ đẹp thì animate trực tiếp từ ảnh thật.
- Thứ tự ưu tiên mới: R → ảnh AI thuần (cảnh chung chung) → text-to-video
  (trừu tượng/chuyển động khó).
- QA B4: kiểm 3 frame + so side-by-side với ảnh ref thật.
- Cập nhật: SKILL.md (header V1.5, workflow B4, rule 13), `references/ai-fallback.md`.

## V1.4 (12/10/2026) — tiêu chuẩn chất lượng footage đầu vào

- Thêm mục "Tiêu chuẩn chất lượng đầu vào" trong `references/footage-sourcing.md`
  + operating rule 12 trong SKILL.md, áp dụng ở B3 trước khi chọn clip:
  - **Độ phân giải & độ nét:** ưu tiên ≥1080p; kiểm 3 frame (đầu/giữa/cuối)
    không mờ/nhòe; upscale ở B5 không cứu được clip mờ → loại từ B3.
  - **Cảnh đẹp:** sáng đủ, bố cục rõ chủ thể, không rung lắc mạnh, không
    watermark/logo.
  - **Thực tế với thời điểm hiện tại:** ưu tiên footage mới upload; kiểm
    visual cues (xe, biển hiệu, công trình); không dùng footage vài năm trước
    cho nội dung "hiện tại"; nghi ngờ thì thà `needs_ai`.
- Không đạt chuẩn sau 2 lần viết lại query → `needs_ai` (ghi rõ lý do quality)
  → B4 render AI video theo chuẩn V.
- Cập nhật: SKILL.md (header V1.4, workflow B3, rule 12),
  `references/assembly.md` (ghi chú normalize không cứu clip mờ).

## V1.3 (12/10/2026) — bỏ burn subtitle

- Không burn subtitle vào video nữa: `final.mp4` giữ hình ảnh sạch.
- Vẫn tạo `subs.srt` tiếng Anh theo timing TTS (file riêng trong `out/<slug>/`,
  upload kèm khi đăng YouTube).
- Cập nhật: SKILL.md (description, workflow B5, output contract, rule 6),
  `references/assembly.md` (§4, §6), README.md.

## Patch 12/10/2026 — quy tắc bản đồ code-drawn (sau sự cố shot_02 video Ninh Bình)

- `travel-vox-combo/references/vietnam-map.md` thêm mục "Quy tắc dựng bản đồ
  bằng code": bản đồ phải render từ dữ liệu biên giới thật (Natural Earth 50m
  qua world-atlas TopoJSON, ISO id 704), cấm vẽ polygon tay; **cấm AI animate
  bản đồ code-drawn** (image-to-video/text-to-video) — chỉ animate bằng ffmpeg
  zoompan; QA clip đã animate ở đầu/giữa/cuối, đối chiếu với PNG nguồn.
- `travel-montage/references/qa-geo-travel.md` §2 trỏ về chuẩn duy nhất
  (`vietnam-map.md`) theo khung QA thống nhất, tóm tắt các điểm bắt buộc.

## V1.2 (10/10/2026) — QA khớp hình–lời + QA món ăn

- Thêm `references/qa-visual-match.md` + nguyên tắc vàng 5 + operating rule 10:
  - Mọi visual phải thể hiện đúng thứ narration nhắc tới (named entities, mốc
    thời gian, hành động, quy mô); cấm thay thế bằng clip "gần giống".
  - B1: `visual_note` bắt buộc chứa anchor trích từ narration.
  - B3/B4: mỗi asset chấm match/partial/mismatch, ghi `visual_match` +
    `match_note` vào `asset_manifest.json`; mismatch → loại, viết lại query
    hoặc `needs_ai`; partial chờ duyệt ở GATE 2.
  - GATE 2: contact sheet có cột narration để duyệt hình–lời song song.
  - B5: xem lướt toàn video có bật tiếng, kiểm hình–lời từng beat.
- Thêm `references/qa-food-travel.md` + operating rule 11:
  - Món ăn phải đúng món thật (tên, vùng miền, đặc trưng nhận diện); không
    dùng món khác "trông giống" thay thế, không bịa.
  - Không có footage → tìm reference photo thật trước (ghi provenance,
    kiểm license), ưu tiên image-to-video từ chính ref photo thật; AI gen
    món ăn phải mô tả đặc trưng thật và đối chiếu 3 frame với ref.
  - Asset món ăn ghi thêm `food_ref: {photo_url, license}` trong manifest.

## V1.1 (09/10/2026) — QA địa lý – bản đồ – tiền tệ

- Thêm `references/qa-geo-travel.md` + operating rule 8 trong SKILL.md:
  - Địa danh đúng vị trí thật (tỉnh/vùng), visual đúng đặc trưng nhận diện
    (Hạ Long = núi đá vôi trên biển...); sai địa danh → loại, thà needs_ai.
  - Bản đồ Việt Nam bắt buộc có đầy đủ Hoàng Sa – Trường Sa; cấm bản đồ
    thiếu 2 quần đảo / đường lưỡi bò; kiểm mắt mọi frame bản đồ ở B5.
  - Tiền tệ: VND chuẩn, quy đổi USD theo tỷ giá hiện hành + chữ "about";
    giá cả phải kiểm chứng được, format nhất quán toàn video.

## V1.0 (09/10/2026) — bản đầu tiên

- Skill sản xuất video du lịch tiếng Anh cho kênh Wonders of Vietnam.
- Triết lý retrieval-first (học từ OpenMontage documentary-montage, viết lại
  hoàn toàn, không copy code AGPL): săn footage miễn phí khớp từng shot trước,
  slot nào không có mới fallback AI.
- Fallback AI ngay trên Muse (theo yêu cầu DINH): ưu tiên image-to-video
  (gen ảnh → upscale → animate), không đạt mới text-to-video; tối đa 2 lần
  thử/slot, 6 video/lượt.
- 2 gate bắt buộc: GATE 1 duyệt kịch bản EN, GATE 2 duyệt contact sheet footage
  + danh sách slot AI.
- Budget cap AI fallback: $3/video.
- Kèm SEO pack tiếng Anh (title/description/tags/hashtags) cho Wonders of Vietnam.
