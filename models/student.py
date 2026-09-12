from models.user import User


class Student(User):
    def __init__(self, name, email, student_id):
        super().__init__(name, email, "student")
        self.student_id = student_id

    def __str__(self):
        return f"Student: {self.name} ({self.student_id})"