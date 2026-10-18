# -*- coding: utf-8 -*-
"""区域 skill 四目录脚手架（rules / config / references / scripts）。

背景：2026-10-18 用户决策——每个 region skill 建四目录、保持「每区独有结构」。
本工具为指定区域（缺省全部）幂等创建四目录骨架并生成区级视图：

    rules/README.md        该区独有规则索引 + 本区三条硬规则占位（人工填）
    config/README.md       三表分工 + 真身指针 + 本区覆盖落差（自动读 tracking/<R>/config）
    config/region_view.json 机器可读摘要（as_of + 默认档 + cells 概况）
    scripts/README.md      家规 + 清单（本区 skill 级脚本；当前是否为空自动判定）
    SKILL.md               在「## 区域控制面板」之前幂等插入「本区结构导航（四目录）」块

**只增不删**：已存在的文件一律不覆盖（打印 SKIP）；不碰任何生成块内容；不改 references/。
幂等：可重复执行。已有 SKILL.md 导航块则跳过。

用法（仓库根执行，必须用 MCP venv 解释器）：
    $WQ_PY tools/skills/gen_region_skill_scaffold.py --list
    $WQ_PY tools/skills/gen_region_skill_scaffold.py --region USA --apply
    $WQ_PY tools/skills/gen_region_skill_scaffold.py --all --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "Claude" / "skills"
NAV_TITLE = "## 本区结构导航（四目录）"
NAV_MARK = "<!-- region-scaffold:nav:start -->"
PANEL_HEADING = "## 区域控制面板"


def regions() -> list[str]:
    out = []
    for d in sorted(SKILLS.glob("wq-brain-ra-*")):
        if d.name == "wq-brain-ra-pipeline" or not (d / "SKILL.md").exists():
            continue
        out.append(d.name.removeprefix("wq-brain-ra-").upper())
    return out


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def nav_block(r: str, has_refs: bool = True) -> str:
    # 无组合分支文件（未开战役）时不链 references/ ——否则造死链
    refs_row = (
        "| [`references/`](references/) | **实证**：`<类别>.md` 组合分支卡（render 生成）+ `_` 前缀专题（战役 / 手册 / 快照） | [references/](references/) |"
        if has_refs else
        "| `references/` | **实证**：本区暂无组合分支文件（未开战役）⇒ 不建目录 | — |"
    )
    return f"""{NAV_MARK}
| 目录 | 装什么 | 入口 |
|---|---|---|
| **SKILL.md** | 职责边界 + 怎么用 + 生成块（区域控制面板 / 组合分支 / 流程差异） | 本文 |
| [`rules/`](rules/README.md) | **{r} 独有规则与纪律**（六步覆盖、改控制、闸门与提交纪律） | [rules/README.md](rules/README.md) |
| [`config/`](config/README.md) | **配置视图**（真身在 `tracking/{r}/config/`）：三表分工、区域默认档、覆盖落差 | [config/README.md](config/README.md) |
{refs_row}
| [`scripts/`](scripts/README.md) | 本 skill 级脚本（区域探针脚本家 = `tracking/{r}/scripts/`） | [scripts/README.md](scripts/README.md) |

细则不写在 SKILL.md：规则 → `rules/`，实证 → `references/`，配置 → `config/`，脚本 → `scripts/`。
<!-- region-scaffold:nav:end -->"""


def rules_readme(r: str, skill_md: Path) -> str:
    n_lines = len(skill_md.read_text(encoding="utf-8").splitlines()) if skill_md.exists() else 0
    return f"""# {r} 区域独有规则（rules/）

> **定位**：只放**{r} 特有**的规则与纪律；九步通用正文在 `../../wq-brain-ra-pipeline/SKILL.md`，不在此重复。
> **as_of**：{date.today().isoformat()} ｜ 手写区，SKILL.md 生成块重渲不会覆盖它。
> **分工**：SKILL.md 只留入口与摘要（目标 ≤250 行，当前 {n_lines} 行）；细则在 `rules/` 与 `../references/`。

| 文件 | 内容 |
|---|---|
| （待填）`six-step-{r.lower()}-override.md` | 六步纵深骨架的 {r} 覆盖项 + 改控制纪律（从 SKILL.md 手写区下沉） |
| （待填）`gate-and-submit-discipline.md` | 本区闸门纪律（prod / self / 提交链路 / base payment 选型，若本区有实证） |

## 填充纪律

1. 只写**本区独有**的（别的区通用的回 `../wq-brain-ra-pipeline/`）；跨区普适规律沉淀到 `docs/experience/`。
2. 实证数字必须带 `as_of` + alpha id / 波号；判死结论写清「结构性 / 可修复」。
3. 门槛数字不抄字面量——引用 `PLATFORM_CHECK_LINES` / `GATES_*` 常量名（`tools/skill_lint` const-literal 闸）。
"""


def config_readme(r: str) -> str:
    return f"""# {r} 配置视图（config/）

> ⚠ **本目录不是事实源**。真身在 `tracking/{r}/config/`；本目录只给**视图 + 差异说明 + 证据索引**。
> 原因：`wqb.profiles explain / render / sync-cells` 按 `tracking/<R>/config/` 解析，
> 覆盖值强制 `_evidence`；把真身搬进 skill 会复制事实源并断掉 profiles 链。
> 机器可读摘要见 [`region_view.json`](region_view.json)（改配置后须同步其 `as_of` 与要点）。

## 三表分工

