# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'RedditLike.js'
copyright = '2024, Onion Kim'
author = 'Onion Kim'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser'
]

myst_enable_extensions = [
    # "amsmath",
    # "attrs_inline",
    # "colon_fence",
    # "deflist",
    # "dollarmath",
    # "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    # "replacements",
    # "smartquotes",
    # "strikethrough",
    # "substitution",
    # "tasklist",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',

}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['../_static']

html_favicon = 'assets/favicon.ico'