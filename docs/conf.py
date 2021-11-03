import pydata_sphinx_theme
import datetime
import os
import sys

sys.path.append(os.path.abspath('../extensions'))

project = 'Documentation'
copyright = '2021, Mecha Karen'
author = 'Mecha Karen'
release = '0.0.1a'

extensions = [
   'sphinx.ext.autodoc', 
   'sphinx.ext.coverage', 
   'sphinx.ext.napoleon',
   'sphinx.ext.extlinks',
   'sphinx.ext.intersphinx',
   'sphinx.ext.autosummary',
]

intersphinx_mapping = {
  'py': ('https://docs.python.org/3', None),
}

templates_path = ['_templates']

exclude_patterns = ['*.md', '*.template']


html_theme = 'pydata_sphinx_theme'
html_logo = "_static/karen.png"

html_theme_options = {
   "favicons": [
      {
         "rel": "icon",
         "sizes": "16x16",
         "href": "karen.png",
      },
      {
         "rel": "icon",
         "sizes": "32x32",
         "href": "karen.png",
      },
      {
         "rel": "apple-touch-icon",
         "sizes": "180x180",
         "href": "karen.png"
      },
   ],

   "icon_links": [
      {
         "name": "GitHub",
         "url": "https://github.com/Mecha-Karen/",
         "icon": "fab fa-github",
      },
      {
         "name": "Discord",
         "url": "https://discord.com/invite/Q5mFhUM",
         "icon": "fab fa-discord"
      },
      {
         "name": "Dashboard",
         "url": "https://mechakaren.xyz/dashboard",
         "icon": "fas fa-box"
      }
    ],

   "use_edit_page_button": True,
   "collapse_navigation": False,
   "show_prev_next": False,
   "navigation_depth": 3,
   "search_bar_text": "Search the docs ...",
   "footer_items": ["copyright", "last-updated"],
}

html_context = {
    "github_url": "https://github.com",
    "github_user": "Mecha-Karen",
    "github_repo": "Documentation",
    "github_version": "main",
    "doc_path": "source",
    "last_updated": datetime.datetime.utcnow().strftime('%d/%m/%Y'),
}

html_sidebars = {
    "**": ["search-field", "sidebar-nav-bs"],
    "index": ["search-field", "home-navbar"]
}

if os.path.exists('./_templates/arc.html'):
   for key in html_sidebars.keys():
      html_sidebars[key].append('arc.html')

html_static_path = ['_static']
html_css_files = [
    'css/style.css',
    'css/codeblocks.css'
]

html_title = "Mecha Karen"

suppress_warnings = [
   "image.not_readable"
]
