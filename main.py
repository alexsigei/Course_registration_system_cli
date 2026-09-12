from services.auth_service import AuthService


def main():
    auth = AuthService()

    try:
        auth.view_profile()

    except PermissionError as error:
        print("Before login:", error)

    # Login existing student
    try:
        user = auth.login(
            email="alex@example.com",
            password="secret123"
        )

        print("Logged in as:", user)
        print("Role:", user.role)

    except ValueError as error:
        print("Login error:", error)
        return

    print()

    # Test login_required
    try:
        profile = auth.view_profile()
        print("Profile access:", profile)

    except PermissionError as error:
        print("Permission error:", error)

    print()

    # Test admin access
    try:
        result = auth.admin_action()
        print(result)

    except PermissionError as error:
        print("Admin access:", error)


if __name__ == "__main__":
    main()