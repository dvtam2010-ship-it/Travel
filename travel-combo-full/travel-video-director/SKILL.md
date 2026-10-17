---
name: travel-video-director
description: >
  Điều phối sản xuất video du lịch tiếng Anh về Việt Nam: MẶC ĐỊNH dùng
  travel-montage làm khung xương (kịch bản → săn footage thật → SEO → ráp
  final), từng shot/beat được phân loại [FOOTAGE] / [EXPLAIN] / [GEN] —
  beat cần đồ họa giải thích (bản đồ, tuyến đường, so sánh giá, cảnh báo)
  hoặc thiếu footage thật thì gen theo chuẩn travel-vox-combo — và áp dụng
  một khung QA thống nhất không chồng chéo (references/qa-unified.md).
  Độ dài video KHÔNG quyết định phương án. Đọc skill này TRƯỚC khi bắt đầu
  bất kỳ video du lịch nào.
metadata: { "includeInPrompt": true }
---

# Travel Video Director

> **Phiên bản: V1.4** (12/10/2026) — xem `VERSION.md`.

Skill điều phối, không thay thế 2 pipeline. Nguyên tắc cốt lõi: **M
(travel-montage) là khung xương mặc định cho mọi video** — kịch bản, shot
plan, săn footage, SEO, ráp final đều chạy pipeline M. **Từng shot/beat được
phân loại** ở khâu viết kịch bản; beat nào cần đồ họa giải thích hoặc thiếu
footage thật thì gen theo chuẩn V (travel-vox-combo). **Độ dài video không
quyết định phương án** — short 60s hay video 10 phút đều chạy cùng một khung.

Chi tiết: `references/routing.md` (phân loại shot), `references/qa-unified.md`
(khung QA không trùng).

## Hai pipeline

| | **M — travel-montage** (`../travel-montage/`) | **V — travel-vox-combo** (`../travel-vox-combo/`) |
|---|---|---|
| Triết lý | Retrieval-first: footage thật trước, AI chỉ lấp slot `needs_ai` | Generation-first: gen 100% scene bằng Muse video |
| Độ dài / format | 3–6+ phút, 16:9 (hoặc 9:16), YouTube | Short-form 30s–3 phút, 9:16 (Shorts/TikTok/Reels) |
| Phong cách | Montage du lịch, lời bình ấm áp như bạn bản địa | Vox editorial: `editorial_collage` + `real_life_documentary`, một narrator nhất quán |
| Kênh | Wonders of Vietnam | Short-form / giải thích |
| Chi phí AI | Cap $3/video, tối đa 6 video/lượt | Gen mọi scene (~10s/scene), không cap cố định |
| Gate người | GATE 1 (kịch bản) + GATE 2 (contact sheet) bắt buộc | Frame QA bằng mắt trên 5 frames/scene; user review khi frames inconclusive |
| Output | `out/<slug>/final.mp4` (1080p, không subtitle burn, -14 LUFS) + `seo.json` + `subs.srt` riêng | `out/<slug>/final.mp4` + script plan + project JSON |

## Phân loại shot — điều phối theo từng beat (không theo số phút)

Khi viết kịch bản ở B1 (pipeline M), phân loại từng beat:

- **`[FOOTAGE]` (mặc định):** beat thường, có footage thật → săn theo M
  (B2–B3). Săn 2 lần không có → chuyển sang `[GEN]`, không "chữa cháy" bằng
  clip sai.
- **`[EXPLAIN]`:** beat cần giải thích bằng đồ họa — bản đồ, tuyến đường, so
  sánh giá, cảnh báo scam, "7 mistakes", timeline → gen scene theo chuẩn V
  (`editorial_collage`, Steps 4–8 của travel-vox-combo).
- **`[GEN]`:** thiếu footage thật (nơi hẻo lánh, sự kiện quá khứ, concept trừu
  tượng), hoặc cần dãy scene có narrator/style đồng nhất tuyệt đối → gen AI
  video theo chuẩn V (`real_life_documentary` hoặc collage, Steps 4–9), áp dụng
  **phương án R**: tìm ảnh bối cảnh thật → tạo ảnh AI giống thật nhất
  (kiểm side-by-side) → image-to-video.

**Thiếu footage → sinh video AI:** B4 của M áp chuẩn gen của V — prompt chi
tiết theo framework (địa điểm, hành vi, bằng chứng môi trường, negative
prompt), **phương án R cho địa danh/bối cảnh cụ thể** (ảnh thật → ảnh AI giống
thật → video), frame QA 5 frames/scene (accept/regenerate), audio QA nếu clip có
bed. Món ăn gen AI vẫn phải qua QA món ăn (`qa-food-travel.md`):
reference-grounded, cấm bịa.

