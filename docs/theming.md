---
title: Theming
description: Change the colors and fonts of diagrams, or style one diagram.
---

# Theming

Pele draws diagrams with [CSS variables](https://pele.run/theming).
zensical-pele sets them from the variables of the Zensical theme, so diagrams
use your palette in light and dark mode.

## Variables

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

Node borders and highlights follow the `accent` of your palette:

```toml
[[project.theme.palette]]
scheme = "default"
accent = "deep purple"
```

## Override colors

Set the variables in a stylesheet:

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

```toml
[project]
extra_css = ["stylesheets/diagrams.css"]
```

The [Pele theming guide](https://pele.run/theming) lists every variable,
including chart series, critical tasks and font weights. To drop the mapping
and start from Pele's own colors, set [`theme`](configuration.md#theme) to
`false`.

## Style one diagram

With the `attr_list` extension, attributes on the code block go to the diagram
element:

````markdown
``` { .mermaid #checkout-flow }
flowchart LR
  Cart --> Payment --> Done
```
````

``` { .mermaid #checkout-flow }
flowchart LR
  Cart --> Payment --> Done
```

Pele gives each node a `data-id` with its id from the source. This rule
highlights the `Done` node:

```css
#checkout-flow .pele-node[data-id="Done"] .pele-label {
  fill: var(--md-accent-fg-color);
  font-weight: bold;
}
```

Colors set inside a diagram, with `style` or `classDef`, are fixed and don't
change with the color scheme.
