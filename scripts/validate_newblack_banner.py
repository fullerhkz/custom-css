"""Reproduce the opaque-logo regression and check actual banner visibility."""
import json
import re
import urllib.request

from playwright.sync_api import sync_playwright
from build_themes import ROOT

BANNER = 'https://i.bj-share.info/d8837e6abd86bcefd987e116dc58b4ef.png'


if __name__ == '__main__':
    with urllib.request.urlopen(BANNER, timeout=20) as response:
        assert response.headers.get('Content-Type', '').startswith('image/')
        banner_bytes = response.read()
    fixture = (ROOT / 'validation/preview.html').read_text()
    fixture = re.sub(r'<script>[\s\S]*?</script>|<link[^>]*>', '', fixture)
    current = (ROOT / 'BJ-NewBlack.css').read_text()
    previous = (ROOT / 'old/d0d6041/BJ-NewBlack.css').read_text()
    report = {'banner': BANNER, 'previousRegressionReproduced': False, 'checks': []}
    screenshots = ROOT / 'validation/screenshots'
    screenshots.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/google-chrome-stable', headless=True)
        page = browser.new_page()
        page.route('**/*', lambda route: route.fulfill(body=banner_bytes, content_type='image/png')
                   if route.request.url == BANNER else route.abort())

        def render(text, width, enabled):
            page.set_viewport_size({'width': width, 'height': 900})
            if not enabled:
                text = text.replace('@media all {', '@media not all {')
            page.set_content(fixture + '<style>' + text + '</style>')
            page.add_style_tag(content='* { animation: none !important; transition: none !important; }')
            page.mouse.move(width - 1, 899)
            dimensions = page.evaluate('''url => new Promise((resolve, reject) => {
                const image = new Image();
                image.onload = () => resolve([image.naturalWidth, image.naturalHeight]);
                image.onerror = reject; image.src = url;
            })''', BANNER)
            assert all(dimensions)
            assert BANNER in page.locator('#header').evaluate('e => getComputedStyle(e).backgroundImage')

        def logo_pixels():
            return page.locator('#logo').screenshot()

        def transparent_reference():
            page.add_style_tag(content='#logo { background-color: transparent !important; }')
            return logo_pixels()

        # This must fail for the deployed version reported in bug.png.
        render(previous, 1910, True)
        before = logo_pixels()
        (screenshots / 'NewBlack-banner-before.png').write_bytes(before)
        assert before != transparent_reference(), 'The test did not reproduce the black overlay'
        report['previousRegressionReproduced'] = True

        for width in [375, 900, 1440, 1910]:
            for enabled in [True, False]:
                render(current, width, enabled)
                actual = logo_pixels()
                assert actual == transparent_reference(), (width, enabled, 'Banner covered by #logo')
                report['checks'].append({'width': width, 'fixedMenu': enabled, 'bannerVisible': True})
                if enabled and width in [375, 1910]:
                    page.screenshot(path=str(screenshots / f'NewBlack-banner-fixed-{width}.png'))
        browser.close()
    (ROOT / 'validation/newblack-banner.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Falha anterior reproduzida; banner visível em 8 cenários, incluindo celular e menu desligado.')
