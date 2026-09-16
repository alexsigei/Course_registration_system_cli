from models.enrollment import Enrollment
from models.module import Module
from models.result import Result
from models.course_enrollment import CourseEnrollment
from storage.json_storage import JSONStorage


class EnrollmentService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.enrollments_file = "enrollments.json"
        self.modules_file = "modules.json"
        self.results_file = "results.json"
        self.course_enrollments_file = "course_enrollments.json"

    def _load_enrollments(self):
        data = self.storage.load(
            self.enrollments_file
        )

        return [
            Enrollment.from_dict(enrollment)
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

    def _load_modules(self):
        data = self.storage.load(
            self.modules_file
        )

        return [
            Module.from_dict(module)
            for module in data
        ]

    def _load_results(self):
        data = self.storage.load(
            self.results_file
        )

        return [
            Result.from_dict(result)
            for result in data
        ]

    def _load_course_enrollments(self):
        data = self.storage.load(
            self.course_enrollments_file
        )

        return [
            CourseEnrollment.from_dict(enrollment)
            for enrollment in data
        ]

    def _has_passed_previous_module(
        self,
        student_id,
        module
    ):
        if module.sequence <= 1:
            return True

        modules = self._load_modules()
        results = self._load_results()
        enrollments = self._load_enrollments()

        previous_module = None

        for item in modules:
            if (
                item.course_id == module.course_id
                and item.sequence == module.sequence - 1
            ):
                previous_module = item
                break

        if previous_module is None:
            return True

        for enrollment in enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.module_id
                == previous_module.module_id
            ):
                for result in results:
                    if (
                        result.enrollment_id
                        == enrollment.enrollment_id
                        and result.passed
                    ):
                        return True

        return False

    def _get_current_course_enrollment(
        self,
        student_id,
        course_id
    ):
        course_enrollments = (
            self._load_course_enrollments()
        )

        for enrollment in course_enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.course_id == course_id
                and enrollment.status == "active"
            ):
                return enrollment

        return None

    def enroll_student(
        self,
        student_id,
        module_id
    ):
        modules = self._load_modules()

        module = None

        for item in modules:
            if item.module_id == module_id:
                module = item
                break

        if module is None:
            raise ValueError(
                "Module not found."
            )

        course_enrollment = (
            self._get_current_course_enrollment(
                student_id,
                module.course_id
            )
        )

        if course_enrollment is None:
            raise ValueError(
                "Student is not enrolled in this course."
            )

        cohort_id = course_enrollment.cohort_id

        if not cohort_id:
            raise ValueError(
                "Student does not have a current cohort "
                "for this course."
            )

        if not self._has_passed_previous_module(
            student_id,
            module
        ):
            raise ValueError(
                "Student must pass the previous module first."
            )

        enrollments = self._load_enrollments()

        for enrollment in enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.module_id == module_id
                and enrollment.status == "active"
            ):
                raise ValueError(
                    "Student is already enrolled in this module."
                )

        enrollment_id = (
            f"ENR{len(enrollments) + 1:03d}"
        )

        enrollment = Enrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            module_id=module_id,
            cohort_id=cohort_id
        )

        enrollments.append(enrollment)

        self._save_enrollments(enrollments)

        return enrollment

    def get_available_seats(self, cohort_id):
        raise ValueError(
            "Seat availability is managed at the course "
            "cohort level."
        )

    def get_student_enrollments(self, student_id):
        enrollments = self._load_enrollments()

        return [
            enrollment
            for enrollment in enrollments
            if enrollment.student_id == student_id
        ]