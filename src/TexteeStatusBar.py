'''
This class will be only used for StatusBar of the Main window. It will contain methods to communicate with the master from the Textee class. 
Basic functionality: hide/show status bar, show line no and column no, status messages like processing
'''
from Tkinter import Frame, StringVar, Label, SUNKEN, X, Y

class TexteeStatusBar(Frame):
	def __init__(self, master):
		Frame.__init__(self, master)
		self.status_label_variable = StringVar()
		self.status_label = Label(self, relief=SUNKEN, bd=1, textvariable=self.status_label_variable)
		self.status_label.pack(fill=X)
		self.pack() # By default enable the status bar

	def hide(self):
		this.pack_forget()
	
	def show(self):
		this.pack()

	def update_status(self, message):
		this.status_label_variable = message

	def appened_status(self, message):
		this.status_label_variable += message

	def timeout_status(self, message, timeout=5):
		# display the previous status after tempory timeout status message
		pass
		
	# use to display back the old value after displaying temporary value
	def reset_status(self):
		pass


