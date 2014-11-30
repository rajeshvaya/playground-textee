#!/usr/bin/python
''' IMPORTS '''
import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog, tkMessageBox

from bindings import *
from utilities import *


''' CLASS '''
class Textee:
    def __init__(self, master):
        self.master = master
        self.create_menu(master)
        self.create_ui(master)
        self.set_bindings(master)

    def create_menu(self, master):
        self.menu = Menu(master)
        master.config(menu=self.menu)
        filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=do_nothing)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)
        helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.about)

    def create_ui(self, master):
        self.editor = ScrolledText(master, width=100, height=50)
        self.editor.pack()

    def set_bindings(self, master):
        master.bind_class('Text', '<Control-a>', select_all)

    def open_file(self):
        self.file = tkFileDialog.askopenfile(parent=self.master,mode='rb',title='Select a file')
        if self.file != None:
            contents = self.file.read()
            self.editor.insert('1.0',contents)
            self.file.close()

    def save_file(self):
        file = tkFileDialog.asksaveasfile(mode='w')
        if file != None:
            data = self.editor.get('1.0', END+'-1c')
            file.write(data)
            file.close()

    def about(self, master):
        tkMessageBox.showinfo("About", "Textee - A stupid text editor")

    def exit(self, master):
        if tkMessageBox.askokcancel("Quit", "Are you sure?"):
            master.destroy()



