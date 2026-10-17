# Viết kịch bản du lịch tiếng Anh (Wonders of Vietnam)

Khán giả: **khách nước ngoài** muốn du lịch Việt Nam, tiếng Anh không phải tiếng
mẹ đẻ của đa số — viết **đơn giản, rõ ràng, ấm áp**, tránh slang và thành ngữ
khó. Giọng: người bạn bản địa am hiểu, không phải giáo trình.

## Cấu trúc chuẩn (3–6 phút)

1. **HOOK (0–15s, 1 shot):** một câu hỏi hoặc sự thật gây tò mò. Không chào hỏi
   dài dòng.
   - Tốt: *"What if I told you Vietnam has a loop so beautiful, bikers call it
     the last great road trip on Earth?"*
   - Dở: *"Hello guys, welcome back to my channel. Today we will talk about..."*
2. **BEATS (mỗi shot ~10s):** mỗi beat = 1 ý hoàn chỉnh, 25–35 từ (đọc ~10s ở
   tốc độ tự nhiên). Một beat chỉ nói MỘT điều: địa danh, món ăn, mẹo, cảnh báo.
   - Luân phiên nhịp: fact → cảm xúc → mẹo thực tế → fact...
   - Số liệu phải kiểm chứng được (giá tiền, khoảng cách, giờ mở cửa) — ghi chú
     nguồn trong `visual_note` nếu cần đối chiếu.
3. **CTA (cuối, 1 shot):** một hành động duy nhất — subscribe / xem video liên
   quan. Ngắn, thân thiện.

## Quy tắc lời bình

- Thì hiện tại, câu ngắn. Mỗi beat đọc thử bằng TTS để đo thời lượng thật —
  **không đoán**.
- Tên địa danh Việt Nam: viết đúng chính tả, thêm phiên âm gợi ý trong ngoặc
  cho TTS nếu cần (ví dụ `Ha Giang (HAH ZYANG)`).
- Không bịa: lễ hội, giá cả, "best time" phải có căn cứ (kinh nghiệm kênh, nguồn
  uy tín). Không chắc → bỏ, đừng đoán.
- Cấm clickbait sai sự thật trong narration (title có thể giật tít nhưng nội
  dung phải đúng).

## beats.json

```json
[
  {
    "id": "shot_01",
    "narration_en": "What if I told you Vietnam has a loop so beautiful, bikers call it the last great road trip on Earth?",
    "duration_s": 10,
    "visual_note": "aerial winding mountain road, motorbikes"
  }
]
```

- `duration_s`: mặc định 10, chỉnh theo TTS đo thật ở B5.
- `visual_note`: gợi ý hình ảnh EN ngắn gọn — chính là nguyên liệu cho
  `build-queries.py` ở B2.

## SEO (ghi vào seo.json, chi tiết xem seo-travel-en.md)

- **Title** (≤70 ký tự): keyword chính đầu câu + yếu tố tò mò.
  Ví dụ: *"Ha Giang Loop: Vietnam's Most Epic Motorbike Route (Full Guide)"*
- **Description**: 2 dòng hook + tóm tắt + chapters + nguồn + footer kênh.
- **Tags**: 10–15 tags EN (địa danh, "vietnam travel", "things to do in...").
- **Hashtags**: 3–5 (#VietnamTravel #HaGiangLoop #WondersOfVietnam...).
