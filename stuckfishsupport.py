import tkinter as tk
from tkinter.messagebox import showinfo

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

def convert_col(col):
    if col == 1:
        return "a"
    elif col == 2:
        return "b"
    elif col == 3:
        return "c"
    elif col == 4:
        return "d"
    elif col == 5:
        return "e"
    elif col == 6:
        return "f"
    elif col == 7:
        return "g"
    elif col == 8:
        return "h"
    elif col == "a":
        return 1
    elif col == "b":
        return 2
    elif col == "c":
        return 3
    elif col == "d":
        return 4
    elif col == "e":
        return 5
    elif col == "f":
        return 6
    elif col == "g":
        return 7
    elif col == "h":
        return 8
    else:
        #error
        return


