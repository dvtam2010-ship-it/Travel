---
name: travel-montage
description: >
  Sản xuất video du lịch tiếng Anh cho kênh Wonders of Vietnam từ 3 input
  (chủ đề, định dạng 16:9/9:16, thời lượng): viết kịch bản & lời bình tiếng Anh
  chuẩn SEO → shot plan → săn footage MIỄN PHÍ (Pexels/Pixabay/Coverr/Mixkit/
  Wikimedia) khớp từng shot → slot nào không săn được thì fallback tạo video
  bằng media pipeline của Muse (ưu tiên image-to-video: gen ảnh → upscale →
  animate) → TTS tiếng Anh + nhạc royalty-free → final.mp4
  (ffmpeg). Triết lý: footage thật trước, AI chỉ lấp chỗ trống.
metadata: { "includeInPrompt": true }
---

# Travel Montage — Content du lịch Wonders of Vietnam

> **Phiên bản: V1.5** (12/10/2026) — xem `VERSION.md` để biết nội dung từng bản.

Từ một chủ đề du lịch Việt Nam → kịch bản tiếng Anh → shot plan → **săn footage
miễn phí** khớp từng shot → slot thiếu thì **fallback AI ngay trên Muse** (ưu tiên
image-to-video) → TTS tiếng Anh + nhạc royalty-free → `final.mp4` (không burn
subtitle; file `subs.srt` riêng để upload kèm).

Ý tưởng retrieval-first học từ OpenMontage (pipeline documentary-montage), viết
lại hoàn toàn cho cách làm của mình — không copy code AGPL của họ.

## Nguyên tắc vàng (bất khả xâm phạm)

1. **Footage thật trước, AI sau.** Mọi slot đều phải thử săn footage miễn phí
   trước (tối đa 2 lần viết lại query). Chỉ slot gắn `needs_ai` mới được dùng AI.
2. **Provenance bắt buộc.** Mỗi asset ghi đủ `provider`, `original_url`, `license`
   trong `asset_manifest.json`. Không rõ license thì không dùng.
3. **Mắt người là gate cuối.** Contact sheet footage và danh sách slot AI đều phải
   qua user duyệt trước khi ráp.
4. **Budget.** AI fallback cap **$3/video** (mặc định). Vượt cap thì dừng và hỏi.
5. **Hình phải khớp lời.** Mọi visual phải thể hiện đúng thứ narration nhắc tới
   (địa danh, món ăn, thời gian, hành động, quy mô) — xem
   `references/qa-visual-match.md`. Sai chi tiết thì loại, không "chữa cháy"
   bằng clip gần giống.

## Workflow chuẩn

```
INPUT của user: CHỦ ĐỀ + ĐỊNH DẠNG (16:9 / 9:16) + THỜI LƯỢNG (mặc định 3–6 phút)
  │
  ├─ B0. khởi tạo   python3 scripts/new-project.py   (tương tác hoặc args)
  │                 → out/<slug>/PROJECT.md + beats.json (scaffold, ~10s/shot)
  │
  ├─ B1. kịch bản   đọc references/script-writing-travel-en.md
  │                 → beats.json: hook + narration EN từng shot + CTA
  │                 → visual_note chứa anchor trích từ narration
  │                   (địa danh, mốc thời gian, hành động, quy mô)
  │                 → seo.json: title, description, tags, hashtags
  │                                              ◀── GATE 1: user duyệt kịch bản
  │
  ├─ B2. shot plan  python3 scripts/build-queries.py out/<slug>/beats.json
  │                 → queries.json: 2–3 search query EN cho mỗi shot
  │                   (script gợi ý draft, agent hiệu đính trước khi săn)
  │
  ├─ B3. săn footage  đọc references/footage-sourcing.md
  │                   → tải 2–3 clip/query theo thứ tự ưu tiên:
  │                     Pexels → Pixabay → Coverr/Mixkit → Wikimedia Commons
  │                   → kiểm thumbnail bằng mắt: đúng địa danh + khớp lời bình
  │                     (match/partial/mismatch, xem qa-visual-match.md)
  │                   → kiểm chuẩn chất lượng đầu vào: ≥1080p (hoặc upscale
  │                     vẫn nét), không mờ, cảnh đẹp, đúng thời điểm hiện tại
  │                     → không đạt thì loại, 2 lần viết lại query không có
  │                     → "needs_ai" → B4 render AI video
  │                   → món ăn không có footage: tìm reference photo thật
  │                     trước, không bịa (xem qa-food-travel.md)
  │                   → asset_manifest.json (ghi visual_match + match_note)
  │                   → slot thất bại sau 2 lần viết lại query → "needs_ai"
  │                                              ◀── GATE 2: user duyệt contact
  │                                                   sheet (có cột narration
  │                                                   để kiểm hình–lời) +
  │                                                   danh sách slot AI
  │
  ├─ B4. fallback AI  đọc references/ai-fallback.md
  │                   → prompt AI liệt kê anchor từ narration;
  │                     món ăn AI phải dựa trên reference thật
  │                     (xem qa-food-travel.md)
  │                   → phương án R TRƯỚC: tìm ảnh bối cảnh thật → tạo ảnh AI
  │                     giống thật nhất (kiểm side-by-side với ảnh thật) →
  │                     image-to-video; không có ảnh thật phù hợp thì ảnh AI
  │                     thuần → image-to-video; không đạt mới text-to-video;
  │                     tối đa 2 lần thử/slot, tối đa 6 video/lượt
  │                     (giới hạn media pipeline)
  │
  └─ B5. ráp final  đọc references/assembly.md
                    → TTS tiếng Anh + timing sync → nhạc royalty-free
                      (ducking đúng chiều, voice luôn trên nhạc)
                    → ffmpeg 1080p final.mp4 (KHÔNG burn subtitle;
                      tạo subs.srt riêng để upload kèm)
                    → xem lướt toàn video CÓ BẬT TIẾNG, kiểm hình–lời từng beat
                    → giao SEO pack (title/description/tags)
```

