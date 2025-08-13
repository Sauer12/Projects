import string
import random

print("Welcome to the password generator v0.1!")

while True:
    while True:
        #length of password
        try:
            size_of_password = int(input("Enter the size of the password [7-100]: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if 6 < size_of_password <= 100:
            break
        else:
            print("Invalid size of the password!")

    types = []

    #special chars
    is_special_characters = input("Do you want the password to contain special characters? [y/n]: ").lower()
    if is_special_characters == "y":
        types.append("special")

    #uppercase letters
    is_uppercase_letters = input("Do you want the password to contain capital letters? [y/n]: ").lower()
    if is_uppercase_letters == "y":
        types.append("upper")

    #lower letters
    is_lowercase_letters = input("Do you want the password to contain lower letters? [y/n]: ").lower()
    if is_lowercase_letters == "y":
        types.append("lower")

    #digits
    is_digits = input("Do you want the password to contain numbers? [y/n]: ").lower()
    if is_digits == "y":
        types.append("digits")

    if not types:
        print("At least one character type must be selected")
        continue

    #generator
    lower_letters = "abcdefghijklmnopqrstuvwxyz"
    upper_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    special_symbols = string.punctuation
    password = ""

    for i in range(size_of_password):
        t = random.choice(types)
        if t == "special":
            password += random.choice(special_symbols)
        elif t == "upper":
            password += random.choice(upper_letters)
        elif t == "lower":
            password += random.choice(lower_letters)
        else:
            password += random.choice(digits)

    print(f"Your new generated password is: {password}")
    save = input("\nDo you want to save a password to the file? [y/n]").lower()

    from datetime import datetime
    filename = "password_log.txt"
    if save == "y":
        with open(filename, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} - {password}\n")

    is_next = input("\nDo you want the password again? [y/n]: ").lower()
    if is_next != "y":
        break

print("Goodbye!")

