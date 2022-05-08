import datetime
import pytest
from typer.testing import CliRunner

from pytodo_cli import app

my_runner = CliRunner()


def test_app_with_no_args():
    result = my_runner.invoke(app)
    assert result.exit_code == 0


def test_show_all_with_no_data():
    result = my_runner.invoke(app, ["show"])
    assert result.exit_code == 0
    assert "No todo items are stored yet." in result.stdout


def test_show_single_with_no_data():
    result = my_runner.invoke(app, ["show", "3"])
    assert result.exit_code == 0
    assert "No todo item found for supplied position index: #3" in result.stdout


def test_add():
    result = my_runner.invoke(app, ["add", "Test", "pytest"])
    assert result.exit_code == 0
    assert (
        "│ 1      │ Test                 │       pytest │              ❌ │"
        in result.stdout
    )


def test_show_single_with_data():
    result = my_runner.invoke(app, ["show", "1"])
    assert result.exit_code == 0
    date_added_formatted = (
        f"{datetime.datetime.now().strftime('%a, %d-%B-%Y %I:%M %p')}"
    )
    assert date_added_formatted in result.stdout


def test_complete():
    result = my_runner.invoke(app, ["complete", "1"])
    assert result.exit_code == 0
    assert "✅ │" in result.stdout


def test_update():
    result = my_runner.invoke(app, ["update", "1", "--task=Tested"])
    assert result.exit_code == 0


def test_delete():
    result = my_runner.invoke(app, ["delete", "1"])
    assert result.exit_code == 0
