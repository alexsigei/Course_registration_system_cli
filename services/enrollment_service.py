from models.cohort import Cohort
from models.enrollment import Enrollment
from models.module import Module
from models.result import Result
from storage.json_storage import JSONStorage


class EnrollmentService:
    def __init__(self, storage=None):
        # Initialize storage and data files
        self.storage = storage or JSONStorage()

        self.cohorts_file = "cohorts.json"
        self.enrollments_file = "enrollments.json"
        self.modules_file = "modules.json"
        self.results_file = "results.json"

    def _load_cohorts(self):
        # Load cohort data
        data = self.storage.load(self.cohorts_file)

        return [
            Cohort.from_dict(cohort)
            for cohort in data
        ]

    def _save_cohorts(self, cohorts):
        # Save cohort data
        data = [
            cohort.to_dict()
            for cohort in cohorts
        ]

        self.storage.save(
            self.cohorts_file,
            data
        )

    def _load_enrollments(self):
        # Load enrollment data
        data = self.storage.load(self.enrollments_file)

        return [
            Enrollment.from_dict(enrollment)
            for enrollment in data
        ]

    def _save_enrollments(self, enrollments):
        # Save enrollment data
        data = [
            enrollment.to_dict()
            for enrollment in enrollments
        ]

        self.storage.save(
            self.enrollments_file,
            data
        )

    def _load_modules(self):
        # Load module data
        data = self.storage.load(self.modules_file)

        return [
            Module.from_dict(module)
            for module in data
        ]

    def _load_results(self):
        # Load student results
        data = self.storage.load(self.results_file)

        return [
            Result.from_dict(result)
            for result in data
        ]

    def _has_passed_previous_module(
        self,
        student_id,
        module
    ):
        # Check prerequisite module
        if module.sequence <= 1:
            return True

        modules = self._load_modules()
        results = self._load_results()
        enrollments = self._load_enrollments()

        previous_module = None

        # Find the previous module
        for item in modules:
            if (
                item.course_id == module.course_id
                and item.sequence == module.sequence - 1
            ):
                previous_module = item
                break

        if previous_module is None:
            return True

        # Check if the student passed it
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

    def enroll_student(
        self,
        student_id,
        module_id,
        cohort_id
    ):
        # Enroll student in a module
        cohorts = self._load_cohorts()
        enrollments = self._load_enrollments()

        cohort = None

        # Find selected cohort
        for item in cohorts:
            if item.cohort_id == cohort_id:
                cohort = item
                break

        if cohort is None:
            raise ValueError("Cohort not found.")

        # Validate cohort and module
        if cohort.module_id != module_id:
            raise ValueError(
                "This cohort does not belong to the selected module."
            )

        modules = self._load_modules()

        module = None

        for item in modules:
            if item.module_id == module_id:
                module = item
                break

        if module is None:
            raise ValueError("Module not found.")

        # Enforce sequential progression
        if not self._has_passed_previous_module(
            student_id,
            module
        ):
            raise ValueError(
                "Student must pass the previous module first."
            )

        # Prevent duplicate active enrollment
        for enrollment in enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.module_id == module_id
                and enrollment.status == "active"
            ):
                raise ValueError(
                    "Student is already enrolled in this module."
                )

        # Add student to the cohort
        cohort.add_student(student_id)

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

        # Save updated data
        self._save_cohorts(cohorts)
        self._save_enrollments(enrollments)

        return enrollment

    def get_available_seats(self, cohort_id):
        # Get remaining cohort seats
        cohorts = self._load_cohorts()

        for cohort in cohorts:
            if cohort.cohort_id == cohort_id:
                return cohort.seats_available

        raise ValueError("Cohort not found.")

    def get_cohorts_for_module(self, module_id):
        # Get cohorts for a module
        cohorts = self._load_cohorts()

        return [
            cohort
            for cohort in cohorts
            if cohort.module_id == module_id
        ]

    def get_student_enrollments(self, student_id):
        # Get all student enrollments
        enrollments = self._load_enrollments()

        return [
            enrollment
            for enrollment in enrollments
            if enrollment.student_id == student_id
        ]
