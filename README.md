![corneMXSep25](docs/corne+dongle.jpg)
## Corne MX

[Leia em Português (Brasil)](docs/README.pt-BR.md)

- 42 MX Keys;
- Wireless;
- Dongle Mode;
- Brown switches;
-  KLP Lame keycaps

> Also in this repo: [Charybdis Mini 3x6](docs/charybdis.md) — a handwired
> 41-key split with a PMW3610 trackball.

### Keymap:
Heavily based on [Miryoku Layout](https://github.com/manna-harbour/miryoku), with some changes to fit my needs.

The home-row modifiers and tap-hold tuning are also inspired by
[urob's ZMK configuration](https://github.com/urob/zmk-config#timeless-homerow-mods).

#### Shift states

The keymap deliberately provides several Shift modes for different contexts:

| State | Binding | Result |
|---|---|---|
| Home-row Shift | Hold `S` or `L` on Base | Holds `Left Shift` while another key is pressed. The positional hold-tap tuning favors normal same-hand rolls as taps. |
| Sticky Shift | Tap the outer-right `smart_shift` key on Base | Applies `Left Shift` to the next key. It expires after 900 ms and releases immediately after use. |
| Caps Word | Activate `smart_shift` while `Left Shift` is already held | Starts Caps Word for identifiers and consecutive capital letters. |
| Number-layer Shift | Hold the left outer Shift key, or tap sticky Shift, on Num | Provides conventional or one-shot Shift while entering numbers and symbols. |
| Game Shift | Hold the left outer key on Game | Uses a plain `Left Shift` without home-row tap-hold behavior. |
| Dota Shift | Hold the left outer thumb on Dota | Uses a dedicated plain `Left Shift` suited to gameplay. |
| Shift + Backspace | Hold either Shift and press the Base Backspace/Delete key | The mod-morph emits `Delete`; without Shift it emits `Backspace`. |

The Base home-row Shift behaviors use the same 280 ms balanced, positional
hold-tap strategy described by urob. Sticky Shift is intended for capitalization
without timing a home-row chord, while Caps Word handles longer uppercase
sequences.

#### macOS mode

The board is used on Linux/Windows and on macOS, so the keymap keeps one rule: **the same finger performs the same action on both systems**. The `mac` layer moves the modifiers instead of making your hands relearn shortcuts:

| Finger | Linux / Windows | macOS (`mac` layer) |
|---|---|---|
| ring (15/20) | `Ctrl` — `Ctrl+T`, `Ctrl+C`, `Ctrl+Z` | **`Cmd`** — `⌘T`, `⌘C`, `⌘Z` |
| middle (16/19) | `Alt` — `Alt+Tab`, `Alt+F4` | **`Cmd`** — `⌘Tab`, `⌘W` |
| index (17/18) | `Super` | **`Ctrl`** — terminal `Ctrl+C/A/E/K` |
| outer column (23) | — | **`Option`** — accents (`⌥e`, `⌥c`) and `⌥←/→` |
| pinky | `Shift` | `Shift` (unchanged) |

Copying follows the same idea: the Linux gestures (`X+C` = `Ctrl+Ins` / 2× `Ctrl+X`; `C+V` = `Shift+Ins`) have macOS twins on the same keys (`⌘C` / 2× `⌘X`; `⌘V`). Independently of the combos, mod+letter always works: hold `D` + `C` = `⌘C`.

When mac mode is on, two thin layers stack automatically on top of `NAV` and `FUN`, redefining only what differs:

| Key | Linux | macOS |
|---|---|---|
| NAV 12 | `Alt+F4` | `⌘W` (close window/tab) |
| NAV 18 / 21 (hold) | Home / End | `⌘←` / `⌘→` (line start/end) |
| NAV 22 / 23 | `[` `]` | `⌥←` / `⌥→` (word) — brackets remain on Num (6/10) |
| NAV 24 | workspace switch | `Ctrl`: `⌃←/→` Spaces, `⌃↑` Mission Control |
| NAV 30 / 33 | Home / End | `⌘↑` / `⌘↓` (document start/end) |
| NAV 34 | Insert | `` ⌘` `` (cycle windows of the same app) |
| FUN 30 / 11 | PrintScreen | `⌘⇧3` (full screen) / `⌘⇧4` (region) |
| thumb 37 (tap) | `Super` (overview) | `⌘Space` (Spotlight) |

The space position stays a space everywhere in mac mode — including while `NAV` is held, where the Linux side deliberately has `Delete`.

**Switching modes.** Press the two ends of the left outer column together (positions **0 + 24**, the two `▽` cells). The gesture uses no thumb, so the NAV layer cannot be engaged by accident. Alternative route: `SYS` → key 3 = `Lin/Win`, key 4 = `mac`. The mode is persistent (stored in the dongle's settings) and the display confirms it (`base` ⇄ `mac`; `navM`/`fnM` while a mac-mode nav/fn layer is active).

**macOS-side checklist** (System Settings → Keyboard):

- *Input sources*: the keyboard can no longer emit `⌃Space` by accident, but the system shortcut "Select the previous input source" still swallows a deliberate one — keep it or disable it.
- *Text*: "Add period with double-space" turns `␣␣` into `. ` — disable it if you type double spaces on purpose.
- *Keyboard Shortcuts → Modifier Keys*: this dialog is **per keyboard**. Use it only for the Mac's built-in keyboard (swap Control ⇄ Command there so your hands behave the same on both). The Corne does its remapping in firmware, per layer.
- Karabiner-Elements / BetterTouchTool rules are also **per device**: add the dongle, and when "the same key behaves differently", debug there first.

> ⚠️ **Layer-structure changes require `settings_reset`.** This build enables ZMK Studio, which can store a keymap **inside the keyboard** (`ZMK_KEYMAP_SETTINGS_STORAGE` + `ZMK_KEYMAP_LAYER_REORDERING`), and a stored keymap overrides the compiled firmware. One saved before a layer is added/removed/reordered keeps the **old layer indices** and silently applies the wrong bindings (that is how the `mac` layer once inherited the old `nav` layer and the space key emitted Delete). If a key does something the keymap does not say: open ZMK Studio, compare that binding with `config/corne.keymap`, and if they differ, run `settings_reset` on all three controllers (resetting the dongle also drops the split pairing), reflash all three and re-pair. Do not save the keymap from Studio.

### Layout:
![keymap](keymap-drawer/corne.svg)

## Flashing

The dongle is the ZMK central and both keyboard halves are peripherals. Keymap
processing happens primarily on the central, so a keymap-only update normally
requires flashing only `corne_dongle`. A regular firmware update does **not**
require `settings_reset`; standard firmware preserves the existing split and
host bonds — **except after a layer-structure change** (adding, removing or
reordering layers). In that case a keymap previously saved by ZMK Studio would
still point at the old layer indices and shadow the new firmware, so run the
`settings_reset` procedure below first. See "macOS mode" for the full story.

### Keymap-only update

Recommended when only `config/corne.keymap` has changed:

1. Flash `corne_dongle` to the dongle.
2. Reconnect or restart the dongle.
3. Test the changed bindings.

The halves do not normally need to be reflashed because the dongle owns the
keymap state. See [ZMK Split Keyboards](https://zmk.dev/docs/features/split-keyboards#central-and-peripheral-roles).

### Full firmware update without resetting bonds

Recommended after ZMK/module upgrades or changes that affect all controllers:

1. Turn both keyboard halves off.
2. Flash `corne_dongle` to the dongle.
3. Flash `corne_left` to the left half.
4. Flash `corne_right` to the right half.
5. Reconnect the dongle and turn both halves on.

With existing bonds intact, the left and right halves may be flashed in either
order. Flashing the dongle first is a project convention, not a ZMK pairing
requirement.

### First dongle setup or changing the central/peripheral topology

Use this procedure when introducing the dongle for the first time, changing
which controller is central, replacing controllers, or deliberately starting
with clean bonds:

1. Turn both keyboard halves off.
2. Flash `settings_reset` to the dongle.
3. Flash `settings_reset` to the left half.
4. Flash `settings_reset` to the right half.
5. Flash `corne_dongle` to the dongle.
6. Flash `corne_left` to the left half.
7. Flash `corne_right` to the right half.
8. Reconnect the dongle.
9. Turn on the left half and wait for it to connect.
10. Turn on the right half and wait for it to connect.
11. Remove the old keyboard entry from the host, then pair it again.

ZMK requires clearing old bonds when converting an existing split to a dongle
topology. Pairing the left peripheral before the right is also recommended for
dongle displays that assign battery widgets by connection order. See
[ZMK Dongle Setup](https://zmk.dev/docs/hardware-integration/dongle),
[ZMK Connection Issues](https://zmk.dev/docs/troubleshooting/connection-issues),
and [ZMK Dongle Screen Pairing](https://github.com/janpfischer/zmk-dongle-screen#pairing).

### Recovering broken split pairing

Use this only when a half no longer connects after normal restarts:

1. Flash `settings_reset` to the dongle and both halves.
2. Flash the matching runtime image to each controller.
3. Reconnect the dongle.
4. Power on the left half and wait for it to connect.
5. Power on the right half.
6. Forget the keyboard on every host and pair it again.

`settings_reset` erases persistent settings, including Bluetooth profiles and
output selection. Do not use it as part of routine updates. The official reset
procedure is documented in
[ZMK Connection Issues](https://zmk.dev/docs/troubleshooting/connection-issues#split-keyboard-parts-unable-to-pair).

> [!WARNING]
> Always match `corne_dongle`, `corne_left`, and `corne_right` to the correct
> Nice!Nano. Do not disconnect or overwrite the wrong mounted bootloader drive.





### Log
https://gist.github.com/redmasters/c388c28b4bfd8b269c60cc647f9fd280

## Second keyboard: Charybdis Mini 3x6

Handwired 41-key split with a PMW3610 trackball on the right half. It shares
the same nice!nano dongle with the Corne (one firmware at a time). See the
[Charybdis build guide](docs/charybdis.md) (pt-BR) for wiring, firmware and
the dongle-switching procedure.
