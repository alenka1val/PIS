import tkinter as tk
from views.settings import Settigs


class Index(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        root.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        self.test = tk.Button(self, text="Test", command=self.testMe)
        self.test.pack(side="top")

    def testMe(self):
        self.destroy()
        app = Settigs(master=root)


root = tk.Tk()
app = Index(master=root)
app.mainloop()
