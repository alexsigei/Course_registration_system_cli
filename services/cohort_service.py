from models.cohort import Cohort
from storage.json_storage import JSONStorage
from utils.validators import validate_capacity


class CohortService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.cohorts_file = "cohorts.json"
        self.courses_file = "courses.json"

    def _load_cohorts(self):
        data = self.storage.load(self.cohorts_file)

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

    def _load_courses(self):
        return self.storage.load(
            self.courses_file
        )

    def get_cohorts(self):
        return self._load_cohorts()

    def get_cohorts_for_course(self, course_id):
        cohorts = self._load_cohorts()

        return [
            cohort
            for cohort in cohorts
            if cohort.course_id == course_id
        ]

    def get_cohort(self, cohort_id):
        cohorts = self._load_cohorts()

        for cohort in cohorts:
            if cohort.cohort_id == cohort_id:
                return cohort

        raise ValueError("Cohort not found.")

    def add_cohort(
        self,
        cohort_id,
        course_id,
        name,
        capacity,
        start_date,
        end_date
    ):
        cohorts = self._load_cohorts()
        courses = self._load_courses()

        for cohort in cohorts:
            if cohort.cohort_id == cohort_id:
                raise ValueError(
                    "A cohort with this ID already exists."
                )

        course_exists = False

        for course in courses:
            if course["course_id"] == course_id:
                course_exists = True
                break

        if not course_exists:
            raise ValueError("Course not found.")

        capacity = validate_capacity(capacity)

        if not start_date or not end_date:
            raise ValueError(
                "Start date and end date are required."
            )

        if start_date >= end_date:
            raise ValueError(
                "End date must be after start date."
            )

        cohort = Cohort(
            cohort_id=cohort_id,
            course_id=course_id,
            name=name,
            capacity=capacity,
            start_date=start_date,
            end_date=end_date
        )

        cohorts.append(cohort)

        self._save_cohorts(cohorts)

        return cohort