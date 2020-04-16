import tkinter as tk

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


root = tk.Tk()
app = sucessDialog(master=root)
app.mainloop()