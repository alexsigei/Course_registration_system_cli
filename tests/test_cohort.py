from services.cohort_service import CohortService
from storage.json_storage import JSONStorage


def setup_cohort_data(tmp_path):
    storage = JSONStorage(tmp_path)

    storage.save(
        "modules.json",
        [
            {
                "module_id": "MOD001",
                "course_id": "CS001",
                "name": "Python Programming",
                "pass_mark": 50,
                "sequence": 1
            }
        ]
    )

    storage.save(
        "cohorts.json",
        []
    )

    return storage


def test_add_cohort(tmp_path):
    storage = setup_cohort_data(tmp_path)

    service = CohortService(storage)

    cohort = service.add_cohort(
        cohort_id="COH001",
        module_id="MOD001",
        name="Python Morning",
        capacity=30,
        start_date="2026-10-01",
        end_date="2026-10-31"
    )

    assert cohort.cohort_id == "COH001"
    assert cohort.module_id == "MOD001"
    assert cohort.capacity == 30
    assert cohort.seats_available == 30


def test_multiple_cohorts_can_use_same_module(tmp_path):
    storage = setup_cohort_data(tmp_path)

    service = CohortService(storage)

    service.add_cohort(
        cohort_id="COH001",
        module_id="MOD001",
        name="Python Morning",
        capacity=30,
        start_date="2026-10-01",
        end_date="2026-10-31"
    )

    service.add_cohort(
        cohort_id="COH002",
        module_id="MOD001",
        name="Python Evening",
        capacity=30,
        start_date="2026-11-01",
        end_date="2026-11-30"
    )

    cohorts = service.get_cohorts_for_module("MOD001")

    assert len(cohorts) == 2


def test_duplicate_cohort_id_is_rejected(tmp_path):
    storage = setup_cohort_data(tmp_path)

    service = CohortService(storage)

    service.add_cohort(
        cohort_id="COH001",
        module_id="MOD001",
        name="Python Morning",
        capacity=30,
        start_date="2026-10-01",
        end_date="2026-10-31"
    )

    try:
        service.add_cohort(
            cohort_id="COH001",
            module_id="MOD001",
            name="Python Evening",
            capacity=30,
            start_date="2026-11-01",
            end_date="2026-11-30"
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "A cohort with this ID already exists."
        )


def test_cohort_requires_existing_module(tmp_path):
    storage = setup_cohort_data(tmp_path)

    service = CohortService(storage)

    try:
        service.add_cohort(
            cohort_id="COH001",
            module_id="MOD999",
            name="Unknown Module Cohort",
            capacity=30,
            start_date="2026-10-01",
            end_date="2026-10-31"
        )
        assert False
    except ValueError as error:
        assert str(error) == "Module not found."


def test_cohort_rejects_invalid_dates(tmp_path):
    storage = setup_cohort_data(tmp_path)

    service = CohortService(storage)

    try:
        service.add_cohort(
            cohort_id="COH001",
            module_id="MOD001",
            name="Invalid Cohort",
            capacity=30,
            start_date="2026-10-31",
            end_date="2026-10-01"
        )
        assert False
    except ValueError as error:
        assert str(error) == (
            "End date must be after start date."
        )