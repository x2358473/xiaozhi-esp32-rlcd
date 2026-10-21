#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 RLCD 单色屏专用的 48x48 表情图片（LVGL RGB565 C 数组）。

twemoji 彩色图在 1-bit 屏上二值化后无法辨认，这里用线条绘制一套单色表情。
用法：python scripts/gen_emoji.py
输出：main/boards/waveshare-s3-rlcd-4.2/assets/emoji/ui_img_emo_*.c
"""

import math
import os

W = H = 48
OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "main", "boards", "waveshare-s3-rlcd-4.2", "assets", "emoji",
)


def canvas():
    return [[0] * W for _ in range(H)]


def put(px, x, y, th=2):
    x = int(round(x))
    y = int(round(y))
    for dy in range(th):
        for dx in range(th):
            xx, yy = x + dx, y + dy
            if 0 <= xx < W and 0 <= yy < H:
                px[yy][xx] = 1


def line(px, x0, y0, x1, y1, th=2):
    n = int(max(abs(x1 - x0), abs(y1 - y0), 1))
    for i in range(n + 1):
        put(px, x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, th)


def disc(px, cx, cy, r):
    for y in range(H):
        for x in range(W):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                px[y][x] = 1


def ring(px, cx, cy, r, th=2):
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - cx, y - cy)
            if r - th / 2 <= d <= r + th / 2:
                px[y][x] = 1


def arc(px, cx, cy, r, a0, a1, th=2):
    steps = max(int(abs(a1 - a0) * 2), 2)
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        put(px, cx + r * math.cos(a), cy + r * math.sin(a), th)


def heart_shape(px, cx, cy, s):
    for y in range(int(cy - 2 * s), int(cy + 2 * s) + 1):
        for x in range(int(cx - 2 * s), int(cx + 2 * s) + 1):
            if not (0 <= x < W and 0 <= y < H):
                continue
            nx = (x - cx) / s
            ny = (cy - y) / s
            if (nx * nx + ny * ny - 1) ** 3 - nx * nx * ny * ny * ny <= 0:
                px[y][x] = 1


def wave(px, x0, x1, y, amp=2, th=2):
    step = 1
    for x in range(int(x0), int(x1) + 1, step):
        yy = y + amp * math.sin((x - x0) / 2.0 * math.pi / 2)
        put(px, x, yy, th)


def face(px, outline=True):
    if outline:
        ring(px, 24, 24, 21, 2)


def frame_round():
    px = canvas()
    face(px)
    return px


def emo_neutral():
    px = frame_round()
    disc(px, 17, 19, 2)
    disc(px, 31, 19, 2)
    line(px, 19, 32, 29, 32, 2)
    return px


def emo_happy():
    px = frame_round()
    disc(px, 17, 19, 2)
    disc(px, 31, 19, 2)
    arc(px, 24, 28, 9, 20, 160, 2)
    return px


def emo_laughing():
    px = frame_round()
    arc(px, 17, 20, 5, 200, 340, 2)
    arc(px, 31, 20, 5, 200, 340, 2)
    arc(px, 24, 27, 10, 15, 165, 2)
    line(px, 15, 31, 33, 31, 2)
    return px


def emo_funny():
    px = frame_round()
    disc(px, 17, 19, 2)
    arc(px, 31, 20, 5, 200, 340, 2)
    line(px, 18, 31, 30, 31, 2)
    arc(px, 24, 31, 7, 10, 150, 2)
    disc(px, 24, 38, 3)
    return px


def emo_sad():
    px = frame_round()
    disc(px, 17, 19, 2)
    disc(px, 31, 19, 2)
    arc(px, 24, 35, 9, 200, 340, 2)
    return px


def emo_angry():
    px = frame_round()
    line(px, 12, 14, 21, 17, 2)
    line(px, 36, 14, 27, 17, 2)
    disc(px, 17, 20, 2)
    disc(px, 31, 20, 2)
    arc(px, 24, 36, 9, 200, 340, 2)
    return px


def emo_crying():
    px = frame_round()
    arc(px, 17, 20, 5, 200, 340, 2)
    arc(px, 31, 20, 5, 200, 340, 2)
    arc(px, 24, 35, 9, 200, 340, 2)
    # 泪滴
    disc(px, 14, 27, 2)
    put(px, 13, 30, 2)
    disc(px, 34, 27, 2)
    put(px, 33, 30, 2)
    return px


def emo_loving():
    px = frame_round()
    heart_shape(px, 17, 19, 4)
    heart_shape(px, 31, 19, 4)
    arc(px, 24, 28, 9, 20, 160, 2)
    return px


def emo_embarrassed():
    px = frame_round()
    disc(px, 17, 19, 2)
    disc(px, 31, 19, 2)
    ring(px, 24, 33, 4, 2)
    line(px, 9, 26, 13, 28, 2)
    line(px, 35, 28, 39, 26, 2)
    return px


def emo_surprised():
    px = frame_round()
    ring(px, 17, 19, 4, 2)
    ring(px, 31, 19, 4, 2)
    ring(px, 24, 33, 4, 2)
    return px


def emo_shocked():
    px = frame_round()
    ring(px, 16, 19, 5, 2)
    ring(px, 32, 19, 5, 2)
    ring(px, 24, 34, 6, 2)
    return px


def emo_thinking():
    px = frame_round()
    line(px, 13, 18, 21, 18, 2)
    disc(px, 31, 19, 2)
    wave(px, 19, 29, 33, 2, 2)
    # 问号
    arc(px, 38, 12, 3, 180, 480, 2)
    put(px, 38, 17, 2)
    return px


def emo_winking():
    px = frame_round()
    arc(px, 17, 20, 5, 200, 340, 2)
    disc(px, 31, 19, 2)
    arc(px, 24, 28, 9, 20, 160, 2)
    return px


def emo_cool():
    px = frame_round()
    # 墨镜
    for x in range(10, 22):
        for y in range(16, 23):
            if (x - 16) ** 2 + (y - 19) ** 2 <= 36:
                px[y][x] = 1
    for x in range(26, 38):
        for y in range(16, 23):
            if (x - 32) ** 2 + (y - 19) ** 2 <= 36:
                px[y][x] = 1
    line(px, 22, 19, 26, 19, 2)
    line(px, 10, 17, 6, 16, 2)
    line(px, 38, 17, 42, 16, 2)
    arc(px, 24, 30, 8, 20, 160, 2)
    return px


def emo_relaxed():
    px = frame_round()
    arc(px, 17, 20, 5, 20, 160, 2)
    arc(px, 31, 20, 5, 20, 160, 2)
    arc(px, 24, 28, 9, 20, 160, 2)
    return px


def emo_delicious():
    px = frame_round()
    arc(px, 17, 20, 5, 200, 340, 2)
    arc(px, 31, 20, 5, 200, 340, 2)
    arc(px, 24, 27, 9, 20, 160, 2)
    line(px, 17, 31, 31, 31, 2)
    disc(px, 24, 37, 3)
    return px


def emo_kissy():
    px = frame_round()
    arc(px, 17, 20, 5, 20, 160, 2)
    arc(px, 31, 20, 5, 20, 160, 2)
    ring(px, 24, 33, 3, 2)
    heart_shape(px, 39, 11, 3)
    return px


def emo_confident():
    px = frame_round()
    line(px, 12, 16, 21, 15, 2)
    line(px, 36, 16, 27, 15, 2)
    disc(px, 17, 20, 2)
    disc(px, 31, 20, 2)
    line(px, 19, 31, 29, 29, 2)
    # 星星
    line(px, 39, 8, 39, 14, 2)
    line(px, 36, 11, 42, 11, 2)
    return px


def emo_sleepy():
    px = frame_round()
    line(px, 13, 19, 21, 19, 2)
    line(px, 27, 19, 35, 19, 2)
    disc(px, 24, 33, 3)
    # Z
    line(px, 34, 8, 42, 8, 2)
    line(px, 42, 8, 34, 15, 2)
    line(px, 34, 15, 42, 15, 2)
    return px


def emo_silly():
    px = frame_round()
    disc(px, 17, 19, 2)
    arc(px, 31, 20, 5, 200, 340, 2)
    arc(px, 24, 28, 9, 20, 160, 2)
    line(px, 20, 34, 28, 34, 2)
    disc(px, 28, 38, 3)
    return px


def emo_confused():
    px = frame_round()
    line(px, 12, 14, 21, 17, 2)
    line(px, 27, 17, 36, 14, 2)
    disc(px, 17, 20, 2)
    ring(px, 31, 20, 3, 2)
    wave(px, 18, 30, 33, 2, 2)
    return px


def emo_fear():
    px = frame_round()
    ring(px, 16, 19, 5, 2)
    ring(px, 32, 19, 5, 2)
    wave(px, 15, 33, 33, 3, 2)
    line(px, 8, 10, 12, 14, 2)
    line(px, 40, 10, 36, 14, 2)
    return px


def emo_disgusted():
    px = frame_round()
    line(px, 13, 17, 21, 19, 2)
    line(px, 35, 17, 27, 19, 2)
    disc(px, 17, 21, 2)
    disc(px, 31, 21, 2)
    ring(px, 24, 31, 3, 2)
    line(px, 24, 34, 24, 37, 2)
    line(px, 20, 37, 28, 37, 2)
    return px


def emo_microchip_ai():
    px = canvas()
    # 方形脸
    for x in range(8, 40):
        px[8][x] = px[39][x] = 1
    for y in range(8, 40):
        px[y][8] = px[y][39] = 1
    # 方眼
    for x in range(14, 22):
        for y in range(17, 23):
            px[y][x] = 1
    for x in range(26, 34):
        for y in range(17, 23):
            px[y][x] = 1
    # 天线
    line(px, 24, 4, 24, 8, 2)
    disc(px, 24, 4, 2)
    # 嘴
    line(px, 16, 31, 32, 31, 2)
    for x in range(18, 31, 4):
        px[31][x] = 0
    return px


EMOJIS = {
    "neutral": emo_neutral,
    "happy": emo_happy,
    "laughing": emo_laughing,
    "funny": emo_funny,
    "sad": emo_sad,
    "angry": emo_angry,
    "crying": emo_crying,
    "loving": emo_loving,
    "embarrassed": emo_embarrassed,
    "surprised": emo_surprised,
    "shocked": emo_shocked,
    "thinking": emo_thinking,
    "winking": emo_winking,
    "cool": emo_cool,
    "relaxed": emo_relaxed,
    "delicious": emo_delicious,
    "kissy": emo_kissy,
    "confident": emo_confident,
    "sleepy": emo_sleepy,
    "silly": emo_silly,
    "confused": emo_confused,
    "fear": emo_fear,
    "disgusted": emo_disgusted,
    "microchip_ai": emo_microchip_ai,
}

NAMES_CN = {
    "neutral": "待命", "happy": "开心", "laughing": "大笑", "funny": "搞笑",
    "sad": "难过", "angry": "生气", "crying": "哭泣", "loving": "喜爱",
    "embarrassed": "害羞", "surprised": "惊讶", "shocked": "震惊", "thinking": "思考",
    "winking": "眨眼", "cool": "耍酷", "relaxed": "放松", "delicious": "好吃",
    "kissy": "亲亲", "confident": "自信", "sleepy": "犯困", "silly": "调皮",
    "confused": "困惑", "fear": "害怕", "disgusted": "嫌弃", "microchip_ai": "就绪",
}


def to_c(name, px):
    data = []
    for y in range(H):
        for x in range(W):
            data.append(0xFF if px[y][x] == 0 else 0x00)  # 白底
            data.append(0xFF if px[y][x] == 0 else 0x00)
    lines = []
    for i in range(0, len(data), 16):
        lines.append("    " + ",".join("0x%02x" % b for b in data[i:i + 16]) + ",")
    return f"""/* 自动生成：单色表情 "{NAMES_CN.get(name, name)}"（48x48，RGB565 白底黑线） */
/* 生成脚本：scripts/gen_emoji.py，请勿手工修改 */
#include "lvgl.h"

static const uint8_t ui_img_emo_{name}_map[] = {{
{chr(10).join(lines)}
}};

const lv_image_dsc_t ui_img_emo_{name} = {{
    .header.magic = LV_IMAGE_HEADER_MAGIC,
    .header.cf = LV_COLOR_FORMAT_RGB565,
    .header.w = {W},
    .header.h = {H},
    .header.stride = {W * 2},
    .data_size = {len(data)},
    .data = ui_img_emo_{name}_map,
}};
"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in EMOJIS.items():
        px = fn()
        text = to_c(name, px)
        path = os.path.join(OUT_DIR, f"ui_img_emo_{name}.c")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("generated", path)
    print(f"total {len(EMOJIS)} emojis")


if __name__ == "__main__":
    main()
