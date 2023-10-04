import tkinter as tk


class CheckRow(tk.Frame):
    """Component with habit label and 7 checks for each day of the week"""

    def __init__(
        self, master=None, habitName: str = "", altColor: bool = False, *args, **kwargs
    ):
        """
        Constructor for CheckRow

        Parameters
        ----------
            master: Any
                Parent window or frame
            habitName: str
                Name of this row's habit
            altColor: bool
                Whether to use alternate bg color
        """
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.habitName = habitName  #

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
