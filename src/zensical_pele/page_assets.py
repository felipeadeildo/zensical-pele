"""Styles and script added to pages that contain at least one diagram."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zensical_pele.settings import PeleSettings

DIAGRAM_ATTRIBUTE = "data-pele-diagram"
"""Attribute that marks diagram elements, for the browser and the injector."""

_DEFAULT_CLASS_SELECTOR = ".pele-diagram"


def _read_asset(name: str) -> str:
    return files("zensical_pele").joinpath("assets", name).read_text(encoding="utf-8")


def render_page_assets(settings: PeleSettings) -> str:
    """Render the ``<style>`` and ``<script>`` elements for a page with diagrams.

    The script is an inline module, so instant navigation runs it again on every
    page it lands on. It imports Pele and mounts each diagram of the page.

    Args:
        settings: The extension settings.

    Returns:
        HTML to append to the page content.
    """
    stylesheets = ["layout.css", "theme.css"] if settings.theme else ["layout.css"]
    css = "".join(_read_asset(name) for name in stylesheets)
    css = css.replace(_DEFAULT_CLASS_SELECTOR, f".{settings.class_name}")

    replacements = {
        "__PELE_URL__": settings.pele_url,
        "__DIAGRAM_SELECTOR__": f".{settings.class_name}[{DIAGRAM_ATTRIBUTE}]",
        "__MOUNT_OPTIONS__": dict(settings.mount_options),
    }
    script = _read_asset("mount-diagrams.js")
    for placeholder, value in replacements.items():
        script = script.replace(placeholder, _to_script_literal(value))

    return f'\n<style>{css}</style>\n<script type="module">\n{script}</script>\n'


def _to_script_literal(value: object) -> str:
    # JSON is valid JavaScript. Escaping "<" keeps "</script>" from closing the
    # element early when it shows up in a URL or an option value.
    return json.dumps(value).replace("<", "\\u003c")
