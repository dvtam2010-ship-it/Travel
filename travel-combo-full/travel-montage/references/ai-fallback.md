# Fallback AI trên Muse (B4)

Chỉ áp dụng cho slot đã đánh `needs_ai` ở B3 (đã thử săn footage 2 lần không
đạt, và đã qua GATE 2). **Không gen AI cho slot đã có footage đạt.**

Dùng media pipeline của Muse — không cần API key ngoài.

## Thứ tự ưu tiên

### Cách 1 — Phương án R: ảnh thật → ảnh AI giống thật nhất → video (làm TRƯỚC)

Phương án R (reference-grounded) — bắt buộc cho địa danh cụ thể, công trình,
món ăn, bối cảnh cần "giống thật":

1. **Tìm ảnh bối cảnh thật.** Tìm 1–3 ảnh thật của đúng địa danh/bối cảnh
   (Wikimedia Commons, Flickr CC, travel blog uy tín...). Kiểm: đúng địa danh,
   đúng đặc trưng nhận diện, đúng thời điểm. Ghi provenance (provider,
   original_url, license) vào `asset_manifest.json` như footage thường
   (CC-BY thì ghi attribution).
2. **Tạo ảnh AI giống thật nhất.** Dùng ảnh thật làm reference: đưa ảnh thật
   vào image prompt kèm ảnh ref (nếu tool hỗ trợ) hoặc mô tả chi tiết đặc
   trưng rút từ ảnh thật (địa hình, kiến trúc, màu sắc, ánh sáng, bố cục).
   Kiểm **side-by-side với ảnh thật**: địa hình/kiến trúc/màu sắc phải khớp;
   không thêm chi tiết bịa (công trình không có thật, chữ lạ...).
3. **Upscale** ảnh lên chất lượng cao nhất có thể trước khi animate.
4. **Image-to-video**: animate thành clip ~10s, motion prompt mô tả chuyển
   động camera/chủ thể nhẹ nhàng (slow push-in, gentle pan, drifting clouds...).

Lưu ý: nếu ảnh thật đã đủ đẹp và nét, **image-to-video trực tiếp từ ảnh thật**
là lựa chọn tốt nhất (xem `qa-food-travel.md` — quy trình này đã áp dụng cho
món ăn, nay mở rộng cho mọi slot `[GEN]`).

Vì sao ưu tiên R: với travel B-roll, bám ảnh thật giữ **độ chính xác địa danh**
cao nhất, ít hallucination (không tự bịa thêm chi tiết sai).

### Cách 1b — Image-to-video từ ảnh AI thuần (khi không có ảnh thật phù hợp)

Gen ảnh AI từ `visual_note` (prompt tả bố cục, ánh sáng, màu sắc; tránh chữ
trong ảnh) → upscale → image-to-video. Chỉ dùng cho cảnh chung chung, không
định danh địa danh cụ thể.

### Cách 2 — Text-to-video (khi cách 1 không đạt)

Dùng cho slot trừu tượng hoặc chuyển động khó dựng từ ảnh tĩnh: timelapse,
flyover, dòng người/phương tiện, hiệu ứng thời tiết. Prompt video: tả cảnh +
chuyển động camera + mood, cấm chữ/logo trong khung hình.

## Quy tắc

- Mỗi slot tối đa **2 lần thử** (1 lần image-to-video, 1 lần text-to-video).
  Vẫn không đạt → báo user, không cố thêm (tránh đốt budget).
- **Tối đa 6 video/lượt** (giới hạn media pipeline, tính cả video do subagent
  tạo). Slot AI nhiều hơn 6 thì chia nhiều lượt, báo user trước.
- Clip AI normalize về 1080p/30fps như footage thường, ghi vào
  `asset_manifest.json` với `source: "ai"`, `provider: "muse-media"`.
- QA bằng mắt: kiểm 3 frame (đầu/giữa/cuối) — không chữ lạ, không logo, không
  chi tiết vô lý (tay thừa, chữ Hán ngẫu nhiên...); slot dùng phương án R thì
  so thêm với ảnh ref thật (side-by-side). Lỗi thì thử lại trong quota.
- Budget cap $3/video cho toàn bộ B4 — chạm cap thì dừng, hỏi user trước khi
  gen tiếp.
