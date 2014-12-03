# imports
import sys
from setuptools import setup

# declarations
MAIN_SCRIPT = '../src/main.py'
ICON_WINDOWS = '../src/textee.ico'
ICON_MAC = '../src/textee.icns'
PLATFORM = sys.platform

# Build OSX .app file
if PLATFORM == 'darwin':
	import py2app
	options = {'iconfile': ICON_MAC}
	setup(
		app = [MAIN_SCRIPT],
		data_files = [],
		options = {'py2app': options},
		setup_requires = ['py2app']
	)
