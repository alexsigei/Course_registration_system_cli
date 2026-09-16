from rich.console import Console


console = Console()


def get_login_details():
    console.print("\n[bold cyan]Login[/bold cyan]")

    email = console.input("Email: ")
    password = console.input("Password: ")

    return email, password


def get_registration_details():
    console.print(
        "\n[bold cyan]Create Account[/bold cyan]"
    )

    name = console.input("Name: ")
    email = console.input("Email: ")
    password = console.input("Password: ")

    return (
        name,
        email,
        password
    )
