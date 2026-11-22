---
title: zensical-pele
description: Render Mermaid diagrams with Pele in Zensical and MkDocs.
icon: lucide/house
---

# zensical-pele

zensical-pele renders the Mermaid diagrams of a [Zensical](https://zensical.org)
site with [Pele](https://pele.run) instead of Mermaid.js. You keep writing
` ```mermaid ` blocks, and readers get diagrams in your theme colors that adapt
to small screens.

```mermaid
flowchart LR
  md[Markdown with mermaid blocks] --> ext[zensical-pele]
  ext --> page[Page with diagram sources]
  page --> pele([Pele in the browser])
  pele --> svg[SVG in theme colors]
```

Pele drew the diagram above, and every other diagram on this site. Switch the
color scheme in the header: the diagram changes colors without being drawn
again.

```sh
uvx --with zensical-pele zensical serve
```

That command runs your site once with the extension installed. To keep it,
add `[project.markdown_extensions.pele]` to `zensical.toml`.

<div class="grid cards" markdown>

-   :lucide-rocket:{ .lg .middle } **Get started**

    ---

    Install the extension, enable it and render a first diagram.

    [:lucide-arrow-right: Get started](get-started/index.md)

-   :lucide-settings-2:{ .lg .middle } **Setup**

    ---

    Pin the Pele version, host Pele yourself, change colors and zoom.

    [:lucide-arrow-right: Setup](setup/index.md)

-   :lucide-layout-grid:{ .lg .middle } **Gallery**

    ---

    All 32 diagram types, each with the Markdown that produced it.

    [:lucide-arrow-right: Gallery](examples/index.md)

-   :lucide-bot:{ .lg .middle } **llms.txt**

    ---

    Give coding agents your docs with diagrams as `mermaid` blocks.

    [:lucide-arrow-right: llms.txt](setup/llms-txt.md)

</div>

## Why Pele

Pele is a Mermaid renderer that the [Obsidian](https://obsidian.md) team wrote
to draw diagrams quickly in the colors of the app's theme. It reads Mermaid
syntax and supports every diagram type built into Mermaid 12.1. The Pele site
compares it with Mermaid.js:

|                    | Pele              | Mermaid.js          |
| ------------------ | ----------------- | ------------------- |
| Bundle size (gzip) | 230 kB            | 1.6 MB              |
| Render time        | 0.05 to 0.3 ms    | 6 to 82 ms          |
| Dependencies       | 0                 | 23                  |
| Small screens      | Adapts the layout | Scales the diagram  |
| Theming            | CSS variables     | Theme configuration |

The CSS variables are what make the theme work. zensical-pele points Pele's
color and font variables at the variables of the Zensical theme, so a diagram
in dark mode uses the dark palette with no extra configuration.
[Colors and fonts](setup/colors-and-fonts.md) lists the mapping.

Small screens get a different layout, not a smaller picture. Below 640 pixels,
Pele can turn a wide left-to-right flowchart into a top-to-bottom one, and
readers can zoom and pan a diagram that still doesn't fit.
