import pytest

from models.course_enrollment import CourseEnrollment


def test_course_enrollment_creation():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001"
    )

    assert enrollment.enrollment_id == "CENR001"
    assert enrollment.student_id == "STU001"
    assert enrollment.course_id == "CS001"
    assert enrollment.status == "active"


def test_course_enrollment_to_dict():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001"
    )

    data = enrollment.to_dict()

    assert data == {
        "enrollment_id": "CENR001",
        "student_id": "STU001",
        "course_id": "CS001",
        "status": "active"
    }


def test_course_enrollment_from_dict():
    data = {
        "enrollment_id": "CENR001",
        "student_id": "STU001",
        "course_id": "CS001",
        "status": "active"
    }

    enrollment = CourseEnrollment.from_dict(data)

    assert enrollment.enrollment_id == "CENR001"
    assert enrollment.student_id == "STU001"
    assert enrollment.course_id == "CS001"
    assert enrollment.status == "active"


def test_course_enrollment_complete():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001"
    )

    enrollment.complete()

    assert enrollment.status == "completed"


def test_course_enrollment_withdraw():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001"
    )

    enrollment.withdraw()

    assert enrollment.status == "withdrawn"


def test_invalid_course_enrollment_status():
    with pytest.raises(ValueError):
        CourseEnrollment(
            enrollment_id="CENR001",
            student_id="STU001",
            course_id="CS001",
            status="failed"
        )