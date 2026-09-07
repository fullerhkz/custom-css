# BJ CSS — fixed screen

Versões autônomas e responsivas dos dez temas BJ-Share. O layout comum vem de
`../examples/css2-midnight.css`; cores, logotipos, fundos e detalhes visuais são
preservados a partir dos arquivos `../BJ-*.css` correspondentes.

## Arquivos prontos para uso

- `BJ-Black.css`
- `BJ-Blue.css`
- `BJ-Clean.css`
- `BJ-DarkBlue.css`
- `BJ-Darkness.css`
- `BJ-Grey.css`
- `BJ-Midnight.css`
- `BJ-NewBlack.css`
- `BJ-Pink.css`
- `BJ-Red.css`

## Padronizações e correções

- mesma estrutura e os mesmos breakpoints em todos os temas;
- paletas centralizadas em propriedades customizadas no `:root`;
- cabeçalho, menu, busca, alertas, conteúdo, sidebar e carrossel responsivos;
- suporte a monitores 1440p/4K e telas estreitas;
- `box-sizing: border-box` global, com dimensões compensadas;
- imagens fluidas mantendo a proporção original;
- foco do editor corrigido (o brilho aparecia permanentemente no modelo);
- destaque da seção ativa e suporte a redução de movimento;
- URLs relativas de ícones e barras substituídas por URLs absolutas válidas;
- estilos particulares dos temas mantidos em uma seção de compatibilidade.

## Regeneração

Execute na raiz do repositório:

```bash
python3 BJ-css-fixed-screen/build_themes.py
```

O gerador usa apenas a biblioteca padrão do Python e sempre recria os dez CSS
de forma determinística. Os arquivos originais fora desta pasta não são
alterados.
