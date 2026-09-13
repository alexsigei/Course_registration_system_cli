from models.cohort import Cohort
from services.enrollment_service import EnrollmentService
from storage.json_storage import JSONStorage


def main():
    storage = JSONStorage()

    cohort = Cohort(
        cohort_id="COH001",
        module_id="MOD001",
        name="Python Cohort A",
        capacity=2
    )

    storage.save(
        "cohorts.json",
        [cohort.to_dict()]
    )

    enrollment_service = EnrollmentService(storage)

    print(
        "Available seats:",
        enrollment_service.get_available_seats("COH001")
    )

    enrollment = enrollment_service.enroll_student(
        student_id="STU003",
        module_id="MOD001",
        cohort_id="COH001"
    )

    print("\nEnrollment created:")
    print(enrollment)

    print(
        "\nAvailable seats:",
        enrollment_service.get_available_seats("COH001")
    )


if __name__ == "__main__":
    main()