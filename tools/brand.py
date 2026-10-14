"""World City Trail post templates — brand kit compliant.

Navy #111A28 · Mint #7AE7C7 · Teal #2F8F73 · Sand #F4EFE4
Headings: Fraunces semibold (mint italic for highlighted words) · Text: Manrope
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
NAVY = (17, 26, 40)
MINT = (122, 231, 199)
TEAL = (47, 143, 115)
SAND = (244, 239, 228)
BODY = (168, 182, 196)

FDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
F_REG = f"{FDIR}/Fraunces[SOFT,WONK,opsz,wght].ttf"
F_ITA = f"{FDIR}/Fraunces-Italic[SOFT,WONK,opsz,wght].ttf"
M_VAR = f"{FDIR}/Manrope[wght].ttf"
MARK = f"{FDIR}/mark_mint.png"

M = 96  # margin


def fraunces(size, weight=600, italic=False):
    f = ImageFont.truetype(F_ITA if italic else F_REG, size)
    # axes order: Optical Size, Weight, Softness, Wonky
    f.set_variation_by_axes([min(144, max(9, size)), weight, 0, 0])
    return f


def manrope(size, weight=500):
    f = ImageFont.truetype(M_VAR, size)
    f.set_variation_by_axes([weight])
    return f


def canvas():
    """Navy background with a soft teal glow in the lower left, as in the brand banners."""
    img = Image.new("RGB", (W, H), NAVY)
    glow = Image.new("RGB", (W // 4, H // 4), NAVY)
    g = ImageDraw.Draw(glow)
    cx, cy = int(W * 0.18 / 4), int(H * 0.80 / 4)
    for i in range(26, 0, -1):
        r = i * 13
        t = i / 26
        col = (
            int(NAVY[0] + (34 - NAVY[0]) * (1 - t) * 0.9),
            int(NAVY[1] + (74 - NAVY[1]) * (1 - t) * 0.9),
            int(NAVY[2] + (66 - NAVY[2]) * (1 - t) * 0.9),
        )
        g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.LANCZOS)
    return Image.blend(img, glow, 0.85)


def lockup(img, d):
    """Mint mark + 'World city trail' wordmark, top left."""
    mark = Image.open(MARK).convert("RGBA")
    mh = 58
    mw = int(mark.width * mh / mark.height)
    mark = mark.resize((mw, mh), Image.LANCZOS)
    img.paste(mark, (M, 74), mark)
    f = manrope(26, 600)
    x = M + mw + 22
    for i, line in enumerate(["World", "city trail"]):
        d.text((x, 76 + i * 32), line, font=f, fill=SAND)


def badge(d, text, y=76):
    """Small outlined pill, right aligned."""
    f = manrope(24, 700)
    tw = d.textlength(text, font=f)
    pad_x, h = 22, 44
    x1 = W - M
    x0 = x1 - (tw + pad_x * 2)
    d.rounded_rectangle([x0, y, x1, y + h], radius=h // 2, outline=TEAL, width=2)
    d.text((x0 + pad_x, y + 9), text, font=f, fill=MINT)


def _tokens(text, highlight):
    """Split text into (word, is_highlight) using a trailing highlight phrase."""
    if highlight and highlight in text:
        before, _, after = text.partition(highlight)
        out = [(w, False) for w in before.split()]
        out += [(w, True) for w in highlight.split()]
        out += [(w, False) for w in after.split()]
        return out
    return [(w, False) for w in text.split()]


def draw_headline(d, text, highlight, top, size, max_w, leading=1.18):
    toks = _tokens(text, highlight)
    reg, ita = fraunces(size, 600), fraunces(size, 600, italic=True)
    sp = d.textlength(" ", font=reg)
    lines, cur, cw = [], [], 0.0
    for w, hl in toks:
        f = ita if hl else reg
        ww = d.textlength(w, font=f)
        add = ww if not cur else sp + ww
        if cw + add > max_w and cur:
            lines.append(cur)
            cur, cw = [(w, hl, ww, f)], ww
        else:
            cur.append((w, hl, ww, f))
            cw += add
    if cur:
        lines.append(cur)
    y = top
    lh = size * leading
    for line in lines:
        x = M
        for i, (w, hl, ww, f) in enumerate(line):
            if i:
                x += sp
            d.text((x, y), w, font=f, fill=MINT if hl else SAND)
            x += ww
        y += lh
    return y


def fit_headline(d, text, highlight, max_w, max_h, start=86, floor=46):
    size = start
    while size > floor:
        reg = fraunces(size, 600)
        sp = d.textlength(" ", font=reg)
        toks = _tokens(text, highlight)
        n, cw = 1, 0.0
        ok = True
        for w, hl in toks:
            f = fraunces(size, 600, italic=True) if hl else reg
            ww = d.textlength(w, font=f)
            if ww > max_w:
                ok = False
                break
            add = ww if cw == 0 else sp + ww
            if cw + add > max_w:
                n += 1
                cw = ww
            else:
                cw += add
        if ok and n * size * 1.18 <= max_h:
            return size, n
        size -= 3
    return floor, 6


def body_block(d, text, top, max_w, size=40):
    f = manrope(size, 450)
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    y = top
    for l in lines:
        d.text((M, y), l, font=f, fill=BODY)
        y += size * 1.48
    return y


def footer(d, right_text):
    f = manrope(26, 500)
    d.text((M, H - 92), "worldcitytrail.com", font=f, fill=BODY)
    if right_text:
        tw = d.textlength(right_text, font=f)
        d.text((W - M - tw, H - 92), right_text, font=f, fill=BODY)


def riddle_card(path, city, question, highlight=None, cta="Answer in the comments"):
    img = canvas()
    d = ImageDraw.Draw(img)
    lockup(img, d)
    badge(d, "RIDDLE")
    max_w = W - M * 2
    size, n = fit_headline(d, question, highlight, max_w, 620, start=86)
    block = n * size * 1.18 + 54 + 40
    top = (H - block) / 2 - 20
    y = draw_headline(d, question, highlight, top, size, max_w)
    f = manrope(34, 700)
    d.text((M, y + 54), cta, font=f, fill=MINT)
    footer(d, city.upper())
    img.save(path, optimize=True)


def slide_card(path, label, counter, headline, highlight, body, cta=None):
    img = canvas()
    d = ImageDraw.Draw(img)
    lockup(img, d)
    badge(d, label.upper())
    max_w = W - M * 2
    size, n = fit_headline(d, headline, highlight, max_w, 430, start=80)
    y = draw_headline(d, headline, highlight, 390, size, max_w)
    if body:
        y = body_block(d, body, y + 46, max_w)
    if cta:
        f = manrope(34, 700)
        d.text((M, y + 30), cta, font=f, fill=MINT)
    footer(d, counter)
    img.save(path, optimize=True)
