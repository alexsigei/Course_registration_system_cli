import json

import pytest

from services.course_enrollment_service import CourseEnrollmentService


@pytest.fixture
def service(tmp_path, monkeypatch):
    courses_file = tmp_path / "courses.json"
    enrollments_file = tmp_path / "course_enrollments.json"

    courses = [
        {
            "course_id": "CS001",
            "name": "Computer Science",
            "description": "A foundational computer science programme.",
            "module_ids": ["MOD001", "MOD002", "MOD003"]
        },
        {
            "course_id": "CS002",
            "name": "Information Technology",
            "description": "An information technology programme.",
            "module_ids": ["MOD004"]
        }
    ]

    with open(courses_file, "w") as file:
        json.dump(courses, file)

    with open(enrollments_file, "w") as file:
        json.dump([], file)

    monkeypatch.setattr(
        "services.course_enrollment_service.COURSES_FILE",
        courses_file
    )

    monkeypatch.setattr(
        "services.course_enrollment_service.ENROLLMENTS_FILE",
        enrollments_file
    )

    return CourseEnrollmentService()


def test_student_can_enroll_in_course(service):
    enrollment = service.enroll_student(
        student_id="STU001",
        course_id="CS001"
    )

    assert enrollment.student_id == "STU001"
    assert enrollment.course_id == "CS001"
    assert enrollment.status == "active"


def test_course_enrollment_is_saved(service):
    service.enroll_student(
        student_id="STU001",
        course_id="CS001"
    )

    enrollments = service.get_student_enrollments("STU001")

    assert len(enrollments) == 1
    assert enrollments[0].course_id == "CS001"


def test_student_cannot_enroll_in_same_course_twice(service):
    service.enroll_student(
        student_id="STU001",
        course_id="CS001"
    )

    with pytest.raises(ValueError):
        service.enroll_student(
            student_id="STU001",
            course_id="CS001"
        )


def test_student_can_enroll_in_multiple_courses(service):
    first = service.enroll_student(
        student_id="STU001",
        course_id="CS001"
    )

    second = service.enroll_student(
        student_id="STU001",
        course_id="CS002"
    )

    assert first.course_id == "CS001"
    assert second.course_id == "CS002"

    enrollments = service.get_student_enrollments("STU001")

    assert len(enrollments) == 2


def test_enrollment_requires_existing_course(service):
    with pytest.raises(ValueError):
        service.enroll_student(
            student_id="STU001",
            course_id="INVALID"
        )


def test_is_enrolled(service):
    assert service.is_enrolled(
        "STU001",
        "CS001"
    ) is False

    service.enroll_student(
        student_id="STU001",
        course_id="CS001"
    )

    assert service.is_enrolled(
        "STU001",
        "CS001"
    ) is True


def test_get_student_courses(service):
    service.enroll_student(
        student_id="STU001",
        course_id="CS001"
    )

    service.enroll_student(
        student_id="STU001",
        course_id="CS002"
    )

    courses = service.get_student_courses("STU001")

    course_ids = {
        course["course_id"]
        for course in courses
    }

    assert course_ids == {"CS001", "CS002"}