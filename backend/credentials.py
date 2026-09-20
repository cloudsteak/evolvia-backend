import random
import string


def generate_credentials():
    username = "tanulo-" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=6)
    )

    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|"

    password_chars = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(symbols),
    ]
    remaining_length = 18 - len(password_chars)
    all_chars = uppercase + lowercase + digits + symbols
    password_chars += random.choices(all_chars, k=remaining_length)
    random.shuffle(password_chars)
    return username, "".join(password_chars)
