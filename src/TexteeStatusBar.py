'''
This class will be only used for StatusBar of the Main window. It will contain methods to communicate with the master from the Textee class. 
Basic functionality: hide/show status bar, show line no and column no, status messages like processing
'''
from Tkinter import Frame, StringVar, Label, SUNKEN, X, Y, BOTTOM, LEFT, RIGHT
import tkFont

class TexteeStatusBar(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.update_interval = 100 # updat the statusbar with line numbers after every 100ms
		self.status_label_variable = StringVar()
		font = tkFont.Font(self.master, family='Arial', size='10')
		self.status_label = Label(self, relief=SUNKEN, bd=1, textvariable=self.status_label_variable, anchor='w', font=font)
		self.status_label.pack(fill=X) # this will pack the label within the status bar, statusbar needs to be packed when needed
		self.pack(side=BOTTOM, fill=X)

	def display(self, flag):
		self.show() if flag else self.hide()

	def hide(self):
		self.pack_forget()
	
	def show(self):
		# TODO : this is not working after hiding, it works on the child label but not parent. fix it later
		self.pack(side=BOTTOM, fill=X)

	def update_status(self, message):
		self.status_label_variable.set(message)

	def appened_status(self, message):
		updated_status = self.status_label_variable.get() + ' %s' % (message)
		self.status_label_variable.set(updated_status) 

	def timeout_status(self, message, timeout=5):
		# TODO : display the previous status after tempory timeout status message
		pass
		
	# TODO :use to display back the old value after displaying temporary value
	def reset_status(self):
		pass


