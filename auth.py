from helpers import profile


def main():
    user_profile = profile()
    user_name = user_profile["display_name"]
    print(
        f"{user_name} authenticated successfully!\nNow run python app.py to get started."
    )


if __name__ == "__main__":
    main()
