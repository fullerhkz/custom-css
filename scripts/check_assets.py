"""Check every active image URL without accessing an authenticated account."""
from concurrent.futures import ThreadPoolExecutor
import json
import re
import urllib.request
from build_themes import ROOT


def check(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method='HEAD'), timeout=20) as response:
            return {'url': url, 'status': response.status, 'type': response.headers.get('content-type')}
    except Exception as error:
        return {'url': url, 'error': str(error)}


if __name__ == '__main__':
    urls = sorted({url for path in (ROOT / 'new').glob('*.css')
                   for url in re.findall(r'url\("([^\"]+)"\)', path.read_text())})
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(check, urls))
    (ROOT / 'validation/assets.json').write_text(json.dumps(results, indent=2) + '\n')
    for result in results:
        if result.get('status') != 200 or not result.get('type', '').startswith('image/'):
            print(result)
    print(f'{sum(r.get("status") == 200 for r in results)}/{len(results)} URLs retornaram HTTP 200.')
    assert all(r.get('status') == 200 and r.get('type', '').startswith('image/') for r in results)
