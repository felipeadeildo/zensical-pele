---
title: Configuration
description: Options of the zensical-pele extension.
---

# Configuration

All options are optional. Set them on the extension:

=== "zensical.toml"

    ```toml
    [project.markdown_extensions.zensical_pele]
    version = "1.13.0"
    mount_options = { zoom = false }
    ```

=== "mkdocs.yml"

    ```yaml
    markdown_extensions:
      - zensical_pele:
          version: "1.13.0"
          mount_options:
            zoom: false
    ```

| Option          | Default            | Description                                         |
| --------------- | ------------------ | --------------------------------------------------- |
| `fences`        | `["mermaid"]`      | Code block languages rendered with Pele.            |
| `class_name`    | `"pele-diagram"`   | CSS class of the element that holds each diagram.   |
| `version`       | `"1"`              | Pele version loaded from jsDelivr.                  |
| `module_url`    | `""`               | URL of a Pele module you host. Overrides `version`. |
| `theme`         | `true`             | Use the colors and fonts of the Zensical theme.     |
| `mount_options` | `{}`               | Options for Pele's `mount()`.                       |

## `fences`

The code block languages that Pele renders. Add a language to render it as
well, for example to keep `mermaid` blocks on Mermaid.js and opt in per
diagram:

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "mermaid", class = "mermaid", format = "pymdownx.superfences.fence_code_format" },
]

[project.markdown_extensions.zensical_pele]
fences = ["pele"]
```

## `class_name`

The CSS class of the `<div>` that holds each diagram. The built-in styles
follow the class you choose.

## `version`

The Pele version that browsers load from
[jsDelivr](https://www.jsdelivr.com/package/npm/pele). The default, `"1"`,
follows the latest 1.x release. Pin an exact version so a Pele update can't
change your published diagrams:

```toml
[project.markdown_extensions.zensical_pele]
version = "1.13.0"
```

## `module_url`

The URL of a Pele ES module, for sites that can't load scripts from a CDN. The
module must export `mountAsync` or `mount`. To serve Pele from your own site:

1. Copy the `dist/esm` folder of the [`pele`](https://www.npmjs.com/package/pele)
   npm package into your docs:

    ```sh
    npm pack pele@1.13.0
    tar -xzf pele-1.13.0.tgz
    mkdir -p docs/assets/pele
    cp -r package/dist/esm/. docs/assets/pele/
    rm -r package pele-1.13.0.tgz
    ```

2. Point the extension at the lazy entry point, with the path your site is
   served under. For a GitHub Pages project site, that path starts with the
   repository name:

    ```toml
    [project.markdown_extensions.zensical_pele]
    module_url = "/my-project/assets/pele/lazy.js"
    ```

3. Build the site and open a page with a diagram. In the network panel of the
   browser, the Pele files come from `assets/pele/` and none from jsDelivr.

The URL must resolve from every page, so use a path that starts with `/`, or a
full URL. A relative path such as `assets/pele/lazy.js` breaks on every page
below the site root.

## `theme`

Maps the Pele color and font variables to the Zensical theme variables.
Set it to `false` to start from Pele's own colors. See [Theming](theming.md).

## `mount_options`

Options passed to Pele's
[`mount()`](https://pele.run/api#mount) in the browser, as written in the Pele
docs. Some useful ones:

| Option                | Effect                                                     |
| --------------------- | ---------------------------------------------------------- |
| `zoom`                | `false` disables zoom, `true` enables it on every diagram. |
| `autoDirection`       | `false` keeps the direction of the source on small screens.|
| `directionBreakpoint` | Width in pixels below which layouts may turn vertical.     |
| `fontSize`            | Base font size in pixels.                                  |
| `padding`             | Space around each diagram in pixels.                       |

```toml
[project.markdown_extensions.zensical_pele]
mount_options = { zoom = true, autoDirection = false, padding = 8 }
```

## Per-diagram attributes

With the `attr_list` extension enabled, attributes on the code block end up on
the diagram element. Use them to link to a diagram or style it:

````markdown
``` { .mermaid #checkout-flow .wide }
flowchart LR
  Cart --> Payment --> Done
```
````

``` { .mermaid #checkout-flow .wide }
flowchart LR
  Cart --> Payment --> Done
```
