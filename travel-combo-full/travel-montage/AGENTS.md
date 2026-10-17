# AGENTS.md — travel-montage

Entry point cho coding agent (Claude Code, Codex, ...).

## Skill này làm gì

Đọc `SKILL.md` và làm đúng workflow trong đó: từ một **chủ đề du lịch Việt Nam**
tạo **video tiếng Anh hoàn chỉnh** cho kênh Wonders of Vietnam — kịch bản EN
(`beats.json`) + SEO (`seo.json`) → shot plan (`queries.json`) → **săn footage
miễn phí** khớp từng shot (`asset_manifest.json`) → slot thiếu thì **fallback AI
trên media pipeline của Muse** (ưu tiên image-to-video) → TTS tiếng Anh + nhạc
royalty-free → `final.mp4` (ffmpeg, không burn subtitle; `subs.srt` riêng).

**Phạm vi:** `beats.json` → `queries.json` → `asset_manifest.json` → clips →
`audio/` → `final.mp4`. Không gen toàn bộ video bằng AI — AI chỉ lấp slot
`needs_ai`.

## Tài liệu cần đọc (theo thứ tự)

1. `SKILL.md` — workflow đầy đủ, nguyên tắc vàng, output contract.
2. `references/script-writing-travel-en.md` — trước khi viết kịch bản: cấu trúc
   hook/beats/CTA tiếng Anh cho khán giả nước ngoài + SEO.
3. `references/footage-sourcing.md` — trước khi săn footage: thứ tự nguồn,
   cách viết query EN, kiểm thumbnail, provenance, quy tắc đánh `needs_ai`.
4. `references/ai-fallback.md` — trước khi gen AI: image-to-video trước,
   text-to-video sau, giới hạn 2 thử/slot và 6 video/lượt.
5. `references/assembly.md` — trước khi ráp: TTS timing, nhạc ducking,
   subtitle SRT riêng (không burn), lệnh ffmpeg.
6. `references/seo-travel-en.md` — khi viết `seo.json`: title/description/tags
   cho Wonders of Vietnam.
7. `references/qa-geo-travel.md` — QA ở B1/B3/B4/B5: địa danh đúng vị trí,
   bản đồ đủ Hoàng Sa – Trường Sa, tiền tệ VND + quy đổi USD đúng tỷ giá.
8. `references/qa-visual-match.md` — trước/sau khi săn footage và gen AI:
   kiểm visual khớp đúng chi tiết narration nhắc tới (anchor → checklist →
   match/partial/mismatch).
9. `references/qa-food-travel.md` — khi shot có món ăn: đúng món thật (tên,
   vùng miền, đặc trưng nhận diện); không có footage thì tìm reference photo
   thật trước, ưu tiên image-to-video từ ref thật, cấm bịa món "gần giống".

## Quy ước

- Ngôn ngữ output: **tiếng Anh toàn bộ** (narration, subtitle, SEO). Tài liệu
  skill viết tiếng Việt.
- 2 gate bắt buộc: GATE 1 (kịch bản) và GATE 2 (footage + slot AI) — không
  bỏ qua, không gộp.
- Mọi thay đổi workflow: analyze → propose → user duyệt → mới update skill.
