from rich.console import Console
from rich.table import Table

from services.course_service import CourseService
from services.course_enrollment_service import CourseEnrollmentService
from services.enrollment_service import EnrollmentService
from services.progression_service import ProgressionService
from services.result_service import ResultService


console = Console()


def show_profile(user):
    table = Table()

    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Student ID", user.student_id)
    table.add_row("Name", user.name)
    table.add_row("Email", user.email)

    console.print("\n[bold cyan]Student Profile[/bold cyan]")
    console.print(table)


def browse_courses():
    course_service = CourseService()

    courses = course_service.get_courses()

    if not courses:
        console.print(
            "\n[yellow]No courses available.[/yellow]"
        )
        return

    table = Table()

    table.add_column("Course ID")
    table.add_column("Course Name")
    table.add_column("Description")

    for course in courses:
        table.add_row(
            course.course_id,
            course.name,
            course.description
        )

    console.print("\n[bold cyan]Available Courses[/bold cyan]")
    console.print(table)


def enroll_in_course(user):
    course_service = CourseService()
    course_enrollment_service = CourseEnrollmentService()

    courses = course_service.get_courses()

    if not courses:
        console.print(
            "\n[yellow]No courses available.[/yellow]"
        )
        return

    console.print(
        "\n[bold cyan]Available Courses[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Course ID")
    table.add_column("Course Name")

    for index, course in enumerate(courses, start=1):
        table.add_row(
            str(index),
            course.course_id,
            course.name
        )

    console.print(table)

    choice = input(
        "\nSelect course number: "
    ).strip()

    try:
        choice = int(choice)
    except ValueError:
        console.print(
            "[red]Invalid course selection.[/red]"
        )
        return

    if choice < 1 or choice > len(courses):
        console.print(
            "[red]Invalid course selection.[/red]"
        )
        return

    selected_course = courses[choice - 1]

    course_id = selected_course.course_id

    if course_enrollment_service.is_enrolled(
        user.student_id,
        course_id
    ):
        console.print(
            "\n[yellow]You are already enrolled "
            "in this course.[/yellow]"
        )
        return

    available_cohorts = (
        course_enrollment_service.get_available_cohorts(
            course_id
        )
    )

    if not available_cohorts:
        console.print(
            f"\n[yellow]There are no available cohorts "
            f"for {selected_course.name}.[/yellow]"
        )
        console.print(
            "Please check again later or contact an "
            "administrator to create a new cohort."
        )
        return

    console.print(
        f"\n[bold cyan]Available Cohorts - "
        f"{selected_course.name}[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Cohort ID")
    table.add_column("Cohort")
    table.add_column("Capacity")
    table.add_column("Seats Available")
    table.add_column("Start Date")
    table.add_column("End Date")
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
            cohort.start_date or "-",
            cohort.end_date or "-",
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

    selected_cohort = available_cohorts[choice - 1]

    console.print(
        f"\nYou selected: "
        f"[bold]{selected_course.name}[/bold]"
    )
    console.print(
        f"Cohort: [bold]{selected_cohort.name}[/bold]"
    )
    console.print(
        f"Start date: {selected_cohort.start_date}"
    )
    console.print(
        f"End date: {selected_cohort.end_date}"
    )
    console.print(
        f"Seats available: "
        f"{selected_cohort.seats_available}"
    )

    confirmation = input(
        "\nEnroll in this course and cohort? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        console.print(
            "\n[yellow]Course enrollment cancelled.[/yellow]"
        )
        return

    try:
        enrollment = course_enrollment_service.enroll_student(
            student_id=user.student_id,
            course_id=course_id,
            cohort_id=selected_cohort.cohort_id
        )

        console.print(
            "\n[green]Course enrollment successful![/green]"
        )

        console.print(
            f"Enrollment ID: {enrollment.enrollment_id}"
        )

        console.print(
            f"Course: {selected_course.name}"
        )

        console.print(
            f"Cohort: {selected_cohort.name}"
        )

        console.print(
            f"Seats remaining: "
            f"{selected_cohort.seats_available}"
        )

    except ValueError as error:
        console.print(
            f"\n[red]Enrollment failed: {error}[/red]"
        )


