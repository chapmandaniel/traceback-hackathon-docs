TRACEBACK DOCUMENTATION SITE

The .md files are the editable source. The adjacent .html files and assets/
are generated. Open project-docs/index.html directly in a browser. The site, search,
navigation, styles, and static diagrams work offline without a server.

Reading requires no installation. To rebuild, use Python 3.10+ and the pinned
dependency in requirements.txt.

After extracting the ZIP, run these commands from the directory containing
project-docs/. They create build dependencies in a separate sibling folder,
traceback-docs-build/, so the documentation builder never scans them:

  python3 -m venv traceback-docs-build/venv
  traceback-docs-build/venv/bin/python -m pip install -r project-docs/site-tools/requirements.txt
  traceback-docs-build/venv/bin/python project-docs/site-tools/build.py

These commands use macOS/Linux virtual-environment paths. On Windows, use
traceback-docs-build\venv\Scripts\python.exe for the environment's Python.

The builder preserves existing static diagram assets keyed by source hash.
When adding or editing Mermaid diagrams, install the optional local renderer:
  PUPPETEER_SKIP_DOWNLOAD=1 npm install --prefix traceback-docs-build/mermaid --no-audit --no-fund --save-exact @mermaid-js/mermaid-cli@11.12.0

Then build with a locally installed Chrome executable, for example on macOS:
  traceback-docs-build/venv/bin/python project-docs/site-tools/build.py --mermaid-cli traceback-docs-build/mermaid/node_modules/.bin/mmdc --chrome-bin '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

The optional renderer setup above uses macOS/Linux shell syntax. On other
systems, set PUPPETEER_SKIP_DOWNLOAD in that shell, use its executable paths,
and supply the installed Chrome location. Mermaid rendering is only needed
when changing a diagram; the included SVGs work without these dependencies.

Without a renderer or cached SVG, the diagram remains readable source and
the build reports a warning. Runtime Mermaid JavaScript is unnecessary.

Publish or distribute the whole project-docs folder, retaining its structure.
Do not distribute only index.html: pages, local assets, search index, and
Markdown source links depend on their relative paths.

Navigation follows the macro-to-micro groups declared in build.py. New
Markdown files within an existing group are discovered automatically.
README.md becomes index.html; other Markdown files retain their stem.
Python-Markdown generates stable heading anchors; explicit HTML anchors
in source documents are preserved. Local document links are rewritten.

Design: quiet editorial reading canvas; warm off-white and deep teal;
left navigation, central document, right section inspector. Focused search,
mobile dialog navigation, active-section tracking, and reduced-motion support.
