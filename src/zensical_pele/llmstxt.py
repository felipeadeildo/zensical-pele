"""Turn diagram elements back into ``mermaid`` code blocks for Zensical's llms.txt.

Zensical converts each page's HTML into Markdown for ``llms.txt``. Without this
step, a diagram element becomes one line of flattened text. Point the
``preprocess`` setting of the ``llmstxt`` plugin at a script that imports
:func:`preprocess`::

    from zensical_pele.llmstxt import preprocess

    __all__ = ["preprocess"]
"""

from __future__ import annotations

import re

from zensical_pele.page_assets import DIAGRAM_ATTRIBUTE

# The extension escapes the source, so the element holds no "<" before its
# closing tag.
_DIAGRAM_ELEMENT = re.compile(
    rf"<div\b[^>]*\s{DIAGRAM_ATTRIBUTE}(?=[\s/>])[^>]*>(?P<source>[^<]*)</div>"
)


def preprocess(html: str, output: str) -> str:
    """Replace each diagram element with a ``mermaid`` code block.

    Args:
        html: HTML of one page, as Zensical passes it to the hook.
        output: Path of the Markdown file that Zensical writes. Not used.

    Returns:
        The HTML with ``<pre><code class="language-mermaid">`` in place of
        each diagram element.
    """
    del output
    return _DIAGRAM_ELEMENT.sub(
        r'<pre><code class="language-mermaid">\g<source></code></pre>', html
    )
