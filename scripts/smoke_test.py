"""Check that a built distribution installs and renders a diagram."""

import markdown

html = markdown.markdown(
    "```mermaid\nflowchart LR\n  A --> B\n```\n",
    extensions=["pymdownx.superfences", "zensical_pele"],
)

if "data-pele-diagram" not in html or "<script" not in html:
    message = f"zensical_pele did not render the diagram:\n{html}"
    raise SystemExit(message)
print("zensical_pele renders diagrams")
