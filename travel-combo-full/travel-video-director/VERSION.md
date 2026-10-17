# travel-video-director — VERSION

**Phiên bản hiện tại: V1.4** — chốt ngày 12/10/2026.

## V1.4 (12/10/2026) — phương án R cho [GEN] (theo travel-montage V1.5)

- `[GEN]` áp dụng phương án R: tìm ảnh bối cảnh thật → tạo ảnh AI giống thật
  nhất (kiểm side-by-side) → image-to-video; ảnh thật đủ đẹp thì animate
  trực tiếp từ ảnh thật.
- Khung QA thống nhất thêm hạng mục 10 (phương án R).
- Cập nhật: SKILL.md (header V1.4, phân loại `[GEN]`, danh sách QA),
  `references/routing.md`.

## V1.3 (12/10/2026) — tiêu chuẩn chất lượng footage đầu vào (theo travel-montage V1.4)

- Khung QA thống nhất thêm hạng mục 12: chất lượng footage đầu vào ở B3
  (≥1080p, không mờ, cảnh đẹp, đúng thời điểm hiện tại; không đạt → `needs_ai`
  → render AI video).
- Sửa output pipeline M trong bảng so sánh: không subtitle burn (đồng bộ V1.3).
- Cập nhật: SKILL.md (header V1.3, bảng pipeline, danh sách QA), `references/qa-unified.md`.

## V1.2 (12/10/2026) — bỏ burn subtitle (theo travel-montage V1.3)

- Chuẩn assembly thống nhất: không burn subtitle vào video; tạo `subs.srt`
  riêng để upload kèm khi đăng YouTube.
- Cập nhật: SKILL.md, `references/routing.md`, SUMMARY.md.

## V1.1 (11/10/2026) — điều phối theo từng shot, M làm mặc định

- Bỏ cây quyết định theo độ dài video ("chứ không theo số phút"): mọi video
  bắt đầu bằng pipeline M làm khung xương (kịch bản → shot plan → săn
  footage → SEO → ráp final).
- Phân loại từng beat ở B1: `[FOOTAGE]` (mặc định — săn footage thật) /
  `[EXPLAIN]` (cần đồ họa giải thích: bản đồ, tuyến đường, so sánh giá, cảnh
  báo scam, "7 mistakes" → gen collage theo chuẩn V) / `[GEN]` (thiếu footage
  thật hoặc cần narrator/style đồng nhất tuyệt đối → gen AI video theo chuẩn V).
- Thiếu footage → sinh video AI: beat `[FOOTAGE]` săn 2 lần không có thì
  chuyển `[GEN]`; B4 áp chuẩn gen của V (prompt framework chi tiết, frame QA
  5 frames, audio QA); món ăn gen AI vẫn qua QA món ăn.
- Một narrator voice id cho cả video; ráp chung một lần ở B5; mỗi asset chỉ
  qua QA của pipeline đã sinh ra nó (không chấm trùng).
- Cập nhật: SKILL.md (phân loại shot + chế độ mặc định), routing.md (bảng
  phân loại beat + ví dụ kết hợp trong một video), qa-unified.md, SUMMARY.md.

## V1.0 (11/10/2026) — bản đầu tiên

- Skill điều phối 2 pipeline video du lịch tiếng Anh: `travel-montage` V1.2
  (retrieval-first) và `travel-vox-combo` V1.2 (generation-first).
- Cây quyết định chọn phương án M / V / H theo: độ dài, định dạng, nơi đăng,
  nhu cầu giải thích đồ họa, mức độ sẵn có của footage thật, ngân sách AI,
  yêu cầu chân thực.
- `references/routing.md`: bảng quy tắc nhanh + ví dụ cụ thể từng trường hợp
  + quy trình hybrid 6 bước.
- `references/qa-unified.md`: khung QA thống nhất 11 hạng mục, mỗi hạng mục
  một chủ + một thời điểm kiểm duy nhất; gộp các cặp QA từng chồng chéo
  (bản đồ, tiền tệ, khớp hình–lời, món ăn, audio, narrator).
- `SUMMARY.md`: bản tóm tắt trường hợp → phương án.
