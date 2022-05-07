import datetime
import sqlite3
from tkinter.messagebox import RETRY
from typing import List, Tuple

from model import Todo

conn = sqlite3.connect("todos.db")
cursor = conn.cursor()


def create_table():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS todos 
        (
            task text, 
            category text, 
            date_added text, 
            date_completed text, 
            status integer, 
            position integer
        )
        """
    )


create_table()


def insert_todo(todo: Todo) -> None:
    cursor.execute("SELECT COUNT(*) FROM todos")
    count = cursor.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        cursor.execute(
            "INSERT INTO todos VALUES(:task, :category, :date_added, :date_completed, :status, :position)",
            {
                "task": todo.task,
                "category": todo.category,
                "date_added": todo.date_added,
                "date_completed": todo.date_completed,
                "status": todo.status,
                "position": todo.position,
            },
        )


def get_all_todos() -> List[Todo]:
    cursor.execute("SELECT * FROM todos")
    results = cursor.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos


def get_single_todo(position: int) -> Todo:
    cursor.execute(
        "SELECT * FROM todos WHERE position = :position", {"position": position}
    )
    result = cursor.fetchone()
    if result:
        todo = Todo(*result)
        return todo
    return None


def delete_todo(position: int) -> Tuple[bool, str]:
    cursor.execute("SELECT COUNT(*) FROM todos")
    count = cursor.fetchone()[0]
    if count == 0:
        return False, "no_items"
    with conn:
        cursor.execute(
            "DELETE FROM todos WHERE position=:position", {"position": position}
        )
        if cursor.rowcount == 0:
            return False, "not_found"
        for pos in range(position + 1, count):
            change_position(pos, pos - 1, False)
    return True, "ok"


def change_position(old_position: int, new_position: int, commit: bool = False) -> None:
    cursor.execute(
        "UPDATE todos SET position = :new_position WHERE position = :old_position",
        {"old_position": old_position, "new_position": new_position},
    )
    if commit:
        conn.commit()


def update_todo(position: int, task: str, category: str) -> Tuple[bool, str]:
    with conn:
        if task is not None and category is not None:
            cursor.execute(
                "UPDATE todos SET task = :task, category = :category WHERE position = :position",
                {"position": position, "task": task, "category": category},
            )
        elif task is not None:
            cursor.execute(
                "UPDATE todos SET task = :task WHERE position = :position",
                {"position": position, "task": task},
            )
        elif category is not None:
            cursor.execute(
                "UPDATE todos SET category = :category WHERE position = :position",
                {"position": position, "category": category},
            )
    if cursor.rowcount == 0:
        return False, "not_found"
    elif cursor.rowcount == -1:
        return False, "no_args"
    conn.commit()
    return True, "ok"


def complete_todo(position: int) -> bool:
    cursor.execute(
        "UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position",
        {
            "date_completed": datetime.datetime.now().strftime("%a, %d-%B-%Y %I:%M %p"),
            "position": position,
        },
    )
    if cursor.rowcount > 0:
        conn.commit()
        return True
    else:
        return False
