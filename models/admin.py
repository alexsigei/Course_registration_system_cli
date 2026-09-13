from models.user import User


class Admin(User):
    def __init__(
        self,
        name,
        email,
        admin_id,
        user_id=None,
        salt=None,
        password_hash=None
    ):
        super().__init__(
            name=name,
            email=email,
            role="admin",
            user_id=user_id,
            salt=salt,
            password_hash=password_hash
        )

        self.admin_id = admin_id

    def to_dict(self):
        data = super().to_dict()
        data["admin_id"] = self.admin_id
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            email=data["email"],
            admin_id=data["admin_id"],
            user_id=data.get("user_id"),
            salt=data.get("salt"),
            password_hash=data.get("password_hash")
        )

    def __str__(self):
        return f"Admin: {self.name} ({self.admin_id})"