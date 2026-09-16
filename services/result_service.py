from models.result import Result
from models.enrollment import Enrollment
from models.module import Module
from storage.json_storage import JSONStorage
from utils.validators import validate_score


class ResultService:
    # Handles the business logic for entering, validating, storing,
    # and retrieving student academic results.
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()
        # Results, enrollments, and modules are stored separately.
        # They are linked together when a result is entered.

        self.results_file = "results.json"
        self.enrollments_file = "enrollments.json"
        self.modules_file = "modules.json"

    def _load_results(self):
         # Load saved results and convert each dictionary back into a Result object.
        data = self.storage.load(self.results_file)

        return [
            Result.from_dict(result)
            for result in data
        ]

    def _save_results(self, results):
        # Convert Result objects into dictionaries before saving them as JSON.
        data = [
            result.to_dict()
            for result in results
        ]

        self.storage.save(self.results_file, data)

    def _load_enrollments(self):
         # Load enrollments so result entry can update the enrollment status.
        data = self.storage.load(self.enrollments_file)

        return [
            Enrollment.from_dict(enrollment)
            for enrollment in data
        ]

    def _save_enrollments(self, enrollments):
         # Persist enrollment status changes such as active -> completed/failed.
        data = [
            enrollment.to_dict()
            for enrollment in enrollments
        ]

        self.storage.save(self.enrollments_file, data)

    def _load_modules(self):
        # Load modules so the correct module-specific pass mark can be used.
        data = self.storage.load(self.modules_file)

        return [
            Module.from_dict(module)
            for module in data
        ]

    def get_active_enrollments(self):
        # Only active enrollments are eligible for a new result.
        # Completed or failed enrollments should not be graded again.
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
                # Stop searching as soon as the requested enrollment is found.
                enrollment = item
                break

        if enrollment is None:
            # Results can only be entered for an enrollment that is still active.
            raise ValueError(
                "Enrollment not found."
            )
       
        if enrollment.status != "active":
            # Results can only be entered for an enrollment that is still active.
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
        # Each enrollment should have one result, so reject duplicate result entry.
        for result in results:
            if result.enrollment_id == enrollment_id:
                raise ValueError(
                    "A result already exists for this enrollment."
                )
        
         # Generate the next result identifier using the number of existing results.
        result_id = f"RES{len(results) + 1:03d}"

        # The Result model calculates the grade and PASS/FAIL status automatically.
        result = Result(
            result_id=result_id,
            student_id=enrollment.student_id,
            module_id=enrollment.module_id,
            enrollment_id=enrollment.enrollment_id,
            score=score,
            pass_mark=module.pass_mark
        )

        # A passing result completes the current enrollment.
        # A failing result marks the enrollment as failed so the student can repeat it.
        if result.passed:
            enrollment.complete()
        else:
            enrollment.fail()
        #Save both sides of the transaction so the result and enrollment status
        # remain consistent after the application is restarted.

        results.append(result)

        self._save_results(results)
        self._save_enrollments(enrollments)

        return result

    def get_student_results(self, student_id):
        # Return only the results belonging to the requested student.
        # This is used by the student CLI to display academic history.
        results = self._load_results()

        return [
            result
            for result in results
            if result.student_id == student_id
        ]