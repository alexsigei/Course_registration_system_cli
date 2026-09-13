from services.enrollment_service import EnrollmentService
from storage.json_storage import JSONStorage
from services.result_service import ResultService


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

def test_second_module_requires_first_module_to_be_passed(
    tmp_path
):
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
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "module_id": "MOD002",
                "name": "DSA Morning",
                "capacity": 2,
                "student_ids": []
            }
        ]
    )

    storage.save("enrollments.json", [])
    storage.save("results.json", [])

    service = EnrollmentService(storage)

    try:
        service.enroll_student(
            student_id="STU001",
            module_id="MOD002",
            cohort_id="COH001"
        )
        assert False
    except ValueError as error:
        assert (
            str(error)
            == "Student must pass the previous module first."
        )


def test_second_module_can_be_taken_after_passing_first(
    tmp_path
):
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
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "module_id": "MOD001",
                "name": "Python Morning",
                "capacity": 2,
                "student_ids": []
            },
            {
                "cohort_id": "COH002",
                "module_id": "MOD002",
                "name": "DSA Morning",
                "capacity": 2,
                "student_ids": []
            }
        ]
    )

    storage.save(
        "enrollments.json",
        [
            {
                "enrollment_id": "ENR001",
                "student_id": "STU001",
                "module_id": "MOD001",
                "cohort_id": "COH001",
                "status": "active"
            }
        ]
    )

    storage.save("results.json", [])

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=75
    )

    service = EnrollmentService(storage)

    enrollment = service.enroll_student(
        student_id="STU001",
        module_id="MOD002",
        cohort_id="COH002"
    )

    assert enrollment.module_id == "MOD002"
    assert enrollment.status == "active"


def test_failed_previous_module_blocks_next_module(
    tmp_path
):
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
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "module_id": "MOD001",
                "name": "Python Morning",
                "capacity": 2,
                "student_ids": ["STU001"]
            },
            {
                "cohort_id": "COH002",
                "module_id": "MOD002",
                "name": "DSA Morning",
                "capacity": 2,
                "student_ids": []
            }
        ]
    )

    storage.save(
        "enrollments.json",
        [
            {
                "enrollment_id": "ENR001",
                "student_id": "STU001",
                "module_id": "MOD001",
                "cohort_id": "COH001",
                "status": "active"
            }
        ]
    )

    storage.save("results.json", [])

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    service = EnrollmentService(storage)

    try:
        service.enroll_student(
            student_id="STU001",
            module_id="MOD002",
            cohort_id="COH002"
        )
        assert False
    except ValueError as error:
        assert (
            str(error)
            == "Student must pass the previous module first."
        )

def test_student_can_enroll_in_new_cohort_after_first_is_full(
    tmp_path
):
    storage = setup_enrollment_data(tmp_path)

    service = EnrollmentService(storage)

    # Fill the first cohort.
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

    assert service.get_available_seats("COH001") == 0

    # Admin creates a second cohort for the same module.
    from services.cohort_service import CohortService

    cohort_service = CohortService(storage)

    new_cohort = cohort_service.add_cohort(
        cohort_id="COH002",
        module_id="MOD001",
        name="Python Evening",
        capacity=2,
        start_date="2026-11-01",
        end_date="2026-11-30"
    )

    assert new_cohort.cohort_id == "COH002"
    assert new_cohort.module_id == "MOD001"
    assert new_cohort.seats_available == 2

    # A new student can enroll in the new cohort.
    enrollment = service.enroll_student(
        student_id="STU003",
        module_id="MOD001",
        cohort_id="COH002"
    )

    assert enrollment.student_id == "STU003"
    assert enrollment.module_id == "MOD001"
    assert enrollment.cohort_id == "COH002"
    assert enrollment.status == "active"

    assert service.get_available_seats("COH002") == 1