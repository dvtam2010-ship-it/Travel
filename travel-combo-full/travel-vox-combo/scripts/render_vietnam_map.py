#!/usr/bin/env python3
"""V1.1 Vietnam map renderer — beautiful code-drawn maps + animated route drawing.

Renders Vietnam from REAL boundary data (Natural Earth 50m via world-atlas
TopoJSON, ISO id 704). Hand-drawn polygons are BANNED. Animation is
code-rendered frame-by-frame (PIL) and encoded with ffmpeg — fully
deterministic, NO AI animation of the map (per the 12/10/2026 rule).

Usage:
  render_vietnam_map.py --places '[{"name":"Hanoi","lon":105.85,"lat":21.03},
      {"name":"Ninh Binh","lon":105.97,"lat":20.25}]' \\
      --title "VIETNAM" --subtitle "Hanoi to Ninh Binh" --out route.mp4

Outputs <out> (mp4, 1920x1080, 30fps) and a still PNG next to it.
"""
import argparse, json, math, os, subprocess, sys, urllib.request

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "WondersOfVietnamBot/1.0"}
W, H = 1920, 1080

# ---- V1.1 style palette ----
OCEAN_TOP = (13, 43, 74)       # deep navy
OCEAN_BOT = (29, 92, 138)      # lighter blue
GRATICULE = (255, 255, 255, 22)
NEIGHBOR = (74, 90, 110)       # muted neighbors
NEIGHBOR_LINE = (52, 66, 84)
VN_FILL = (242, 193, 78)       # warm amber land
VN_GLOW = (255, 236, 170)
VN_SHADOW = (0, 0, 0, 90)
ISLAND = (255, 209, 102)
ROUTE_CASING = (255, 255, 255)
ROUTE_LINE = (255, 159, 28)    # amber route
PIN = (255, 90, 60)
PILL_BG = (10, 32, 58, 235)
WHITE = (255, 255, 255)
INK = (240, 244, 248)


