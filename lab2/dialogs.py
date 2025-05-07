import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

class AddDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title('Add Teacher')
        self.geometry('300x300')
        
        ttk.Label(self, text='Department:').pack()
        self.department_entry = ttk.Entry(self)
        self.department_entry.pack()
        
        ttk.Label(self, text='Full Name:').pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()
        
        ttk.Label(self, text='Academic Title:').pack()
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack()
        
        ttk.Label(self, text='Academic Degree:').pack()
        self.degree_entry = ttk.Entry(self)
        self.degree_entry.pack()
        
        ttk.Label(self, text='Work Experience (years):').pack()
        self.experience_entry = ttk.Entry(self)
        self.experience_entry.pack()
        
        ttk.Button(self, text='Add', command=self.add_teacher).pack(pady=10)
        
    def add_teacher(self):
        try:
            department = self.department_entry.get()
            full_name = self.name_entry.get()
            academic_title = self.title_entry.get()
            academic_degree = self.degree_entry.get()
            work_experience = int(self.experience_entry.get())
            
            if not all([department, full_name, academic_title, academic_degree]):
                messagebox.showerror('Error', 'All fields except experience must be filled')
                return
            if work_experience < 0:
                messagebox.showerror('Error', 'Work Experience cannot be negative')
                return
                
            self.controller.add_teacher(department, full_name, academic_title, academic_degree, work_experience)
            self.destroy()
        except ValueError:
            messagebox.showerror('Error', 'Invalid Work Experience')

class SearchDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title('Search Teachers')
        self.geometry('500x400')
        
        ttk.Label(self, text='Full Name contains:').pack()
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()
        
        ttk.Label(self, text='Academic Title:').pack()
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack()
        
        ttk.Label(self, text='Department:').pack()
        self.department_entry = ttk.Entry(self)
        self.department_entry.pack()
        
        ttk.Label(self, text='Work Experience (min):').pack()
        self.min_exp_entry = ttk.Entry(self)
        self.min_exp_entry.pack()
        
        ttk.Label(self, text='Work Experience (max):').pack()
        self.max_exp_entry = ttk.Entry(self)
        self.max_exp_entry.pack()
        
        ttk.Button(self, text='Search', command=self.search).pack(pady=10)
        
        self.result_table = ttk.Treeview(self, columns=('ID', 'Department', 'Full Name', 'Academic Title', 'Academic Degree', 'Work Experience'), show='headings')
        self.result_table.heading('ID', text='ID')
        self.result_table.heading('Department', text='Department')
        self.result_table.heading('Full Name', text='Full Name')
        self.result_table.heading('Academic Title', text='Academic Title')
        self.result_table.heading('Academic Degree', text='Academic Degree')
        self.result_table.heading('Work Experience', text='Work Experience')
        self.result_table.pack(expand=True, fill='both')

    def search(self):
        full_name = self.name_entry.get() or None
        academic_title = self.title_entry.get() or None
        department = self.department_entry.get() or None
        try:
            min_exp = int(self.min_exp_entry.get()) if self.min_exp_entry.get() else None
            max_exp = int(self.max_exp_entry.get()) if self.max_exp_entry.get() else None
        except ValueError:
            min_exp, max_exp = None, None
            
        results = self.controller.model.search_teachers(
            full_name=full_name, academic_title=academic_title, department=department,
            min_experience=min_exp, max_experience=max_exp
        )
        
        for item in self.result_table.get_children():
            self.result_table.delete(item)
            
        for teacher in results:
            self.result_table.insert('', 'end', values=(
                teacher['id'], teacher['department'], teacher['full_name'], 
                teacher['academic_title'], teacher['academic_degree'], teacher['work_experience']
            ))

class DeleteDialog(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title('Delete Teachers')
        self.geometry('400x400')
        
        ttk.Label(self, text='Departments (comma-separated):').pack()
        self.departments_entry = ttk.Entry(self)
        self.departments_entry.pack()
        
        ttk.Label(self, text='Academic Degrees (comma-separated):').pack()
        self.degrees_entry = ttk.Entry(self)
        self.degrees_entry.pack()
        
        ttk.Label(self, text='Academic Titles (comma-separated):').pack()
        self.titles_entry = ttk.Entry(self)
        self.titles_entry.pack()
        
        ttk.Label(self, text='Minimum Work Experience:').pack()
        self.experience_entry = ttk.Entry(self)
        self.experience_entry.pack()
        
        ttk.Button(self, text='Delete', command=self.delete).pack(pady=10)
        
        self.result_list = tk.Listbox(self, height=5)
        self.result_list.pack(expand=True, fill='both')

    def delete(self):
        departments = [d.strip() for d in self.departments_entry.get().split(',') if d.strip()] or None
        degrees = [d.strip() for d in self.degrees_entry.get().split(',') if d.strip()] or None
        titles = [t.strip() for t in self.titles_entry.get().split(',') if t.strip()] or None
        try:
            experience = int(self.experience_entry.get()) if self.experience_entry.get() else None
        except ValueError:
            experience = None
            
        count = self.controller.model.delete_teachers(
            departments=departments, academic_degrees=degrees,
            academic_titles=titles, work_experience=experience
        )
        
        self.result_list.delete(0, tk.END)
        self.result_list.insert(tk.END, f'Deleted {count} records')
        self.controller.update_view()
