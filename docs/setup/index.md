---
title: Setup
description: Every option of the pele Markdown extension.
icon: lucide/settings-2
---

# Setup

The extension works without options. Set them on the extension entry, in
either configuration format:

=== "zensical.toml"

    ```toml
    [project.markdown_extensions.pele]
    version = "1.13.0"
    mount_options = { zoom = false }
    ```

=== "mkdocs.yml"

    ```yaml
    markdown_extensions:
      - pele:
          version: "1.13.0"
          mount_options:
            zoom: false
    ```

An invalid value stops the build with a message that names the option.

| Option          | Default          | What it sets                                   | Page                                        |
| --------------- | ---------------- | ---------------------------------------------- | ------------------------------------------- |
| `version`       | `"1"`            | Pele version loaded from jsDelivr              | [Load Pele](loading-pele.md#version)        |
| `module_url`    | `""`             | URL of a Pele module you host                  | [Load Pele](loading-pele.md#module_url)     |
| `theme`         | `true`           | Diagrams use the theme's colors and fonts      | [Colors and fonts](colors-and-fonts.md)     |
| `mount_options` | `{}`             | Options for Pele's `mount()`                   | [Zoom and layout](zoom-and-layout.md)       |
| `fences`        | `["mermaid"]`    | Code block languages rendered with Pele        | [Fences](fences.md#fences)                  |
| `class_name`    | `"pele-diagram"` | CSS class of the element that holds a diagram  | [Fences](fences.md#class_name)              |

[llms.txt](llms-txt.md) has no option on the extension: it sets up a hook of
the Zensical `llmstxt` plugin.
