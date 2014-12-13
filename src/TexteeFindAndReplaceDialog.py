''' 
This will be the base for all find and replace dialogs for all uses in Textee editor
'''
import Tkinter
from Tkinter import *
import tkSimpleDialog

class TexteeFindAndReplaceDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		self.resizable(0,0)
		self.lbl_find_text = Label(master, text="Find Text: ", anchor='w')
		self.lbl_replace_with = Label(master, text="Replace with: ", anchor='w')
		self.entry_find_text = Entry(master)
		self.entry_replace_with = Entry(master)

		# grid the widgets onto the window
		self.lbl_find_text.grid(row=0, sticky='w')
		self.entry_find_text.grid(row=0, column=1)
		self.lbl_replace_with.grid(row=1, sticky='w')
		self.entry_replace_with.grid(row=1, column=1)		
		
	def apply(self):
		# do find and replace here. Will need to centralize the find function outside of the main Textee.py class. 
		# TODO : convert the find function of the Textee.find to a class of its own
		pass
