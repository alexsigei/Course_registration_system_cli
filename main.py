from services.auth_service import AuthService


def main():
    auth = AuthService()

    try:
        user = auth.register(
            name="Alex",
            email="alex@example.com",
            password="secret123"
        )

        print("Registered:")
        print(user)
        print(user.to_dict())

    except ValueError as error:
        print("Registration error:", error)

    print()

    try:
        logged_in_user = auth.login(
            email="alex@example.com",
            password="secret123"
        )

        print("Login successful:")
        print(logged_in_user)
        print("Current user:", auth.get_current_user())

    except ValueError as error:
        print("Login error:", error)


if __name__ == "__main__":
    main()