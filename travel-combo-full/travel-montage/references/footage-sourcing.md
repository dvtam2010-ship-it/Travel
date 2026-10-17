# Săn footage miễn phí (B3)

Triết lý: **footage thật trước, AI sau**. Mỗi shot trong `queries.json` đều phải
đi qua bước này trước khi được đánh `needs_ai`.

## Thứ tự nguồn (ưu tiên từ trên xuống)

1. **Pexels Video** (pexels.com) — kho lớn nhất, Pexels License (free, không cần
   attribution). API key đăng ký miễn phí.
2. **Pixabay Video** (pixabay.com) — Pixabay Content License (free, không cần
   attribution). API key miễn phí.
3. **Coverr** (coverr.co) — free, không cần key, kho nhỏ hơn nhưng chất
   lượng ổn.
4. **Mixkit** (mixkit.co) — CHỈ dùng clip có nhãn **"Stock Video Free License"**.
   Nút "Free Download" bản 720p là **Restricted License (personal use only)** —
   CẤM dùng trên YouTube/video kiếm tiền (xác minh live 12/10/2026; bản 1080p
   thương mại phải trả phí Envato). Kiểm nhãn license dưới nút download của
   TỪNG clip trước khi tải.
5. **Wikimedia Commons** (commons.wikimedia.org) — CC đủ loại, **phải kiểm tra
   từng file** (CC-BY thì ghi attribution).

## Cách viết query (tiếng Anh, cụ thể)

- Dùng **danh từ + tính từ cụ thể**, không trừu tượng:
  - Tốt: `"aerial ha giang mountain pass motorbike"`, `"vietnamese street food night market steam"`
  - Dở: `"beautiful vietnam"`, `"amazing travel"`
- Mỗi shot 2–3 query: 1 query bám sát `visual_note`, 1–2 query nới rộng
  (địa danh → vùng miền → concept chung). Ví dụ shot "phở Hà Nội":
  `"pho noodle soup hanoi"` → `"vietnamese noodle soup steam"` →
  `"asian street food bowl"`.
- Địa danh Việt Nam ít footage: thử tên tiếng Anh (`"Mekong Delta"`),
  rồi nới ra concept (`"rice boat river vietnam"`).

## Quy trình săn

1. Đọc `queries.json`. Với mỗi shot, tải **2–3 clip/query** (ưu tiên clip
   ≥1080p, ngang nếu format 16:9, dài 3–40s).
2. Trích thumbnail (ffmpeg) → **kiểm bằng mắt**: đúng địa danh/chủ thể không?
   Ánh sáng và màu có "đi" được với nhau không? (Không cần hoàn hảo — grade
   màu ở B5 sẽ thống nhất.)
   → **Kiểm license TRƯỚC khi tải bản full**: đọc nhãn license trên trang
   video của từng clip (đặc biệt Mixkit — xem mục 4 ở trên). Clip Restricted/
   personal-use-only → loại ngay. Ghi đúng tên license vào `asset_manifest.json`
   (không ghi "free" chung chung).
3. **Kiểm chuẩn chất lượng đầu vào** (xem mục dưới) — clip không đạt thì loại
   ngay, không chờ đến B5.
4. Chọn 1 clip/shot → ghi vào `asset_manifest.json`:
   `shot_id, path, provider, original_url, license, source: "stock"`.
5. Shot nào sau **2 lần viết lại query** vẫn không có clip đạt (đúng chủ thể
   + đạt chuẩn chất lượng) → đánh `"needs_ai"` trong `asset_manifest.json`,
   ghi rõ lý do quality (VD: "chỉ có footage 720p mờ", "footage 2019 đã cũ")
   để GATE 2 duyệt → B4 render AI video.

## Tiêu chuẩn chất lượng đầu vào (V1.4)

Clip stock chỉ được chọn khi đạt cả 3 nhóm tiêu chuẩn. Không đạt → loại,
không "tạm dùng".

### 1. Độ phân giải & độ nét

- Ưu tiên clip **≥1080p**. Clip thấp hơn chỉ dùng nếu upscale lên 1080p vẫn
  nét (kiểm thumbnail phóng 100%: không vỡ hạt, không nhòe).
- Kiểm **3 frame (đầu/giữa/cuối)** ở độ phân giải thật: không mờ, không
  out-of-focus, không motion blur nặng, không noise hạt to.
- Normalize ở B5 upscale lên 1080p nhưng **không cứu được clip mờ** — clip
  mờ đã bị loại ở bước này, không đem đi upscale.

### 2. Cảnh đẹp (thẩm mỹ tối thiểu)

- Ánh sáng đủ, bố cục rõ chủ thể; không rung lắc mạnh (trừ handheld có chủ ý
  mà vẫn xem được); không cháy sáng/thiếu sáng hoàn toàn.
- Không clip dính watermark/logo/chữ lạ (quy tắc cũ vẫn giữ).

### 3. Thực tế với thời điểm hiện tại

- Ưu tiên footage **upload gần đây** (kiểm ngày upload trên Pexels/Pixabay
  khi trang có hiển thị).
- Kiểm visual cues: mẫu xe, biển hiệu, thời trang, công trình — nơi nào đã
  sửa chữa/xây mới thì không dùng cảnh cũ.
- **Không dùng footage quay từ vài năm trước cho nội dung "hiện tại"**:
  khi narration nói "nowadays/hiện nay/2026" thì hình phải phản ánh hiện tại
  (diện mạo phố, biển hiệu, giá cả hiển thị trong hình...).
- Nghi ngờ tuổi footage mà không kiểm chứng được → thà đánh `needs_ai`.

## Săn qua website (khi không có API key)

Từ 10/2026 Pexels **tạm dừng cấp API key mới** — khi không có key, săn trực
tiếp qua website thay vì API (vẫn giữ nguyên thứ tự ưu tiên nguồn):

- **Pixabay website**: GET `https://pixabay.com/videos/search/<query>/` với
  desktop User-Agent (truy cập tốt, không bị chặn, không cần key). Parse link
  trang video từ kết quả → mở 2–3 trang video → lấy link MP4 trực tiếp
  (CDN `cdn.pixabay.com/video/...mp4`, ưu tiên bản large/HD) → tải về.
  License: Pixabay Content License (free commercial, không cần attribution).
  Riêng từ khóa "hoi an" đã có 19+ clip 4K/HD.
- **Pexels website**: thử `https://www.pexels.com/search/<query>/` — nếu bị
  Cloudflare chặn thì bỏ qua nguồn này, ghi chú vào manifest.
- Mọi quy tắc kiểm thumbnail, provenance, `needs_ai` vẫn áp dụng như săn
  qua API. Lịch sự với server: delay ngắn giữa các request; gặp 429 thì dừng
  scope đó và báo cáo.

## Quy tắc

- Không dùng 1 clip cho 2 shot (trừ montage cố ý, phải ghi chú).
- Không dùng clip dính watermark/logo.
- Kiểm license từng clip trước khi tải (đặc biệt Mixkit) — clip Restricted
  thì loại ngay, không "tạm dùng", không để lọt vào manifest.
- Clip người: tránh mặt rõ nét trừ khi license cho phép (Pexels/Pixabay OK).
- Không "chữa cháy" bằng clip sai chủ thể chỉ vì đẹp — sai địa danh là sai
  nội dung, thà để `needs_ai`.
- Lưu toàn bộ clip vào `clips/raw/`, normalize ở B5.
