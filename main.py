import tkinter as tk
from controller.webServices import webServices
from model.test import test
from controller.testController import testController
from model.geographic_point import geographic_point
from tkinter import messagebox
from model.testForKnowledge import testFromDB
from view.views import Index

root = tk.Tk()
app = Index(master=root)
app.mainloop()