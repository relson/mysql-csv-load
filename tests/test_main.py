import csv
import tempfile
import unittest
from pathlib import Path

from mysql_csv_load.main import import_csv


class FakeCursor:
    def __init__(self):
        self.executed = []
        self.batches = []

    def execute(self, query):
        self.executed.append(query)

    def executemany(self, query, rows):
        self.batches.append((query, list(rows)))


class FakeConnection:
    def __init__(self):
        self.commits = 0

    def commit(self):
        self.commits += 1


class ImportCsvTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_file = Path(self.temp_dir.name) / "records.csv"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_csv(self, rows):
        with self.csv_file.open("w", encoding="utf-8", newline="") as file:
            csv.writer(file).writerows(rows)

    def test_imports_streamed_batches_and_quotes_identifiers(self):
        self.write_csv(
            [
                ["id", "select", "odd`name"],
                ["1", "a", ""],
                ["2", "b", "value"],
                ["3", "c", "value"],
                ["4", "d", "value"],
                ["5", "e", "value"],
            ]
        )
        cursor = FakeCursor()
        connection = FakeConnection()

        imported = import_csv(self.csv_file, "records`table", cursor, connection, 2)

        self.assertEqual(imported, 5)
        self.assertEqual(connection.commits, 4)
        self.assertEqual(
            cursor.executed,
            [
                "CREATE TABLE IF NOT EXISTS `records``table` "
                "(`id` TEXT, `select` TEXT, `odd``name` TEXT)"
            ],
        )
        self.assertEqual([len(batch) for _, batch in cursor.batches], [2, 2, 1])
        self.assertEqual(cursor.batches[0][1][0], ("1", "a", ""))

    def test_rejects_rows_with_wrong_number_of_columns(self):
        self.write_csv([["id", "name"], ["1", "first"], ["2"]])
        cursor = FakeCursor()
        connection = FakeConnection()

        with self.assertRaisesRegex(ValueError, "record 3"):
            import_csv(self.csv_file, "records", cursor, connection, 1)

        self.assertEqual(connection.commits, 2)
        self.assertEqual(len(cursor.batches), 1)

    def test_rejects_duplicate_column_names(self):
        self.write_csv([["id", "id"], ["1", "2"]])
        cursor = FakeCursor()
        connection = FakeConnection()

        with self.assertRaisesRegex(ValueError, "duplicate"):
            import_csv(self.csv_file, "records", cursor, connection, 1)

        self.assertEqual(cursor.executed, [])


if __name__ == "__main__":
    unittest.main()
