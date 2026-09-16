from services.enrollment_service import EnrollmentService
from services.result_service import ResultService
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
                "pass_mark": 50,
                "sequence": 1
            },
            {
                "module_id": "MOD002",
                "course_id": "CS001",
                "name": "Data Structures",
                "pass_mark": 50,
                "sequence": 2
            }
        ]
    )

    storage.save(
        "course_enrollments.json",
        [
            {
                "enrollment_id": "CENR001",
                "student_id": "STU001",
                "course_id": "CS001",
                "cohort_id": "COH001",
                "status": "active"
            }
        ]
    )

    storage.save(
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "course_id": "CS001",
                "name": "CS Morning",
                "capacity": 3,
                "student_ids": ["STU001"],
                "start_date": "2026-10-01",
                "end_date": "2026-10-31"
            }
        ]
    )

    storage.save("enrollments.json", [])
    storage.save("results.json", [])

    return storage


def test_enroll_student(tmp_path):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    assert enrollment.student_id == "STU001"
    assert enrollment.module_id == "MOD001"
    assert enrollment.cohort_id == "COH001"
    assert enrollment.status == "active"


def test_enrollment_does_not_change_course_cohort_seats(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    assert enrollment.cohort_id == "COH001"

    cohorts = storage.load("cohorts.json")

    assert cohorts[0]["student_ids"] == ["STU001"]


def test_full_cohort_does_not_affect_module_enrollment(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)

    cohorts = storage.load("cohorts.json")

    cohorts[0]["capacity"] = 1

    storage.save(
        "cohorts.json",
        cohorts
    )

    service = EnrollmentService(storage)

    enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    assert enrollment.cohort_id == "COH001"


def test_student_cannot_have_two_active_enrollments(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    try:
        service.enroll_student(
            student_id="STU001",
            module_id="MOD001"
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Student is already enrolled in this module."
        )


def test_get_student_enrollments(tmp_path):
    storage = setup_enrollment_data(tmp_path)
    service = EnrollmentService(storage)

    service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    enrollments = service.get_student_enrollments(
        "STU001"
    )

    assert len(enrollments) == 1
    assert enrollments[0].module_id == "MOD001"
    assert enrollments[0].cohort_id == "COH001"


def test_second_module_requires_first_module_to_be_passed(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)

    service = EnrollmentService(storage)

    try:
        service.enroll_student(
            student_id="STU001",
            module_id="MOD002"
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Student must pass the previous module first."
        )


def test_second_module_can_be_taken_after_passing_first(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)

    service = EnrollmentService(storage)

    first_enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id=first_enrollment.enrollment_id,
        score=75
    )

    second_enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD002"
    )

    assert second_enrollment.module_id == "MOD002"
    assert second_enrollment.cohort_id == "COH001"


def test_failed_previous_module_blocks_next_module(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)

    service = EnrollmentService(storage)

    first_enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id=first_enrollment.enrollment_id,
        score=42
    )

    try:
        service.enroll_student(
            student_id="STU001",
            module_id="MOD002"
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Student must pass the previous module first."
        )


def test_module_enrollment_uses_current_course_cohort(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)

    storage.save(
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "course_id": "CS001",
                "name": "CS Morning",
                "capacity": 3,
                "student_ids": ["STU001"],
                "start_date": "2026-10-01",
                "end_date": "2026-10-31"
            },
            {
                "cohort_id": "COH002",
                "course_id": "CS001",
                "name": "CS Evening",
                "capacity": 3,
                "student_ids": []
                ,
                "start_date": "2026-11-01",
                "end_date": "2026-11-30"
            }
        ]
    )

    service = EnrollmentService(storage)

    enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD001"
    )

    assert enrollment.cohort_id == "COH001"