## Output contract

Mỗi project `out/<slug>/` chứa:
- `PROJECT.md` — tóm tắt brief (chủ đề, format, thời lượng, số shot)
- `beats.json` — `[{id, narration_en, duration_s, visual_note}]`
- `seo.json` — `{title, description, tags[], hashtags[]}`
- `queries.json` — `[{shot_id, queries[]}]`
- `asset_manifest.json` — `[{shot_id, path, provider, original_url, license, source: "stock"|"ai", visual_match: "match"|"partial"|"mismatch", match_note, food_ref?}]`
- `clips/` — footage/AI clips đã normalize (1080p, 30fps)
- `audio/` — narration TTS + music bed
- `final.mp4` — deliverable (1080p, không subtitle burn, -14 LUFS)
- `subs.srt` — subtitle tiếng Anh theo timing TTS (file riêng, không cháy vào
  hình; upload kèm khi đăng YouTube)

## Operating rules

1. Không bỏ qua gate: GATE 1 (kịch bản) và GATE 2 (footage + slot AI) là bắt buộc.
2. Không săn footage bằng query tiếng Việt — luôn viết query tiếng Anh.
3. Không dùng clip không rõ license. Ưu tiên license không cần attribution
   (Pexels License, Pixabay Content License); CC-BY thì ghi attribution vào
   `asset_manifest.json` và description video.
4. Không gen AI cho slot đã có footage đạt — AI chỉ cho `needs_ai`.
5. Mỗi lượt media pipeline tối đa 6 video — slot AI nhiều thì chia nhiều lượt,
   báo user trước.
6. Không burn subtitle vào video. Vẫn tạo file `subs.srt` tiếng Anh theo timing
   TTS (file riêng, upload kèm khi đăng YouTube) — không cháy chữ vào hình.
7. Nhạc: royalty-free only (Pixabay Music, Mixkit...), ducking đúng chiều —
   voice -20 LUFS đều, nhạc -40 LUFS nền, duck tối đa 6dB theo voice.
8. QA địa lý – bản đồ – tiền tệ theo `references/qa-geo-travel.md`: kiểm ở B1
   (số liệu/giá), B3/B4 (visual đúng địa danh), B5 (bản đồ đủ Hoàng Sa –
   Trường Sa, tiền tệ VND + quy đổi USD theo tỷ giá hiện hành).
9. Mọi thay đổi workflow phải qua quy trình analyze → propose → user duyệt
   (quy tắc chung của DINH), rồi mới update skill.
10. QA khớp hình–lời theo `references/qa-visual-match.md`: B1 trích anchor từ
    narration vào `visual_note`; B3/B4 chấm mỗi asset match/partial/mismatch
    và ghi `visual_match` + `match_note` vào `asset_manifest.json`; mismatch
    thì loại (viết lại query hoặc `needs_ai`), partial chờ duyệt ở GATE 2;
    B5 xem lướt có bật tiếng kiểm từng beat.
11. QA món ăn theo `references/qa-food-travel.md`: đúng món thật (tên, vùng
    miền, đặc trưng nhận diện); không có footage thì tìm reference photo thật
    trước — cấm bịa món "gần giống"; ưu tiên image-to-video từ chính ref photo
    thật, AI gen món ăn phải đối chiếu ref thật; ghi provenance ref photo vào
    manifest.
12. Tiêu chuẩn chất lượng footage đầu vào (B3, xem `references/footage-sourcing.md`):
    ưu tiên ≥1080p, kiểm 3 frame không mờ/nhòe (upscale ở B5 không cứu được
    clip mờ), cảnh đẹp (sáng đủ, bố cục rõ, không rung lắc mạnh), và thực tế
    với thời điểm hiện tại (ưu tiên footage mới upload, không dùng footage vài
    năm trước cho nội dung "hiện tại"); không đạt chuẩn sau 2 lần viết lại
    query → `needs_ai` → B4 render AI video.
13. Phương án R cho slot `[GEN]` (xem `references/ai-fallback.md`): tìm ảnh bối
    cảnh thật → tạo ảnh AI bám sát ảnh thật nhất có thể (kiểm side-by-side) →
    image-to-video; ảnh thật đủ đẹp thì animate trực tiếp từ ảnh thật; ghi
    provenance ảnh ref vào manifest.
