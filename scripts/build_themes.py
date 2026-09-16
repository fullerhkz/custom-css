"""Combine the supplied layout with the paint declarations of each legacy theme.

The browser expands CSS shorthands; tinycss2 preserves selectors, rule order,
importance and media/keyframe nesting. No approximate hex-to-hex mapping.
"""
from pathlib import Path
import re
from urllib.parse import urljoin

import tinycss2 as css
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'examples/CSS new.css'
FIXES = ROOT / 'scripts/layout-fixes.css'
PAINT = {'color', 'background-color', 'background-image', 'box-shadow',
         'text-shadow', 'fill', 'stroke', 'outline-color', 'caret-color',
         'accent-color', 'text-decoration-color', 'column-rule-color',
         '-webkit-box-shadow', '-moz-box-shadow', '-webkit-text-fill-color'}
BACKGROUND = ['background-color', 'background-image', 'background-position',
              'background-size', 'background-repeat', 'background-origin',
              'background-clip', 'background-attachment']


def parse(text):
    return css.parse_stylesheet(text, skip_whitespace=True, skip_comments=True)


def declarations(rule):
    parsed = css.parse_declaration_list(rule.content, skip_whitespace=True, skip_comments=True)
    # BJ-Blue's legacy tbody contains a lone "ECECEC" token (line 944).
    # Browsers ignore it; keep the archive intact and omit it from new output.
    for d in parsed:
        if d.type == 'error':
            assert css.serialize(rule.prelude).strip() == 'tbody' and d.source_line == 944, d
    return [d for d in parsed if d.type == 'declaration']


def is_paint(prop):
    return prop in PAINT or (prop.startswith('border-') and prop.endswith('-color'))


def absolute_urls(value, theme):
    # Legacy relative assets were relative to the theme on BJ-Share, not GitHub.
    # These custom themes have no native image directory (verified HTTP 404).
    # Share Black's generic assets for dark themes, Blue's for the light Pink.
    asset_theme = {'BJ-Midnight': 'bj-black', 'BJ-DarkBlue': 'bj-black',
                   'BJ-Darkness': 'bj-black', 'BJ-Red': 'bj-black',
                   'BJ-Pink': 'bj-blue'}.get(theme, theme.lower())
    base = f'https://bj-share.info/static/styles/{asset_theme}/'
    return re.sub(r'url\(\s*[\"\']?([^\"\')]+)[\"\']?\s*\)',
                  lambda m: 'url("' + urljoin(base, m[1].strip()) + '")', value)


def entries(nodes):
    for node in nodes:
        assert node.type != 'error', node
        if node.type == 'qualified-rule':
            for d in declarations(node):
                assert d.type == 'declaration', d
                yield d
        elif node.type == 'at-rule' and node.content is not None:
            yield from entries(css.parse_rule_list(node.content, skip_whitespace=True, skip_comments=True))


def expansion_cache(page, trees):
    values = sorted({(d.lower_name, css.serialize(d.value).strip())
                     for tree in trees for d in entries(tree)
                     if d.lower_name == 'background' or
                     re.fullmatch(r'border(?:-(?:top|right|bottom|left))?', d.lower_name)})
    expanded = page.evaluate('''values => values.map(([prop, value]) => {
      const s = document.createElement('div').style;
      // The reference uses variables only for colors in these shorthands.
      s.setProperty(prop, value.replace(/var\\(--[\\w-]+\\)/g, 'currentColor'));
      const names = prop === 'background' ?
        ['background-color','background-image','background-position','background-size',
         'background-repeat','background-origin','background-clip','background-attachment'] :
        (prop === 'border' ? ['top','right','bottom','left'].flatMap(side =>
          ['width','style','color'].map(kind => `border-${side}-${kind}`)) :
          ['width','style','color'].map(kind => `${prop}-${kind}`));
      return names.map(name => [name, s.getPropertyValue(name)]);
    })''', values)
    return dict(zip(values, expanded))


def split(d, cache, theme):
    prop, value = d.lower_name, css.serialize(d.value).strip()
    parts = cache.get((prop, value), [(prop, value)])
    return [(p, absolute_urls(v, theme), d.important) for p, v in parts if v]


def emit_rule(selector, decls):
    if not decls:
        return ''
    return selector + ' {\n' + ''.join(
        f'   {p}: {v}{" !important" if important else ""};\n'
        for p, v, important in decls) + '}\n\n'


