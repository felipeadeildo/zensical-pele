---
title: Zoom and layout
description: Pass options to Pele's mount() to change zoom, direction and spacing.
icon: lucide/zoom-in
---

# Zoom and layout

`mount_options` goes to Pele's [`mount()`](https://pele.run/api#mount) in the
browser, unchanged, so it takes the option names from the Pele docs. These are
the ones that change how diagrams behave on a docs site:

| Option                | Effect                                                      |
| --------------------- | ----------------------------------------------------------- |
| `zoom`                | `false` disables zoom, `true` enables it on every diagram.  |
| `autoDirection`       | `false` keeps the direction of the source on small screens. |
| `directionBreakpoint` | Width in pixels below which layouts may turn vertical.      |
| `fontSize`            | Base font size in pixels.                                   |
| `padding`             | Space around each diagram in pixels.                        |

For example, to zoom every diagram, keep the direction of the source and
tighten the spacing:

```toml
[project.markdown_extensions.pele]
mount_options = { zoom = true, autoDirection = false, padding = 8 }
```

The extension checks that `mount_options` is a table, and passes the names and
values to Pele without checking them. Compare the spelling with the Pele docs
when an option doesn't seem to apply.
