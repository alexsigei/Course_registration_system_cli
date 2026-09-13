from services.auth_service import AuthService
from cli.menu import show_welcome, show_main_menu
from cli.auth_cli import get_login_details, get_registration_details
from cli.student_cli import show_student_menu
from cli.admin_cli import show_admin_menu


def main():
    auth = AuthService()

    show_welcome()

    while True:
        show_main_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            email, password = get_login_details()

            try:
                user = auth.login(email, password)

                print(
                    f"\nLogin successful. Welcome, {user.name}!"
                )

                if user.role == "student":
                    show_student_menu(user)

                elif user.role == "admin":
                    show_admin_menu(user)

                auth.logout()

            except ValueError as error:
                print(
                    f"\nLogin failed: {error}"
                )

        elif choice == "2":
            name, email, password = get_registration_details()

            try:
                user = auth.register_student(
                    name=name,
                    email=email,
                    password=password
                )

                print(
                    f"\nAccount created for {user.name}."
                )

                print(
                    f"Your student ID is {user.student_id}."
                )

            except ValueError as error:
                print(
                    f"\nRegistration failed: {error}"
                )

        elif choice == "3":
            print("\nGoodbye!")
            break

        else:
            print(
                "\nInvalid choice. "
                "Please select 1, 2 or 3."
            )


if __name__ == "__main__":
    main()