def transform(nodes, cache, theme, mode, keyframes=None):
    output = ''
    for node in nodes:
        if node.type == 'qualified-rule':
            selector = css.serialize(node.prelude).strip()
            out = []
            for d in declarations(node):
                if d.lower_name.startswith('--'):
                    continue
                for prop, value, important in split(d, cache, theme):
                    if mode == 'paint':
                        # Background geometry describes the image. The common
                        # layout below can still resize it at mobile breakpoints.
                        if is_paint(prop) or prop in BACKGROUND:
                            out.append((prop, value, important))
                    elif not is_paint(prop):
                        out.append((prop, value, important))
            if keyframes is not None:
                out += keyframes.get(selector, [])
            output += emit_rule(selector, out)
        elif node.type == 'at-rule' and node.content is not None:
            name, params = node.lower_at_keyword, css.serialize(node.prelude).strip()
            nested = css.parse_rule_list(node.content, skip_whitespace=True, skip_comments=True)
            if name.endswith('keyframes'):
                if mode == 'paint':
                    continue  # A second @keyframes would discard the layout animation.
                inner = transform(nested, cache, theme, mode, KEYFRAMES.get(params, {}))
            else:
                inner = transform(nested, cache, theme, mode)
            if inner:
                if name == 'media' and params == 'all':
                    output += ('/* MENU FIXO: troque somente a próxima linha para\n'
                               ' * @media not all { para desativar. Até 900px o menu rola com a página. */\n')
                output += f'@{name} {params} {{\n' + inner + '}\n\n'
    return output


def legacy_keyframes(tree, cache, theme):
    result = {}
    for node in tree:
        if node.type == 'at-rule' and node.lower_at_keyword.endswith('keyframes'):
            name = css.serialize(node.prelude).strip()
            result[name] = {}
            for frame in css.parse_rule_list(node.content, skip_whitespace=True, skip_comments=True):
                paints = [part for d in declarations(frame) for part in split(d, cache, theme) if is_paint(part[0])]
                # Different grouping (0%,100% vs 0%,12%,100%) is common.
                for selector in css.serialize(frame.prelude).split(','):
                    result[name][selector.strip()] = paints
    return result


def defaults(page, paint):
    page.set_content('<style>' + paint + '</style><body><input><div class="box"></div></body>')
    colors = page.evaluate('''() => {
      const body = getComputedStyle(document.body);
      const input = getComputedStyle(document.querySelector('input'));
      const box = getComputedStyle(document.querySelector('.box'));
      return {text: body.color, surface: box.backgroundColor,
              field: input.backgroundColor, fieldText: input.color,
              border: input.borderTopColor};
    }''')
    page.locator('input').focus()
    colors['focus'] = page.locator('input').evaluate('(e) => getComputedStyle(e).borderTopColor')
    # Only components added in the example need defaults. Old declarations
    # remain unlayered, so their original selector cascade always takes priority.
    return '''/* Cores auxiliares derivadas deste tema antigo, para componentes novos. */
@layer bj-defaults {
''' + emit_rule(
        'input, textarea, .sceditor-container textarea', [('color', colors['fieldText'], False)]) + emit_rule(
        'dialog', [('color', colors['text'], False), ('background-color', colors['surface'], False)]) + emit_rule(
        '.sceditor-container', [('background-color', colors['field'], False)]) + emit_rule(
        '.sceditor-container:focus-within', [('border-color', colors['focus'], False),
                                           ('box-shadow', f'0 0 15px {colors["focus"]}', False)]) + '}\n\n'


KEYFRAMES = {}


def main():
    global KEYFRAMES
    base = parse(BASE.read_text())
    sources = {path.stem: parse(path.read_text()) for path in sorted((ROOT / 'old').glob('BJ-*.css'))}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome-stable', headless=True)
        page = browser.new_page()
        page.route('**/*', lambda route: route.abort())
        cache = expansion_cache(page, [base, *sources.values()])
        for theme, tree in sources.items():
            paint = transform(tree, cache, theme, 'paint')
            # Resolve each base keyframe group against the old animation.
            legacy = legacy_keyframes(tree, cache, theme)
            KEYFRAMES = {}
            for node in base:
                if node.type == 'at-rule' and node.lower_at_keyword.endswith('keyframes'):
                    name = css.serialize(node.prelude).strip()
                    KEYFRAMES[name] = {}
                    for frame in css.parse_rule_list(node.content, skip_whitespace=True, skip_comments=True):
                        sel = css.serialize(frame.prelude).strip()
                        KEYFRAMES[name][sel] = legacy.get(name, {}).get(sel.split(',')[0].strip(), [])
            layout = transform(base, cache, theme, 'layout')
            generated = (f'/* BJ-Share — {theme} — base CSS new, cores/imagens de ba4e315.\n'
                         ' * Gerado por scripts/build_themes.py. Arquivo independente, sem @import. */\n\n'
                         + defaults(page, paint)
                         + '/* ===== Aparência original: cores, imagens e sombras ===== */\n' + paint
                         + '/* ===== Estrutura comum e menu opcional do exemplo ===== */\n' + layout
                         + FIXES.read_text())
            generated = '\n'.join(line.rstrip() for line in generated.splitlines()) + '\n'
            (ROOT / f'{theme}.css').write_text(generated)
            print(f'{theme}: {len(generated)} bytes')
        browser.close()


if __name__ == '__main__':
    main()
