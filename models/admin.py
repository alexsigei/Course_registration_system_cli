from models.user import User


class Admin(User):
    def __init__(self, name, email, admin_id):
        super().__init__(name, email, "admin")
        self.admin_id = admin_id

    def __str__(self):
        return f"Admin: {self.name} ({self.admin_id})"