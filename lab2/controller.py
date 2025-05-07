import tkinter as tk
from tkinter import filedialog
from model import TeacherModel
from dialogs import AddDialog, SearchDialog, DeleteDialog

class TeacherController:
    def __init__(self, model: TeacherModel, view):
        self.model = model
        self.view = view
        self.current_page = 1
        self.total_pages = 1
        self.view.set_controller(self)
        self.update_view()

    def add_teacher(self, department: str, full_name: str, academic_title: str, academic_degree: str, work_experience: int):
        self.model.add_teacher(department, full_name, academic_title, academic_degree, work_experience)
        self.update_view()

    def show_add_dialog(self):
        AddDialog(self.view.root, self)

    def show_search_dialog(self):
        SearchDialog(self.view.root, self)

    def show_delete_dialog(self):
        DeleteDialog(self.view.root, self)

    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension='.xml')
        if filename:
            self.model.save_to_xml(filename)

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[('XML files', '*.xml')])
        if filename:
            self.model.load_from_xml(filename)
            self.update_view()

    def set_page(self, page: int):
        try:
            page_size = int(self.view.page_size_var.get())
        except ValueError:
            page_size = 10
            
        total = len(self.model.data)
        self.total_pages = (total + page_size - 1) // page_size
        self.current_page = max(1, min(page, self.total_pages))
        
        start = (self.current_page - 1) * page_size
        end = start + page_size
        self.update_view()

    def update_view(self):
        try:
            page_size = int(self.view.page_size_var.get())
        except ValueError:
            page_size = 10
            
        start = (self.current_page - 1) * page_size
        end = start + page_size
        teachers = self.model.data[start:end]
        
        self.view.update_table(teachers, self.current_page, page_size, len(self.model.data))
        self.view.update_tree(self.model.data)