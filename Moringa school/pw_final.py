import string

# Define a set of common weak passwords to check against
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "123456789", "qwerty",
    "admin", "welcome", "password123", "abc123456", "monkey"
]

def check_length(password):
    """Checks if the password is at least 12 characters long."""
    if len(password) >= 12:
        return True, "✔ Password length is sufficient (12+ characters)."
    else:
        return False, "✖ Password should be at least 12 characters long."

def check_case(password):
    """Checks for both uppercase and lowercase characters."""
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    
    if has_upper and has_lower:
        return True, "✔ Password contains both uppercase and lowercase letters."
    elif not has_upper and not has_lower:
        return False, "✖ Password must contain both uppercase and lowercase letters."
    elif not has_upper:
        return False, "✖ Add at least one uppercase letter."
    else:
        return False, "✖ Add at least one lowercase letter."

def check_numbers_special(password):
    """Checks for digits and special characters."""
    has_digit = any(char.isdigit() for char in password)
    special_chars = set(string.punctuation)
    has_special = any(char in special_chars for char in password)
    
    if has_digit and has_special:
        return True, "✔ Password contains both numbers and special characters."
    elif not has_digit and not has_special:
        return False, "✖ Password must include at least one number and one special character."
    elif not has_digit:
        return False, "✖ Add at least one number."
    else:
        return False, "✖ Add at least one special character (e.g., !, @, #, $)."

def check_common_passwords(password):
    """Checks if the password is a commonly used weak password."""
    if password.lower() in COMMON_PASSWORDS:
        return False, "✖ Password is too common and easily guessable."
    return True, "✔ Password is not in the list of common passwords."

def check_password_strength(password):
    """Evaluates the password using all checks and returns feedback."""
    results = []
    
    # Call each function and collect feedback
    length_ok, length_msg = check_length(password)
    case_ok, case_msg = check_case(password)
    num_spec_ok, num_spec_msg = check_numbers_special(password)
    common_ok, common_msg = check_common_passwords(password)

    results.append(length_msg)
    results.append(case_msg)
    results.append(num_spec_msg)
    results.append(common_msg)

    # Determine overall strength
    if all([length_ok, case_ok, num_spec_ok, common_ok]):
        return "Strong password! Good job."
    else:
        return "Weak password. Recommendations:\n" + "\n".join(results)

def main():
    print("=== Password Strength Checker ===")
    
    # Input validation using a while loop
    while True:
        user_password = input("Enter a password to check: ").strip()
        if user_password:
            break
        print("Error: Password cannot be empty. Please enter a valid password.\n")

    # Evaluate password
    feedback = check_password_strength(user_password)
    print("\n" + feedback)

if __name__ == "__main__":
    main()