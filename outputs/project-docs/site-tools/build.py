#!/usr/bin/env python3
"""Build an offline, linked HTML edition of the adjacent Markdown documentation."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit, urlunsplit

import markdown

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
GROUPS = [
    ("Project", "", ["README.md", "project-scope.md", "system-architecture.md", "delivery-plan.md", "decisions.md"]),
    ("01 / Web app & ETL", "pillars/01-web-app-and-etl", ["README.md", "web-experience.md", "fi-data-contract.md", "etl-and-lineage.md"]),
    ("02 / Knowledge & retrieval", "pillars/02-knowledge-and-retrieval", ["README.md", "knowledge-contract.md", "retrieval-workflow.md"]),
    ("03 / Graph investigator", "pillars/03-graph-investigator", ["README.md", "investigation-workflow.md", "resolution-workflow.md"]),
    ("Shared contracts & proof", "shared", []),
]

def html_path(source: Path) -> Path:
    return source.with_name("index.html") if source.name == "README.md" else source.with_suffix(".html")

def rel(target: Path, current: Path) -> str:
    return Path(os.path.relpath(target, current.parent)).as_posix()

def escape(value: object) -> str:
    return html.escape(str(value), quote=True)

def title_of(text: str) -> str:
    result = re.search(r"^#\s+(.+)$", text, re.M)
    return result.group(1).strip() if result else "Documentation"

def nav_label(source: Path, title: str) -> str:
    if source.name == "README.md":
        return "Start here" if source.parent == ROOT else "Overview"
    return title

def strip_html(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mermaid-cli", type=Path, help="Local mmdc executable for static SVG rendering")
    parser.add_argument("--chrome-bin", type=Path, help="Existing Chrome executable used only while building")
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    for asset in ("site.css", "site.js"):
        shutil.copy2(Path(__file__).parent / asset, ASSETS / asset)

    sources = {p: p.read_text(encoding="utf-8") for p in ROOT.rglob("*.md") if "site-tools" not in p.parts}
    groups = []
    ordered = []
    for group_name, folder, names in GROUPS:
        base = ROOT / folder
        candidates = [base / n for n in names]
        candidates += sorted(p for p in sources if p.parent == base and p not in candidates)
        pages = [p for p in candidates if p in sources]
        if pages:
            groups.append((group_name, pages))
            ordered.extend(pages)
    extras = sorted(set(sources) - set(ordered))
    if extras:
        groups.append(("Additional documentation", extras))
        ordered.extend(extras)
    titles = {p: title_of(sources[p]) for p in ordered}
    page_groups = {p: name for name, pages in groups for p in pages}
    rendered = {}
    index = []
    warnings = []

    def render_diagram(match: re.Match, page: Path) -> str:
        source = match.group(1).strip()
        digest = hashlib.sha256(source.encode()).hexdigest()[:16]
        target = ASSETS / f"diagram-{digest}.svg"
        if not target.exists() and args.mermaid_cli:
            with tempfile.TemporaryDirectory(prefix="traceback-diagram-") as temporary:
                temp = Path(temporary)
                input_path = temp / "diagram.mmd"
                input_path.write_text(source)
                config = temp / "theme.json"
                config.write_text(json.dumps({"theme": "base", "themeVariables": {"fontFamily": "Arial, sans-serif", "primaryColor": "#e9f2ee", "primaryTextColor": "#243932", "primaryBorderColor": "#80a296", "lineColor": "#64786f", "secondaryColor": "#f5f5ee", "tertiaryColor": "#f9f8f4"}, "flowchart": {"htmlLabels": False, "curve": "basis"}}))
                command = [str(args.mermaid_cli.resolve()), "-i", str(input_path), "-o", str(target), "-b", "transparent", "-c", str(config)]
                if args.chrome_bin:
                    browser = temp / "puppeteer.json"
                    browser.write_text(json.dumps({"executablePath": str(args.chrome_bin), "args": ["--no-sandbox"]}))
                    command += ["-p", str(browser)]
                subprocess.run(command, check=True, capture_output=True, text=True)
        if target.exists():
            return f'\n<figure class="diagram"><a href="{escape(rel(target, html_path(page)))}" target="_blank" rel="noopener" aria-label="Open full-size architecture diagram"><img src="{escape(rel(target, html_path(page)))}" alt="Architecture diagram showing the relationships and evidence flow described in this section"></a><figcaption>Architecture relationships · select to open full size</figcaption></figure>\n'
        warnings.append(f"Diagram source retained in {page.relative_to(ROOT)}; install Mermaid CLI and rebuild to render.")
        return "\n```text\n" + source + "\n```\n"

    for page in ordered:
        text = re.sub(r"```mermaid\s*\n(.*?)\n```", lambda m: render_diagram(m, page), sources[page], flags=re.S)
        md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"], extension_configs={"toc": {"permalink": False, "toc_depth": "2-3"}})
        content = md.convert(text)

        def rewrite(match: re.Match) -> str:
            value = html.unescape(match.group(1))
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path.endswith(".md"):
                return match.group(0)
            source_target = (page.parent / unquote(parsed.path)).resolve()
            if source_target in sources:
                new_path = rel(html_path(source_target), html_path(page))
                value = urlunsplit(("", "", new_path, parsed.query, parsed.fragment))
            return f'href="{escape(value)}"'

        content = re.sub(r'href="([^"]+)"', rewrite, content)
        content = re.sub(r"<table>(.*?)</table>", r'<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable data table"><table>\1</table></div>', content, flags=re.S)
        # The canonical Markdown keeps its cross-links; the HTML shell provides this navigation.
        content = re.sub(r'<p>(?:<a href="[^"]+">[^<]+</a>\s*(?:[·|]\s*)?){2,}</p>', "", content)
        content = re.sub(r'<p><strong>Status:</strong>(.*?)</p>', r'<p class="document-status"><span class="status-dot" aria-hidden="true"></span><strong>Status:</strong>\1</p>', content)
        rendered[page] = (content, md.toc)
        index.append({"title": titles[page], "group": page_groups[page], "url": html_path(page).relative_to(ROOT).as_posix(), "text": strip_html(content)})

    (ASSETS / "search-index.js").write_text("window.TRACEBACK_SEARCH = " + json.dumps(index, ensure_ascii=False).replace("</", "<\\/") + ";\n", encoding="utf-8")

    for position, page in enumerate(ordered):
        output = html_path(page)
        home = rel(ROOT / "index.html", output)
        base = rel(ROOT, output)
        asset = lambda name: escape(rel(ASSETS / name, output))
        navigation = []
        for name, pages in groups:
            links = []
            for item in pages:
                current = ' aria-current="page"' if item == page else ""
                links.append(f'<a href="{escape(rel(html_path(item), output))}"{current}>{escape(nav_label(item, titles[item]))}</a>')
            navigation.append(f'<section class="nav-group"><h2>{escape(name)}</h2>{"".join(links)}</section>')
        nav = "".join(navigation)
        crumbs = [f'<a href="{escape(home)}">Documentation</a>']
        if page.parent != ROOT:
            parent = page.parent / "README.md"
            group_title = page_groups[page].split(" / ", 1)[-1]
            if parent in sources and parent != page:
                crumbs.append(f'<a href="{escape(rel(html_path(parent), output))}">{escape(group_title)}</a>')
            elif page.name != "README.md":
                crumbs.append(f'<span>{escape(group_title)}</span>')
        if page != ROOT / "README.md":
            crumbs.append(f'<span aria-current="page">{escape(nav_label(page, titles[page]))}</span>')
        previous = ordered[position - 1] if position else None
        following = ordered[position + 1] if position + 1 < len(ordered) else None
        footer = []
        for other, direction in ((previous, "Previous"), (following, "Next")):
            if other:
                footer.append(f'<a class="page-{direction.lower()}" href="{escape(rel(html_path(other), output))}"><span>{direction}</span><strong>{escape(nav_label(other, titles[other]))}</strong><small>{escape(page_groups[other])}</small></a>')
        body, toc = rendered[page]
        search_icon = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg>'
        page_html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{escape(titles[page])} · Traceback</title><meta name="description" content="Traceback project planning documentation: scope, three pillars, interfaces, and acceptance criteria."><link rel="stylesheet" href="{asset('site.css')}"><script defer src="{asset('search-index.js')}"></script><script defer src="{asset('site.js')}"></script></head>
<body data-root="{escape(base)}"><a class="skip-link" href="#main">Skip to content</a><noscript><style>.search-button,.menu-button,.compact-search{{display:none!important}}</style><details class="no-script-nav"><summary>Traceback documentation navigation</summary><nav aria-label="Documentation">{nav}</nav></details></noscript>
<aside class="sidebar"><a class="wordmark" href="{escape(home)}"><span class="brand-mark" aria-hidden="true">t</span>Traceback<span class="wordmark-detail">PROJECT DOCS</span></a><button class="search-button" data-search-open>{search_icon}<span>Search documentation</span><kbd>⌘ K</kbd></button><nav aria-label="Documentation">{nav}</nav><div class="sidebar-foot">Working documentation<br><span>Scope → systems → contracts</span></div></aside>
<div class="page-shell"><header class="topbar"><button class="menu-button" data-nav-open aria-label="Open documentation navigation" aria-haspopup="dialog"><svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" fill="none" stroke-width="1.6" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button><nav class="breadcrumbs" aria-label="Breadcrumb">{'<span class="crumb-divider" aria-hidden="true">/</span>'.join(crumbs)}</nav><button class="compact-search" data-search-open aria-label="Search documentation">{search_icon}</button><a class="source-link" href="{escape(rel(page, output))}">Markdown source <span aria-hidden="true">↗</span></a></header>
<div class="reading-layout"><main id="main" class="document" tabindex="-1"><div class="page-eyebrow">{escape(page_groups[page])}</div><article>{body}</article><nav class="page-pagination" aria-label="Adjacent pages">{''.join(footer)}</nav><footer class="document-footer">Traceback · Project planning<a href="{escape(rel(page, output))}">Open Markdown source</a></footer></main><aside class="page-toc" aria-label="On this page"><div class="toc-inner"><h2>On this page</h2>{toc}<a class="back-to-top" href="#main">Back to top ↑</a></div></aside></div></div>
<dialog class="mobile-nav" aria-label="Documentation navigation"><div class="dialog-heading"><strong>Traceback documentation</strong><button data-dialog-close aria-label="Close navigation">×</button></div><nav aria-label="Mobile documentation">{nav}</nav></dialog>
<dialog class="search-dialog" aria-labelledby="search-title"><div class="search-heading"><label id="search-title" for="doc-search">Search documentation</label><button data-dialog-close aria-label="Close search">×</button></div><div class="search-input-wrap">{search_icon}<input id="doc-search" type="search" autocomplete="off" placeholder="Search scope, contracts, investigation…" spellcheck="false"></div><p class="search-status" id="search-status" role="status">Search across all project documents.</p><div class="search-results" id="search-results"></div><div class="search-footer">Search works offline.<span><kbd>esc</kbd> to close</span></div></dialog>
</body></html>'''
        output.write_text(page_html, encoding="utf-8")
    print(f"Built {len(ordered)} pages with offline search and {len(list(ASSETS.glob('diagram-*.svg')))} static diagrams.")
    for warning in sorted(set(warnings)):
        print("WARNING:", warning)

if __name__ == "__main__":
    main()
