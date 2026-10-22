#!/usr/bin/env python3
"""Confere se as posições compartilhadas dos dois keymaps continuam iguais.

O Corne tem 42 teclas e o Charybdis 41. As posições 0-35 (as 36 teclas
principais) devem ser idênticas nos dois arquivos. Os polegares 36-40 começam
iguais, mas podem divergir porque o Charybdis tem só cinco. A
posição 41 do Corne é a única que não existe no Charybdis; no lugar dela, o
Charybdis usa combos 39+40 definidos no próprio keymap.

Rode antes de commitar uma mudança feita no keymap-editor:

    python3 scripts/check-keymap-sync.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORNE = ROOT / "config" / "corne.keymap"
CHARYBDIS = ROOT / "config" / "charybdis.keymap"

LAYER_RE = re.compile(
    r'\n\s{8}([a-z_]+)\s*\{\s*\n\s*display-name\s*=\s*"([^"]+)";',
)
BINDINGS_RE = re.compile(r"bindings\s*=\s*<(.*?)>\s*;", re.S)


def parse_layers(path: Path) -> dict[str, list[str]]:
    text = path.read_text()
    try:
        start = text.index("\n    keymap {")
        end = text.index("\n    };\n};", start)
    except ValueError as exc:
        raise SystemExit(f"{path}: nó keymap não encontrado") from exc

    keymap = text[start:end]
    layers: dict[str, list[str]] = {}
    for match in LAYER_RE.finditer(keymap):
        name = match.group(1)
        bindings = BINDINGS_RE.search(keymap, match.end())
        if not bindings:
            raise SystemExit(f"{path}: layer {name} sem bindings")
        groups: list[str] = []
        current: list[str] = []
        for token in bindings.group(1).split():
            if token.startswith("&"):
                if current:
                    groups.append(" ".join(current))
                current = [token]
            else:
                current.append(token)
        if current:
            groups.append(" ".join(current))
        layers[name] = groups
    return layers


def main() -> int:
    corne = parse_layers(CORNE)
    charybdis = parse_layers(CHARYBDIS)

    errors: list[str] = []
    if set(corne) != set(charybdis):
        errors.append(
            "layers diferentes: "
            f"Corne={sorted(corne)} Charybdis={sorted(charybdis)}"
        )

    for name in sorted(set(corne) & set(charybdis)):
        c = corne[name]
        b = charybdis[name]
        if len(c) != 42:
            errors.append(f"{name}: Corne tem {len(c)} bindings (esperado 42)")
        if len(b) != 41:
            errors.append(f"{name}: Charybdis tem {len(b)} bindings (esperado 41)")
        if len(c) < 41 or len(b) < 41:
            continue
        for pos in range(36):
            if c[pos] != b[pos]:
                errors.append(
                    f"{name}[{pos}]: Corne={c[pos]!r} Charybdis={b[pos]!r}"
                )

    if errors:
        print("Keymaps fora de sincronia:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print(
            "\nAs posições 0-35 precisam ser iguais nos dois keymaps. "
            "Atualize o outro arquivo ou rode scripts/port_corne_to_charybdis.py "
            "e revise o diff.",
            file=sys.stderr,
        )
        return 1

    thumb_diffs = [
        pos
        for pos in range(36, 41)
        if corne.get("base") and charybdis.get("base") and corne["base"][pos] != charybdis["base"][pos]
    ]
    if thumb_diffs:
        print(
            "Nota: os polegares 36-40 diferem nas posições "
            + ", ".join(str(pos) for pos in thumb_diffs)
            + " (permitido; o Charybdis tem cinco polegares)."
        )

    print(
        f"OK: {len(corne)} layers, posições 0-35 iguais; "
        "Corne tem 42 teclas e Charybdis 41."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
