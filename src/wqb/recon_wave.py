# -*- coding: utf-8 -*-
"""波级默认取证（`forum_recon_wave`）的纯逻辑：从一波回测结果派生「本波最该问论坛的那一个决策问题」。

为什么要有它——论坛检索是 token 黑洞（`forum-recon-triggers.md`：不在触发表内的场合不查），但「卡墙时想起去查」
靠 Agent 的记性不可靠。波级默认取证 = 收批时由代码替 Agent 问一次：对本波**共同卡住的那堵墙**（或全灭时的「有无解法」）
问论坛，结果落 ledger；之后 Mode B 找武器、判死闸取证都先读这条记录，不再各查各的。

决策问题怎么派生（机械、确定、无 LLM：同一波同一批结果 → 同一问题）。每条**已出指标**的回测行归入三类之一：

  pass     RA 闸全过、强度线过、prod 不超线                                —— 不需要武器
  blocked  强度线过了，被别的墙挡住（2Y / CW / robust / SUB / tvr / prod）  —— 找武器的对象
  weak     强度线没过                                                     —— 没有「墙」可破，缺的是想法（Mode B 换概念），不是配方
  （没有指标的行——仿真 ERROR / 未回测——不参与；它们不是论坛问题的证据）

  ① blocked 行里同一堵墙挡住 ≥ `MIN_ROWS` 条 → **墙问题**：`<REGION> <dataset> <墙> 破墙配方`（触发表 #4）
  ② 否则本波没有 pass、没有 blocked、weak ≥ `MIN_ROWS` → **判死取证问题**：`<REGION> <dataset> 有无解法`（触发表 #5，
     判死前取证的默认路径；`seal_dead_end` 的取证闸读它落下的 ledger 记录）
  ③ 其余不问（本波有产出，或没有共同瓶颈——不在触发表内）

`backtest_results.ra_failed_checks` 的读法沿用 store 的约定：**NULL 与空列表同义（无 RA 失败）**——写入方把「RA 全过」也存成 NULL
（`wqb.store._backtest`），全库读取方一律按「无失败」计。因此强度线另按数值兜底（`GATES_PLATFORM` 的 `sharpe_min` / `fitness_min`，
与 `submit_queue.is_pass` 同口径）：名单里没带强度项的旧行，sharpe / fitness 数值不够也算 weak，不会被误记成 pass。

「每波 ≤ 1 次」：可靠结局（有货 / 无解）落 `forum_recon_wave_<wave>` 标记后占用本波额度；**工具故障不占额度**
（故障 ≠ 取证，修好后同一波应能重跑）。标记之外还有 `tools/forum_recon.py` 自己的 7 天问题缓存——同数据集同墙的问题跨波复用，
不重复 live 查。
"""
from __future__ import annotations

import json
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional

from . import recon_evidence as RE
from .config import GATES_PLATFORM, PRODCORR_CEILING

#: 同一堵墙至少挡住几条才算「本波的共同瓶颈」。2 是能把「共同」与「个案」分开的最小值：1 条卡住是那条 alpha 自己的事，
#: 论坛没有针对单条表达式的答案；≥2 条同墙才谈得上「这个数据集在这堵墙上有系统性问题」。不是统计推导，也不随波大小缩放——
#: 波再大，能否找到破墙配方看的是有没有同一堵墙，而不是占比。
MIN_ROWS = 2

#: 强度线的数值兜底（与 `submit_queue.is_pass` 同口径，单一事实源 = `wqb.config.GATES_PLATFORM`）
SHARPE_MIN = float(GATES_PLATFORM["sharpe_min"])
FITNESS_MIN = float(GATES_PLATFORM["fitness_min"])

#: RA 资格门闸名 → 墙。词汇与 step7 §7.3 / `forum-recon-triggers.md` 的「prod / 2Y / CW / tvr / robust」一致，
#: 另有 `SUB`（子宇宙）与 `sharpe`（强度）——是同一张 RA 闸表（`wqb.config.RA_CHECK_NAMES`）里的其余项。
#: 与 `RA_CHECK_NAMES` 的一一对应由 `tests/unit/08_forum_recon/test_recon_wave.py` 守护：config 新增一项 RA 闸而这里没给它墙，测试即红。
WALL_BY_CHECK: Dict[str, str] = {
    "LOW_SHARPE": "sharpe", "LOW_FITNESS": "sharpe", "LOW_RETURNS": "sharpe",
    "LOW_GLB_AMER_SHARPE": "sharpe", "LOW_GLB_APAC_SHARPE": "sharpe", "LOW_GLB_EMEA_SHARPE": "sharpe",
    "LOW_ASI_JPN_SHARPE": "sharpe",
    "LOW_2Y_SHARPE": "2Y", "IS_LADDER_SHARPE": "2Y",
    "LOW_SUB_UNIVERSE_SHARPE": "SUB",
    "LOW_ROBUST_UNIVERSE_SHARPE": "robust", "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO": "robust",
    "LOW_ROBUST_UNIVERSE_RETURNS": "robust", "LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE": "robust",
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE": "robust",
    "HIGH_TURNOVER": "tvr", "LOW_TURNOVER": "tvr",
    "CONCENTRATED_WEIGHT": "CW",
}

