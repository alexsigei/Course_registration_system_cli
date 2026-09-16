import pytest

from models.person import Person
from models.module import Module
from models.cohort import Cohort
from models.enrollment import Enrollment
from models.result import Result


def test_person_email_validation():
    person = Person(
        name="Test User",
        email="test@example.com"
    )

    assert person.email == "test@example.com"


def test_person_rejects_invalid_email():
    try:
        Person(
            name="Test User",
            email="invalid-email"
        )
        assert False
    except ValueError:
        assert True


def test_module_pass_mark():
    module = Module(
        module_id="MOD001",
        course_id="CS001",
        name="Python Programming",
        pass_mark=50
    )

    assert module.is_passed(50)
    assert module.is_passed(75)
    assert not module.is_passed(49)


def test_cohort_seat_availability():
    cohort = Cohort(
        cohort_id="COH001",
        course_id="CS001",
        name="Python Morning",
        capacity=2
    )

    cohort.add_student("STU001")

    assert cohort.seats_available == 1


def test_full_cohort_rejects_student():
    cohort = Cohort(
        cohort_id="COH001",
        course_id="CS001",
        name="Python Morning",
        capacity=1
    )

    cohort.add_student("STU001")

    with pytest.raises(ValueError):
        cohort.add_student("STU002")


def test_enrollment_can_fail():
    enrollment = Enrollment(
        enrollment_id="ENR001",
        student_id="STU001",
        module_id="MOD001",
        cohort_id="COH001"
    )

    enrollment.fail()

    assert enrollment.status == "failed"


def test_result_pass():
    result = Result(
        result_id="RES001",
        student_id="STU001",
        module_id="MOD001",
        enrollment_id="ENR001",
        score=75,
        pass_mark=50
    )

    assert result.grade == "A"
    assert result.passed is True


def test_result_fail():
    result = Result(
        result_id="RES002",
        student_id="STU001",
        module_id="MOD001",
        enrollment_id="ENR002",
        score=42,
        pass_mark=50
    )

    assert result.grade == "D"
    assert result.passed is False