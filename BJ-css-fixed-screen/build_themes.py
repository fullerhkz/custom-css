#!/usr/bin/env python3
"""Build responsive, standalone BJ-Share themes from the css2 model.

The layout and responsive behavior come from examples/css2-midnight.css.
Visual declarations are transferred from each legacy theme when an equivalent
selector/property exists, so logos, colors and theme-specific assets survive.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent
TEMPLATE = PROJECT / "examples" / "css2-midnight.css"

THEMES = (
    "BJ-Black.css",
    "BJ-Blue.css",
    "BJ-Clean.css",
    "BJ-DarkBlue.css",
    "BJ-Darkness.css",
    "BJ-Grey.css",
    "BJ-Midnight.css",
    "BJ-NewBlack.css",
    "BJ-Pink.css",
    "BJ-Red.css",
)

# Variables cover declarations introduced by the new model that have no
# equivalent in the legacy files. Existing theme declarations still take
# precedence when transferred by selector/property below.
PALETTES = {
    "BJ-Black.css": {
        "scheme": "dark",
        "bg-deep": "#151515",
        "bg-base": "#303030",
        "bg-surface": "#1c1c1c",
        "bg-raised": "#282828",
        "bg-overlay": "#353535",
        "bg-header": "#1d1d1d",
        "border": "#3a3a3a",
        "border-sub": "#303030",
        "text-primary": "#ccc",
        "text-muted": "#999",
        "text-bright": "#fff",
        "accent": "#5c8eac",
        "gold": "#eebc58",
        "green": "#4db87a",
        "red": "#d95b5b",
        "input-text": "#ddd",
        "surface-1c": "#1c1c1c",
        "surface-1e": "#282828",
        "btn-grad-dark": "#151515",
        "btn-grad-mid": "#303030",
    },
    "BJ-Blue.css": {
        "scheme": "light",
        "bg-deep": "#6f96d0",
        "bg-base": "#fafafa",
        "bg-surface": "#fff",
        "bg-raised": "#fff",
        "bg-overlay": "#e5edf8",
        "bg-header": "#9abcf0",
        "border": "#cacaca",
        "border-sub": "#d7d7d7",
        "text-primary": "#111",
        "text-muted": "#555",
        "text-bright": "#173b75",
        "accent": "#173b75",
        "gold": "#8a6500",
        "green": "#237a3b",
        "red": "#b33131",
        "input-text": "#222",
        "surface-1c": "#f4f4f4",
        "surface-1e": "#eaeaea",
        "btn-grad-dark": "#dce8f8",
        "btn-grad-mid": "#fff",
    },
    "BJ-Clean.css": {
        "scheme": "light",
        "bg-deep": "#d5d5d5",
        "bg-base": "#eaeaea",
        "bg-surface": "#e8e8e8",
        "bg-raised": "#fff",
        "bg-overlay": "#f2f2f2",
        "bg-header": "#f2f2f2",
        "border": "#cacaca",
        "border-sub": "#ddd",
        "text-primary": "#111",
        "text-muted": "#666",
        "text-bright": "#1e4754",
        "accent": "#1e6278",
        "gold": "#846000",
        "green": "#237a3b",
        "red": "#b33131",
        "input-text": "#222",
        "surface-1c": "#f7f7f7",
        "surface-1e": "#eee",
        "btn-grad-dark": "#ddd",
        "btn-grad-mid": "#fff",
    },
    "BJ-DarkBlue.css": {
        "scheme": "dark",
        "bg-deep": "#0e0e11",
        "bg-base": "#151518",
        "bg-surface": "#1a1a1e",
        "bg-raised": "#1c1c20",
        "bg-overlay": "#2a2a34",
        "bg-header": "#1a1a1e",
        "border": "#38383f",
        "border-sub": "#2b2b33",
        "text-primary": "#c6c7cf",
        "text-muted": "#999",
        "text-bright": "#e8e8f0",
        "accent": "#5b8dd9",
        "gold": "#eebc58",
        "green": "#4db87a",
        "red": "#d95b5b",
        "input-text": "#e0e0e0",
        "surface-1c": "#1c1c20",
        "surface-1e": "#1e1e23",
        "btn-grad-dark": "#14141a",
        "btn-grad-mid": "#2a2a38",
    },
    "BJ-Darkness.css": {
        "scheme": "dark",
        "bg-deep": "#101010",
        "bg-base": "#18181a",
        "bg-surface": "#181818",
        "bg-raised": "#202021",
        "bg-overlay": "#2b2b2d",
        "bg-header": "#1a1a1a",
        "border": "#303030",
        "border-sub": "#292929",
        "text-primary": "#bdc0c5",
        "text-muted": "#777",
        "text-bright": "#e0e0e6",
        "accent": "#718fae",
        "gold": "#eebc58",
        "green": "#4db87a",
        "red": "#d95b5b",
        "input-text": "#ddd",
        "surface-1c": "#1c1c1c",
        "surface-1e": "#202021",
        "btn-grad-dark": "#121212",
        "btn-grad-mid": "#292929",
    },
    "BJ-Grey.css": {
        "scheme": "light",
        "bg-deep": "#999",
        "bg-base": "#e2e2e2",
        "bg-surface": "#ccc",
        "bg-raised": "#eaeaea",
        "bg-overlay": "#ddd",
        "bg-header": "#bbb",
        "border": "#666",
        "border-sub": "#aaa",
        "text-primary": "#111",
        "text-muted": "#555",
        "text-bright": "#222",
        "accent": "#3f5966",
        "gold": "#806000",
        "green": "#237a3b",
        "red": "#b33131",
        "input-text": "#222",
        "surface-1c": "#eee",
        "surface-1e": "#ddd",
        "btn-grad-dark": "#bbb",
        "btn-grad-mid": "#eee",
    },
    "BJ-Midnight.css": {
        "scheme": "dark",
        "bg-deep": "#0e0e11",
        "bg-base": "#131316",
        "bg-surface": "#18181c",
        "bg-raised": "#1d1d22",
        "bg-overlay": "#25252e",
        "bg-header": "#1a1a1f",
        "border": "#2e2e38",
        "border-sub": "#252530",
        "text-primary": "#d4d5de",
        "text-muted": "#7c7d8a",
        "text-bright": "#eeeef4",
        "accent": "#5b8dd9",
        "gold": "#eebc58",
        "green": "#4db87a",
        "red": "#d95b5b",
        "input-text": "#e0e0e8",
        "surface-1c": "#1c1c22",
        "surface-1e": "#1e1e24",
        "btn-grad-dark": "#14141a",
        "btn-grad-mid": "#2a2a38",
    },
    "BJ-NewBlack.css": {
        "scheme": "dark",
        "bg-deep": "#141414",
        "bg-base": "#1d1d1d",
        "bg-surface": "#1c1c1c",
        "bg-raised": "#292929",
        "bg-overlay": "#333",
        "bg-header": "#1e1e1e",
        "border": "#303030",
        "border-sub": "#292929",
        "text-primary": "#bbb",
        "text-muted": "#888",
        "text-bright": "#eee",
        "accent": "#4d7c9a",
        "gold": "#eebc58",
        "green": "#4db87a",
        "red": "#d95b5b",
        "input-text": "#ddd",
        "surface-1c": "#202020",
        "surface-1e": "#282828",
        "btn-grad-dark": "#151515",
        "btn-grad-mid": "#303030",
    },
    "BJ-Pink.css": {
        "scheme": "light",
        "bg-deep": "#b66aa5",
        "bg-base": "#eaeaea",
        "bg-surface": "#fff",
        "bg-raised": "#eee",
        "bg-overlay": "#f8e2f3",
        "bg-header": "#eab3e1",
        "border": "#cacaca",
        "border-sub": "#dfb4d7",
        "text-primary": "#111",
        "text-muted": "#6f4869",
        "text-bright": "#6f1064",
        "accent": "#8f267e",
        "gold": "#806000",
        "green": "#237a3b",
        "red": "#b33131",
        "input-text": "#222",
        "surface-1c": "#f8f0f6",
        "surface-1e": "#f2f2f2",
        "btn-grad-dark": "#e2b7da",
        "btn-grad-mid": "#fff",
    },
    "BJ-Red.css": {
        "scheme": "dark",
        "bg-deep": "#151515",
        "bg-base": "#1d1d1d",
        "bg-surface": "#1c1c1c",
        "bg-raised": "#282828",
        "bg-overlay": "#373030",
        "bg-header": "#303030",
        "border": "#3a3030",
        "border-sub": "#302828",
        "text-primary": "#bbb",
        "text-muted": "#888",
        "text-bright": "#fff",
        "accent": "#bd4a4a",
        "gold": "#eebc58",
        "green": "#4db87a",
        "red": "#e15b5b",
        "input-text": "#ddd",
        "surface-1c": "#202020",
        "surface-1e": "#282828",
        "btn-grad-dark": "#181414",
        "btn-grad-mid": "#3a2929",
    },
}

VISUAL_PROPERTIES = {
    "background",
    "background-color",
    "background-image",
    "background-position",
    "background-repeat",
    "background-size",
    "border",
    "border-bottom",
    "border-bottom-color",
    "border-color",
    "border-left",
    "border-left-color",
    "border-right",
    "border-right-color",
    "border-top",
    "border-top-color",
    "box-shadow",
    "color",
    "fill",
    "outline-color",
    "text-shadow",
}

COMPATIBILITY_SELECTORS = (
    "#content",
    "#logo",
    "#menu",
    ".head",
    ".colhead",
    ".colhead_dark",
    "tr.rowa",
    "table.forum_unread",
    ".head a",
    "#torrent_details .torrentdetails",
    ".forum_post .colhead_dark",
    ".forum_post .colhead_dark a",
    ".torrent_table tr.group_torrent:nth-child(4n)",
    ".torrent_table tr.group_torrent:nth-child(4n+2)",
    "table.torrent_table.cats.numbering.border",
)


def strip_comments(value: str) -> str:
    return re.sub(r"/\*.*?\*/", "", value, flags=re.S)


def split_top_level(value: str, delimiter: str) -> list[str]:
    parts: list[str] = []
    start = 0
    quote: str | None = None
    comment = False
    parens = brackets = 0
    i = 0
    while i < len(value):
        char = value[i]
        pair = value[i : i + 2]
        if comment:
            if pair == "*/":
                comment = False
                i += 2
                continue
        elif quote:
            if char == "\\":
                i += 2
                continue
            if char == quote:
                quote = None
        elif pair == "/*":
            comment = True
            i += 2
            continue
        elif char in "'\"":
            quote = char
        elif char == "(":
            parens += 1
        elif char == ")":
            parens = max(0, parens - 1)
        elif char == "[":
            brackets += 1
        elif char == "]":
            brackets = max(0, brackets - 1)
        elif char == delimiter and not parens and not brackets:
            parts.append(value[start:i])
            start = i + 1
        i += 1
    parts.append(value[start:])
    return parts


def canonical_selector(selector: str) -> str:
    selector = strip_comments(selector).strip()
    selector = re.sub(r"\s+", " ", selector)
    selector = re.sub(r"\s*([>+~])\s*", r"\1", selector)
    selector = re.sub(
        r"\[\s*([\w-]+)\s*=\s*(['\"]?)([^'\"\]]+)\2\s*\]",
        lambda match: f"[{match.group(1)}={match.group(3).strip()}]",
        selector,
    )
    return selector


def selector_list(header: str) -> list[str]:
    return [canonical_selector(part) for part in split_top_level(header, ",")]


def find_blocks(css: str) -> list[tuple[int, int, int, int, str]]:
    """Return header/body spans for direct child blocks in a CSS fragment."""
    blocks: list[tuple[int, int, int, int, str]] = []
    cursor = 0
    length = len(css)
    while cursor < length:
        while cursor < length and (css[cursor].isspace() or css[cursor] == ";"):
            cursor += 1
        if cursor >= length:
            break
        header_start = cursor
        quote: str | None = None
        comment = False
        parens = 0
        while cursor < length:
            pair = css[cursor : cursor + 2]
            char = css[cursor]
            if comment:
                if pair == "*/":
                    comment = False
                    cursor += 2
                    continue
            elif quote:
                if char == "\\":
                    cursor += 2
                    continue
                if char == quote:
                    quote = None
            elif pair == "/*":
                comment = True
                cursor += 2
                continue
            elif char in "'\"":
                quote = char
            elif char == "(":
                parens += 1
            elif char == ")":
                parens = max(0, parens - 1)
            elif char == "{" and not parens:
                break
            elif char == ";" and not parens:
                cursor += 1
                header_start = cursor
            cursor += 1
        if cursor >= length:
            break
        open_brace = cursor
        header = css[header_start:open_brace].strip()
        cursor += 1
        body_start = cursor
        depth = 1
        quote = None
        comment = False
        while cursor < length and depth:
            pair = css[cursor : cursor + 2]
            char = css[cursor]
            if comment:
                if pair == "*/":
                    comment = False
                    cursor += 2
                    continue
            elif quote:
                if char == "\\":
                    cursor += 2
                    continue
                if char == quote:
                    quote = None
            elif pair == "/*":
                comment = True
                cursor += 2
                continue
            elif char in "'\"":
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            cursor += 1
        if depth:
            raise ValueError(f"Unclosed CSS block near: {header[:80]}")
        blocks.append((header_start, open_brace, body_start, cursor - 1, header))
    return blocks


def declaration_map(body: str) -> dict[str, str]:
    declarations: dict[str, str] = {}
    for segment in split_top_level(body, ";"):
        clean = strip_comments(segment).strip()
        if not clean or ":" not in clean:
            continue
        prop, value = clean.split(":", 1)
        prop = prop.strip().lower()
        if re.fullmatch(r"[\w-]+", prop) and value.strip():
            declarations[prop] = value.strip()
    return declarations


def collect_rules(css: str) -> dict[str, dict[str, str]]:
    rules: dict[str, dict[str, str]] = {}

    def visit(fragment: str) -> None:
        for _, _, body_start, body_end, raw_header in find_blocks(fragment):
            header = strip_comments(raw_header).strip()
            body = fragment[body_start:body_end]
            if header.startswith(("@media", "@supports", "@layer", "@container", "@document")):
                visit(body)
            elif not header.startswith("@"):
                declarations = declaration_map(body)
                for selector in selector_list(header):
                    rules.setdefault(selector, {}).update(declarations)

    visit(css)
    return rules


def replace_declarations(
    body: str,
    selectors: list[str],
    theme_rules: dict[str, dict[str, str]],
) -> str:
    replacements: list[tuple[int, int, str]] = []
    cursor = 0
    for segment in split_top_level(body, ";"):
        segment_start = cursor
        segment_end = cursor + len(segment)
        cursor = segment_end + 1
        # Preserve string length while masking comments so a colon inside an
        # explanatory comment cannot be mistaken for the declaration colon.
        masked = re.sub(r"/\*.*?\*/", lambda match: " " * len(match.group()), segment, flags=re.S)
        colon = masked.find(":")
        if colon < 0:
            continue
        prop = masked[:colon].strip().lower()
        if prop not in VISUAL_PROPERTIES:
            continue
        candidates = [
            theme_rules[selector][prop]
            for selector in selectors
            if selector in theme_rules and prop in theme_rules[selector]
        ]
        if not candidates:
            continue
        replacement = Counter(candidates).most_common(1)[0][0]
        real_colon = colon
        value_start = real_colon + 1
        while value_start < len(segment) and segment[value_start].isspace():
            value_start += 1
        value_end = len(segment)
        while value_end > value_start and segment[value_end - 1].isspace():
            value_end -= 1
        replacements.append(
            (segment_start + value_start, segment_start + value_end, replacement)
        )
    for start, end, replacement in reversed(replacements):
        body = body[:start] + replacement + body[end:]
    return body


def transfer_theme(css: str, theme_rules: dict[str, dict[str, str]]) -> str:
    def visit(fragment: str, inside_conditional: bool = False) -> str:
        replacements: list[tuple[int, int, str]] = []
        for _, _, body_start, body_end, raw_header in find_blocks(fragment):
            header = strip_comments(raw_header).strip()
            body = fragment[body_start:body_end]
            if header.startswith(("@media", "@supports", "@layer", "@container", "@document")):
                new_body = visit(body, True)
            elif header.startswith(("@keyframes", "@-webkit-keyframes")):
                new_body = body
            elif not header.startswith("@") and not inside_conditional and header != ":root":
                new_body = replace_declarations(body, selector_list(header), theme_rules)
            else:
                new_body = body
            if new_body != body:
                replacements.append((body_start, body_end, new_body))
        for start, end, replacement in reversed(replacements):
            fragment = fragment[:start] + replacement + fragment[end:]
        return fragment

    return visit(css)


def apply_palette(css: str, palette: dict[str, str]) -> str:
    for name, value in palette.items():
        if name == "scheme":
            continue
        pattern = rf"(--{re.escape(name)}\s*:\s*)[^;]+;"
        css, count = re.subn(pattern, rf"\g<1>{value};", css, count=1)
        if count != 1:
            raise ValueError(f"Variable --{name} was not found exactly once")
    css = css.replace(":root {", f':root {{\n      color-scheme: {palette["scheme"]};', 1)
    return css


def repair_template(css: str) -> str:
    # Fix focus selectors: without :focus the editor iframe/textarea kept a
    # permanent blue glow. Use the theme accent for a consistent focus ring.
    css = css.replace(
        ".sceditor-container iframe,\n.sceditor-container textarea,",
        ".sceditor-container iframe:focus,\n.sceditor-container textarea:focus,",
    )
    css = css.replace("#3463a7", "var(--accent)")
    css = css.replace("#4281da", "var(--accent)")

    # The explanatory comment already promised intrinsic image proportions;
    # the declaration itself was missing.
    css = css.replace(
        "img {\n      border: none;\n      max-width: 100%;\n}",
        "img {\n      border: none;\n      max-width: 100%;\n      height: auto;\n}",
    )

    # left has no effect on a statically positioned ul and obscures intent.
    css = css.replace("      left: 0.5%;\n", "")

    # Keep new-only components theme-aware. Where a legacy theme has a value
    # for the same selector/property, transfer_theme still overrides these.
    semantic_values = {
        "      fill: #676e77;": "      fill: var(--text-muted);",
        "      background: #1d1d23;": "      background: var(--bg-raised);",
        "      background: #202028;": "      background: var(--surface-1e);",
        "      color: #b8b9c8;": "      color: var(--text-primary);",
        "      color: #b8b9ca;": "      color: var(--text-primary);",
        "      color: #c0c2d0;": "      color: var(--text-bright);",
        "      background: rgba(24, 24, 28, 0.98);": "      background: var(--bg-surface);",
        "      background-color: rgba(38, 38, 46, 0.92);": "      background-color: var(--bg-raised);",
        "      background-color: rgba(32, 33, 40, 0.92);": "      background-color: var(--surface-1e);",
        "      background-color: rgba(28, 29, 38, 0.92);": "      background-color: var(--bg-overlay);",
        "      border-left: 2px solid rgb(80, 80, 93);": "      border-left: 2px solid var(--border);",
        "      border-right: 2px solid rgb(80, 80, 93);": "      border-right: 2px solid var(--border);",
        "      border-left: 2px solid rgb(95, 85, 115);": "      border-left: 2px solid var(--accent);",
        "      border-right: 2px solid rgb(95, 85, 115);": "      border-right: 2px solid var(--accent);",
        "      border-left: 2px solid rgb(80, 80, 120);": "      border-left: 2px solid var(--accent);",
        "      border-right: 2px solid rgb(80, 80, 120);": "      border-right: 2px solid var(--accent);",
        "      border: 1px solid #30303a;": "      border: 1px solid var(--border);",
        "      background-color: #1d1d23;": "      background-color: var(--surface-1e);",
        "      color: #fff;": "      color: var(--text-bright);",
        "      color: #aaa !important;": "      color: var(--text-muted) !important;",
        "      background-color: #202028 !important;": "      background-color: var(--surface-1e) !important;",
        "      border-color: #3a3a44 !important;": "      border-color: var(--border) !important;",
        "      background: #1c1c24 !important;": "      background: var(--bg-overlay) !important;",
        "      background-color: #1a1a22;": "      background-color: var(--bg-header);",
        "      color: #e8e8f0;": "      color: var(--text-bright);",
        "      color: #d8d8e4;": "      color: var(--text-bright);",
        "      background: rgba(14, 14, 18, 0.82);": "      background: var(--bg-deep);",
        "      background: #111116;": "      background: var(--bg-deep);",
        "      color: #ccc;": "      color: var(--text-primary);",
        "      color: #555;": "      color: var(--text-muted);",
        "      background: #263a52;": "      background: var(--accent);",
        "      background: linear-gradient(to top, #46464e, #14151a);": "      background: linear-gradient(to top, var(--btn-grad-mid), var(--btn-grad-dark));",
        "      background: linear-gradient(180deg, #141416 0, #303038 1px, #242430 2px, var(--surface-1c));": "      background: linear-gradient(180deg, var(--btn-grad-dark) 0, var(--btn-grad-mid) 1px, var(--btn-grad-mid) 2px, var(--surface-1c));",
        "      background: linear-gradient(180deg, #17171b 0, #232332 1px, #20202a 2px, var(--surface-1c));": "      background: linear-gradient(180deg, var(--btn-grad-dark) 0, var(--btn-grad-mid) 1px, var(--btn-grad-mid) 2px, var(--surface-1c));",
    }
    for old, new in semantic_values.items():
        css = css.replace(old, new)

    # Alternative Midnight logos were implementation notes, not selectable
    # options. Removing them prevents unrelated assets leaking into every file.
    css = re.sub(
        r"\n\s*/\* background: url\(https://i\.bj-share\.info/(?:a9aab389c218de39ab2016adba2e7a4b|39cc9dcf61cc9adcc3f0a90d965c3f55)\.(?:gif|png)\) no-repeat top center; \*/",
        "",
        css,
    )

    # These assets exist on the shared bj-black path (HTTP 200) and relative
    # URLs break when the CSS is loaded outside the original theme directory.
    css = css.replace("url(images/bar.gif)", "url(https://bj-share.info/static/styles/bj-black/images/bar.gif)")
    css = css.replace("url(images/bar_left.gif)", "url(https://bj-share.info/static/styles/bj-black/images/bar_left.gif)")
    css = css.replace("url(images/bar_right.gif)", "url(https://bj-share.info/static/styles/bj-black/images/bar_right.gif)")
    active_page_rule = """

