import tkinter as tk
from model import TeacherModel
from view import TeacherView
from controller import TeacherController

if __name__ == '__main__':
    root = tk.Tk()
    model = TeacherModel()
    view = TeacherView(root)
    controller = TeacherController(model, view)
    root.geometry('1280x960')
    root.mainloop()