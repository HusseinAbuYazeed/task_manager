from models import Users, Tasks, Admin
from validators import Validator

current_user = None

def register_process() -> None:
    print("\n--- Register New Account ---")
    
    username = input("Enter username: ").strip()
    username_valid = Validator.validate_username(username)
    if username_valid != True:
        print(f"Error: {username_valid}")
        return

    email = input("Enter email: ").strip()
    email_valid = Validator.validate_email(email)
    if email_valid != True:
        print(f"Error: {email_valid}")
        return

    password = input("Enter password: ").strip()
    password_valid = Validator.validate_password(password)
    if password_valid != True:
        print(f"Error {password_valid}")
        return
    
    print("\nChoose account type:")
    print("1. Normal User")
    print("2. Admin")
    role_choice = input("Your choice: ").strip()

    if role_choice == "2":
        Admin(user_name=username, email=email, password=password)
        print(f"Admin '{username}' registered successfully!")
    else:
        Users(user_name=username, email=email, password=password, role="user")
        print(f"Normal User '{username}' registered successfully!")

def login(username: str, password: str) -> Users:
    for user in Users.users.values():
        if user.user_name == username and user.password == password:
            if user.is_banned:
                raise ValueError("User is banned")

            return user

    raise ValueError("Invalid username or password")