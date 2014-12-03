
import os
import Tkinter
from Textee import Textee

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

def main():

    root = Tkinter.Tk(className=" Textee")
    root.title("Textee - A Stupid Text Editor")
    app = Textee(root)
    root.mainloop()

if __name__ == '__main__':
    main()




