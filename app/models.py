import uuid
from typing import ClassVar


class User:
    def __init__(self, user_name: str, email: str, password: str, role: str):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role = role
        self.user_id: str = str(uuid.uuid4())
        self.is_banned: bool = False

    def __repr__(self) -> str:
        return f"User(ID: {self.user_id[:8]}..., Name: {self.user_name}, Role: {self.role})"


class Task:
    def __init__(self, user_id: str, task_name: str, task_description: str, completed: bool = False):
        self.user_id = user_id
        self.task_id = str(uuid.uuid4())
        self.task_name = task_name
        self.task_description = task_description
        self.completed = completed

    def __repr__(self) -> str:
        status = "done" if self.completed else "not done"
        return f"Task('{self.task_name}', owner_id: {self.user_id[:8]}..., status: {status})"


class UserRepository:
    def __init__(self):
        self._users: dict[str, User] = {}
        self._total_count: int = 0

    def add(self, user: User) -> None:
        self._users[user.user_id] = user
        self._total_count += 1

    def get_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def get_by_username(self, username: str) -> User | None:
        for user in self._users.values():
            if user.user_name == username:
                return user
        return None

    def get_all(self) -> list[User]:
        return list(self._users.values())

    def update(self, user_id: str, user: User) -> bool:
        if user_id in self._users:
            self._users[user_id] = user
            return True
        return False

    def delete(self, user_id: str) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            self._total_count -= 1
            return True
        return False

    def exists(self, user_id: str) -> bool:
        return user_id in self._users

    def total_users(self) -> int:
        return self._total_count


class TaskRepository:
    def __init__(self):
        self._tasks: dict[str, Task] = {}

    def add(self, task: Task) -> None:
        self._tasks[task.task_id] = task

    def get_by_id(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def get_by_user(self, user_id: str) -> list[Task]:
        return [task for task in self._tasks.values() if task.user_id == user_id]

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, task_id: str, task: Task) -> bool:
        if task_id in self._tasks:
            self._tasks[task_id] = task
            return True
        return False

    def delete(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def delete_by_user(self, user_id: str) -> int:
        tasks_to_delete = [task_id for task_id, task in self._tasks.items() if task.user_id == user_id]
        for task_id in tasks_to_delete:
            del self._tasks[task_id]
        return len(tasks_to_delete)

    def exists(self, task_id: str) -> bool:
        return task_id in self._tasks