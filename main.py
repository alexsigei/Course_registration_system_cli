from models.student import Student
from storage.json_storage import JSONStorage


def main():
    student = Student(
        name="Alex",
        email="alex@example.com",
        student_id="STU001",
        user_id="USR001",
        salt="example-salt",
        password_hash="example-hash"
    )

    storage = JSONStorage()

    storage.save("test_users.json", [student.to_dict()])

    saved_data = storage.load("test_users.json")

    loaded_student = Student.from_dict(saved_data[0])

    print("Original:")
    print(student)

    print()

    print("Loaded from JSON:")
    print(loaded_student)

    print()

    print("Loaded email:")
    print(loaded_student.email)


if __name__ == "__main__":
    main()