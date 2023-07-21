from tkinter import *
from tkinter import messagebox

"""
Borrowed from stack overflow
https://stackoverflow.com/questions/58006764/is-there-a-way-to-ask-for-multiple-choices-in-a-popup-like-messagebox-do
"""


class OptionDialog(Toplevel):
    """
        This dialog accepts a list of options.
        If an option is selected, the results property is to that option value
        If the box is closed, the results property is set to zero
    """

    def __init__(self, parent, title, question, options):
        Toplevel.__init__(self, parent)
        self.lift()
        # self.geometry(str(int((super().winfo_screenwidth()-800)/2)) + '+' + str(int((super().winfo_screenheight()-800)/2)))
        self.geometry(
            "185x45"
            + "+"
            + str(int((super().winfo_screenwidth() - 800) / 2))
            + "+"
            + str(int((super().winfo_screenheight() - 800) / 2))
        )
        self.title(title)
        self.question = question
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.options = options
        self.result = "_"
        self.createWidgets()
        self.grab_set()
        ## wait.window ensures that calling function waits for the window to
        ## close before the result is returned.
        self.wait_window()

    def createWidgets(self):
        frmQuestion = Frame(self)
        Label(frmQuestion, text=self.question).grid()
        frmQuestion.grid(row=1)
        frmButtons = Frame(self)
        frmButtons.grid(row=2)
        column = 0
        for option in self.options:
            btn = Button(
                frmButtons, text=option, command=lambda x=option: self.setOption(x)
            )
            btn.grid(column=column, row=0)
            column += 1

    def setOption(self, optionSelected):
        self.result = optionSelected
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()
