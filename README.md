# Travel — travel-combo-full

Bộ skill sản xuất video du lịch tiếng Anh về Việt Nam: kết hợp **footage thật**
và **AI video** trong cùng một video, điều phối **từng shot theo kịch bản**.

## Tải về

Toàn bộ skill nằm giải nén trong thư mục [`travel-combo-full/`](travel-combo-full/)
— clone hoặc download repo là dùng được (đường dẫn tương đối `../` giữa các
skill hoạt động khi ba thư mục nằm cạnh nhau).

## Thành phần (bundle V1.1, 17/10/2026)

| Skill | Phiên bản | Vai trò |
|---|---|---|
| `travel-video-director/` | V1.4 | **ĐIỀU PHỐI — đọc đầu tiên.** Phân loại từng beat `[FOOTAGE]`/`[EXPLAIN]`/`[GEN]`, khung QA thống nhất không chồng chéo |
| `travel-montage/` | V1.5 + patch Mixkit 17/10/2026 | Pipeline chính: kịch bản → săn footage thật → SEO → ráp final (retrieval-first) |
| `travel-vox-combo/` | V1.3 | Pipeline gen AI: phong cách Vox editorial, narrator nhất quán, **chuẩn bản đồ V1.1 + animation vẽ chỉ đường** |

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

## Changelog

- **V1.1 (17/10/2026):** nâng cấp bản đồ — `travel-vox-combo` lên V1.3: script
  `scripts/render_vietnam_map.py` vẽ bản đồ đẹp hơn từ dữ liệu biên giới thật
  Natural Earth 50m (ocean gradient, nước lân cận mờ, nhãn pill tự tránh đè,
  la bàn + thước tỉ lệ); **animation vẽ chỉ đường bằng code** bắt buộc cho mọi
  beat có chỉ dẫn địa lý (đường Catmull-Rom tự vẽ dần, badge số bật nảy, nhãn
  tổng km). Animation code-rendered, không phải AI.
- **V1.0 (12/10/2026):** bundle đầu tiên (director V1.4 + montage V1.5 +
  vox-combo V1.2); patch 17/10/2026: quy tắc license Mixkit.
