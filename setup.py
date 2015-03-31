import sys
from cx_Freeze import setup, Executable

# Dependencies?

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(   name = 'fo_tag_demo',
        version = '0.1',
        description = 'Simple demo for the fo_tag tagger',
        executables = [Executable('fo_tag_demo_ui.py',base=base)])
