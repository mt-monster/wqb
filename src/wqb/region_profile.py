# -*- coding: utf-8 -*-
"""区域 profile front-matter 的**唯一解析器**（2026-10-01 落地）。

背景：仓库里曾有 4 套各自为政的简易解析器（assemble_priors 行扫描 / region_status 单键
正则 / index_tables 通用单键正则 / test_region_alignment 的 static 块解析）。本模块收口为
一套，覆盖 profile front-matter 实际用到的 YAML 子集，不依赖 PyYAML：

- 顶层键 / 2 空格缩进嵌套 map
- inline list（`[a, b]`，元素可带引号；中文逗号、括号安全）
- block list（`- item`；元素可为标量或 dict 项 `- key: value` + 更深缩进的续行键）
- 引号 / 裸标量 / 空值 / 行尾未加引号的 `#` 注释

`datasets` 块的结构化形态（2026-10-01 精确化迁移，见 region-profile-contract.md §5）：

```yaml
datasets:
  red:
    - datasets: [model109, model170]      # 数据集级（精确层：id 必须落在 datasets.name）
      reason: "已判死（ledger *_dead ∪ dead_end 层）"
    - scope: family                        # 族级（本来就不绑定单个数据集）
      families: [chart_patterns, ai_ml]
      reason: "3 连死"
  green:
    - datasets: [other466]
      note: "registry win 层实证绑定"
  yellow: [model264]                       # 保持简单标量列表，drift 不消费
```

消费方：wqb.profile_drift（步 9 回写钩子）/ tools/profile_drift_check.py。
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

#: 仓库权威 profile 目录（同步安装位由 tools/sync_skills.py 负责，读取一律以仓库为准）
PROFILE_DIR = (
    Path(__file__).resolve().parents[2]
    / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "regions"
)

_FM = re.compile(r"\s*---\s*\r?\n(.*?)\r?\n---", re.S)
_KEY = re.compile(r"^([A-Za-z_][\w]*):\s*(.*)$")


def _strip_comment(v: str) -> str:
    """去掉未加引号标量的行尾 `#` 注释（引号内的 # 保留）。"""
    if not v or v[0] in "\"'":
        return v
    i = v.find(" #")
    return v[:i] if i >= 0 else v


def _strip_quotes(v: str) -> str:
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def _split_inline(inner: str) -> List[str]:
    """按逗号切 inline list 元素，跳过引号内的逗号。"""
    out, buf, quote = [], [], None
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            out.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf).strip())
    return [_strip_quotes(x) for x in out if x]


def _parse_scalar(v: str) -> Any:
    v = _strip_comment(v).strip()
    if not v:
        return None
    if v.startswith("[") and v.endswith("]"):
        return _split_inline(v[1:-1])
    return _strip_quotes(v)


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _parse_node(lines: List[str], i: int, indent: int):
    """递归解析一个块（map 或 list）。返回 (value, 下一行下标)。"""
    mapping: Optional[Dict[str, Any]] = None
    items: Optional[List[Any]] = None
    n = len(lines)
    while i < n:
        raw = lines[i]
        if not raw.strip() or raw.strip().startswith("#"):
            i += 1
            continue
        cur = _indent(raw)
        if cur < indent:
            break
        s = raw.strip()
        if s.startswith("- "):
            if mapping is not None:
                break
            if items is None:
                items = []
            content = s[2:]
            item_indent = cur + 2
            km = _KEY.match(content)
            if km:
                d: Dict[str, Any] = {}
                if km.group(2).strip():
                    d[km.group(1)] = _parse_scalar(km.group(2))
                    i += 1
                else:
                    child, i = _parse_node(lines, i + 1, item_indent + 2)
                    d[km.group(1)] = child
                # 续行键（与 dict 项内容同缩进）
                while i < n:
                    raw2 = lines[i]
                    if not raw2.strip():
                        i += 1
                        continue
                    ci2 = _indent(raw2)
                    s2 = raw2.strip()
                    if ci2 < item_indent or s2.startswith("- "):
                        break
                    km2 = _KEY.match(s2)
                    if not km2:
                        break
                    if km2.group(2).strip():
                        d[km2.group(1)] = _parse_scalar(km2.group(2))
                        i += 1
                    else:
                        child, i = _parse_node(lines, i + 1, ci2 + 2)
                        d[km2.group(1)] = child
                items.append(d)
            else:
                items.append(_parse_scalar(content))
                i += 1
            continue
        km = _KEY.match(s)
        if not km:
            i += 1
            continue
        if items is not None:
            break
        if mapping is None:
            mapping = {}
        key, val = km.group(1), km.group(2)
        if val.strip():
            mapping[key] = _parse_scalar(val)
            i += 1
        else:
            # 空值 → 看下一行决定是否嵌套块
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and _indent(lines[j]) > cur and not lines[j].strip().startswith("#"):
                child, i = _parse_node(lines, i + 1, _indent(lines[j]))
                mapping[key] = child
            else:
                mapping[key] = None
                i += 1
    if items is not None and mapping is None:
        return items, i
    return (mapping or {}), i


