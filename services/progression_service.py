from models.cohort import Cohort
from models.enrollment import Enrollment
from models.result import Result
from storage.json_storage import JSONStorage


class ProgressionService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.cohorts_file = "cohorts.json"
        self.enrollments_file = "enrollments.json"
        self.results_file = "results.json"

    def _load_cohorts(self):
        data = self.storage.load(self.cohorts_file)

        return [
            Cohort.from_dict(cohort)
            for cohort in data
        ]

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

        self.storage.save(self.enrollments_file, data)

    def _load_results(self):
        data = self.storage.load(self.results_file)

        return [
            Result.from_dict(result)
            for result in data
        ]

    def get_failed_modules(self, student_id):
        enrollments = self._load_enrollments()
        results = self._load_results()

        failed_modules = []

        for enrollment in enrollments:

            if enrollment.student_id != student_id:
                continue

            if enrollment.status != "failed":
                continue

            for result in results:
                if result.enrollment_id == enrollment.enrollment_id:
                    failed_modules.append({
                        "module_id": enrollment.module_id,
                        "enrollment_id": enrollment.enrollment_id,
                        "cohort_id": enrollment.cohort_id,
                        "score": result.score,
                        "grade": result.grade
                    })

                    break

        return failed_modules

    def get_repeat_cohorts(self, student_id, module_id):
        cohorts = self._load_cohorts()
        enrollments = self._load_enrollments()

        previous_cohort_ids = set()

        for enrollment in enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.module_id == module_id
            ):
                previous_cohort_ids.add(enrollment.cohort_id)

        available_cohorts = []

        for cohort in cohorts:

            if cohort.module_id != module_id:
                continue

            if cohort.cohort_id in previous_cohort_ids:
                continue

            if cohort.is_full:
                continue

            available_cohorts.append(cohort)

        return available_cohorts

    def repeat_module(
        self,
        student_id,
        module_id,
        new_cohort_id
    ):
        cohorts = self._load_cohorts()
        enrollments = self._load_enrollments()

        previous_cohort_ids = set()

        for enrollment in enrollments:
            if (
                enrollment.student_id == student_id
                and enrollment.module_id == module_id
            ):
                previous_cohort_ids.add(enrollment.cohort_id)

        cohort = None

        for item in cohorts:
            if item.cohort_id == new_cohort_id:
                cohort = item
                break

        if cohort is None:
            raise ValueError("Cohort not found.")

        if cohort.module_id != module_id:
            raise ValueError(
                "This cohort does not belong to the selected module."
            )

        if new_cohort_id in previous_cohort_ids:
            raise ValueError(
                "Student must be assigned to a different cohort."
            )

        if cohort.is_full:
            raise ValueError(
                "This cohort is full."
            )

        cohort.add_student(student_id)

        enrollment_id = f"ENR{len(enrollments) + 1:03d}"

        enrollment = Enrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            module_id=module_id,
            cohort_id=new_cohort_id,
            status="active"
        )

        enrollments.append(enrollment)

        cohort_data = [
            cohort_item.to_dict()
            for cohort_item in cohorts
        ]

        self.storage.save(
            self.cohorts_file,
            cohort_data
        )

        self._save_enrollments(enrollments)

        return enrollment