# QA hình ảnh món ăn (travel)

Nguyên tắc: món ăn trên hình phải là **đúng món thật** — đúng tên, đúng vùng
miền, đúng đặc trưng nhận diện. Không dùng món khác "trông giống" để thay
thế, không bịa.

Vì sao cần QA riêng: khán giả nước ngoài xem video để nhận biết món khi đến
Việt Nam. Sai món là sai nội dung nghiêm trọng, mất uy tín kênh. Các cặp dễ
nhầm: phở vs hủ tiếu; cao lầu vs mì Quảng; bánh xèo vs bánh khọt; cà phê
trứng vs cà phê sữa đá; bún bò Huế vs bún riêu; cơm gà Hội An vs cơm tấm.

## 1. Không có footage video: tìm reference photo thật TRƯỚC

1. Tìm ảnh thật của đúng món (Wikimedia Commons, Flickr CC, food blog uy
   tín, trang của quán nổi tiếng...). Kiểm bằng mắt: đúng tên món, đúng đặc
   trưng (sợi, nước dùng, topping, cách trình bày, bát đĩa).
2. **Không bịa:** không lấy ảnh món khác gắn mác món này; không dùng ảnh AI
   tự vẽ món khi chưa có ảnh thật để đối chiếu.
3. Ghi provenance của reference photo vào `asset_manifest.json` như footage
   thường (provider, original_url, license). License ảnh phải cho phép dùng
   (CC-BY thì ghi attribution vào description video).

## 2. Từ reference photo → clip

- **Ưu tiên image-to-video từ chính reference photo thật** (animate nhẹ:
  hơi nóng bốc lên, slow push-in...) — giữ nguyên độ chính xác của món thật.
- Nếu image-to-video không đạt, gen AI món ăn: prompt phải mô tả chi tiết
  đặc trưng thật rút từ reference (loại sợi, màu nước dùng, topping, bát),
  và kiểm 3 frame (đầu/giữa/cuối) **so trực tiếp với reference photo**.
- Quy tắc B4 vẫn áp dụng: tối đa 2 lần thử/slot, 6 video/lượt, cap $3/video.

## 3. Checklist món ăn (footage, ref photo và AI đều kiểm)

1. **Đúng tên món, đúng vùng miền.** Cao lầu = Hội An; mì Quảng = Quảng Nam;
   bún bò = Huế. Lời bình nói món nào, hình phải là món đó.
2. **Đặc trưng nhận diện đúng.** VD phở bò: sợi phở dẹt, nước dùng trong,
   thịt bò thái lát, hành + rau thơm; cà phê trứng: lớp kem trứng vàng nổi
   trên mặt cốc. Thiếu đặc trưng chính = fail.
3. **Không lẫn nguyên liệu sai.** Không có chi tiết không thuộc về món
   (VD: topping kiểu món khác, bát đĩa sai vùng).
4. **Bối cảnh hợp lý.** Món đường phố thì không gian quán vỉa hè/chợ, không
   phải nhà hàng fine-dining Tây — trừ khi lời bình nói vậy.
5. **Không chữ/logo lạ** trong khung hình (kiểm như QA AI thường).

## 4. Ghi nhận

Asset món ăn trong `asset_manifest.json` thêm `food_ref` khi dùng reference
photo: `{photo_url, license}`; đồng thời chấm `visual_match`/`match_note`
theo `qa-visual-match.md` (món ăn là một anchor bắt buộc của narration).
