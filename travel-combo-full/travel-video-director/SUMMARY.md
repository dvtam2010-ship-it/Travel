# TÓM TẮT — Phân loại shot trong một video (không theo số phút)

Nguyên tắc: **mọi video bắt đầu bằng M (travel-montage)** làm khung xương —
kịch bản, shot plan, săn footage, SEO, ráp final. **Từng beat được phân loại**
khi viết kịch bản; beat nào cần đồ họa giải thích hoặc thiếu footage thật thì
gen theo chuẩn V (travel-vox-combo).

## Ba loại shot

| Loại | Khi nào | Xử lý |
|---|---|---|
| **`[FOOTAGE]`** (mặc định) | Beat thường, có footage thật | M: B2 viết query EN → B3 săn footage (Pexels → Pixabay → Coverr/Mixkit → Wikimedia), eye-check match/partial/mismatch, ghi provenance |
| **`[EXPLAIN]`** | Cần giải thích bằng đồ họa: bản đồ, tuyến đường, so sánh giá, cảnh báo scam, "7 mistakes", timeline | V: gen `editorial_collage` (Steps 4–8), không săn footage |
| **`[GEN]`** | Thiếu footage thật (săn 2 lần không có: nơi hẻo lánh, quá khứ, concept trừu tượng) HOẶC cần dãy scene narrator/style đồng nhất tuyệt đối | V: gen AI video (Steps 4–9) — prompt chi tiết theo framework, frame QA 5 frames/scene, audio QA |

**Thiếu footage → sinh video AI:** không "chữa cháy" bằng clip sai; chuyển
beat sang `[GEN]`, gen theo chuẩn V. Món ăn gen AI phải qua QA món ăn
(reference photo thật trước, image-to-video từ ref thật, cấm bịa).

## Quy trình mặc định mọi video

1. B0–B1 (M): kịch bản EN + phân loại từng beat + SEO → **GATE 1 duyệt**
2. `[FOOTAGE]` → M: B2–B3 săn footage → **GATE 2:** contact sheet có cột narration
3. `[EXPLAIN]`/`[GEN]` → V: scene design → validate → voiceover **chung một
   voice id** → generate → frame QA + audio QA
4. B5: ráp chung một lần (voice -20 LUFS, bed -40 LUFS, duck đúng chiều,
   master -14 LUFS, KHÔNG burn subtitle — `subs.srt` riêng)
5. Final verification một lần theo checklist thống nhất

## Ví dụ

- **Hội An 5 phút (30 beats):** 24 `[FOOTAGE]` + 3 `[EXPLAIN]` (bản đồ, so sánh
  giá vé, timeline thương cảng) + 3 `[GEN]` (góc Chùa Cầu đẹp, lễ hội đèn lồng)
- **E-Visa 7 mistakes (60s Shorts):** 6/6 `[EXPLAIN]` collage
- **Itinerary 10 ngày (10 phút):** `[FOOTAGE]` cho từng điểm đến + 3 `[EXPLAIN]`
  (bản đồ hành trình, breakdown chi phí, so sánh phương tiện)

## QA không chồng chéo (ghi nhớ)

Mỗi asset chỉ qua QA của pipeline đã sinh ra nó (footage → M, scene gen → V).
Mỗi hạng mục QA một chủ + kiểm một lần: fact check ở kịch bản; bản đồ một
chuẩn duy nhất (đủ Hoàng Sa–Trường Sa); tiền tệ chia số liệu/hình ảnh; audio
một chuẩn pass/fail (bed ≥4 dB dưới voice, master -14 LUFS). Chi tiết:
`references/qa-unified.md`.
