import tkinter as tk
import tkinter.font as tkFont
import tkinter.simpledialog as tkDialog
from CheckRow import CheckRow
from DatesHeader import DatesHeader
from datetime import date, timedelta
from typing import List
import json
from os.path import exists


class HabitTracker(tk.Tk):
    """Habit Tracker program that allow user to define habits and track their progress"""

    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Habit Tracker (made with tkinter)")
        self.geometry("700x500")

        self.habitDict = {}  # Dictionary to store habit info
        self.checkRows: List[CheckRow] = []  # List to store CheckRow components

        # Set up grid for main window
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=9)
        self.grid_columnconfigure(index=2, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

        today = date.today()
        daysFromMonday = today.weekday()
        self.thisWeek = today - timedelta(
            days=daysFromMonday
        )  # Date of this week's Monday

        self.altColor = True # Whether or not to use alternate bg color for CheckRow

        self.middleFrame = tk.Frame(
            self, bg="#F0F0F0"
        )  # Main area where habits are listed

        largeFont = tkFont.Font(family="Helvetica", size=20, weight="bold")

        lastWeekBtn = tk.Button(
            self, text="<", font=largeFont, command=self.decrementWeek
        )
        nextWeekBtn = tk.Button(
            self, text=">", font=largeFont, command=self.incrementWeek
        )

        lastWeekBtn.grid(row=0, column=0, sticky="nsew")

        nextWeekBtn.grid(row=0, column=2, sticky="nsew")

        self.middleFrame.grid(row=0, column=1, sticky="nsew")

        self.monthVar = tk.StringVar(
            self.middleFrame, 
            self.thisWeek.strftime("%B %Y")
        ) # Variable to update month label
        monthLabel = tk.Label(
            self.middleFrame,
            justify=tk.CENTER, 
            font=largeFont, 
            textvariable=self.monthVar,
            bg="#F0F0F0",
            fg="black",
        ) # Label for current month that will update with thisWeek
        monthLabel.pack(fill=tk.X)

        self.datesHeader = DatesHeader(self.middleFrame)  # Header with week days and dates
        self.datesHeader.pack(fill=tk.X)

        addHabitBtn = tk.Button(
            self.middleFrame,
            text="+ Habit",
            command=self.addHabit,
            font=largeFont,
            justify=tk.CENTER,
        )
        addHabitBtn.pack(side=tk.BOTTOM)

        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.loadHabits()

        self.updateChecks()

    def incrementWeek(self):
        """Increment self.thisWeek by 7 days and update date labels"""

        self.updateHabitDict()

        newWeek = self.thisWeek + timedelta(days=7)
        self.datesHeader.updateLabels(newWeek)
        self.thisWeek = newWeek

        self.monthVar.set(newWeek.strftime("%B %Y"))

        self.updateChecks()

    def decrementWeek(self):
        """Decrement self.thisWeek by 7 days and update date labels"""

        self.updateHabitDict()

        newWeek = self.thisWeek - timedelta(days=7)
        self.datesHeader.updateLabels(newWeek)
        self.thisWeek = newWeek

        self.monthVar.set(newWeek.strftime("%B %Y"))

        self.updateChecks()

    def updateHabitDict(self):
        """Using current state of checks, update habit dictionary"""

        for row in self.checkRows:
            for i, check in enumerate(row.checkVars):
                day = (self.thisWeek + timedelta(days=i)).strftime("%m-%d-%Y")

                if check.get():
                    # Check is checked
                    if day not in self.habitDict[row.habitName]:
                        # Selected day is not in habitDict, so add it
                        self.habitDict[row.habitName].append(day)
                elif day in self.habitDict[row.habitName]:
                    # Check is NOT checked AND day is in habitDict, so remove it
                    self.habitDict[row.habitName].remove(day)

    def updateChecks(self):
        """Update check marks according to habit data and the current week"""

        for row in self.checkRows:
            for i, check in enumerate(row.checkVars):
                day = (self.thisWeek + timedelta(days=i)).strftime("%m-%d-%Y")

                if day in self.habitDict[row.habitName]:
                    check.set(1)  # checked
                else:
                    check.set(0)  # unchecked

    def addHabit(self):
        """Prompt user for new habit name and add it to the window"""

        habitName = tkDialog.askstring(
            "Habit Name", "Please enter a name for your new habit."
        )  # Name of the new habit

        while habitName in self.habitDict:
            habitName = tkDialog.askstring(
                "Habit Name Already Exists",
                '"' + habitName + '" already exists. Please choose a new name.',
            )

        newRow = CheckRow(
            self.middleFrame, habitName, altColor=self.altColor
        )  # New row of check marks for the new habits
        newRow.pack(fill=tk.X)
        self.checkRows.append(newRow)

        self.altColor = not self.altColor  # Flip between colors for each row

        self.habitDict[
            habitName
        ] = []  # Add habitName as key to habitDict and init with empty list for dates

    def loadHabits(self):
        """Load habits from file called data.json"""

        if exists("data.json"):
            jsonFile = open("data.json", "r")  # File handle for data.json

            self.habitDict = json.load(jsonFile)

            jsonFile.close()

            for habit in self.habitDict:
                newRow = CheckRow(self.middleFrame, habit, altColor=self.altColor)
                newRow.pack(fill=tk.X)
                self.checkRows.append(newRow)

                self.altColor = not self.altColor

    def onClosing(self):
        """To be executed on window close. Save habits to data.json"""

        self.updateHabitDict()

        jsonFile = open("data.json", "w")  # File handle for data.json

        json.dump(self.habitDict, jsonFile)

        jsonFile.close()

        self.destroy()


HabitTracker().mainloop()
