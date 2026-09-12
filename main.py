from models.student import Student
from models.admin import Admin


def main():
    student = Student(
        "Alex",
        "alex@example.com",
        "STU001"
    )

    admin = Admin(
        "System Administrator",
        "admin@example.com",
        "ADM001"
    )

    print(student)
    print(student.role)
    print(student.email)

    print()

    print(admin)
    print(admin.role)
    print(admin.email)


if __name__ == "__main__":
    main()