import importlib.util

# The browser tests need Playwright, which only the "browser" dependency group installs.
collect_ignore_glob = [] if importlib.util.find_spec("playwright") else ["browser/*"]
