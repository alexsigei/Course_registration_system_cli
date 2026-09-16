from models.cohort import Cohort
from models.enrollment import Enrollment
from models.result import Result
from models.module import Module
from models.course_enrollment import CourseEnrollment
from storage.json_storage import JSONStorage


class ProgressionService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.cohorts_file = "cohorts.json"
        self.enrollments_file = "enrollments.json"
        self.results_file = "results.json"
        self.modules_file = "modules.json"
        self.courses_file = "courses.json"
        self.course_enrollments_file = "course_enrollments.json"

    def _load_cohorts(self):
        data = self.storage.load(
            self.cohorts_file
        )

        return [
            Cohort.from_dict(cohort)
            for cohort in data
        ]

    def _save_cohorts(self, cohorts):
        data = [
            cohort.to_dict()
            for cohort in cohorts
        ]

        self.storage.save(
            self.cohorts_file,
            data
        )

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

    def _load_results(self):
        data = self.storage.load(
            self.results_file
        )

        return [
            Result.from_dict(result)
            for result in data
        ]

    def _load_modules(self):
        data = self.storage.load(
            self.modules_file
        )

        return [
            Module.from_dict(module)
            for module in data
        ]

    def _load_courses(self):
        return self.storage.load(
            self.courses_file
        )

    def _load_course_enrollments(self):
        data = self.storage.load(
            self.course_enrollments_file
        )

        return [
            CourseEnrollment.from_dict(enrollment)
            for enrollment in data
        ]

    def _get_module(self, module_id):
        modules = self._load_modules()

        for module in modules:
            if module.module_id == module_id:
                return module

        return None

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

    def get_failed_modules(self, student_id):
        enrollments = self._load_enrollments()
        results = self._load_results()
        modules = self._load_modules()
        courses = self._load_courses()

        failed_modules = []

        for enrollment in enrollments:

            if enrollment.student_id != student_id:
                continue

            if enrollment.status != "failed":
                continue

            module = None

            for item in modules:
                if item.module_id == enrollment.module_id:
                    module = item
                    break

            if module is None:
                continue

            course_name = enrollment.module_id

            for course in courses:
                if course["course_id"] == module.course_id:
                    course_name = course["name"]
                    break

            for result in results:

                if result.enrollment_id == enrollment.enrollment_id:

                    failed_modules.append({
                        "module_id": enrollment.module_id,
                        "module_name": module.name,
                        "course_id": module.course_id,
                        "course_name": course_name,
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
        module = self._get_module(module_id)

        if module is None:
            raise ValueError(
                "Module not found."
            )

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

            if cohort.course_id != module.course_id:
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
        module = self._get_module(module_id)

        if module is None:
            raise ValueError(
                "Module not found."
            )

        cohorts = self._load_cohorts()
        enrollments = self._load_enrollments()

        failed_modules = self.get_failed_modules(
            student_id
        )

        failed_module = None

        for item in failed_modules:
            if item["module_id"] == module_id:
                failed_module = item
                break

        if failed_module is None:
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

        new_cohort = None

        for cohort in cohorts:

            if cohort.cohort_id == new_cohort_id:
                new_cohort = cohort
                break

        if new_cohort is None:
            raise ValueError(
                "Cohort not found."
            )

        if new_cohort.course_id != module.course_id:
            raise ValueError(
                "This cohort does not belong "
                "to the selected course."
            )

        if new_cohort_id in previous_cohort_ids:
            raise ValueError(
                "Student must be assigned "
                "to a different cohort."
            )

        if new_cohort.status != "NOT_STARTED":
            raise ValueError(
                "Student can only join a cohort "
                "that has not started."
            )

        if new_cohort.is_full:
            raise ValueError(
                "This cohort is full."
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

        old_cohort_id = course_enrollment.cohort_id

        new_cohort.add_student(student_id)

        if old_cohort_id:
            for cohort in cohorts:

                if cohort.cohort_id == old_cohort_id:
                    cohort.remove_student(student_id)
                    break

        course_enrollment.change_cohort(
            new_cohort_id
        )

        course_enrollments = (
            self._load_course_enrollments()
        )

        for enrollment in course_enrollments:

            if (
                enrollment.student_id == student_id
                and enrollment.course_id == module.course_id
                and enrollment.status == "active"
            ):
                enrollment.change_cohort(
                    new_cohort_id
                )
                break

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

        self._save_cohorts(cohorts)
        self._save_enrollments(enrollments)

        self.storage.save(
            self.course_enrollments_file,
            [
                item.to_dict()
                for item in course_enrollments
            ]
        )

        return enrollment

    def get_student_progress(self, student_id):
        """
        Return the academic progression of a student.
        """

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

            if passed:
                status = "PASSED"

            elif active:
                status = "IN PROGRESS"

            elif failed:
                status = "REPEAT REQUIRED"

            else:
                previous_module_passed = False

                if module.sequence == 1:
                    previous_module_passed = True

                else:
                    previous_module = None

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

        return sorted(
            progress,
            key=lambda item: (
                item["course_id"],
                item["sequence"]
            )
        )