/* Realça a seção atual mesmo quando o backend marca apenas o body. */
#chat #nav_irc,
#collage #nav_collages,
#forums #nav_forums,
#index #nav_index,
#moderar #nav_moderar,
#requests #nav_requests,
#rules #nav_rules,
#staff #nav_staff,
#top10 #nav_top10,
#torrents #nav_torrents,
#user #nav_userinfor,
#wiki #nav_wiki {
      background-color: var(--bg-overlay);
      border-bottom: 2px solid var(--accent);
}
"""
    marker = "\n#menudrop ul ul {"
    if marker not in css:
        raise ValueError("Menu insertion marker not found")
    css = css.replace(marker, active_page_rule + marker, 1)
    return css


def normalize_asset_urls(css: str) -> str:
    """Make shared legacy image paths safe for standalone/custom CSS use."""
    replacements = {
        "url(images/go_last_read.png)": "url(https://bj-share.info/static/styles/bj-black/images/go_last_read.png)",
        "url(images/bar.gif)": "url(https://bj-share.info/static/styles/bj-black/images/bar.gif)",
        "url(images/bar_left.gif)": "url(https://bj-share.info/static/styles/bj-black/images/bar_left.gif)",
        "url(images/bar_right.gif)": "url(https://bj-share.info/static/styles/bj-black/images/bar_right.gif)",
    }
    for relative, absolute in replacements.items():
        css = css.replace(relative, absolute)
    return css


def replace_body_background(css: str, legacy_rules: dict[str, dict[str, str]]) -> str:
    body = legacy_rules.get("body", {})
    value = body.get("background") or body.get("background-color")
    if not value:
        return css
    pattern = re.compile(
        r"(body,\s*\n#userinfo,\s*\n#alerts,.*?\{\s*\n\s*background:\s*)[^;]+;",
        re.S,
    )
    css, count = pattern.subn(rf"\g<1>{value};", css, count=1)
    if count != 1:
        raise ValueError("Shared body background rule was not found")
    return css


def compatibility_rules(legacy_rules: dict[str, dict[str, str]]) -> str:
    chunks: list[str] = []
    for selector in COMPATIBILITY_SELECTORS:
        declarations = legacy_rules.get(canonical_selector(selector))
        if not declarations:
            continue
        visual = {
            prop: value for prop, value in declarations.items() if prop in VISUAL_PROPERTIES
        }
        if not visual:
            continue
        lines = [f"{selector} {{"]
        lines.extend(f"      {prop}: {value};" for prop, value in visual.items())
        lines.append("}")
        chunks.append("\n".join(lines))
    if not chunks:
        return ""
    return (
        "\n\n/* ===== Compatibilidade visual específica deste tema ===== */\n"
        + "\n\n".join(chunks)
        + "\n"
    )


def shared_background_overrides(legacy_rules: dict[str, dict[str, str]]) -> str:
    """Undo the Midnight-only background grouping when a theme differs."""
    chunks: list[str] = []
    for selector in ("body", "#userinfo", "#alerts"):
        declarations = legacy_rules.get(selector, {})
        value = declarations.get("background") or declarations.get("background-color")
        if value:
            chunks.append(f"{selector} {{\n      background: {value};\n}}")
    tooltip_value = (
        legacy_rules.get("a.BJinfoBox span", {}).get("background")
        or legacy_rules.get("a.BJinfoBox span", {}).get("background-color")
        or legacy_rules.get("body", {}).get("background")
        or legacy_rules.get("body", {}).get("background-color")
    )
    if tooltip_value:
        chunks.append(
            "a.BJinfoBox span,\n"
            "form a.BJinfoBox span,\n"
            ".post_return a.BJinfoBox span {\n"
            f"      background: {tooltip_value};\n"
            "}"
        )
    if not chunks:
        return ""
    return "\n\n/* ===== Fundos próprios deste tema ===== */\n" + "\n\n".join(chunks) + "\n"


def theme_header(filename: str) -> str:
    name = filename.removesuffix(".css").removeprefix("BJ-")
    return f"""/*
 * BJ-Share custom CSS — tema {name}
 * Base: css2 responsiva, organizada e corrigida.
 * Arquivo autônomo; não requer importação de outra folha de estilo.
 */

"""


def build() -> None:
    base = repair_template(TEMPLATE.read_text(encoding="utf-8"))
    for filename in THEMES:
        legacy = (PROJECT / filename).read_text(encoding="utf-8")
        legacy_rules = collect_rules(legacy)
        css = base
        if filename != "BJ-Midnight.css":
            css = transfer_theme(css, legacy_rules)
            css = replace_body_background(css, legacy_rules)
        css = apply_palette(css, PALETTES[filename])
        css = normalize_asset_urls(css)
        css = theme_header(filename) + css.lstrip()
        css += compatibility_rules(legacy_rules)
        if filename != "BJ-Midnight.css":
            css += shared_background_overrides(legacy_rules)
        (OUTPUT / filename).write_text(css.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
