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


def login_process() -> None:
    global current_user
    print("\n--- Login to System ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    found_user = None
    for user_obj in Users.users.values():
        if user_obj.user_name == username and user_obj.password == password:
            found_user = user_obj
            break

    if found_user:
        if found_user.is_banned:
            print("\nLogin Denied: You are banned from this system!")
            return
            
        current_user = found_user
        print(f"Login successful! Welcome back, {current_user.user_name}.")
        
        if current_user.role == "admin":
            admin_panel()
        else:
            user_panel()
    else:
        print("Invalid username or password!")


def admin_panel() -> None:
    global current_user
    while True:
        print(f"\n --- Admin Dashboard [{current_user.user_name}] --- ")
        print("1- Show all users & their tasks")  
        print("2- Ban a user")                    
        print("3- Update user info & reset tasks") 
        print("4- Create and assign a new Task")
        print("5- Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\nCurrent Users and their Tasks:")
            if not Users.users:
                print("No users found in memory.")
            for u in Users.users.values():
                status = "[BANNED]" if u.is_banned else "[Active]"
                print(f"\n{u.user_name} ({u.role}) {status} - ID: {u.user_id[:8]}...")

                user_tasks = [t for t in Tasks.tasks.values() if t.user_id == u.user_id]
                if user_tasks:
                    for idx, task in enumerate(user_tasks, 1):
                        print(f" - Task {idx}: {task.task_name} -> {task.task_description} [Status: {'Done' if task.completed else 'Pending'}]")
                else:
                    print("  - No tasks assigned yet.")

        elif choice == "2":
            target_name = input("Enter username to ban: ").strip()
            found = False
            for u in Users.users.values():
                if u.user_name == target_name:
                    if u.role == "admin":
                        print("Error: You cannot ban another admin!")
                    else:
                        u.is_banned = True
                        print(f"Success: {target_name} has been banned.")
                    found = True
                    break
            if not found:
                print("User not found.")

        elif choice == "3":
            target_name = input("Enter username to update: ").strip()
            user_to_update = None
            for u in Users.users.values():
                if u.user_name == target_name:
                    user_to_update = u
                    break
            
            if user_to_update:
                new_name = input(f"Enter new name (current: {user_to_update.user_name}): ").strip()
                new_email = input(f"Enter new email (current: {user_to_update.email}): ").strip()
                
                if Validator.validate_username(new_name) == True and Validator.validate_email(new_email) == True:
                    user_to_update.user_name = new_name
                    user_to_update.email = new_email
                    
                    tasks_to_remove = [k for k, t in Tasks.tasks.items() if t.user_id == user_to_update.user_id]
                    for k in tasks_to_remove:
                        del Tasks.tasks[k]
                        
                    print(f"Success: {target_name} updated to {new_name} and all tasks were reset!")
                else:
                    print("Update failed due to invalid format rules.")
            else:
                print("User not found.")

        elif choice == "4":
            target_name = input("Enter username to assign task to: ").strip()
            target_user = next((u for u in Users.users.values() if u.user_name == target_name), None)
            if target_user:
                t_name = input("Task title: ")
                t_desc = input("Task description: ")
                Tasks(user_id=target_user.user_id, task_name=t_name, task_description=t_desc, completed=False)
                print(f"Task assigned to {target_name}!")
            else:
                print("User not found.")

        elif choice == "5":
            current_user = None
            print("Logged out from Admin Dashboard.")
            break


def user_panel() -> None:
    global current_user
    while True:
        print(f"\n--- User Panel [{current_user.user_name}] ---")
        print("1- Show my profile info")
        print("2- View my tasks")
        print("3- Create a new task")
        print("4- Mark a task as completed")
        print("5- Update a task info")
        print("6- Logout")
        choice = input("Choose an option: ").strip()

        my_tasks = [t for t in Tasks.tasks.values() if t.user_id == current_user.user_id]

        if choice == "1":
            print(f"\nYour Profile Info: Name: {current_user.user_name} | Email: {current_user.email} | Role: {current_user.role}")

        elif choice == "2":
            print("\n--- My Tasks ---")
            if my_tasks:
                for idx, t in enumerate(my_tasks, 1):
                    status = "Completed" if t.completed else "Pending"
                    print(f"[{idx}] Title: {t.task_name} | Status: {status}")
                    print(f"    Description: {t.task_description}")
            else:
                print("You have no tasks.")

        elif choice == "3":
            print("\n--- Create New Task ---")
            t_name = input("Enter task title: ").strip()
            t_desc = input("Enter task description: ").strip()
            Tasks(user_id=current_user.user_id, task_name=t_name, task_description=t_desc, completed=False)
            print("Task created successfully!")

        elif choice == "4":
            print("\n--- Mark Task as Completed ---")
            if not my_tasks:
                print("You have no tasks to complete.")
                continue
                
            for idx, t in enumerate(my_tasks, 1):
                status = "Done" if t.completed else "Pending"
                print(f"{idx}- {t.task_name} [{status}]")
                
            task_idx_str = input("Select the task number to mark as done: ").strip()
            if task_idx_str.isdigit():
                task_idx = int(task_idx_str) - 1
                if 0 <= task_idx < len(my_tasks):
                    my_tasks[task_idx].completed = True
                    print(f"Success: '{my_tasks[task_idx].task_name}' is now marked as completed!")
                else:
                    print("Invalid task number.")
            else:
                print("Please enter a valid numeric input.")

        elif choice == "5":
            print("\n--- Update Task Info ---")
            if not my_tasks:
                print("You have no tasks to update.")
                continue
                
            for idx, t in enumerate(my_tasks, 1):
                print(f"{idx}- {t.task_name}")
                
            task_idx_str = input("Select the task number to update: ").strip()
            if task_idx_str.isdigit():
                task_idx = int(task_idx_str) - 1
                if 0 <= task_idx < len(my_tasks):
                    selected_task = my_tasks[task_idx]
                    new_title = input(f"Enter new title (Current: {selected_task.task_name}): ").strip()
                    new_desc = input(f"Enter new description (Current: {selected_task.task_description}): ").strip()
                    
                    if new_title:
                        selected_task.task_name = new_title
                    if new_desc:
                        selected_task.task_description = new_desc
                        
                    print("Task updated successfully!")
                else:
                    print("Invalid task number.")
            else:
                print("Please enter a valid numeric input.")

        elif choice == "6":
            current_user = None
            print("Logged out from User Panel.")
            break
        else:
            print("Invalid option!")
