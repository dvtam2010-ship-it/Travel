# Ráp final (B5)

## 1. Normalize clips

Mọi clip (stock + AI) về cùng chuẩn trước khi ráp:

```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -r 30 -c:v libx264 -crf 18 -preset medium \
-c:a aac clips/norm/shot_01.mp4
```

(9:16 thì `scale=1080:1920` tương tự.)

Lưu ý: normalize upscale lên 1080p nhưng **không cứu được clip mờ** — clip
không đạt chuẩn nét đã bị loại ở B3 (rule 12), không đem upscale ở đây.

## 2. TTS tiếng Anh + timing sync

- Dùng TTS skill (`/opt/hatch/skills/tts/SKILL.md`): giọng EN tự nhiên, tốc độ
  vừa phải. Mỗi beat thu riêng → đo duration thật → cập nhật `duration_s`
  trong `beats.json`.
- Cắt/nối clip theo duration TTS thật của beat đó (clip dài hơn thì cắt, ngắn
  hơn thì loop nhẹ hoặc speed 0.95–1.05 — không slow-motion lộ liễu).

## 3. Nhạc nền (ducking đúng chiều)

- Nguồn: Pixabay Music / Mixkit — royalty-free only, ghi tên track + license
  vào description video.
- Chain: voice **-20 LUFS** đều → nhạc **-40 LUFS** nền (thấp hơn voice 20dB)
  → nhạc duck theo voice (tối đa 6dB) → mix → master **-14 LUFS**.
- Tuyệt đối không duck ngược (nén voice khi nhạc lên) — lỗi đã từng gặp ở
  skill Vox cũ.

```bash
ffmpeg -i voice.wav -i music.mp3 -filter_complex \
"[1:a]volume=-20dB[m];[m][0:a]sidechaincompress=threshold=0.02:ratio=8:attack=200:release=1000[duck];\
[0:a][duck]amix=inputs=2:duration=first:dropout_transition=0[mix];\
[mix]loudnorm=I=-14:TP=-1.5:LRA=11" final-audio.m4a
```

## 4. Subtitle: file SRT riêng, KHÔNG burn vào video

- Tạo `subs.srt` tiếng Anh từ `narration_en` từng beat, canh theo timing TTS —
  file riêng để upload kèm khi đăng YouTube.
- **Không burn subtitle vào hình** (quyết định từ V1.3): `final.mp4` giữ hình
  ảnh sạch, không chữ cháy.

## 5. Ghép final + kiểm tra

```bash
# concat
ffmpeg -f concat -safe 0 -i clips.txt -c copy body.mp4
# mux audio + grade màu nhẹ thống nhất
ffmpeg -i body.mp4 -i final-audio.m4a -vf "eq=saturation=1.05:contrast=1.02" \
-c:v libx264 -crf 18 -c:a aac -shortest final.mp4
```

Kiểm tra trước khi giao: ffprobe (đúng 1080p/30fps), xem lướt toàn video
(không black frame, không clip lỗi), nghe thử (voice đều, nhạc không lấn),
`subs.srt` khớp timing lời bình.

## 6. Giao deliverable

- `final.mp4` (1080p, không subtitle burn, -14 LUFS)
- `subs.srt` (file riêng, upload kèm khi đăng YouTube)
- `seo.json` → paste lên YouTube (title/description/tags/hashtags)
- Ghi chú: track nhạc đã dùng + license để điền description
