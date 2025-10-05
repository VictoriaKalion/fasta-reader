import os
import sys

# Добавляем путь к нашим классам
sys.path.insert(0, os.path.abspath('../../src'))

project = 'FASTA Reader'
copyright = '05.10.2025, Victoria'
author = 'Victoria'
release = '1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinxdoc'
html_static_path = ['_static']

master_doc = 'index'