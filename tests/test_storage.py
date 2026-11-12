import os
import tempfile
import unittest
from datetime import date

from src.storage import (
    add_habit,
    get_connection,
    get_history,
    get_streak,
    init_db,
    list_habits,
    log_habit,
)


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.conn = get_connection(self.tmp.name)
        init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        os.unlink(self.tmp.name)

    def test_add_and_list_habits(self):
        add_habit(self.conn, "Leer")
        add_habit(self.conn, "Ejercicio")
        names = [h["name"] for h in list_habits(self.conn)]
        self.assertEqual(names, ["Ejercicio", "Leer"])

    def test_duplicate_habit(self):
        add_habit(self.conn, "Leer")
        with self.assertRaises(ValueError):
            add_habit(self.conn, "leer")

    def test_log_and_history(self):
        add_habit(self.conn, "Leer")
        log_habit(self.conn, "Leer", "2026-11-10")
        log_habit(self.conn, "Leer", "2026-11-11")
        self.assertEqual(get_history(self.conn, "Leer"), ["2026-11-11", "2026-11-10"])

    def test_duplicate_log_same_day(self):
        add_habit(self.conn, "Leer")
        log_habit(self.conn, "Leer", "2026-11-10")
        with self.assertRaises(ValueError):
            log_habit(self.conn, "Leer", "2026-11-10")

    def test_streak_current_ending_today(self):
        add_habit(self.conn, "Leer")
        for d in ["2026-11-10", "2026-11-11", "2026-11-12"]:
            log_habit(self.conn, "Leer", d)
        self.assertEqual(get_streak(self.conn, "Leer", today=date(2026, 11, 12)), 3)

    def test_streak_current_ending_yesterday(self):
        add_habit(self.conn, "Leer")
        for d in ["2026-11-10", "2026-11-11"]:
            log_habit(self.conn, "Leer", d)
        self.assertEqual(get_streak(self.conn, "Leer", today=date(2026, 11, 12)), 2)

    def test_streak_broken(self):
        add_habit(self.conn, "Leer")
        for d in ["2026-11-09", "2026-11-11"]:
            log_habit(self.conn, "Leer", d)
        self.assertEqual(get_streak(self.conn, "Leer", today=date(2026, 11, 12)), 1)

    def test_log_unknown_habit(self):
        with self.assertRaises(ValueError):
            log_habit(self.conn, "NoExiste", "2026-11-10")


if __name__ == "__main__":
    unittest.main()
