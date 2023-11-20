import atexit

class EDnevnik:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Initialize other necessary variables or connections

    def logout_user(self):
        # Placeholder method to logout the user session
        print("Logged out the user session")

    def authenticate(self):
        # Method to authenticate with the API using provided credentials
        # Example implementation
        print("Authenticated with username:", self.username)
        atexit.register(self.logout_user)  # Register logout_user on program exit


    @property
    def student_info(self):
        return ("ime", "prezimenovic")  # Placeholder for user info

    @property
    def courses(self):
        return [Course(123), Course(456)]  # Placeholder for available courses

    # @property
    # def all_grades(self):
    #     # Method to retrieve grades from all courses
    #     pass

    def get_course(self, course_id):
        # Method to retrieve a Course object with the provided ID
        # This method should interact with the API to get course details
        # For now, returning a Course object with placeholder data
        return Course(course_id)


class Course:
    def __init__(self, course_id):
        self.course_id = course_id
        # Fetch course details from API using course_id
        # Placeholder data for demonstration purposes
        self.course_name = "Sample Course"
        self.course_years = "2023-2024"
        self.test_objects = []  # Placeholder for Test objects
        self.headmaster = "John Doe"
        self.school_name = "Sample School"
        self.grade_objects = []  # Placeholder for Grade objects

    @property
    def all_grades(self):
        return self.grade_objects

    @property
    def average_grade(self):
        # Calculate the average grade of all subjects in the course
        # Placeholder code for average grade calculation
        return 4.5  # Placeholder average grade value

    @property
    def subjects(self):
        # Return Subject objects for the course
        # Placeholder code to fetch subjects from the API
        return [Subject("Math", "Teacher1"), Subject("Science", "Teacher2")]

    def get_subject(self, subject_name):
        # Method to retrieve a Subject object by name
        # Placeholder code to get subject details
        return Subject(subject_name, "Teacher")

    # Add other methods for Course class


class Subject:
    def __init__(self, subject_name, teacher_name):
        self.subject_name = subject_name
        self.teacher_name = teacher_name
        self.grade_objects = []  # Placeholder for Grade objects

    @property
    def average_grade(self):
        # Calculate the average grade for the subject
        # Placeholder code for average grade calculation
        return 4.2  # Placeholder average grade value

    # Add other methods for Subject class


class Grade:
    def __init__(self, date, note, element, mark, subject):
        self.date = date
        self.note = note
        self.element = element
        self.mark = mark
        self.subject = subject

    # Add other methods for Grade class

if __name__ == "__main__":
    
    # Test the functionality
    edc = EDnevnik("username", "password")
    edc.authenticate()
    print(edc.student_info)  # Output: ('ime', 'prezimenovic')
    print(edc.courses)  # Output: [Course(123), Course(456)]

    course = edc.get_course(092187309123)
    print(course)  # Output: Course object with placeholder data

    print(course.course_name)  # Output: Sample Course
    print(course.average_grade)  # Output: 4.5 (Placeholder value)

    subjects = course.subjects
    print(subjects)  # Output: [Subject('Math', 'Teacher1'), Subject('Science', 'Teacher2')]

    math_subject = course.get_subject("Math")
    print(math_subject)  # Output: Subject object for Math

    print(math_subject.average_grade)  # Output: 4.2 (Placeholder value)
