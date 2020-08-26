from PIL import Image, ImageDraw, ImageFont

class Paint:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.output = Image.new('RGBA', (width, height))
        self.font = ImageFont.truetype('./gfx/font.ttf', 22)
        self.fontSubTitle = ImageFont.truetype('./gfx/font.ttf', 20)
        self.fontTitle = ImageFont.truetype('./gfx/font.ttf', 24)

    def save(self, path, show=False):
        image = self.output.convert("RGB")
        image.save(path)
        if show:
            image.show()

    def printTitle(self, text, x, y, align_h="L", align_v="T", color=(255,255,255)):
        self.print(text, x, y, align_h, align_v, color, self.fontTitle)

    def printSubTitle(self, text, x, y, align_h="L", align_v="T", color=(155,155,155)):
        self.print(text, x, y, align_h, align_v, color, self.fontSubTitle)

    def print(self, text, x, y, align_h="L", align_v="T", color=(255,255,255), font=None):
        if font == None:
            font = self.font
        draw = ImageDraw.Draw(self.output)
        for line in text.split("\n"):
            (w, h) = font.getsize(line)
            sx, sy = 0, 0
            if align_h in "cC":
                sx = -w / 2
            elif align_h in "rR":
                sx = -w
            if align_v in "cC":
                sy = -h / 2
            elif align_v in "bB":
                sy = -h
            draw.text((int(x + sx), int(y + sy)), line, font=font, fill=color)
            y += h * 1.2

    def paint_image(self, path, x=0, y=0, scale=1, crop=None):
        input = Image.open(path)
        (input_w, input_h) = input.size
        if scale != 1:
            input.resize((int(scale * input_w), int(scale * input_h)), Image.LANCZOS)
        if crop != None:
            (cx, cy, cw, ch) = crop
            cw = clamp(cw, 0, input_w - cx) * scale
            ch = clamp(ch, 0, input_h - cy) * scale
            cx = clamp(cx, 0, input_w) * scale
            cy = clamp(cy, 0, input_h) * scale
            input = input.crop((cx, cy, cx + cw, cy + ch))
        if input.mode == "RGBA":
            self.output.alpha_composite(input, (int(x), int(y)))
        else:
            self.output.paste(input, (int(x), int(y)))


def clamp(v, min, max):
    if v < min:
        return min
    if v > max:
        return max
    return v
