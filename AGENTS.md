# Working on zensical-pele

zensical-pele is a Python Markdown extension. It renders `mermaid` fences as
elements that Pele mounts in the browser. The docs in `docs/` are a Zensical
site that uses the extension.

## Commands

```sh
uv sync
uv run pytest
uv run ruff format && uv run ruff check
uv run ty check
uv run --group browser pytest -m browser
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
- `docs/examples/` and the gallery entries of the `nav` in `zensical.toml` are
  generated. Change `scripts/sync_pele_examples.py` instead.
- Load the `technical-writing`, `writing-for-humans` and `unslop` skills before
  writing docs or the README.
