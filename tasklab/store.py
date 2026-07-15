"""JSON-backed storage for TaskLab."""

import json
from pathlib import Path
from typing import Dict, List


Task = Dict[str, object]


class TaskStoreError(RuntimeError):
    """Raised when the task file cannot be read safely."""


class TaskStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list_tasks(self) -> List[Task]:
        if not self.path.exists():
            return []

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TaskStoreError(f"Cannot read task file: {self.path}") from exc

        if not isinstance(data, list):
            raise TaskStoreError(f"Task file must contain a JSON list: {self.path}")
        return data

    def add(self, title: str) -> Task:
        tasks = self.list_tasks()
        task: Task = {
            "id": max((int(item["id"]) for item in tasks), default=0) + 1,
            "title": title,
            "completed": False,
        }
        tasks.append(task)
        self._save(tasks)
        return task

    def complete(self, task_id: int) -> Task:
        tasks = self.list_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                task["completed"] = True
                self._save(tasks)
                return task
        raise TaskStoreError(f"Task {task_id} does not exist")

    def _save(self, tasks: List[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(tasks, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
