from models.user import User
from storage.json_storage import JSONStorage
from utils.hashing import hash_password, verify_password


class AuthService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()
        self.users_file = "users.json"
        self.current_user = None

    def _load_users(self):
        return self.storage.load(self.users_file)

    def _save_users(self, users):
        self.storage.save(self.users_file, users)

    def register(self, name, email, password, role="student"):
        users = self._load_users()

        for user_data in users:
            if user_data["email"].lower() == email.lower():
                raise ValueError("A user with this email already exists.")

        salt, password_hash = hash_password(password)

        user_id = f"USR{len(users) + 1:03d}"

        user = User(
            name=name,
            email=email,
            role=role,
            user_id=user_id,
            salt=salt,
            password_hash=password_hash
        )

        users.append(user.to_dict())
        self._save_users(users)

        return user

    def login(self, email, password):
        users = self._load_users()

        for user_data in users:
            if user_data["email"].lower() == email.lower():

                password_valid = verify_password(
                    password,
                    user_data["salt"],
                    user_data["password_hash"]
                )

                if not password_valid:
                    raise ValueError("Invalid email or password.")

                user = User.from_dict(user_data)
                self.current_user = user

                return user

        raise ValueError("Invalid email or password.")

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user