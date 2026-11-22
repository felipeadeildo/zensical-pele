# Working on zensical-pele

zensical-pele is a Python Markdown extension, registered as `pele`, with the
module `zensical_pele`. It renders `mermaid` fences as elements that Pele
mounts in the browser. The docs in `docs/` are a Zensical site that uses the
extension and publishes llms.txt.

## Commands

```sh
uv sync
uv run pytest
uv run ruff format && uv run ruff check
uv run ty check
uv run pytest -m browser
uv run zensical build --clean --strict
uv run scripts/sync_pele_examples.py
```

Run the browser tests after changing `src/zensical_pele/assets/` or anything
that changes the page HTML.

## Conventions

- Commits follow Conventional Commits, one short line: `feat: add module_url option`.
- Comments explain a reason the code can't show, in one short line. No section
  banners, separators or ASCII art.
- Names say what a thing is or does: `FenceRegistration`, `render_page_assets`.
- `docs/examples/` and the example entries of the `nav` in `zensical.toml` are
  generated. Change `scripts/sync_pele_examples.py` instead.
- Docs follow the layout of https://pele.run: a flat sidebar, few pages, plain
  Markdown with no cards or icons. A new page goes in the `nav` and in the
  `llmstxt.sections` of `zensical.toml`.
- Load the `technical-writing`, `writing-for-humans` and `unslop` skills before
  writing docs or the README.
