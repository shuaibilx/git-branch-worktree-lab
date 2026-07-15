"""Command-line interface for TaskLab."""

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence, TextIO

from tasklab.store import TaskStore, TaskStoreError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tasklab",
        description="Manage a small local task list.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("tasks.json"),
        help="JSON file used to store tasks (default: tasks.json)",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add", help="Add a task")
    add_parser.add_argument("title", help="Task title")

    commands.add_parser("list", help="List tasks")

    complete_parser = commands.add_parser("complete", help="Complete a task")
    complete_parser.add_argument("task_id", type=int, help="Numeric task ID")
    return parser


def main(
    argv: Optional[Sequence[str]] = None,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> int:
    args = build_parser().parse_args(argv)
    store = TaskStore(args.file)

    try:
        if args.command == "add":
            task = store.add(args.title)
            print(f"Added task {task['id']}: {task['title']}", file=stdout)
            return 0

        if args.command == "list":
            tasks = store.list_tasks()
            if not tasks:
                print("No tasks.", file=stdout)
                return 0
            for task in tasks:
                marker = "x" if task.get("completed") else " "
                print(f"[{marker}] {task['id']}: {task['title']}", file=stdout)
            return 0

        task = store.complete(args.task_id)
        print(f"Completed task {task['id']}: {task['title']}", file=stdout)
        return 0
    except TaskStoreError as exc:
        print(f"error: {exc}", file=stderr)
        return 1


def entrypoint() -> None:
    raise SystemExit(main())
