"""Build the docs and check that Pele renders them in Chromium.

Run with ``uv run pytest -m browser``. Needs network access to
load Pele from jsDelivr, and a Playwright browser: ``playwright install chromium``.
"""

from __future__ import annotations

import functools
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import sync_playwright

if TYPE_CHECKING:
    from collections.abc import Iterator

    from playwright.sync_api import Browser, Page

pytestmark = pytest.mark.browser

ROOT = Path(__file__).resolve().parents[2]
SITE_DIR = ROOT / "site"
EXAMPLE_PAGES = sorted(
    page.stem
    for page in (ROOT / "docs" / "examples").glob("*.md")
    if page.stem != "index"
)
MOUNT_TIMEOUT_MS = 15_000


@pytest.fixture(scope="session")
def site_url() -> Iterator[str]:
    subprocess.run(
        [sys.executable, "-m", "zensical", "build", "--clean", "--strict"],
        cwd=ROOT,
        check=True,
    )
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(SITE_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}/"
    server.shutdown()


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser) -> Iterator[Page]:
    page = browser.new_page()
    errors: list[str] = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    yield page
    page.close()
    assert not errors, errors


def wait_for_diagrams(page: Page) -> list[str]:
    """Wait until the page has diagrams and none is loading, then return their states.

    After instant navigation the URL changes before the content does, so the page
    must have at least one diagram before the states count.
    """
    page.wait_for_function(
        """() => {
          const elements = [...document.querySelectorAll("[data-pele-diagram]")];
          const done = ["mounted", "failed"];
          return elements.length > 0
            && elements.every((element) => done.includes(element.dataset.peleState));
        }""",
        timeout=MOUNT_TIMEOUT_MS,
    )
    states = page.eval_on_selector_all(
        "[data-pele-diagram]",
        """(elements) => elements.map((element) =>
          element.querySelector("svg.pele") ? element.dataset.peleState : "no-svg")""",
    )
    return [str(state) for state in states]


@pytest.mark.parametrize("slug", EXAMPLE_PAGES)
def test_example_page_mounts_every_diagram(page: Page, site_url: str, slug: str):
    page.goto(f"{site_url}examples/{slug}/")
    states = wait_for_diagrams(page)
    assert states
    assert set(states) == {"mounted"}


def test_instant_navigation_mounts_new_page(page: Page, site_url: str):
    page.goto(site_url)
    assert wait_for_diagrams(page) == ["mounted"]

    page.click('.md-content a[href$="examples/"]')
    page.wait_for_url("**/examples/")
    page.click('.md-content a[href$="sequence/"]')
    page.wait_for_url("**/examples/sequence/")

    assert set(wait_for_diagrams(page)) == {"mounted"}
    mounted = page.evaluate("globalThis.__zensicalPele.mounted.length")
    assert mounted == len(page.query_selector_all("[data-pele-diagram]"))


def test_color_scheme_switch_keeps_the_svg(page: Page, site_url: str):
    page.goto(site_url)
    wait_for_diagrams(page)
    svg = page.locator("[data-pele-diagram] svg.pele").first
    background = "(svg) => getComputedStyle(svg).getPropertyValue('--pele-bg')"

    svg.evaluate("(svg) => { svg.dataset.marker = 'original'; }")
    light = svg.evaluate(background)
    page.evaluate("document.body.setAttribute('data-md-color-scheme', 'slate')")
    dark = svg.evaluate(background)

    assert light != dark
    assert svg.evaluate("(svg) => svg.dataset.marker") == "original"


def test_page_without_diagrams_does_not_load_pele(page: Page, site_url: str):
    requests: list[str] = []
    page.on("request", lambda request: requests.append(request.url))
    page.goto(f"{site_url}configuration/")
    page.wait_for_load_state("networkidle")
    assert not [url for url in requests if "pele" in url and "jsdelivr" in url]


def test_llms_markdown_keeps_diagrams_as_mermaid_blocks(site_url: str):
    del site_url
    markdown = (SITE_DIR / "examples" / "pie" / "index.md").read_text()
    assert "```mermaid\npie title Fish caught by the crew\n" in markdown
    assert 'Fish caught by the crew "' not in markdown


def test_llms_index_lists_every_page_in_the_nav(site_url: str):
    del site_url
    index = (SITE_DIR / "llms.txt").read_text()
    pages = [page.relative_to(ROOT / "docs") for page in (ROOT / "docs").rglob("*.md")]
    for page in pages:
        url_path = page.with_suffix("").as_posix().removesuffix("index").rstrip("/")
        url_path = f"{url_path}/index.md" if url_path else "index.md"
        assert f"zensical-pele/{url_path}>" in index, url_path


def test_unreachable_pele_leaves_the_source_as_a_code_block(page: Page, site_url: str):
    page.route("**/cdn.jsdelivr.net/**", lambda route: route.abort())
    page.goto(site_url)
    page.wait_for_function(
        """() => [...document.querySelectorAll("[data-pele-diagram]")]
          .every((element) => element.dataset.peleState === "failed")""",
        timeout=MOUNT_TIMEOUT_MS,
    )
    source = page.text_content("[data-pele-diagram] code.language-mermaid")
    assert source is not None
    assert source.startswith("flowchart LR")


@pytest.mark.parametrize("slug", EXAMPLE_PAGES)
def test_example_page_has_one_tab_set_per_example(page: Page, site_url: str, slug: str):
    page.goto(f"{site_url}examples/{slug}/")
    tab_counts = page.eval_on_selector_all(
        ".md-content .tabbed-set",
        """(sets) => sets.map(
          (set) => set.querySelectorAll(".tabbed-labels > label").length)""",
    )
    assert tab_counts
    assert all(count == 2 for count in tab_counts), tab_counts
