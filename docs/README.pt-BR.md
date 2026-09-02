![corneMXSep25](docs/corne+dongle.jpg)
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
split e os hosts.

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

![keymap](../keymap-drawer/corne.svg)

### Layout

### Log

https://gist.github.com/redmasters/c388c28b4bfd8b269c60cc647f9fd280
