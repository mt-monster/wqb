#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""migrate_ideas_to_db.py — 将现有 idea JSON 文件批量迁移到 SQLite 数据库.

扫描指定目录下的所有 *idea*.json 文件，导入到 ideas.db 中.
支持断点续跑：已导入的记录会自动跳过.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from wqb.memory.idea_store import IdeaStore


def scan_idea_files(root_dirs: list[str]) -> list[Path]:
    """扫描指定目录下的所有 idea JSON 文件."""
    idea_files = []
    for root_dir in root_dirs:
        root = Path(root_dir)
        if not root.exists():
            print(f"[WARN] 目录不存在: {root_dir}")
            continue
        # 匹配 *idea*.json 和 *idea_context*.json
        for pattern in ["**/*idea*.json", "**/*idea_context*.json"]:
            idea_files.extend(root.glob(pattern))
    return sorted(set(idea_files))


def migrate_file(store: IdeaStore, json_path: Path) -> bool:
    """迁移单个 JSON 文件到数据库."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 生成 idea_id: 使用文件名（不含扩展名）
        idea_id = json_path.stem

        # 检查是否已存在
        existing = store.get_idea(idea_id)
        if existing:
            print(f"[SKIP] 已存在: {idea_id}")
            return False

        # 特殊处理 idea_context.json 格式
        if "expression_list" in data and isinstance(data.get("expression_list"), list):
            # 这是 idea_context 格式，需要提取外层字段
            idea_data = {
                "region": data.get("region", ""),
                "dataset_id": data.get("dataset_id") or data.get("dataset", ""),
                "delay": data.get("delay", 1),
                "universe": data.get("universe", ""),
                "neutralization": data.get("neutralization", ""),
                "expression_list": data.get("expression_list", []),
                "target": data.get("target", {}),
                "focus": data.get("focus"),
                "pyramid": data.get("pyramid"),
                "fieldCount": data.get("fieldCount"),
                "coverage": data.get("coverage"),
                "metadata": {
                    "source_file": str(json_path),
                    "migrated_from": "idea_context",
                },
            }
        else:
            # 标准 idea 格式
            idea_data = data.copy()
            idea_data["metadata"] = idea_data.get("metadata", {})
            idea_data["metadata"]["source_file"] = str(json_path)
            idea_data["metadata"]["migrated_from"] = "idea_json"

        store.save_idea(idea_id, idea_data)
        print(f"[OK] 导入成功: {idea_id}")
        return True

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 解析失败 {json_path}: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 迁移失败 {json_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="迁移 idea JSON 文件到 SQLite 数据库")
    parser.add_argument(
        "--dirs",
        nargs="+",
        default=[
            "tracking",
            "logs",
            "data",
        ],
        help="要扫描的根目录列表（默认: tracking logs data）",
    )
    parser.add_argument(
        "--db",
        default=None,
        help="数据库文件路径（默认: data/ideas.db）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅扫描不导入，用于预览",
    )
    args = parser.parse_args()

    # 扫描文件
    idea_files = scan_idea_files(args.dirs)
    print(f"发现 {len(idea_files)} 个 idea JSON 文件")

    if args.dry_run:
        for f in idea_files:
            print(f"  - {f}")
        return

    # 初始化数据库
    store = IdeaStore(args.db)
    print(f"数据库: {store.db_path}")

    # 迁移
    success_count = 0
    skip_count = 0
    error_count = 0

    for json_path in idea_files:
        result = migrate_file(store, json_path)
        if result is True:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1

    store.close()

    print("\n=== 迁移完成 ===")
    print(f"成功导入: {success_count}")
    print(f"跳过已存在: {skip_count}")
    print(f"失败: {error_count}")
    print(f"总计: {len(idea_files)}")


if __name__ == "__main__":
    main()
