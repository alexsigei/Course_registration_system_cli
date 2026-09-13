from rich.console import Console
from rich.table import Table

from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.progression_service import ProgressionService


console = Console()


def show_profile(user):
    console.print("\n[bold cyan]My Profile[/bold cyan]")

    console.print(f"Name: {user.name}")
    console.print(f"Email: {user.email}")
    console.print(f"Role: {user.role}")


def browse_courses():
    course_service = CourseService()

    courses = course_service.get_courses()

    if not courses:
        console.print("\n[yellow]No courses available.[/yellow]")
        return

    table = Table(title="Available Courses")

    table.add_column("ID")
    table.add_column("Course")
    table.add_column("Description")

    for course in courses:
        table.add_row(
            course.course_id,
            course.name,
            course.description
        )

    console.print()
    console.print(table)


def view_modules():
    course_service = CourseService()

    course_id = console.input("\nEnter course ID: ")

    try:
        modules = course_service.get_modules_for_course(course_id)

        if not modules:
            console.print(
                "\n[yellow]No modules found for this course.[/yellow]"
            )
            return

        table = Table(title="Course Modules")

        table.add_column("ID")
        table.add_column("Module")
        table.add_column("Pass Mark")

        for module in modules:
            table.add_row(
                module.module_id,
                module.name,
                str(module.pass_mark)
            )

        console.print()
        console.print(table)

    except ValueError as error:
        console.print(f"\n[red]{error}[/red]")


def enroll_in_module(user):
    course_service = CourseService()
    enrollment_service = EnrollmentService()

    module_id = console.input("\nEnter module ID: ")

    try:
        module = course_service.get_module(module_id)

        cohorts = enrollment_service.get_cohorts_for_module(
            module_id
        )

        if not cohorts:
            console.print(
                "\n[yellow]No cohorts are available for this module.[/yellow]"
            )
            return

        table = Table(title=f"{module.name} - Available Cohorts")

        table.add_column("ID")
        table.add_column("Cohort")
        table.add_column("Capacity")
        table.add_column("Seats Available")
        table.add_column("Status")

        for cohort in cohorts:
            status = "FULL" if cohort.is_full else "AVAILABLE"

            table.add_row(
                cohort.cohort_id,
                cohort.name,
                str(cohort.capacity),
                str(cohort.seats_available),
                status
            )

        console.print()
        console.print(table)

        cohort_id = console.input(
            "\nEnter cohort ID to enroll: "
        )

        enrollment = enrollment_service.enroll_student(
            student_id=user.student_id,
            module_id=module_id,
            cohort_id=cohort_id
        )

        console.print(
            f"\n[green]Successfully enrolled.[/green]"
        )
        console.print(enrollment)

    except ValueError as error:
        console.print(f"\n[red]Enrollment failed: {error}[/red]")


def show_my_enrollments(user):
    enrollment_service = EnrollmentService()

    student_enrollments = (
        enrollment_service.get_student_enrollments(
            user.student_id
        )
    )

    if not student_enrollments:
        console.print(
            "\n[yellow]You have no enrollments.[/yellow]"
        )
        return

    table = Table(title="My Enrollments")

    table.add_column("Enrollment")
    table.add_column("Module")
    table.add_column("Cohort")
    table.add_column("Status")

    for enrollment in student_enrollments:
        table.add_row(
            enrollment.enrollment_id,
            enrollment.module_id,
            enrollment.cohort_id,
            enrollment.status
        )

    console.print()
    console.print(table)


def show_progress(user):
    progression_service = ProgressionService()

    failed_modules = progression_service.get_failed_modules(
        user.student_id
    )

    console.print("\n[bold cyan]My Progress[/bold cyan]")

    if not failed_modules:
        console.print(
            "[green]No failed modules. Keep progressing![/green]"
        )
        return

    table = Table(title="Modules Requiring a Repeat")

    table.add_column("Module")
    table.add_column("Score")
    table.add_column("Grade")
    table.add_column("Previous Cohort")

    for item in failed_modules:
        table.add_row(
            item["module_id"],
            f'{item["score"]}%',
            item["grade"],
            item["cohort_id"]
        )

    console.print()
    console.print(table)


def repeat_failed_module(user):
    progression_service = ProgressionService()

    failed_modules = progression_service.get_failed_modules(
        user.student_id
    )

    if not failed_modules:
        console.print(
            "\n[green]You have no modules to repeat.[/green]"
        )
        return

    console.print("\n[bold cyan]Failed Modules[/bold cyan]")

    for item in failed_modules:
        console.print(
            f'{item["module_id"]} - '
            f'{item["score"]}% ({item["grade"]})'
        )

    module_id = console.input(
        "\nEnter module ID to repeat: "
    )

    matching_module = None

    for item in failed_modules:
        if item["module_id"] == module_id:
            matching_module = item
            break

    if matching_module is None:
        console.print(
            "\n[red]You have not failed that module.[/red]"
        )
        return

    cohorts = progression_service.get_repeat_cohorts(
        user.student_id,
        module_id
    )

    if not cohorts:
        console.print(
            "\n[yellow]No suitable repeat cohorts are currently available.[/yellow]"
        )
        return

    table = Table(title="Available Repeat Cohorts")

    table.add_column("ID")
    table.add_column("Cohort")
    table.add_column("Seats Available")

    for cohort in cohorts:
        table.add_row(
            cohort.cohort_id,
            cohort.name,
            str(cohort.seats_available)
        )

    console.print()
    console.print(table)

    cohort_id = console.input(
        "\nEnter new cohort ID: "
    )

    try:
        enrollment = progression_service.repeat_module(
            student_id=user.student_id,
            module_id=module_id,
            new_cohort_id=cohort_id
        )

        console.print(
            "\n[green]Repeat enrollment successful.[/green]"
        )
        console.print(enrollment)

    except ValueError as error:
        console.print(
            f"\n[red]Repeat enrollment failed: {error}[/red]"
        )


def show_student_menu(user):
    while True:
        console.print("\n[bold cyan]Student Menu[/bold cyan]")
        console.print(f"Welcome, {user.name}!\n")

        console.print("1. View Profile")
        console.print("2. Browse Courses")
        console.print("3. View Course Modules")
        console.print("4. Enroll in Module")
        console.print("5. My Enrollments")
        console.print("6. My Progress")
        console.print("7. Repeat Failed Module")
        console.print("8. Logout")

        choice = console.input("\nChoose an option: ")

        if choice == "1":
            show_profile(user)

        elif choice == "2":
            browse_courses()

        elif choice == "3":
            view_modules()

        elif choice == "4":
            enroll_in_module(user)

        elif choice == "5":
            show_my_enrollments(user)

        elif choice == "6":
            show_progress(user)

        elif choice == "7":
            repeat_failed_module(user)

        elif choice == "8":
            console.print("\nLogging out...")
            break

        else:
            console.print(
                "\n[red]Invalid choice.[/red]"
            )