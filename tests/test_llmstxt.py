from __future__ import annotations

import markdown

from zensical_pele.llmstxt import preprocess


def page_html(source: str, extensions: tuple[str, ...] = ()) -> str:
    return markdown.markdown(
        source, extensions=["pymdownx.superfences", "pele", *extensions]
    )


def test_turns_diagram_into_mermaid_code_block():
    html = page_html("```mermaid\nflowchart LR\n  A --> B\n```\n")
    result = preprocess(html, "index.md")
    assert '<pre><code class="language-mermaid">flowchart LR\n  A --&gt; B' in result
    assert "<div" not in result


def test_keeps_escaped_characters_escaped():
    html = page_html('```mermaid\nflowchart LR\n  A["a & b"] -- "x<y" --> B\n```\n')
    result = preprocess(html, "index.md")
    assert 'A["a &amp; b"] -- "x&lt;y" --&gt; B' in result


def test_handles_attributes_and_several_diagrams():
    html = page_html(
        '``` { .mermaid #login title="a > b" }\ngraph LR\n  A --> B\n```\n\n'
        'Text\n\n```mermaid\npie\n  "A" : 1\n```\n',
        extensions=("attr_list",),
    )
    result = preprocess(html, "index.md")
    assert result.count('<code class="language-mermaid">') == 2
    assert "<p>Text</p>" in result


def test_leaves_other_html_alone():
    html = '<div class="pele-diagram-legend">Legend</div><pre><code>x</code></pre>'
    assert preprocess(html, "index.md") == html
