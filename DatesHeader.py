import tkinter as tk
from datetime import date, timedelta
from typing import List


class DatesHeader(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        today = date.today()
        daysFromMonday = today.weekday()
        self.thisWeek = today - timedelta(days=daysFromMonday)

        dayFrame = tk.Frame(self)
        dayFrame.grid_rowconfigure(index=0, weight=1)
        dayFrame.grid_columnconfigure(index=0, weight=2)
        numFrame = tk.Frame(self)
        numFrame.grid_rowconfigure(index=0, weight=1)
        numFrame.grid_columnconfigure(index=0, weight=2)

        self.numLabels: List[tk.Label] = []

        for i in range(1, 8):
            day = self.thisWeek + timedelta(days=(i - 1))

            dayFrame.grid_columnconfigure(index=i, weight=1)
            numFrame.grid_columnconfigure(index=i, weight=1)

            dayLabel = tk.Label(
                dayFrame,
                text=day.strftime("%a"),
                justify=tk.CENTER,
                borderwidth=1,
                relief="ridge",
            )
            dayLabel.grid(row=0, column=i, sticky=tk.NSEW)

            numLabel = tk.Label(
                numFrame,
                text=day.strftime("%d"),
                justify=tk.CENTER,
                borderwidth=1,
                relief="ridge",
            )
            numLabel.grid(row=0, column=i, sticky=tk.NSEW)
            self.numLabels.append(numLabel)

        dayFrame.pack(fill=tk.X, expand=True)
        numFrame.pack(fill=tk.X, expand=True)

    def updateLabels(self, newWeek: date):
        for i, label in enumerate(self.numLabels):
            day = newWeek + timedelta(days=(i))

            label["text"] = day.strftime("%d")
