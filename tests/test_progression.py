from services.progression_service import ProgressionService
from services.result_service import ResultService
from storage.json_storage import JSONStorage
from datetime import date, timedelta


def setup_progression_data(tmp_path):
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
            }
        ]
    )

    storage.save(
        "courses.json",
        [
            {
                "course_id": "CS001",
                "name": "Software Engineering",
                "description": "Software Engineering course"
            }
        ]
    )

    storage.save(
        "cohorts.json",
        [
            {
                "cohort_id": "COH001",
                "course_id": "CS001",
                "name": "Python Morning",
                "capacity": 2,
                "student_ids": ["STU001"],
                "start_date": (
                    date.today() + timedelta(days=7)
                ).isoformat(),
                "end_date": (
                    date.today() + timedelta(days=37)
                ).isoformat()
            },
            {
                "cohort_id": "COH002",
                "course_id": "CS001",
                "name": "Python Afternoon",
                "capacity": 2,
                "student_ids": [],
                "start_date": (
                    date.today() + timedelta(days=14)
                ).isoformat(),
                "end_date": (
                    date.today() + timedelta(days=44)
                ).isoformat()
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

    storage.save(
        "results.json",
        []
    )

    return storage


def test_failed_result_marks_enrollment_failed(tmp_path):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result = result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    assert result.passed is False
    assert result.grade == "D"

    enrollments = storage.load("enrollments.json")

    assert enrollments[0]["status"] == "failed"


def test_failed_module_appears_in_progression(
    tmp_path
):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    progression = ProgressionService(storage)

    failed_modules = progression.get_failed_modules(
        "STU001"
    )

    assert len(failed_modules) == 1
    assert failed_modules[0]["module_id"] == "MOD001"
    assert failed_modules[0]["course_id"] == "CS001"
    assert failed_modules[0]["score"] == 42
    assert failed_modules[0]["cohort_id"] == "COH001"


def test_repeat_requires_different_cohort(tmp_path):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    progression = ProgressionService(storage)

    cohorts = progression.get_repeat_cohorts(
        student_id="STU001",
        module_id="MOD001"
    )

    assert len(cohorts) == 1
    assert cohorts[0].cohort_id == "COH002"
    assert cohorts[0].course_id == "CS001"


def test_repeat_creates_new_enrollment(tmp_path):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    progression = ProgressionService(storage)

    new_enrollment = progression.repeat_module(
        student_id="STU001",
        module_id="MOD001",
        new_cohort_id="COH002"
    )

    assert new_enrollment.enrollment_id == "ENR002"
    assert new_enrollment.student_id == "STU001"
    assert new_enrollment.module_id == "MOD001"
    assert new_enrollment.cohort_id == "COH002"
    assert new_enrollment.status == "active"


def test_repeat_updates_current_course_cohort(
    tmp_path
):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    progression = ProgressionService(storage)

    progression.repeat_module(
        student_id="STU001",
        module_id="MOD001",
        new_cohort_id="COH002"
    )

    course_enrollments = storage.load(
        "course_enrollments.json"
    )

    assert len(course_enrollments) == 1
    assert course_enrollments[0]["student_id"] == "STU001"
    assert course_enrollments[0]["course_id"] == "CS001"
    assert course_enrollments[0]["cohort_id"] == "COH002"
    assert course_enrollments[0]["status"] == "active"


def test_repeat_moves_student_between_cohorts(
    tmp_path
):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    progression = ProgressionService(storage)

    progression.repeat_module(
        student_id="STU001",
        module_id="MOD001",
        new_cohort_id="COH002"
    )

    cohorts = storage.load("cohorts.json")

    old_cohort = None
    new_cohort = None

    for cohort in cohorts:
        if cohort["cohort_id"] == "COH001":
            old_cohort = cohort

        if cohort["cohort_id"] == "COH002":
            new_cohort = cohort

    assert old_cohort is not None
    assert new_cohort is not None

    assert "STU001" not in old_cohort["student_ids"]
    assert "STU001" in new_cohort["student_ids"]


def test_repeat_cannot_use_previous_cohort(
    tmp_path
):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    progression = ProgressionService(storage)

    try:
        progression.repeat_module(
            student_id="STU001",
            module_id="MOD001",
            new_cohort_id="COH001"
        )

        assert False

    except ValueError as error:
        assert (
            str(error)
            == "Student must be assigned "
            "to a different cohort."
        )


def test_repeat_can_be_completed(tmp_path):
    storage = setup_progression_data(tmp_path)

    result_service = ResultService(storage)

    result_service.enter_result(
        enrollment_id="ENR001",
        score=42
    )

    progression = ProgressionService(storage)

    new_enrollment = progression.repeat_module(
        student_id="STU001",
        module_id="MOD001",
        new_cohort_id="COH002"
    )

    result = result_service.enter_result(
        enrollment_id=new_enrollment.enrollment_id,
        score=75
    )

    assert result.passed is True
    assert result.grade == "A"

    enrollments = storage.load(
        "enrollments.json"
    )

    original = enrollments[0]
    repeat = enrollments[1]

    assert original["status"] == "failed"
    assert repeat["status"] == "completed"


def test_first_module_is_available_when_not_started(
    tmp_path
):
    storage = setup_progression_data(tmp_path)

    storage.save(
        "enrollments.json",
        []
    )

    storage.save(
        "results.json",
        []
    )

    progression = ProgressionService(storage)

    progress = progression.get_student_progress(
        "STU001"
    )

    assert progress[0]["status"] == "AVAILABLE"


def test_next_module_is_locked_until_previous_is_passed(
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
        []
    )

    storage.save(
        "enrollments.json",
        []
    )

    storage.save(
        "results.json",
        []
    )

    progression = ProgressionService(storage)

    progress = progression.get_student_progress(
        "STU001"
    )

    assert progress[0]["status"] == "AVAILABLE"
    assert progress[1]["status"] == "LOCKED"


def test_next_module_becomes_available_after_previous_passes(
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
        []
    )

    storage.save(
        "enrollments.json",
        [
            {
                "enrollment_id": "ENR001",
                "student_id": "STU001",
                "module_id": "MOD001",
                "cohort_id": "COH001",
                "status": "completed"
            }
        ]
    )

    storage.save(
        "results.json",
        [
            {
                "result_id": "RES001",
                "student_id": "STU001",
                "module_id": "MOD001",
                "enrollment_id": "ENR001",
                "score": 75,
                "pass_mark": 50,
                "grade": "A",
                "passed": True
            }
        ]
    )

    progression = ProgressionService(storage)

    progress = progression.get_student_progress(
        "STU001"
    )

    assert progress[0]["status"] == "PASSED"
    assert progress[1]["status"] == "AVAILABLE"