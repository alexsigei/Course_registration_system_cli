from rich.console import Console
from rich.table import Table

from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.progression_service import ProgressionService
from services.result_service import ResultService


console = Console()


def show_profile(user):
    console.print("\n[bold cyan]My Profile[/bold cyan]")

    table = Table()

    table.add_column("Field")
    table.add_column("Value")

    table.add_row("User ID", user.user_id)
    table.add_row("Student ID", user.student_id)
    table.add_row("Name", user.name)
    table.add_row("Email", user.email)
    table.add_row("Role", user.role)

    if hasattr(user, "course_id"):
        table.add_row("Course", user.course_id)

    console.print(table)


def browse_courses():
    service = CourseService()

    courses = service.get_courses()

    if not courses:
        console.print(
            "\n[yellow]No courses available.[/yellow]"
        )
        return

    table = Table(title="Available Courses")

    table.add_column("Course ID")
    table.add_column("Course Name")

    for course in courses:
        table.add_row(
            course["course_id"],
            course["name"]
        )

    console.print()
    console.print(table)


def view_modules():
    service = CourseService()

    courses = service.get_courses()

    if not courses:
        console.print(
            "\n[yellow]No courses available.[/yellow]"
        )
        return

    console.print("\n[bold cyan]Course Modules[/bold cyan]")

    for course in courses:
        console.print(
            f"\n[bold]{course['course_id']} - "
            f"{course['name']}[/bold]"
        )

        modules = service.get_modules(
            course["course_id"]
        )

        if not modules:
            console.print(
                "[yellow]No modules available.[/yellow]"
            )
            continue

        table = Table()

        table.add_column("Module ID")
        table.add_column("Module")
        table.add_column("Sequence")
        table.add_column("Pass Mark")

        for module in modules:
            table.add_row(
                module.module_id,
                module.name,
                str(module.sequence),
                str(module.pass_mark)
            )

        console.print(table)


def enroll_in_module(user):
    progression_service = ProgressionService()
    enrollment_service = EnrollmentService()

    progress = progression_service.get_student_progress(
        user.student_id
    )

    available_modules = [
        item
        for item in progress
        if item["status"] == "AVAILABLE"
    ]

    if not available_modules:
        console.print(
            "\n[yellow]There are no modules currently "
            "available for enrollment.[/yellow]"
        )
        return

    console.print(
        "\n[bold cyan]Available Modules[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Module ID")
    table.add_column("Module")
    table.add_column("Status")

    for index, module in enumerate(
        available_modules,
        start=1
    ):
        table.add_row(
            str(index),
            module["module_id"],
            module["module_name"],
            module["status"]
        )

    console.print(table)

    choice = input(
        "\nSelect module number: "
    ).strip()

    try:
        choice = int(choice)
    except ValueError:
        console.print(
            "[red]Invalid module selection.[/red]"
        )
        return

    if choice < 1 or choice > len(available_modules):
        console.print(
            "[red]Invalid module selection.[/red]"
        )
        return

    selected_module = available_modules[
        choice - 1
    ]

    module_id = selected_module["module_id"]

    cohorts = enrollment_service.get_cohorts_for_module(
        module_id
    )

    available_cohorts = [
        cohort
        for cohort in cohorts
        if not cohort.is_full
        and cohort.status == "NOT_STARTED"
    ]

    if not available_cohorts:
        console.print(
            "\n[yellow]There are no available cohorts "
            "for this module.[/yellow]"
        )
        console.print(
            "Please check again later or contact an administrator."
        )
        return

    console.print(
        "\n[bold cyan]Available Cohorts[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Cohort ID")
    table.add_column("Cohort")
    table.add_column("Capacity")
    table.add_column("Seats Available")
    table.add_column("Status")

    for index, cohort in enumerate(
        available_cohorts,
        start=1
    ):
        table.add_row(
            str(index),
            cohort.cohort_id,
            cohort.name,
            str(cohort.capacity),
            str(cohort.seats_available),
            cohort.status
        )

    console.print(table)

    choice = input(
        "\nSelect cohort number: "
    ).strip()

    try:
        choice = int(choice)
    except ValueError:
        console.print(
            "[red]Invalid cohort selection.[/red]"
        )
        return

    if choice < 1 or choice > len(available_cohorts):
        console.print(
            "[red]Invalid cohort selection.[/red]"
        )
        return

    selected_cohort = available_cohorts[
        choice - 1
    ]

    try:
        enrollment = enrollment_service.enroll_student(
            student_id=user.student_id,
            module_id=module_id,
            cohort_id=selected_cohort.cohort_id
        )

        console.print(
            "\n[green]Enrollment successful![/green]"
        )

        console.print(
            f"Enrollment ID: {enrollment.enrollment_id}"
        )
        console.print(
            f"Module: {enrollment.module_id}"
        )
        console.print(
            f"Cohort: {enrollment.cohort_id}"
        )

        remaining_seats = (
            enrollment_service.get_available_seats(
                selected_cohort.cohort_id
            )
        )

        console.print(
            f"Seats remaining: {remaining_seats}"
        )

    except ValueError as error:
        console.print(
            f"\n[red]{error}[/red]"
        )


