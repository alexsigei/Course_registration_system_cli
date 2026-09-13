from models.cohort import Cohort
from storage.json_storage import JSONStorage
from utils.validators import validate_capacity


class CohortService:
    def __init__(self, storage=None):
        self.storage = storage or JSONStorage()

        self.cohorts_file = "cohorts.json"
        self.modules_file = "modules.json"

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

        self.storage.save(self.cohorts_file, data)

    def _load_modules(self):
        return self.storage.load(self.modules_file)

    def get_cohorts(self):
        return self._load_cohorts()

    def get_cohorts_for_module(self, module_id):
        cohorts = self._load_cohorts()

        return [
            cohort
            for cohort in cohorts
            if cohort.module_id == module_id
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
        module_id,
        name,
        capacity
    ):
        cohorts = self._load_cohorts()
        modules = self._load_modules()

        # Check for duplicate cohort ID
        for cohort in cohorts:
            if cohort.cohort_id == cohort_id:
                raise ValueError(
                    "A cohort with this ID already exists."
                )

        # Check that the module exists
        module_exists = False

        for module in modules:
            if module["module_id"] == module_id:
                module_exists = True
                break

        if not module_exists:
            raise ValueError(
                "Module not found."
            )

        # Validate capacity
        capacity = validate_capacity(capacity)

        cohort = Cohort(
            cohort_id=cohort_id,
            module_id=module_id,
            name=name,
            capacity=capacity
        )

        cohorts.append(cohort)

        self._save_cohorts(cohorts)

        return cohort