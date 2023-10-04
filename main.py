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

        self.altColor = True  # Whether or not to use alternate bg color for CheckRow

        self.middleFrame = tk.Frame(
            self, bg="#F0F0F0"
        )  # Main area where habits are listed

        buttonFont = tkFont.Font(family="Helvetica", size=20, weight="bold")

        lastWeekBtn = tk.Button(
            self, text="<", font=buttonFont, command=self.decrementWeek
        )
        nextWeekBtn = tk.Button(
            self, text=">", font=buttonFont, command=self.incrementWeek
        )

        lastWeekBtn.grid(row=0, column=0, sticky="nsew")

        nextWeekBtn.grid(row=0, column=2, sticky="nsew")

        self.middleFrame.grid(row=0, column=1, sticky="nsew")

        self.datesHeader = DatesHeader(
            self.middleFrame
        )  # Header with week days and dates
        self.datesHeader.pack(fill=tk.X)

        addHabitBtn = tk.Button(
            self.middleFrame,
            text="+ Habit",
            command=self.addHabit,
            font=buttonFont,
            justify=tk.CENTER,
        )
        addHabitBtn.pack(side=tk.BOTTOM)

        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.loadHabits()

        self.updateChecks()

        # 1. Create label + checks component
        # 2. Add button that adds a CheckRow
        # 3. Create dates header
        # 4. Change dates when side buttons are pressed
        # 5. Create storage structure
        # 6. Create handleCheck function that updates storage structure
        # 7. Save to and load from JSON

    def incrementWeek(self):
        """Increment self.thisWeek by 7 days and update date labels"""

        self.updateHabitDict()

        newWeek = self.thisWeek + timedelta(days=7)
        self.datesHeader.updateLabels(newWeek)
        self.thisWeek = newWeek

        self.updateChecks()

    def decrementWeek(self):
        """Decrement self.thisWeek by 7 days and update date labels"""

        self.updateHabitDict()

        newWeek = self.thisWeek - timedelta(days=7)
        self.datesHeader.updateLabels(newWeek)
        self.thisWeek = newWeek

        self.updateChecks()

    def updateHabitDict(self):
        """Using current state of checks, update habit dictionary"""
        for row in self.checkRows:
            for i, check in enumerate(row.checkVars):
                day = (self.thisWeek + timedelta(days=i)).strftime("%m-%d-%Y")

                if check.get():
                    if day not in self.habitDict[row.habitName]:
                        self.habitDict[row.habitName].append(day)

    def updateChecks(self):
        for row in self.checkRows:
            for i, check in enumerate(row.checkVars):
                day = (self.thisWeek + timedelta(days=i)).strftime("%m-%d-%Y")

                if day in self.habitDict[row.habitName]:
                    check.set(1)
                else:
                    check.set(0)

    def addHabit(self):
        habitName = tkDialog.askstring(
            "Habit Name", "Please enter a name for your new habit."
        )

        while habitName in self.habitDict:
            habitName = tkDialog.askstring(
                "Habit Name Already Exists",
                '"' + habitName + '" already exists. Please choose a new name.',
            )

        newRow = CheckRow(self.middleFrame, habitName, altColor=self.altColor)
        newRow.pack(fill=tk.X)
        self.checkRows.append(newRow)

        self.altColor = not self.altColor

        self.habitDict[habitName] = []

    def loadHabits(self):
        if exists("data.json"):
            jsonFile = open("data.json", "r")

            self.habitDict = json.load(jsonFile)

            jsonFile.close()

            for i, habit in enumerate(self.habitDict):
                newRow = CheckRow(self.middleFrame, habit, altColor=self.altColor)
                newRow.pack(fill=tk.X)
                self.checkRows.append(newRow)

                self.altColor = not self.altColor

    def onClosing(self):
        self.updateHabitDict()

        jsonFile = open("data.json", "w")

        json.dump(self.habitDict, jsonFile)

        jsonFile.close()

        self.destroy()


HabitTracker().mainloop()