def view_modules(user):
    course_service = CourseService()

    courses = course_service.get_courses()

    if not courses:
        console.print(
            "\n[yellow]No courses available.[/yellow]"
        )
        return

    console.print(
        "\n[bold cyan]Courses[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Course ID")
    table.add_column("Course Name")

    for index, course in enumerate(courses, start=1):
        table.add_row(
            str(index),
            course.course_id,
            course.name
        )

    console.print(table)

    choice = input(
        "\nSelect course number: "
    ).strip()

    try:
        choice = int(choice)
    except ValueError:
        console.print(
            "[red]Invalid course selection.[/red]"
        )
        return

    if choice < 1 or choice > len(courses):
        console.print(
            "[red]Invalid course selection.[/red]"
        )
        return

    selected_course = courses[choice - 1]

    modules = course_service.get_modules_for_course(
        selected_course.course_id
    )

    if not modules:
        console.print(
            "\n[yellow]No modules found for this course.[/yellow]"
        )
        return

    table = Table()

    table.add_column("No.")
    table.add_column("Module ID")
    table.add_column("Module Name")
    table.add_column("Sequence")

    for index, module in enumerate(modules, start=1):
        table.add_row(
            str(index),
            module.module_id,
            module.name,
            str(module.sequence)
        )

    console.print(
        f"\n[bold cyan]Modules - "
        f"{selected_course.name}[/bold cyan]"
    )

    console.print(table)


