from Tkinter import *
from ttk import *

# functions
def close():
    global root
    print "Closing the application"
    root.quit()


# main
root = Tk()

frame1 = Frame(root, width=300, height=300)
frame1.pack()

label1 = Label(frame1, text='Hello World!',)
label1.pack()

button1 = Button(frame1, text='Exit', command=close)
button1.pack()

# how long to live?
root.mainloop()



