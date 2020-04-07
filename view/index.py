import tkinter as tk
from view.settinngs import Settings


class Index(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        # root.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Vitajte!").grid(row=0, column=0, columnspan=5, pady=5)

        tk.Button(self, text="Vytvoriť test", command=self.createTest).grid(row=1, column=0, pady=5, padx=5, sticky='E')

        tk.Label(self, width=50, height=15, bg="grey").grid(row=3, column=0,  padx=10, pady=10)

    def createTest(self):
        self.destroy()
        app = Settings(master=self.master)


root = tk.Tk()
app = Index(master=root)
app.mainloop()
