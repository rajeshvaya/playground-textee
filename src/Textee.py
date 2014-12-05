#!/usr/bin/python
''' IMPORTS '''
import pprint
import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog, tkMessageBox, tkSimpleDialog

from bindings import *
from utilities import *


''' CLASS '''
class Textee:
    def __init__(self, master):
        self.master = master
        self.theme = 'dark' # the startup will always be opposite
        self.create_menu(master)
        self.create_ui(master)
        self.set_bindings(master)
        self.file = None

    def create_menu(self, master):
        self.menu = Menu(master)
        master.config(menu=self.menu)
        
        filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)

        viewmenu = Menu(self.menu)
        self.menu.add_cascade(label='View', menu=viewmenu)
        viewmenu.add_command(label='Toggle theme', command=self.toggle_theme)
        viewmenu.add_command(label='Toggle wrap', command=self.toggle_wrap)
        
        helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.about)

    def create_ui(self, master):
        self.editor = ScrolledText(master, width=100, height=50, highlightthickness=0)
        self.editor.config(undo=True)
        self.editor.pack(fill=X, padx=0, pady=0)
        self.toggle_theme()
        print_configs(self.editor)
        

    def set_bindings(self, master):
        master.bind_class('Text', '<Control-a>', select_all)
        master.bind_class('Text', '<Control-s>', lambda event: self.save_file())
        master.bind_class('Text', '<Control-o>', lambda event: self.open_file())
        master.bind_class('Text', '<Control-n>', lambda event: self.new_file())
        master.bind_class('Text', '<Control-g>', lambda event: self.goto_line())

    def new_file(self):
        self.file = None
        self.editor.delete('1.0', END+'-1c') # clear all the contents

    def open_file(self):
        self.file = tkFileDialog.askopenfilename(parent=self.master,title='Select a file')
        if self.file != None and self.file != '':
            self.editor.delete('1.0', END+'-1c') # clear all the contents
            infile = open(self.file, 'r')
            contents = infile.read()
            self.editor.insert('1.0',contents)
            infile.close()

    def save_file(self):
        data = self.editor.get('1.0', END+'-1c')

        if self.file != None:
            outfile = open(self.file, 'w')
            outfile.write(data)
            outfile.close()
        else:
            self.file = tkFileDialog.asksaveasfile(mode='w')
            if self.file != None:
                self.file.write(data)
                self.file.close()

    def goto_line(self):
        lineno = tkSimpleDialog.askinteger('Textee', 'Goto line:')
        if lineno > 0:
            self.editor.mark_set(INSERT, lineno + 0.0) #convert to float
            self.editor.see(INSERT)
        self.editor.focus_set()

    def toggle_theme(self):
        if self.theme == 'light':
            self.editor.config(bg='black', fg='white', insertbackground='white',highlightcolor='black')
            self.editor.frame.config(bg='black')
            self.theme = 'dark'
        else:
            self.editor.config(bg='white', fg='black', insertbackground='black',highlightcolor='white')
            self.editor.frame.config(bg='white')
            self.theme = 'light'

    def toggle_wrap(self):
        if self.editor.cget('wrap') != 'none':
            self.editor.config(wrap='none')
        else:
            self.editor.config(wrap='word')

    def about(self, master):
        tkMessageBox.showinfo("About", "Textee - A stupid text editor")

    def exit(self, master):
        if tkMessageBox.askokcancel("Quit", "Are you sure?"):
            master.destroy()



