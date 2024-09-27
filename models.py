import re

class Person:
    """
    Represents a generic person with a name, age, and email.

    Attributes:
        name (str): The person's name.
        age (int): The person's age.
        _email (str): The person's email address (private attribute).
    """

    def __init__(self, name, age, email):
        """
        Initializes a new instance of the Person class.

        Args:
            name (str): The name of the person.
            age (int): The age of the person. Must be non-negative.
            email (str): The email address of the person.

        Raises:
            ValueError: If the age is negative or the email format is invalid.
        """
        self.name = name
        if age >= 0:
            self.age = age
        else:
            raise ValueError("Age cannot be negative")
        if self.validate_email(email):
            self._email = email  # Private attribute
        else:
            raise ValueError("Invalid email format")

    def introduce(self):
        """
        Prints an introduction message including the person's name and age.
        """
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def get_email(self):
        """
        Retrieves the person's email address.

        Returns:
            str: The email address.
        """
        return self._email

    def set_email(self, email):
        """
        Updates the person's email address after validating the format.

        Args:
            email (str): The new email address to set.

        Raises:
            ValueError: If the email format is invalid.
        """
        if self.validate_email(email):
            self._email = email
        else:
            raise ValueError("Invalid email format")

    @staticmethod
    def validate_email(email):
        """
        Validates the format of an email address using a regular expression.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email format is valid, False otherwise.
        """
        pattern = r'^\S+@\S+\.\S+$'
        return re.match(pattern, email) is not None

    def to_dict(self):
        """
        Converts the Person object into a dictionary.

        Returns:
            dict: A dictionary representation of the Person.
        """
        return {
            'name': self.name,
            'age': self.age,
            '_email': self._email
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Person instance from a dictionary.

        Args:
            data (dict): A dictionary containing 'name', 'age', and '_email' keys.

        Returns:
            Person: An instance of the Person class.
        """
        return cls(data['name'], data['age'], data['_email'])


class Student(Person):
    """
    Represents a student, inheriting from Person.

    Attributes:
        student_id (str): The unique identifier for the student.
        registered_courses (list): A list of Course objects the student is registered in.
    """

    def __init__(self, name, age, email, student_id):
        """
        Initializes a new instance of the Student class.

        Args:
            name (str): The student's name.
            age (int): The student's age.
            email (str): The student's email address.
            student_id (str): The unique identifier for the student.
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []  # List of Course objects

    def register_course(self, course):
        """
        Registers the student in a course.

        Args:
            course (Course): The course to register the student in.
        """
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            course.add_student(self)

    def unregister_course(self, course):
        """
        Unregisters the student from a course.

        Args:
            course (Course): The course to unregister the student from.
        """
        if course in self.registered_courses:
            self.registered_courses.remove(course)
            course.enrolled_students.remove(self)

    def to_dict(self):
        """
        Converts the Student object into a dictionary.

        Returns:
            dict: A dictionary representation of the Student.
        """
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Student instance from a dictionary.

        Args:
            data (dict): A dictionary containing student data.

        Returns:
            Student: An instance of the Student class.
        """
        student = cls(data['name'], data['age'], data['_email'], data['student_id'])
        return student


class Instructor(Person):
    """
    Represents an instructor, inheriting from Person.

    Attributes:
        instructor_id (str): The unique identifier for the instructor.
        assigned_courses (list): A list of Course objects the instructor is assigned to.
    """

    def __init__(self, name, age, email, instructor_id):
        """
        Initializes a new instance of the Instructor class.

        Args:
            name (str): The instructor's name.
            age (int): The instructor's age.
            email (str): The instructor's email address.
            instructor_id (str): The unique identifier for the instructor.
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []  # List of Course objects

    def assign_course(self, course):
        """
        Assigns a course to the instructor.

        Args:
            course (Course): The course to assign.
        """
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            course.set_instructor(self)

    def unassign_course(self, course):
        """
        Unassigns a course from the instructor.

        Args:
            course (Course): The course to unassign.
        """
        if course in self.assigned_courses:
            self.assigned_courses.remove(course)
            course.instructor = None

    def to_dict(self):
        """
        Converts the Instructor object into a dictionary.

        Returns:
            dict: A dictionary representation of the Instructor.
        """
        data = super().to_dict()
        data.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        })
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates an Instructor instance from a dictionary.

        Args:
            data (dict): A dictionary containing instructor data.

        Returns:
            Instructor: An instance of the Instructor class.
        """
        instructor = cls(data['name'], data['age'], data['_email'], data['instructor_id'])
        return instructor


class Course:
    """
    Represents a course with students and an instructor.

    Attributes:
        course_id (str): The unique identifier for the course.
        course_name (str): The name of the course.
        instructor (Instructor): The instructor assigned to the course.
        enrolled_students (list): A list of Student objects enrolled in the course.
    """

    def __init__(self, course_id, course_name, instructor=None):
        """
        Initializes a new instance of the Course class.

        Args:
            course_id (str): The unique identifier for the course.
            course_name (str): The name of the course.
            instructor (Instructor, optional): The instructor assigned to the course. Defaults to None.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []  # List of Student objects

    def add_student(self, student):
        """
        Enrolls a student in the course.

        Args:
            student (Student): The student to add to the course.
        """
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            if self not in student.registered_courses:
                student.register_course(self)

    def set_instructor(self, instructor):
        """
        Assigns an instructor to the course.

        Args:
            instructor (Instructor): The instructor to assign.
        """
        self.instructor = instructor
        if self not in instructor.assigned_courses:
            instructor.assign_course(self)

    def to_dict(self):
        """
        Converts the Course object into a dictionary.

        Returns:
            dict: A dictionary representation of the Course.
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor.instructor_id if self.instructor else None,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Course instance from a dictionary.

        Args:
            data (dict): A dictionary containing course data.

        Returns:
            Course: An instance of the Course class.
        """
        course = cls(data['course_id'], data['course_name'])
        return course
