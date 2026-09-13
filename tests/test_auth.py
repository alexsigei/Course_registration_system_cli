import pytest

from services.auth_service import AuthService
from services.course_service import CourseService
from storage.json_storage import JSONStorage


@pytest.fixture
def auth_with_course(tmp_path):
    storage = JSONStorage(tmp_path)

    course_service = CourseService(storage)

    course_service.add_course(
        course_id="CS001",
        name="Computer Science",
        description="Computer Science course"
    )

    return AuthService(storage)


def test_student_registration(auth_with_course):
    auth = auth_with_course

    student = auth.register_student(
        name="Test Student",
        email="student@example.com",
        password="password123",
        course_id="CS001"
    )

    assert student.student_id == "STU001"
    assert student.course_id == "CS001"


def test_password_is_not_stored_directly(tmp_path):
    storage = JSONStorage(tmp_path)
    auth = AuthService(storage)

    auth.register_student(
        name="Test Student",
        email="student@example.com",
        password="password123"
    )

    users = storage.load("users.json")

    assert users[0]["password_hash"] != "password123"
    assert "password" not in users[0]


def test_student_login(tmp_path):
    storage = JSONStorage(tmp_path)
    auth = AuthService(storage)

    auth.register_student(
        name="Test Student",
        email="student@example.com",
        password="password123"
    )

    user = auth.login(
        email="student@example.com",
        password="password123"
    )

    assert user.name == "Test Student"
    assert user.role == "student"
    assert auth.get_current_user() == user


def test_wrong_password_is_rejected(tmp_path):
    storage = JSONStorage(tmp_path)
    auth = AuthService(storage)

    auth.register_student(
        name="Test Student",
        email="student@example.com",
        password="password123"
    )

    try:
        auth.login(
            email="student@example.com",
            password="wrong-password"
        )
        assert False
    except ValueError:
        assert True


def test_duplicate_email_is_rejected(tmp_path):
    storage = JSONStorage(tmp_path)
    auth = AuthService(storage)

    auth.register_student(
        name="First Student",
        email="student@example.com",
        password="password123"
    )

    try:
        auth.register_student(
            name="Second Student",
            email="student@example.com",
            password="different-password"
        )
        assert False
    except ValueError:
        assert True


def test_admin_action_requires_admin(tmp_path):
    storage = JSONStorage(tmp_path)
    auth = AuthService(storage)

    auth.register_student(
        name="Test Student",
        email="student@example.com",
        password="password123"
    )

    auth.login(
        email="student@example.com",
        password="password123"
    )

    try:
        auth.admin_action()
        assert False
    except PermissionError:
        assert True


def test_logout(tmp_path):
    storage = JSONStorage(tmp_path)
    auth = AuthService(storage)

    auth.register_student(
        name="Test Student",
        email="student@example.com",
        password="password123"
    )

    auth.login(
        email="student@example.com",
        password="password123"
    )

    assert auth.get_current_user() is not None

    auth.logout()

    assert auth.get_current_user() is None