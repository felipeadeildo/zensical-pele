---
title: Colors and fonts
description: How diagrams take the colors and fonts of your Zensical theme.
icon: lucide/palette
---

# Colors and fonts

Pele draws diagrams with [CSS variables](https://pele.run/theming).
zensical-pele sets those variables from the variables of the Zensical theme, so
diagrams match your palette in light and dark mode. Switching the color scheme
changes the variables, and the diagrams follow without being drawn again.

## Default mapping

| Pele variable        | Zensical variable                   | Used for                  |
| -------------------- | ----------------------------------- | ------------------------- |
| `--pele-bg`          | `--md-default-bg-color`             | Backgrounds               |
| `--pele-fg`          | `--md-default-fg-color`             | Text                      |
| `--pele-muted`       | `--md-default-fg-color--light`      | Secondary text            |
| `--pele-line`        | `--md-default-fg-color--light`      | Edges and arrowheads      |
| `--pele-surface`     | `--md-accent-fg-color--transparent` | Node fill                 |
| `--pele-surface-alt` | `--md-code-bg-color`                | Subgraph fill             |
| `--pele-border`      | `--md-accent-fg-color`              | Node and subgraph borders |
| `--pele-accent`      | `--md-accent-fg-color`              | Highlights                |
| `--pele-font`        | `--md-text-font-family`             | Labels                    |
| `--pele-font-mono`   | `--md-code-font-family`             | Monospace labels          |

The accent color comes from the `accent` setting of your palette:

```toml
[[project.theme.palette]]
scheme = "default"
accent = "deep purple"
```

## Override colors

Add a stylesheet with your own values:

=== "docs/stylesheets/diagrams.css"

    ```css
    .pele-diagram {
      --pele-surface: var(--md-primary-fg-color--light);
      --pele-border: var(--md-primary-fg-color);
      --pele-radius: 8px;
    }

    [data-md-color-scheme="slate"] .pele-diagram {
      --pele-line: var(--md-default-fg-color);
    }
    ```

=== "zensical.toml"

    ```toml
    [project]
    extra_css = ["stylesheets/diagrams.css"]
    ```

Pele also has variables for chart series (`--pele-series-1` to
`--pele-series-8`), critical tasks, errors and font weights. The
[Pele theming guide](https://pele.run/theming) lists them all. To style one
diagram instead of all of them, see [Style a diagram](../authoring/styling.md).

## `theme`

Set `theme` to `false` to drop the mapping and start from Pele's own colors,
then set the variables you want in a stylesheet:

```toml
[project.markdown_extensions.pele]
theme = false
```
