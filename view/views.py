import tkinter as tk
from controller.webServices import webServices
from model.test import test
from controller.testController import testController


class Index(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Vitajte!").grid(row=0, column=0, columnspan=5, pady=5)

        tk.Button(self, text="Vytvoriť test", command=self.createTest).grid(row=1, column=0, pady=5, padx=5, sticky='E')

        tk.Label(self, width=50, height=15, bg="grey").grid(row=3, column=0, padx=10, pady=10)

    def createTest(self):
        self.destroy()
        webServices.setWebServices()
        app = Settings(master=self.master)


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

        tk.Checkbutton(self, text="Mestá", variable=self.city).grid(row=2, column=0, padx=5, pady=5)
        tk.Checkbutton(self, text="Vrchy", variable=self.hill).grid(row=3, column=0, padx=5, pady=5)

        tk.Button(self, text="OK", command=self.testMe).grid(row=4, column=0, padx=5, pady=5, sticky='E')

        tk.Label(self, width=30, height=0, bg="white").grid(row=5, column=0)

    def testMe(self):
        if self.hill.get() == 0 and self.city.get() == 0:
            tk.Label(self, text="Prosím vyplňte nastavenia testu!", fg="red").grid(row=1, column=0, padx=5, pady=5)
        else:
            print("Vrchy: " + str(self.hill.get()))
            print("Mesta: " + str(self.city.get()))
            testController.createTest(str(self.hill.get()), str(self.city.get()))
            self.destroy()
            app = questionForm(master=self.master)


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
        tk.Label(self, text="Otázka " + str(test.questions.__len__() + 1)).grid(row=0, column=0)

        tk.Label(self, text="Typ miesta A:").grid(row=1, column=0, sticky="W")
        if test.hill == '1' and test.town == '1':
            tk.OptionMenu(self, self.locationAType, "Mesto", "Vrch").grid(row=2, column=0, sticky="EW")
        elif test.hill == '1' and test.town == '0':
            tk.Label(self, text="Vrch", fg="blue").grid(row=2, column=0, sticky="W")
            self.locationAType = "Vrch"
        else:
            tk.Label(self, text="Mesto", fg="blue").grid(row=2, column=0, sticky="W")
            self.locationAType = "Mesto"

        tk.Label(self, text="Miesto A:").grid(row=3, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationAName).grid(row=4, column=0, sticky="W")

        tk.Label(self, text="Miesto A - nápoveda:").grid(row=5, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationAHint).grid(row=6, column=0, sticky="W")

        tk.Label(self, width=25, height=0, bg="white").grid(row=7, column=1)

        tk.Label(self, text="Typ miesta B:").grid(row=9, column=0, sticky="W")
        if test.hill == '1' and test.town == '1':
            tk.OptionMenu(self, self.locationBType, "Mesto", "Vrch").grid(row=10, column=0, sticky="EW")
        elif test.hill == '1' and test.town == '0':
            tk.Label(self, text="Vrch", fg="blue").grid(row=10, column=0, sticky="W")
            self.locationBType = "Vrch"
        else:
            tk.Label(self, text="Mesto", fg="blue").grid(row=10, column=0, sticky="W")
            self.locationBType = "Mesto"

        tk.Label(self, text="Miesto B:").grid(row=11, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationBName).grid(row=12, column=0, sticky="W")

        tk.Label(self, text="Miesto B - nápoveda:").grid(row=13, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationBHint).grid(row=14, column=0, sticky="W")

        tk.Button(self, text="Ďalšie", command=self.validation).grid(row=15, column=1, sticky='E')

        tk.Label(self, width=25, height=0, bg="white").grid(row=16, column=1)

    def testMe(self):

        pointA = webServices.setGP(self.locationAName.get(), self.locationAType, self.locationAHint.get())
        pointB = webServices.setGP(self.locationBName.get(), self.locationBType, self.locationBHint.get())

        testController.addQuestion(pointA, pointB)

        self.destroy()

        if test.questions.__len__() > 2 and test.questions.__len__() < 5:
            app = nextQuestionDialog(master=self.master)
        elif test.questions.__len__() == 5:
            app = sucessDialog(master=self.master)
        else:
            app = questionForm(master=self.master)

    def validation(self):
        error = 0

        if test.hill == '1' and test.town == '1':
            self.locationAType = self.locationAType.get()
            self.locationBType = self.locationBType.get()

        if self.locationAType == '':
            tk.Label(self, text="Prosím vyplňte pole!", fg="red").grid(row=2, column=1, padx=5, pady=5)
            error+=1

        if self.locationAName.get() == '':
            tk.Label(self, text="Prosím vyplňte pole!", fg="red").grid(row=4, column=1, padx=5, pady=5)
            error += 1

        if self.locationAHint.get() == '':
            tk.Label(self, text="Prosím vyplňte pole!", fg="red").grid(row=6, column=1, padx=5, pady=5)
            error += 1

        if self.locationBType == '':
            tk.Label(self, text="Prosím vyplňte pole!", fg="red").grid(row=10, column=1, padx=5, pady=5)
            error += 1

        if self.locationBName.get() == '':
            tk.Label(self, text="Prosím vyplňte pole!", fg="red").grid(row=12, column=1, padx=5, pady=5)
            error += 1

        if self.locationBHint.get() == '':
            tk.Label(self, text="Prosím vyplňte pole!", fg="red").grid(row=14, column=1, padx=5, pady=5)
            error += 1

        if error == 0:
            self.testMe();


class nextQuestionDialog(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Prajete si zadať ďalšiu otázku?").grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        tk.Button(self, text="Áno", command=self.yes).grid(row=3, column=0, padx=40, pady=5, sticky='E')
        tk.Button(self, text="Nie", command=self.no).grid(row=3, column=0, padx=40, pady=5, sticky='W')

        tk.Label(self, width=30, height=0, bg="white").grid(row=4, column=0)

    def yes(self):
        self.destroy()
        app = questionForm(master=self.master)

    def no(self):
        self.destroy()

        # TODO save it all

        app = Index(master=self.master)


class sucessDialog(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Test bol úspešne vytvorený").grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        tk.Button(self, text="Rozumiem", command=self.testMe).grid(row=3, column=0, padx=5, pady=5)

        tk.Label(self, width=30, height=0, bg="white").grid(row=4, column=0)

    def testMe(self):
        # TODO save it all

        self.destroy()
        app = Index(master=self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = Index(master=root)
    app.mainloop()