def show_my_enrollments(user):
    enrollment_service = EnrollmentService()
    result_service = ResultService()

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

    results = result_service.get_student_results(
        user.student_id
    )

    table = Table(title="My Enrollments")

    table.add_column("Enrollment")
    table.add_column("Module")
    table.add_column("Cohort")
    table.add_column("Status")
    table.add_column("Score")
    table.add_column("Grade")

    for enrollment in student_enrollments:

        score = "-"
        grade = "-"

        for result in results:
            if result.enrollment_id == enrollment.enrollment_id:
                score = f"{result.score}%"
                grade = result.grade
                break

        table.add_row(
            enrollment.enrollment_id,
            enrollment.module_id,
            enrollment.cohort_id,
            enrollment.status,
            score,
            grade
        )

    console.print()
    console.print(table)


def show_progress(user):
    service = ProgressionService()

    progress = service.get_student_progress(
        user.student_id
    )

    if not progress:
        console.print(
            "\n[yellow]No progression data available.[/yellow]"
        )
        return

    table = Table(title="My Academic Progress")

    table.add_column("Module")
    table.add_column("Module Name")
    table.add_column("Status")
    table.add_column("Score")
    table.add_column("Grade")

    passed_count = 0

    for item in progress:

        score = (
            str(item["score"])
            if item["score"] is not None
            else "-"
        )

        grade = (
            item["grade"]
            if item["grade"] is not None
            else "-"
        )

        table.add_row(
            item["module_id"],
            item["module_name"],
            item["status"],
            score,
            grade
        )

        if item["status"] == "PASSED":
            passed_count += 1

    console.print()
    console.print(table)

    total_modules = len(progress)

    percentage = (
        (passed_count / total_modules) * 100
        if total_modules > 0
        else 0
    )

    console.print(
        f"\n[bold cyan]Progress:[/bold cyan] "
        f"{passed_count} / {total_modules} "
        f"modules passed "
        f"({percentage:.1f}%)"
    )


def repeat_failed_module(user):
    progression_service = ProgressionService()

    failed_modules = (
        progression_service.get_failed_modules(
            user.student_id
        )
    )

    if not failed_modules:
        console.print(
            "\n[green]You have no failed modules "
            "requiring a repeat.[/green]"
        )
        return

    console.print(
        "\n[bold cyan]Modules Requiring a Repeat[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Module")
    table.add_column("Previous Enrollment")
    table.add_column("Previous Cohort")
    table.add_column("Score")
    table.add_column("Grade")

    for index, item in enumerate(
        failed_modules,
        start=1
    ):
        table.add_row(
            str(index),
            item["module_id"],
            item["enrollment_id"],
            item["cohort_id"],
            f"{item['score']}%",
            item["grade"]
        )

    console.print(table)

    choice = input(
        "\nSelect module number to repeat: "
    ).strip()

    try:
        choice = int(choice)
    except ValueError:
        console.print(
            "[red]Invalid module selection.[/red]"
        )
        return

    if choice < 1 or choice > len(failed_modules):
        console.print(
            "[red]Invalid module selection.[/red]"
        )
        return

    selected_module = failed_modules[
        choice - 1
    ]

    module_id = selected_module["module_id"]

    cohorts = progression_service.get_repeat_cohorts(
        student_id=user.student_id,
        module_id=module_id
    )

    if not cohorts:
        console.print(
            "\n[yellow]There are no available repeat "
            "cohorts for this module.[/yellow]"
        )
        console.print(
            "Please contact an administrator to create "
            "a new cohort."
        )
        return

    console.print(
        "\n[bold cyan]Available Repeat Cohorts[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Cohort ID")
    table.add_column("Cohort")
    table.add_column("Capacity")
    table.add_column("Seats Available")
    table.add_column("Status")

    for index, cohort in enumerate(
        cohorts,
        start=1
    ):
        table.add_row(
            str(index),
            cohort.cohort_id,
            cohort.name,
            str(cohort.capacity),
            str(cohort.seats_available),
            cohort.status
        )

    console.print(table)

    choice = input(
        "\nSelect repeat cohort number: "
    ).strip()

    try:
        choice = int(choice)
    except ValueError:
        console.print(
            "[red]Invalid cohort selection.[/red]"
        )
        return

    if choice < 1 or choice > len(cohorts):
        console.print(
            "[red]Invalid cohort selection.[/red]"
        )
        return

    selected_cohort = cohorts[
        choice - 1
    ]

    try:
        enrollment = progression_service.repeat_module(
            student_id=user.student_id,
            module_id=module_id,
            new_cohort_id=selected_cohort.cohort_id
        )

        console.print(
            "\n[green]Repeat enrollment successful![/green]"
        )

        console.print(
            f"New Enrollment ID: "
            f"{enrollment.enrollment_id}"
        )
        console.print(
            f"Module: {enrollment.module_id}"
        )
        console.print(
            f"New Cohort: {enrollment.cohort_id}"
        )

    except ValueError as error:
        console.print(
            f"\n[red]{error}[/red]"
        )


def show_student_menu(user):
    while True:
        console.print(
            "\n[bold cyan]Student Menu[/bold cyan]"
        )

        console.print("1. View Profile")
        console.print("2. Browse Courses")
        console.print("3. View Course Modules")
        console.print("4. Enroll in Module")
        console.print("5. My Enrollments")
        console.print("6. My Progress")
        console.print("7. Repeat Failed Module")
        console.print("8. Logout")

        choice = input(
            "\nChoose an option: "
        ).strip()

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
            console.print(
                "\n[green]Logged out successfully.[/green]"
            )
            break

        else:
            console.print(
                "\n[red]Invalid option. "
                "Please try again.[/red]"
            )