## Chế độ mặc định: kết hợp trong một video

1. Viết kịch bản chung một lần (M: B1, GATE 1) — phân loại từng beat
   `[FOOTAGE]`/`[EXPLAIN]`/`[GEN]`; chốt **một narrator voice id** cho cả video.
2. Beat `[FOOTAGE]` → M: B2–B3 săn footage, B4 fallback cho slot `needs_ai`.
3. Beat `[EXPLAIN]`/`[GEN]` → V: Steps 4–9 (scene design → project JSON →
   validate → voiceover chung → generate → frame QA + audio QA).
4. Ráp chung một lần ở B5 theo chuẩn assembly thống nhất: voice -20 LUFS,
   bed -40 LUFS nền, duck đúng chiều (không duck ngược), master -14 LUFS,
   true peak ≤ -1 dBFS, KHÔNG burn subtitle (tạo `subs.srt` riêng để upload kèm).
5. **QA không trùng:** mỗi asset chỉ qua QA của pipeline đã sinh ra nó —
   footage stock → `qa-visual-match.md` (M); scene gen → `frame-qa.md` (V).
   Không chấm lại asset đã accept bằng cổng QA kia. Final verification một
   lần theo checklist thống nhất (`qa-unified.md`).

## Khung QA thống nhất (chi tiết: references/qa-unified.md)

Mỗi hạng mục QA có đúng một "chủ" và một thời điểm kiểm duy nhất:

1. **Fact check** (số liệu, giá, giờ mở cửa): kiểm 1 lần ở khâu kịch bản
   (M: B1/GATE 1, V: Step 3). Giá: VND chuẩn + "about $X" theo tỷ giá hiện hành.
2. **Khớp hình–lời (anchor):** M chấm stock footage (match/partial/mismatch);
   V chấm generated scenes (accept/regenerate qua frame checklist). Mỗi asset
   chỉ chấm 1 lần.
3. **Địa danh đúng vị trí:** một chuẩn cho cả hai (đúng tỉnh/vùng, đúng đặc
   trưng nhận diện).
4. **Bản đồ Việt Nam:** một chuẩn duy nhất — đủ Hoàng Sa + Trường Sa, đúng
   vị trí; kiểm 1 lần trên frame/thumbnail, không kiểm lại nếu không đổi.
5. **Tiền tệ:** số liệu (VND + USD) kiểm ở script; hình ảnh tiền theo
   `vietnam-currency.md` (không close-up, portrait dignity) — áp dụng cho cả
   hai pipeline khi có cảnh tiền.
6. **Món ăn:** `qa-food-travel.md` cho cả hai — đúng món thật; V documentary
   food scenes phải reference-grounded (không bịa chi tiết món).
7. **Audio:** một chuẩn pass/fail — bed ≥4 dB dưới voice (fail nếu <4 dB),
   không duck ngược, master -14 LUFS, true peak ≤ -1 dBFS. M dùng chain nhẹ
   (nhạc royalty-free); V denoise + deep duck (bed AI hissy).
8. **Final verification:** một checklist duy nhất trước khi giao (runtime,
   thứ tự scene, map integrity, audio không clip, sub khớp).
9. **Chất lượng footage đầu vào** (chỉ M, ở B3): ưu tiên ≥1080p, 3 frame không
   mờ (upscale không cứu được clip mờ), cảnh đẹp, thực tế với thời điểm hiện
   tại — không đạt sau 2 lần viết lại query → `needs_ai` → render AI video.
10. **Phương án R cho `[GEN]`**: tìm ảnh bối cảnh thật → tạo ảnh AI bám sát
    thật nhất (kiểm side-by-side) → image-to-video; ảnh thật đủ đẹp thì
    animate trực tiếp từ ảnh thật; ghi provenance ảnh ref vào manifest.

## Quy tắc điều phối

1. Luôn bắt đầu bằng M; phân loại từng shot ở B1 (`[FOOTAGE]`/`[EXPLAIN]`/
   `[GEN]`) — không chọn pipeline theo độ dài video hay thói quen.
2. Không trộn tooling của hai pipeline trong cùng một stage (không dùng
   `assemble_clips.py` của V để ráp footage của M và ngược lại) — chỉ ráp
   chung một lần ở B5 theo chuẩn assembly thống nhất.
3. Mọi thay đổi routing/QA: analyze → propose → user duyệt rồi mới update skill.
