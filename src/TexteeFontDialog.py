''' 
Since there is no dialog for font selection for tkinter, it is good to build a custom dialog with all the font familylies and font sizes list 
This will be the base for all font manipulations from the Textee editor.
'''
import Tkinter
import tkFont

class TexteeFontDialog:
	def __init__(self):
		self._fonts = list(tkFont.families()) # fetch all the available fonts at the system level
		self._font.sort()
		self.selected_font = '' # should be passed from the TopLevel() i.e. the root/master window
		pass

	def show_dialog():
		# code to show the selection panel
		pass

	def close_dialog():
		pass