from models.course_enrollment import CourseEnrollment
from models.cohort import Cohort
from storage.json_storage import JSONStorage


class CourseEnrollmentService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.courses_file = "courses.json"
        self.cohorts_file = "cohorts.json"
        self.enrollments_file = "course_enrollments.json"

    def _load_courses(self):
        return self.storage.load(
            self.courses_file
        )

    def _load_cohorts(self):
        data = self.storage.load(
            self.cohorts_file
        )

        return [
            Cohort.from_dict(cohort)
            for cohort in data
        ]

    def _load_enrollments(self):
        data = self.storage.load(
            self.enrollments_file
        )

        return [
            CourseEnrollment.from_dict(enrollment)
            for enrollment in data
        ]

    def _save_enrollments(self, enrollments):
        data = [
            enrollment.to_dict()
            for enrollment in enrollments
        ]

        self.storage.save(
            self.enrollments_file,
            data
        )

    def _save_cohorts(self, cohorts):
        data = [
            cohort.to_dict()
            for cohort in cohorts
        ]

        self.storage.save(
            self.cohorts_file,
            data
        )

    def _course_exists(self, course_id):
        courses = self._load_courses()

        return any(
            course["course_id"] == course_id
            for course in courses
        )

    def is_enrolled(self, student_id, course_id):
        enrollments = self._load_enrollments()

        return any(
            enrollment.student_id == student_id
            and enrollment.course_id == course_id
            and enrollment.status == "active"
            for enrollment in enrollments
        )

    def get_cohorts_for_course(self, course_id):
        cohorts = self._load_cohorts()

        return [
            cohort
            for cohort in cohorts
            if cohort.course_id == course_id
        ]

    def get_available_cohorts(self, course_id):
        cohorts = self.get_cohorts_for_course(course_id)

        return [
            cohort
            for cohort in cohorts
            if not cohort.is_full
            and cohort.status == "NOT_STARTED"
        ]

    def get_course_enrollment(
        self,
        student_id,
        course_id
    ):
        enrollments = self._load_enrollments()

        for enrollment in enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.course_id == course_id
            ):
                return enrollment

        return None

    def enroll_student(
        self,
        student_id,
        course_id,
        cohort_id
    ):
        if not self._course_exists(course_id):
            raise ValueError(
                "Course does not exist."
            )

        if self.is_enrolled(student_id, course_id):
            raise ValueError(
                "Student is already enrolled in this course."
            )

        cohorts = self._load_cohorts()

        selected_cohort = None

        for cohort in cohorts:
            if cohort.cohort_id == cohort_id:
                selected_cohort = cohort
                break

        if selected_cohort is None:
            raise ValueError(
                "Cohort not found."
            )

        if selected_cohort.course_id != course_id:
            raise ValueError(
                "Cohort does not belong to this course."
            )

        if selected_cohort.is_full:
            raise ValueError(
                "This cohort is full."
            )

        if selected_cohort.status != "NOT_STARTED":
            raise ValueError(
                "Students can only join a cohort that has not started."
            )

        selected_cohort.add_student(student_id)

        enrollments = self._load_enrollments()

        enrollment_number = len(enrollments) + 1
        enrollment_id = f"CENR{enrollment_number:03d}"

        enrollment = CourseEnrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            course_id=course_id,
            cohort_id=cohort_id
        )

        enrollments.append(enrollment)

        self._save_enrollments(enrollments)
        self._save_cohorts(cohorts)

        return enrollment

    def get_student_courses(self, student_id):
        courses = self._load_courses()
        enrollments = self._load_enrollments()

        course_ids = {
            enrollment.course_id
            for enrollment in enrollments
            if (
                enrollment.student_id == student_id
                and enrollment.status == "active"
            )
        }

        return [
            course
            for course in courses
            if course["course_id"] in course_ids
        ]