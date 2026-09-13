from models.course import Course
from models.module import Module
from models.cohort import Cohort


def main():
    course = Course(
        course_id="CS101",
        name="Computer Science Fundamentals",
        description="Introduction to computer science."
    )

    module = Module(
        module_id="MOD001",
        course_id="CS101",
        name="Python Programming",
        pass_mark=50
    )

    course.add_module(module.module_id)

    cohort = Cohort(
        cohort_id="COH001",
        module_id=module.module_id,
        name="Python Cohort A",
        capacity=2
    )

    print(course)
    print(course.to_dict())

    print()

    print(module)
    print("Score 75 passed:", module.is_passed(75))
    print("Score 40 passed:", module.is_passed(40))

    print()

    print(cohort)
    print("Seats:", cohort.seats_available)

    cohort.add_student("STU001")
    print(cohort)

    cohort.add_student("STU002")
    print(cohort)

    print("Is full:", cohort.is_full)

    try:
        cohort.add_student("STU003")
    except ValueError as error:
        print("Enrollment error:", error)


if __name__ == "__main__":
    main()