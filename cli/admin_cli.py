from rich.console import Console
from rich.table import Table

from services.course_service import CourseService


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
            console.print(
                "\nCohort management will be implemented next."
            )

        elif choice == "4":
            console.print(
                "\nStudent management will be implemented next."
            )

        elif choice == "5":
            console.print(
                "\nResult management will be implemented next."
            )

        elif choice == "6":
            console.print("\nLogging out...")
            break

        else:
            console.print(
                "\n[red]Invalid choice.[/red]"
            )