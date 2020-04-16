import tkinter as tk

class nextQuestionDialog(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Prajete si zadať ďalšiu otázku?").grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        tk.Button(self, text="Áno", command=self.testMe).grid(row=3, column=0, padx=40, pady=5, sticky='E')
        tk.Button(self, text="Nie", command=self.testMe).grid(row=3, column=0, padx=40, pady=5, sticky='W')

        tk.Label(self, width=30, height=0, bg="white").grid(row=4, column=0)


    def testMe(self):
        self.destroy()


root = tk.Tk()
app = nextQuestionDialog(master=root)
app.mainloop()
