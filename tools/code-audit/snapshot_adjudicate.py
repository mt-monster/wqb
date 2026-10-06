#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""snapshot_adjudicate.py — 抢救点独有源码的**三态裁决台账**（2026-10-06 治理评审 P2-7）。

为什么需要它
------------
2026-10-06 治理评审实测：本地抢救点（8 个 `preserve/*` tag + 2 条 `wip/DANGER-*` 分支）里
存在**对象库有、main 没有**的源码/文档 795 件（其中代码与文档 296 件），而 `dc18a1a → 36f9bca`
那串以「恢复丢失的源码」「P4 收尾」为标题的提交只裁决了 **6 件**。其余无台账、无裁决、无闸
—— 时间一长就变成「没人知道为什么留着」的债，而且这些 ref 只存在一块盘上（见 branch_policy §5）。

本工具做的事
------------
1. 从 `repo_governance_check.snapshot_unique_sources()` 取全量清单（受跟踪树 + 未跟踪父提交两条腿）；
2. 按**机械规则**给每件打初判，再叠加 `tests/fixtures/snapshot_adjudication.json` 里的**人工裁决**；
3. 渲染成 `docs/governance/snapshot_adjudication.md`（人读的表），支持 `--check` 反向校验
   「文档与当前对象库是否还一致」——新增一件独有文件而没人裁决，`--check` 就红。

三态口径（与文档一致，不得自造第四态）
--------------------------------------
- `RESTORED`   已取回 main（本次或历次治理），列出即留痕；
- `DROPPED`    裁决**不回迁**：零活动引用 / 职责已被现通道覆盖 / 属未合入工作线且单件回迁会造悬空依赖；
- `ARTIFACT`   运行产物 / 数据转储（可重跑、或区域数据湖的时点快照），**不是资产**，不入库；
- `PENDING`    待人工裁决 —— 这一态**必须为 0 才叫裁决完成**；非 0 时 `--check` 给出清单。

规则只给**初判**，最终态由 overrides（人工）覆盖。规则本身写在代码里并可读，
不假装「机器替人做了价值判断」。

用法
----
    python tools/code-audit/snapshot_adjudicate.py            # 干跑：只打印统计
    python tools/code-audit/snapshot_adjudicate.py --apply     # 写文档（默认不写）
    python tools/code-audit/snapshot_adjudicate.py --check     # 文档是否仍与对象库一致
    python tools/code-audit/snapshot_adjudicate.py --json      # 机读明细
