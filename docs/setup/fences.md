---
title: Fences
description: Choose which code blocks render with Pele, and the class of the diagram element.
icon: lucide/code-xml
---

# Fences

The extension renders ` ```mermaid ` blocks. These options change which blocks
it renders and the element it renders them into.

## `fences`

The code block languages that Pele renders. Set a single language or a list:

```toml
[project.markdown_extensions.pele]
fences = ["mermaid", "pele"]
```

A language in this list takes precedence over a custom fence with the same
name in SuperFences. To keep Mermaid.js for ` ```mermaid ` blocks and render
only ` ```pele ` blocks with Pele, see
[Migrate one diagram at a time](../get-started/migrate.md#migrate-one-diagram-at-a-time).

## `class_name`

The CSS class of the `<div>` that holds each diagram. The extension's styles,
including the [color mapping](colors-and-fonts.md), use the class you choose:

```toml
[project.markdown_extensions.pele]
class_name = "diagram"
```

The class must be a valid CSS identifier: letters, digits, `-` and `_`, not
starting with a digit. Change it when `pele-diagram` clashes with a class on
your site, and use the new class in your stylesheets.
