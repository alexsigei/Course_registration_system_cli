class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email address.")

        self._email = value

    def __str__(self):
        return f"{self.name} ({self.email})"