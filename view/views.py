import tkinter as tk
from controller.webServices import webServices
from model.test import test
from controller.testController import testController
from model.geographic_point import geographic_point
from tkinter import messagebox


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
            message="Prosím vyplňte nastavenia testu!"
            messagebox.showerror(title="Chyba", message=message)
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
        self.posib = tk.StringVar(self)
        self.posib2 = tk.StringVar(self)

        self.moznostiA = []
        self.moznostiB = []

        self.locationATypeString = ''
        self.locationBTypeString = ''

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Otázka " + str(test.questions.__len__() + 1)).grid(row=0, column=0)

        tk.Label(self, text="Typ miesta A:").grid(row=1, column=0, sticky="W")
        if test.hill == '1' and test.town == '1':
            tk.OptionMenu(self, self.locationAType, "Mesto", "Vrch").grid(row=2, column=0, sticky="EW")
        elif test.hill == '1' and test.town == '0':
            tk.Label(self, text="Vrch", fg="blue").grid(row=2, column=0, sticky="W")
            self.locationATypeString = "Vrch"
        else:
            tk.Label(self, text="Mesto", fg="blue").grid(row=2, column=0, sticky="W")
            self.locationATypeString = "Mesto"

        tk.Label(self, text="Miesto A:").grid(row=3, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationAName).grid(row=4, column=0, sticky="W")
        tk.Button(self, text="Vyhľadaj", command=self.searchA).grid(row=4, column=1, sticky='W')
        self.menuA = tk.OptionMenu(self, self.posib, ())
        self.menuA.grid(row=4, column=2, sticky="W")

        tk.Label(self, text="Miesto A - nápoveda:").grid(row=5, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationAHint).grid(row=6, column=0, sticky="W")

        tk.Label(self, width=25, height=0, bg="white").grid(row=7, column=1)

        tk.Label(self, text="Typ miesta B:").grid(row=9, column=0, sticky="W")
        if test.hill == '1' and test.town == '1':
            tk.OptionMenu(self, self.locationBType, "Mesto", "Vrch").grid(row=10, column=0, sticky="EW")
        elif test.hill == '1' and test.town == '0':
            tk.Label(self, text="Vrch", fg="blue").grid(row=10, column=0, sticky="W")
            self.locationBTypeString = "Vrch"
        else:
            tk.Label(self, text="Mesto", fg="blue").grid(row=10, column=0, sticky="W")
            self.locationBTypeString = "Mesto"

        tk.Label(self, text="Miesto B:").grid(row=11, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationBName).grid(row=12, column=0, sticky="W")
        tk.Button(self, text="Vyhľadaj", command=self.searchB).grid(row=12, column=1, sticky='W')
        self.menuB = tk.OptionMenu(self, self.posib2, ())
        self.menuB.grid(row=12, column=2, sticky="W")

        tk.Label(self, text="Miesto B - nápoveda:").grid(row=13, column=0, sticky="W")
        tk.Entry(self, textvariable=self.locationBHint).grid(row=14, column=0, sticky="W")

        tk.Button(self, text="Ďalšie", command=self.validation).grid(row=15, column=1, sticky='E')

        tk.Label(self, width=25, height=0, bg="white").grid(row=16, column=1)

    def testMe(self):

        miesto = self.posib.get()
        print(miesto)

        lat1 = self.moznostiA[int(miesto[0])].coord_lat
        lon1 = self.moznostiA[int(miesto[0])].coord_lon

        miesto = self.posib2.get()
        lat2 = self.moznostiB[int(miesto[0])].coord_lat
        lon2 = self.moznostiB[int(miesto[0])].coord_lon

        pointA = geographic_point(self.locationAName.get(), self.locationATypeString, self.locationAHint.get(), lat1,
                                  lon1)
        pointB = geographic_point(self.locationBName.get(), self.locationBTypeString, self.locationBHint.get(), lat2,
                                  lon2)

        testController.addQuestion(pointA, pointB)

        self.destroy()

        if test.questions.__len__() > 1 and test.questions.__len__() < 5:
            app = nextQuestionDialog(master=self.master)
        elif test.questions.__len__() == 5:
            app = sucessDialog(master=self.master)
        else:
            app = questionForm(master=self.master)

    def validation(self):
        error = 0
        message = ""

        if test.hill == '1' and test.town == '1':
            self.locationATypeString = self.locationAType.get()
            self.locationBTypeString = self.locationBType.get()

        if self.locationATypeString == '':
            errmes = "Prosím vyplňte pole: Typ miesta A\n"
            message = message + errmes

            error += 1

        if self.locationAName.get() == '':
            errmes = "Prosím vyplňte pole: Miesto A\n"
            message = message + errmes

            error += 1

        if self.locationAHint.get() == '':
            errmes = "Prosím vyplňte pole: Miesto A - nápoveda\n"
            message = message + errmes

            error += 1

        if self.locationBTypeString == '':
            errmes = "Prosím vyplňte pole: Typ miesta B\n"
            message = message + errmes

            error += 1

        if self.locationBName.get() == '':
            errmes = "Prosím vyplňte pole: Miesto B\n"
            message = message + errmes

            error += 1

        if self.locationBHint.get() == '':
            errmes = "Prosím vyplňte pole: Miesto B - nápoveda\n"
            message = message + errmes

            error += 1

        if error == 0:
            self.testMe()
        else:
            messagebox.showerror(title="Chyba", message=message)

    def multiple(self):
        print("dostal som sa sem")
        tk.OptionMenu(self, self.locationBType, "Mesto", "Vrch").grid(row=10, column=0, sticky="EW")
        return "veverka"

    def searchA(self):
        error = 0
        message = ""

        if test.hill == '1' and test.town == '1':
            self.locationATypeString = self.locationAType.get()

        if self.locationATypeString == '':
            errmes = "Prosím vyplňte pole: Typ miesta A\n"
            message = message + errmes

            error += 1
        if self.locationAName.get() == '':
            errmes = "Prosím vyplňte pole: Miesto A\n"
            message = message + errmes

            error += 1

        if error == 0:
            point = webServices.setGP(self.locationAName.get(), self.locationATypeString)

            if isinstance(point, str):
                error_message = "Niektoré zo zadaných miest sa nepodarilo nájsť. \n Chybne zadané údaje: {} .\n Overte správnosť zadaných údajov, alebo zvoľte iné.".format(
                    point)
                messagebox.showerror(title='Chyba!', message=error_message)

            elif len(point) > 0:
                self.moznostiA = point
                moznosti = []
                for x in range(len(point)):
                    moznost = (str(x) + ': ' + point[x].name + ' lat: ' + str(point[x].coord_lat) + ", lon: " + str(
                        point[x].coord_lon))
                    moznosti.append(moznost)

                self.posib.set('')
                self.menuA['menu'].delete(0, 'end')
                for choice in moznosti:
                    self.menuA['menu'].add_command(label=choice, command=tk._setit(self.posib, choice))
                self.posib.set(moznosti[0])
        else:
            messagebox.showerror(title="Chyba", message=message)

    def searchB(self):
        error = 0
        message = ""

        if test.hill == '1' and test.town == '1':
            self.locationBTypeString = self.locationBType.get()

        if self.locationBTypeString == '':
            errmes = "Prosím vyplňte pole: Typ miesta B\n"
            message = message + errmes
            error += 1
        if self.locationBName.get() == '':
            errmes = "Prosím vyplňte pole: Miesto B\n"
            message = message + errmes
            error += 1

        if error == 0:
            point = webServices.setGP(self.locationBName.get(), self.locationBTypeString)

            if isinstance(point, str):
                error_message = "Niektoré zo zadaných miest sa nepodarilo nájsť. \n Chybne zadané údaje: {} .\n Overte správnosť zadaných údajov, alebo zvoľte iné.".format(
                    point)
                messagebox.showerror(title='Chyba!', message=error_message)

            elif len(point) > 0:
                self.moznostiB = point
                moznosti = []
                for x in range(len(point)):
                    moznost = (str(x) + ': ' + point[x].name + ' lat: ' + str(point[x].coord_lat) + ", lon: " + str(
                        point[x].coord_lon))
                    moznosti.append(moznost)

                self.posib2.set('')
                self.menuB['menu'].delete(0, 'end')
                for choice in moznosti:
                    self.menuB['menu'].add_command(label=choice, command=tk._setit(self.posib2, choice))
                self.posib2.set(moznosti[0])
        else:
            messagebox.showerror(title="Chyba", message=message)

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

        webServices.saveTest()

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

        self.destroy()
        app = Index(master=self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = Index(master=root)
    app.mainloop()
