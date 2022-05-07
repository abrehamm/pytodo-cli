from typing import Optional
from rich.console import Console
from rich.table import box, Table
import typer

from db import (
    delete_todo,
    get_all_todos,
    get_single_todo,
    insert_todo,
    update_todo,
    complete_todo,
)
from model import Todo


def callback():
    """
    A simple but functional ToDo app... here on the terminal.
    """


app = typer.Typer(callback=callback, no_args_is_help=True)
console = Console()


@app.command(short_help="add a new todo item")
def add(task: str, category: str):
    todo = Todo(task=task, category=category)
    console.print(f"[bold green]Adding new todo -> {todo}[/bold green]")
    insert_todo(todo)
    show(None)


@app.command(short_help="delete a todo item")
def delete(position: int):
    op_status, msg = delete_todo(position=position - 1)
    if op_status:
        console.print(f"[bold cyan]Deleted todo #{position}[/bold cyan]")
        show(None)
    else:
        if msg == "no_items":
            console.print(f"[bold red]No todo items are stored yet.[/bold red]")
        elif msg == "not_found":
            console.print(
                f"[bold red]No todo item found for supplied position index: #{position}.[/bold red]"
            )


@app.command(short_help="update a todo item")
def update(
    position: int,
    task: str = typer.Option(None, help="new name of the task to be updated"),
    category: str = typer.Option(None, help="new category of the task to be updated"),
):
    op_status, msg = update_todo(position=position - 1, task=task, category=category)
    if op_status:
        console.print(f"[bold cyan]Updated todo #{position}[/bold cyan]")
        show(None)
    else:
        if msg == "no_args":
            console.print(
                f"[bold red]No value is provded to either Task or Category of the todo.[/bold red]"
            )
        elif msg == "not_found":
            console.print(
                f"[bold red]No todo item found for supplied position index: #{position}.[/bold red]"
            )


@app.command(short_help="mark a todo item as completed")
def complete(position: int):
    op_satus = complete_todo(position=position - 1)
    if not op_satus:
        console.print(
            f"[bold red]No todo item found for supplied position index: #{position}.[/bold red]"
        )
    else:
        show(None)


@app.command(short_help="show all todos")
def show(position: Optional[int] = typer.Argument(None)):

    if position is None:
        todos = get_all_todos()
        table = Table(title="Todos 🎯", show_header=True, header_style="bold blue")
        table.add_column("#", style="dim", width=6)
        table.add_column("Task", min_width=20)
        table.add_column("Category", min_width=12, justify="right")
        table.add_column("Done", min_width=15, justify="right")

        for todo in todos:
            is_done_emoji = "✅" if todo.status == 2 else "❌"
            table.add_row(
                str(todo.position + 1), todo.task, todo.category, is_done_emoji
            )
        console.print(table)
    else:
        todo = get_single_todo(position=position - 1)
        if todo:
            table = Table(
                title=f"{todo.task}",
                show_header=False,
                header_style=None,
                box=box.HORIZONTALS,
            )
            table.add_column(style="dim")
            table.add_column(style="cyan")
            for key, val in todo.__dict__.items():
                if key == "position":
                    val = int(val) + 1
                if key == "status":
                    val = "✅" if val == 2 else "❌"
                table.add_row(key.replace("_", " ").capitalize(), str(val))
            console.print(table)
        else:
            console.print(
                f"[bold red]No todo item found for supplied position index: #{position}[/bold red]"
            )


if __name__ == "__main__":
    app()
