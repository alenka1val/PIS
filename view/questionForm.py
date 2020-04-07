import tkinter as tk
from model.geographic_point import geographic_point

class questionForm(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.locationAName = tk.StringVar()
        self.locationAHint = tk.StringVar()
        self.locationAType = tk.StringVar()
        self.locationBName = tk.StringVar()
        self.locationBHint = tk.StringVar()
        self.locationBType = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Testová otázka").grid(row=0, column=0)

        tk.Label(self, text="Miesto A").grid(row=1, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationAName).grid(row=2, column=0, sticky="W")

        tk.Label(self, text="Miesto A - nápoveda").grid(row=3, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationAHint).grid(row=4, column=0, sticky="W")

        tk.Label(self, text="Typ miesta A").grid(row=5, column=0, sticky="W")
        tk.OptionMenu(self, self.locationAType, "Miesto", "Vrch").grid(row=6, column=0, sticky="EW")

        tk.Label(self, text="Miesto B").grid(row=7, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationBName).grid(row=8, column=0, sticky="W")

        tk.Label(self, text="Miesto B - nápoveda").grid(row=9, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationBHint).grid(row=10, column=0, sticky="W")

        tk.Label(self, text="Typ miesta B").grid(row=11, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationBType).grid(row=12, column=0, sticky="W")

        tk.Button(self, text="OK", command=self.testMe).grid(row=13, column=1, sticky='E')

        tk.Label(self, width=25, height=0, bg="white").grid(row=14, column=1)




    def testMe(self):

        pointA = geographic_point(self.locationAName.get(), self.locationAType.get(), self.locationAHint.get())
        pointB = geographic_point(self.locationBName.get(), self.locationBType.get(), self.locationAHint.get())