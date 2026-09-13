import argparse

from rich.console import Console
from rich.table import Table

from services.auth_service import AuthService
from services.course_service import CourseService
from services.cohort_service import CohortService
from services.student_service import StudentService

from cli.menu import show_welcome, show_main_menu
from cli.auth_cli import (
    get_login_details,
    get_registration_details
)
from cli.student_cli import show_student_menu
from cli.admin_cli import show_admin_menu


console = Console()


def interactive_mode():
    """
    Start the normal interactive CLI application.
    """

    auth = AuthService()

    show_welcome()

    while True:
        show_main_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            email, password = get_login_details()

            try:
                user = auth.login(
                    email,
                    password
                )

                console.print(
                    f"\n[green]Login successful. "
                    f"Welcome, {user.name}![/green]"
                )

                if user.role == "student":
                    show_student_menu(user)

                elif user.role == "admin":
                    show_admin_menu(user)

                auth.logout()

            except ValueError as error:
                console.print(
                    f"\n[red]Login failed: {error}[/red]"
                )

        elif choice == "2":
            name, email, password = (
                get_registration_details()
            )

            try:
                user = auth.register_student(
                    name=name,
                    email=email,
                    password=password
                )

                console.print(
                    "\n[green]Account created successfully.[/green]"
                )

                console.print(
                    f"Name: {user.name}"
                )

                console.print(
                    f"Student ID: {user.student_id}"
                )

            except ValueError as error:
                console.print(
                    f"\n[red]Registration failed: {error}[/red]"
                )

        elif choice == "3":
            console.print("\nGoodbye!")
            break

        else:
            console.print(
                "\n[red]Invalid choice. "
                "Please select 1, 2 or 3.[/red]"
            )


def list_courses():
    """
    Display all courses using an argparse command.
    """

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

    console.print(table)


def list_cohorts():
    """
    Display all cohorts using an argparse command.
    """

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
        status = (
            "FULL"
            if cohort.is_full
            else "AVAILABLE"
        )

        table.add_row(
            cohort.cohort_id,
            cohort.module_id,
            cohort.name,
            str(cohort.capacity),
            str(cohort.seats_available),
            status
        )

    console.print(table)


def list_students():
    """
    Display all registered students using an argparse command.
    """

    student_service = StudentService()

    students = student_service.get_students()

    if not students:
        console.print(
            "\n[yellow]No students registered.[/yellow]"
        )
        return

    table = Table(title="Students")

    table.add_column("Student ID")
    table.add_column("Name")
    table.add_column("Email")

    for student in students:
        table.add_row(
            student.student_id,
            student.name,
            student.email
        )

    console.print(table)


def create_parser():
    """
    Create the application's argparse parser.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Student Course Registration "
            "System CLI"
        )
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    subparsers.add_parser(
        "courses",
        help="List all courses"
    )

    subparsers.add_parser(
        "cohorts",
        help="List all cohorts"
    )

    subparsers.add_parser(
        "students",
        help="List all registered students"
    )

    return parser


def main():
    parser = create_parser()

    args = parser.parse_args()

    if args.command == "courses":
        list_courses()

    elif args.command == "cohorts":
        list_cohorts()

    elif args.command == "students":
        list_students()

    else:
        interactive_mode()


if __name__ == "__main__":
    main()
