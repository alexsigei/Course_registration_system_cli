from utils.hashing import hash_password, verify_password


def main():
    password = "secret123"

    salt, password_hash = hash_password(password)

    print("Salt:", salt)
    print("Hash:", password_hash)

    print("Correct password:", verify_password(
        "secret123",
        salt,
        password_hash
    ))

    print("Wrong password:", verify_password(
        "wrongpassword",
        salt,
        password_hash
    ))


if __name__ == "__main__":
    main()