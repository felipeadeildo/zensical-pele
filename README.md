# zensical-pele

zensical-pele renders the Mermaid diagrams of a [Zensical](https://zensical.org)
or MkDocs site with [Pele](https://pele.run) instead of Mermaid.js. You keep
writing ` ```mermaid ` blocks, and readers get diagrams in your theme colors
that adapt to small screens.

Documentation and a gallery of every diagram type:
https://felipeadeildo.github.io/zensical-pele/

## Usage

Try it on a Zensical site without changing the project:

```sh
uvx --with zensical-pele zensical serve
```

To keep it, add the package and enable the extension in `zensical.toml`:

```sh
uv add zensical-pele
```

```toml
[project.markdown_extensions.zensical_pele]
```

With MkDocs, list it in `mkdocs.yml` after `pymdownx.superfences`:

```yaml
markdown_extensions:
  - pymdownx.superfences
  - zensical_pele
```

The [configuration page](https://felipeadeildo.github.io/zensical-pele/configuration/)
covers pinning the Pele version, serving Pele from your own site and passing
options to Pele.

## Development

The project uses [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run pytest
uv run ruff format && uv run ruff check
uv run ty check
uv run zensical serve
```

The browser tests build the docs and check every diagram in Chromium:

```sh
uv run --group browser playwright install chromium
uv run --group browser pytest -m browser
```

The gallery in `docs/examples/` is generated from https://pele.run/examples.
Regenerate it with:

```sh
uv run scripts/sync_pele_examples.py
```

## License

MIT. The gallery examples come from the Pele documentation, which is MIT
licensed, and many of them from Mermaid, also MIT licensed.
