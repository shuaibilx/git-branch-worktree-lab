import tempfile
import unittest
from io import StringIO
from pathlib import Path

from tasklab.cli import main


class TaskLabCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.task_file = Path(self.temporary_directory.name) / "tasks.json"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_cli(self, *arguments: str):
        stdout = StringIO()
        stderr = StringIO()
        exit_code = main(
            ["--file", str(self.task_file), *arguments],
            stdout=stdout,
            stderr=stderr,
        )
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_empty_list(self) -> None:
        exit_code, stdout, stderr = self.run_cli("list")

        self.assertEqual(0, exit_code)
        self.assertEqual("No tasks.\n", stdout)
        self.assertEqual("", stderr)

    def test_add_and_list_task(self) -> None:
        exit_code, stdout, _ = self.run_cli("add", "Learn Git branches")
        self.assertEqual(0, exit_code)
        self.assertEqual("Added task 1: Learn Git branches\n", stdout)

        exit_code, stdout, _ = self.run_cli("list")
        self.assertEqual(0, exit_code)
        self.assertEqual("[ ] 1: Learn Git branches\n", stdout)

    def test_complete_task(self) -> None:
        self.run_cli("add", "Practise worktrees")

        exit_code, stdout, stderr = self.run_cli("complete", "1")

        self.assertEqual(0, exit_code)
        self.assertEqual("Completed task 1: Practise worktrees\n", stdout)
        self.assertEqual("", stderr)
        _, stdout, _ = self.run_cli("list")
        self.assertEqual("[x] 1: Practise worktrees\n", stdout)

    def test_complete_unknown_task_returns_error(self) -> None:
        exit_code, stdout, stderr = self.run_cli("complete", "99")

        self.assertEqual(1, exit_code)
        self.assertEqual("", stdout)
        self.assertIn("Task 99 does not exist", stderr)


if __name__ == "__main__":
    unittest.main()
