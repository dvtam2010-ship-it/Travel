# TRAVEL COMBO FULL — V1.1

Bộ skill sản xuất video du lịch tiếng Anh về Việt Nam: kết hợp **footage thật**
và **AI video** trong cùng một video, điều phối **từng shot theo kịch bản**.

## Thành phần

| Skill | Phiên bản | Vai trò |
|---|---|---|
| `travel-video-director/` | V1.4 | **ĐIỀU PHỐI — đọc đầu tiên.** Phân loại từng beat `[FOOTAGE]`/`[EXPLAIN]`/`[GEN]`, khung QA thống nhất không chồng chéo |
| `travel-montage/` | V1.5 + patch Mixkit 17/10/2026 | Pipeline chính: kịch bản → săn footage thật → SEO → ráp final (retrieval-first) |
| `travel-vox-combo/` | V1.3 | Pipeline gen AI: phong cách Vox editorial (`editorial_collage` + `real_life_documentary`), narrator nhất quán, **chuẩn bản đồ V1.1 + animation vẽ chỉ đường** |

## Cách dùng (điều phối theo kịch bản)

1. **Đọc `travel-video-director/SKILL.md` trước** mỗi video.
2. Mọi video bắt đầu bằng pipeline **M (travel-montage)**: B0 scaffold →
   B1 viết kịch bản + **phân loại từng beat**:
   - `[FOOTAGE]` (mặc định): săn footage thật (B2–B3). Chuẩn đầu vào: ≥1080p,
     không mờ, cảnh đẹp, đúng thời điểm hiện tại. Săn 2 lần không có → `[GEN]`.
   - `[EXPLAIN]`: cần đồ họa giải thích (bản đồ đủ Hoàng Sa–Trường Sa, tuyến
     đường, so sánh giá, cảnh báo scam, "7 mistakes") → gen collage chuẩn V.
   - `[GEN]`: thiếu footage thật → **phương án R**: tìm ảnh bối cảnh thật →
     tạo ảnh AI giống thật nhất (kiểm side-by-side) → image-to-video.
3. **Một narrator voice id** cho cả video. Ráp chung một lần ở B5
   (voice -20 LUFS, bed -40 LUFS, duck đúng chiều, master -14 LUFS,
   không burn subtitle — `subs.srt` riêng).
4. QA theo `travel-video-director/references/qa-unified.md`: mỗi hạng mục một
   chủ, kiểm một lần — không chồng chéo.

## Lưu ý license footage

- **Mixkit**: chỉ dùng clip có nhãn **"Stock Video Free License"**. Nút
  "Free Download" bản 720p là **Restricted License (personal use only)** —
  cấm dùng trên YouTube/video kiếm tiền. Luôn đọc nhãn license dưới nút
  download của từng clip trước khi tải.

## Cấu trúc thư mục

```
travel-combo-full/
├── README.md                    ← file này
├── travel-video-director/       ← điều phối + routing + QA thống nhất
├── travel-montage/              ← pipeline footage thật (B0–B5)
└── travel-vox-combo/            ← pipeline gen AI (Steps 1–11)
```

Ba thư mục nằm cạnh nhau để các đường dẫn tương đối `../travel-montage/` và
`../travel-vox-combo/` trong skill điều phối hoạt động đúng.

## Changelog

- **V1.1 (17/10/2026):** nâng cấp bản đồ — `travel-vox-combo` lên V1.3: script
  `scripts/render_vietnam_map.py` vẽ bản đồ Việt Nam đẹp hơn (ocean gradient,
  nước lân cận mờ, nhãn pill tự tránh đè nhau, la bàn + thước tỉ lệ) từ dữ liệu
  biên giới thật Natural Earth 50m; **animation vẽ chỉ đường bằng code**
  (đường Catmull-Rom tự vẽ dần, badge số bật nảy, nhãn tổng km) bắt buộc cho mọi
  beat có chỉ dẫn địa lý trong narration. Animation code-rendered, không phải AI
  (tuân thủ lệnh cấm AI animate bản đồ 12/10/2026). `travel-video-director`
  trỏ beat bản đồ sang script chuẩn mới.
