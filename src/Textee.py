#!/usr/bin/python
''' IMPORTS '''
import os
import re
import pprint
import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog, tkMessageBox, tkSimpleDialog
import tkFont

from TexteeOptions import *
from TexteeFontDialog import *
from TexteeStatusBar import *
from bindings import *
from utilities import *


''' CLASS '''
class Textee:
    def __init__(self, master):
        self.master = master
        self.theme = 'dark' # the startup will always be opposite
        self.options = TexteeOptions()
        self.status_bar = TexteeStatusBar(master)
        self.create_menu(master)
        self.create_ui(master)
        self.set_bindings(master)
        self.file = None
        self.find_text = ''
        self.font_dialog = ''
        
    def create_menu(self, master):
        self.menu = Menu(master)
        master.config(menu=self.menu)
        
        filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.new_file)
        filemenu.add_command(label="Open...", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As", command=lambda: self.save_file(save_as=True))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)

        editmenu = Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=editmenu)
        editmenu.add_command(label='Copy', command=lambda: event_generate(self.editor, 'Copy'))
        editmenu.add_command(label='Paste', command=lambda: event_generate(self.editor, 'Paste'))
        editmenu.add_command(label='Undo', command=lambda: event_generate(self.editor, 'Undo'))
        editmenu.add_separator()
        editmenu.add_command(label='Goto', command=self.goto_line) # need to develop custom find with regex
        editmenu.add_command(label='Find', command=self.find) # need to develop custom find with regex
        editmenu.add_command(label='Find & Replace', command=do_nothing) # need to test the replace logic in separate playground
        editmenu.add_separator()
        editmenu.add_command(label='Check spelling', command=self.spell_check) # need to see how to use system's grammer check.. if not possible remove it.

        formatmenu = Menu(self.menu)
        self.menu.add_cascade(label='Format', menu=formatmenu)
        formatmenu.add_command(label='Font', command=self.select_font) # pop-up to select system fonts
        formatmenu.add_checkbutton(label='Wrap', onvalue=True, offvalue=False, variable=self.options.wrap, command=self.toggle_wrap)
        
        viewmenu = Menu(self.menu)
        self.menu.add_cascade(label='View', menu=viewmenu)
        viewmenu.add_checkbutton(label='Status bar', onvalue=True, offvalue=False, variable=self.options.status_bar, command=lambda: self.status_bar.display(self.options.status_bar.get()))
        viewmenu.add_command(label='Toggle theme', command=self.toggle_theme)
        
        helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=lambda : self.about())

    def create_ui(self, master):
        self.editor = ScrolledText(master, width=100, height=50, highlightthickness=0)
        self.editor.config(undo=True)
        self.editor.pack(expand=YES, fill='both', padx=0, pady=0)
        self.toggle_theme()
        #print_configs(self.editor)
        
        # Create pop-menu for the entire editor.. do some cool stuff with it
        self.editor.popmenu = Menu(self.master, tearoff=0)
        # TODO : later need to do smart copy/paste i.e. selected text copy of entire line copy
        self.editor.popmenu.add_command(label='Copy', command=lambda: event_generate(self.editor, 'Copy'))
        self.editor.popmenu.add_command(label='Paste', command=lambda: event_generate(self.editor, 'Paste'))
        # TODO : disable undo when not available, not sure if its possible. Need to check research later
        self.editor.popmenu.add_command(label='Undo', command=lambda: event_generate(self.editor, 'Undo'))
        self.editor.popmenu.add_separator()
        # TODO : 'share' this will be the best feature in the editor, share the file with the future textee sharing api
        self.editor.popmenu.add_command(label='Share', command=do_nothing)

        # add status bar by default, it can be hidden from menu
        self.status_bar.update_status('Hi there')
        
    def set_bindings(self, master):
        master.bind_class('Text', '<Control-a>', select_all)
        master.bind_class('Text', '<Control-s>', lambda event: self.save_file())
        master.bind_class('Text', '<Control-o>', lambda event: self.open_file())
        master.bind_class('Text', '<Control-n>', lambda event: self.new_file())
        master.bind_class('Text', '<Control-g>', lambda event: self.goto_line())
        master.bind_class('Text', '<Control-f>', lambda event: self.find())
        master.bind_class('Text', '<Control-;>', lambda event: self.spell_check()) # this function is only for temporoy use - for dev purpose only
        # editor section bindings only
        self.editor.bind('<Button-2>', self.show_right_click_menu) # for right-click
        self.editor.bind('<Button-3>', self.show_right_click_menu) # for middle-click (scroll press)

        self.display_current_position()


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

    def save_file(self, save_as=False):
        data = self.editor.get('1.0', END+'-1c')
        save_as_file = None

        # if saving the file by creation
        if self.file == None or save_as == True:
            save_as_file = tkFileDialog.asksaveasfilename() # attempt to select the filename, the user can select cancel so check agian below

        # the above could result in None if the user cancels the dialog
        if save_as_file:
            self.file = save_as_file

        # final check, as both the above could result in None
        if self.file != None:
            outfile = open(self.file, 'w')
            outfile.write(data)
            outfile.close()

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
            # theme for misspelled words
            self.editor.tag_configure("misspelled", foreground="red", underline=True)
            self.theme = 'dark'
        else:
            self.editor.config(bg='white', fg='black', insertbackground='black',highlightcolor='white')
            self.editor.frame.config(bg='white')
            # theme for misspelled words
            self.editor.tag_configure("misspelled", foreground="red", underline=True)
            self.theme = 'light'

    def toggle_wrap(self):
        # self.editor.cget('wrap') # gets the config value
        if not self.options.wrap.get():
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
            
    def select_font(self):
        self.font_dialog = TexteeFontDialog(self.master)
        fs = 12 # default size for any font selected

        if self.font_dialog.selected_font_family:
            ff = self.font_dialog.selected_font_family
        
        if self.font_dialog.selected_font_size:
            fs = self.font_dialog.selected_font_size

        print ff, fs, " - font properties"

        if ff and fs > 0:
            self.default_font = tkFont.Font(self.master, family=ff, size=fs)
            self.editor.config(font=self.default_font)

    def show_right_click_menu(self, event):
        print 'going to display popmenu at', event.x_root, event.y_root
        try:
            self.editor.popmenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # TODO: not sure why we need this, pasting it from the documentation. Later check to remove it
            self.editor.popmenu.grab_release()

    def spell_check(self):
        # check if the dictonary exists in the system (only mac and linux have it at this location)
        # TODO: to check on windows how to do?
        print "inside the spell check"
        if not os.path.exists('/usr/share/dict/words'):
            return

        with open('/usr/share/dict/words', 'r') as words_file:
            system_words = words_file.read().split('\n') 
            current_file_lines = self.editor.get('1.0', END+'-1c').split('\n') 

            for lineno, current_line in enumerate(current_file_lines):
                current_line_words = re.split('\W', current_line)
                columnposition = 0 # this is to ignore the white space with which we split above, the marking of the invalid word should be be without the space
                for word in current_line_words:
                    start_index = '%s.%s' % (lineno+1, columnposition)
                    end_index = '%s+%dc' % (start_index, len(word))
                    if word in system_words:
                        self.editor.tag_remove('misspelled', start_index, end_index)
                    else:
                        self.editor.tag_add('misspelled', start_index, end_index)
                    columnposition += len(word)+1 # take into account the space
     
    def display_current_position(self):
        cursor_position =  self.editor.index("insert").replace('.', ',')
        self.status_bar.update_status(cursor_position)
        self.master.after(self.status_bar.update_interval, self.display_current_position)

    def about(self):
        tkMessageBox.showinfo("About", "Textee - A stupid text editor")

    def exit(self, master):
        if tkMessageBox.askokcancel("Quit", "Are you sure?"):
            master.destroy()



