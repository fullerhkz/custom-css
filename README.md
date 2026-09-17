# Custom CSS

Repositório com arquivos CSS personalizados para uso em interfaces e temas visuais.

Os arquivos disponíveis aqui são folhas de estilo organizadas para facilitar consulta e manutenção.

## Versão 2.0 (17/09/2026) — Temas Otimizados e Reorganizados

A **raiz da `main` contém a versão atual dos nove temas ativos**, servida diretamente via GitHub Pages em `https://theme.bj-share.org/<arquivo.css>`. Por exemplo: [BJ-Midnight.css](https://theme.bj-share.org/BJ-Midnight.css) ou [BJ-NewBlack.css](https://theme.bj-share.org/BJ-NewBlack.css). Cada folha CSS é totalmente independente, sem dependência de `@import` ou arquivos auxiliares.

Os temas foram modularizados e organizados em seções documentadas com sumário interno, indentação uniforme padronizada (3 espaços), remoção de artefatos vazios e correção de erros de sintaxe (como a declaração de banner em Midnight).

A versão anterior (`f8e8be5`) está preservada na íntegra em [old/f8e8be5/](old/f8e8be5/), com todos os dez temas históricos (incluindo o antigo DarkBlue, que foi descontinuado).

| Tema | Arquivo na Raiz (`main`) | URL GitHub Pages |
| --- | --- | --- |
| Black | [BJ-Black.css](BJ-Black.css) | `https://theme.bj-share.org/BJ-Black.css` |
| Blue | [BJ-Blue.css](BJ-Blue.css) | `https://theme.bj-share.org/BJ-Blue.css` |
| Clean | [BJ-Clean.css](BJ-Clean.css) | `https://theme.bj-share.org/BJ-Clean.css` |
| Darkness | [BJ-Darkness.css](BJ-Darkness.css) | `https://theme.bj-share.org/BJ-Darkness.css` |
| Grey | [BJ-Grey.css](BJ-Grey.css) | `https://theme.bj-share.org/BJ-Grey.css` |
| Midnight | [BJ-Midnight.css](BJ-Midnight.css) | `https://theme.bj-share.org/BJ-Midnight.css` |
| NewBlack | [BJ-NewBlack.css](BJ-NewBlack.css) | `https://theme.bj-share.org/BJ-NewBlack.css` |
| Pink | [BJ-Pink.css](BJ-Pink.css) | `https://theme.bj-share.org/BJ-Pink.css` |
| Red | [BJ-Red.css](BJ-Red.css) | `https://theme.bj-share.org/BJ-Red.css` |

> **Nota:** O tema `BJ-DarkBlue` foi descontinuado e removido dos temas ativos. Sua versão anterior permanece arquivada em [old/f8e8be5/BJ-DarkBlue.css](old/f8e8be5/BJ-DarkBlue.css).


A estrutura vem de [examples/CSS new.css](examples/CSS%20new.css), cópia do exemplo recebido com extensão `.cts`. As cores, imagens, gradientes e sombras vêm de **[old/](old/)**, recuperado do commit [`ba4e315`](https://github.com/fullerhkz/custom-css/commit/ba4e31540ff0843df7c2a8e4b3f6fbc07cc894c4), anterior à reformulação responsiva. A aparência é transferida por seletor e declaração, preservando a ordem e `!important`, inclusive as diferenças entre temas claros e escuros. Não há substituição aproximada de paleta.

### Menu fixo

Em cada arquivo novo, procure o comentário `MENU FIXO`. A única regra `@media all {` ativa o menu fixo. Troque essa linha por `@media not all {` para desativá-lo. Até 900px, o menu acompanha a rolagem em ambos os modos, conforme o exemplo. Isto prepara o CSS para a opção proposta; a implementação do controle na conta do usuário depende do site.

### Ajustes verificados

- [scripts/layout-fixes.css](scripts/layout-fixes.css) contém três correções comuns ao exemplo: posicionamento do bloco de perfil à direita, empilhamento dos blocos de usuário no celular e limite de largura dos alertas. Essas regras já estão incorporadas nos dez CSS.
- A declaração inválida `ECECEC`, encontrada no `tbody` do Blue antigo, é omitida na geração. O arquivo arquivado permanece intacto.
- No NewBlack, o fundo de `#logo` é transparente: o preto do tema antigo ficava invisível com largura zero, mas cobria o banner quando aplicado ao bloco de largura total do exemplo. A imagem original de `#header` foi mantida. O teste visual [scripts/validate_newblack_banner.py](scripts/validate_newblack_banner.py) reproduz a falha anterior e compara a imagem renderizada em oito cenários.
- URLs relativas de imagens foram transformadas em URLs HTTPS do BJ-Share. As pastas nativas de Midnight, DarkBlue, Darkness, Red e Pink retornaram 404. Nesses casos, somente os ícones genéricos relativos usam os recursos compartilhados do Black (temas escuros) ou Blue (Pink). Logos, banners, texturas e imagens com URLs explícitas mantêm suas fontes antigas.

### Prévia e validação

Execute `python -m http.server 8000` na raiz e abra [http://localhost:8000/validation/preview.html](http://localhost:8000/validation/preview.html). A prévia permite trocar o tema e ligar/desligar o menu com conteúdo fictício. Use o servidor local para que o navegador permita acessar as regras da folha CSS.

Os testes usam Chrome e comparam cores, fundos, imagens, bordas e sombras com o CSS antigo; também verificam foco/hover, rolagem do menu, cliques nos alertas, sobreposição do cabeçalho e a estrutura comum. São dez larguras, de 320 a 3840px, com o menu ligado e desligado, para cada um dos dez temas: **200 combinações**.

```sh
python -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/build_themes.py
.venv/bin/python scripts/validate_themes.py
.venv/bin/python scripts/check_assets.py
.venv/bin/python scripts/capture_preview.py
.venv/bin/python scripts/validate_newblack_banner.py
```

Os scripts usam `/usr/bin/google-chrome-stable`; ajuste esse caminho se o Chrome estiver instalado em outro local. Resultados: [comparação dos temas](validation/report.json) e [disponibilidade das imagens](validation/assets.json). As capturas são geradas em `validation/screenshots/` e não são versionadas.

A comparação automatizada usa uma página local e bloqueia recursos externos; a disponibilidade das imagens é verificada separadamente por HTTP. A prévia não substitui um teste nas páginas autenticadas do BJ-Share, às quais esta validação não teve acesso.
