import json
import sqlite3
from models import Student, Instructor, Course

class DataManager:
    """
    Manages the database operations for the school management system.

    This class handles the creation of tables, addition and deletion of students,
    instructors, and courses, as well as backing up and loading data.

    Attributes:
        db_name (str): The name of the SQLite database file.
        conn (sqlite3.Connection): The SQLite database connection object.
        students (dict): In-memory dictionary of students, keyed by student_id.
        instructors (dict): In-memory dictionary of instructors, keyed by instructor_id.
        courses (dict): In-memory dictionary of courses, keyed by course_id.
    """

    def __init__(self, db_name='school_management.db'):
        """
        Initializes the DataManager instance.

        Connects to the SQLite database and initializes in-memory dictionaries.

        Args:
            db_name (str, optional): The database file name. Defaults to 'school_management.db'.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute('PRAGMA foreign_keys = ON;')  # Enable foreign key support
        self.create_tables()
        self.students = {}     # key: student_id, value: Student object
        self.instructors = {}  # key: instructor_id, value: Instructor object
        self.courses = {}      # key: course_id, value: Course object

    def create_tables(self):
        """
        Creates the necessary tables in the SQLite database if they do not exist.
        """
        cursor = self.conn.cursor()
        # SQL commands to create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructors (
                instructor_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                instructor_id TEXT,
                FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
                ON DELETE SET NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                student_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
                ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
                ON DELETE CASCADE
            );
        ''')
        self.conn.commit()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()

    def add_student(self, student):
        """
        Adds a student to the database and updates the in-memory dictionary.

        Args:
            student (Student): The Student object to be added.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO students (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (student.student_id, student.name, student.age, student.get_email()))
            self.conn.commit()
            self.students[student.student_id] = student
        except sqlite3.Error as e:
            print(f"An error occurred while adding student: {e}")

    def add_instructor(self, instructor):
        """
        Adds an instructor to the database and updates the in-memory dictionary.

        Args:
            instructor (Instructor): The Instructor object to be added.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO instructors (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
            ''', (instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))
            self.conn.commit()
            self.instructors[instructor.instructor_id] = instructor
        except sqlite3.Error as e:
            print(f"An error occurred while adding instructor: {e}")

    def add_course(self, course):
        """
        Adds a course to the database and updates the in-memory dictionary.

        Args:
            course (Course): The Course object to be added.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO courses (course_id, course_name, instructor_id)
                VALUES (?, ?, ?)
            ''', (course.course_id, course.course_name, course.instructor.instructor_id if course.instructor else None))
            self.conn.commit()
            self.courses[course.course_id] = course
        except sqlite3.Error as e:
            print(f"An error occurred while adding course: {e}")

    def delete_student(self, student_id):
        """
        Deletes a student from the database and removes them from in-memory dictionaries.

        Args:
            student_id (str): The ID of the student to be deleted.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM students
                WHERE student_id = ?
            ''', (student_id,))
            # The ON DELETE CASCADE in registrations table will automatically remove the student's registrations
            self.conn.commit()
            self.students.pop(student_id, None)
        except sqlite3.Error as e:
            print(f"An error occurred while deleting student: {e}")

    def delete_instructor(self, instructor_id):
        """
        Deletes an instructor from the database and updates related courses.

        Args:
            instructor_id (str): The ID of the instructor to be deleted.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM instructors
                WHERE instructor_id = ?
            ''', (instructor_id,))
            # Set instructor_id to NULL in courses where this instructor was assigned
            cursor.execute('''
                UPDATE courses
                SET instructor_id = NULL
                WHERE instructor_id = ?
            ''', (instructor_id,))
            self.conn.commit()
            self.instructors.pop(instructor_id, None)
            # Update in-memory courses
            for course in self.courses.values():
                if course.instructor and course.instructor.instructor_id == instructor_id:
                    course.instructor = None
        except sqlite3.Error as e:
            print(f"An error occurred while deleting instructor: {e}")

    def delete_course(self, course_id):
        """
        Deletes a course from the database and removes it from in-memory dictionaries.

        Args:
            course_id (str): The ID of the course to be deleted.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                DELETE FROM courses
                WHERE course_id = ?
            ''', (course_id,))
            # The ON DELETE CASCADE in registrations table will automatically remove the course's registrations
            self.conn.commit()
            self.courses.pop(course_id, None)
        except sqlite3.Error as e:
            print(f"An error occurred while deleting course: {e}")

    def backup_database(self, backup_filename):
        """
        Backs up the current database to a specified file.

        Args:
            backup_filename (str): The filename where the backup will be saved.
        """
        try:
            self.conn.execute(f"VACUUM INTO '{backup_filename}'")
        except sqlite3.Error as e:
            print(f"An error occurred during backup: {e}")

    def save_data(self, filename):
        """
        Saves the in-memory data to a JSON file.

        Args:
            filename (str): The filename where the data will be saved.
        """
        data = {
            'students': [student.to_dict() for student in self.students.values()],
            'instructors': [instructor.to_dict() for instructor in self.instructors.values()],
            'courses': [course.to_dict() for course in self.courses.values()]
        }
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"An error occurred while saving data: {e}")

    def load_data(self, filename):
        """
        Loads data from a JSON file into the in-memory dictionaries.

        Args:
            filename (str): The filename from which to load the data.
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except IOError as e:
            print(f"An error occurred while loading data: {e}")
            return

        # Load students
        self.students = {}
        for s_data in data['students']:
            student = Student.from_dict(s_data)
            self.students[student.student_id] = student
            # Add student to database if not exists
            self.add_student(student)

        # Load instructors
        self.instructors = {}
        for i_data in data['instructors']:
            instructor = Instructor.from_dict(i_data)
            self.instructors[instructor.instructor_id] = instructor
            # Add instructor to database if not exists
            self.add_instructor(instructor)

        # Load courses
        self.courses = {}
        for c_data in data['courses']:
            instructor_id = c_data['instructor_id']
            instructor = self.instructors.get(instructor_id) if instructor_id else None
            course = Course.from_dict(c_data)
            course.set_instructor(instructor)
            self.courses[course.course_id] = course
            # Add course to database if not exists
            self.add_course(course)

        # Enroll students in courses
        for c_data in data['courses']:
            course_id = c_data['course_id']
            student_ids = c_data.get('enrolled_students', [])
            course = self.courses.get(course_id)
            if course:
                for student_id in student_ids:
                    student = self.students.get(student_id)
                    if student:
                        course.add_student(student)
                        self.register_student_in_course(student_id, course_id)
