import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QHBoxLayout, QHeaderView, QMessageBox, QTabWidget, QFileDialog, QComboBox)

from models_PyQt import student, instructor, course 

def create_db():
    """
    Create the necessary tables in the SQLite database.

    This function creates the `students`, `instructors`, `courses`, `student_courses`, 
    and `instructor_courses` tables if they don't already exist.

    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, email TEXT, student_id TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS instructors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, email TEXT, instructor_id TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, course_name TEXT, course_id TEXT, instructor_id INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS student_courses (student_id INTEGER, course_id INTEGER, FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(course_id) REFERENCES courses(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS instructor_courses (instructor_id INTEGER, course_id INTEGER, FOREIGN KEY(instructor_id) REFERENCES instructors(id), FOREIGN KEY(course_id) REFERENCES courses(id))''')
    conn.commit()
    conn.close()

def add_student_db(student_obj):
    """
    Add a student to the database.

    :param student_obj: The student object containing the student's details.
    :type student_obj: student
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO students (name, age, email, student_id) VALUES (?, ?, ?, ?)''', 
                   (student_obj.name, student_obj.age, student_obj._email, student_obj.student_id))
    conn.commit()
    conn.close()

def update_student_db(student_obj, id):
    """
    Update a student's information in the database.

    :param student_obj: The student object with updated information.
    :type student_obj: student
    :param id: The ID of the student in the database.
    :type id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE students SET name=?, age=?, email=?, student_id=? WHERE id=?''', 
                   (student_obj.name, student_obj.age, student_obj._email, student_obj.student_id, id))
    conn.commit()
    conn.close()

def get_students_db():
    """
    Retrieve all students from the database.

    :return: A list of student objects from the database.
    :rtype: list[student]
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students_data = cursor.fetchall()
    conn.close()
    student_objects = [student(name=row[1], age=row[2], _email=row[3], student_id=row[4], registered_courses=[]) for row in students_data]
    return student_objects

def delete_student_db(id):
    """
    Delete a student from the database.

    :param id: The ID of the student to delete.
    :type id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

def add_instructor_db(instructor_obj):
    """
    Add an instructor to the database.

    :param instructor_obj: The instructor object containing the instructor's details.
    :type instructor_obj: instructor
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO instructors (name, age, email, instructor_id) VALUES (?, ?, ?, ?)''', 
                   (instructor_obj.name, instructor_obj.age, instructor_obj._email, instructor_obj.instructor_id))
    conn.commit()
    conn.close()

def update_instructor_db(instructor_obj, id):
    """
    Update an instructor's information in the database.

    :param instructor_obj: The instructor object with updated information.
    :type instructor_obj: instructor
    :param id: The ID of the instructor in the database.
    :type id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE instructors SET name=?, age=?, email=?, instructor_id=? WHERE id=?''', 
                   (instructor_obj.name, instructor_obj.age, instructor_obj._email, instructor_obj.instructor_id, id))
    conn.commit()
    conn.close()

def get_instructors_db():
    """
    Retrieve all instructors from the database.

    :return: A list of instructor objects from the database.
    :rtype: list[instructor]
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM instructors")
    instructors_data = cursor.fetchall()
    conn.close()
    instructor_objects = [instructor(name=row[1], age=row[2], _email=row[3], instructor_id=row[4], assigned_courses=[]) for row in instructors_data]
    return instructor_objects

def delete_instructor_db(id):
    """
    Delete an instructor from the database.

    :param id: The ID of the instructor to delete.
    :type id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM instructors WHERE id=?", (id,))
    conn.commit()
    conn.close()

def add_course_db(course_obj):
    """
    Add a course to the database.

    :param course_obj: The course object containing the course details.
    :type course_obj: course
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO courses (course_name, course_id, instructor_id) VALUES (?, ?, ?)''', 
                   (course_obj.course_name, course_obj.course_id, course_obj.instructor.instructor_id if course_obj.instructor else None))
    conn.commit()
    conn.close()

