import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from data_manager import DataManager
from models import Student, Instructor, Course

class SchoolManagementSystem:
    """
    A GUI application for managing students, instructors, and courses.

    This class creates a Tkinter-based GUI that allows users to add, edit, delete,
    and display records of students, instructors, and courses. It also provides
    functionality to save and load data.

    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        data_manager (DataManager): An instance to handle data operations.
        sorting_order (bool): A flag to track the sorting order in the treeview.
        edit_mode (str): Indicates the current edit mode ('student', 'instructor', 'course').
        current_edit_id (str): The ID of the record currently being edited.
    """

    def __init__(self, root):
        """
        Initializes the SchoolManagementSystem GUI.

        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("School Management System")
        self.data_manager = DataManager()
        self.sorting_order = False  # For sorting treeview columns
        self.edit_mode = None       # Can be 'student', 'instructor', 'course'
        self.current_edit_id = None
        self.create_widgets()

    def create_widgets(self):
        """
        Creates the main widgets of the GUI, including tabs for students,
        instructors, courses, display records, and settings.
        """
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')

        # Student Tab
        self.student_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.student_tab, text='Students')
        self.create_student_tab()

        # Instructor Tab
        self.instructor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.instructor_tab, text='Instructors')
        self.create_instructor_tab()

        # Course Tab
        self.course_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.course_tab, text='Courses')
        self.create_course_tab()

        # Display Tab
        self.display_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.display_tab, text='Display Records')
        self.create_display_tab()

        # Settings Tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text='Settings')
        self.create_settings_tab()

    def create_settings_tab(self):
        """
        Creates the settings tab with options to save and load data.
        """
        # Save and Load buttons
        save_button = ttk.Button(
            self.settings_tab, text="Save Data", command=self.save_data
        )
        save_button.grid(row=0, column=0, padx=5, pady=5)

        load_button = ttk.Button(
            self.settings_tab, text="Load Data", command=self.load_data
        )
        load_button.grid(row=0, column=1, padx=5, pady=5)

    def save_data(self):
        """
        Opens a file dialog to save data to a JSON file.
        """
        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            self.data_manager.save_data(filename)
            messagebox.showinfo("Success", "Data saved successfully!")

    def load_data(self):
        """
        Opens a file dialog to load data from a JSON file.
        """
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            self.data_manager.load_data(filename)
            messagebox.showinfo("Success", "Data loaded successfully!")
            self.update_student_courses_listbox()   # Update course list in student tab
            self.update_instructor_courses_listbox()  # Update course list in instructor tab
            self.update_display()


    def create_student_tab(self):
        """
        Creates the student tab with input fields and controls for adding or editing students.
        """
        # Labels and Entry widgets
        ttk.Label(self.student_tab, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.student_name = ttk.Entry(self.student_tab)
        self.student_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.student_tab, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        self.student_age = ttk.Entry(self.student_tab)
        self.student_age.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.student_tab, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.student_email = ttk.Entry(self.student_tab)
        self.student_email.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.student_tab, text="Student ID:").grid(row=3, column=0, padx=5, pady=5)
        self.student_id = ttk.Entry(self.student_tab)
        self.student_id.grid(row=3, column=1, padx=5, pady=5)

        # Course Selection
        ttk.Label(self.student_tab, text="Select Courses:").grid(row=4, column=0, padx=5, pady=5)
        self.student_courses_listbox = tk.Listbox(self.student_tab, selectmode=tk.MULTIPLE)
        self.student_courses_listbox.grid(row=4, column=1, padx=5, pady=5)
        self.update_student_courses_listbox()

        # Add Button
        self.student_add_button = ttk.Button(
            self.student_tab, text="Add Student", command=self.add_student
        )
        self.student_add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def update_student_courses_listbox(self):
        """
        Updates the listbox in the student tab with the available courses.
        """
        self.student_courses_listbox.delete(0, tk.END)
        for course in self.data_manager.courses.values():
            self.student_courses_listbox.insert(
                tk.END, f"{course.course_id} - {course.course_name}"
            )

    def add_student(self):
        """
        Adds a new student or updates an existing one based on the input fields.

        Validates the input data, creates a Student object, and registers selected courses.
        """
        name = self.student_name.get()
        age = self.student_age.get()
        email = self.student_email.get()
        student_id = self.student_id.get()

        try:
            age = int(age)
            # Get selected courses
            selected_indices = self.student_courses_listbox.curselection()
            selected_courses = []
            for index in selected_indices:
                course_entry = self.student_courses_listbox.get(index)
                course_id = course_entry.split(' - ')[0]
                course = self.data_manager.courses.get(course_id)
                if course:
                    selected_courses.append(course)

            if self.edit_mode == 'student' and self.current_edit_id == student_id:
                # Update existing student
                student = self.data_manager.students[student_id]
                student.name = name
                student.age = age
                student.set_email(email)
                # Remove student from all courses first
                for course in list(student.registered_courses):
                    student.unregister_course(course)
                # Register selected courses
                for course in selected_courses:
                    student.register_course(course)
                messagebox.showinfo("Success", "Student updated successfully!")
                self.edit_mode = None
                self.current_edit_id = None
                self.student_add_button.config(text='Add Student')
                self.student_id.configure(state='normal')
            else:
                # Check if student ID already exists
                if student_id in self.data_manager.students:
                    messagebox.showerror("Error", "Student ID already exists.")
                    return
                student = Student(name, age, email, student_id)
                # Register selected courses
                for course in selected_courses:
                    student.register_course(course)
                self.data_manager.add_student(student)
                messagebox.showinfo("Success", "Student added successfully!")

            self.clear_student_fields()
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_student_fields(self):
        """
        Clears all input fields in the student tab and resets the form.
        """
        self.student_name.delete(0, tk.END)
        self.student_age.delete(0, tk.END)
        self.student_email.delete(0, tk.END)
        self.student_id.delete(0, tk.END)
        self.student_courses_listbox.selection_clear(0, tk.END)
        if self.edit_mode == 'student':
            self.edit_mode = None
            self.current_edit_id = None
            self.student_add_button.config(text='Add Student')
            self.student_id.configure(state='normal')


    def create_instructor_tab(self):
        """
        Creates the instructor tab with input fields and controls for adding or editing instructors.
        """
        # Labels and Entry widgets
        ttk.Label(self.instructor_tab, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.instructor_name = ttk.Entry(self.instructor_tab)
        self.instructor_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.instructor_tab, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        self.instructor_age = ttk.Entry(self.instructor_tab)
        self.instructor_age.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.instructor_tab, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.instructor_email = ttk.Entry(self.instructor_tab)
        self.instructor_email.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.instructor_tab, text="Instructor ID:").grid(row=3, column=0, padx=5, pady=5)
        self.instructor_id = ttk.Entry(self.instructor_tab)
        self.instructor_id.grid(row=3, column=1, padx=5, pady=5)

        # Course Selection
        ttk.Label(self.instructor_tab, text="Assign to Courses:").grid(row=4, column=0, padx=5, pady=5)
        self.instructor_courses_listbox = tk.Listbox(self.instructor_tab, selectmode=tk.MULTIPLE)
        self.instructor_courses_listbox.grid(row=4, column=1, padx=5, pady=5)
        self.update_instructor_courses_listbox()

        # Add Button
        self.instructor_add_button = ttk.Button(
            self.instructor_tab, text="Add Instructor", command=self.add_instructor
        )
        self.instructor_add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def update_instructor_courses_listbox(self):
        """
        Updates the listbox in the instructor tab with the available courses.
        """
        self.instructor_courses_listbox.delete(0, tk.END)
        for course in self.data_manager.courses.values():
            self.instructor_courses_listbox.insert(
                tk.END, f"{course.course_id} - {course.course_name}"
            )

    def add_instructor(self):
        """
        Adds a new instructor or updates an existing one based on the input fields.

        Validates the input data, creates an Instructor object, and assigns selected courses.
        """
        name = self.instructor_name.get()
        age = self.instructor_age.get()
        email = self.instructor_email.get()
        instructor_id = self.instructor_id.get()

        try:
            age = int(age)
            # Get selected courses
            selected_indices = self.instructor_courses_listbox.curselection()
            selected_courses = []
            for index in selected_indices:
                course_entry = self.instructor_courses_listbox.get(index)
                course_id = course_entry.split(' - ')[0]
                course = self.data_manager.courses.get(course_id)
                if course:
                    selected_courses.append(course)

            if self.edit_mode == 'instructor' and self.current_edit_id == instructor_id:
                # Update existing instructor
                instructor = self.data_manager.instructors[instructor_id]
                instructor.name = name
                instructor.age = age
                instructor.set_email(email)
                # Remove instructor from all courses first
                for course in list(instructor.assigned_courses):
                    instructor.unassign_course(course)
                # Assign selected courses
                for course in selected_courses:
                    instructor.assign_course(course)
                messagebox.showinfo("Success", "Instructor updated successfully!")
                self.edit_mode = None
                self.current_edit_id = None
                self.instructor_add_button.config(text='Add Instructor')
                self.instructor_id.configure(state='normal')
            else:
                # Check if instructor ID already exists
                if instructor_id in self.data_manager.instructors:
                    messagebox.showerror("Error", "Instructor ID already exists.")
                    return
                instructor = Instructor(name, age, email, instructor_id)
                # Assign selected courses
                for course in selected_courses:
                    instructor.assign_course(course)
                self.data_manager.add_instructor(instructor)
                messagebox.showinfo("Success", "Instructor added successfully!")

            self.clear_instructor_fields()
            self.update_display()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def clear_instructor_fields(self):
        """
        Clears all input fields in the instructor tab and resets the form.
        """
        self.instructor_name.delete(0, tk.END)
        self.instructor_age.delete(0, tk.END)
        self.instructor_email.delete(0, tk.END)
        self.instructor_id.delete(0, tk.END)
        self.instructor_courses_listbox.selection_clear(0, tk.END)
        if self.edit_mode == 'instructor':
            self.edit_mode = None
            self.current_edit_id = None
            self.instructor_add_button.config(text='Add Instructor')
            self.instructor_id.configure(state='normal')

    def create_course_tab(self):
        """
        Creates the course tab with input fields and controls for adding or editing courses.
        """
        # Labels and Entry widgets
        ttk.Label(self.course_tab, text="Course Name:").grid(row=0, column=0, padx=5, pady=5)
        self.course_name = ttk.Entry(self.course_tab)
        self.course_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.course_tab, text="Course ID:").grid(row=1, column=0, padx=5, pady=5)
        self.course_id = ttk.Entry(self.course_tab)
        self.course_id.grid(row=1, column=1, padx=5, pady=5)

        # Add Button
        self.course_add_button = ttk.Button(
            self.course_tab, text="Add Course", command=self.add_course
        )
        self.course_add_button.grid(row=2, column=0, columnspan=2, pady=10)

    def add_course(self):
        """
        Adds a new course or updates an existing one based on the input fields.

        Validates the input data and creates a Course object.
        """
        course_name = self.course_name.get()
        course_id = self.course_id.get()

        if self.edit_mode == 'course' and self.current_edit_id == course_id:
            # Update existing course
            course = self.data_manager.courses[course_id]
            course.course_name = course_name
            messagebox.showinfo("Success", "Course updated successfully!")
            self.edit_mode = None
            self.current_edit_id = None
            self.course_add_button.config(text='Add Course')
            self.course_id.configure(state='normal')
        else:
            if course_id in self.data_manager.courses:
                messagebox.showerror("Error", "Course ID already exists.")
                return
            course = Course(course_id, course_name)
            self.data_manager.add_course(course)
            messagebox.showinfo("Success", "Course added successfully!")

        self.clear_course_fields()
        self.update_student_courses_listbox()   # Update course list in student tab
        self.update_instructor_courses_listbox()  # Update course list in instructor tab
        self.update_display()

    def clear_course_fields(self):
        """
        Clears all input fields in the course tab and resets the form.
        """
        self.course_name.delete(0, tk.END)
        self.course_id.delete(0, tk.END)
        if self.edit_mode == 'course':
            self.edit_mode = None
            self.current_edit_id = None
            self.course_add_button.config(text='Add Course')
            self.course_id.configure(state='normal')

    def create_display_tab(self):
        """
        Creates the display tab with a treeview to show all records and controls for editing and deleting records.
        """
        # Filter Entry
        ttk.Label(self.display_tab, text="Filter:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_entry = ttk.Entry(self.display_tab)
        self.filter_entry.grid(row=0, column=1, padx=5, pady=5)
        self.filter_entry.bind("<KeyRelease>", lambda e: self.update_display())

        # Treeview for display
        self.tree = ttk.Treeview(
            self.display_tab,
            columns=('Type', 'ID', 'Name', 'Info'),
            show='headings'
        )
        self.tree.heading('Type', text='Type', command=lambda: self.sort_column('Type'))
        self.tree.heading('ID', text='ID', command=lambda: self.sort_column('ID'))
        self.tree.heading('Name', text='Name', command=lambda: self.sort_column('Name'))
        self.tree.heading('Info', text='Additional Info', command=lambda: self.sort_column('Info'))
        self.tree.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.display_tab.grid_rowconfigure(1, weight=1)
        self.display_tab.grid_columnconfigure(1, weight=1)

        # Edit and Delete Buttons
        self.edit_button = ttk.Button(self.display_tab, text="Edit", command=self.edit_record)
        self.edit_button.grid(row=2, column=0, padx=5, pady=5)

        self.delete_button = ttk.Button(self.display_tab, text="Delete", command=self.delete_record)
        self.delete_button.grid(row=2, column=1, padx=5, pady=5)

        self.update_display()

    def sort_column(self, col):
        """
        Sorts the treeview column when the column header is clicked.

        Args:
            col (str): The column name to sort by.
        """
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=self.sorting_order)
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)
        self.sorting_order = not self.sorting_order

    def update_display(self):
        """
        Updates the treeview with records filtered by the text in the filter entry.
        """
        # Get filter text
        filter_text = self.filter_entry.get().lower()

        # Clear the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert Students
        for student in self.data_manager.students.values():
            courses_names = ', '.join([course.course_name for course in student.registered_courses]) \
                if student.registered_courses else "None"
            if filter_text in student.name.lower() or \
               filter_text in student.student_id.lower() or \
               filter_text in courses_names.lower():
                self.tree.insert(
                    '', tk.END,
                    values=(
                        'Student',
                        student.student_id,
                        student.name,
                        f"Age: {student.age}, Courses: {courses_names}"
                    )
                )

        # Insert Instructors
        for instructor in self.data_manager.instructors.values():
            assigned_courses = ', '.join([course.course_name for course in instructor.assigned_courses]) \
                if instructor.assigned_courses else "None"
            if filter_text in instructor.name.lower() or \
               filter_text in instructor.instructor_id.lower() or \
               filter_text in assigned_courses.lower():
                self.tree.insert(
                    '', tk.END,
                    values=(
                        'Instructor',
                        instructor.instructor_id,
                        instructor.name,
                        f"Age: {instructor.age}, Courses: {assigned_courses}"
                    )
                )

        # Insert Courses
        for course in self.data_manager.courses.values():
            instructor_name = course.instructor.name if course.instructor else "None"
            if filter_text in course.course_name.lower() or \
               filter_text in course.course_id.lower() or \
               filter_text in instructor_name.lower():
                self.tree.insert(
                    '', tk.END,
                    values=(
                        'Course',
                        course.course_id,
                        course.course_name,
                        f"Instructor: {instructor_name}"
                    )
                )

    def edit_record(self):
        """
        Handles the edit action for the selected record in the treeview.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to edit.")
            return

        item = self.tree.item(selected_item[0])
        record_type = item['values'][0]
        record_id = str(item['values'][1])

        if record_type == 'Student':
            self.edit_student(record_id)
        elif record_type == 'Instructor':
            self.edit_instructor(record_id)
        elif record_type == 'Course':
            self.edit_course(record_id)

    def edit_student(self, student_id):
        """
        Loads the selected student data into the student tab for editing.

        Args:
            student_id (str): The ID of the student to edit.
        """
        student = self.data_manager.students.get(student_id)
        if student:
            # Fill student data in student tab for editing
            self.notebook.select(self.student_tab)
            self.student_name.delete(0, tk.END)
            self.student_name.insert(0, student.name)
            self.student_age.delete(0, tk.END)
            self.student_age.insert(0, student.age)
            self.student_email.delete(0, tk.END)
            self.student_email.insert(0, student.get_email())
            self.student_id.delete(0, tk.END)
            self.student_id.insert(0, student.student_id)
            self.student_id.configure(state='disabled')

            # Populate course selection for the student
            self.update_student_courses_listbox()
            for i, course in enumerate(self.data_manager.courses.values()):
                if course in student.registered_courses:
                    self.student_courses_listbox.select_set(i)

            # Set edit mode
            self.edit_mode = 'student'
            self.current_edit_id = student_id
            self.student_add_button.config(text='Update Student')

    def edit_instructor(self, instructor_id):
        """
        Loads the selected instructor data into the instructor tab for editing.

        Args:
            instructor_id (str): The ID of the instructor to edit.
        """
        instructor = self.data_manager.instructors.get(instructor_id)
        if instructor:
            # Fill instructor data in instructor tab for editing
            self.notebook.select(self.instructor_tab)
            self.instructor_name.delete(0, tk.END)
            self.instructor_name.insert(0, instructor.name)
            self.instructor_age.delete(0, tk.END)
            self.instructor_age.insert(0, instructor.age)
            self.instructor_email.delete(0, tk.END)
            self.instructor_email.insert(0, instructor.get_email())
            self.instructor_id.delete(0, tk.END)
            self.instructor_id.insert(0, instructor.instructor_id)
            self.instructor_id.configure(state='disabled')

            # Populate course selection for the instructor
            self.update_instructor_courses_listbox()
            for i, course in enumerate(self.data_manager.courses.values()):
                if course in instructor.assigned_courses:
                    self.instructor_courses_listbox.select_set(i)

            # Set edit mode
            self.edit_mode = 'instructor'
            self.current_edit_id = instructor_id
            self.instructor_add_button.config(text='Update Instructor')

    def edit_course(self, course_id):
        """
        Loads the selected course data into the course tab for editing.

        Args:
            course_id (str): The ID of the course to edit.
        """
        course = self.data_manager.courses.get(course_id)
        if course:
            # Fill course data in course tab for editing
            self.notebook.select(self.course_tab)
            self.course_name.delete(0, tk.END)
            self.course_name.insert(0, course.course_name)
            self.course_id.delete(0, tk.END)
            self.course_id.insert(0, course.course_id)
            self.course_id.configure(state='disabled')

            # Set edit mode
            self.edit_mode = 'course'
            self.current_edit_id = course_id
            self.course_add_button.config(text='Update Course')

    def delete_record(self):
        """
        Deletes the selected record from the data manager and updates the display.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return

        item = self.tree.item(selected_item[0])
        record_type = item['values'][0]
        record_id = str(item['values'][1])

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this {record_type}?"
        )
        if not confirm:
            return

        if record_type == 'Student':
            self.data_manager.delete_student(record_id)
        elif record_type == 'Instructor':
            self.data_manager.delete_instructor(record_id)
        elif record_type == 'Course':
            self.data_manager.delete_course(record_id)

        messagebox.showinfo("Success", f"{record_type} record deleted successfully!")
        self.update_display()

    def close_application(self):
        """
        Closes the application safely.
        """
        self.root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.close_application)
    root.mainloop()