#: 强度墙：过不了它的行是 `weak`（缺想法，不是缺破墙配方），不参与选墙。
STRENGTH_WALL = "sharpe"

#: 并列时的选墙顺序（越是「改表达式细节绕不开」的越靠前）：prod 是相关性硬墙、2Y / CW 是结构性缺陷，
#: robust / SUB 次之，tvr 通常可用 decay / 平滑调回，最后。
WALL_PRIORITY = ("prod", "2Y", "CW", "robust", "SUB", "tvr")

#: 墙在问题文本里的说法（英文缩写 + 中文名：论坛以中文帖为主，光有缩写搜不到东西）
WALL_TITLE: Dict[str, str] = {
    "prod": "prod 相关性墙", "2Y": "2Y 稳健性墙", "CW": "CW 权重集中墙",
    "robust": "robust 稳健宇宙墙", "SUB": "SUB 子宇宙墙", "tvr": "tvr 换手墙",
}

KIND_WALL = "wall"
KIND_DEAD_END = "dead_end"

#: 不问的原因码
SKIP_NO_ROWS = "no_rows"
SKIP_NO_DATASET = "no_dataset"
SKIP_TOO_FEW = "too_few_rows"
SKIP_NOTHING = "nothing_to_ask"
SKIP_DONE = "already_done"


# ----------------------------------------------------------------------------- 行分类
def failed_names(value: Any) -> Optional[List[str]]:
    """`ra_failed_checks` 列 → RA 失败项名列表；NULL / 无法解析 → None（说不清），空列表 = RA 全过。"""
    v = value
    if isinstance(v, (str, bytes)):
        s = v.decode("utf-8", "replace") if isinstance(v, bytes) else v
        if not s.strip():
            return None
        try:
            v = json.loads(s)
        except ValueError:
            return None
    if v is None or not isinstance(v, (list, tuple)):
        return None
    names = [x.get("name") if isinstance(x, dict) else x for x in v]
    return [n for n in names if isinstance(n, str) and n]


def _num(x: Any) -> Optional[float]:
    try:
        return None if x is None or x == "" else float(x)
    except (TypeError, ValueError):
        return None


def classify_row(row: Dict[str, Any], prod_ceiling: float = PRODCORR_CEILING) -> Dict[str, Any]:
    """一条回测行 → `{"category": pass|blocked|weak|none, "walls": [...]}`（`none` = 没有指标，不参与）。"""
    sharpe = _num(row.get("sharpe"))
    if sharpe is None:
        return {"category": "none", "walls": []}
    walls: List[str] = []
    for n in failed_names(row.get("ra_failed_checks")) or []:        # NULL 与 [] 同义：store 把「RA 全过」也存成 NULL
        w = WALL_BY_CHECK.get(n)
        if w and w not in walls:
            walls.append(w)
    fitness = _num(row.get("fitness"))
    if sharpe < SHARPE_MIN or (fitness is not None and fitness < FITNESS_MIN):
        if STRENGTH_WALL not in walls:                                # 名单没带强度项（旧行）时数值也算数
            walls.append(STRENGTH_WALL)
    prod = _num(row.get("prod_correlation"))
    if prod is not None and prod >= prod_ceiling and "prod" not in walls:
        walls.append("prod")
    if STRENGTH_WALL in walls:
        return {"category": "weak", "walls": walls}
    return {"category": "blocked" if walls else "pass", "walls": walls}


def _dominant_wall(counts: Counter) -> Optional[str]:
    """票数最多的墙（≥ MIN_ROWS）；并列按 `WALL_PRIORITY`。"""
    eligible = {w: n for w, n in counts.items() if n >= MIN_ROWS and w in WALL_TITLE}
    if not eligible:
        return None
    top = max(eligible.values())
    tied = [w for w, n in eligible.items() if n == top]
    return sorted(tied, key=WALL_PRIORITY.index)[0]