def font(sz, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


# ---------- boundary data ----------
def load_topojson():
    local = os.path.join(HERE, "countries-50m.json")
    if os.path.exists(local):
        return json.load(open(local))
    for url in ("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json",
                "https://unpkg.com/world-atlas@2/countries-50m.json"):
        try:
            req = urllib.request.Request(url, headers=UA)
            data = json.load(urllib.request.urlopen(req, timeout=60))
            json.dump(data, open(local, "w"))
            print("downloaded", url, flush=True)
            return data
        except Exception as e:
            print("fetch failed:", url, e, flush=True)
    sys.exit("ERROR: cannot obtain countries-50m.json")


def decode_polys(topo, ids):
    tf = topo["transform"]
    sx, sy = tf["scale"]
    tx, ty = tf["translate"]

    def decode_arc(arc):
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        return pts

    arcs = [decode_arc(a) for a in topo["arcs"]]
    geoms = topo["objects"]["countries"]["geometries"]
    out = {}
    for gid in ids:
        g = next(x for x in geoms if str(x.get("id")) == str(gid))
        polys = []
        arclists = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        for poly in arclists:
            rings = []
            for ring in poly:
                pts = []
                for idx in ring:
                    a = arcs[~idx] if idx < 0 else arcs[idx]
                    pts.extend(reversed(a) if idx < 0 else a)
                rings.append(pts)
            polys.append(rings)
        out[gid] = polys
    return out


# ---------- projection ----------
LON0, LON1, LAT0, LAT1 = 99.0, 111.5, 6.6, 23.9
_COS = math.cos(math.radians(15.5))
_KX = (W - 120) / ((LON1 - LON0) * _COS)
_KY = (H - 120) / (LAT1 - LAT0)
K = min(_KX, _KY)
_X0 = (W - (LON1 - LON0) * K * _COS) / 2
_Y0 = (H - (LAT1 - LAT0) * K) / 2


def proj(lon, lat):
    return (_X0 + (lon - LON0) * K * _COS, _Y0 + (LAT1 - lat) * K)


# ---------- base map ----------
def base_map(title, subtitle):
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    # ocean vertical gradient
    for y in range(H):
        t = y / H
        c = tuple(int(OCEAN_TOP[i] + (OCEAN_BOT[i] - OCEAN_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c + (255,))
    # vignette
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 110))
    img = Image.composite(img, black, vig)
    d = ImageDraw.Draw(img)
    # graticule every 2 deg
    lon = math.ceil(LON0)
    while lon <= LON1:
        x, _ = proj(lon, LAT1)
        if lon % 2 == 0:
            d.line([(x, 0), (x, H)], fill=GRATICULE, width=2)
        lon += 1
    lat = math.ceil(LAT0)
    while lat <= LAT1:
        _, y = proj(LON0, lat)
        if lat % 2 == 0:
            d.line([(0, y), (W, y)], fill=GRATICULE, width=2)
        lat += 1

    topo = load_topojson()
    polys = decode_polys(topo, ["704", "418", "116", "156", "764", "104"])

    def draw_poly(pid, fill, outline, width):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for poly in polys[pid]:
            for ring in poly:
                xy = [proj(lo, la) for lo, la in ring]
                ld.polygon(xy, fill=fill + (255,), outline=outline + (255,), width=width)
        return layer

    # neighbors, muted
    for nid in ["418", "116", "156", "764", "104"]:
        img = Image.alpha_composite(img, draw_poly(nid, NEIGHBOR, NEIGHBOR_LINE, 2))
    # VN drop shadow
    sh = draw_poly("704", (0, 0, 0), (0, 0, 0), 10)
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for poly in polys["704"]:
        for ring in poly:
            xy = [(x + 10, y + 14) for x, y in (proj(lo, la) for lo, la in ring)]
            sd.polygon(xy, fill=VN_SHADOW)
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    img = Image.alpha_composite(img, sh)
    # VN glow + fill + crisp coastline
    glow = draw_poly("704", VN_GLOW, VN_GLOW, 14).filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, glow)
    img = Image.alpha_composite(img, draw_poly("704", VN_FILL, WHITE, 3))

    d = ImageDraw.Draw(img)
    # Hoang Sa (Paracel) ~16.5N 112E — small cluster east of central VN
    hs = proj(112.0, 16.5)
    for dx, dy, r in [(0, 0, 9), (24, -13, 6), (-21, 17, 6), (14, 24, 5), (-27, -20, 5)]:
        x, y = hs[0] + dx, hs[1] + dy
        d.ellipse([x - r - 5, y - r - 5, x + r + 5, y + r + 5], fill=(255, 209, 102, 90))
        d.ellipse([x - r, y - r, x + r, y + r], fill=ISLAND + (255,), outline=WHITE + (255,), width=2)
    pill(d, hs[0] + 40, hs[1] - 66, "Hoang Sa\n(Paracel Islands)", 26)
    # Truong Sa (Spratly) dispersed 7-11.5N 111.5-116.5E
    import random
    random.seed(7)
    for _ in range(14):
        x, y = proj(random.uniform(111.5, 116.5), random.uniform(7.5, 11.5))
        r = 5
        d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=(255, 209, 102, 90))
        d.ellipse([x - r, y - r, x + r, y + r], fill=ISLAND + (255,), outline=WHITE + (255,), width=2)
    ts = proj(114.0, 8.6)
    pill(d, ts[0] - 320, ts[1] + 30, "Truong Sa\n(Spratly Islands)", 26)

    # title block
    d.text((70, 56), title.upper(), fill=WHITE + (255,), font=font(64, bold=True))
    if subtitle:
        d.text((72, 140), subtitle, fill=(255, 255, 255, 200), font=font(34))
    d.line([(70, 200), (70 + 300, 200)], fill=ROUTE_LINE + (255,), width=6)

    # compass rose
    cx, cy, cr = W - 110, 120, 44
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=WHITE + (180,), width=3)
    d.polygon([(cx, cy - cr + 8), (cx - 12, cy + 10), (cx + 12, cy + 10)], fill=WHITE + (230,))
    d.text((cx - 13, cy + 16), "N", fill=WHITE + (230,), font=font(26, bold=True))

    # scale bar (km per pixel at 15.5N)
    km_px = 111.32 * _COS / (K * _COS)
    for target in (200, 100, 50):
        wpx = target / km_px
        if wpx < 260:
            bx, by = 70, H - 70
            d.rectangle([bx, by - 8, bx + wpx, by], fill=WHITE + (230,))
            d.rectangle([bx, by - 8, bx + wpx / 2, by], fill=(10, 32, 58, 230))
            d.text((bx, by - 52), f"{target} km", fill=WHITE + (230,), font=font(28))
            break
    return img


def pill(d, x, y, text, size):
    f = font(size)
    lines = text.split("\n")
    tw = max(d.textlength(l, font=f) for l in lines)
    th = len(lines) * (size + 8)
    pad, r = 18, 16
    d.rounded_rectangle([x - pad, y - pad, x + tw + pad, y + th + pad], r, fill=PILL_BG)
    yy = y
    for l in lines:
        d.text((x, yy), l, fill=WHITE + (255,), font=f)
        yy += size + 8


