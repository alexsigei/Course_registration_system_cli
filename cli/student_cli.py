from rich.console import Console


console = Console()


def show_student_menu(user):
    while True:
        console.print("\n[bold cyan]Student Menu[/bold cyan]")
        console.print(f"Welcome, {user.name}!")
        console.print("1. View Profile")
        console.print("2. Browse Courses")
        console.print("3. My Enrollments")
        console.print("4. My Progress")
        console.print("5. Logout")

        choice = console.input("\nChoose an option: ")

        if choice == "1":
            console.print("\n[bold]Profile[/bold]")
            console.print(f"Name: {user.name}")
            console.print(f"Email: {user.email}")
            console.print(f"Role: {user.role}")

        elif choice == "2":
            console.print("\nCourse browsing will be implemented next.")

        elif choice == "3":
            console.print("\nEnrollment functionality will be implemented next.")

        elif choice == "4":
            console.print("\nProgress tracking will be implemented next.")

        elif choice == "5":
            console.print("\nLogging out...")
            break

        else:
            console.print("[red]Invalid choice.[/red]")