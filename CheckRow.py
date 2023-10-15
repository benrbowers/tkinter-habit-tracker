import tkinter as tk


class CheckRow:
    """Component with habit label and 7 checks for each day of the week"""

    def __init__(
        self, row: int, master=None, habitName: str = "", altColor: bool = False
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

        self.habitName = habitName  # Name of this row's habit

        bgColor = "#F0F0F0"
        if altColor:
            bgColor = "lightgray"

        habitLabel = tk.Label(
            master, text=(habitName + ":"), anchor=tk.W, bg=bgColor, fg="black"
        )
        habitLabel.grid(row=row, column=0, sticky=tk.NSEW)

        self.checkVars = [tk.IntVar() for _ in range(7)]

        for i in range(1, 8):
            check = tk.Checkbutton(
                master,
                variable=self.checkVars[i - 1],
                bg=bgColor,
                activebackground=bgColor,
            )
            check.grid(row=row, column=i, sticky=tk.NSEW)
