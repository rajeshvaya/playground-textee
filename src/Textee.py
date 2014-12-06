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
        self.find_text = ''

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

        editmenu = Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=editmenu)
        editmenu.add_command(label='Copy', command=lambda: event_generate(self.editor, 'Copy'))
        editmenu.add_command(label='Paste', command=lambda: event_generate(self.editor, 'Paste'))
        editmenu.add_command(label='Undo', command=lambda: event_generate(self.editor, 'Undo'))
        editmenu.add_separator()
        editmenu.add_command(label='Find', command=do_nothing) # need to develop custom find with regex
        editmenu.add_command(label='Find & Replace', command=do_nothing) # need to test the replace logic in separate playground
        editmenu.add_separator()
        editmenu.add_command(label='Check spelling & grammer', command=do_nothing) # need to see how to use system's grammer check.. if not possible remove it.

        formatmenu = Menu(self.menu)
        self.menu.add_cascade(label='Format', menu=formatmenu)
        formatmenu.add_command(label='Font', command=do_nothing) # pop-up to select system fonts
        formatmenu.add_command(label='Toggle wrap', command=self.toggle_wrap)
        
        viewmenu = Menu(self.menu)
        self.menu.add_cascade(label='View', menu=viewmenu)
        viewmenu.add_command(label='Toggle theme', command=self.toggle_theme)
        
        helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=lambda : self.about())

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
        master.bind_class('Text', '<Control-f>', lambda event: self.find())

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

    def find(self):
        self.find_text = tkSimpleDialog.askstring("Textee", "Enter text to search", initialvalue=self.find_text)
        if self.find_text:
            start_pos = self.editor.search(self.find_text, '1.0', stopindex=END, nocase=True)
            if(start_pos):
                end_pos = '%s+%sc' % (start_pos, len(self.find_text))
                self.editor.tag_add(SEL, start_pos, end_pos)
                self.editor.mark_set(INSERT, end_pos) # mark the cursor to end of find text to start editing
                self.editor.see(INSERT) # bing the cursor position in the viewport incase of long text causinng scrollbar
                self.editor.focus_set() # strangely tkinter doesnt return focus after prompt
            else:
                tkMessageBox.showinfo("Textee", "No matches found")
        else:
            self.editor.focus_set() # strangely tkinter doesnt return focus after prompt
            

    def about(self):
        tkMessageBox.showinfo("About", "Textee - A stupid text editor")

    def exit(self, master):
        if tkMessageBox.askokcancel("Quit", "Are you sure?"):
            master.destroy()



