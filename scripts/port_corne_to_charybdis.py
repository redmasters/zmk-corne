#!/usr/bin/env python3
"""Gera config/charybdis.keymap a partir de config/corne.keymap.

O Charybdis Mini 3x6 tem 41 teclas: as 36 teclas principais e os polegares
36-40 do Corne. A posição 41 do Corne (o sexto polegar) não existe.

O script é intencionalmente de mão única: ele lê o Corne e reescreve o
Charybdis. Depois do primeiro port, o keymap do Charybdis passa a ser editado
no keymap-editor; não rode este script de novo sem revisar o diff.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "config" / "corne.keymap"
TARGET = ROOT / "config" / "charybdis.keymap"

FORMATTER_MODELINE = (
    '// dt-formatter: indent="    ", multilineIntegerCellsIndent="keep"\n'
)

THUMB_41_COMBOS = """

        // O case de 41 teclas não tem a posição 41. Cada layer que usava a 41
        // reencontra o binding no combo dos dois polegares direitos (39 + 40).
        // BASE/MAC/GAME/FNGAME/MEDIA: BSPC/DEL (o &bs_delete original).
        // NAV: BSPC; FUN: APP; NUM: ponto; DOTA: F8; MOUSE: clique do meio.

        thumb_41_bs_del {
            bindings = <&bs_delete>;
            key-positions = <39 40>;
            layers = <BASE MAC GAME FNGAME MEDIA>;
            timeout-ms = <35>;
        };

        thumb_41_nav {
            bindings = <&kp BACKSPACE>;
            key-positions = <39 40>;
            layers = <NAV NAV_MAC>;
            timeout-ms = <35>;
        };

        thumb_41_fn {
            bindings = <&kp K_APPLICATION>;
            key-positions = <39 40>;
            layers = <FUN FUN_MAC>;
            timeout-ms = <35>;
        };

        thumb_41_num {
            bindings = <&kp DOT>;
            key-positions = <39 40>;
            layers = <NUM>;
            timeout-ms = <35>;
        };

        thumb_41_dota {
            bindings = <&kp F8>;
            key-positions = <39 40>;
            layers = <DOTA>;
            timeout-ms = <35>;
        };

        thumb_41_mouse {
            bindings = <&mkp MCLK>;
            key-positions = <39 40>;
            layers = <MOUSE>;
            timeout-ms = <35>;
        };
