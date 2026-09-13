from rich.console import Console
from rich.table import Table

from services.course_service import CourseService
from services.cohort_service import CohortService
from services.student_service import StudentService
from services.result_service import ResultService


console = Console()


def show_profile(user):
    console.print("\n[bold cyan]My Profile[/bold cyan]")

    console.print(f"Name: {user.name}")
    console.print(f"Email: {user.email}")
    console.print(f"Role: {user.role}")
    console.print(f"Admin ID: {user.admin_id}")


def view_courses():
    course_service = CourseService()

    courses = course_service.get_courses()

    if not courses:
        console.print(
            "\n[yellow]No courses available.[/yellow]"
        )
        return

    table = Table(title="Courses")

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


def add_course():
    course_service = CourseService()

    console.print("\n[bold cyan]Add Course[/bold cyan]")

    course_id = console.input("Course ID: ")
    name = console.input("Course name: ")
    description = console.input("Description: ")

    try:
        course = course_service.add_course(
            course_id=course_id,
            name=name,
            description=description
        )

        console.print(
            f"\n[green]Course created successfully.[/green]"
        )
        console.print(course)

    except ValueError as error:
        console.print(
            f"\n[red]Failed to create course: {error}[/red]"
        )


def add_module():
    course_service = CourseService()

    console.print("\n[bold cyan]Add Module[/bold cyan]")

    module_id = console.input("Module ID: ")
    course_id = console.input("Course ID: ")
    name = console.input("Module name: ")
    pass_mark_input = console.input(
        "Pass mark (default 50): "
    )

    try:
        if pass_mark_input.strip():
            pass_mark = int(pass_mark_input)
        else:
            pass_mark = 50

        if pass_mark < 0 or pass_mark > 100:
            raise ValueError(
                "Pass mark must be between 0 and 100."
            )

        module = course_service.add_module(
            module_id=module_id,
            course_id=course_id,
            name=name,
            pass_mark=pass_mark
        )

        console.print(
            f"\n[green]Module created successfully.[/green]"
        )
        console.print(module)

    except ValueError as error:
        console.print(
            f"\n[red]Failed to create module: {error}[/red]"
        )


def manage_courses():
    while True:
        console.print("\n[bold cyan]Course Management[/bold cyan]")

        console.print("1. View Courses")
        console.print("2. Add Course")
        console.print("3. Add Module")
        console.print("4. Back")

        choice = console.input("\nChoose an option: ")

        if choice == "1":
            view_courses()

        elif choice == "2":
            add_course()

        elif choice == "3":
            add_module()

        elif choice == "4":
            break

        else:
            console.print(
                "\n[red]Invalid choice.[/red]"
            )


def view_cohorts():
    cohort_service = CohortService()

    cohorts = cohort_service.get_cohorts()

    if not cohorts:
        console.print(
            "\n[yellow]No cohorts available.[/yellow]"
        )
        return

    table = Table(title="Cohorts")

    table.add_column("ID")
    table.add_column("Module")
    table.add_column("Cohort")
    table.add_column("Capacity")
    table.add_column("Seats Available")
    table.add_column("Status")

    for cohort in cohorts:
        status = "FULL" if cohort.is_full else "AVAILABLE"

        table.add_row(
            cohort.cohort_id,
            cohort.module_id,
            cohort.name,
            str(cohort.capacity),
            str(cohort.seats_available),
            status
        )

    console.print()
    console.print(table)


def add_cohort():
    cohort_service = CohortService()

    console.print("\n[bold cyan]Add Cohort[/bold cyan]")

    cohort_id = console.input("Cohort ID: ")
    module_id = console.input("Module ID: ")
    name = console.input("Cohort name: ")
    capacity_input = console.input("Capacity: ")

    try:
        capacity = int(capacity_input)

        cohort = cohort_service.add_cohort(
            cohort_id=cohort_id,
            module_id=module_id,
            name=name,
            capacity=capacity
        )

        console.print(
            "\n[green]Cohort created successfully.[/green]"
        )

        console.print(cohort)

    except ValueError as error:
        console.print(
            f"\n[red]Failed to create cohort: {error}[/red]"
        )


def manage_cohorts():
    while True:
        console.print("\n[bold cyan]Cohort Management[/bold cyan]")

        console.print("1. View Cohorts")
        console.print("2. Add Cohort")
        console.print("3. Back")

        choice = console.input("\nChoose an option: ")

        if choice == "1":
            view_cohorts()

        elif choice == "2":
            add_cohort()

        elif choice == "3":
            break

        else:
            console.print(
                "\n[red]Invalid choice.[/red]"
            )


