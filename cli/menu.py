from rich.console import Console
from rich.panel import Panel


console = Console()


def show_welcome():
    console.print(
        Panel(
            "[bold cyan]Course Registration System[/bold cyan]\n"
            "Manage courses, enrollment, cohorts and student progress.",
            title="Welcome",
            border_style="cyan"
        )
    )


def show_main_menu():
    console.print("\n[bold]Main Menu[/bold]")
    console.print("1. Login")
    console.print("2. Register")
    console.print("3. Exit")