"""

COMMENT_REPLACEMENTS = {
    # diagramas de teclas
    "//                       |ESC/FN|GUI/NAV|TAB/NUM| |ENT/MED|SPACE|BSPC/DEL|":
        "//                       |ESC/FN|GUI/NAV|TAB/NUM| |ENT/MED|SPACE|",
    "//                    |  ▽  |  ▽  |  ▽  |   | ENTER| DEL | BSPC |":
        "//                    |  ▽  |  ▽  |  ▽  |   | ENTER| DEL |",
    "//                    |  ▽  |  ▽  |  ▽  |   |  ▽  |SPACE| APP |":
        "//                    |  ▽  |  ▽  |  ▽  |   | TAB |SPACE|   (39+40 = APP)",
    "//                    |  ▽  |  ▽  |  ▽  |   |  -  |  0  |  .  |":
        "//                    |  ▽  |  ▽  |  ▽  |   |  -  |  0  |",
    "//                    |ESC/FNG|SPACE| TAB |   |ENTER|  ▽  |  ▽  |":
        "//                    |ESC/FNG|SPACE| TAB |   |ENTER|  ▽  |",
    "//                    | SFT |SPC/FNG| TAB |   |ENTER|SPACE| F8  |":
        "//                    | SFT |SPC/FNG| TAB |   |ENTER|SPACE|",
    "//                    |  ▽  |  ▽  |  ▽  |   |  ▽  |  0  |  ▽  |":
        "//                    |  ▽  |  ▽  |  ▽  |   |  ▽  |  0  |",
    "//                    |  ▽  |  ▽  |  ▽  |   |LCLK |RCLK |MCLK |":
        "//                    |  ▽  |  ▽  |  ▽  |   |LCLK |RCLK |   (39+40 = MCLK)",
    "//                    |MUTE |PLAY |STOP |   |  ▽  |  ▽  |  ▽  |":
        "//                    |MUTE |PLAY |STOP |   |  ▽  |  ▽  |",
    "//                     |  ·  | EXIT|  ·  |   |  ·  | EXIT|  ·  |":
        "//                     |  ·  | EXIT|  ·  |   |  ·  | EXIT|",
}


def remove_last_binding(body: str, expected: int) -> str:
    """Remove o último binding da última linha não vazia de um bloco."""
    lines = body.split("\n")
    last = max(i for i, line in enumerate(lines) if line.strip())
    line = lines[last]

    groups: list[str] = []
    current: list[str] = []
    for token in line.split():
        if token.startswith("&"):
            if current:
                groups.append(" ".join(current))
            current = [token]
        else:
            current.append(token)
    if current:
        groups.append(" ".join(current))

    if len(groups) != expected:
        raise ValueError(
            f"esperava {expected} bindings na linha de polegar, achei {len(groups)}: {line!r}"
        )

    # Remove apenas o último grupo, preservando o alinhamento das colunas.
    new_line = re.sub(r"\s+" + re.escape(groups[-1]) + r"\s*$", "", line)
    lines[last] = new_line
    return "\n".join(lines)


def main() -> None:
    text = SOURCE.read_text()

    # Modeline do keymap-editor (o Corne já tem; mantém idempotente).
    if FORMATTER_MODELINE not in text:
        text = text.replace(" */\n\n", " */\n\n" + FORMATTER_MODELINE + "\n", 1)

    # Nota de port, específica do Charybdis.
    if "// Port 41 teclas" not in text:
        note = (
            "// Port 41 teclas do Corne. A posição 41 não existe; os bindings dela\n"
            "// viram combos nos polegares 39+40 (ver o nó combos no fim).\n"
            "// Guia de montagem: docs/charybdis.md\n"
        )
        text = text.replace(FORMATTER_MODELINE, FORMATTER_MODELINE + "\n" + note, 1)

    # Cabeçalho próprio do Charybdis.
    text = text.replace(
        "Keymap Padrão do ZMK para Corne",
        "Keymap do Charybdis Mini 3x6 (41 teclas), baseado no Corne",
        1,
    )

    # Posições válidas de polegar no case de 41 teclas.
    text = text.replace(
        "#define THUMBS 39 40 41 36 37 38",
        "#define THUMBS 39 40 36 37 38",
    )
    text = text.replace(
        "#define THUMBS_NO_SPACE 39 41 36 37 38",
        "#define THUMBS_NO_SPACE 39 36 37 38",
    )

    for old, new in COMMENT_REPLACEMENTS.items():
        text = text.replace(old, new)

    # Localiza o nó keymap para não mexer nos bindings dos behaviors.
    keymap_start = text.index("\n    keymap {")
    keymap_end = text.index("\n    };\n};", keymap_start)
    keymap = text[keymap_start:keymap_end]

    replacements: list[tuple[int, int, str]] = []
    for match in re.finditer(r"bindings\s*=\s*<(.*?)>\s*;", keymap, re.S):
        new_body = remove_last_binding(match.group(1), expected=6)
        start = keymap_start + match.start(1)
        end = keymap_start + match.end(1)
        replacements.append((start, end, new_body))

    if len(replacements) != 13:
        raise ValueError(
            f"esperava 13 layers no keymap, encontrei {len(replacements)}"
        )

    for start, end, new_body in reversed(replacements):
        text = text[:start] + new_body + text[end:]

    # Insere os combos antes do fechamento do nó combos.
    anchor = "\n    };\n\n    // Ativa as variantes macOS"
    if text.count(anchor) != 1:
        raise ValueError("âncora do nó combos não encontrada de forma única")
    text = text.replace(
        anchor,
        THUMB_41_COMBOS + "\n    };\n\n    // Ativa as variantes macOS",
        1,
    )

    TARGET.write_text(text)
    print(f"gerado: {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
