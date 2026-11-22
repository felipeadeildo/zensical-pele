"""Python Markdown extension that renders Mermaid fences with Pele."""

from __future__ import annotations

import html
import logging
import sys
from typing import TYPE_CHECKING, Any

from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor

from zensical_pele.page_assets import DIAGRAM_ATTRIBUTE, render_page_assets
from zensical_pele.settings import DEFAULTS, PeleSettings

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from markdown import Markdown

logger = logging.getLogger("zensical_pele")

# SuperFences registers its fenced block preprocessor at priority 25, and
# preprocessors run from the highest priority to the lowest.
_BEFORE_SUPERFENCES = 26
_LAST = 0


class PeleExtension(Extension):
    """Render Mermaid fences with Pele instead of Mermaid.js.

    The extension takes over the configured fences from ``pymdownx.superfences``.
    Each fence becomes an element holding the escaped diagram source, and pages
    with diagrams get a small script that mounts them with Pele in the browser.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.config = {name: list(option) for name, option in DEFAULTS.items()}
        super().__init__(**kwargs)

    @override
    def extendMarkdown(self, md: Markdown) -> None:
        """Register the extension with a Markdown instance.

        Args:
            md: The Markdown instance.
        """
        settings = PeleSettings.from_config(self.getConfigs())
        fence = DiagramFence(settings)
        md.registerExtension(self)
        md.preprocessors.register(
            FenceRegistration(md, fence), "pele_fences", _BEFORE_SUPERFENCES
        )
        md.postprocessors.register(
            PageAssetsInjection(md, render_page_assets(settings)),
            "pele_page_assets",
            _LAST,
        )


class DiagramFence:
    """Formatter and validator for the SuperFences custom fence API."""

    def __init__(self, settings: PeleSettings) -> None:
        self.settings = settings

    def validate(
        self,
        language: str,
        inputs: dict[str, str],
        options: dict[str, Any],
        attrs: dict[str, str],
        md: Markdown,
    ) -> bool:
        """Accept every fence and keep its key-value pairs as HTML attributes."""
        del language, options, md
        attrs.update(inputs)
        return True

    def format(  # noqa: PLR0913, PLR0917 (signature defined by SuperFences)
        self,
        src: str = "",
        language: str = "",
        md: Markdown | None = None,
        options: dict[str, Any] | None = None,
        classes: list[str] | None = None,
        id_value: str = "",
        attrs: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> str:
        """Render the element that the browser mounts the diagram into."""
        del language, md, options, kwargs
        class_names = " ".join([self.settings.class_name, *(classes or [])])
        attributes = [f'class="{html.escape(class_names)}"', DIAGRAM_ATTRIBUTE]
        if id_value:
            attributes.append(f'id="{html.escape(id_value)}"')
        attributes.extend(
            f'{html.escape(name)}="{html.escape(value)}"'
            for name, value in (attrs or {}).items()
        )
        source = html.escape(src, quote=False)
        return f"<div {' '.join(attributes)}>{source}</div>"

    def superfences_entry(self, name: str) -> dict[str, Any]:
        """Describe the fence the way SuperFences stores its custom fences."""
        return {
            "name": name,
            "test": lambda language: language == name,
            "formatter": self.format,
            "validator": self.validate,
            "reset": None,
        }


class FenceRegistration(Preprocessor):
    """Add the diagram fences to SuperFences before the first page is converted.

    SuperFences may be loaded before or after this extension, so the fences are
    added here instead of in ``extendMarkdown``. SuperFences tries its fences in
    reverse order, so these take precedence over the default ``mermaid`` fence.
    """

    def __init__(self, md: Markdown, fence: DiagramFence) -> None:
        super().__init__(md)
        self.fence = fence
        self.registered = False

    @override
    def run(self, lines: list[str]) -> list[str]:
        """Register the fences once and return the lines unchanged."""
        if self.registered:
            return lines
        self.registered = True

        superfences = _find_superfences(self.md)
        if superfences is None:
            logger.warning(
                "zensical-pele needs pymdownx.superfences, diagrams are not rendered"
            )
            return lines

        for name in self.fence.settings.fences:
            superfences.superfences.append(self.fence.superfences_entry(name))
        return lines


class PageAssetsInjection(Postprocessor):
    """Append the styles and script to pages that contain a diagram."""

    def __init__(self, md: Markdown, page_assets: str) -> None:
        super().__init__(md)
        self.page_assets = page_assets

    @override
    def run(self, text: str) -> str:
        """Return the page HTML, with the assets appended when it has diagrams."""
        # The attribute only appears unescaped in elements that DiagramFence made.
        if f" {DIAGRAM_ATTRIBUTE}" not in text:
            return text
        return text + self.page_assets


def _find_superfences(md: Markdown) -> Any | None:
    if "fenced_code_block" not in md.preprocessors:
        return None
    extension = getattr(md.preprocessors["fenced_code_block"], "extension", None)
    return extension if hasattr(extension, "superfences") else None