退出码：0 = 一致 / 1 = 文档过期或有新增待裁决 / 2 = 工具故障
"""
from __future__ import annotations

import argparse
import importlib.util as _ilu
import json
import sys
from collections import Counter
from pathlib import Path

# 复用同目录那份读数实现（它本身就是「先行指标」的单源），避免两处各数一遍。
_REPO = Path(__file__).resolve()
for _p in _REPO.parents:
    if (_p / "pyproject.toml").exists() and (_p / "src" / "wqb").is_dir():
        break
else:
    print("[snapshot_adjudicate] 仓库根未找到（向上未见 pyproject.toml + src/wqb）", file=sys.stderr)
    raise SystemExit(2)
REPO = _p

_RG_PATH = REPO / "tools" / "code-audit" / "repo_governance_check.py"
_spec = _ilu.spec_from_file_location("repo_governance_check", str(_RG_PATH))
_rg = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_rg)

FIXTURE = REPO / "tests" / "fixtures" / "snapshot_adjudication.json"
DOC = REPO / "docs" / "governance" / "snapshot_adjudication.md"

VERDICTS = ("RESTORED", "DROPPED", "ARTIFACT", "PENDING")

#: 判 `ARTIFACT` 的路径规则：可重跑产物 / 数据转储 / 断点，不是「人的结论」
ARTIFACT_DIR_RULES = (
    "tracking/mining/",              # 共享数据湖（字段体检 dump）
    "tracking/prod_probe/",          # 探针 dump
    "tracking/PPA_USA/",             # PPA 运行期产物
    "tracking/_scratch/",            # 临时区
)
ARTIFACT_NAME_RULES = (
    ("tracking/", ".json"),          # 区域战役的运行期 JSON（候选/体检/ckpt）
    ("output_report/", ".json"),
)
ARTIFACT_SUFFIXES = ("_ckpt.json", ".pkl", ".xlsx", ".log")


def load_overrides() -> dict:
    """人工裁决表：`{"verdicts": {"<path>": {"verdict": "...", "basis": "..."}}}`。"""
    if not FIXTURE.is_file():
        return {"verdicts": {}, "_doc": "fixture 缺失 —— 全部走规则初判"}
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"[snapshot_adjudicate] fixture 解析失败（{e}），拒绝以偏概全")
    return {"verdicts": data.get("verdicts") or {}, "_doc": data.get("_doc", "")}


def rule_verdict(path: str, blob: str, main_idx: dict) -> tuple[str, str]:
    """机械初判：只区分三件事 —— 运行产物 / 只是搬了目录 / 真正需要人判。

    ⚠ 规则**故意不自判「不回迁」**（除非 blob 逐字相等）：「零活动引用 / 职责已被覆盖」
    是价值判断，必须由人在 fixture 里写下依据，否则就是把「没人看」固化成「已裁决」。

    路径重组判定靠 **blob 相等**（同仓库同算法，可直接比）：
    实测 2026-09 的 `tests/unit/` 主题化重组与 `tools/` 下沉都留下一批
    「快照里旧路径、main 里新路径」的同名件 —— 它们不是丢失资产，但也不允许
    拿同名就当成已处理：内容不同则仍算分叉，继续留 PENDING。
    """
    if any(path.startswith(r) for r in ARTIFACT_DIR_RULES):
        return "ARTIFACT", "运行期数据目录（可重跑 / 探针 dump）"
    if path.endswith(ARTIFACT_SUFFIXES):
        return "ARTIFACT", "断点 / 缓存 / 报表类运行产物"
    for dirp, ext in ARTIFACT_NAME_RULES:
        if path.startswith(dirp) and path.endswith(ext):
            return "ARTIFACT", f"{dirp} 下的 {ext} 运行产物（可重跑）"

    name = path.rsplit("/", 1)[-1]
    same_name = [(p, b) for p, b in main_idx.get(name, []) if p != path]
    if blob and any(b == blob for p, b in same_name):
        where = next(p for p, b in same_name if b == blob)
        return "DROPPED", f"路径重组，件未丢失：main 已有内容逐字相同的 `{where}`（blob 相等）"
    if same_name:
        where = ", ".join(f"`{p}`" for p, _b in same_name[:2])
        return "PENDING", f"同名件在 main 是 {where} 但**内容不同**（分叉或版本差）——需人工比对"
    return "PENDING", "需人工裁决：代码 / 文档 / 结论类资产，main 无同名件"


def classify() -> list[dict]:
    ov = load_overrides()
    main_idx = _rg.main_blob_index()
    rows = []
    for rec in _rg.snapshot_unique_records():
        p, blob = rec["path"], rec["blob"]
        rv, rb = rule_verdict(p, blob, main_idx)
        human = ov["verdicts"].get(p)
        if human:
            if human.get("verdict") not in VERDICTS:
                raise SystemExit(f"[snapshot_adjudicate] fixture 里 {p} 的 verdict="
                                 f"{human.get('verdict')!r} 不在三态口径 {VERDICTS} 内")
            if human["verdict"] in ("DROPPED", "RESTORED") and not (human.get("basis") or "").strip():
                # 不回迁 / 已取回都是**人的价值判断**，没依据就是「没人看过」的另一种写法。
                raise SystemExit(f"[snapshot_adjudicate] fixture 里 {p} 判 {human['verdict']} 但未写依据")
            rows.append({"path": p, "verdict": human["verdict"], "basis": human.get("basis", ""),
                         "source": "human", "blob": blob, "refs": rec["refs"]})
        else:
            rows.append({"path": p, "verdict": rv, "basis": rb, "source": "rule",
                         "blob": blob, "refs": rec["refs"]})
    return rows


def stale_overrides(rows: list[dict]) -> list[str]:
    """fixture 里写了裁决、但**已不在清单中**的路径（件已被取回、或已从快照消失）。

    不报它们就会逐逐变成「fixture 里一堆没人对得上的条目」—— 那正是本台账要防的形状。
    """
    present = {r["path"] for r in rows}
    return sorted(set(load_overrides()["verdicts"]) - present)


def render(rows: list[dict], stats_note: str = "") -> str:
    c = Counter(r["verdict"] for r in rows)
    total = len(rows)
    lines = [
        "# 抢救点独有源码的三态裁决台账（snapshot adjudication）",
        "",
        "> **本文件由 `tools/code-audit/snapshot_adjudicate.py --apply` 生成，请勿手改正文表**；",
        "> 要改裁决请改 `tests/fixtures/snapshot_adjudication.json`（人工依据的唯一入口），再重跑生成。",
        "> 上位文档：[`branch_policy.md`](branch_policy.md)（取件纪律与抢救点清单）。",
        "",
        "> ⚠ **本文件是清单，不是路径承诺**：表里绝大多数路径**按定义就不在工作区**（它们只在对象库"
        "的某个快照里）。因此 `tools/code-audit/doc_path_refs.py` 把本文件归为**非活文档**，"
        "不对它做死指针判定（实测当活文档扫会新增 542 条假 BROKEN，把闸顶成永久红）；"
        "本文件自身的一致性由它自己的生成器守：`snapshot_adjudicate.py --check`，"
        "并由 `tests/unit/07_docs_skills/test_governance_gates_selfcheck.py` 在 pre-commit 里拦过期台账。",
        "",
        "## 0. 这份台账解决什么问题",
        "",
        "抢救点（`preserve/*` tag 与 `wip/DANGER-*` 分支）里有一批「对象库有、`main` 没有」的源码与文档。",
        "2026-10-06 治理评审的实测缺口：那串以「恢复丢失的源码 / P4 收尾」为标题的提交只裁决了 6 件，",
        "其余**无台账、无裁决、无闸**。本文件把「有没有人判过」变成可校验的读数：",
        "`PENDING` 必须归零；新增一件独有文件而没人裁决，`--check` 即红（守护测试见 "
        "`tests/unit/07_docs_skills/test_snapshot_adjudication.py`）。",
        "",
        "## 1. 三态口径（不得自造第四态）",
        "",
        "| 态 | 含义 | 判据 |",
        "|---|---|---|",
        "| `RESTORED` | 已取回 `main` | 本次或历次治理已 checkout 并入库，留痕用 |",
        "| `DROPPED` | 裁决**不回迁** | 零活动引用 / 职责已被现通道覆盖 / 属未合入工作线且单件回迁会造悬空依赖；**逐件必须写依据**。另含一类**机械判定**：路径重组且 blob 逐字相等（件未丢失，只是搬过目录） |",
        "| `ARTIFACT` | 运行产物 / 数据转储 | 可重跑的 dump、断点、缓存；不是「人的结论」，不入库 |",
        "| `PENDING` | 待人工裁决 | 代码 / 文档 / 结论类资产且尚无人判过 —— **这一态非 0 就是欠债** |",
        "",
        "## 2. 读数",
        "",
        f"- 清单总数（所有抢救点 ∪ 未跟踪父提交，减去 `main`）：**{total}**",
        "- " + "；".join(f"`{v}` = {c.get(v, 0)}" for v in VERDICTS),
    ]
    if stats_note:
        lines.append(f"- {stats_note}")
    lines += [
        "",
        "取数口径（两条腿都要，只取受跟踪部分会漏关键依赖 —— 本仓已踩过）：",
        "",
        "```bash",
        "git ls-tree -r --name-only <ref>       # 受跟踪树",
        "git ls-tree -r --name-only <ref>^3     # stash 式快照的未跟踪父提交",
        "```",
        "",
        "## 3. 逐件表",
        "",
    ]
    for v in VERDICTS:
        subset = [r for r in rows if r["verdict"] == v]
        if not subset:
            continue
        lines += [f"### 3.{VERDICTS.index(v) + 1} `{v}`（{len(subset)} 件）", "",
                  "| 路径 | 依据 | 来源 |", "|---|---|---|"]
        for r in subset:
            basis = (r["basis"] or "—").replace("|", "\\|")
            lines.append(f"| `{r['path']}` | {basis} | {r['source']} |")
        lines.append("")
    lines += [
        "## 4. 处置纪律",
        "",
        "- 取件用 `git checkout <ref> -- <path>` 再 `git restore --staged <path>`；"
        "**禁 `git stash pop/apply`、禁 `git restore --staged .`**（会扫到别人的在途文件）。",
        "- 判 `DROPPED` 前必须做**三源交叉**：`git ls-files`（main）+ 每个 `preserve/*` 的"
        " `ls-tree` + `git log --all --diff-filter=D -- <path>`。任一为「有」就不得写「从未存在」"
        "（2026-10-06 就发生过一次：`src/wqb/semantic_ledger.py` 被按「工作区没有」误判成「从未落地」）。",
        "- 分叉线不得单件回迁：若「A 有 B 无」与「B 有 A 无」同时存在，只能由该线所有者整线合并，"
        "任何方向覆盖都丢工作（`branch_policy.md` §2 取件纪律）。",
        "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="抢救点独有源码的三态裁决台账")
    ap.add_argument("--apply", action="store_true", help="写 docs/governance/snapshot_adjudication.md")
    ap.add_argument("--check", action="store_true", help="文档是否与当前对象库一致（不一致 rc=1）")
    ap.add_argument("--json", action="store_true", help="打印机读明细")
    a = ap.parse_args(argv)

    rows = classify()
    c = Counter(r["verdict"] for r in rows)
    stale = stale_overrides(rows)

    if a.json:
        print(json.dumps({"total": len(rows), "counts": dict(c),
                          "stale_overrides": stale, "rows": rows},
                         ensure_ascii=False, indent=1))
        return 0

    doc = render(rows, stats_note=(
        f"已写裁决但不在清单中的陈旧条目：{len(stale)} 件（取回或消失后请从 fixture 删掉）"
        if stale else "fixture 与清单逐件对应，无陈旧条目"
    ))
    if a.apply:
        DOC.parent.mkdir(parents=True, exist_ok=True)
        DOC.write_text(doc, encoding="utf-8", newline="\n")
        print(f"[snapshot_adjudicate] 已写 {DOC.relative_to(REPO).as_posix()}"
              f"（{len(rows)} 件，PENDING={c.get('PENDING', 0)}，陈旧条目={len(stale)}）")
        return 0

    if a.check:
        if not DOC.is_file():
            print(f"[snapshot_adjudicate] ❌ 台账缺失：{DOC.relative_to(REPO).as_posix()}"
                  " —— 跑 --apply 生成")
            return 1
        if DOC.read_text(encoding="utf-8") != doc:
            pend = [r["path"] for r in rows if r["verdict"] == "PENDING"]
            print(f"[snapshot_adjudicate] ❌ 台账与对象库不一致"
                  f"（总数 {len(rows)}，PENDING {len(pend)}）。")
            print("    含义：出现了**尚无人裁决**的抢救点独有文件，或某件已从快照消失。")
            for p in pend[:20]:
                print(f"    · {p}")
            if len(pend) > 20:
                print(f"    …共 {len(pend)} 件，全量：--json")
            print("    修法：在 tests/fixtures/snapshot_adjudication.json 里逐件写 verdict+basis，"
                  "再跑 --apply")
            return 1
        print(f"[snapshot_adjudicate] ✅ 台账与对象库一致（{len(rows)} 件，"
              f"PENDING={c.get('PENDING', 0)}）")
        return 0

    print(f"[snapshot_adjudicate] 共 {len(rows)} 件 | "
          + " | ".join(f"{v}={c.get(v, 0)}" for v in VERDICTS))
    if stale:
        print(f"  ⚠ fixture 有 {len(stale)} 条陈旧裁决（件已取回或已从快照消失）：{stale[:8]}")
    print("  （默认干跑不写盘；生成文档请加 --apply，核对一致性用 --check）")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:  # 工具自身坏了 ≠ 「无欠债」：响亮退 2，不能让闸空转后当通过
        print(f"[snapshot_adjudicate] 工具故障（{type(e).__name__}: {e}）", file=sys.stderr)
        sys.exit(2)