def pin(d, x, y, number=None, r=30, alpha=255):
    glow = r + 14
    d.ellipse([x - glow, y - glow, x + glow, y + glow], fill=(255, 90, 60, int(70 * alpha / 255)))
    d.ellipse([x - r, y - r, x + r, y + r], fill=PIN + (alpha,), outline=WHITE + (alpha,), width=5)
    if number is not None:
        f = font(int(r * 1.05), bold=True)
        t = str(number)
        tw = d.textlength(t, font=f)
        d.text((x - tw / 2, y - r * 0.72), t, fill=WHITE + (alpha,), font=f)

# ---------- route math ----------
def haversine_km(a, b):
    R = 6371.0
    dlat = math.radians(b[1] - a[1])
    dlon = math.radians(b[0] - a[0])
    h = math.sin(dlat / 2) ** 2 + math.cos(math.radians(a[1])) * math.cos(math.radians(b[1])) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def catmull_rom(points, samples_per_leg=160):
    """Smooth curve through pixel waypoints -> list of (x, y)."""
    if len(points) == 2:
        p0, p1 = points
        return [(p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
                for t in [i / samples_per_leg for i in range(samples_per_leg + 1)]]
    P = [points[0]] + points + [points[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(samples_per_leg):
            t = j / samples_per_leg
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(points[-1])
    return out


def ease(t):
    return 1 - (1 - t) ** 3  # easeOutCubic


# ---------- animation ----------
def animate_route(places, title, subtitle, out_mp4, duration=10.0, fps=30):
    base = base_map(title, subtitle)
    px = [proj(p["lon"], p["lat"]) for p in places]
    curve = catmull_rom(px)
    total_km = sum(haversine_km((places[i]["lon"], places[i]["lat"]),
                                (places[i + 1]["lon"], places[i + 1]["lat"]))
                   for i in range(len(places) - 1))
    n = len(curve)
    nframes = int(duration * fps)
    intro, outro = int(0.9 * fps), int(1.4 * fps)
    draw_frames = nframes - intro - outro
    tmp = os.path.join(HERE, "_frames_tmp")
    os.makedirs(tmp, exist_ok=True)

    # ---- label layout with collision avoidance (computed once) ----
    _ld = ImageDraw.Draw(base)
    _fl = font(30, bold=True)
    label_pos, label_boxes = [], []

    def _overlaps(b):
        return any(not (b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3])
                   for o in label_boxes)

    for wx, wy in px:
        nm = places[len(label_pos)]["name"]
        tw = _ld.textlength(nm, font=_fl)
        cands = [(wx + 48, wy - 88), (wx - tw - 92, wy - 88), (wx + 48, wy + 48),
                 (wx - tw / 2, wy - 150), (wx - tw / 2, wy + 64), (wx + 48, wy - 40)]
        placed = None
        for lx, ly in cands:
            lx = min(max(lx, 60), W - tw - 110)
            ly = min(max(ly, 215), H - 130)
            box = (lx - 18, ly - 18, lx + tw + 18, ly + 56)
            if not _overlaps(box):
                placed = (lx, ly, box)
                break
        if placed is None:
            lx, ly = cands[0]
            lx = min(max(lx, 60), W - tw - 110)
            ly = min(max(ly, 215), H - 130)
            placed = (lx, ly, (lx - 18, ly - 18, lx + tw + 18, ly + 56))
        label_pos.append((placed[0], placed[1]))
        label_boxes.append(placed[2])

    # ---- distance pill position: longest-leg midpoint, sea side, clear of labels ----
    leg_km = [haversine_km((places[i]["lon"], places[i]["lat"]),
                           (places[i + 1]["lon"], places[i + 1]["lat"]))
              for i in range(len(places) - 1)]
    li = max(range(len(leg_km)), key=lambda i: leg_km[i])
    (x1, y1), (x2, y2) = px[li], px[li + 1]
    _mx, _my = (x1 + x2) / 2, (y1 + y2) / 2
    _dx, _dy = x2 - x1, y2 - y1
    _L = math.hypot(_dx, _dy) or 1.0
    _km_cands = [(_mx - _dy / _L * 170, _my + _dx / _L * 120),
                 (_mx + _dy / _L * 170, _my - _dx / _L * 120),
                 (_mx + 200, _my - 60), (_mx - 200, _my + 80)]
    km_xy = None
    for cx_, cy_ in _km_cands:
        box = (cx_ - 150, cy_ - 110, cx_ + 150, cy_ - 40)
        ok = (150 < cx_ < W - 200 and 280 < cy_ < H - 140 and not _overlaps(box)
              and all(math.hypot(cx_ - qx, cy_ - qy) > 110 for qx, qy in px))
        if ok:
            km_xy = (cx_, cy_)
            break
    if km_xy is None:
        km_xy = (_mx + 210, _my - 80)
    _km_fl = font(30, bold=True)
    _km_txt = f"\u2248 {int(round(total_km)):,} km".replace(",", ".")
    _km_tw = _ld.textlength(_km_txt, font=_km_fl)

    for f in range(nframes):
        img = base.copy()
        d = ImageDraw.Draw(img)
        # intro: gentle scale-in + fade from dark
        if f < intro:
            t = ease(f / intro)
            sc = 1.07 - 0.07 * t
            zw, zh = int(W * sc), int(H * sc)
            z = img.resize((zw, zh), Image.LANCZOS).crop(((zw - W) // 2, (zh - H) // 2,
                                                         (zw - W) // 2 + W, (zh - H) // 2 + H))
            dim = Image.new("RGBA", (W, H), (0, 0, 0, int(120 * (1 - t))))
            img = Image.alpha_composite(z.convert("RGBA"), dim)
            d = ImageDraw.Draw(img)
        else:
            df = min(f - intro, draw_frames - 1)
            frac = ease(df / max(draw_frames - 1, 1))
            k = max(2, int(n * frac))
            seg = curve[:k]
            if len(seg) > 1:
                d.line(seg, fill=ROUTE_CASING + (255,), width=15, joint="curve")
                d.line(seg, fill=ROUTE_LINE + (255,), width=8, joint="curve")
            # head dot + pulses
            hx, hy = seg[-1]
            ph = (f * 0.12) % 1.0
            for pr, al in ((46, 90), (30, 140)):
                rr = pr * (0.5 + ph)
                d.ellipse([hx - rr, hy - rr, hx + rr, hy + rr],
                          outline=(255, 255, 255, int(al * (1 - ph))), width=4)
            pin(d, hx, hy, r=20)
            # badges pop at reached waypoints
            finished = frac >= 0.999
            for i, (wx, wy) in enumerate(px):
                reach = next((j for j, (cx_, cy_) in enumerate(curve)
                              if abs(cx_ - wx) < 3 and abs(cy_ - wy) < 3), n - 1)
                if finished:
                    pop = 1.0
                elif k >= reach:
                    since = (k - reach) / n
                    pop = min(1.0, since * 6)
                else:
                    continue
                s = 1.2 - 0.2 * (1 - pop) ** 2 if pop < 1 else 1.0
                r = int(30 * max(s, 0.01))
                pin(d, wx, wy, number=i + 1, r=r, alpha=int(255 * min(pop * 1.5, 1)))
                if pop >= 1:
                    pill(d, label_pos[i][0], label_pos[i][1], places[i]["name"], 30)
            # total distance pill (precomputed clear position)
            if frac > 0.55:
                mx, my = km_xy
                a = min(1.0, (frac - 0.55) / 0.2)
                d.rounded_rectangle([mx - _km_tw / 2 - 22, my - 100, mx + _km_tw / 2 + 22, my - 52],
                                    18, fill=(10, 32, 58, int(235 * a)))
                if a > 0.3:
                    d.text((mx - _km_tw / 2, my - 94), _km_txt,
                           fill=(255, 255, 255, int(255 * a)), font=_km_fl)
        img.convert("RGB").save(os.path.join(tmp, "f%04d.png" % f))

    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", str(fps), "-i",
           os.path.join(tmp, "f%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", "18", "-movflags", "+faststart", out_mp4]
    subprocess.run(cmd, check=True)
    still = os.path.splitext(out_mp4)[0] + ".png"
    base.copy()
    # final still = last frame look
    Image.open(os.path.join(tmp, "f%04d.png" % (nframes - 1))).save(still)
    import shutil
    shutil.rmtree(tmp)
    print("wrote", out_mp4, "and", still, "| total route ≈ %d km" % round(total_km), flush=True)
    return out_mp4, still


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--places", required=True, help="JSON list of {name, lon, lat}")
    ap.add_argument("--title", default="VIETNAM")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--out", required=True, help="output mp4 path")
    ap.add_argument("--duration", type=float, default=10.0)
    ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args()
    places = json.loads(a.places)
    assert len(places) >= 2, "need at least 2 places for a route"
    animate_route(places, a.title, a.subtitle, a.out, a.duration, a.fps)


if __name__ == "__main__":
    main()
