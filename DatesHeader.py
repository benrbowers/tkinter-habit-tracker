import tkinter as tk
from datetime import date, timedelta
from typing import List


class DatesHeader(tk.Frame):
    """Header component that contains a row of day names and a row of dates"""

    def __init__(self, *args, **kwargs):
        """Constructor for DatesHeader"""

        tk.Frame.__init__(self, *args, **kwargs)
        today = date.today()
        daysFromMonday = today.weekday()
        self.thisWeek = today - timedelta(
            days=daysFromMonday
        )  # Date of this week's Monday

        dayFrame = tk.Frame(
            self
        )  # Frame for labels containing day names (e.g., Mon, Tue)
        dayFrame.grid_rowconfigure(index=0, weight=1)
        dayFrame.grid_columnconfigure(index=0, weight=2)

        dateFrame = tk.Frame(self)  # Frame for labels containing dates (e.g., 30, 31)
        dateFrame.grid_rowconfigure(index=0, weight=1)
        dateFrame.grid_columnconfigure(index=0, weight=2)

        self.dateLabels: List[
            tk.Label
        ] = []  # List for storing date labels, which will all need to be updated

        for i in range(1, 8):
            day = self.thisWeek + timedelta(days=(i - 1))

            dayFrame.grid_columnconfigure(index=i, weight=1)
            dateFrame.grid_columnconfigure(index=i, weight=1)

            dayLabel = tk.Label(
                dayFrame,
                text=day.strftime("%a"),
                justify=tk.CENTER,
                borderwidth=1,
                relief="ridge",
                bg="#F0F0F0",
                fg="black",
            )  # Label for day of the week
            dayLabel.grid(row=0, column=i, sticky=tk.NSEW)

            dateLabel = tk.Label(
                dateFrame,
                text=day.strftime("%d"),
                justify=tk.CENTER,
                borderwidth=1,
                relief="ridge",
                bg="#F0F0F0",
                fg="black",
            )  # Label for date
            dateLabel.grid(row=0, column=i, sticky=tk.NSEW)
            self.dateLabels.append(dateLabel)

        dayFrame.pack(fill=tk.X, expand=True)
        dateFrame.pack(fill=tk.X, expand=True)

    def updateLabels(self, newWeek: date):
        """
        Updates header labels according to date provided

        Parameters
        ----------
            newWeek: date
                Date of the Monday for selected week
        """
        for i, label in enumerate(self.dateLabels):
            day = newWeek + timedelta(
                days=(i)
            )  # Monday's date + i, starting at 0 for Mon-Sun

            label["text"] = day.strftime("%d")
