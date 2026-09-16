from models.user import User


class Student(User):
    def __init__(
        self,
        name,
        email,
        student_id,
        user_id=None,
        salt=None,
        password_hash=None
    ):
        # Initialize student as a user
        super().__init__(
            name=name,
            email=email,
            role="student",
            user_id=user_id,
            salt=salt,
            password_hash=password_hash
        )

        # Store student details
        self.student_id = student_id

    def to_dict(self):
        # Convert student to dictionary
        data = super().to_dict()

        data["student_id"] = self.student_id

        return data

    @classmethod
    def from_dict(cls, data):
        # Create student from dictionary
        return cls(
            name=data["name"],
            email=data["email"],
            student_id=data["student_id"],
            user_id=data.get("user_id"),
            salt=data.get("salt"),
            password_hash=data.get("password_hash")
        )

    def __str__(self):
        # Display student information
        return (
            f"Student: {self.name} "
            f"({self.student_id})"
        )
