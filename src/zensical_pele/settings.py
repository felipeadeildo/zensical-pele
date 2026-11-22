"""User settings of the extension, validated once when Markdown loads it."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping

PELE_CDN_URL = "https://cdn.jsdelivr.net/npm/pele@{version}/dist/esm/lazy.js"

_CSS_IDENTIFIER = re.compile(r"^-?[A-Za-z_][A-Za-z0-9_-]*$")
_PELE_VERSION = re.compile(r"^[0-9]+(\.[0-9]+){0,2}([-+][0-9A-Za-z.-]+)?$")

DEFAULTS: dict[str, tuple[Any, str]] = {
    "fences": (
        ["mermaid"],
        "Fence names rendered with Pele. Default: ['mermaid']",
    ),
    "class_name": (
        "pele-diagram",
        "CSS class of the element that holds each diagram. Default: 'pele-diagram'",
    ),
    "version": (
        "1",
        "Pele version loaded from jsDelivr, such as '1' or '1.13.0'. Default: '1'",
    ),
    "module_url": (
        "",
        "URL of a Pele ES module, for self-hosting. Overrides 'version'. Default: ''",
    ),
    "theme": (
        True,
        "Map Pele colors and fonts to the Zensical theme. Default: True",
    ),
    "mount_options": (
        {},
        "Options passed to Pele's mount(), such as {'zoom': False}. Default: {}",
    ),
}


class SettingsError(ValueError):
    """Raised when the extension is configured with an invalid value."""


@dataclass(frozen=True)
class PeleSettings:
    """Validated settings of the extension.

    Attributes:
        fences: Fence names rendered with Pele.
        class_name: CSS class of the element that holds each diagram.
        version: Pele version loaded from jsDelivr.
        module_url: URL of a Pele ES module. Overrides ``version`` when set.
        theme: Whether Pele colors and fonts follow the Zensical theme.
        mount_options: Options passed to Pele's ``mount()`` in the browser.
    """

    fences: tuple[str, ...] = ("mermaid",)
    class_name: str = "pele-diagram"
    version: str = "1"
    module_url: str = ""
    theme: bool = True
    mount_options: Mapping[str, Any] = field(default_factory=dict)

    @property
    def pele_url(self) -> str:
        """URL of the Pele ES module that the browser imports."""
        return self.module_url or PELE_CDN_URL.format(version=self.version)

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> PeleSettings:
        """Validate the configuration that Python Markdown passes to the extension.

        Args:
            config: Option values keyed by option name.

        Returns:
            The validated settings.

        Raises:
            SettingsError: If an option has an invalid value.
        """
        fences = config["fences"]
        if isinstance(fences, str):
            fences = [fences]
        if not fences or not all(isinstance(name, str) and name for name in fences):
            message = "'fences' must be a non-empty list of fence names"
            raise SettingsError(message)

        class_name = config["class_name"]
        if not isinstance(class_name, str) or not _CSS_IDENTIFIER.match(class_name):
            message = f"'class_name' must be a CSS class name, got {class_name!r}"
            raise SettingsError(message)

        version = str(config["version"])
        if not _PELE_VERSION.match(version):
            message = f"'version' must be a Pele version like '1.13.0', got {version!r}"
            raise SettingsError(message)

        module_url = config["module_url"] or ""
        if not isinstance(module_url, str):
            message = "'module_url' must be a string"
            raise SettingsError(message)

        mount_options = config["mount_options"] or {}
        if not isinstance(mount_options, dict):
            message = "'mount_options' must be a table of Pele mount() options"
            raise SettingsError(message)

        return cls(
            fences=tuple(fences),
            class_name=class_name,
            version=version,
            module_url=module_url,
            theme=bool(config["theme"]),
            mount_options=dict(mount_options),
        )
