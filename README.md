# Git Branch & Worktree Lab

这是一个用于真实练习 Git branch、worktree、GitHub Pull Request 和 Codex
并行任务的小型 Python CLI 项目。它把任务保存在本地 JSON 文件中，不需要数据库或第三方运行时依赖。

## 本地使用

项目需要 Python 3.9 或更高版本。

```powershell
python -m pip install --editable .
tasklab add "学习 Git branch"
tasklab list
tasklab complete 1
```

也可以不安装，直接从仓库运行：

```powershell
python -m tasklab add "练习 worktree"
python -m tasklab list
python -m tasklab complete 1
```

默认数据文件是仓库当前目录下的 `tasks.json`，该文件已被 Git 忽略。可以通过
`--file` 指定其他位置：

```powershell
python -m tasklab --file .\demo-tasks.json list
```

## 运行测试

```powershell
python -m unittest discover --start-directory tests --verbose
```

## 练习工作流

本仓库采用 `main` 作为默认分支。日常工作使用 `feature/`、`fix/`、`docs/`
分支；Codex 独立任务使用 `codex/` 前缀。初始提交完成后，功能开发统一经过：

```text
任务 → 分支或 worktree → 测试 → 提交 → 推送 → PR → 检查 → 合并 → 清理
```
