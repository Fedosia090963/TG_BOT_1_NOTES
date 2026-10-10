import csv
import io
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from app.database import Database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "tasks.db"
        self.database = Database(self.database_path)

    def tearDown(self):
        self.database.close()
        self.temp_dir.cleanup()

    def test_create_table_and_add_task(self):
        self.database.init_db()
        task_id = self.database.add_task(
            text="Сделать домашнее задание",
            user="test_user",
        )

        self.assertIsInstance(task_id, int)
        self.assertGreater(task_id, 0)

        tasks = self.database.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["text"], "Сделать домашнее задание")
        self.assertEqual(tasks[0]["user"], "test_user")

    def test_export_tasks_to_csv(self):
        self.database.init_db()
        self.database.add_task("Первая задача", "alice")
        self.database.add_task("Вторая задача", "bob")

        csv_text = self.database.export_tasks_to_csv()
        rows = list(csv.DictReader(io.StringIO(csv_text)))

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["text"], "Первая задача")
        self.assertEqual(rows[1]["user"], "bob")

        self.assertEqual(rows[0]["id"], "1")
        self.assertIn("id,text,user,created_at", csv_text)


if __name__ == "__main__":
    unittest.main()
