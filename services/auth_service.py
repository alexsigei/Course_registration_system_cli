from models.user import User
from models.student import Student
from models.admin import Admin
from storage.json_storage import JSONStorage
from utils.hashing import hash_password, verify_password
from utils.decorators import login_required, role_required


class AuthService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.users_file = "users.json"
        self.current_user = None

    def _load_users(self):
        return self.storage.load(self.users_file)

    def _save_users(self, users):
        self.storage.save(self.users_file, users)

    def _create_student_id(self, users):
        student_count = sum(
            1 for user in users
            if user.get("role") == "student"
        )

        return f"STU{student_count + 1:03d}"

    def _create_admin_id(self, users):
        admin_count = sum(
            1 for user in users
            if user.get("role") == "admin"
        )

        return f"ADM{admin_count + 1:03d}"

    def register_student(self, name, email, password):
        users = self._load_users()

        for user_data in users:
            if user_data["email"].lower() == email.lower():
                raise ValueError(
                    "A user with this email already exists."
                )

        salt, password_hash = hash_password(password)

        user_id = f"USR{len(users) + 1:03d}"
        student_id = self._create_student_id(users)

        student = Student(
            name=name,
            email=email,
            student_id=student_id,
            user_id=user_id,
            salt=salt,
            password_hash=password_hash
        )

        users.append(student.to_dict())
        self._save_users(users)

        return student

    @role_required("admin")
    def create_admin(self, name, email, password):
        users = self._load_users()

        for user_data in users:
            if user_data["email"].lower() == email.lower():
                raise ValueError(
                    "A user with this email already exists."
                )

        salt, password_hash = hash_password(password)

        user_id = f"USR{len(users) + 1:03d}"
        admin_id = self._create_admin_id(users)

        admin = Admin(
            name=name,
            email=email,
            admin_id=admin_id,
            user_id=user_id,
            salt=salt,
            password_hash=password_hash
        )

        users.append(admin.to_dict())
        self._save_users(users)

        return admin

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
                    raise ValueError(
                        "Invalid email or password."
                    )

                role = user_data["role"]

                if role == "student":
                    student_id = user_data.get(
                        "student_id"
                    )

                    if student_id is None:
                        student_id = (
                            f"STU{user_data['user_id'][3:]}"
                        )

                        user_data["student_id"] = student_id
                        self._save_users(users)

                    user = Student.from_dict(user_data)

                elif role == "admin":
                    admin_id = user_data.get(
                        "admin_id"
                    )

                    if admin_id is None:
                        admin_position = 0

                        for item in users:
                            if item.get("role") == "admin":
                                admin_position += 1

                            if item is user_data:
                                break

                        admin_id = f"ADM{admin_position:03d}"

                        user_data["admin_id"] = admin_id
                        self._save_users(users)

                    user = Admin.from_dict(user_data)

                else:
                    user = User.from_dict(user_data)

                self.current_user = user

                return user

        raise ValueError("Invalid email or password.")

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    @login_required
    def view_profile(self):
        return self.current_user

    @role_required("admin")
    def admin_action(self):
        return "Admin action completed successfully."