"""Render Mermaid diagrams with Pele (https://pele.run) in Zensical and MkDocs."""

from __future__ import annotations

from typing import Any

from zensical_pele.extension import PeleExtension
from zensical_pele.settings import PeleSettings, SettingsError

__all__ = ["PeleExtension", "PeleSettings", "SettingsError", "makeExtension"]


def makeExtension(**kwargs: Any) -> PeleExtension:  # noqa: N802
    """Create the extension, as Python Markdown expects from extension modules."""
    return PeleExtension(**kwargs)
