---
title: Migrating from Mermaid.js
description: What changes when a site with Mermaid diagrams switches to Pele.
---

# Migrating from Mermaid.js

Your Markdown doesn't change. Once the extension is enabled, every `mermaid`
code block renders with Pele, and Mermaid.js stops loading.

## Configuration

A `mermaid` entry in `custom_fences`, like the one the Zensical docs suggest,
can stay. The extension's fence takes precedence over it:

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" },
]
```

Settings passed to Mermaid.js, for example in a script that calls
`mermaid.initialize()`, no longer apply. Pele takes colors and fonts from CSS
variables; see [Theming](theming.md).

## Layout

Pele lays out diagrams its own way, so they won't look exactly as before. The
[Pele compatibility notes](https://pele.run/compatibility) list the
differences. Check the pages with the most complex diagrams before you publish.

## One diagram at a time

To keep Mermaid.js for `mermaid` code blocks and move diagrams over one by one,
give Pele its own fence name:

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" },
]

[project.markdown_extensions.pele]
fences = ["pele"]
```

Code blocks marked `pele` render with Pele. When every diagram is moved,
remove `fences` and the custom fence, and mark the blocks `mermaid` again.
