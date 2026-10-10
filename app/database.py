"""Модуль работы с базой SQLite для хранения задач."""

import csv
import io
import sqlite3
from pathlib import Path
from typing import Any


class Database:
    """Небольшой слой для чтения и записи задач."""

    def __init__(self, database_path: str | Path = "tasks.db"):
        self.database_path = Path(database_path)
        self.connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        """Создаёт соединение с базой данных."""
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self) -> None:
        """Закрывает соединение при завершении работы."""
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def init_db(self) -> None:
        """Создаёт таблицу, если она ещё не существует."""
        connection = self.connect()
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.commit()
        self.close()

    def add_task(self, text: str, user: str) -> int:
        """Добавляет новую задачу и возвращает её идентификатор."""
        if not text.strip():
            raise ValueError("Текст задачи не может быть пустым.")

        connection = self.connect()
        cursor = connection.execute(
            """
            INSERT INTO tasks (text, user, created_at)
            VALUES (?, ?, datetime('now', 'localtime'))
            """,
            (text.strip(), user),
        )
        connection.commit()
        task_id = cursor.lastrowid
        self.close()
        return task_id

    def get_all_tasks(self) -> list[dict[str, Any]]:
        """Возвращает все задачи в порядке создания."""
        connection = self.connect()
        rows = connection.execute(
            "SELECT id, text, user, created_at FROM tasks ORDER BY id"
        ).fetchall()
        self.close()
        return [dict(row) for row in rows]

    def export_tasks_to_csv(self) -> str:
        """Формирует содержимое CSV-таблицы со всеми задачами."""
        tasks = self.get_all_tasks()
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=["id", "text", "user", "created_at"],
        )
        writer.writeheader()
        writer.writerows(tasks)
        return output.getvalue()
