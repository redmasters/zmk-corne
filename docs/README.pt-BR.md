![corneMXSep25](corne+dongle.jpg)
## Corne MX

[Read in English](../README.md)

- 42 teclas;
- Sem fio;
- Modo dongle;
- Teclas MX;
- Switches Brown;
- Keycaps KLP Lame.

## Gravação do firmware

O dongle é o central do ZMK e as duas metades do teclado são periféricos. O
processamento do keymap acontece principalmente no central, portanto uma
atualização apenas do keymap normalmente exige gravar somente o
`corne_dongle`. Uma atualização normal de firmware **não** exige
`settings_reset`; o firmware padrão preserva os vínculos existentes entre o
split e os hosts — **exceto depois de uma mudança na estrutura de layers**
(adicionar, remover ou reordenar layers). Nesse caso, um keymap salvo
anteriormente pelo ZMK Studio continuaria apontando para os índices antigos e
sobreporia o firmware novo; rode o procedimento de `settings_reset` abaixo
primeiro. Veja "Modo macOS" para a história completa.

### Atualização somente do keymap

Recomendado quando apenas `config/corne.keymap` foi alterado:

1. Grave `corne_dongle` no dongle.
2. Reconecte ou reinicie o dongle.
3. Teste os bindings alterados.

Normalmente, as metades não precisam ser regravadas, pois o dongle mantém o
estado do keymap. Consulte
[ZMK Split Keyboards](https://zmk.dev/docs/features/split-keyboards#central-and-peripheral-roles).

### Atualização completa sem apagar os vínculos

Recomendado após atualizar o ZMK, módulos ou configurações que afetam todos os
controladores:

1. Desligue as duas metades do teclado.
2. Grave `corne_dongle` no dongle.
3. Grave `corne_left` na metade esquerda.
4. Grave `corne_right` na metade direita.
5. Reconecte o dongle e ligue as duas metades.

Com os vínculos existentes preservados, as metades esquerda e direita podem ser
gravadas em qualquer ordem. Gravar o dongle primeiro é uma convenção deste
projeto, não um requisito de pareamento do ZMK.

### Primeiro setup do dongle ou mudança da topologia central/periférico

Use este procedimento ao introduzir o dongle pela primeira vez, mudar qual
controlador é o central, substituir controladores ou começar deliberadamente
com vínculos limpos:

1. Desligue as duas metades do teclado.
2. Grave `settings_reset` no dongle.
3. Grave `settings_reset` na metade esquerda.
4. Grave `settings_reset` na metade direita.
5. Grave `corne_dongle` no dongle.
6. Grave `corne_left` na metade esquerda.
7. Grave `corne_right` na metade direita.
8. Reconecte o dongle.
9. Ligue a metade esquerda e aguarde a conexão.
10. Ligue a metade direita e aguarde a conexão.
11. Remova do host a entrada antiga do teclado e faça o pareamento novamente.

O ZMK exige a limpeza dos vínculos antigos ao converter um split existente para
uma topologia com dongle. Parear o periférico esquerdo antes do direito também é
recomendado para displays de dongle que associam os indicadores de bateria pela
ordem de conexão. Consulte
[ZMK Dongle Setup](https://zmk.dev/docs/hardware-integration/dongle),
[ZMK Connection Issues](https://zmk.dev/docs/troubleshooting/connection-issues)
e [ZMK Dongle Screen Pairing](https://github.com/janpfischer/zmk-dongle-screen#pairing).

### Recuperação de um pareamento quebrado do split

Use este procedimento somente quando uma metade não se reconectar após
reinicializações normais:

1. Grave `settings_reset` no dongle e nas duas metades.
2. Grave a imagem de execução correspondente em cada controlador.
3. Reconecte o dongle.
4. Ligue a metade esquerda e aguarde a conexão.
5. Ligue a metade direita.
6. Esqueça o teclado em todos os hosts e faça o pareamento novamente.

`settings_reset` apaga configurações persistentes, inclusive perfis Bluetooth e
a seleção de saída. Não o utilize em atualizações rotineiras. O procedimento
oficial está documentado em
[ZMK Connection Issues](https://zmk.dev/docs/troubleshooting/connection-issues#split-keyboard-parts-unable-to-pair).

> [!WARNING]
> Sempre associe `corne_dongle`, `corne_left` e `corne_right` ao Nice!Nano
> correto. Não desconecte nem sobrescreva por engano a unidade de bootloader
> montada de outro controlador.

### Keymap

Fortemente baseado no [Miryoku Layout](https://github.com/manna-harbour/miryoku),
com algumas mudanças para atender às minhas necessidades.

Os modificadores da home row e o ajuste de tap-hold também são inspirados na
[configuração ZMK do urob](https://github.com/urob/zmk-config#timeless-homerow-mods).

#### Estados de Shift

O keymap oferece deliberadamente vários modos de Shift para contextos
diferentes:

| Estado | Binding | Resultado |
|---|---|---|
| Shift na home row | Segure `S` ou `L` na Base | Mantém `Left Shift` enquanto outra tecla é pressionada. O ajuste posicional de hold-tap favorece rolls normais da mesma mão como taps. |
| Sticky Shift | Toque na tecla externa direita `smart_shift` na Base | Aplica `Left Shift` à próxima tecla. Expira após 900 ms e é liberado imediatamente depois do uso. |
| Caps Word | Acione `smart_shift` enquanto `Left Shift` estiver pressionado | Inicia Caps Word para identificadores e sequências de letras maiúsculas. |
| Shift da camada Num | Segure a tecla Shift externa esquerda ou toque em sticky Shift na Num | Oferece Shift convencional ou one-shot ao inserir números e símbolos. |
| Shift da Game | Segure a tecla externa esquerda na Game | Usa um `Left Shift` simples, sem o comportamento tap-hold da home row. |
| Shift da Dota | Segure o polegar externo esquerdo na Dota | Usa um `Left Shift` dedicado, adequado a jogos. |
| Shift + Backspace | Segure qualquer Shift e pressione a tecla Backspace/Delete da Base | O mod-morph envia `Delete`; sem Shift, envia `Backspace`. |

Os behaviors de Shift na home row da Base usam a mesma estratégia posicional
`balanced`, com 280 ms, descrita pelo urob. Sticky Shift serve para capitalizar
sem precisar temporizar um acorde da home row, enquanto Caps Word atende a
sequências maiores em maiúsculas.

#### Modo macOS

O teclado é usado em Linux/Windows e no macOS, então o keymap mantém uma regra: **o mesmo dedo executa a mesma ação nos dois sistemas**. A layer `mac` move os modificadores em vez de obrigar as mãos a reaprender atalhos:

| Dedo | Linux / Windows | macOS (layer `mac`) |
|---|---|---|
| anelar (15/20) | `Ctrl` — `Ctrl+T`, `Ctrl+C`, `Ctrl+Z` | **`Cmd`** — `⌘T`, `⌘C`, `⌘Z` |
| médio (16/19) | `Alt` — `Alt+Tab`, `Alt+F4` | **`Cmd`** — `⌘Tab`, `⌘W` |
| indicador (17/18) | `Super` | **`Ctrl`** — terminal `Ctrl+C/A/E/K` |
| coluna externa (23) | — | **`Option`** — acentos (`⌥e`, `⌥c`) e `⌥←/→` |
| mindinho | `Shift` | `Shift` (igual) |

Copiar/recortar/colar segue a mesma ideia: os gestos do Linux (`X+C` = `Ctrl+Ins` / 2× `Ctrl+X`; `C+V` = `Shift+Ins`) têm gêmeos no macOS nas mesmas teclas (`⌘C` / 2× `⌘X`; `⌘V`). Independentemente dos combos, mod+letra sempre funciona: segure `D` + `C` = `⌘C`.

Com o modo mac ligado, duas layers finas entram automaticamente por cima da `NAV` e da `FUN`, redefinindo só o que difere:

| Tecla | Linux | macOS |
|---|---|---|
| NAV 12 | `Alt+F4` | `⌘W` (fecha janela/aba) |
| NAV 18 / 21 (segurando) | Home / End | `⌘←` / `⌘→` (início/fim de linha) |
| NAV 22 / 23 | `[` `]` | `⌥←` / `⌥→` (palavra) — os colchetes continuam na Num (6/10) |
| NAV 24 | troca de workspace | `Ctrl`: `⌃←/→` troca de Space, `⌃↑` Mission Control |
| NAV 30 / 33 | Home / End | `⌘↑` / `⌘↓` (início/fim do documento) |
| NAV 34 | Insert | `` ⌘` `` (alterna janelas do mesmo app) |
| FUN 30 / 11 | PrintScreen | `⌘⇧3` (tela toda) / `⌘⇧4` (região) |
| polegar 37 (toque) | `Super` (overview) | `⌘Space` (Spotlight) |

A posição do espaço continua sendo espaço em todo o modo mac — inclusive com a `NAV` segurada, onde o lado Linux tem `Delete` por escolha de projeto.

**Trocar de modo.** Aperte juntas as duas pontas da coluna externa esquerda (posições **0 + 24**, as duas células `▽`). O gesto não usa polegar, então não há risco de acionar a layer `NAV` por acidente. Caminho alternativo: `SYS` → tecla 3 = `Lin/Win`, tecla 4 = `mac`. O modo é persistente (fica gravado nas settings do dongle) e o display confirma (`base` ⇄ `mac`; `navM`/`fnM` quando uma layer de navegação do modo mac está ativa).

**Checklist do lado macOS** (Ajustes do Sistema → Teclado):

- *Fontes de entrada*: o teclado não consegue mais emitir `⌃Space` por acidente, mas o atalho "Selecionar a fonte de entrada anterior" ainda engole um `⌃Space` deliberado — mantenha ou desative.
- *Texto*: "Adicionar ponto com dois espaços" transforma `␣␣` em `. ` — desative se você digita dois espaços de propósito.
- *Atalhos de Teclado → Teclas Modificadoras*: esse diálogo é **por teclado**. Use apenas no teclado embutido do Mac (troque Control ⇄ Command lá para as mãos se comportarem igual). O Corne faz o remapeamento no firmware, por layer.
- Regras do Karabiner-Elements / BetterTouchTool também são **por dispositivo**: inclua o dongle, e quando "a mesma tecla se comporta diferente", investigue ali primeiro.

> ⚠️ **Mudanças na estrutura de layers exigem `settings_reset`.** Este build habilita o ZMK Studio, que consegue gravar um keymap **dentro do teclado** (`ZMK_KEYMAP_SETTINGS_STORAGE` + `ZMK_KEYMAP_LAYER_REORDERING`), e o keymap gravado sobrepõe o firmware compilado. Um keymap salvo antes de uma layer ser adicionada/removida/reordenada continua apontando para os **índices antigos** e aplica bindings errados em silêncio (foi assim que a layer `mac` herdou a antiga `nav` e o espaço passou a dar Delete). Se uma tecla fizer algo diferente do keymap: abra o ZMK Studio, compare aquele binding com o `config/corne.keymap` e, se diferirem, rode o `settings_reset` nos três controladores (resetar o dongle também derruba o pareamento do split), regrave os três e repareie. Não salve o keymap pelo Studio.

### Layout
![keymap](../keymap-drawer/corne.svg)

### Log

https://gist.github.com/redmasters/c388c28b4bfd8b269c60cc647f9fd280
