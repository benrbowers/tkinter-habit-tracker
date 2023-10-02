import tkinter as tk
from typing import List


class CheckRow(tk.Frame):
    def __init__(
        self, master=None, habitName: str = "", altColor: bool = False, *args, **kwargs
    ):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.habitName = habitName

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=2)

        bgColor = "#F0F0F0"
        if altColor:
            bgColor = "lightgray"

        habitLabel = tk.Label(
            self, text=(habitName + ":"), anchor=tk.W, bg=bgColor, fg="black"
        )
        habitLabel.grid(row=0, column=0, sticky=tk.NSEW)

        self.checkVars = [tk.IntVar() for _ in range(7)]

        for i in range(1, 8):
            self.grid_columnconfigure(index=i, weight=1)
            check = tk.Checkbutton(
                self,
                variable=self.checkVars[i - 1],
                bg=bgColor,
                activebackground=bgColor,
            )
            check.grid(row=0, column=i, sticky=tk.NSEW)
