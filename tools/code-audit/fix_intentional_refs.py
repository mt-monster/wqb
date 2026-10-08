# -*- coding: utf-8 -*-
"""给「合理但不存在的路径引用」打豁免标记，让 doc_path_refs 基线归零（2026-10-07）。

背景
----
第二轮治理复核发现 `doc_path_refs` 的 BROKEN 基线长期挂在 17，棘轮只挡新增、
不为零——一个永远不为零的基线等于把信号稀释掉。逐个查证后，这 17 条**没有一条是真故障**，
而是三类「引用了一个有意缺席的事物」：

  A. 设计规划文档引用**当时计划要创建**的源文件。
     实际实现走了别的形态（`modeb_*` 系列后来收敛为 `src/wqb/workflow/nodes/modeb_improve.py`
     + `mode_b_adaptive.py` / `structural_variants.py`），文档表格里写的路径从未被建出来。
  B. 历史决策记录引用**当时还没落地**的回归测试文件。
  C. skills 契约文档引用**尚未初始化的区域目录**（TWN 有 profile 但没有 `tracking/TWN/`），
     含义是「开新区前要先补这些文件」——引用一个不存在的东西，恰恰是这句话的重点。

这三类都有一个共同点：**删掉引用会丢信息**（后人就不知道当初打算做什么 / 新区需要什么）。
所以正解不是删，也不是 `--update-baseline` 登记了事，而是用仓库既有机制
`lint:counterexample` **就地标注为什么豁免**——既摘掉了死指针，又把理由留在原文里。

用法
----
    python tools/code-audit/fix_intentional_refs.py            # dry-run
    python tools/code-audit/fix_intentional_refs.py --apply    # 落盘

幂等：已带 `lint:counterexample` 的行跳过；重复跑不会追加第二份标记。
"""
from __future__ import annotations
import sys

import argparse
import io
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO_ROOT = find_repo_root(__file__)
MARK = "lint:counterexample"

