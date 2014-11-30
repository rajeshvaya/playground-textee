
import Tkinter
from Textee import Textee

# def select_all(event):
#     print "Going to select all"
#     event.widget.tag_add(SEL, "1.0", "end-1c")
#     event.widget.mark_set(INSERT, "1.0")
#     event.widget.see(INSERT)
#     return "break"

# root = Tkinter.Tk(className=" Textee")
# root.bind_class('Text', '<Control-a>', select_all)

# textPad = ScrolledText(root, width=100, height=50)

# def open_command():
#     file = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
#     if file != None:
#             contents = file.read()
#             textPad.insert('1.0',contents)
#             file.close()

# def save_command():
#     global textPad
#     file = tkFileDialog.asksaveasfile(mode='w')
#     if file != None:
#         data = textPad.get('1.0', END+'-1c')
#         file.write(data)
#         file.close()

# def exit_command():
#     if tkMessageBox.askokcancel("Quit", "Are you sure?"):
#         root.destroy()

# def about_command():
#     label = tkMessageBox.showinfo("About", "Textee - A stupid text editor")


# menu = Menu(root)
# root.config(menu=menu)
# filemenu = Menu(menu)
# menu.add_cascade(label="File", menu=filemenu)
# filemenu.add_command(label="New", command=do_nothing)
# filemenu.add_command(label="Open...", command=open_command)
# filemenu.add_command(label="Save", command=save_command)
# filemenu.add_separator()
# filemenu.add_command(label="Exit", command=exit_command)
# helpmenu = Menu(menu)
# menu.add_cascade(label="Help", menu=helpmenu)
# helpmenu.add_command(label="About...", command=about_command)

# #
# textPad.pack()
# root.mainloop()

def main():
    root = Tkinter.Tk(className=" Textee")
    app = Textee(root)
    root.mainloop()

if __name__ == '__main__':
    main()




