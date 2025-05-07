import tkinter as tk
from tkinter import ttk
from typing import List

class TeacherView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Teacher Management')
        
        # Меню
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save to XML", command=lambda: self.controller.save_file())
        file_menu.add_command(label="Load from XML", command=lambda: self.controller.load_file())
        menubar.add_cascade(label="File", menu=file_menu)
        
        action_menu = tk.Menu(menubar, tearoff=0)
        action_menu.add_command(label="Add Teacher", command=lambda: self.controller.show_add_dialog())
        action_menu.add_command(label="Search Teachers", command=lambda: self.controller.show_search_dialog())
        action_menu.add_command(label="Delete Teachers", command=lambda: self.controller.show_delete_dialog())
        menubar.add_cascade(label="Actions", menu=action_menu)
        
        root.config(menu=menubar)
        
        # Панель инструментов
        toolbar = tk.Frame(root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(toolbar, text="Add", command=lambda: self.controller.show_add_dialog()).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Search", command=lambda: self.controller.show_search_dialog()).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Delete", command=lambda: self.controller.show_delete_dialog()).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Save XML", command=lambda: self.controller.save_file()).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Load XML", command=lambda: self.controller.load_file()).pack(side=tk.LEFT)
        
        # Основной фрейм
        self.main_frame = ttk.Notebook(root)
        self.main_frame.pack(expand=True, fill='both')
        
        # Таблица
        self.table_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.table_frame, text='Table View')
        
        self.table = ttk.Treeview(self.table_frame, columns=('ID', 'Department', 'Full Name', 'Academic Title', 'Academic Degree', 'Work Experience'), show='headings')
        self.table.heading('ID', text='ID')
        self.table.heading('Department', text='Department')
        self.table.heading('Full Name', text='Full Name')
        self.table.heading('Academic Title', text='Academic Title')
        self.table.heading('Academic Degree', text='Academic Degree')
        self.table.heading('Work Experience', text='Work Experience')
        self.table.pack(expand=True, fill='both')
        
        # Дерево
        self.tree_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.tree_frame, text='Tree View')
        
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.pack(expand=True, fill='both')
        
        # Пагинация
        self.pagination_frame = ttk.Frame(root)
        self.pagination_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.page_size_var = tk.StringVar(value='10')
        ttk.Entry(self.pagination_frame, textvariable=self.page_size_var, width=5).pack(side=tk.LEFT)
        ttk.Label(self.pagination_frame, text='records per page').pack(side=tk.LEFT)
        
        ttk.Button(self.pagination_frame, text='First', command=lambda: self.controller.set_page(1)).pack(side=tk.LEFT)
        ttk.Button(self.pagination_frame, text='Prev', command=lambda: self.controller.set_page(self.controller.current_page - 1)).pack(side=tk.LEFT)
        ttk.Button(self.pagination_frame, text='Next', command=lambda: self.controller.set_page(self.controller.current_page + 1)).pack(side=tk.LEFT)
        ttk.Button(self.pagination_frame, text='Last', command=lambda: self.controller.set_page(self.controller.total_pages)).pack(side=tk.LEFT)
        
        self.page_info = ttk.Label(self.pagination_frame, text='')
        self.page_info.pack(side=tk.LEFT, padx=10)
        
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def update_table(self, teachers: List[dict], page: int, page_size: int, total: int):
        for item in self.table.get_children():
            self.table.delete(item)
            
        for teacher in teachers:
            self.table.insert('', 'end', values=(
                teacher['id'], teacher['department'], teacher['full_name'], 
                teacher['academic_title'], teacher['academic_degree'], teacher['work_experience']
            ))
            
        total_pages = (total + page_size - 1) // page_size
        self.page_info.config(text=f'Page {page} of {total_pages}, Total records: {total}')

    def update_tree(self, teachers: List[dict]):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for teacher in teachers:
            teacher_node = self.tree.insert('', 'end', text=f"Teacher {teacher['id']}")
            self.tree.insert(teacher_node, 'end', text=f"Department: {teacher['department']}")
            self.tree.insert(teacher_node, 'end', text=f"Full Name: {teacher['full_name']}")
            self.tree.insert(teacher_node, 'end', text=f"Academic Title: {teacher['academic_title']}")
            self.tree.insert(teacher_node, 'end', text=f"Academic Degree: {teacher['academic_degree']}")
            self.tree.insert(teacher_node, 'end', text=f"Work Experience: {teacher['work_experience']}")