import sys

def check_password_strength(password):
    if len(password) < 6:
        return "Weak password: Too short"
    elif not any(char.isdigit() for char in password):
        return "Weak password: Add some numbers"
    elif not any(char.isupper() for char in password):
        return "Weak password: Add some uppercase letters"
    else:
        return "Strong password"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        password = sys.argv[1]
        print(check_password_strength(password))
    else:
        print("No password provided")