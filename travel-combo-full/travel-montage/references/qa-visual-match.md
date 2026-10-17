# QA khớp hình–lời (visual-script match)

Mục đích: ở mọi shot, những gì khán giả **nghe** (narration) và những gì họ
**thấy** (visual) phải là cùng một câu chuyện. Nghe "airport" mà thấy cầu
đường hoàng hôn chung chung, nghe "Japanese Covered Bridge" mà thấy phố đèn
lồng — đều là fail, dù footage có đẹp.

## 1. Trích anchor từ narration (làm ở B1)

Với mỗi beat, trích từ `narration_en` các anchor và đưa vào `visual_note`:
- **Named entities**: địa danh, công trình, tên món ăn, lễ hội
  (VD: "Japanese Covered Bridge", "Lantern Festival", "cao lau")
- **Mốc thời gian/không gian**: dusk, dawn, night, rainy season, "on the coast"
- **Hành động**: walking, floating lanterns, cooking, riding
- **Quy mô/số lượng**: thousands of lanterns, dozens of boats

`visual_note` phải chứa đủ anchor — đây là "hợp đồng" để B2 viết query,
B3/B4 kiểm.

## 2. Checklist kiểm visual (B3 footage, B4 AI)

Với mỗi clip (hoặc ảnh AI), kiểm từng anchor:
1. **Named entity đúng và nhận diện được.** Lời nhắc công trình X → hình
   phải là X, không phải công trình "na ná".
2. **Thời gian/không gian khớp.** Lời nói dusk → hình không phải giữa trưa;
   lời nói "on the coast" → hình phải thấy biển.
3. **Hành động khớp.** Lời nói "release floating lanterns" → hình phải có
   người đang thả đèn, không phải phố đèn tĩnh.
4. **Quy mô khớp.** Lời nói "thousands of lanterns" → hình phải thể hiện
   số lượng lớn, không phải 1–2 chiếc.
5. **Không mâu thuẫn.** Lời nói "quiet dawn" mà hình là chợ đêm đông đúc =
   fail.
6. **Cấm thay thế "gần giống".** Không có footage đúng → viết lại query
   (tối đa 2 lần) hoặc đánh `needs_ai`. Đẹp nhưng sai còn tệ hơn xấu.

## 3. Verdict: match / partial / mismatch

- **match**: khớp toàn bộ anchor → dùng.
- **partial**: khớp phần lớn, thiếu chi tiết phụ (VD: đúng Chùa Cầu nhưng
  quay ban ngày trong khi lời nói dusk) → ghi lý do vào `match_note`,
  để user quyết ở GATE 2.
- **mismatch**: sai anchor chính → loại ngay, không dùng.

Ghi vào `asset_manifest.json` cho mỗi asset:
`visual_match: "match"|"partial"|"mismatch"`, `match_note: "..."`.
Chỉ asset `match`, hoặc `partial` được duyệt ở GATE 2, mới vào final.

## 4. GATE 2: kiểm song song hình–lời

Contact sheet mỗi shot hiển thị: thumbnail + `narration_en` + verdict +
`match_note`. User duyệt từng shot theo cặp hình–lời, không duyệt hình
riêng, lời riêng.

## 5. B5: xem lướt có bật tiếng

Trước khi giao final, xem toàn video **có bật tiếng**, kiểm từng beat:
lời đang nói gì, hình đang chiếu gì. Phát hiện lệch → thay clip hoặc
đánh lại verdict, không "để vậy cũng được".