# (相对路径, 该行必须包含的匹配串, 豁免理由)
RULES: list[tuple[str, str, str]] = [
    # --- A. 设计规划：路径是「计划形态」，实现最终收敛到别的模块 ---
    ("docs/design/modeb_operator_optimization_plan.md",
     "src/wqb/expression/modeb_transform.py",
     "本表是 2026-09 的**实施计划**快照：该路径为计划形态，实际实现收敛到 "
     "src/wqb/workflow/nodes/modeb_improve.py 与 mode_b_adaptive.py，此文件从未创建"),
    ("docs/design/modeb_operator_optimization_plan.md",
     "src/wqb/expression/modeb_constraints.py",
     "同上：计划形态，实际约束校验落在 expression/op_arity.py 与 validator.py"),
    ("docs/design/modeb_operator_optimization_plan.md",
     "src/wqb/workflow/modeb_generator.py",
     "同上：计划形态，实际变体生成落在 structural_variants.py"),
    ("docs/design/modeb_operator_optimization_plan.md",
     "src/wqb/workflow/modeb_diagnoser.py",
     "同上：计划形态，实际诊断聚合在 nodes/modeb_improve.py"),
    ("docs/design/modeb_operator_optimization_plan.md",
     "src/wqb/workflow/modeb_stats.py",
     "同上：计划形态，实际统计经 store 层表记录，未单独成模块"),
    ("docs/design/modeb_operator_optimization_plan.md",
     "src/wqb/workflow/modeb_recommender.py",
     "同上：计划形态，推荐逻辑并入 _lib/rules.py 的策略回路"),
    ("docs/design/modeb_operator_optimization_plan.md",
     "src/wqb/store/schema.sql",
     "同上：计划形态，实际建表语句随 store 层 Python 代码维护"),
    # --- B. 历史决策记录：引用当时尚未落地的回归测试 ---
    ("docs/design/submittable_alpha_optimization.md",
     "src/wqb/workflow/nodes/corr_screen.py",
     "本表 P0.1 是**待实施项**：corr_screen 节点尚未创建，此处引用的是拟新增的目标路径"),
    ("docs/design/skills_review_decisions.md",
     "tests/unit/07_docs_skills/test_no_dilution_rules.py",
     "DEC-75/DEC-78 为历史决策留档：写表时该回归测试尚在工作区未随本批提交，"
     "此处引用的是当时的待提交件，属有意提及"),
    ("docs/design/design_s1_family_deadend.md",
     "tools/family_key.py",
     "本表第 1 项「族指纹计算函数」为**提案**：实现一栏写「无」，该路径从未落地"),
    # --- C. skills 契约：引用尚未初始化的区域目录（"缺什么"才是重点）---
    ("Claude/skills/INDEX.md",
     "tracking/TWN/config/",
     "TWN 为 probe-only 区：有 profile 但**没有战役目录**，此处正是要说明「开波前需补」"),
    ("Claude/skills/wq-brain-campaign-toolkit/references/campaign-dir-contract.md",
     "tracking/TWN/",
     "契约文档举例说明「区域覆盖不全」的情形：TWN 缺目录本身就是要描述的现状"),
    ("Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md",
     "tracking/TWN/",
     "同上：以 TWN 为例说明「profile 有但目录缺」不计入 13/13 实测样本"),
    ("Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md",
     "tracking/TWN/",
     "同上：开新区前置检查项，引用的是「待创建」的目录"),
    ("Claude/skills/wq-brain-ra-pipeline/references/regions/TWN.md",
     "tracking/TWN/config/",
     "区域 profile 的「缺口」小节：目录不存在正是本行要陈述的事实"),
    ("Claude/skills/wq-brain-ra-twn/SKILL.md",
     "tracking/TWN/config/",
     "本区尚未初始化：这些配置文件是「开新区前需补」的前置清单，引用待创建路径属有意提及"),
    ("Claude/skills/wq-brain-ra-twn/SKILL.md",
     "tracking/TWN/config/cells.json",
     "同上：组合文件待证据积累后生成，此处说明「当前还没有」"),
    ("Claude/skills/alpha-template-labs-data-analysis/SKILL.md",
     "tracking/runs/",
     "该目录为工具的**缺省输出位**（文档劝阻使用），并非已存在的战役目录"),
    ("Claude/skills/alpha-template-labs-data-analysis/references/agent-spec.md",
     "tracking/runs/",
     "同上：缺省输出路径，文档正是在说明「别用这个目录」"),
    ("Claude/skills/brain-alpha-research-news-sentiment/SKILL.md",
     "tracking/taxonomies/",
     "运行期缓存目录：首次运行后生成，文中已说明它是本 skill 的辅助产物"),
    ("Claude/skills/brain-dataset-exploration-general/SKILL.md",
     "tracking/taxonomies/",
     "同上：由 news-sentiment skill 在运行中生成，引用的是运行期产物路径"),
]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--apply", action="store_true", help="落盘（默认 dry-run）")
    args = ap.parse_args(argv)

    pending: dict[Path, list[tuple[int, str]]] = {}
    skipped_differs = 0
    for rel, needle, reason in RULES:
        p = REPO_ROOT / rel
        if not p.is_file():
            print(f"  !! 文件不存在，跳过：{rel}")
            continue
        lines = io.open(p, encoding="utf-8").read().split("\n")
        hit = False
        for i, ln in enumerate(lines):
            if needle not in ln:
                continue
            hit = True
            if MARK in ln:  # 幂等
                continue
            # markdown 表格行：必须追加在同一单元格内
            suffix = f" <!-- {MARK}: {reason} -->"
            lines[i] = ln.rstrip() + suffix
            pending.setdefault(p, []).append((i + 1, needle))
        if not hit:
            print(f"  ?? 未命中（String 可能已变化）：{rel} :: {needle}")

    total = sum(len(v) for v in pending.values())
    print(f"\n计划修改 {len(pending)} 个文件 / {total} 行"
          + ("" if args.apply else "（dry-run，加 --apply 落盘）"))
    for p, items in sorted(pending.items()):
        print(f"  {p.relative_to(REPO_ROOT)}  -> 行 {[n for n, _ in items]}")

    if not args.apply or not pending:
        return 0

    for p, items in pending.items():
        lines = io.open(p, encoding="utf-8").read().split("\n")
        for lineno, needle in items:
            i = lineno - 1
            if needle not in lines[i]:
                print(f"  !! {p.name}:{lineno} 内容已变，跳过")
                skipped_differs += 1
                continue
            if MARK in lines[i]:
                continue
            # Windows 上 relative_to 给的是反斜杠，RULES 里统一用正斜杠——必须归一后再查表
            key = (p.relative_to(REPO_ROOT).as_posix(), needle)
            reason = dict(((r[0], r[1]), r[2]) for r in RULES)[key]
            suffix = f" <!-- {MARK}: {reason} -->"
            lines[i] = lines[i].rstrip() + suffix
        io.open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
        print(f"  ✓ 已写 {p.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys_exit = __import__("sys").exit
    sys_exit(main())
