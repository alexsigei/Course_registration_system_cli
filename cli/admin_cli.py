from rich.console import Console


console = Console()


def show_admin_menu(user):
    while True:
        console.print("\n[bold cyan]Admin Menu[/bold cyan]")
        console.print(f"Welcome, {user.name}!")
        console.print("1. View Profile")
        console.print("2. Manage Courses")
        console.print("3. Manage Cohorts")
        console.print("4. Manage Students")
        console.print("5. Enter Results")
        console.print("6. Logout")

        choice = console.input("\nChoose an option: ")

        if choice == "1":
            console.print("\n[bold]Profile[/bold]")
            console.print(f"Name: {user.name}")
            console.print(f"Email: {user.email}")
            console.print(f"Role: {user.role}")

        elif choice == "2":
            console.print("\nCourse management will be implemented next.")

        elif choice == "3":
            console.print("\nCohort management will be implemented next.")

        elif choice == "4":
            console.print("\nStudent management will be implemented next.")

        elif choice == "5":
            console.print("\nResult management will be implemented next.")

        elif choice == "6":
            console.print("\nLogging out...")
            break

        else:
            console.print("[red]Invalid choice.[/red]")