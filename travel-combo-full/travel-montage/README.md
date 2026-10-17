# 🎬 Travel Montage — Content du lịch Wonders of Vietnam

Biến **một chủ đề du lịch Việt Nam** thành **video tiếng Anh hoàn chỉnh**:
kịch bản EN chuẩn SEO → săn **footage miễn phí** (Pexels/Pixabay/Coverr/Mixkit/
Wikimedia) khớp từng shot → slot thiếu thì **fallback tạo video bằng AI ngay
trên Muse** (ưu tiên image-to-video: gen ảnh → upscale → animate) → TTS tiếng Anh
+ nhạc royalty-free → `final.mp4` (ffmpeg, không burn subtitle; `subs.srt` riêng).

Triết lý: **footage thật trước, AI chỉ lấp chỗ trống** — ngược với cách "gen toàn
bộ bằng AI" thường thấy.

## Cách dùng

Bạn chỉ cần đưa 3 input — **chủ đề, định dạng (16:9/9:16), thời lượng**:

> *"Làm video về Ha Giang Loop — 16:9, 4 phút."*

Agent sẽ:
1. Chạy `python3 scripts/new-project.py` → scaffold `beats.json` (~10s/shot)
2. Đọc `references/script-writing-travel-en.md` → viết kịch bản & lời bình tiếng
   Anh + SEO pack — **bạn duyệt kịch bản** (GATE 1)
3. Chạy `scripts/build-queries.py` → `queries.json` (2–3 query EN/shot)
4. Săn footage miễn phí theo `references/footage-sourcing.md`, kiểm thumbnail
   bằng mắt → `asset_manifest.json` (ghi đủ provider/URL/license) — **bạn duyệt
   contact sheet + danh sách slot cần AI** (GATE 2)
5. Fallback AI theo `references/ai-fallback.md`: image-to-video trước,
   text-to-video sau
6. Ráp final theo `references/assembly.md`: TTS EN + nhạc (ducking) → `final.mp4`
   1080p (không burn subtitle; `subs.srt` riêng để upload kèm)

## Không cần API key

- Footage: Pexels/Pixabay API key đăng ký miễn phí (có thể dùng không key với
  giới hạn thấp hơn); Coverr/Mixkit/Wikimedia không cần key.
- AI fallback: dùng media pipeline của Muse, không cần key ngoài.
- Budget guard: AI fallback cap $3/video, vượt thì hỏi trước khi gen tiếp.

## Cấu trúc

```
travel-montage/
├── SKILL.md                 workflow + nguyên tắc + output contract
├── AGENTS.md                entry point cho coding agent
├── VERSION.md               lịch sử phiên bản
├── references/
│   ├── script-writing-travel-en.md   viết kịch bản EN + SEO
│   ├── footage-sourcing.md           săn footage miễn phí
│   ├── ai-fallback.md                fallback AI trên Muse
│   ├── assembly.md                   TTS + nhạc + subtitle + ffmpeg
│   ├── seo-travel-en.md              SEO cho Wonders of Vietnam
│   ├── qa-geo-travel.md              QA địa lý – bản đồ – tiền tệ
│   ├── qa-visual-match.md            QA khớp hình–lời (match/partial/mismatch)
│   └── qa-food-travel.md             QA món ăn đúng món thật
├── scripts/
│   ├── new-project.py       scaffold project
│   └── build-queries.py     beats.json → queries.json (draft)
└── out/                     project workspace (mỗi video một thư mục)
```
