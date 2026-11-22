---
title: Migrate from Mermaid.js
description: What changes when a Zensical site with Mermaid diagrams switches to Pele.
icon: lucide/arrow-right-left
---

# Migrate from Mermaid.js

Your Markdown doesn't change. Once the extension is enabled, every
` ```mermaid ` block renders with Pele, and Mermaid.js stops loading, because
Zensical only loads it for `pre.mermaid` elements and the extension doesn't
write any.

## Your configuration

A `mermaid` entry in `custom_fences`, like the one the Zensical docs suggest,
can stay where it is. The extension's fence takes precedence over it, so you
can remove the entry whenever you like:

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" },
]
```

Settings that you passed to Mermaid.js, for example a script that calls
`mermaid.initialize()`, no longer apply. Pele takes its colors and fonts from
CSS variables, which [Colors and fonts](../setup/colors-and-fonts.md) covers.

## How diagrams look

Pele lays out diagrams its own way, so your diagrams won't look exactly as they
did. Read the [Pele compatibility notes](https://pele.run/compatibility) for
the differences, then check the pages with the most complex diagrams.

Colors set inside a diagram, with `style` or `classDef`, still apply. They are
fixed colors, so they don't change with the color scheme.

## Migrate one diagram at a time

To keep Mermaid.js for existing diagrams and opt in to Pele per diagram, give
the extension a fence name of its own. Blocks marked ` ```pele ` render with
Pele, and ` ```mermaid ` blocks keep the Mermaid.js fence:

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" },
]

[project.markdown_extensions.pele]
fences = ["pele"]
```

When every diagram is on Pele, remove `fences` and the custom fence, and
rename the blocks back to ` ```mermaid `.
