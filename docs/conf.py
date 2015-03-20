# -*- coding: utf-8 -*-

import alabaster
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))

extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'MapleTree'
copyright = u'2015, TomokiNakamaru'
version = '0.6.3'
release = '0.6.3'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

html_static_path = ['_static']
htmlhelp_basename = 'MapleTreedoc'

html_theme_path = [alabaster.get_path()]
extensions += ['alabaster']
html_theme = 'alabaster'
html_sidebars = {
    '**': [
        'about.html', 'navigation.html',
    ]
}
html_theme_options = {
    'github_user': 'tomokinakamaru',
    'github_repo': 'mapletree',
    'github_banner': True,
    'github_button': False,
    'travis_button': True,
    'analytics_id': 'UA-60884918-1'
}
