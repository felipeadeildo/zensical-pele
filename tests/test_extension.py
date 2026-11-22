from __future__ import annotations

from typing import Any

import markdown
import pytest
from pymdownx.superfences import fence_code_format

FLOWCHART = """\
```mermaid
flowchart LR
  A[<b>Start</b>] --> B
```
"""

MERMAID_FENCE = {"name": "mermaid", "class": "mermaid", "format": fence_code_format}
SUPERFENCES_FIRST = ("pymdownx.superfences", "zensical_pele")


def render(
    text: str = FLOWCHART,
    extensions: tuple[str, ...] = SUPERFENCES_FIRST,
    **settings: Any,
) -> str:
    configs: dict[str, dict[str, Any]] = {
        "pymdownx.superfences": {"custom_fences": [MERMAID_FENCE]},
        "zensical_pele": settings,
    }
    return markdown.markdown(
        text, extensions=list(extensions), extension_configs=configs
    )


@pytest.mark.parametrize(
    "extensions",
    [SUPERFENCES_FIRST, tuple(reversed(SUPERFENCES_FIRST))],
    ids=["superfences-first", "pele-first"],
)
def test_takes_over_mermaid_fence(extensions):
    html = render(extensions=extensions)
    assert '<div class="pele-diagram" data-pele-diagram>' in html
    assert '<pre class="mermaid">' not in html


def test_escapes_diagram_source():
    html = render()
    assert "A[&lt;b&gt;Start&lt;/b&gt;] --&gt; B" in html


def test_adds_page_assets_once_per_page():
    html = render(FLOWCHART + "\n" + FLOWCHART)
    assert html.count('<script type="module">') == 1
    assert html.count("<style>") == 1
    assert '"https://cdn.jsdelivr.net/npm/pele@1/dist/esm/lazy.js"' in html


def test_skips_page_assets_without_diagrams():
    html = render("```python\nprint(1)\n```\n")
    assert "<script" not in html
    assert "<style>" not in html


def test_ignores_attribute_name_inside_code():
    html = render("```html\n<div data-pele-diagram></div>\n```\n")
    assert "<script" not in html


def test_keeps_fence_classes_id_and_attributes():
    html = render(
        '``` { .mermaid #login .wide title="Login" }\ngraph LR\n  A --> B\n```\n',
        extensions=(*SUPERFENCES_FIRST, "attr_list"),
    )
    assert (
        '<div class="pele-diagram wide" data-pele-diagram id="login" title="Login">'
        in html
    )


def test_renders_additional_fences():
    html = render("```pele\ngraph LR\n  A --> B\n```\n", fences=["mermaid", "pele"])
    assert "data-pele-diagram" in html


def test_applies_class_name_to_markup_and_styles():
    html = render(class_name="diagram")
    assert '<div class="diagram" data-pele-diagram>' in html
    assert ".diagram {" in html
    assert ".pele-diagram" not in html
    assert '".diagram[data-pele-diagram]"' in html


def test_maps_theme_variables_by_default():
    assert "--pele-accent: var(--md-accent-fg-color)" in render()
    assert "--pele-accent" not in render(theme=False)


def test_pins_pele_version():
    assert '"https://cdn.jsdelivr.net/npm/pele@1.13.0/dist/esm/lazy.js"' in render(
        version="1.13.0"
    )


def test_module_url_overrides_version():
    html = render(module_url="/assets/pele/lazy.js", version="1.13.0")
    assert 'const peleUrl = "/assets/pele/lazy.js";' in html
    assert "jsdelivr" not in html


def test_passes_mount_options_to_the_browser():
    html = render(mount_options={"zoom": False, "fontSize": 14})
    assert 'const mountOptions = {"zoom": false, "fontSize": 14};' in html


def test_escapes_script_end_tags_in_options():
    html = render(mount_options={"label": "</script><script>alert(1)"})
    assert "</script><script>alert(1)" not in html
    assert html.count("</script>") == 1


def test_warns_without_superfences(caplog):
    html = markdown.markdown(FLOWCHART, extensions=["zensical_pele"])
    assert "data-pele-diagram" not in html
    assert "needs pymdownx.superfences" in caplog.text
