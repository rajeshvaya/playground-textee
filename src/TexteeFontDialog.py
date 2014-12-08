''' 
Since there is no dialog for font selection for tkinter, it is good to build a custom dialog with all the font familylies and font sizes list 
This will be the base for all font manipulations from the Textee editor.
'''
import Tkinter
from Tkinter import *
import tkSimpleDialog
import tkFont

class TexteeFontDialog(tkSimpleDialog.Dialog):
	def body(self, master):
		# get data 
		self.fonts = list(tkFont.families())
		self.fonts.sort()

		# prepare the widgets
		self.listbox_font_family = Listbox(master)
		self.entry_font_size = Entry(master)
		self.lbl_font_family = Label(master, text="Choose font: ")
		self.lbl_font_size = Label(master, text="Choose font size: ")

		for font in self.fonts:
			self.listbox_font_family.insert(END, font)

		# grid the widgets onto the window
		self.lbl_font_family.grid(row=0)
		self.lbl_font_size.grid(row=1)
		self.listbox_font_family.grid(row=0, column=1)
		self.entry_font_size.grid(row=1, column=1)
		
	def apply(self):
		self.selected_font_family = self.fonts[int(self.listbox_font_family.curselection()[0])]
		self.selected_font_size = self.entry_font_size.get()
		pass
