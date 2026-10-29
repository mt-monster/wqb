#!/usr/bin/env python
"""读取 MCP 工具输出被外部化后的 chunked JSONL 产物。

用法：
    python tools/code-audit/read_tool_artifact.py <artifact.jsonl> --keys
    python tools/code-audit/read_tool_artifact.py <artifact.jsonl> --json 0 --keys
    python tools/code-audit/read_tool_artifact.py <artifact.jsonl> --json 0.datasets \
        --table id,name,coverage --width 46
    python tools/code-audit/read_tool_artifact.py <artifact.jsonl> --json 0 --dump > out.json

设计要点：
- 产物是 chunked JSONL：首行 header、其后每行 {"type":"chunk","index":n,"text":...}，
  必须按 index 顺序拼接 text 才能还原原始 JSON。
- 同一个产物文件里可能拼着**多段** JSON（chunk index 会从 0 重新开始），
  因此按「遇到重复 index 就开新组」切分，每组再用 raw_decode 顺序解析，
  支持一段文本里背靠背的多个 JSON 文档。
- 多段时返回 list，用 --json 1 选段。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _text_groups(path: Path) -> list[str]:
    """把 chunked JSONL 还原成若干段原始文本。"""
    groups: list[dict[int, str]] = []
    current: dict[int, str] = {}
    with path.open("r", encoding="utf-8-sig") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("type") != "chunk":
                continue
            idx = int(row["index"])
            if idx in current:
                groups.append(current)
                current = {}
            current[idx] = row.get("text", "")
    if current:
        groups.append(current)
    return ["".join(group[i] for i in sorted(group)) for group in groups]


def load_artifact(path: Path) -> Any:
    """把 chunked JSONL 拼回原始 JSON 对象（可能多段）。"""
    texts = _text_groups(path)
    if not texts:
        raise SystemExit(f"no chunk rows found in {path}")

    docs: list[Any] = []
    decoder = json.JSONDecoder()
    for text in texts:
        pos = 0
        while pos < len(text):
            while pos < len(text) and text[pos] in " \r\n\t":
                pos += 1
            if pos >= len(text):
                break
            try:
                obj, pos = decoder.raw_decode(text, pos)
            except json.JSONDecodeError as exc:
                docs.append({"_parse_error": str(exc), "_raw_head": text[pos : pos + 400]})
                break
            docs.append(obj)
    if not docs:
        raise SystemExit(f"no JSON document found in {path}")
    return docs[0] if len(docs) == 1 else docs


def load_text(path: str | Path) -> str:
    """把 chunked JSONL 还原成原始文本（多段时按换行拼接）。

    兼容旧 API：``profile_dataset_fields.load_payload`` 会 ``from read_tool_artifact
    import extract_json, load_text``。
    """
    texts = _text_groups(Path(path))
    if not texts:
        raise SystemExit(f"no chunk rows found in {path}")
    return "\n".join(texts)


def extract_json(text: str) -> Any:
    """从文本里解析第一个 JSON 文档，容忍前后噪声（兼容旧 API）。

    与 ``load_artifact`` 的区别：后者按 chunk index 分组后再解析，本函数只吃
    纯文本，供已经把文本读出来的调用方使用。
    """
    decoder = json.JSONDecoder()
    pos = 0
    n = len(text)
    while pos < n:
        while pos < n and text[pos] in " \r\n\t":
            pos += 1
        if pos >= n:
            break
        try:
            obj, _end = decoder.raw_decode(text, pos)
        except json.JSONDecodeError:
            pos += 1
            continue
        return obj
    raise ValueError("no JSON document found in text")


def describe(node: Any) -> str:
    if isinstance(node, list):
        return f"list: len={len(node)}"
    if isinstance(node, dict):
        keys = list(node)[:12]
        return f"dict: keys={keys}{'...' if len(node) > 12 else ''}"
    return type(node).__name__


def short(val: Any, limit: int = 80) -> str:
    text = str(val).replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 3] + "..."


def walk(node: Any, path: str, out: list[tuple[str, str]], depth: int, max_depth: int) -> None:
    """递归收集 (path, 描述) 便于人工定位。"""
    if depth > max_depth:
        return
    if isinstance(node, dict):
        items = list(node.items())
        for key, val in items:
            child = f"{path}.{key}" if path else str(key)
            out.append((child, describe(val) if isinstance(val, (dict, list)) else f"{type(val).__name__} = {short(val)}"))
            if isinstance(val, (dict, list)):
                walk(val, child, out, depth + 1, max_depth)
    elif isinstance(node, list):
        for i, val in enumerate(node):
            child = f"{path}[{i}]" if path else f"[{i}]"
            out.append((child, describe(val) if isinstance(val, (dict, list)) else f"{type(val).__name__} = {short(val)}"))
            if isinstance(val, (dict, list)):
                walk(val, child, out, depth + 1, max_depth)


def resolve(root: Any, expr: str) -> Any:
    """按 a.b[0].c 形式取子节点。"""
    if not expr:
        return root
    node = root
    parts: list[Any] = []
    token = ""
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch == ".":
            if token:
                parts.append(token)
                token = ""
        elif ch == "[":
            if token:
                parts.append(token)
                token = ""
            end = expr.index("]", i)
            parts.append(int(expr[i + 1 : end]))
            i = end
        else:
            token += ch
        i += 1
    if token:
        parts.append(token)
    for part in parts:
        if isinstance(node, list) and isinstance(part, str):
            part = int(part)
        node = node[part]
    return node


def print_table(node: Any, fields: list[str], width: int) -> None:
    rows = node if isinstance(node, list) else [node]
    if not rows:
        print("(empty)")
        return
    is_dict = isinstance(rows[0], dict)
    header = fields if is_dict else ["value"]
    cells: list[list[str]] = []
    for row in rows:
        if not is_dict:
            cells.append([short(row, width)])
        else:
            cells.append([short(row.get(f, ""), width) for f in header])
    widths = [min(max(len(header[i]), *(len(r[i]) for r in cells)), width) for i in range(len(header))]
    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(header)))
    print("  ".join("-" * widths[i] for i in range(len(header))))
    for row in cells:
        print("  ".join(row[i].ljust(widths[i]) for i in range(len(header))))
    print(f"\n({len(cells)} rows)")


def main() -> int:
    ap = argparse.ArgumentParser(description="读取外部化的 MCP 工具输出产物")
    ap.add_argument("artifact", help="*.readable.v1.jsonl 路径")
    ap.add_argument("--json", dest="json_path", default="", help="子节点路径，如 0.datasets")
    ap.add_argument("--keys", action="store_true", help="打印 key 索引而不是完整值")
    ap.add_argument("--table", default="", help="逗号分隔的字段投影（list[dict] 才有意义）")
    ap.add_argument("--width", type=int, default=40, help="表格单元格最大宽度（默认 40）")
    ap.add_argument("--depth", type=int, default=3, help="--keys 递归深度（默认 3）")
    ap.add_argument("--dump", action="store_true", help="打印完整 JSON（慎用）")
    args = ap.parse_args()

    path = Path(args.artifact)
    if not path.exists():
        print(f"artifact not found: {path}", file=sys.stderr)
        return 2

    root = load_artifact(path)
    node = resolve(root, args.json_path)

    if args.dump:
        json.dump(node, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    if args.table:
        print_table(node, [f.strip() for f in args.table.split(",") if f.strip()], args.width)
        return 0

    out: list[tuple[str, str]] = [(args.json_path or "$", describe(node))]
    walk(node, args.json_path, out, 0, args.depth)
    width = max((len(p) for p, _ in out), default=0)
    for p, d in out:
        print(f"{p.ljust(width)}  {d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
