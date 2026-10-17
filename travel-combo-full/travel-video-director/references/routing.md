# Routing — phân loại từng shot, không theo số phút

Nguyên tắc: **mọi video bắt đầu bằng pipeline M** (kịch bản → shot plan → săn
footage → SEO → ráp final). Khi viết kịch bản ở B1, phân loại **từng beat**
thành `[FOOTAGE]` / `[EXPLAIN]` / `[GEN]`. Độ dài video không quyết định
phương án.

## Bảng phân loại beat

| Tín hiệu ở từng beat | Loại | Xử lý |
|---|---|---|
| Beat thường, có footage thật (mặc định) | `[FOOTAGE]` | M: B2 viết query → B3 săn footage, eye-check, provenance |
| Cần giải thích bằng đồ họa: bản đồ, tuyến đường, so sánh giá, cảnh báo scam, "7 mistakes", timeline | `[EXPLAIN]` | V: gen `editorial_collage` (Steps 4–8) |
| Săn 2 lần không có footage: nơi hẻo lánh, sự kiện quá khứ, concept trừu tượng | `[GEN]` | V: gen AI video (Steps 4–9) theo **phương án R** — tìm ảnh bối cảnh thật → ảnh AI giống thật nhất (side-by-side) → image-to-video; áp frame QA + audio QA |
| Cần dãy scene có narrator/style đồng nhất tuyệt đối | `[GEN]` | V: gen AI với cùng voice id + continuity notes |
| Beat về món ăn | `[FOOTAGE]` ưu tiên | M: B3 săn; thiếu → `[GEN]` + QA món ăn (`qa-food-travel.md`): reference photo thật trước, image-to-video từ ref thật, cấm bịa |

## Quy tắc chuyển loại

- `[FOOTAGE]` săn 2 lần (viết lại query) vẫn không có clip đạt → chuyển thành
  `[GEN]`, ghi lý do. Không "chữa cháy" bằng clip sai chủ thể.
- `[EXPLAIN]` không bao giờ săn footage — đi thẳng sang gen collage.
- Một beat chỉ thuộc đúng một loại tại một thời điểm.

## Ví dụ: một video kết hợp nhiều loại shot

**"Hoi An: Is It Still Worth Visiting in 2026?" — 5 phút, 30 beats:**
- 24 beats `[FOOTAGE]`: phố cổ, đèn lồng, sông Hoài, chợ đêm… (săn Pexels/Pixabay)
- 3 beats `[EXPLAIN]`: bản đồ vị trí Hội An (Hoàng Sa–Trường Sa đủ), so sánh
  giá vé các điểm, timeline lịch sử thương cảng
- 3 beats `[GEN]`: Chùa Cầu góc đẹp không có footage, cảnh lễ hội đèn lồng
  full-moon không săn được clip đúng

**"Vietnam E-Visa: 7 Mistakes That Get You Rejected" — 60s Shorts:**
- 6/6 scenes `[EXPLAIN]`: mỗi lỗi một collage minh họa (không cần footage thật)

**"Ultimate 10-day Vietnam itinerary" — 10 phút:**
- Beats `[FOOTAGE]` cho từng điểm đến + 3 scenes `[EXPLAIN]` (bản đồ hành
  trình, breakdown chi phí di chuyển, so sánh tàu/xe/máy bay)

**"What is ca phe trung?" — 90s:**
- 2 beats `[FOOTAGE]` (quán cà phê Hà Nội) + 3 beats `[GEN]` (cận cảnh lớp kem
  trứng — phải reference-grounded theo QA món ăn) + 1 beat `[EXPLAIN]`
  (so sánh cà phê trứng vs cà phê sữa đá)

## Quy trình chạy (mặc định mọi video)

1. **B0–B1 (M):** scaffold project → viết kịch bản EN + phân loại từng beat
   `[FOOTAGE]`/`[EXPLAIN]`/`[GEN]` → SEO pack → **GATE 1: user duyệt kịch bản**
   (duyệt luôn phân loại beat).
2. **Beat `[FOOTAGE]` → M:** B2 build queries → B3 săn footage + eye-check
   (match/partial/mismatch) + provenance → **GATE 2:** contact sheet có cột
   narration.
3. **Beat `[EXPLAIN]`/`[GEN]` → V:** Steps 4–8 (scene design → project JSON →
   validate) → voiceover **chung một voice id** với cả video → generate →
   Step 9 frame QA (5 frames/scene, accept/regenerate) + audio QA.
4. **B5 (M):** ráp chung một lần — voice -20 LUFS, bed -40 LUFS nền, duck
   đúng chiều, master -14 LUFS, true peak ≤ -1 dBFS, KHÔNG burn subtitle
   (`subs.srt` riêng để upload kèm).
5. **Final verification** một lần theo checklist thống nhất (`qa-unified.md`).
