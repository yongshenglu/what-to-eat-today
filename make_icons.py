# -*- coding: utf-8 -*-
"""生成「今天吃什么」的 PWA 图标 (icon-192.png / icon-512.png)

设计：暖橙渐变圆角方块 + 白色饭碗 + 热气
运行：python make_icons.py
"""
import math
from PIL import Image, ImageDraw

TOP = (255, 145, 70)      # #FF9146
BOTTOM = (214, 69, 69)    # #D64545
WHITE = (255, 255, 255, 255)


def rounded_mask(size, radius):
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return mask


def gradient(size):
    img = Image.new("RGBA", (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / max(size - 1, 1)
        c = tuple(int(TOP[i] + (BOTTOM[i] - TOP[i]) * t) for i in range(3)) + (255,)
        d.line([(0, y), (size, y)], fill=c)
    return img


def draw_steam(d, cx, top, height, width, w):
    pts = []
    for i in range(21):
        t = i / 20
        y = top + height * t
        x = cx + width * math.sin(t * math.pi * 1.5)
        pts.append((x, y))
    d.line(pts, fill=(255, 255, 255, 215), width=w, joint="curve")
    r = w // 2
    d.ellipse([pts[0][0] - r, pts[0][1] - r, pts[0][0] + r, pts[0][1] + r], fill=(255, 255, 255, 215))
    d.ellipse([pts[-1][0] - r, pts[-1][1] - r, pts[-1][0] + r, pts[-1][1] + r], fill=(255, 255, 255, 215))


def make_icon(size, path):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    S = size
    # 圆角渐变背景
    bg = gradient(S)
    img.paste(bg, (0, 0), rounded_mask(S, int(S * 0.22)))
    d = ImageDraw.Draw(img)

    # 热气
    stroke = max(int(S * 0.030), 2)
    draw_steam(d, S * 0.500, S * 0.185, S * 0.155, S * 0.028, stroke)
    draw_steam(d, S * 0.365, S * 0.225, S * 0.135, S * 0.024, stroke)
    draw_steam(d, S * 0.635, S * 0.225, S * 0.135, S * 0.024, stroke)

    # 碗身（半椭圆，上沿与碗沿相接）
    d.pieslice([S * 0.235, S * 0.265, S * 0.765, S * 0.845], 0, 180, fill=WHITE)
    # 碗沿
    d.rounded_rectangle(
        [S * 0.175, S * 0.470, S * 0.825, S * 0.555],
        radius=int(S * 0.042), fill=WHITE,
    )

    img.save(path)
    print("written:", path)


if __name__ == "__main__":
    make_icon(192, "icon-192.png")
    make_icon(512, "icon-512.png")
