# Travel — travel-combo-full

Bộ skill sản xuất video du lịch tiếng Anh về Việt Nam: kết hợp **footage thật**
và **AI video** trong cùng một video, điều phối **từng shot theo kịch bản**.

## Tải về

- **[travel-combo-full-V1.0.zip](travel-combo-full-V1.0.zip)** — bundle đầy đủ,
  giải nén là dùng được.

## Thành phần

| Skill | Phiên bản | Vai trò |
|---|---|---|
| `travel-video-director/` | V1.4 | **ĐIỀU PHỐI — đọc đầu tiên.** Phân loại từng beat `[FOOTAGE]`/`[EXPLAIN]`/`[GEN]`, khung QA thống nhất không chồng chéo |
| `travel-montage/` | V1.5 + patch Mixkit 17/10/2026 | Pipeline chính: kịch bản → săn footage thật → SEO → ráp final (retrieval-first) |
| `travel-vox-combo/` | V1.2 | Pipeline gen AI: phong cách Vox editorial, narrator nhất quán |

## Cách dùng nhanh

1. Đọc `travel-video-director/SKILL.md` trước mỗi video.
2. Mọi video bắt đầu bằng pipeline M: B1 viết kịch bản + phân loại từng beat
   `[FOOTAGE]` (săn footage thật) / `[EXPLAIN]` (đồ họa giải thích: bản đồ đủ
   Hoàng Sa–Trường Sa, so sánh giá, cảnh báo) / `[GEN]` (thiếu footage →
   phương án R: ảnh thật → ảnh AI giống thật → image-to-video).
3. Một narrator voice id cho cả video; ráp chung một lần ở B5.

## Lưu ý license footage

- **Mixkit**: chỉ dùng clip nhãn **"Stock Video Free License"**. Nút
  "Free Download" 720p là **Restricted License (personal use only)** — cấm
  YouTube/monetized.
