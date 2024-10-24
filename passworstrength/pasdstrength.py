import re

def password_strength(password):
    points = 0
    total_points = 4

    # Check length
    if len(password) >= 8:
        points += 1
    else:
        print("Password is invalid due to length.")

    # Check for symbols
    if len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password)) > 2:
        points += 1

    # Check for numbers
    if len(re.findall(r'[0-9]', password)) > 2:
        points += 1

    # Check for both uppercase and lowercase
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        points += 1

    print(f"Password strength: {points}/{total_points}")

# Example usage
password = input("Enter a password to check its strength: ")
password_strength(password)