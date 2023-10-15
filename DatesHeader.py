import tkinter as tk
from datetime import date, timedelta
from typing import List


class DatesHeader:
    """Header component that contains a row of day names and a row of dates"""

    def __init__(self, master=None):
        """Constructor for DatesHeader"""

        today = date.today()
        daysFromMonday = today.weekday()
        self.thisWeek = today - timedelta(
            days=daysFromMonday
        )  # Date of this week's Monday

        nameLabel = tk.Label(
            master, text="Habit Name", justify=tk.CENTER
        )  # Column label for habit names
        nameLabel.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)

        self.dateLabels: List[
            tk.Label
        ] = []  # List for storing date labels, which will all need to be updated

        for i in range(1, 8):
            day = self.thisWeek + timedelta(days=(i - 1))

            dayLabel = tk.Label(
                master,
                text=day.strftime("%a"),
                justify=tk.CENTER,
                borderwidth=1,
                relief="ridge",
                bg="#F0F0F0",
                fg="black",
            )  # Label for day of the week
            dayLabel.grid(row=0, column=i, sticky=tk.NSEW)

            dateLabel = tk.Label(
                master,
                text=day.strftime("%d"),
                justify=tk.CENTER,
                borderwidth=1,
                relief="ridge",
                bg="#F0F0F0",
                fg="black",
            )  # Label for date
            dateLabel.grid(row=1, column=i, sticky=tk.NSEW)
            self.dateLabels.append(dateLabel)

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
