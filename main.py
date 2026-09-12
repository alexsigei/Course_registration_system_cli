from storage.json_storage import JSONStorage


def main():
    storage = JSONStorage()

    students = [
        {
            "student_id": "STU001",
            "name": "Alex",
            "email": "alex@example.com"
        },
        {
            "student_id": "STU002",
            "name": "John",
            "email": "john@example.com"
        }
    ]

    storage.save("students.json", students)

    loaded_students = storage.load("students.json")

    print(loaded_students)


if __name__ == "__main__":
    main()