def update_course_db(course_obj, id):
    """
    Update a course's information in the database.

    :param course_obj: The course object with updated information.
    :type course_obj: course
    :param id: The ID of the course in the database.
    :type id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE courses SET course_name=?, course_id=?, instructor_id=? WHERE id=?''', 
                   (course_obj.course_name, course_obj.course_id, course_obj.instructor.instructor_id if course_obj.instructor else None, id))
    conn.commit()
    conn.close()

def get_courses_db():
    """
    Retrieve all courses from the database.

    :return: A list of course objects from the database.
    :rtype: list[course]
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT courses.id, courses.course_name, courses.course_id, instructors.instructor_id, instructors.name
        FROM courses
        LEFT JOIN instructors ON courses.instructor_id = instructors.id
    ''')
    courses_data = cursor.fetchall()
    conn.close()
    
    course_objects = []
    for row in courses_data:
        if row[3] is not None: 
            instructor_obj = instructor(name=row[4], age=None, _email=None, instructor_id=row[3], assigned_courses=[])
        else:
            instructor_obj = None  
        course_obj = course(course_name=row[1], course_id=row[2], instructor=instructor_obj, enrolled_students=[])
        course_objects.append(course_obj)
    
    return course_objects

def delete_course_db(id):
    """
    Delete a course from the database.

    :param id: The ID of the course to delete.
    :type id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    conn.close()

def add_course_to_student(student_id, course_id):
    """
    Assign a course to a student.

    :param student_id: The ID of the student.
    :type student_id: int
    :param course_id: The ID of the course to assign.
    :type course_id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
    conn.commit()
    conn.close()

def add_course_to_instructor(instructor_id, course_id):
    """
    Assign a course to an instructor.

    :param instructor_id: The ID of the instructor.
    :type instructor_id: int
    :param course_id: The ID of the course to assign.
    :type course_id: int
    :return: None
    """
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO instructor_courses (instructor_id, course_id) VALUES (?, ?)", (instructor_id, course_id))
    conn.commit()
    conn.close()

def backup_database():
    """
    Create a backup of the current database.

    :return: None
    """
    file_name, _ = QFileDialog.getSaveFileName(None, "Backup Database", "", "SQLite Files (*.db)")
    if file_name:
        conn = sqlite3.connect('school.db')
        backup_conn = sqlite3.connect(file_name)
        conn.backup(backup_conn)
        backup_conn.close()
        conn.close()
        QMessageBox.information(None, "Backup", "Database backup completed successfully!")

class SchoolManagementSystem(QMainWindow):
    """
    Main window for the School Management System.

    This class manages the overall layout and functionality of the application, including
    tabs for managing students, instructors, and courses.
    """
    def __init__(self):
        """
        Initialize the SchoolManagementSystem window and set up the GUI.
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 900, 600)
        create_db()
        self.initialize_gui()

    def initialize_gui(self):
        """
        Set up the main GUI layout, including tabs for students, instructors, and courses.
        """
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_course_tab()
        self.create_backup_button()
    def create_student_tab(self):
        """
        Create the tab for managing students in the GUI.

        This includes the form for adding, editing, and deleting students,
        as well as the table for displaying all students.

        :return: None
        """
        student_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()
        self.student_id_input = QLineEdit()
        form_layout.addRow(QLabel("Name:"), self.student_name_input)
        form_layout.addRow(QLabel("Age:"), self.student_age_input)
        form_layout.addRow(QLabel("Email:"), self.student_email_input)
        form_layout.addRow(QLabel("Student ID:"), self.student_id_input)

        self.student_course_dropdown = QComboBox()
        courses = get_courses_db()
        self.student_course_dropdown.addItems([course_obj.course_name for course_obj in courses])
        form_layout.addRow(QLabel("Assign Course:"), self.student_course_dropdown)

        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        
        self.assign_course_button = QPushButton("Assign Course to Student")
        self.assign_course_button.clicked.connect(self.assign_course_to_student)

        self.edit_student_button = QPushButton("Edit Student")
        self.edit_student_button.clicked.connect(self.edit_student)

        self.delete_student_button = QPushButton("Delete Student")
        self.delete_student_button.clicked.connect(self.delete_student)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_student_button)
        button_layout.addWidget(self.edit_student_button)
        button_layout.addWidget(self.delete_student_button)
        button_layout.addWidget(self.assign_course_button)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email", "Student ID"])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.student_table)

        student_tab.setLayout(layout)
        self.tabs.addTab(student_tab, "Students")
        self.refresh_student_table()

    def create_instructor_tab(self):
        """
        Create the tab for managing instructors in the GUI.

        This includes the form for adding, editing, and deleting instructors,
        as well as the table for displaying all instructors.

        :return: None
        """
        instructor_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.instructor_name_input = QLineEdit()
        self.instructor_age_input = QLineEdit()
        self.instructor_email_input = QLineEdit()
        self.instructor_id_input = QLineEdit()
        form_layout.addRow(QLabel("Name:"), self.instructor_name_input)
        form_layout.addRow(QLabel("Age:"), self.instructor_age_input)
        form_layout.addRow(QLabel("Email:"), self.instructor_email_input)
        form_layout.addRow(QLabel("Instructor ID:"), self.instructor_id_input)

        self.instructor_course_dropdown = QComboBox()
        courses = get_courses_db()
        self.instructor_course_dropdown.addItems([course_obj.course_name for course_obj in courses])
        form_layout.addRow(QLabel("Assign Course:"), self.instructor_course_dropdown)

        self.add_instructor_button = QPushButton("Add Instructor")
        self.add_instructor_button.clicked.connect(self.add_instructor)
        
        self.assign_course_instructor_button = QPushButton("Assign Course to Instructor")
        self.assign_course_instructor_button.clicked.connect(self.assign_course_to_instructor)

        self.edit_instructor_button = QPushButton("Edit Instructor")
        self.edit_instructor_button.clicked.connect(self.edit_instructor)

        self.delete_instructor_button = QPushButton("Delete Instructor")
        self.delete_instructor_button.clicked.connect(self.delete_instructor)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_instructor_button)
        button_layout.addWidget(self.edit_instructor_button)
        button_layout.addWidget(self.delete_instructor_button)
        button_layout.addWidget(self.assign_course_instructor_button)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.instructor_table = QTableWidget()
        self.instructor_table.setColumnCount(5)
        self.instructor_table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Email", "Instructor ID"])
        self.instructor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.instructor_table)

        instructor_tab.setLayout(layout)
        self.tabs.addTab(instructor_tab, "Instructors")
        self.refresh_instructor_table()

    def create_course_tab(self):
        """
        Create the tab for managing courses in the GUI.

        This includes the form for adding, editing, and deleting courses,
        as well as the table for displaying all courses.

        :return: None
        """
        course_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.course_name_input = QLineEdit()
        self.course_id_input = QLineEdit()
        self.instructor_dropdown = QComboBox()

        instructors = get_instructors_db()
        if instructors:
            self.instructor_dropdown.addItems([f"{inst.name} (ID: {inst.instructor_id})" for inst in instructors])
        else:
            self.instructor_dropdown.addItem("No Instructors Available")

        form_layout.addRow(QLabel("Course Name:"), self.course_name_input)
        form_layout.addRow(QLabel("Course ID:"), self.course_id_input)
        form_layout.addRow(QLabel("Instructor:"), self.instructor_dropdown)

        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)

        self.edit_course_button = QPushButton("Edit Course")
        self.edit_course_button.clicked.connect(self.edit_course)

        self.delete_course_button = QPushButton("Delete Course")
        self.delete_course_button.clicked.connect(self.delete_course)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_course_button)
        button_layout.addWidget(self.edit_course_button)
        button_layout.addWidget(self.delete_course_button)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.course_table = QTableWidget()
        self.course_table.setColumnCount(3)
        self.course_table.setHorizontalHeaderLabels(["Course Name", "Course ID", "Instructor ID"])
        self.course_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.course_table)

        course_tab.setLayout(layout)
        self.tabs.addTab(course_tab, "Courses")
        self.refresh_course_table()

    def refresh_student_table(self):
        """
        Refresh the student table with the latest data from the database.

        :return: None
        """
        students = get_students_db()
        self.student_table.setRowCount(0)
        for row, student_obj in enumerate(students):
            self.student_table.insertRow(row)
            self.student_table.setItem(row, 0, QTableWidgetItem(str(row+1)))  
            self.student_table.setItem(row, 1, QTableWidgetItem(student_obj.name))
            self.student_table.setItem(row, 2, QTableWidgetItem(str(student_obj.age)))
            self.student_table.setItem(row, 3, QTableWidgetItem(student_obj._email))
            self.student_table.setItem(row, 4, QTableWidgetItem(student_obj.student_id))

    def refresh_instructor_table(self):
        """
        Refresh the instructor table with the latest data from the database.

        :return: None
        """
        instructors = get_instructors_db()
        self.instructor_table.setRowCount(0)
        for row, instructor_obj in enumerate(instructors):
            self.instructor_table.insertRow(row)
            self.instructor_table.setItem(row, 0, QTableWidgetItem(str(row+1))) 
            self.instructor_table.setItem(row, 1, QTableWidgetItem(instructor_obj.name))
            self.instructor_table.setItem(row, 2, QTableWidgetItem(str(instructor_obj.age)))
            self.instructor_table.setItem(row, 3, QTableWidgetItem(instructor_obj._email))
            self.instructor_table.setItem(row, 4, QTableWidgetItem(instructor_obj.instructor_id))

    def refresh_course_table(self):
        """
        Refresh the course table with the latest data from the database.

        :return: None
        """
        courses = get_courses_db()
        self.course_table.setRowCount(0)
        for row, course_obj in enumerate(courses):
            self.course_table.insertRow(row)
            self.course_table.setItem(row, 0, QTableWidgetItem(course_obj.course_name))
            self.course_table.setItem(row, 1, QTableWidgetItem(course_obj.course_id))
            if course_obj.instructor is not None:
                self.course_table.setItem(row, 2, QTableWidgetItem(course_obj.instructor.instructor_id))
            else:
                self.course_table.setItem(row, 2, QTableWidgetItem("No Instructor"))

    def add_student(self):
        """
        Add a new student to the database based on the input fields in the GUI.

        :return: None
        """
        try:
            name = self.student_name_input.text()
            age = int(self.student_age_input.text())
            email = self.student_email_input.text()
            student_id = self.student_id_input.text()

            new_student = student(name=name, age=age, _email=email, student_id=student_id, registered_courses=[])
            add_student_db(new_student)
            self.refresh_student_table()

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

    def edit_student(self):
        """
        Edit the selected student's information in the database based on the input fields.

        :return: None
        """
        selected_row = self.student_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a student to edit.")
            return

        id = selected_row + 1
        name = self.student_name_input.text()
        age = int(self.student_age_input.text())
        email = self.student_email_input.text()
        student_id = self.student_id_input.text()

        updated_student = student(name=name, age=age, _email=email, student_id=student_id)
        update_student_db(updated_student, id)
        self.refresh_student_table()

    def delete_student(self):
        """
        Delete the selected student from the database.

        :return: None
        """
        selected_row = self.student_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a student to delete.")
            return

        id = selected_row + 1
        delete_student_db(id)
        self.refresh_student_table()

    def assign_course_to_student(self):
        """
        Assign a course to the selected student.

        :return: None
        """
        selected_row = self.student_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a student to assign a course.")
            return

        student_id = selected_row + 1
        course_name = self.student_course_dropdown.currentText()
        courses = get_courses_db()
        course_id = [course_obj.course_id for course_obj in courses if course_obj.course_name == course_name][0]

        add_course_to_student(student_id, course_id)
        QMessageBox.information(self, "Success", f"Assigned {course_name} to the student.")
        self.refresh_student_table()

    def add_instructor(self):
        """
        Add a new instructor to the database based on the input fields in the GUI.

        :return: None
        """
        try:
            name = self.instructor_name_input.text()
            age = int(self.instructor_age_input.text())
            email = self.instructor_email_input.text()
            instructor_id = self.instructor_id_input.text()

            new_instructor = instructor(name=name, age=age, _email=email, instructor_id=instructor_id, assigned_courses=[])
            add_instructor_db(new_instructor)
            self.refresh_instructor_table()

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

    def edit_instructor(self):
        """
        Edit the selected instructor's information in the database based on the input fields.

        :return: None
        """
        selected_row = self.instructor_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an instructor to edit.")
            return

        id = selected_row + 1
        name = self.instructor_name_input.text()
        age = int(self.instructor_age_input.text())
        email = self.instructor_email_input.text()
        instructor_id = self.instructor_id_input.text()

        updated_instructor = instructor(name=name, age=age, _email=email, instructor_id=instructor_id)
        update_instructor_db(updated_instructor, id)
        self.refresh_instructor_table()

    def delete_instructor(self):
        """
        Delete the selected instructor from the database.

        :return: None
        """
        selected_row = self.instructor_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an instructor to delete.")
            return

        id = selected_row + 1
        delete_instructor_db(id)
        self.refresh_instructor_table()

    def assign_course_to_instructor(self):
        """
        Assign a course to the selected instructor.

        :return: None
        """
        selected_row = self.instructor_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an instructor to assign a course.")
            return

        instructor_id = selected_row + 1
        course_name = self.instructor_course_dropdown.currentText()
        courses = get_courses_db()
        course_id = [course_obj.course_id for course_obj in courses if course_obj.course_name == course_name][0]

        add_course_to_instructor(instructor_id, course_id)
        QMessageBox.information(self, "Success", f"Assigned {course_name} to the instructor.")
        self.refresh_instructor_table()

    def add_course(self):
        """
        Add a new course to the database based on the input fields in the GUI.

        :return: None
        """
        try:
            course_name = self.course_name_input.text()
            course_id = self.course_id_input.text()

            selected_instructor = self.instructor_dropdown.currentText()
            if "No Instructors Available" in selected_instructor:
                instructor_obj = None
            else:
                instructor_id = selected_instructor.split("ID: ")[1][:-1]
                instructors = get_instructors_db()
                instructor_obj = next(inst for inst in instructors if inst.instructor_id == instructor_id)

            new_course = course(course_name=course_name, course_id=course_id, instructor=instructor_obj, enrolled_students=[])
            add_course_db(new_course)
            self.refresh_course_table()

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

    def edit_course(self):
        """
        Edit the selected course's information in the database based on the input fields.

        :return: None
        """
        selected_row = self.course_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a course to edit.")
            return

        try:
            id = selected_row + 1
            course_name = self.course_name_input.text()
            course_id = self.course_id_input.text()

            selected_instructor = self.instructor_dropdown.currentText()
            if "No Instructors Available" in selected_instructor:
                instructor_obj = None
            else:
                instructor_id = selected_instructor.split("ID: ")[1][:-1]
                instructors = get_instructors_db()
                instructor_obj = next(inst for inst in instructors if inst.instructor_id == instructor_id)

            updated_course = course(course_name=course_name, course_id=course_id, instructor=instructor_obj, enrolled_students=[])
            update_course_db(updated_course, id)
            self.refresh_course_table()

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

    def delete_course(self):
        """
        Delete the selected course from the database.

        :return: None
        """
        selected_row = self.course_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a course to delete.")
            return

        id = selected_row + 1
        delete_course_db(id)
        self.refresh_course_table()

    def create_backup_button(self):
        """
        Create the backup button in the main window.

        This button allows the user to back up the current database.

        :return: None
        """
        backup_button = QPushButton("Backup Database")
        backup_button.clicked.connect(backup_database)
        self.main_layout.addWidget(backup_button)

def main():
    """
    The main entry point for the PyQt5 application.

    It creates and shows the main window of the School Management System.

    :return: None
    """
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

