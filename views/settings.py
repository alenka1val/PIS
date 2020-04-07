import tkinter as tk

class Settigs(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()


    def create_widgets(self):

        self.test = tk.Button(self, text="OK", command=self.testMe)
        self.test.pack(side="top")


    def testMe(self):
        print("Test!")


#root = tk.Tk()
#app = Settigs(master=root)
#app.mainloop()
