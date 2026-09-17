Arquivos originais recuperados do GitHub, sem alterações de conteúdo ou de finais de linha.

- Repositório: https://github.com/fullerhkz/custom-css
- Commit: `ba4e31540ff0843df7c2a8e4b3f6fbc07cc894c4`
- Data do commit: 12/05/2026, 22:13:05 -03:00
- Mensagem: `chore: standardize CSS filenames`

Este é o último commit da linha principal antes de `2b1a758` (`feat(css): add responsive fixed-screen themes`). Estes originais fornecem as cores e imagens dos temas atuais.

O teste `scripts/validate_themes.py` compara os bytes de cada arquivo com `git show ba4e315:<nome>` e registra o SHA-256 no relatório. Até erros legados, como o `ECECEC` solto no Blue, são preservados neste arquivo histórico; os temas atuais estão na raiz da `main`.

A subpasta [ee82239/](ee82239/) preserva os dez CSS que estavam publicados na raiz antes da promoção dos temas novos, byte a byte conforme o commit `ee8223954fb463cf4a383be5bec362d275e3af65`. Assim, a URL principal sempre serve o tema atual e as duas gerações anteriores permanecem no GitHub.

A subpasta [d0d6041/](d0d6041/) preserva o NewBlack publicado antes da correção do fundo preto de `#logo`, que cobria o banner na estrutura nova. Os outros nove temas não foram alterados nessa correção.

A subpasta [f8e8be5/](f8e8be5/) preserva os dez temas publicados na raiz até o commit `f8e8be5`, antes da promoção dos temas reorganizados e otimizados da versão 2.0 (que removeu o tema DarkBlue e refinou a paleta e formatação dos 9 temas remanescentes).

