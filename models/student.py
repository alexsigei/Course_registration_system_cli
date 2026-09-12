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
        super().__init__(
            name=name,
            email=email,
            role="student",
            user_id=user_id,
            salt=salt,
            password_hash=password_hash
        )

        self.student_id = student_id

    def to_dict(self):
        data = super().to_dict()
        data["student_id"] = self.student_id
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            student_id=data["student_id"],
            user_id=data.get("user_id"),
            salt=data.get("salt"),
            password_hash=data.get("password_hash")
        )

    def __str__(self):
        return f"Student: {self.name} ({self.student_id})"