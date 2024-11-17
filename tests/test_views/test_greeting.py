from datetime import datetime

from src.views import greeting


def test_morning(freezer):
    for i in range(4, 12):
        date = datetime(2024, 11, 11, i, 00, 00)
        freezer.move_to(date)
        assert greeting() == "Доброе утро"


def test_day(freezer):
    for i in range(12, 16):
        date = datetime(2024, 11, 11, i, 00, 00)
        freezer.move_to(date)
        assert greeting() == "Добрый день"


def test_evening(freezer):
    for i in range(16, 23):
        date = datetime(2024, 11, 11, i, 00, 00)
        freezer.move_to(date)
        assert greeting() == "Добрый вечер"


def test_night(freezer):
    for i in range(0, 4):
        date = datetime(2024, 11, 11, i, 00, 00)
        freezer.move_to(date)
        assert greeting() == "Доброй ночи"
