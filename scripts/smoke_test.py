"""Check that a built distribution installs and renders a diagram."""

import markdown

html = markdown.markdown(
    "```mermaid\nflowchart LR\n  A --> B\n```\n",
    extensions=["pymdownx.superfences", "pele"],
)

if "data-pele-diagram" not in html or "<script" not in html:
    message = f"the pele extension did not render the diagram:\n{html}"
    raise SystemExit(message)
print("the pele extension renders diagrams")
