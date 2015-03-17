# -*- coding: utf-8 -*-

import alabaster
import sphinx_rtd_theme
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
version = '0.6.1'
release = '0.6.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_static_path = ['_static']
htmlhelp_basename = 'MapleTreedoc'
