from models.result import Result
from models.enrollment import Enrollment
from storage.json_storage import JSONStorage


class ResultService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.results_file = "results.json"
        self.enrollments_file = "enrollments.json"

    def _load_results(self):
        data = self.storage.load(self.results_file)

        return [
            Result.from_dict(result)
            for result in data
        ]

    def _save_results(self, results):
        data = [
            result.to_dict()
            for result in results
        ]

        self.storage.save(self.results_file, data)

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

    def enter_result(
        self,
        student_id,
        module_id,
        enrollment_id,
        score
    ):
        if score < 0 or score > 100:
            raise ValueError(
                "Score must be between 0 and 100."
            )

        enrollments = self._load_enrollments()
        results = self._load_results()

        enrollment = None

        for item in enrollments:
            if item.enrollment_id == enrollment_id:
                enrollment = item
                break

        if enrollment is None:
            raise ValueError("Enrollment not found.")

        if enrollment.student_id != student_id:
            raise ValueError(
                "Enrollment does not belong to this student."
            )

        if enrollment.module_id != module_id:
            raise ValueError(
                "Enrollment does not belong to this module."
            )

        if enrollment.status != "active":
            raise ValueError(
                "A result can only be entered for an active enrollment."
            )

        for result in results:
            if result.enrollment_id == enrollment_id:
                raise ValueError(
                    "A result already exists for this enrollment."
                )

        result_id = f"RES{len(results) + 1:03d}"

        result = Result(
            result_id=result_id,
            student_id=student_id,
            module_id=module_id,
            enrollment_id=enrollment_id,
            score=score
        )

        if result.passed:
            enrollment.complete()
        else:
            enrollment.fail()

        results.append(result)

        self._save_results(results)
        self._save_enrollments(enrollments)

        return result