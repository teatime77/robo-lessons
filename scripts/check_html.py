"""Sphinx生成HTMLのローカル参照とアンカーを確認する（外部通信なし）。"""

from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


class References(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.source = source
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append((self.getpos()[0], attrs[key]))


def check(directory):
    root = directory.resolve()
    pages = {}
    for source in sorted(root.rglob("*.html")):
        parser = References(source)
        parser.feed(source.read_text(encoding="utf-8"))
        pages[source] = parser
    if not pages or root / "index.html" not in pages:
        print(f"HTMLの目次が見つかりません: {root / 'index.html'}", file=sys.stderr)
        return 1

    errors = []
    checked = 0
    for source, page in pages.items():
        for line, reference in page.links:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if not path:
                target = source
            elif path.startswith("/"):
                target = root / path.lstrip("/")
            else:
                target = source.parent / path
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            checked += 1
            if not target.is_file():
                errors.append(f"{source.relative_to(root)}:{line}: ファイルなし: {reference}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{source.relative_to(root)}:{line}: アンカーなし: {reference}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"HTML {len(pages)}ページ、ローカル参照 {checked}件: 参照切れなし")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("使い方: python scripts/check_html.py _build/html")
    raise SystemExit(check(Path(sys.argv[1])))
