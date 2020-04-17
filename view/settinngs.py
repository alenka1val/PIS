import tkinter as tk

from controller.testController import testController

class Settings(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.city = tk.IntVar()
        self.hill = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Nastavenia testu").grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        tk.Checkbutton(self, text="Mestá", variable=self.city).grid(row=1, column=0, padx=5, pady=5)
        tk.Checkbutton(self, text="Vrchy", variable=self.hill).grid(row=2, column=0, padx=5, pady=5)

        tk.Button(self, text="OK", command=self.testMe).grid(row=3, column=0, padx=5, pady=5, sticky='E')

        tk.Label(self, width=30, height=0, bg="white").grid(row=4, column=0)


    def testMe(self):
        print("Vrchy: " + str(self.hill.get()))
        print("Mesta: " + str(self.city.get()))
        testController.createTest(self, str(self.hill.get()), str(self.city.get()))
