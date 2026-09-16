"""Browser regression checks using the legacy CSS as an independent color oracle."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

import tinycss2 as css
from playwright.sync_api import sync_playwright
from build_themes import ROOT, BASE, FIXES, parse, absolute_urls

WIDTHS = [320, 375, 768, 900, 901, 1024, 1440, 1920, 2560, 3840]
SELECTORS = ['body', 'h2', '#sample-link', '#header', '#menu', '#menudrop ul a',
             '#userinfo', '#userinfo a', '#stats_seeding .stat', '#stats_leeching .stat',
             '#stats_bjpontos .stat', '#alerts', '#alert-link', '#content',
             '.box', '.head', '.head a', '.colhead', '.resolution_header',
             '.season_header', '.rowa', 'td', '#sample-input', '#sample-textarea',
             '#sample-select', '#sample-button', 'blockquote', '.internalbox',
             '.torrent_label.seeding', 'table.shoutTable', 'td.shoutTable',
             '.row1', '.row2', '.r01', '.r50', '#footer']
PROPS = ['color', 'backgroundColor', 'backgroundImage', 'borderTopColor',
         'borderBottomColor', 'boxShadow', 'textShadow']
LAYOUT_SELECTORS = ['#header', '#logo', '#menu', '#userinfo', '#searchbars', '#alerts',
                    '#content', '.thin', '.sidebar', '.main_column', '#footer']
LAYOUT_PROPS = ['position', 'top', 'left', 'width', 'minWidth', 'maxWidth',
                'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
                'marginTop', 'marginBottom', 'display', 'float', 'zIndex', 'pointerEvents']


def styles(page, selectors, props):
    return page.evaluate('''([selectors, props]) => Object.fromEntries(selectors.map(sel => {
      const s = getComputedStyle(document.querySelector(sel));
      return [sel, Object.fromEntries(props.map(p => [p, s[p]]))];
    }))''', [selectors, props])


def syntax_errors(text):
    errors = []
    def visit(nodes):
        for n in nodes:
            if n.type == 'error':
                errors.append(f'{n.source_line}: {n.message}')
            elif n.type == 'qualified-rule':
                visit(css.parse_declaration_list(n.content, skip_comments=True, skip_whitespace=True))
            elif n.type == 'at-rule' and n.content is not None:
                visit(css.parse_rule_list(n.content, skip_comments=True, skip_whitespace=True))
    visit(parse(text))
    return errors


def main():
    fixture = (ROOT / 'validation/preview.html').read_text()
    fixture = re.sub(r'<script>[\s\S]*?</script>', '', fixture)
    fixture = re.sub(r'<link[^>]*>', '', fixture)
    fixture = fixture.replace('<div class="pad" id="long-content"></div>',
                              '<div class="pad" id="long-content">' + '<p>Rolagem de teste</p>' * 80 + '</div>')
    disable_motion = '<style>*{transition:none!important;animation:none!important}</style>'
    report = {'legacyCommit': 'ba4e315', 'widths': WIDTHS, 'themes': {}, 'failures': [],
              'scope': 'Fixture local; recursos externos bloqueados. Não é validação do site autenticado.'}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome-stable', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.route('**/*', lambda route: route.abort())
        def render(text, width=1440):
            page.set_viewport_size({'width': width, 'height': 900})
            page.mouse.move(width - 1, 899)
            page.set_content(fixture + '<style>' + text + '</style>' + disable_motion)

        base = BASE.read_text() + FIXES.read_text()
        reference = {}
        for enabled in [True, False]:
            text = base if enabled else base.replace('@media all {', '@media not all {')
            for width in WIDTHS:
                render(text, width)
                reference[enabled, width] = styles(page, LAYOUT_SELECTORS, LAYOUT_PROPS)
        current_themes = sorted(ROOT.glob('BJ-*.css'))
        assert len(current_themes) == 10
        assert {p.name for p in current_themes} == {p.name for p in (ROOT / 'old').glob('BJ-*.css')}
        for path in current_themes:
            theme = path.stem
            old_bytes = (ROOT / 'old' / path.name).read_bytes()
            archived = subprocess.check_output(['git', 'show', f'ba4e315:{path.name}'])
            assert old_bytes == archived, f'{theme}: archive changed'
            assert (ROOT / 'old/ee82239' / path.name).read_bytes() == subprocess.check_output(
                ['git', 'show', f'ee82239:{path.name}']), f'{theme}: previous published archive changed'
            new = path.read_text()
            errors = syntax_errors(new)
            assert not errors, (theme, errors)
            assert len(re.findall(r'^@media all \{', new, re.M)) == 1
            assert all(url.strip('\"\' ').startswith('https://')
                       for url in re.findall(r'url\(([^)]+)\)', new))
            old = absolute_urls(old_bytes.decode(), theme)
            render(old)
            expected = styles(page, SELECTORS, PROPS)
            render(new)
            actual = styles(page, SELECTORS, PROPS)
            color_diffs = []
            for sel in SELECTORS:
                for prop in PROPS:
                    if expected[sel][prop] != actual[sel][prop]:
                        color_diffs.append([sel, prop, expected[sel][prop], actual[sel][prop]])
            # Focus and hover use the original theme's cascade as well.
            state_diffs = []
            for state, sel in [('focus', '#sample-input'), ('hover', '#sample-button'),
                               ('hover', '#sample-link'), ('hover', '#menudrop ul a')]:
                snapshots = []
                for text in [old, new]:
                    render(text)
                    if state == 'focus':
                        page.locator(sel).first.focus()
                    else:
                        page.locator(sel).first.hover()
                    snapshots.append(styles(page, [sel], PROPS)[sel])
                for prop in PROPS:
                    if snapshots[0][prop] != snapshots[1][prop]:
                        state_diffs.append([state, sel, prop, snapshots[0][prop], snapshots[1][prop]])
            layout_diffs, checks = [], 0
            for enabled in [True, False]:
                text = new if enabled else new.replace('@media all {', '@media not all {')
                for width in WIDTHS:
                    render(text, width)
                    actual_layout = styles(page, LAYOUT_SELECTORS, LAYOUT_PROPS)
                    # Color changes can affect native control metrics. Compare
                    # structural positions rather than content-dependent heights.
                    for sel in LAYOUT_SELECTORS:
                        for prop in LAYOUT_PROPS:
                            if reference[enabled, width][sel][prop] != actual_layout[sel][prop]:
                                layout_diffs.append([enabled, width, sel, prop,
                                                     reference[enabled, width][sel][prop], actual_layout[sel][prop]])
                    position = page.locator('#menu').evaluate('(e) => getComputedStyle(e).position')
                    assert position == ('static' if width <= 900 else 'fixed' if enabled else 'absolute'), (theme, width, enabled, position)
                    username = page.locator('#userinfo_username').bounding_box()
                    major = page.locator('#userinfo_major').bounding_box()
                    assert (major['x'] >= username['x'] + username['width'] if width > 900
                            else major['y'] >= username['y'] + username['height']), (theme, width, 'userinfo overlap')
                    alert_box = page.locator('.alertbar').bounding_box()
                    assert alert_box['width'] <= width, (theme, width, 'alert clipped')
                    y = page.locator('#menu').bounding_box()['y']
                    page.evaluate('scrollTo(0, 500)')
                    if enabled and width > 900:
                        assert page.locator('#menu').bounding_box()['y'] == y == 0
                    else:
                        assert page.locator('#menu').bounding_box()['y'] < y
                    page.evaluate('scrollTo(0, 0)')
                    alert = page.locator('#alert-link')
                    alert_clear = alert.evaluate('''e => { const r=e.getBoundingClientRect();
                        const target=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
                        return target === e || e.contains(target); }''')
                    if not alert_clear:
                        report['failures'].append([theme, width, enabled, 'alert blocked'])
                    if width in [375, 1440] and enabled:
                        (ROOT / 'validation/screenshots').mkdir(exist_ok=True)
                        page.screenshot(path=str(ROOT / f'validation/screenshots/{theme}-{width}.png'))
                    checks += 1
            report['themes'][theme] = {'archiveSha256': hashlib.sha256(old_bytes).hexdigest(),
                                      'viewportModeChecks': checks, 'colorDifferences': color_diffs,
                                      'stateDifferences': state_diffs, 'layoutDifferences': layout_diffs}
            print(theme, 'colors', len(color_diffs), 'states', len(state_diffs), 'layout', len(layout_diffs))
        browser.close()
    (ROOT / 'validation/report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    assert not report['failures'] and all(not data['colorDifferences'] and not data['stateDifferences'] and not data['layoutDifferences']
               for data in report['themes'].values()), 'Inspect validation/report.json'


if __name__ == '__main__':
    main()
