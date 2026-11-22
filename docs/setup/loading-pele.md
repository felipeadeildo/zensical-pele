---
title: Load Pele
description: Pin the Pele version, or serve Pele from your own site.
icon: lucide/package
---

# Load Pele

Browsers load Pele from [jsDelivr](https://www.jsdelivr.com/package/npm/pele)
when a page has a diagram. Without options, they get the latest 1.x release,
so a Pele update can change your published diagrams. Pin a version before you
publish, or host Pele with your site.

## `version`

The Pele version that browsers load from jsDelivr. Pin an exact version:

```toml
[project.markdown_extensions.pele]
version = "1.13.0"
```

A partial version such as `"1.13"` follows the latest 1.13.x release. Find the
current release on the [npm page](https://www.npmjs.com/package/pele).

## `module_url`

The URL of a Pele ES module. It replaces jsDelivr, so `version` has no effect.
The module must export `mountAsync` or `mount`. To serve Pele from your own
site:

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
    [project.markdown_extensions.pele]
    module_url = "/my-project/assets/pele/lazy.js"
    ```

3. Build the site and open a page with a diagram. In the network panel of the
   browser, the Pele files come from `assets/pele/` and none from jsDelivr.

The URL must resolve from every page, so use a path that starts with `/`, or a
full URL. A relative path such as `assets/pele/lazy.js` breaks on every page
below the site root.
