import importlib.metadata

project = "ewokssphinx"
release = importlib.metadata.version(project)
version = ".".join(release.split(".")[:2])
copyright = "2025, ESRF"
author = "ESRF"

extensions = ["myst_parser", "ewokssphinx"]

myst_enable_extensions = ["colon_fence", "substitution"]
myst_substitutions = {"version": version}

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "gitlab",
            "url": "https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx",
            "icon": "fa-brands fa-gitlab",
        },
        {
            "name": "pypi",
            "url": "https://pypi.org/project/ewokssphinx",
            "icon": "fa-brands fa-python",
        },
    ],
}
