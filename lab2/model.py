import sqlite3
import xml.dom.minidom as minidom
import xml.sax
import uuid
from typing import List, Tuple

class TeacherModel:
    def __init__(self):
        self.conn = sqlite3.connect('teachers.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        self.data = []
        self.load_from_db()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teachers (
                id TEXT PRIMARY KEY,
                department TEXT,
                full_name TEXT,
                academic_title TEXT,
                academic_degree TEXT,
                work_experience INTEGER
            )
        ''')
        self.conn.commit()

    def load_from_db(self):
        self.cursor.execute('SELECT * FROM teachers')
        self.data = [
            {'id': row[0], 'department': row[1], 'full_name': row[2], 'academic_title': row[3], 
             'academic_degree': row[4], 'work_experience': row[5]}
            for row in self.cursor.fetchall()
        ]

    def add_teacher(self, department: str, full_name: str, academic_title: str, academic_degree: str, work_experience: int) -> None:
        teacher_id = str(uuid.uuid4())
        self.cursor.execute('INSERT INTO teachers (id, department, full_name, academic_title, academic_degree, work_experience) VALUES (?, ?, ?, ?, ?, ?)',
                          (teacher_id, department, full_name, academic_title, academic_degree, work_experience))
        self.conn.commit()
        self.data.append({
            'id': teacher_id, 'department': department, 'full_name': full_name, 
            'academic_title': academic_title, 'academic_degree': academic_degree, 
            'work_experience': work_experience
        })

    def search_teachers(self, full_name: str = None, academic_title: str = None, department: str = None, 
                       min_experience: int = None, max_experience: int = None) -> List[dict]:
        result = self.data
        if full_name:
            result = [t for t in result if full_name.lower() in t['full_name'].lower()]
        if academic_title and department:
            result = [t for t in result if t['academic_title'].lower() == academic_title.lower() and 
                     t['department'].lower() == department.lower()]
        if min_experience is not None and max_experience is not None:
            result = [t for t in result if min_experience <= t['work_experience'] <= max_experience]
        return result

    def delete_teachers(self, departments: List[str] = None, academic_degrees: List[str] = None, 
                       academic_titles: List[str] = None, work_experience: int = None) -> int:
        matches = self.data
        if departments:
            matches = [t for t in matches if t['department'] in departments]
        if academic_degrees:
            matches = [t for t in matches if t['academic_degree'] in academic_degrees]
        if academic_titles and work_experience is not None:
            matches = [t for t in matches if t['academic_title'] in academic_titles and t['work_experience'] >= work_experience]
            
        for teacher in matches:
            self.cursor.execute('DELETE FROM teachers WHERE id = ?', (teacher['id'],))
            self.data = [t for t in self.data if t['id'] != teacher['id']]
        self.conn.commit()
        return len(matches)

    def save_to_xml(self, filename: str) -> None:
        doc = minidom.Document()
        root = doc.createElement('teachers')
        doc.appendChild(root)
        
        for teacher in self.data:
            teacher_elem = doc.createElement('teacher')
            teacher_elem.setAttribute('id', teacher['id'])
            
            for key in ['department', 'full_name', 'academic_title', 'academic_degree', 'work_experience']:
                elem = doc.createElement(key)
                elem.appendChild(doc.createTextNode(str(teacher[key])))
                teacher_elem.appendChild(elem)
                
            root.appendChild(teacher_elem)
            
        with open(filename, 'w', encoding='utf-8') as f:
            doc.writexml(f, indent='  ', addindent='  ', newl='\n')

    def load_from_xml(self, filename: str) -> None:
        class TeacherHandler(xml.sax.ContentHandler):
            def __init__(self):
                self.teachers = []
                self.current_teacher = {}
                self.current_tag = ''
                
            def startElement(self, name, attrs):
                self.current_tag = name
                if name == 'teacher':
                    self.current_teacher = {'id': attrs['id']}
                    
            def characters(self, content):
                if self.current_tag in ['department', 'full_name', 'academic_title', 'academic_degree', 'work_experience']:
                    self.current_teacher[self.current_tag] = content
                    
            def endElement(self, name):
                if name == 'teacher':
                    self.current_teacher['work_experience'] = int(self.current_teacher['work_experience'])
                    self.teachers.append(self.current_teacher)
                self.current_tag = ''
                
        handler = TeacherHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(filename)
        
        self.cursor.execute('DELETE FROM teachers')
        self.data = []
        for teacher in handler.teachers:
            self.add_teacher(
                teacher['department'], teacher['full_name'], 
                teacher['academic_title'], teacher['academic_degree'], 
                teacher['work_experience']
            )