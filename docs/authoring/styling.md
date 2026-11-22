---
title: Style a diagram
description: Give one diagram an id or class, and style its nodes with CSS.
icon: lucide/brush
---

# Style a diagram

[Colors and fonts](../setup/colors-and-fonts.md) styles every diagram on the
site. To link to one diagram or change how it looks, give it attributes and
target it from a stylesheet.

## Add an id or a class

With the `attr_list` extension enabled, attributes on the code block end up on
the diagram element:

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

The diagram element now has `id="checkout-flow"`, so
[a link to `#checkout-flow`](#checkout-flow) scrolls to it, and the `wide`
class is available to your stylesheet.

## Style nodes

Pele gives each element of the SVG a class, and each node a `data-id` with its
id from the source. This rule highlights the `Done` node of the diagram above:

```css
#checkout-flow .pele-node[data-id="Done"] .pele-label {
  fill: var(--md-accent-fg-color);
  font-weight: bold;
}
```

Theme variables like `--md-accent-fg-color` keep the node in step with the
color scheme. Colors set inside the diagram, with `style` or `classDef`, are
fixed and don't change with it.
