from models.student import Student
from storage.json_storage import JSONStorage


class StudentService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.users_file = "users.json"

    def _load_users(self):
        return self.storage.load(self.users_file)

    def get_students(self):
        users = self._load_users()
        students = []

        for user_data in users:
            if user_data.get("role") == "student":
                students.append(
                    Student.from_dict(user_data)
                )

        return students

    def get_student(self, student_id):
        students = self.get_students()

        for student in students:
            if student.student_id == student_id:
                return student

        raise ValueError("Student not found.")