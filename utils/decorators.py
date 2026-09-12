from functools import wraps


def login_required(function):
    @wraps(function)
    def wrapper(auth_service, *args, **kwargs):
        if auth_service.get_current_user() is None:
            raise PermissionError("You must be logged in to perform this action.")

        return function(auth_service, *args, **kwargs)

    return wrapper


def role_required(required_role):
    def decorator(function):
        @wraps(function)
        def wrapper(auth_service, *args, **kwargs):
            current_user = auth_service.get_current_user()

            if current_user is None:
                raise PermissionError("You must be logged in.")

            if current_user.role != required_role:
                raise PermissionError(
                    f"Access denied. {required_role} role required."
                )

            return function(auth_service, *args, **kwargs)

        return wrapper

    return decorator