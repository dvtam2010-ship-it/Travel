# QA địa lý – bản đồ – tiền tệ (travel)

Áp dụng ở **B1** (số liệu trong kịch bản), **B3/B4** (visual địa danh) và **B5**
(kiểm final). Sai địa lý với khán giả nước ngoài là mất uy tín kênh.

## 1. Địa danh phải đúng vị trí

- Mọi địa danh trong narration phải đúng tỉnh/vùng thật:
  - Ví dụ: Ha Giang (Đông Bắc), Hoi An (Quảng Nam), Phu Quoc (Kiên Giang),
    Da Lat (Lâm Đồng). Không gán nhầm vùng miền.
- Visual (footage hoặc AI) phải đúng đặc trưng nhận diện của địa danh đó:
  - Vịnh Hạ Long = núi đá vôi trên biển; không lấy ảnh vịnh Thái Lan gắn mác
    Hạ Long. Ruộng bậc thang = Hoàng Su Phì/Mù Cang Chải, không phải ruộng
    đồng bằng.
- Quy tắc: footage/AI **sai địa danh → loại ngay**, thà để `needs_ai` hoặc
  viết lại query. Đẹp nhưng sai còn tệ hơn xấu.
- Khi gen ảnh AI cho địa danh cụ thể: prompt nêu rõ đặc trưng địa hình đặc
  trưng, kiểm 3 frame như qa AI thường.

## 2. Bản đồ: bắt buộc có Hoàng Sa – Trường Sa

Chuẩn duy nhất: `travel-vox-combo/references/vietnam-map.md` (theo khung QA
thống nhất, mục 4) — mọi quy tắc dựng và kiểm bản đồ nằm ở đó, không viết
riêng ở đây.

Tóm tắt các điểm bắt buộc khi review:

- Mọi bản đồ Việt Nam xuất hiện trong video (map animation, infographic, AI
  visual) **bắt buộc thể hiện đầy đủ quần đảo Hoàng Sa và Trường Sa**.
- Cấm: bản đồ thiếu 2 quần đảo, bản đồ có "đường lưỡi bò", bản đồ cắt xén
  Biển Đông sai chủ quyền.
- **Cấm AI animate bản đồ vẽ bằng code** (image-to-video/text-to-video):
  model bịa địa hình xung quanh và bóp méo hình đất nước. Bản đồ code-drawn
  chỉ animate bằng ffmpeg zoompan; xem quy tắc đầy đủ trong `vietnam-map.md`.
- Kiểm bằng mắt mọi frame có bản đồ ở B5 trước khi giao final. Phát hiện
  thiếu/sai → vẽ lại hoặc thay visual khác, không "để vậy cũng được".

## 3. Tiền tệ

- Đơn vị chuẩn: **VND** (₫ / đồng). Khi quy đổi USD cho khách nước ngoài:
  dùng **tỷ giá hiện hành tại thời điểm làm video**, luôn ghi "khoảng"
  (approx/about) — ví dụ: *"25,000 VND (about $1)"*.
- Không bịa giá: giá vé tham quan, giá món ăn, giá tour phải kiểm chứng được
  (nguồn uy tín hoặc kinh nghiệm thực tế của kênh). Không chắc → ghi
  "khoảng/từ" hoặc bỏ.
- Format nhất quán toàn video: `[số] VND (about $[số])`.
- Cấm dùng ký hiệu tiền tệ nước khác cho giá ở Việt Nam (không $ cho giá gốc,
  không ¥/€ nhầm lẫn).
