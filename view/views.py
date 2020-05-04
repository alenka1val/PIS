import tkinter as tk
from controller.webServices import webServices
from model.test import test
from controller.testController import testController
from model.geographic_point import geographic_point
from tkinter import messagebox
from model.testForKnowledge import testFromDB


class Index(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Vitajte!").grid(row=0, column=0, columnspan=5, pady=5)

        tk.Button(self, text="Vytvoriť test", command=self.createTest).grid(row=1, column=0, pady=5, padx=5, sticky='E')

        tk.Button(self, text="Test", command=self.createTestForTesting).grid(row=1, column=0, pady=5, padx=5, sticky='W')

        tk.Label(self, width=50, height=15, bg="grey").grid(row=3, column=0, padx=10, pady=10)

    def createTest(self):
        self.destroy()
        webServices.setWebServices()
        app = Settings(master=self.master)

    def createTestForTesting(self):
        self.destroy()
        webServices.setWebServices()
        app = Settings2(master=self.master)


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
            message = "Prosím vyplňte nastavenia testu!"
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
        self.typeA = ''
        self.typeB = ''

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
        lat1 = self.moznostiA[int(miesto[0])].coord_lat
        lon1 = self.moznostiA[int(miesto[0])].coord_lon

        miesto2 = self.posib2.get()
        lat2 = self.moznostiB[int(miesto2[0])].coord_lat
        lon2 = self.moznostiB[int(miesto2[0])].coord_lon

        pointA = geographic_point(self.moznostiA[int(miesto[0])].name, self.typeA, self.locationAHint.get(), lat1, lon1)
        pointB = geographic_point(self.moznostiB[int(miesto2[0])].name, self.typeB, self.locationBHint.get(), lat2,
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

        if self.posib.get() == '':
            errmes = "Prosím vyhľadajte Miesto A\n"
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

        if self.posib2.get() == '':
            errmes = "Prosím vyhľadajte Miesto B\n"
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
                self.typeA = self.locationATypeString
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
                self.typeB = self.locationBTypeString
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


# todo another settings
class Settings2(tk.Frame):

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
            message = "Prosím vyplňte nastavenia testu!"
            messagebox.showerror(title="Chyba", message=message)
        else:
            print("Vrchy: " + str(self.hill.get()))
            print("Mesta: " + str(self.city.get()))

            testController.createTest(str(self.hill.get()), str(self.city.get()))
            error = webServices.getTest()
            if error == 1:
                print('nepodarilo sa ziskat testy')
                # todo Nepodarilo sa nacitat, chcete neviem co<

            elif error == 2:
                print('na z8klade nastavení nebol nájdený žiaden test zvolte ine nastavenia prosim')
                # todo Nebol najdeny ziaden test error

            self.destroy()
            app = Testquestion(master=self.master)


class Testquestion(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.answer = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):

        tk.Label(self, text="Otázka " + str(testFromDB.sucasna_otazka + 1)).grid(row=0, column=0)

        tk.Label(self, text="Určte vzdialenosti medzi miestami:").grid(columnspan=2, sticky="W", pady=10)

        tk.Label(self, text= testFromDB.questions[testFromDB.sucasna_otazka][0] + ":").grid(row=3, column=0, sticky="W")

        tk.Button(self, text="Nápoveda", command=self.show_hintA).grid(row=4, column=0, sticky='W', padx=20)

        tk.Label(self, text= testFromDB.questions[testFromDB.sucasna_otazka][2] + ":").grid(row=3, column=1, sticky="W")

        tk.Button(self, text="Nápoveda", command=self.show_hintB).grid(row=4, column=1, sticky='W', padx=20)

        tk.Entry(self, textvariable=self.answer).grid(row=6, column=0, sticky="W")

        tk.Label(self, text="metrov").grid(row=6, column=1)

        tk.Button(self, text="Potvrdiť", command=self.validation).grid(row=6, column=2, sticky='w', pady=10)

    def show_hintA(self):
        tk.Label(self, text= testFromDB.questions[testFromDB.sucasna_otazka][1]).grid(row=5, column=0, sticky="W")

    def show_hintB(self):
        tk.Label(self, text= testFromDB.questions[testFromDB.sucasna_otazka][3]).grid(row=5, column=1, sticky="W")

    def validation(self):
        error = 0
        message = ""

        if self.answer.get() == '' or self.answer.get().isnumeric() is False:
            errmes = "Prosím korektne vyplňte odpoveď\n"
            message = message + errmes

            error += 1

        if error == 0:
            print(self.answer.get())
            testFromDB.setPoints(self.answer.get())


            self.destroy()
            if testFromDB.dalsi == 1:
                app = Testquestion(master=self.master)
            else:
                #todo zobrazit stav bodov
                app = sucessTest(master=self.master)
                print('pocet ziskanych bodov je: ', testFromDB.body)
        else:
            messagebox.showerror(title="Chyba", message=message)


'''This is a frame which shows after sucesfull end of test'''


# todo
class sucessTest(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Gratulujeme!\n Získali ste:\n" + str(testFromDB.body)).grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        tk.Button(self, text="Potvrdiť", command=self.testMe).grid(row=3, column=0, padx=5, pady=5)

        tk.Label(self, width=30, height=0, bg="white").grid(row=4, column=0)

    def testMe(self):
        self.destroy()
        app = Index(master=self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = Index(master=root)
    app.mainloop()
