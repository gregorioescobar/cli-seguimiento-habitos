import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from src.cli import main


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.db = self.tmp.name

    def tearDown(self):
        os.unlink(self.db)

    def run_cli(self, args):
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--db", self.db] + args)
        return code, out.getvalue(), err.getvalue()

    def test_add_list_log_streak_history(self):
        code, out, _ = self.run_cli(["add", "Meditar"])
        self.assertEqual(code, 0)
        self.assertIn("Hábito agregado", out)

        code, out, _ = self.run_cli(["list"])
        self.assertEqual(code, 0)
        self.assertIn("Meditar", out)

        code, out, _ = self.run_cli(["log", "Meditar", "--date", "2026-11-10"])
        self.assertEqual(code, 0)
        code, out, _ = self.run_cli(["log", "Meditar", "--date", "2026-11-11"])
        self.assertEqual(code, 0)

        code, out, _ = self.run_cli(["history", "Meditar"])
        self.assertEqual(code, 0)
        self.assertIn("2026-11-11", out)
        self.assertIn("2026-11-10", out)

        code, out, _ = self.run_cli(["streak", "Meditar"])
        self.assertEqual(code, 0)
        self.assertIn("Racha actual", out)

    def test_error_on_unknown_habit(self):
        code, _, err = self.run_cli(["log", "Nada", "--date", "2026-11-10"])
        self.assertEqual(code, 1)
        self.assertIn("Error", err)

    def test_list_empty(self):
        code, out, _ = self.run_cli(["list"])
        self.assertEqual(code, 0)
        self.assertIn("No hay hábitos", out)


if __name__ == "__main__":
    unittest.main()
