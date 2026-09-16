import pytest

from services.course_enrollment_service import CourseEnrollmentService
from storage.json_storage import JSONStorage


def setup_course_data(tmp_path):
    storage = JSONStorage(tmp_path)

    storage.save(
        "courses.json",
        [
            {
                "course_id": "CS001",
                "name": "Computer Science",
                "description": "A foundational computer science programme.",
                "module_ids": [
                    "MOD001",
                    "MOD002",
                    "MOD003"
                ]
            },
            {
                "course_id": "CS002",
                "name": "Information Technology",
                "description": "An information technology programme.",
                "module_ids": [
                    "MOD004"
                ]
            }
        ]
    )

    storage.save(
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "course_id": "CS001",
                "name": "CS Monday Cohort",
                "capacity": 3,
                "student_ids": [],
                "start_date": "2026-10-01",
                "end_date": "2026-10-31"
            },
            {
                "cohort_id": "COH002",
                "course_id": "CS001",
                "name": "CS November Cohort",
                "capacity": 2,
                "student_ids": [],
                "start_date": "2026-11-01",
                "end_date": "2026-11-30"
            },
            {
                "cohort_id": "COH003",
                "course_id": "CS002",
                "name": "IT October Cohort",
                "capacity": 3,
                "student_ids": [],
                "start_date": "2026-10-01",
                "end_date": "2026-10-31"
            }
        ]
    )

    storage.save(
        "course_enrollments.json",
        []
    )

    return storage


def test_student_can_enroll_in_course(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    enrollment = service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    assert enrollment.student_id == "STU001"
    assert enrollment.course_id == "CS001"
    assert enrollment.cohort_id == "COH001"
    assert enrollment.status == "active"


def test_course_enrollment_is_saved(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    saved = storage.load(
        "course_enrollments.json"
    )

    assert len(saved) == 1
    assert saved[0]["enrollment_id"] == "CENR001"
    assert saved[0]["student_id"] == "STU001"
    assert saved[0]["course_id"] == "CS001"
    assert saved[0]["cohort_id"] == "COH001"


def test_student_is_added_to_cohort(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    cohorts = storage.load(
        "cohorts.json"
    )

    cohort = next(
        cohort
        for cohort in cohorts
        if cohort["cohort_id"] == "COH001"
    )

    assert "STU001" in cohort["student_ids"]


def test_student_cannot_enroll_in_same_course_twice(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    with pytest.raises(ValueError) as error:
        service.enroll_student(
            student_id="STU001",
            course_id="CS001",
            cohort_id="COH002"
        )

    assert str(error.value) == (
        "Student is already enrolled in this course."
    )


def test_student_can_enroll_in_multiple_courses(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    first = service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    second = service.enroll_student(
        student_id="STU001",
        course_id="CS002",
        cohort_id="COH003"
    )

    assert first.course_id == "CS001"
    assert first.cohort_id == "COH001"

    assert second.course_id == "CS002"
    assert second.cohort_id == "COH003"


def test_enrollment_requires_existing_course(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    with pytest.raises(ValueError) as error:
        service.enroll_student(
            student_id="STU001",
            course_id="CS999",
            cohort_id="COH001"
        )

    assert str(error.value) == "Course does not exist."


def test_is_enrolled(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    assert service.is_enrolled(
        "STU001",
        "CS001"
    ) is False

    service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    assert service.is_enrolled(
        "STU001",
        "CS001"
    ) is True


def test_get_student_courses(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    courses = service.get_student_courses(
        "STU001"
    )

    assert len(courses) == 1
    assert courses[0]["course_id"] == "CS001"


def test_get_cohorts_for_course(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    cohorts = service.get_cohorts_for_course(
        "CS001"
    )

    assert len(cohorts) == 2

    assert all(
        cohort.course_id == "CS001"
        for cohort in cohorts
    )


def test_get_available_cohorts(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    cohorts = service.get_available_cohorts(
        "CS001"
    )

    assert len(cohorts) == 2


def test_get_course_enrollment(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    enrollment = service.get_course_enrollment(
        student_id="STU001",
        course_id="CS001"
    )

    assert enrollment is not None
    assert enrollment.cohort_id == "COH001"


def test_cohort_must_belong_to_course(tmp_path):
    storage = setup_course_data(tmp_path)

    service = CourseEnrollmentService(storage)

    with pytest.raises(ValueError) as error:
        service.enroll_student(
            student_id="STU001",
            course_id="CS001",
            cohort_id="COH003"
        )

    assert str(error.value) == (
        "Cohort does not belong to this course."
    )


def test_full_cohort_is_rejected(tmp_path):
    storage = setup_course_data(tmp_path)

    cohorts = storage.load(
        "cohorts.json"
    )

    cohorts[0]["student_ids"] = [
        "STU010",
        "STU011",
        "STU012"
    ]

    storage.save(
        "cohorts.json",
        cohorts
    )

    service = CourseEnrollmentService(storage)

    with pytest.raises(ValueError) as error:
        service.enroll_student(
            student_id="STU001",
            course_id="CS001",
            cohort_id="COH001"
        )

    assert str(error.value) == (
        "This cohort is full."
    )