#!/usr/bin/python

import pprint
import Tkinter
from Tkinter import *


def select_all(event):
    print "Going to select all"
    event.widget.tag_add(SEL, "1.0", "end-1c")
    event.widget.mark_set(INSERT, "1.0")
    event.widget.see(INSERT)
    return "break"

def print_configs(widget):
	pprint.pprint(widget.config())