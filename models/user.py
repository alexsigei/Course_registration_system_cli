from models.person import Person


class User(Person):
    def __init__(self, name, email, role):
        super().__init__(name, email)
        self.role = role

    def __str__(self):
        return f"{self.name} - {self.role}"