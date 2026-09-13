import re


def validate_email(email):
    email = email.strip()

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):
        raise ValueError("Please enter a valid email address.")

    return email


def validate_name(name):
    name = name.strip()

    if not name:
        raise ValueError("Name cannot be empty.")

    if len(name) < 2:
        raise ValueError("Name must contain at least 2 characters.")

    return name


def validate_password(password):
    if len(password) < 6:
        raise ValueError(
            "Password must contain at least 6 characters."
        )

    return password


def validate_score(score):
    try:
        score = float(score)
    except ValueError:
        raise ValueError("Score must be a number.")

    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")

    return score


def validate_capacity(capacity):
    try:
        capacity = int(capacity)
    except ValueError:
        raise ValueError("Capacity must be a whole number.")

    if capacity <= 0:
        raise ValueError(
            "Capacity must be greater than 0."
        )

    return capacity


def validate_pass_mark(pass_mark):
    try:
        pass_mark = float(pass_mark)
    except ValueError:
        raise ValueError("Pass mark must be a number.")

    if pass_mark < 0 or pass_mark > 100:
        raise ValueError(
            "Pass mark must be between 0 and 100."
        )

    return pass_mark