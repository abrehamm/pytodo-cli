import datetime


class Todo:
    def __init__(
        self,
        task: str,
        category: str,
        date_added: str = None,
        date_completed: str = None,
        status: int = None,
        position: int = None,
    ) -> None:
        self.task = task
        self.category = category
        self.date_added = (
            date_added
            if date_added is not None
            else datetime.datetime.now().strftime("%a, %d-%B-%Y %I:%M %p")
        )
        self.date_completed = date_completed if date_added is not None else None
        self.status = (
            status if status is not None else 1
        )  # 1 for 'incompeted' 2 for 'completed'
        self.position = position if position is not None else None

    def __repr__(self) -> str:
        return f"Task: {self.task}, Category: {self.category}, Done: {'✅' if self.status == 2 else '❌'}"