| 表 | 管什么 | 真身 |
|---|---|---|
| `settings.json` | 区域固定仿真设置 + `_spre_*` 步 1 产物（排除族 / 正交方向 / win 配方 / prod 饱和） | `tracking/{r}/config/settings.json` |
| `thresholds.json` | 审查阈值（review / near / quick_scan / probe_scoring / hard_gates） | `tracking/{r}/config/thresholds.json` |
| `cells.json` | 组合级覆盖（区域 × 类别），每个覆盖须同级 `_evidence` | `tracking/{r}/config/cells.json` |

```bash
$WQ_PY -m wqb.profiles explain --region {r} --dataset <dataset>
$WQ_PY -m wqb.profiles check   --region {r}
```
"""


def scripts_readme(r: str, has: list[str]) -> str:
    rows = "\n".join(f"| `{p}` | （待补用途） | skill 级 |" for p in has) or "| （暂无） | — | — |"
    return f"""# {r} 区域脚本（scripts/）

> **家规**（AGENTS §8.13）：skill 内 `scripts/` 只放**本 skill 的校验器 / 固定流程脚本**；
> 区域探针与一次性战役脚本的家是 `tracking/{r}/scripts/`。
> **as_of**：{date.today().isoformat()}

## 当前清单

| 脚本 | 用途 | 归属 |
|---|---|---|
{rows}

## 不要放进来的东西

- 战役一次性脚本（属 `tracking/{r}/campaign_<date>/`）
- 可复用引擎（属仓库 `tools/`，进 skill 会形成第二份事实源）
- 任何需要凭据的脚本
"""


def region_view(r: str) -> dict:
    cfg = REPO / "tracking" / r / "config"
    s, c = _load(cfg / "settings.json"), _load(cfg / "cells.json")
    cells = c.get("cells") or {}
    overrides = sum(1 for v in cells.values() if isinstance(v, dict) and v.get("backtest"))
    return {
        "region": r,
        "as_of": date.today().isoformat(),
        "_note": "配置视图（非事实源）。真身=tracking/<R>/config/*.json；改配置只改真身后 render --apply。",
        "source_of_truth": {
            "settings": f"tracking/{r}/config/settings.json",
            "thresholds": f"tracking/{r}/config/thresholds.json",
            "cells": f"tracking/{r}/config/cells.json",
        },
        "region_defaults": {
            k: s.get(k) for k in (
                "instrumentType", "region", "universe", "delay", "neutralization",
                "decay", "truncation", "maxTrade", "pasteurization", "unitHandling",
                "nanHandling", "language") if s.get(k) is not None
        },
        "cells": {
            "categories": sorted(cells),
            "count": len(cells),
            "overrides": overrides,
            **({"gap": "零覆盖：explain 只给区域默认档；若本区实测用过其它档位，应补覆盖并附 _evidence"}
               if overrides == 0 else {}),
        },
    }


def put(path: Path, text: str, apply_: bool) -> str:
    if path.exists():
        return "SKIP"
    if apply_:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    return "PLAN"


def insert_nav(r: str, apply_: bool, has_refs: bool = True) -> str:
    p = SKILLS / f"wq-brain-ra-{r.lower()}" / "SKILL.md"
    if not p.exists():
        return "NO-SKILL"
    text = p.read_text(encoding="utf-8")
    if NAV_MARK in text:          # 只认标记：标题文案可变，标记才是幂等锚
        return "SKIP"
    i = text.find(PANEL_HEADING)
    if i < 0:
        return "NO-PANEL"
    new = text[:i].rstrip("\n") + "\n\n" + nav_block(r) + "\n\n" + text[i:]
    if apply_:
        p.write_text(new, encoding="utf-8", newline="\n")
    return "OK" if apply_ else "PLAN"


def main() -> int:
    ap = argparse.ArgumentParser(description="区域 skill 四目录脚手架")
    ap.add_argument("--region", help="单个区域（如 USA）；缺省配合 --all")
    ap.add_argument("--all", action="store_true", help="全部区域")
    ap.add_argument("--list", action="store_true", help="列出区域")
    ap.add_argument("--apply", action="store_true", help="真正写入（缺省只 PLAN）")
    a = ap.parse_args()
    if a.list:
        print(" ".join(regions()))
        return 0
    rs = [a.region.upper()] if a.region else (regions() if a.all else [])
    if not rs:
        ap.error("给 --region <R> 或 --all")

    for r in rs:
        d = SKILLS / f"wq-brain-ra-{r.lower()}"
        skill_md = d / "SKILL.md"
        refs = sorted(p.name for p in (d / "references").glob("*.md")) if (d / "references").is_dir() else []
        scripts = sorted(p.name for p in (d / "scripts").glob("*.py")) if (d / "scripts").is_dir() else []
        acts = {
            "rules/README.md": put(d / "rules/README.md", rules_readme(r, skill_md), a.apply),
            "config/README.md": put(d / "config/README.md", config_readme(r), a.apply),
            "config/region_view.json": put(
                d / "config/region_view.json",
                json.dumps(region_view(r), ensure_ascii=False, indent=2) + "\n", a.apply),
            "scripts/README.md": put(d / "scripts/README.md", scripts_readme(r, scripts), a.apply),
            "SKILL.md#nav": insert_nav(r, a.apply, bool(refs)),
        }
        print(f"[{r}] refs={len(refs)} " + " ".join(f"{k}={v}" for k, v in acts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
