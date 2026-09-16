"""Exercise the actual preview controls and capture it with live public images."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from playwright.sync_api import sync_playwright
from build_themes import ROOT


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    output = ROOT / 'validation/screenshots'
    output.mkdir(exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path='/usr/bin/google-chrome-stable', headless=True)
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/validation/preview.html')
            for theme in ['Midnight', 'Blue']:
                page.select_option('#theme-select', theme)
                page.wait_for_function('theme => document.querySelector("#theme").sheet?.href.endsWith(`BJ-${theme}.css`)', arg=theme)
                # A stylesheet swap is not a navigation: networkidle may still
                # refer to the previous page load. Wait for its paint and images.
                expected = 'rgb(23, 59, 117)' if theme == 'Blue' else 'rgb(198, 199, 207)'
                page.mouse.move(1439, 999)
                page.wait_for_function('color => getComputedStyle(document.querySelector("#sample-link")).color === color', arg=expected)
                failed_images = page.evaluate('''async () => {
                  const urls = new Set([...document.querySelectorAll('*')].flatMap(e =>
                    [...getComputedStyle(e).backgroundImage.matchAll(/url\\("([^\"]+)"\\)/g)].map(m => m[1])));
                  return (await Promise.all([...urls].map(url => new Promise(resolve => {
                    const img = new Image(); img.onload = () => resolve(null);
                    img.onerror = () => resolve(url); img.src = url;
                  })))).filter(Boolean);
                }''')
                assert not failed_images, failed_images
                for width in [1440, 375]:
                    page.set_viewport_size({'width': width, 'height': 1000})
                    page.evaluate('scrollTo(0,0)')
                    page.screenshot(path=str(output / f'preview-{theme}-{width}.png'))
                page.set_viewport_size({'width': 1440, 'height': 1000})
                page.uncheck('#fixed-toggle')
                assert page.locator('#menu').evaluate('e => getComputedStyle(e).position') == 'absolute'
                page.check('#fixed-toggle')
                assert page.locator('#menu').evaluate('e => getComputedStyle(e).position') == 'fixed'
            assert not errors, errors
            browser.close()
        print('Prévia: troca de tema e menu validados; quatro capturas com imagens públicas.')
    finally:
        server.shutdown()
        server.server_close()
