import json
import re

class person():
    """
    A base class representing a person with a name, age, and email.
    """

    def __init__(self, name, age, _email):
        """
        Initialize a person with their name, age, and email.
        
        :param name: The name of the person.
        :type name: str
        :param age: The age of the person.
        :type age: int
        :param _email: The email of the person.
        :type _email: str
        """
        self.validate_name(name)
        self.validate_age(age)
        self.validate_email(_email)

        self.name = name
        self.age = age
        self._email = _email

    def introduce(self):
        """
        Introduce the person with their name, age, and email.
        
        :return: A formatted string introducing the person.
        :rtype: str
        """
        return f"Student name is {self.name} and they are {self.age} years old, and their email is : {self._email}."

    def validate_name(self, name):
        """
        Validate the person's name.

        :param name: The name to validate.
        :type name: str
        :raises ValueError: If the name is empty.
        :return: None
        """
        if not name:
            raise ValueError("Name cannot be empty.")

    def validate_age(self, age):
        """
        Validate the person's age.

        :param age: The age to validate.
        :type age: int
        :raises ValueError: If the age is not an integer or is negative.
        :return: None
        """
        if type(age) != int:
            raise ValueError("Age must be an integer.")
        if age < 0:
            raise ValueError("Age must be a non-negative integer.")
    
    def validate_email(self, email):
        """
        Validate the person's email address.

        :param email: The email to validate.
        :type email: str
        :raises ValueError: If the email format is invalid.
        :return: None
        """
        reg = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(reg, email):
            raise ValueError("Email address is invalid!")


class student(person):
    """
    A class representing a student, inheriting from person.
    """

    def __init__(self, name, age, _email, student_id, registered_courses):
        """
        Initialize a student with their name, age, email, student ID, and registered courses.
        
        :param name: The name of the student.
        :type name: str
        :param age: The age of the student.
        :type age: int
        :param _email: The email of the student.
        :type _email: str
        :param student_id: The student ID.
        :type student_id: str
        :param registered_courses: List of courses the student is registered for.
        :type registered_courses: list
        """
        super().__init__(name, age, _email)
        self.validate_student_id(student_id)

        self.student_id = student_id
        self.registered_courses = registered_courses

    def register_course(self, course):
        """
        Register a student for a course.

        :param course: The course to register for.
        :type course: str
        :raises ValueError: If the course is empty.
        :return: None
        """
        if not course:
            raise ValueError("Course cannot be empty.")
        self.registered_courses.append(course)

    def validate_student_id(self, student_id):
        """
        Validate the student's ID.

        :param student_id: The student ID to validate.
        :type student_id: str
        :raises ValueError: If the student ID is empty.
        :return: None
        """
        if not student_id:
            raise ValueError("Student ID cannot be empty.")


class instructor(person):
    """
    A class representing an instructor, inheriting from person.
    """

    def __init__(self, name, age, _email, instructor_id, assigned_courses):
        """
        Initialize an instructor with their name, age, email, instructor ID, and assigned courses.
        
        :param name: The name of the instructor.
        :type name: str
        :param age: The age of the instructor.
        :type age: int
        :param _email: The email of the instructor.
        :type _email: str
        :param instructor_id: The instructor ID.
        :type instructor_id: str
        :param assigned_courses: List of courses assigned to the instructor.
        :type assigned_courses: list
        """
        super().__init__(name, age, _email)
        self.validate_instructor_id(instructor_id)
        
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses

    def assign_course(self, course):
        """
        Assign a course to the instructor.

        :param course: The course to assign.
        :type course: str
        :raises ValueError: If the course is empty.
        :return: None
        """
        if not course:
            raise ValueError("Course cannot be empty.")
        self.assigned_courses.append(course)

    def validate_instructor_id(self, instructor_id):
        """
        Validate the instructor's ID.

        :param instructor_id: The instructor ID to validate.
        :type instructor_id: str
        :raises ValueError: If the instructor ID is empty.
        :return: None
        """
        if not instructor_id:
            raise ValueError("Instructor ID cannot be empty.")


class course():
    """
    A class representing a course.
    """

    def __init__(self, course_id, course_name, instructor, enrolled_students):
        """
        Initialize a course with its ID, name, instructor, and enrolled students.
        
        :param course_id: The ID of the course.
        :type course_id: str
        :param course_name: The name of the course.
        :type course_name: str
        :param instructor: The instructor for the course.
        :type instructor: instructor
        :param enrolled_students: List of students enrolled in the course.
        :type enrolled_students: list[student]
        """
        self.validate_course_id(course_id)
        self.validate_course_name(course_name)
        
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students

    def add_student(self, student):
        """
        Add a student to the course.

        :param student: The student to add to the course.
        :type student: student
        :raises ValueError: If the object is not a valid student instance.
        :return: None
        """
        if not isinstance(student, student):
            raise ValueError("Student must be a valid student object.")
        self.enrolled_students.append(student)

    # Validation methods
    def validate_course_id(self, course_id):
        """
        Validate the course ID.

        :param course_id: The course ID to validate.
        :type course_id: str
        :raises ValueError: If the course ID is empty.
        :return: None
        """
        if not course_id:
            raise ValueError("Course ID cannot be empty.")

    def validate_course_name(self, course_name):
        """
        Validate the course name.

        :param course_name: The course name to validate.
        :type course_name: str
        :raises ValueError: If the course name is empty.
        :return: None
        """
        if not course_name:
            raise ValueError("Course name cannot be empty.")

    def to_JSON(self):
        """
        Serialize the course object into JSON format.

        :return: A dictionary representing the course in JSON format.
        :rtype: dict
        """
        return {
            "Course": {
                "course_id": self.course_id,
                "course_name": self.course_name,
                "instructor": self.instructor.to_dict(),
                "enrolled_students": [student.to_dict() for student in self.enrolled_students]
            }
        }

    @classmethod
    def from_JSON(cls, data):
        """
        Deserialize JSON data into a course object.

        :param data: The JSON data to deserialize.
        :type data: dict
        :return: A course object initialized with the data.
        :rtype: course
        """
        course_data = data["Course"]
        instructor_obj = instructor.from_dict(course_data["instructor"])
        enrolled_students = [student.from_dict(s) for s in course_data["enrolled_students"]]
        return cls(course_data["course_id"], course_data["course_name"], instructor_obj, enrolled_students)
