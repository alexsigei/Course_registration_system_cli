from models.cohort import Cohort
from models.enrollment import Enrollment
from storage.json_storage import JSONStorage


class EnrollmentService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.cohorts_file = "cohorts.json"
        self.enrollments_file = "enrollments.json"

    def _load_cohorts(self):
        data = self.storage.load(self.cohorts_file)
        return [Cohort.from_dict(cohort) for cohort in data]

    def _save_cohorts(self, cohorts):
        data = [cohort.to_dict() for cohort in cohorts]
        self.storage.save(self.cohorts_file, data)

    def _load_enrollments(self):
        data = self.storage.load(self.enrollments_file)
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

    def enroll_student(
        self,
        student_id,
        module_id,
        cohort_id
    ):
        cohorts = self._load_cohorts()
        enrollments = self._load_enrollments()

        cohort = None

        for item in cohorts:
            if item.cohort_id == cohort_id:
                cohort = item
                break

        if cohort is None:
            raise ValueError("Cohort not found.")

        if cohort.module_id != module_id:
            raise ValueError(
                "This cohort does not belong to the selected module."
            )

        for enrollment in enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.module_id == module_id
                and enrollment.status == "active"
            ):
                raise ValueError(
                    "Student is already enrolled in this module."
                )

        cohort.add_student(student_id)

        enrollment_id = f"ENR{len(enrollments) + 1:03d}"

        enrollment = Enrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            module_id=module_id,
            cohort_id=cohort_id
        )

        enrollments.append(enrollment)

        self._save_cohorts(cohorts)
        self._save_enrollments(enrollments)

        return enrollment

    def get_available_seats(self, cohort_id):
        cohorts = self._load_cohorts()

        for cohort in cohorts:
            if cohort.cohort_id == cohort_id:
                return cohort.seats_available

        raise ValueError("Cohort not found.")

    def get_cohorts_for_module(self, module_id):
        cohorts = self._load_cohorts()

        return [
            cohort
            for cohort in cohorts
            if cohort.module_id == module_id
        ]

    def get_student_enrollments(self, student_id):
        enrollments = self._load_enrollments()

        return [
            enrollment
            for enrollment in enrollments
            if enrollment.student_id == student_id
        ]