def enroll_in_module(user):
    course_service = CourseService()
    course_enrollment_service = CourseEnrollmentService()
    progression_service = ProgressionService()
    enrollment_service = EnrollmentService()

    courses = course_service.get_courses()

    if not courses:
        console.print(
            "\n[yellow]No courses available.[/yellow]"
        )
        return

    console.print(
        "\n[bold cyan]Available Courses[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Course ID")
    table.add_column("Course Name")

    for index, course in enumerate(courses, start=1):
        table.add_row(
            str(index),
            course.course_id,
            course.name
        )

    console.print(table)

    choice = input(
        "\nSelect course number: "
    ).strip()

    try:
        choice = int(choice)
    except ValueError:
        console.print(
            "[red]Invalid course selection.[/red]"
        )
        return

    if choice < 1 or choice > len(courses):
        console.print(
            "[red]Invalid course selection.[/red]"
        )
        return

    selected_course = courses[choice - 1]
    course_id = selected_course.course_id

    course_enrollment = (
        course_enrollment_service.get_course_enrollment(
            user.student_id,
            course_id
        )
    )

    if course_enrollment is None:
        console.print(
            f"\n[yellow]You are not enrolled in "
            f"{selected_course.name}.[/yellow]"
        )
        console.print(
            "[yellow]Please enroll in the course "
            "before enrolling in a module.[/yellow]"
        )
        return

    progress = progression_service.get_student_progress(
        user.student_id
    )

    available_modules = [
        item
        for item in progress
        if (
            item["status"] == "AVAILABLE"
            and item["course_id"] == course_id
        )
    ]

    if not available_modules:
        console.print(
            "\n[yellow]There are no modules currently "
            "available for enrollment in this course.[/yellow]"
        )
        return

    console.print(
        f"\n[bold cyan]Available Modules - "
        f"{selected_course.name}[/bold cyan]"
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

    selected_module = available_modules[choice - 1]
    module_id = selected_module["module_id"]

    try:
        enrollment = enrollment_service.enroll_student(
            student_id=user.student_id,
            module_id=module_id
        )

        console.print(
            "\n[green]Module enrollment successful![/green]"
        )

        console.print(
            f"Enrollment ID: {enrollment.enrollment_id}"
        )

        console.print(
            f"Course: {selected_course.name}"
        )

        console.print(
            f"Module: {enrollment.module_id}"
        )

        console.print(
            f"Current Cohort: {enrollment.cohort_id}"
        )

    except ValueError as error:
        console.print(
            f"\n[red]Enrollment failed: {error}[/red]"
        )


def show_my_enrollments(user):
    enrollment_service = EnrollmentService()
    result_service = ResultService()
    course_service = CourseService()

    enrollments = enrollment_service.get_student_enrollments(
        user.student_id
    )

    if not enrollments:
        console.print(
            "\n[yellow]You have no module enrollments.[/yellow]"
        )
        return

    results = result_service.get_student_results(
        user.student_id
    )

    table = Table()

    table.add_column("Enrollment")
    table.add_column("Course")
    table.add_column("Module")
    table.add_column("Cohort")
    table.add_column("Status")
    table.add_column("Score")
    table.add_column("Grade")

    for enrollment in enrollments:
        module = course_service.get_module(
            enrollment.module_id
        )

        course = course_service.get_course(
            module.course_id
        )

        score = "-"
        grade = "-"

        for result in results:
            if result.enrollment_id == enrollment.enrollment_id:
                score = str(result.score)
                grade = result.grade
                break

        table.add_row(
            enrollment.enrollment_id,
            course.name,
            module.name,
            enrollment.cohort_id,
            enrollment.status,
            score,
            grade
        )

    console.print(
        "\n[bold cyan]My Enrollments[/bold cyan]"
    )

    console.print(table)


def show_progress(user):
    course_enrollment_service = CourseEnrollmentService()
    progression_service = ProgressionService()

    courses = course_enrollment_service.get_student_courses(
        user.student_id
    )

    if not courses:
        console.print(
            "\n[yellow]You are not enrolled in any courses.[/yellow]"
        )
        return

    progress = progression_service.get_student_progress(
        user.student_id
    )

    for course in courses:
        course_id = course["course_id"]

        course_progress = [
            item
            for item in progress
            if item["course_id"] == course_id
        ]

        if not course_progress:
            continue

        console.print(
            f"\n[bold cyan]{course['name']}[/bold cyan]"
        )

        table = Table()

        table.add_column("Module")
        table.add_column("Sequence")
        table.add_column("Status")
        table.add_column("Score")
        table.add_column("Grade")

        for item in course_progress:
            table.add_row(
                item["module_name"],
                str(item["sequence"]),
                item["status"],
                str(item["score"])
                if item["score"] is not None
                else "-",
                item["grade"]
                if item["grade"] is not None
                else "-"
            )

        console.print(table)


def repeat_failed_module(user):
    progression_service = ProgressionService()

    failed_modules = progression_service.get_failed_modules(
        user.student_id
    )

    if not failed_modules:
        console.print(
            "\n[green]You have no failed modules to repeat.[/green]"
        )
        return

    console.print(
        "\n[bold cyan]Failed Modules[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Module ID")
    table.add_column("Module")
    table.add_column("Course")
    table.add_column("Cohort")

    for index, item in enumerate(
        failed_modules,
        start=1
    ):
        table.add_row(
            str(index),
            item["module_id"],
            item["module_name"],
            item["course_name"],
            item["cohort_id"]
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

    selected_module = failed_modules[choice - 1]

    module_id = selected_module["module_id"]

    repeat_cohorts = progression_service.get_repeat_cohorts(
        user.student_id,
        module_id
    )

    if not repeat_cohorts:
        console.print(
            "\n[yellow]No eligible cohorts are available "
            "for repeating this module.[/yellow]"
        )
        return

    console.print(
        "\n[bold cyan]Eligible Repeat Cohorts[/bold cyan]"
    )

    table = Table()

    table.add_column("No.")
    table.add_column("Cohort ID")
    table.add_column("Cohort")
    table.add_column("Seats Available")
    table.add_column("Start Date")
    table.add_column("End Date")
    table.add_column("Status")

    for index, cohort in enumerate(
        repeat_cohorts,
        start=1
    ):
        table.add_row(
            str(index),
            cohort.cohort_id,
            cohort.name,
            str(cohort.seats_available),
            cohort.start_date or "-",
            cohort.end_date or "-",
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

    if choice < 1 or choice > len(repeat_cohorts):
        console.print(
            "[red]Invalid cohort selection.[/red]"
        )
        return

    selected_cohort = repeat_cohorts[choice - 1]

    console.print(
        f"\nYou selected cohort: "
        f"[bold]{selected_cohort.name}[/bold]"
    )

    console.print(
        f"Start date: {selected_cohort.start_date}"
    )

    console.print(
        f"End date: {selected_cohort.end_date}"
    )

    console.print(
        f"Seats available: "
        f"{selected_cohort.seats_available}"
    )

    confirmation = input(
        "\nRepeat this module in this cohort? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        console.print(
            "\n[yellow]Repeat enrollment cancelled.[/yellow]"
        )
        return

    try:
        enrollment = progression_service.repeat_module(
            student_id=user.student_id,
            module_id=module_id,
            new_cohort_id=selected_cohort.cohort_id
        )

        console.print(
            "\n[green]Module repeat enrollment successful![/green]"
        )

        console.print(
            f"Enrollment ID: {enrollment.enrollment_id}"
        )

        console.print(
            f"Module: {module_id}"
        )

        console.print(
            f"New Cohort: {selected_cohort.name}"
        )

    except ValueError as error:
        console.print(
            f"\n[red]Repeat enrollment failed: {error}[/red]"
        )


def student_menu(user):
    while True:
        console.print(
            "\n[bold blue]Student Menu[/bold blue]"
        )

        console.print("1. View Profile")
        console.print("2. Browse Courses")
        console.print("3. Enroll in Course")
        console.print("4. View Course Modules")
        console.print("5. Enroll in Module")
        console.print("6. My Enrollments")
        console.print("7. My Progress")
        console.print("8. Repeat Failed Module")
        console.print("9. Logout")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            show_profile(user)

        elif choice == "2":
            browse_courses()

        elif choice == "3":
            enroll_in_course(user)

        elif choice == "4":
            view_modules(user)

        elif choice == "5":
            enroll_in_module(user)

        elif choice == "6":
            show_my_enrollments(user)

        elif choice == "7":
            show_progress(user)

        elif choice == "8":
            repeat_failed_module(user)

        elif choice == "9":
            console.print(
                "\n[green]Logged out successfully.[/green]"
            )
            break

        else:
            console.print(
                "\n[red]Invalid option. "
                "Please choose a number from 1 to 9.[/red]"
            )