def view_students():
    student_service = StudentService()

    students = student_service.get_students()

    if not students:
        console.print(
            "\n[yellow]No students registered.[/yellow]"
        )
        return

    table = Table(title="Registered Students")

    table.add_column("Student ID")
    table.add_column("Name")
    table.add_column("Email")

    for student in students:
        table.add_row(
            student.student_id,
            student.name,
            student.email
        )

    console.print()
    console.print(table)


def view_student():
    student_service = StudentService()

    student_id = console.input(
        "\nEnter student ID: "
    )

    try:
        student = student_service.get_student(
            student_id
        )

        console.print("\n[bold cyan]Student Profile[/bold cyan]")

        console.print(
            f"Student ID: {student.student_id}"
        )
        console.print(
            f"Name: {student.name}"
        )
        console.print(
            f"Email: {student.email}"
        )

    except ValueError as error:
        console.print(
            f"\n[red]{error}[/red]"
        )


def manage_students():
    while True:
        console.print(
            "\n[bold cyan]Student Management[/bold cyan]"
        )

        console.print("1. View Students")
        console.print("2. View Student")
        console.print("3. Back")

        choice = console.input(
            "\nChoose an option: "
        )

        if choice == "1":
            view_students()

        elif choice == "2":
            view_student()

        elif choice == "3":
            break

        else:
            console.print(
                "\n[red]Invalid choice.[/red]"
            )


def view_active_enrollments():
    result_service = ResultService()

    enrollments = result_service.get_active_enrollments()

    if not enrollments:
        console.print(
            "\n[yellow]There are no active enrollments.[/yellow]"
        )
        return

    table = Table(title="Active Enrollments")

    table.add_column("Enrollment")
    table.add_column("Student")
    table.add_column("Module")
    table.add_column("Cohort")
    table.add_column("Status")

    for enrollment in enrollments:
        table.add_row(
            enrollment.enrollment_id,
            enrollment.student_id,
            enrollment.module_id,
            enrollment.cohort_id,
            enrollment.status
        )

    console.print()
    console.print(table)


def enter_result():
    result_service = ResultService()

    console.print(
        "\n[bold cyan]Enter Student Result[/bold cyan]"
    )

    enrollments = result_service.get_active_enrollments()

    if not enrollments:
        console.print(
            "\n[yellow]There are no active enrollments.[/yellow]"
        )
        return

    table = Table(title="Active Enrollments")

    table.add_column("Enrollment")
    table.add_column("Student")
    table.add_column("Module")
    table.add_column("Cohort")

    for enrollment in enrollments:
        table.add_row(
            enrollment.enrollment_id,
            enrollment.student_id,
            enrollment.module_id,
            enrollment.cohort_id
        )

    console.print()
    console.print(table)

    enrollment_id = console.input(
        "\nEnter enrollment ID: "
    )

    score_input = console.input(
        "Enter score (0-100): "
    )

    try:
        score = float(score_input)

        result = result_service.enter_result(
            enrollment_id=enrollment_id,
            score=score
        )

        console.print(
            "\n[green]Result recorded successfully.[/green]"
        )

        console.print(
            f"Student: {result.student_id}"
        )
        console.print(
            f"Module: {result.module_id}"
        )
        console.print(
            f"Score: {result.score}%"
        )
        console.print(
            f"Grade: {result.grade}"
        )

        if result.passed:
            console.print(
                "[green]Status: PASS[/green]"
            )
        else:
            console.print(
                "[red]Status: FAIL[/red]"
            )

    except ValueError as error:
        console.print(
            f"\n[red]Failed to enter result: {error}[/red]"
        )


def show_admin_menu(user):
    while True:
        console.print("\n[bold cyan]Admin Menu[/bold cyan]")
        console.print(f"Welcome, {user.name}!\n")

        console.print("1. View Profile")
        console.print("2. Manage Courses")
        console.print("3. Manage Cohorts")
        console.print("4. Manage Students")
        console.print("5. Enter Results")
        console.print("6. Logout")

        choice = console.input("\nChoose an option: ")

        if choice == "1":
            show_profile(user)

        elif choice == "2":
            manage_courses()

        elif choice == "3":
            manage_cohorts()

        elif choice == "4":
            manage_students()

        elif choice == "5":
            enter_result()

        elif choice == "6":
            console.print("\nLogging out...")
            break

        else:
            console.print(
                "\n[red]Invalid choice.[/red]"
            )