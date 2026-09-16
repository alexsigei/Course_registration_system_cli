from models.course_enrollment import CourseEnrollment


def test_course_enrollment_defaults_to_active():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    assert enrollment.status == "active"


def test_course_enrollment_stores_cohort():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    assert enrollment.cohort_id == "COH001"


def test_course_enrollment_can_be_completed():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    enrollment.complete()

    assert enrollment.status == "completed"


def test_course_enrollment_can_be_withdrawn():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    enrollment.withdraw()

    assert enrollment.status == "withdrawn"


def test_course_enrollment_can_change_cohort():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    enrollment.change_cohort("COH002")

    assert enrollment.cohort_id == "COH002"


def test_course_enrollment_to_dict():
    enrollment = CourseEnrollment(
        enrollment_id="CENR001",
        student_id="STU001",
        course_id="CS001",
        cohort_id="COH001"
    )

    data = enrollment.to_dict()

    assert data == {
        "enrollment_id": "CENR001",
        "student_id": "STU001",
        "course_id": "CS001",
        "cohort_id": "COH001",
        "status": "active"
    }


def test_course_enrollment_from_dict():
    data = {
        "enrollment_id": "CENR001",
        "student_id": "STU001",
        "course_id": "CS001",
        "cohort_id": "COH001",
        "status": "active"
    }

    enrollment = CourseEnrollment.from_dict(data)

    assert enrollment.enrollment_id == "CENR001"
    assert enrollment.student_id == "STU001"
    assert enrollment.course_id == "CS001"
    assert enrollment.cohort_id == "COH001"
    assert enrollment.status == "active"


def test_invalid_status_is_rejected():
    try:
        CourseEnrollment(
            enrollment_id="CENR001",
            student_id="STU001",
            course_id="CS001",
            cohort_id="COH001",
            status="invalid"
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "Invalid course enrollment status."
        )