def _infer_dataset(rows: Iterable[Dict[str, Any]]) -> str:
    c = Counter(str(r.get("dataset") or "").strip() for r in rows)
    c.pop("", None)
    return c.most_common(1)[0][0] if c else ""


# ----------------------------------------------------------------------------- 决策问题
def derive_decision(region: str, wave: Any, rows: List[Dict[str, Any]], dataset: Optional[str] = None,
                    prod_ceiling: float = PRODCORR_CEILING) -> Dict[str, Any]:
    """一波回测行 → 本波的决策问题。

    返回 `{"kind", "question", "question_key", "context", "wall", "dataset", "reason", "basis"}`：
    `kind` 是 `wall` / `dead_end`，或 None（不问，`reason` 给原因码）。
    """
    region = str(region or "").strip()
    basis: Dict[str, Any] = {"n_rows": len(rows), "n_evaluated": 0, "n_pass": 0, "n_blocked": 0, "n_weak": 0,
                             "wall_counts": {}}
    out: Dict[str, Any] = {"kind": None, "question": None, "question_key": None, "context": {}, "wall": None,
                           "dataset": str(dataset or "").strip(), "reason": None, "basis": basis, "wave": str(wave)}
    walls_seen: Counter = Counter()
    cats: Counter = Counter()
    evaluated: List[Dict[str, Any]] = []
    for r in rows:
        c = classify_row(r, prod_ceiling)
        if c["category"] == "none":
            continue
        evaluated.append(r)
        cats[c["category"]] += 1
        if c["category"] == "blocked":
            walls_seen.update(c["walls"])
    basis.update(n_evaluated=len(evaluated), n_pass=cats["pass"], n_blocked=cats["blocked"], n_weak=cats["weak"],
                 wall_counts=dict(walls_seen))
    if not evaluated:
        out["reason"] = SKIP_NO_ROWS
        return out
    ds = out["dataset"] or _infer_dataset(evaluated)
    if not ds:
        out["reason"] = SKIP_NO_DATASET                  # 没有数据集就没有具体问题：泛问题只会烧 token
        return out
    out["dataset"] = ds

    wall = _dominant_wall(walls_seen)
    if wall:
        out.update(kind=KIND_WALL, wall=wall, question=f"{region} {ds} {WALL_TITLE[wall]} 破墙配方",
                   context={"region": region, "dataset": ds, "wall": wall})
    elif cats["pass"] == 0 and cats["blocked"] == 0 and cats["weak"] >= MIN_ROWS:
        out.update(kind=KIND_DEAD_END, question=f"{region} {ds} 有无解法",
                   context={"region": region, "dataset": ds})
    else:
        known = cats["pass"] + cats["blocked"] + cats["weak"]
        out["reason"] = SKIP_TOO_FEW if known < MIN_ROWS else SKIP_NOTHING
        return out
    out["question_key"] = RE.question_key(out["question"])
    return out


# ----------------------------------------------------------------------------- 波标记（每波 ≤ 1 次）
def marker_status(marker: Any) -> Optional[str]:
    """`forum_recon_wave_<wave>` 标记里的结局：ok / no_result / error；不是标记返回 None。"""
    if not isinstance(marker, dict):
        return None
    s = marker.get("status")
    return s if s in (RE.STATUS_OK, RE.STATUS_NO_RESULT, RE.STATUS_ERROR) else None


def marker_blocks_rerun(marker: Any) -> bool:
    """可靠结局（有货 / 无解）占用本波额度；故障（或看不懂的标记）不占——故障 ≠ 取证。"""
    return marker_status(marker) in (RE.STATUS_OK, RE.STATUS_NO_RESULT)


def build_marker(region: str, wave: Any, decision: Dict[str, Any], outcome: Dict[str, Any], done_at: str,
                 forced: bool = False) -> Dict[str, Any]:
    """完成标记的落库值（region 作用域的 `forum_recon_wave_<wave>`）。`outcome` = `tools/forum_recon.py` 的返回。"""
    found = outcome.get("found")
    return {
        "region": region, "wave": str(wave), "dataset": decision.get("dataset"),
        "kind": decision.get("kind"), "wall": decision.get("wall"),
        "question": decision.get("question"), "question_key": decision.get("question_key"),
        "found": found, "status": RE.status_of(found),
        "sink": outcome.get("sink"), "from_cache": bool(outcome.get("from_cache")),
        "error": outcome.get("error"), "basis": decision.get("basis"),
        "forced": bool(forced), "done_at": done_at,
    }
