from models.cohort import Cohort
from models.enrollment import Enrollment
from models.result import Result
from models.module import Module
from storage.json_storage import JSONStorage


class ProgressionService:
    def __init__(self, storage=None):
        # Initialize storage and data files
        self.storage = storage or JSONStorage()

        self.cohorts_file = "cohorts.json"
        self.enrollments_file = "enrollments.json"
        self.results_file = "results.json"
        self.modules_file = "modules.json"
        self.courses_file = "courses.json"

    def _load_cohorts(self):
        # Load cohort records
        data = self.storage.load(
            self.cohorts_file
        )

        return [
            Cohort.from_dict(cohort)
            for cohort in data
        ]

    def _load_enrollments(self):
        # Load enrollment records
        data = self.storage.load(
            self.enrollments_file
        )

        return [
            Enrollment.from_dict(enrollment)
            for enrollment in data
        ]

    def _save_enrollments(self, enrollments):
        # Save enrollment records
        data = [
            enrollment.to_dict()
            for enrollment in enrollments
        ]

        self.storage.save(
            self.enrollments_file,
            data
        )

    def _load_results(self):
        # Load student results
        data = self.storage.load(
            self.results_file
        )

        return [
            Result.from_dict(result)
            for result in data
        ]

    def _load_modules(self):
        # Load module records
        data = self.storage.load(
            self.modules_file
        )

        return [
            Module.from_dict(module)
            for module in data
        ]

    def _load_courses(self):
        # Load course records
        return self.storage.load(
            self.courses_file
        )

    def get_failed_modules(self, student_id):
        # Find modules the student failed
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

    def get_repeat_cohorts(
        self,
        student_id,
        module_id
    ):
        # Find new cohorts for a repeated module
        cohorts = self._load_cohorts()
        enrollments = self._load_enrollments()

        previous_cohort_ids = set()

        for enrollment in enrollments:

            if (
                enrollment.student_id == student_id
                and enrollment.module_id == module_id
            ):
                previous_cohort_ids.add(
                    enrollment.cohort_id
                )

        available_cohorts = []

        for cohort in cohorts:

            if cohort.module_id != module_id:
                continue

            if cohort.cohort_id in previous_cohort_ids:
                continue

            if cohort.is_full:
                continue

            if cohort.status != "NOT_STARTED":
                continue

            available_cohorts.append(cohort)

        return available_cohorts

    def repeat_module(
        self,
        student_id,
        module_id,
        new_cohort_id
    ):
        # Create enrollment for a repeated module
        cohorts = self._load_cohorts()
        enrollments = self._load_enrollments()

        failed_modules = self.get_failed_modules(
            student_id
        )

        has_failed_module = any(
            item["module_id"] == module_id
            for item in failed_modules
        )

        if not has_failed_module:
            raise ValueError(
                "Student has not failed this module."
            )

        previous_cohort_ids = set()

        for enrollment in enrollments:

            if (
                enrollment.student_id == student_id
                and enrollment.module_id == module_id
            ):
                previous_cohort_ids.add(
                    enrollment.cohort_id
                )

        # Find the selected cohort
        cohort = None

        for item in cohorts:

            if item.cohort_id == new_cohort_id:
                cohort = item
                break

        if cohort is None:
            raise ValueError(
                "Cohort not found."
            )

        if cohort.module_id != module_id:
            raise ValueError(
                "This cohort does not belong "
                "to the selected module."
            )

        # Prevent using the previous cohort
        if new_cohort_id in previous_cohort_ids:
            raise ValueError(
                "Student must be assigned "
                "to a different cohort."
            )

        if cohort.status != "NOT_STARTED":
            raise ValueError(
                "Student can only join a cohort "
                "that has not started."
            )

        if cohort.is_full:
            raise ValueError(
                "This cohort is full."
            )

        # Add student to the new cohort
        cohort.add_student(student_id)

        enrollment_id = (
            f"ENR{len(enrollments) + 1:03d}"
        )

        enrollment = Enrollment(
            enrollment_id=enrollment_id,
            student_id=student_id,
            module_id=module_id,
            cohort_id=new_cohort_id,
            status="active"
        )

        enrollments.append(enrollment)

        # Save updated cohort data
        cohort_data = [
            cohort_item.to_dict()
            for cohort_item in cohorts
        ]

        self.storage.save(
            self.cohorts_file,
            cohort_data
        )

        # Save the new enrollment
        self._save_enrollments(
            enrollments
        )

        return enrollment

    def get_student_progress(self, student_id):
        """
        Return the academic progression of a student.
        """

        # Load data needed for progression
        enrollments = self._load_enrollments()
        results = self._load_results()
        modules = self._load_modules()

        student_enrollments = [
            enrollment
            for enrollment in enrollments
            if enrollment.student_id == student_id
        ]

        progress = []

        for module in modules:

            module_enrollments = [
                enrollment
                for enrollment in student_enrollments
                if enrollment.module_id == module.module_id
            ]

            passed = False
            failed = False
            active = False
            score = None
            grade = None

            # Check the student's module results
            for enrollment in module_enrollments:

                for result in results:

                    if (
                        result.enrollment_id
                        == enrollment.enrollment_id
                    ):
                        if result.passed:
                            passed = True

                        else:
                            failed = True

                        score = result.score
                        grade = result.grade

                if enrollment.status == "active":
                    active = True

            # Determine the module status
            if passed:
                status = "PASSED"

            elif active:
                status = "IN PROGRESS"

            elif failed:
                status = "REPEAT REQUIRED"

            else:
                previous_module_passed = False

                # First module has no prerequisite
                if module.sequence == 1:
                    previous_module_passed = True

                else:
                    previous_module = None

                    # Find the previous module
                    for item in modules:
                        if (
                            item.course_id == module.course_id
                            and item.sequence
                            == module.sequence - 1
                        ):
                            previous_module = item
                            break

                    if previous_module is None:
                        previous_module_passed = True

                    else:
                        # Check whether prerequisite was passed
                        for enrollment in student_enrollments:
                            if (
                                enrollment.module_id
                                == previous_module.module_id
                            ):
                                for result in results:
                                    if (
                                        result.enrollment_id
                                        == enrollment.enrollment_id
                                        and result.passed
                                    ):
                                        previous_module_passed = True
                                        break

                                if previous_module_passed:
                                    break

                # Unlock module when prerequisite is passed
                if previous_module_passed:
                    status = "AVAILABLE"
                else:
                    status = "LOCKED"


            progress.append({
                "module_id": module.module_id,
                "module_name": module.name,
                "course_id": module.course_id,
                "sequence": module.sequence,
                "status": status,
                "score": score,
                "grade": grade
            })

        # Return modules in sequence order
        return sorted(
            progress,
            key=lambda item: item["sequence"]
        )
