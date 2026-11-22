from __future__ import annotations

from typing import Any

import pytest

from zensical_pele import PeleSettings, SettingsError
from zensical_pele.settings import DEFAULTS


def settings_from(**overrides: Any) -> PeleSettings:
    config = {name: default for name, (default, _) in DEFAULTS.items()}
    return PeleSettings.from_config({**config, **overrides})


def test_defaults():
    settings = settings_from()
    assert settings == PeleSettings()
    assert settings.pele_url == "https://cdn.jsdelivr.net/npm/pele@1/dist/esm/lazy.js"


def test_accepts_a_single_fence_name():
    assert settings_from(fences="pele").fences == ("pele",)


@pytest.mark.parametrize(
    ("option", "value"),
    [
        ("fences", []),
        ("fences", [""]),
        ("class_name", "two words"),
        ("class_name", "1st"),
        ("version", "latest"),
        ("version", "1/../../evil"),
        ("module_url", 42),
        ("mount_options", ["zoom"]),
    ],
)
def test_rejects_invalid_values(option, value):
    with pytest.raises(SettingsError, match=option):
        settings_from(**{option: value})


@pytest.mark.parametrize("version", ["1", "1.13", "1.13.0", "2.0.0-beta.1"])
def test_accepts_pele_versions(version):
    assert settings_from(version=version).version == version