def parse_front_matter(text: str) -> Dict[str, Any]:
    """解析 profile 的 YAML front-matter（子集）。无 front-matter 返回 {}。"""
    m = _FM.match(text)
    if not m:
        return {}
    value, _ = _parse_node(m.group(1).splitlines(), 0, 0)
    return value if isinstance(value, dict) else {}


# ----------------------------------------------------------------------------- datasets 块模型

@dataclass
class DatasetEntry:
    """green/red 里的一条记录。datasets 非空 = 数据集级（精确层）；否则为族级（scope=family）。"""

    datasets: List[str] = field(default_factory=list)
    families: List[str] = field(default_factory=list)
    scope: str = "dataset"          # dataset | family
    note: str = ""
    reason: str = ""


def _entries_from(raw: Any, text_key: str) -> List[DatasetEntry]:
    """把 green/red 的解析结果归一成 DatasetEntry 列表。

    兼容输入形态（只读容忍，不是契约）：
      - 新形态：block list of dict（`- datasets: [..]` / `- scope: family, families: [..]`）
      - 旧形态：inline list of str / 单个 str（迁移漏网时的兜底，标 scope=family 存原文）
    """
    out: List[DatasetEntry] = []
    if raw is None:
        return out
    if isinstance(raw, str):
        raw = [raw]
    if not isinstance(raw, list):
        return out
    for item in raw:
        if isinstance(item, dict):
            ds = item.get("datasets") or []
            fams = item.get("families") or []
            if isinstance(ds, str):
                ds = [ds]
            if isinstance(fams, str):
                fams = [fams]
            scope = str(item.get("scope") or ("family" if fams and not ds else "dataset"))
            out.append(DatasetEntry(
                datasets=[str(x) for x in ds],
                families=[str(x) for x in fams],
                scope=scope,
                note=str(item.get("note") or ""),
                reason=str(item.get("reason") or ""),
            ))
        elif item is not None:
            # 旧文本项：不猜它是不是数据集 id，原样按族级保留（精确性由迁移保证）
            out.append(DatasetEntry(scope="family", families=[str(item)]))
    return out


@dataclass
class RegionProfile:
    region: str
    entry_verdict: str
    last_verified: str
    green: List[DatasetEntry]
    red: List[DatasetEntry]
    yellow: List[str]
    path: Optional[Path] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def dataset_refs(self) -> Dict[str, List[str]]:
        """精确层引用的数据集 id：{'green': [...], 'red': [...]}（族级条目不进精确层）。"""
        return {
            "green": sorted({d for e in self.green for d in e.datasets}),
            "red": sorted({d for e in self.red for d in e.datasets}),
        }


def load_profile(region: str, profile_dir: Optional[Path] = None) -> Optional[RegionProfile]:
    """读取并解析某区 profile；文件不存在返回 None。"""
    path = (profile_dir or PROFILE_DIR) / f"{region}.md"
    if not path.exists():
        return None
    fm = parse_front_matter(path.read_text(encoding="utf-8", errors="replace"))
    ds = fm.get("datasets") or {}
    if not isinstance(ds, dict):
        ds = {}
    yellow = ds.get("yellow") or []
    if isinstance(yellow, str):
        yellow = [yellow]
    anchor = fm.get("empirical_anchor") or {}
    if not isinstance(anchor, dict):
        anchor = {}
    return RegionProfile(
        region=str(fm.get("region") or region),
        entry_verdict=str(fm.get("entry_verdict") or ""),
        last_verified=str(anchor.get("last_verified") or ""),
        green=_entries_from(ds.get("green"), "note"),
        red=_entries_from(ds.get("red"), "reason"),
        yellow=[str(y) for y in yellow if y is not None],
        path=path,
        raw=fm,
    )
