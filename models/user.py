from models.person import Person


class User(Person):
    def __init__(
        self,
        name,
        email,
        role,
        user_id=None,
        salt=None,
        password_hash=None
    ):
        super().__init__(name, email)

        self.user_id = user_id
        self.role = role
        self.salt = salt
        self.password_hash = password_hash

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "salt": self.salt,
            "password_hash": self.password_hash
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            role=data["role"],
            user_id=data.get("user_id"),
            salt=data.get("salt"),
            password_hash=data.get("password_hash")
        )

    def __str__(self):
        return f"{self.name} - {self.role}"