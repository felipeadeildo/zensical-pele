---
title: Configuration
description: Every option of the pele Markdown extension.
---

# Configuration

The extension works without options. Set them on the extension entry:

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

| Option                            | Default          | Description                                   |
| --------------------------------- | ---------------- | --------------------------------------------- |
| [`version`](#version)             | `"1"`            | Pele version loaded from jsDelivr             |
| [`module_url`](#module_url)       | `""`             | URL of a Pele module you host                 |
| [`theme`](#theme)                 | `true`           | Use the theme's colors and fonts              |
| [`mount_options`](#mount_options) | `{}`             | Options for Pele's `mount()`                  |
| [`fences`](#fences)               | `["mermaid"]`    | Code block languages rendered with Pele       |
| [`class_name`](#class_name)       | `"pele-diagram"` | CSS class of the element that holds a diagram |

## `version`

The Pele version that browsers load from
[jsDelivr](https://www.jsdelivr.com/package/npm/pele). The default, `"1"`,
follows the latest 1.x release, so a Pele update can change your published
diagrams. Pin an exact version before you publish:

```toml
[project.markdown_extensions.pele]
version = "1.13.0"
```

A partial version such as `"1.13"` follows the latest 1.13.x release.

## `module_url`

The URL of a Pele ES module, in place of jsDelivr. When it is set, `version`
has no effect. The module must export `mountAsync` or `mount`.

To serve Pele from your own site, copy the `dist/esm` folder of the
[`pele`](https://www.npmjs.com/package/pele) npm package into your docs:

```sh
npm pack pele@1.13.0
tar -xzf pele-1.13.0.tgz
mkdir -p docs/assets/pele
cp -r package/dist/esm/. docs/assets/pele/
rm -r package pele-1.13.0.tgz
```

Then point the extension at the lazy entry point:

```toml
[project.markdown_extensions.pele]
module_url = "/my-project/assets/pele/lazy.js"
```

The URL must resolve from every page, so use a path that starts with `/`, or a
full URL. On a GitHub Pages project site, the path starts with the repository
name.

## `theme`

Maps Pele's CSS variables to the variables of the Zensical theme. Set it to
`false` to start from Pele's own colors. [Theming](theming.md) lists the
mapping.

## `mount_options`

Options passed unchanged to Pele's [`mount()`](https://pele.run/api#mount) in
the browser. The extension checks that the value is a table, not the names
inside it.

| Option                | Effect                                                      |
| --------------------- | ----------------------------------------------------------- |
| `zoom`                | `false` disables zoom, `true` enables it on every diagram.  |
| `autoDirection`       | `false` keeps the direction of the source on small screens. |
| `directionBreakpoint` | Width in pixels below which layouts may turn vertical.      |
| `fontSize`            | Base font size in pixels.                                   |
| `padding`             | Space around each diagram in pixels.                        |

```toml
[project.markdown_extensions.pele]
mount_options = { zoom = true, autoDirection = false, padding = 8 }
```

## `fences`

The code block languages that Pele renders. Takes one language or a list:

```toml
[project.markdown_extensions.pele]
fences = ["mermaid", "pele"]
```

A language in this list takes precedence over a SuperFences custom fence with
the same name.

## `class_name`

The CSS class of the `<div>` that holds each diagram. The extension's styles,
including the theme mapping, use this class:

```toml
[project.markdown_extensions.pele]
class_name = "diagram"
```

The class must be a valid CSS identifier: letters, digits, `-` and `_`, not
starting with a digit.
