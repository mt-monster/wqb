# -*- coding: utf-8 -*-
"""GEM 子进程 / CSV / 文件工具层。

2026-09-12 从 run_pipeline.py 拆出。

兼容性注意：headless_runner/run.py 通过替换 `run_pipeline.run_script`
拦截 fetch_dataset.py 的调用（进程内构建 dataframe 替代子进程）。
调用方必须经 run_pipeline 模块全局名（裸名）调用才能被 monkey-patch 拦截；
本模块提供原始实现。
"""
import csv
import shutil
import subprocess
from pathlib import Path


def load_dataset_ids_from_csv(dataset_csv_path: Path) -> list[str]:
    if not dataset_csv_path.exists():
        return []
    ids: list[str] = []
    with dataset_csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if "id" not in (reader.fieldnames or []):
            return []
        for row in reader:
            v = (row.get("id") or "").strip()
            if v:
                ids.append(v)
    return ids


def safe_dataset_id(dataset_id: str) -> str:
    return "".join([c for c in dataset_id if c.isalnum() or c in ("-", "_")])


def run_script(args_list: list[str], cwd: Path):
    result = subprocess.run(args_list, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed: "
            + " ".join(args_list)
            + f"\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout


def delete_path_if_exists(path: Path):
    """Best-effort delete a file or directory."""

    try:
        if not path.exists():
            return
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
    except Exception:
        # Best-effort cleanup only; rerun should still proceed.
        return
