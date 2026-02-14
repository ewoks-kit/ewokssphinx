import importlib.metadata

project = "ewokssphinx"
release = importlib.metadata.version(project)
version = ".".join(release.split(".")[:2])
copyright = "2026, ESRF"
author = "ESRF"

extensions = ["myst_parser", "sphinx_design", "ewokssphinx"]

myst_enable_extensions = ["colon_fence", "substitution"]
myst_substitutions = {"version": version}

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "github",
            "url": "https://github.com/ewoks-kit/ewokssphinx",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "pypi",
            "url": "https://pypi.org/project/ewokssphinx",
            "icon": "fa-brands fa-python",
        },
    ],
}
