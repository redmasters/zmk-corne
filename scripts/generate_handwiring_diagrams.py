#!/usr/bin/env python3
"""Gera as ilustrações de docs/handwiring/ para o Charybdis Mini 3x6.

Sem dependências externas: escreve SVG puro. Rode de qualquer lugar:

    python3 scripts/generate_handwiring_diagrams.py
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "handwiring"

INK = "#111827"
MUTED = "#6b7280"
LINE = "#9ca3af"
BG = "#ffffff"

BLUE_F, BLUE_S = "#dbeafe", "#2563eb"
ORANGE_F, ORANGE_S = "#ffedd5", "#ea580c"
GREEN_F, GREEN_S = "#dcfce7", "#16a34a"
PURPLE_F, PURPLE_S = "#ede9fe", "#7c3aed"
RED_F, RED_S = "#fee2e2", "#dc2626"
GRAY_F, GRAY_S = "#f3f4f6", "#9ca3af"
YELLOW_F, YELLOW_S = "#fef9c3", "#ca8a04"

FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"
MONO = "DejaVu Sans Mono, Liberation Mono, monospace"


def attrs(**kwargs: object) -> str:
    return " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kwargs.items() if v is not None)


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 13,
    fill: str = INK,
    anchor: str = "middle",
    weight: str = "normal",
    font: str = FONT,
    opacity: float | None = None,
) -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
        f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"'
        + (f' opacity="{opacity}"' if opacity is not None else "")
        + f">{escape(value)}</text>"
    )


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = "none",
    stroke: str = "none",
    sw: float = 1.5,
    rx: float = 8,
    dash: str | None = None,
) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
        + (f' stroke-dasharray="{dash}"' if dash else "")
        + "/>"
    )


def line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = LINE, sw: float = 1.5, dash: str | None = None) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linecap="round"'
        + (f' stroke-dasharray="{dash}"' if dash else "")
        + "/>"
    )


def poly(points: list[tuple[float, float]], *, stroke: str, sw: float = 2.0, fill: str = "none", dash: str | None = None) -> str:
    pts = " ".join(f"{x},{y}" for x, y in points)
    return (
        f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
        + (f' stroke-dasharray="{dash}"' if dash else "")
        + "/>"
    )


def circle(cx: float, cy: float, r: float, *, fill: str = "none", stroke: str = INK, sw: float = 1.5) -> str:
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def arrow(x1: float, y1: float, x2: float, y2: float, *, stroke: str = LINE, sw: float = 2.0) -> str:
    # ponta simples, sem marker (mais portátil)
    import math

    ang = math.atan2(y2 - y1, x2 - x1)
    head = 9
    p1 = (x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
    p2 = (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
    return (
        line(x1, y1, x2, y2, stroke=stroke, sw=sw)
        + poly([(x2, y2), p1, p2], stroke=stroke, sw=sw, fill=stroke)
    )


def doc(width: int, height: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">\n'
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="{BG}"/>\n'
        + body
        + "\n</svg>\n"
    )


def header(title: str, subtitle: str) -> str:
    return (
        text(40, 44, title, size=24, weight="bold", anchor="start")
        + text(40, 70, subtitle, size=13, fill=MUTED, anchor="start")
    )


# ---------------------------------------------------------------------------
# Matriz
# ---------------------------------------------------------------------------

BASE = {
    (0, 0): "▽", (0, 1): "Q", (0, 2): "W", (0, 3): "E", (0, 4): "R", (0, 5): "T",
    (0, 6): "Y", (0, 7): "U", (0, 8): "I", (0, 9): "O", (0, 10): "P", (0, 11): "▽",
    (1, 0): "▽", (1, 1): "A", (1, 2): "S", (1, 3): "D", (1, 4): "F", (1, 5): "G",
    (1, 6): "H", (1, 7): "J", (1, 8): "K", (1, 9): "L", (1, 10): ";", (1, 11): "'",
    (2, 0): "▽", (2, 1): "Z", (2, 2): "X", (2, 3): "C", (2, 4): "V", (2, 5): "B",
    (2, 6): "N", (2, 7): "M", (2, 8): ",", (2, 9): ".", (2, 10): "/", (2, 11): "⇧",
}


def matrix_svg() -> str:
    w, h = 1240, 860
    b = header(
        "Matriz do Charybdis Mini 3x6",
        "41 teclas • diodos col2row • nice!nano v2 • a posição 41 não existe",
    )

    panels = [
        (40, "Metade esquerda", "C0 = externo → C5 = interno"),
        (640, "Metade direita", "C0 = interno → C5 = externo"),
    ]
    col_pins = ["D6", "D7", "D8", "D10", "D19", "D20"]
    row_pins = ["D4", "D5", "D9", "D18"]
    cell_w, cell_h, gap = 72, 72, 15

    for px, panel_title, direction in panels:
        b += rect(px, 100, 560, 700, fill="#fbfdff", stroke="#d1d5db", rx=16)
        b += text(px + 280, 132, panel_title, size=18, weight="bold")
        b += text(px + 280, 153, direction, size=12, fill=MUTED)

        grid_x = px + 46
        grid_y = 196
        for c in range(6):
            cx = grid_x + c * (cell_w + gap) + cell_w / 2
            b += text(cx, 178, f"C{c}", size=13, weight="bold")
            b += text(cx, 192, col_pins[c], size=10, fill=MUTED)

        for r in range(4):
            cy = grid_y + r * (cell_h + gap)
            b += text(grid_x - 28, cy + 32, f"R{r}", size=13, weight="bold", anchor="middle")
            b += text(grid_x - 28, cy + 47, row_pins[r], size=10, fill=MUTED, anchor="middle")

        # posições
        for r in range(4):
            for c in range(6):
                x = grid_x + c * (cell_w + gap)
                y = grid_y + r * (cell_h + gap)
                pos = None
                if r < 3:
                    pos = r * 12 + c + (0 if px == 40 else 0)
                    if px == 640:
                        # a direita ocupa as colunas globais 6..11
                        pos = r * 12 + 6 + c
                else:
                    if px == 40 and c >= 3:
                        pos = 36 + (c - 3)
                    elif px == 640 and c <= 1:
                        pos = 39 + c

                if pos is None:
                    b += rect(x, y, cell_w, cell_h, fill=GRAY_F, stroke=GRAY_S, sw=1.2, dash="5 5")
                    b += text(x + cell_w / 2, y + cell_h / 2 + 5, "—", size=20, fill=GRAY_S)
                    continue

                fill, stroke = (ORANGE_F, ORANGE_S) if pos >= 36 else (BLUE_F, BLUE_S)
                b += rect(x, y, cell_w, cell_h, fill=fill, stroke=stroke, sw=1.8, rx=10)
                b += text(x + 9, y + 18, str(pos), size=12, weight="bold", fill=stroke, anchor="start")
                rr, cc = (pos // 12, pos % 12) if pos < 36 else (3, [3, 4, 5, 6, 7][pos - 36])
                label = BASE.get((rr, cc), "—")
                if pos == 36:
                    label = "ESC"
                elif pos == 37:
                    label = "NAV"
                elif pos == 38:
                    label = "NUM"
                elif pos == 39:
                    label = "ENT"
                elif pos == 40:
                    label = "SPC"
                b += text(x + cell_w / 2, y + cell_h / 2 + 8, label, size=16, weight="bold")

        # nota da fileira de polegares
        ty = grid_y + 4 * (cell_h + gap) - 4
        if px == 40:
            b += text(px + 280, ty, "polegares 36-38: R3/C3-C5", size=11, fill=ORANGE_S)
        else:
            b += text(px + 280, ty, "polegares 39-40: R3/C0-C1", size=11, fill=ORANGE_S)

    # legenda / regras
    ly = 620
    b += rect(40, ly, 1160, 200, fill="#ffffff", stroke="#d1d5db", rx=14)
    b += text(60, ly + 30, "Como soldar", size=17, weight="bold", anchor="start")
    b += text(
        60,
        ly + 56,
        "1. Cada switch liga a coluna ao ânodo do diodo.  2. O cátodo (faixa) do diodo vai à linha.",
        size=13,
        anchor="start",
    )
    b += text(
        60,
        ly + 80,
        '3. O firmware usa diode-direction = "col2row" e pull-down interno nas linhas; não precisa de resistor externo.',
        size=13,
        anchor="start",
    )
    b += text(
        60,
        ly + 104,
        "4. A direita soma 6 às colunas locais (col-offset = <6>), por isso C0 local = posição 6 (Y).",
        size=13,
        anchor="start",
    )
    b += text(
        60,
        ly + 128,
        "5. A esquerda e a direita usam os mesmos pinos de coluna, mas a ordem física é espelhada:",
        size=13,
        anchor="start",
    )
    b += text(
        60,
        ly + 150,
        "   esquerda: D6 = coluna externa; direita: D6 = coluna interna. Siga a tabela acima.",
        size=13,
        anchor="start",
    )
    b += text(
        60,
        ly + 176,
        "Linhas: R0 D4 • R1 D5 • R2 D9 • R3 D18     Colunas: C0 D6 • C1 D7 • C2 D8 • C3 D10 • C4 D19 • C5 D20",
        size=12,
        fill=MUTED,
        anchor="start",
    )

    # mini símbolo de diodo na legenda
    dx, dy = 1010, ly + 56
    b += line(dx - 34, dy, dx - 10, dy, stroke=BLUE_S, sw=2)
    b += poly([(dx - 10, dy - 8), (dx + 8, dy), (dx - 10, dy + 8)], stroke=BLUE_S, sw=2, fill=BLUE_F)
    b += line(dx + 8, dy - 11, dx + 8, dy + 11, stroke=BLUE_S, sw=3)
    b += line(dx + 8, dy, dx + 34, dy, stroke=GREEN_S, sw=2)
    b += text(dx, dy + 34, "ânodo ← coluna | linha → cátodo", size=10, fill=MUTED)
    b += text(dx, dy + 50, "faixa no lado da linha", size=10, fill=MUTED)

    return doc(w, h, b)


# ---------------------------------------------------------------------------
# Posições / base
# ---------------------------------------------------------------------------


def positions_svg() -> str:
    w, h = 1240, 560
    b = header(
        "Posições do keymap e layer base",
        "0-35 = teclas principais • 36-40 = polegares • 39+40 = combo BSPC/DEL",
    )

    key_w, key_h, gap_x, gap_y = 66, 54, 10, 14
    left_x, top_y = 48, 112
    right_x = left_x + 6 * (key_w + gap_x) + 66
    thumb_y = top_y + 3 * (key_h + gap_y) + 18

    def key(x: float, y: float, pos: int, label: str, *, thumb: bool = False) -> str:
        fill, stroke = (ORANGE_F, ORANGE_S) if thumb else (BLUE_F, BLUE_S)
        s = rect(x, y, key_w, key_h, fill=fill, stroke=stroke, sw=1.8, rx=9)
        s += text(x + 8, y + 16, str(pos), size=11, weight="bold", fill=stroke, anchor="start")
        s += text(x + key_w / 2, y + 38, label, size=15, weight="bold")
        return s

    for r in range(3):
        for c in range(6):
            pos = r * 12 + c
            b += key(left_x + c * (key_w + gap_x), top_y + r * (key_h + gap_y), pos, BASE[(r, c)])
            pos_r = r * 12 + 6 + c
            b += key(right_x + c * (key_w + gap_x), top_y + r * (key_h + gap_y), pos_r, BASE[(r, c + 6)])

    left_thumbs = [(36, "ESC"), (37, "NAV"), (38, "NUM")]
    for i, (pos, label) in enumerate(left_thumbs):
        b += key(left_x + (3 + i) * (key_w + gap_x), thumb_y, pos, label, thumb=True)

    right_thumbs = [(39, "ENT"), (40, "SPC")]
    for i, (pos, label) in enumerate(right_thumbs):
        b += key(right_x + i * (key_w + gap_x), thumb_y, pos, label, thumb=True)

    # destaque do combo
    combo_x = right_x - 8
    combo_y = thumb_y - 10
    combo_w = 2 * key_w + gap_x + 16
    combo_h = key_h + 20
    b += rect(combo_x, combo_y, combo_w, combo_h, fill="none", stroke=RED_S, sw=2.5, rx=12, dash="7 5")
    b += text(combo_x + combo_w / 2, combo_y - 8, "39 + 40 = BSPC/DEL", size=12, weight="bold", fill=RED_S)

    # notas
    ny = 390
    b += rect(48, ny, 1144, 140, fill="#ffffff", stroke="#d1d5db", rx=14)
    b += text(68, ny + 28, "Leitura rápida", size=17, weight="bold", anchor="start")
    notes = [
        "• A posição 41 do Corne não existe neste case. O &bs_delete dela virou o combo 39+40.",
        "• Na layer NAV o mesmo combo é BSPC; na FUN é APP; na NUM é ponto; na DOTA é F8; na MOUSE é clique do meio.",
        "• 37 = GUI/NAV e 40 = SPACE, iguais ao Corne. A layer base é compartilhada com o Corne nas posições 0-35.",
        "• O combo tem timeout de 35 ms. Se disparar sem querer ao rolar ENTER+SPACE, reduza ou troque as posições no keymap.",
    ]
    for i, note in enumerate(notes):
        b += text(68, ny + 54 + i * 20, note, size=12, anchor="start")

    return doc(w, h, b)


# ---------------------------------------------------------------------------
# Pinout lógico
# ---------------------------------------------------------------------------


def pinout_svg() -> str:
    w, h = 1080, 760
    b = header(
        "Pinagem do nice!nano v2",
        "nomes Dx do silk (pro_micro) • o firmware usa esses mesmos nomes",
    )

    # placa
    bx, by, bw, bh = 410, 110, 260, 520
    b += rect(bx, by, bw, bh, fill="#f9fafb", stroke="#374151", sw=2, rx=18)
    b += text(bx + bw / 2, by + 40, "nice!nano v2", size=20, weight="bold")
    b += text(bx + bw / 2, by + 62, "nRF52840", size=12, fill=MUTED)
    b += rect(bx + 70, by + 86, 120, 34, fill="#e5e7eb", stroke="#9ca3af", rx=6)
    b += text(bx + bw / 2, by + 108, "USB-C", size=11, fill=MUTED)
    b += text(bx + bw / 2, by + bh - 24, "bateria LiPo 3.7 V", size=11, fill=MUTED)

    def pill(x: float, y: float, name: str, fn: str, fill: str, stroke: str, *, side: str) -> str:
        pw, ph = 270, 38
        s = rect(x, y, pw, ph, fill=fill, stroke=stroke, sw=1.5, rx=10)
        if side == "left":
            s += text(x + 12, y + 24, name, size=13, weight="bold", anchor="start", fill=stroke)
            s += text(x + pw - 12, y + 24, fn, size=12, anchor="end")
            s += line(x + pw, y + ph / 2, bx, y + ph / 2, stroke=stroke, sw=1.5)
        else:
            s += text(x + pw - 12, y + 24, name, size=13, weight="bold", anchor="end", fill=stroke)
            s += text(x + 12, y + 24, fn, size=12, anchor="start")
            s += line(bx + bw, y + ph / 2, x, y + ph / 2, stroke=stroke, sw=1.5)
        return s

    # esquerda: linhas e colunas
    b += text(40, 136, "MATRIZ — LINHAS", size=13, weight="bold", fill=GREEN_S, anchor="start")
    rows = [("D4", "R0 topo"), ("D5", "R1 home"), ("D9", "R2 base"), ("D18", "R3 polegar")]
    for i, (pin, fn) in enumerate(rows):
        b += pill(40, 150 + i * 48, pin, fn, GREEN_F, GREEN_S, side="left")

    b += text(40, 382, "MATRIZ — COLUNAS", size=13, weight="bold", fill=BLUE_S, anchor="start")
    cols = [("D6", "C0"), ("D7", "C1"), ("D8", "C2"), ("D10", "C3"), ("D19", "C4"), ("D20", "C5")]
    for i, (pin, fn) in enumerate(cols):
        y = 396 + i * 40
        b += pill(40, y, pin, fn, BLUE_F, BLUE_S, side="left")

    # direita: sensor
    b += text(1040, 136, "SENSOR — SPI0", size=13, weight="bold", fill=PURPLE_S, anchor="end")
    sensor = [
        ("D0", "SCK"),
        ("D1", "MOT / IRQ"),
        ("D2", "SDIO"),
        ("D3", "CS"),
    ]
    for i, (pin, fn) in enumerate(sensor):
        b += pill(770, 150 + i * 48, pin, fn, PURPLE_F, PURPLE_S, side="right")

    # direita: energia
    b += text(1040, 382, "ENERGIA", size=13, weight="bold", fill=RED_S, anchor="end")
    power = [("3V3", "VCC do sensor"), ("GND", "GND do sensor")]
    for i, (pin, fn) in enumerate(power):
        b += pill(770, 396 + i * 48, pin, fn, RED_F, RED_S if pin == "3V3" else "#6b7280", side="right")

    # notas
    b += rect(40, 650, 1000, 70, fill="#fff7ed", stroke=ORANGE_S, rx=12)
    b += text(58, 678, "3.3 V, nunca RAW.", size=14, weight="bold", anchor="start", fill=ORANGE_S)
    b += text(
        58,
        700,
        "O PMW3610 é 3.3 V. RAW é a bateria (até 4.2 V) e pode queimar o sensor. D0/D1 são SPI, não console serial.",
        size=12,
        anchor="start",
    )

    return doc(w, h, b)


# ---------------------------------------------------------------------------
# Sensor
# ---------------------------------------------------------------------------


def sensor_svg() -> str:
    w, h = 1080, 620
    b = header(
        "Trackball PMW3610DM-SUDU",
        "sensor na metade direita • SPI0 • lente e ball do case",
    )

    # breakout
    sx, sy, sw, sh = 90, 165, 260, 260
    b += rect(sx, sy, sw, sh, fill="#f5f3ff", stroke=PURPLE_S, sw=2, rx=16)
    b += text(sx + sw / 2, sy + 32, "breakout PMW3610", size=18, weight="bold", fill=PURPLE_S)
    b += circle(sx + sw / 2, sy - 42, 42, fill="#e5e7eb", stroke="#6b7280", sw=2)
    b += text(sx + sw / 2, sy - 37, "ball", size=12, fill=MUTED)
    b += text(sx + sw / 2, sy + 58, "lente voltada para a ball", size=11, fill=MUTED)

    pins = [
        ("VCC", "3.3 V", RED_S),
        ("GND", "0 V", "#6b7280"),
        ("SCK", "SPI clock", PURPLE_S),
        ("SDIO", "dados", PURPLE_S),
        ("CS", "chip select", PURPLE_S),
        ("MOT", "motion / IRQ", PURPLE_S),
    ]
    pin_y = sy + 84
    for i, (name, fn, color) in enumerate(pins):
        y = pin_y + i * 31
        b += text(sx + 20, y + 5, name, size=12, weight="bold", anchor="start", fill=color)
        b += text(sx + 88, y + 5, fn, size=11, anchor="start", fill=MUTED)
        b += circle(sx + sw - 18, y, 5, fill=color, stroke=color, sw=1)
        b += line(sx + sw, y, sx + sw + 30, y, stroke=color, sw=2)

    # nice!nano
    nx, ny, nw, nh = 760, 145, 230, 280
    b += rect(nx, ny, nw, nh, fill="#f9fafb", stroke="#374151", sw=2, rx=16)
    b += text(nx + nw / 2, ny + 34, "nice!nano v2", size=17, weight="bold")
    b += text(nx + nw / 2, ny + 54, "metade direita", size=11, fill=MUTED)

    targets = [
        ("3V3", "VCC", RED_S),
        ("GND", "GND", "#6b7280"),
        ("D0", "SCK", PURPLE_S),
        ("D2", "SDIO", PURPLE_S),
        ("D3", "CS", PURPLE_S),
        ("D1", "MOT", PURPLE_S),
    ]
    target_y = ny + 88
    for i, (name, fn, color) in enumerate(targets):
        y = target_y + i * 31
        b += text(nx + 18, y + 5, name, size=12, weight="bold", anchor="start", fill=color)
        b += text(nx + 58, y + 5, fn, size=11, anchor="start", fill=MUTED)
        b += circle(nx, y, 5, fill=color, stroke=color, sw=1)
        # ligação breakout -> nice!nano
        src_y = pin_y + i * 31
        mid_x = 560
        b += poly(
            [(sx + sw + 30, src_y), (mid_x, src_y), (mid_x, y), (nx, y)],
            stroke=color,
            sw=2,
        )

    # notas
    b += rect(90, 470, 900, 90, fill="#fff7ed", stroke=ORANGE_S, rx=12)
    b += text(108, 500, "Nunca ligue VCC no RAW.", size=14, weight="bold", anchor="start", fill=ORANGE_S)
    b += text(
        108,
        522,
        "Use 3V3. O sensor é 3.3 V; RAW pode chegar a 4.2 V. A ball precisa ficar centrada e a lente na distância focal.",
        size=12,
        anchor="start",
    )
    b += text(
        108,
        544,
        "Se o cursor andar invertido, descomente swap-xy/invert-x/invert-y em boards/shields/charybdis/charybdis_sensor.dtsi.",
        size=11,
        fill=MUTED,
        anchor="start",
    )

    return doc(w, h, b)


# ---------------------------------------------------------------------------
# Dongle / troca
# ---------------------------------------------------------------------------


def dongle_svg() -> str:
    w, h = 1120, 800
    b = header(
        "O mesmo dongle para os dois teclados",
        "um firmware de dongle por vez • settings_reset + re-pareamento ao trocar",
    )

    # dongle central
    dx, dy, dw, dh = 430, 250, 260, 210
    b += rect(dx, dy, dw, dh, fill="#f0f9ff", stroke=BLUE_S, sw=2.5, rx=18)
    b += text(dx + dw / 2, dy + 38, "Dongle nice!nano", size=19, weight="bold", fill=BLUE_S)
    b += text(dx + dw / 2, dy + 60, "+ OLED 128x32", size=12, fill=MUTED)
    b += text(dx + dw / 2, dy + 96, "central ZMK", size=14, weight="bold")
    b += text(dx + dw / 2, dy + 118, "recebe as duas metades", size=11, fill=MUTED)
    b += text(dx + dw / 2, dy + 140, "e o trackball via split", size=11, fill=MUTED)
    b += rect(dx + 28, dy + 164, dw - 56, 26, fill="#fef9c3", stroke=YELLOW_S, rx=6)
    b += text(dx + dw / 2, dy + 182, "um teclado por vez", size=11, weight="bold", fill=YELLOW_S)

    def device(x: float, y: float, label: str, sub: str, fill: str, stroke: str) -> None:
        nonlocal b
        b += rect(x, y, 190, 96, fill=fill, stroke=stroke, sw=1.8, rx=12)
        b += text(x + 95, y + 38, label, size=15, weight="bold", fill=stroke)
        b += text(x + 95, y + 60, sub, size=11, fill=MUTED)

    # corne
    b += text(80, 104, "CORNE", size=16, weight="bold", fill=GREEN_S, anchor="start")
    device(80, 120, "Corne esquerda", "peripheral", GREEN_F, GREEN_S)
    device(300, 120, "Corne direita", "peripheral", GREEN_F, GREEN_S)
    b += arrow(175, 216, dx + 12, dy + 30, stroke=GREEN_S, sw=2)
    b += arrow(395, 216, dx + 70, dy, stroke=GREEN_S, sw=2)
    b += rect(205, 230, 160, 20, fill=BG, stroke="none", rx=4)
    b += text(285, 244, "grave corne_dongle", size=12, weight="bold", fill=GREEN_S)

    # charybdis
    b += text(80, 520, "CHARYBDIS", size=16, weight="bold", fill=ORANGE_S, anchor="start")
    device(80, 536, "Charybdis esquerda", "peripheral", ORANGE_F, ORANGE_S)
    device(300, 536, "Charybdis direita", "peripheral + trackball", ORANGE_F, ORANGE_S)
    b += arrow(175, 536, dx + 12, dy + dh - 28, stroke=ORANGE_S, sw=2)
    b += arrow(395, 536, dx + 70, dy + dh, stroke=ORANGE_S, sw=2)
    b += text(285, 664, "grave charybdis_dongle", size=12, weight="bold", fill=ORANGE_S)

    # host
    hx, hy = 880, 305
    b += rect(hx, hy, 180, 100, fill="#f9fafb", stroke="#374151", sw=2, rx=14)
    b += text(hx + 90, hy + 40, "Host", size=18, weight="bold")
    b += text(hx + 90, hy + 62, "USB / BLE", size=11, fill=MUTED)
    b += arrow(dx + dw, dy + 105, hx, hy + 50, stroke=BLUE_S, sw=2)

    # passos
    b += rect(60, 700, 1000, 70, fill="#ffffff", stroke="#d1d5db", rx=12)
    b += text(
        78,
        726,
        "Troca: 1) settings_reset no dongle  2) grave o *_dongle do teclado  3) settings_reset nas metades  4) pareie L/R e o host.",
        size=12,
        anchor="start",
    )
    b += text(
        78,
        748,
        "O dongle guarda o keymap do ZMK Studio. Depois de mudar layers, rode settings_reset e evite salvar o keymap pelo Studio.",
        size=11,
        fill=MUTED,
        anchor="start",
    )

    return doc(w, h, b)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "matrix.svg": matrix_svg(),
        "positions.svg": positions_svg(),
        "pinout.svg": pinout_svg(),
        "sensor.svg": sensor_svg(),
        "dongle.svg": dongle_svg(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
        print(f"gerado: {(OUT / name).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
