import unittest
import sqlite3
import os
from model import TeacherModel
from controller import TeacherController
from view import TeacherView
import tkinter as tk
from dialogs import AddDialog, SearchDialog, DeleteDialog

class TestTeacherApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.model = TeacherModel()
        self.view = TeacherView(self.root)
        self.controller = TeacherController(self.model, self.view)
        # Очистка базы данных перед каждым тестом
        self.model.cursor.execute('DELETE FROM teachers')
        self.model.conn.commit()
        self.model.data = []

    def tearDown(self):
        self.root.destroy()
        # Удаление базы данных после тестов
        if os.path.exists('teachers.db'):
            os.remove('teachers.db')

    def test_add_teacher(self):
        self.controller.add_teacher("Computer Science", "Test User", "Professor", "PhD", 10)
        self.assertEqual(len(self.model.data), 1)
        self.assertEqual(self.model.data[0]['full_name'], "Test User")

    def test_add_teacher_invalid_experience(self):
        dialog = AddDialog(self.root, self.controller)
        dialog.department_entry.insert(0, "Computer Science")
        dialog.name_entry.insert(0, "Test User")
        dialog.title_entry.insert(0, "Professor")
        dialog.degree_entry.insert(0, "PhD")
        dialog.experience_entry.insert(0, "6")
        dialog.add_teacher()
        self.assertEqual(len(self.model.data), 0)  # Не добавлено из-за ошибки

    def test_search_teachers(self):
        self.controller.add_teacher("Math", "John Doe", "Associate Professor", "PhD", 15)
        self.controller.add_teacher("Physics", "Jane Doe", "Professor", "Doctor of Sciences", 20)
        results = self.model.search_teachers(full_name="John", min_experience=10, max_experience=20)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['full_name'], "John Doe")

    def test_search_teachers_title_department(self):
        self.controller.add_teacher("Math", "John Doe", "Associate Professor", "PhD", 15)
        self.controller.add_teacher("Math", "Jane Doe", "Professor", "Doctor of Sciences", 20)
        results = self.model.search_teachers(academic_title="Associate Professor", department="Math")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['academic_title'], "Associate Professor")

    def test_delete_teachers(self):
        self.controller.add_teacher("Math", "John Doe", "Associate Professor", "PhD", 15)
        self.controller.add_teacher("Physics", "Jane Doe", "Professor", "PhD", 20)
        count = self.model.delete_teachers(departments=["Math"], academic_titles=["Associate Professor"])
        self.assertEqual(count, 1)
        self.assertEqual(len(self.model.data), 1)
        self.assertEqual(self.model.data[0]['full_name'], "Jane Doe")

    def test_save_and_load_xml(self):
        self.controller.add_teacher("Computer Science", "Test User", "Professor", "PhD", 10)
        filename = "test_output.xml"
        self.model.save_to_xml(filename)
        self.model.data = []
        self.model.load_from_xml(filename)
        self.assertEqual(len(self.model.data), 1)
        self.assertEqual(self.model.data[0]['full_name'], "Test User")
        if os.path.exists(filename):
            os.remove(filename)

    def test_pagination(self):
        for i in range(15):
            self.controller.add_teacher(f"Dept{i}", f"User{i}", "Professor", "PhD", i)
        self.controller.set_page(2)
        self.assertEqual(self.controller.current_page, 2)
        page_size = int(self.view.page_size_var.get())
        start = (self.controller.current_page - 1) * page_size
        end = start + page_size
        self.assertEqual(len(self.model.data[start:end]), min(page_size, len(self.model.data) - start))

    def test_search_dialog(self):
        self.controller.add_teacher("Math", "John Doe", "Associate Professor", "PhD", 15)
        dialog = SearchDialog(self.root, self.controller)
        dialog.name_entry.insert(0, "John")
        dialog.search()
        self.assertEqual(len(dialog.result_table.get_children()), 1)

    def test_delete_dialog(self):
        self.controller.add_teacher("Math", "John Doe", "Associate Professor", "PhD", 15)
        dialog = DeleteDialog(self.root, self.controller)
        dialog.departments_entry.insert(0, "Math")
        dialog.titles_entry.insert(0, "Associate Professor")
        dialog.delete()
        self.assertEqual(len(self.model.data), 0)
        self.assertEqual(dialog.result_list.get(0), "Deleted 1 records")

if __name__ == '__main__':
    unittest.main()
