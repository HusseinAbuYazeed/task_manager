from models import Users, Tasks, Admin
from validators import Validator
from services import login_process, register_process
 
current_user = None
def show_menu() -> None:
    print("\n" + "="*25)
    print("1- Login")
    print("2- Register")
    print("3- Exit")
    print("="*25)


while True:
    show_menu()
    choose = input("choose an option: ").strip()

    if choose == "1":
        print("\nStarting Login Process...")
        login_process()

    elif choose == "2":
        print("\nStarting Register Process...")
        register_process()

    elif choose == "3":
        print("\nExiting... See you later!")
        break
        
    else:
        print("\nInvalid option! Please choose 1, 2, or 3 only.")

