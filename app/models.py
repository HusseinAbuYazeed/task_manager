import uuid
from typing import ClassVar

class Users:
    users: ClassVar[dict[str, "Users"]] = {}
    total_users_count: ClassVar[int] = 0

    def __init__(self, user_name: str, email: str, password: str, role: str):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role = role
        self.user_id: str = str(uuid.uuid4())  # to create a uniqe id each time
        self.is_banned: bool = False         
        Users.total_users_count += 1
        Users.users[self.user_id] = self

    # Representation
    def __repr__(self) -> str:
        return f"User(ID: {self.user_id[:8]}..., Name: {self.user_name}, Role: {self.role})"

class Tasks:
    tasks: ClassVar[dict[str, "Tasks"]] = {}

    def __init__(self, user_id: str, task_name: str, task_description: str,completed: bool = False):
        if user_id not in Users.users:
            raise ValueError(f"id: {user_id} not found in memory")

        self.task_id = str(uuid.uuid4())
        self.task_name = task_name
        self.task_description = task_description
        self.completed = completed
        self.user_id = user_id

        Tasks.tasks[self.task_id] = self

    def __repr__(self) -> str:
        status = "done" if self.completed else "not done"
        assigned_user = Users.users[self.user_id]
        return f"Task('{self.task_name}', owner: {assigned_user.user_name}, status: {status})"

class Admin(Users):
    def __init__(self, user_name: str, email: str, password: str) -> None:
        super().__init__(user_name=user_name, email=email, password=password, role="admin")  

def show_menu() -> None:
    print("\n" + "="*25)
    print("1- Login")
    print("2- Register")
    print("3- Exit")
    print("="*25)

