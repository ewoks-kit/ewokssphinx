import importlib.metadata

project = "ewokssphinx"
release = importlib.metadata.version(project)
version = ".".join(release.split(".")[:2])
copyright = "2025-2026, ESRF"
author = "ESRF"
docstitle = f"{project} {version}"
templates_path = ["_templates"]

extensions = ["myst_parser", "sphinx_design", "ewokssphinx"]

myst_enable_extensions = ["colon_fence", "substitution"]
myst_substitutions = {"version": version}

html_theme = "pydata_sphinx_theme"
html_title = docstitle
html_logo = "_static/logo.png"
html_static_path = ["_static"]

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
    "logo": {
        "text": docstitle,
    },
    "footer_start": ["copyright"],
    "footer_end": ["footer_end"],
}
