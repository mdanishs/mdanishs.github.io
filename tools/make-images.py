"""Generate the OG share card and favicon for mdanishs.com."""

from PIL import Image, ImageDraw, ImageFont

F = "/mnt/skills/examples/canvas-design/canvas-fonts"
SERIF_B = f"{F}/Lora-Bold.ttf"
SANS = f"{F}/InstrumentSans-Regular.ttf"
SANS_B = f"{F}/InstrumentSans-Bold.ttf"

PAPER = (252, 251, 248)
INK = (28, 26, 23)
INK_SOFT = (85, 80, 74)
ACCENT = (168, 69, 29)
RULE = (228, 223, 212)

OUT = "/home/user/mdanishs.github.io/img"


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded_portrait(path, size, radius):
    src = Image.open(path).convert("RGB")
    # center-crop to square, then resize
    w, h = src.size
    s = min(w, h)
    src = src.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    src = src.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius, fill=255)
    src.putalpha(mask)
    return src


def og_card():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # accent spine
    d.rectangle([0, 0, 10, H], fill=ACCENT)

    pad_l, pad_t = 76, 82
    col_w = 640

    eyebrow = ImageFont.truetype(SANS_B, 21)
    head = ImageFont.truetype(SERIF_B, 60)
    name_f = ImageFont.truetype(SANS_B, 27)
    role_f = ImageFont.truetype(SANS, 22)

    y = pad_t
    d.text((pad_l, y), "M D A N I S H S . C O M", font=eyebrow, fill=ACCENT)
    y += 58

    for line in wrap(d, "Helping engineers land interviews in Canada and the US.", head, col_w):
        d.text((pad_l, y), line, font=head, fill=INK)
        y += 74

    y += 34
    d.line([(pad_l, y), (pad_l + 96, y)], fill=ACCENT, width=3)
    y += 40

    d.text((pad_l, y), "Mohammad Danish Siddiqui", font=name_f, fill=INK)
    y += 40
    for line in wrap(
        d,
        "Senior Frontend Engineer  ·  CDI Certified Resume Analyst",
        role_f,
        col_w,
    ):
        d.text((pad_l, y), line, font=role_f, fill=INK_SOFT)
        y += 32

    # portrait
    p = 300
    px, py = W - p - 76, (H - p) // 2
    portrait = rounded_portrait(f"{OUT}/danish.jpg", p, 26)
    d.rounded_rectangle([px - 1, py - 1, px + p, py + p], 27, outline=RULE, width=2)
    img.paste(portrait, (px, py), portrait)

    img.save(f"{OUT}/og-card.png", optimize=True)
    print("wrote og-card.png", img.size)


def favicon():
    S = 512
    img = Image.new("RGB", (S, S), ACCENT)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(SERIF_B, 330)
    box = d.textbbox((0, 0), "D", font=f)
    d.text(
        ((S - (box[2] - box[0])) / 2 - box[0], (S - (box[3] - box[1])) / 2 - box[1]),
        "D",
        font=f,
        fill=PAPER,
    )
    img.save(f"{OUT}/favicon.png", optimize=True)
    print("wrote favicon.png", img.size)


og_card()
favicon()
