from models.result import Result
from models.enrollment import Enrollment
from models.module import Module
from storage.json_storage import JSONStorage
from utils.validators import validate_score


class ResultService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.results_file = "results.json"
        self.enrollments_file = "enrollments.json"
        self.modules_file = "modules.json"

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

    def _load_modules(self):
        data = self.storage.load(self.modules_file)

        return [
            Module.from_dict(module)
            for module in data
        ]

    def get_active_enrollments(self):
        enrollments = self._load_enrollments()

        return [
            enrollment
            for enrollment in enrollments
            if enrollment.status == "active"
        ]

    def enter_result(
        self,
        enrollment_id,
        score
    ):
        score = validate_score(score)

        enrollments = self._load_enrollments()
        results = self._load_results()
        modules = self._load_modules()

        enrollment = None

        for item in enrollments:
            if item.enrollment_id == enrollment_id:
                enrollment = item
                break

        if enrollment is None:
            raise ValueError(
                "Enrollment not found."
            )

        if enrollment.status != "active":
            raise ValueError(
                "A result can only be entered for an active enrollment."
            )

        module = None

        for item in modules:
            if item.module_id == enrollment.module_id:
                module = item
                break

        if module is None:
            raise ValueError(
                "Module associated with this enrollment was not found."
            )

        for result in results:
            if result.enrollment_id == enrollment_id:
                raise ValueError(
                    "A result already exists for this enrollment."
                )

        result_id = f"RES{len(results) + 1:03d}"

        result = Result(
            result_id=result_id,
            student_id=enrollment.student_id,
            module_id=enrollment.module_id,
            enrollment_id=enrollment.enrollment_id,
            score=score,
            pass_mark=module.pass_mark
        )

        if result.passed:
            enrollment.complete()
        else:
            enrollment.fail()

        results.append(result)

        self._save_results(results)
        self._save_enrollments(enrollments)

        return result