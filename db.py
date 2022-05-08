import datetime
import sqlite3
from typing import List, Tuple

from model import Todo


class Database:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
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

    def insert_todo(self, todo: Todo) -> None:
        self.cursor.execute("SELECT COUNT(*) FROM todos")
        count = self.cursor.fetchone()[0]
        todo.position = count if count else 0
        with self.conn:
            self.cursor.execute(
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

    def get_all_todos(self) -> List[Todo]:
        self.cursor.execute("SELECT * FROM todos")
        results = self.cursor.fetchall()
        todos = []
        for result in results:
            todos.append(Todo(*result))
        return todos

    def get_single_todo(self, position: int) -> Todo:
        self.cursor.execute(
            "SELECT * FROM todos WHERE position = :position", {"position": position}
        )
        result = self.cursor.fetchone()
        if result:
            todo = Todo(*result)
            return todo
        return None

    def delete_todo(self, position: int) -> Tuple[bool, str]:
        self.cursor.execute("SELECT COUNT(*) FROM todos")
        count = self.cursor.fetchone()[0]
        if count == 0:
            return False, "no_items"
        with self.conn:
            self.cursor.execute(
                "DELETE FROM todos WHERE position=:position", {"position": position}
            )
            if self.cursor.rowcount == 0:
                return False, "not_found"
            for pos in range(position + 1, count):
                self.change_position(pos, pos - 1, False)
        return True, "ok"

    def change_position(
        self, old_position: int, new_position: int, commit: bool = False
    ) -> None:
        self.cursor.execute(
            "UPDATE todos SET position = :new_position WHERE position = :old_position",
            {"old_position": old_position, "new_position": new_position},
        )
        if commit:
            self.conn.commit()

    def update_todo(self, position: int, task: str, category: str) -> Tuple[bool, str]:
        with self.conn:
            if task is not None and category is not None:
                self.cursor.execute(
                    "UPDATE todos SET task = :task, category = :category WHERE position = :position",
                    {"position": position, "task": task, "category": category},
                )
            elif task is not None:
                self.cursor.execute(
                    "UPDATE todos SET task = :task WHERE position = :position",
                    {"position": position, "task": task},
                )
            elif category is not None:
                self.cursor.execute(
                    "UPDATE todos SET category = :category WHERE position = :position",
                    {"position": position, "category": category},
                )
        if self.cursor.rowcount == 0:
            return False, "not_found"
        elif self.cursor.rowcount == -1:
            return False, "no_args"
        self.conn.commit()
        return True, "ok"

    def complete_todo(self, position: int) -> bool:
        self.cursor.execute(
            "UPDATE todos SET status = 2, date_completed = :date_completed WHERE position = :position",
            {
                "date_completed": datetime.datetime.now().strftime(
                    "%a, %d-%B-%Y %I:%M %p"
                ),
                "position": position,
            },
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        else:
            return False
