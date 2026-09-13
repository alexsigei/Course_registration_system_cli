from services.enrollment_service import EnrollmentService
from storage.json_storage import JSONStorage


def setup_enrollment_data(tmp_path):
    storage = JSONStorage(tmp_path)

    storage.save(
        "modules.json",
        [
            {
                "module_id": "MOD001",
                "course_id": "CS001",
                "name": "Python Programming",
                "pass_mark": 50
            }
        ]
    )

    storage.save(
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "module_id": "MOD001",
                "name": "Python Morning",
                "capacity": 2,
                "student_ids": []
            }
        ]
    )

    storage.save("enrollments.json", [])

    return storage


def test_enroll_student(tmp_path):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD001",
        cohort_id="COH001"
    )

    assert enrollment.student_id == "STU001"
    assert enrollment.module_id == "MOD001"
    assert enrollment.cohort_id == "COH001"
    assert enrollment.status == "active"


def test_enrollment_reduces_available_seats(tmp_path):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    assert service.get_available_seats("COH001") == 2

    service.enroll_student(
        student_id="STU001",
        module_id="MOD001",
        cohort_id="COH001"
    )

    assert service.get_available_seats("COH001") == 1


def test_full_cohort_rejects_enrollment(tmp_path):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        module_id="MOD001",
        cohort_id="COH001"
    )

    service.enroll_student(
        student_id="STU002",
        module_id="MOD001",
        cohort_id="COH001"
    )

    try:
        service.enroll_student(
            student_id="STU003",
            module_id="MOD001",
            cohort_id="COH001"
        )
        assert False
    except ValueError as error:
        assert str(error) == "This cohort is full."


def test_student_cannot_have_two_active_enrollments(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        module_id="MOD001",
        cohort_id="COH001"
    )

    try:
        service.enroll_student(
            student_id="STU001",
            module_id="MOD001",
            cohort_id="COH001"
        )
        assert False
    except ValueError as error:
        assert (
            str(error)
            == "Student is already enrolled in this module."
        )


def test_get_student_enrollments(tmp_path):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        module_id="MOD001",
        cohort_id="COH001"
    )

    enrollments = service.get_student_enrollments("STU001")

    assert len(enrollments) == 1
    assert enrollments[0].student_id == "STU001"