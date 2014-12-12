''' This class should only hold option definitions for the Textee '''
from Tkinter import *

class TexteeOptions:
	def __init__(self):
		self.wrap = BooleanVar(value=True)
		self.theme = 'dark'
		self.font = 'default'
		self.font_size = '12'
		self.status_bar = BooleanVar(value=True)
		self.spell_check = BooleanVar(value=False)

