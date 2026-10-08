# -*- coding: utf-8 -*-
"""区域 skill 与组合分支文件的渲染（2026-10-04）。

- 每个区域一个 skill：`Claude/skills/wq-brain-ra-<区小写>/SKILL.md`（layer L-RA-R：九步骨架的区域分支）；
- 每个组合一个分支文件：同目录 `references/<平台类别>.md`。
生成块（`<!-- profiles:<名>:start -->` … `end`）只由本模块写；手写块（`profiles:manual`）重渲时原样保留；
frontmatter 只在建文件时写一次（之后改 version / last_verified 由人维护）。

数据源只有文件（不读库、不发请求，结果可复现，测试用 `render --check` 守）：
tracking/<R>/config/{settings,thresholds,cells}.json、类别卡、区域 profile front-matter、
Mode B 主闸的文件口径（不含区域台账里的自适应值——实时值看 `explain`）。
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import cards as _cards
from .cells import cell_for, config_dir_of, load_cells
from .locked import GLOBAL_FORBIDDEN, LOCKED, recommends_weighted_mix
from .taxonomy import card_of, group_of

PREFIX = "wq-brain-ra-"
LAYER = "L-RA-R"
_START = "<!-- profiles:{0}:start -->"
_END = "<!-- profiles:{0}:end -->"
_CONST_OK = " <!-- lint:const-ok 证据原文 -->"
_MIX_WARN = "⚠ 加权拼腿已被闸 5 禁止，只作历史证据："
_COUNTER = " <!-- lint:counterexample -->"


def _evidence_text(raw: Any, limit: int = 120) -> Tuple[str, str]:
    """判死 / 胜绩行的说明列：原文里是加权拼腿时加警示前缀并标反例（不能让历史配方读起来像在推荐）。"""
    text = _clean(raw)[:limit]
    if recommends_weighted_mix(str(raw or "")):
        return _MIX_WARN + text, _COUNTER
    return text, ""

#: 区域 skill 面板里展示的阈值键（S4 / S5 判定相关）
_PANEL_THRESHOLDS = ("review.sharpe_min", "review.fitness_min", "review.turnover_min", "review.turnover_max",
                     "review.two_year_sharpe_min", "review.rn_sharpe_min", "near.sharpe_min",
                     "diversity.signal_floor.max_sharpe_floor")


def skills_dir(root: Optional[Path] = None) -> Path:
    if root is None:
        from wqb.config import REPO_ROOT
        root = REPO_ROOT
    return Path(root) / "Claude" / "skills"


def skill_name(region: str) -> str:
    return PREFIX + region.lower()


def skill_dir(region: str, root: Optional[Path] = None) -> Path:
    return skills_dir(root) / skill_name(region)


# ---------------------------------------------------------------- 块操作

def get_block(text: str, name: str) -> Optional[str]:
    s, e = _START.format(name), _END.format(name)
    i, j = text.find(s), text.find(e)
    if i < 0 or j < 0 or j < i:
        return None
    return text[i + len(s):j].strip("\n")


def set_block(text: str, name: str, body: str) -> str:
    s, e = _START.format(name), _END.format(name)
    i, j = text.find(s), text.find(e)
    if i < 0 or j < 0 or j < i:
        raise ValueError(f"缺生成块标记 {s} / {e}")
    return text[:i + len(s)] + "\n" + body.rstrip("\n") + "\n" + text[j:]


def _clean(text: Any) -> str:
    """库里来的文字进表格前：去反引号（避免被当成表达式 / 路径机检）、去换行与竖线。"""
    t = str(text or "").replace("`", "'").replace("|", "／").replace("\r", " ").replace("\n", " ")
    return re.sub(r"\s+", " ", t).strip()


def _v(x: Any) -> str:
    if isinstance(x, str):
        return x
    return json.dumps(x, ensure_ascii=False)


# ---------------------------------------------------------------- 取数（只读文件）

class _NoLedger:
    def get_ledger(self, region, key):
        return None


def _profile(region: str) -> Dict[str, Any]:
    try:
        from wqb.region_profile import load_profile
        p = load_profile(region)
        return {"entry_verdict": (p.entry_verdict if p else "") or "unknown", "raw": (p.raw if p else {}) or {}}
    except Exception:  # noqa: BLE001
        return {"entry_verdict": "unknown", "raw": {}}


def _read_json(p: Path) -> Dict[str, Any]:
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return {}


def _flat(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in d.items():
        if str(k).startswith("_"):
            continue
        key = f"{prefix}.{k}" if prefix else str(k)
        if isinstance(v, dict):
            out.update(_flat(v, key))
        else:
            out[key] = v
    return out


def _mode_b(region: str, category: Optional[str] = None) -> Dict[str, Any]:
    from wqb.workflow.mode_b_config import load_mode_b_config
    cfg = load_mode_b_config(_NoLedger(), region=region, category=category)
    mg = cfg.get("main_gate") or {}
    return {"sharpe_min": mg.get("sharpe_min"), "fitness_min": mg.get("fitness_min"),
            "source": cfg.get("_source"), "clamped_from": cfg.get("_clamped_from")}


def _platform_facts(region: str) -> List[str]:
    from wqb.config import is_multi_country
    facts = [f"宇宙{'跨多个国家' if is_multi_country(region) else '是单一国家'}"
             f"（config.REGION_COUNTRY_SCOPE）：country 轴中性化 / 分组{'有意义' if is_multi_country(region) else '等于全市场，别用'}"]
    try:
        from wqb.config import REPO_ROOT
        pc = json.loads((REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "config"
                         / "platform_constraints.json").read_text(encoding="utf-8"))
        bad_groups = (pc.get("region_invalid_group_fields") or {}).get(region.upper())
        if bad_groups:
            facts.append(f"平台不支持的分组字段：{', '.join(bad_groups)}（闸 2b 拦，platform_constraints.json）")
        bad_fields = (pc.get("region_invalid_fields") or {}).get(region.upper())
        if bad_fields:
            facts.append(f"本区不可用的基础字段：{', '.join(bad_fields[:10])}{' …' if len(bad_fields) > 10 else ''}"
                         "（platform_constraints.json）")
        if region.upper() in (pc.get("region_vector_ts_forbidden") or []):
            facts.append("VECTOR 字段聚合后不能再套 ts_* 算子（platform_constraints.json region_vector_ts_forbidden）")
    except Exception:  # noqa: BLE001
        pass
    return facts


# ---------------------------------------------------------------- 区域 skill

def _frontmatter(region: str) -> str:
    r = region.upper()
    desc = (f"在 {r} 区挖 REGULAR alpha、调 {r} 的回测设置或阈值、查 {r} 某类数据集（区域 × 类别组合）的配方与禁区时使用："
            f"{r} 的区域分支流程与回测把控面板。通用九步走 wq-brain-ra-pipeline，判提交与提交走 worldquant-submit-alpha。")
    today = _dt.date.today().isoformat()
    return ("---\n"
            f"name: {skill_name(r)}\n"
            f"description: \"{desc}\"\n"
            f"layer: {LAYER}\n"
            "allowed-tools:\n  - Read\n  - Bash\n  - mcp__wqb-db__*\n  - mcp__wq-brain-http__*\n"
            "version: \"1.0\"\n"
            f"last_verified: {today}\n"
            "---\n")


def _skeleton(region: str) -> str:
    r = region.upper()
    return f"""
# {r} 区域挖掘流程（RA 区域分支）

## 职责边界

- **本 skill 负责**：{r} 的区域分支——入场状态、回测把控（区域与「区域 × 类别」组合的回测设置 / 阈值 / Mode B 主闸，每个值可查来源）、S1 / S2 / S4 / S5 的 {r} 差异步骤、组合分支文件索引。
- **本 skill 不做**：九步通用正文（→ [`wq-brain-ra-pipeline`](../wq-brain-ra-pipeline/SKILL.md)）；选区（→ `brain-next-move-analysis`）；判提交与提交（`submit_verdict` 只否决，提交走 `worldquant-submit-alpha` 且必须用户确认）；不改其它区域的控制文件。
- **上游 / 下游**：上游 = 用户点名 {r}，或 `wq-brain-ra-pipeline` 步 1 路由到本区；下游 = `wq-brain-ra-pipeline` 各步、`wq-brain-campaign-toolkit` 引擎、`wq-brain-alpha-optimization-v1`（S4 改进）。

## 怎么用

1. **入场**：看下面「区域控制面板」的入场状态。`frozen` 只走 profile 写明的后门；`probe-only` 只许探针批。
2. **每次回测前**按数据集取生效画像（回测设置、阈值、Mode B 主闸、生成与改进要点，每项带来源）：

   ```bash
   $WQ_PY -m wqb.profiles explain --region {r} --dataset <dataset>
   ```

   `workflow_batch_track` 会把该组合的回测覆盖以 `--set` 钉住；直接用 MCP 发仿真（`create_multi_simulation` / `create_simulation`）时，按 explain 输出逐项传设置，不要依赖工具缺省（各入口缺省不同，换档等于换信号）。
3. **走九步**：按 `wq-brain-ra-pipeline` 执行；步 3 / 4 / 7 / 8 先读对应组合的分支文件（下表最后一列）。
4. **步 9 回写之后**刷新组合证据并重渲本 skill：

   ```bash
   $WQ_PY -m wqb.profiles sync-cells --region {r} --apply
   $WQ_PY -m wqb.profiles render --region {r} --apply
   ```

## 区域控制面板

{_START.format('region-panel')}
{_END.format('region-panel')}

## 组合分支（区域 × 类别）

{_START.format('cells-index')}
{_END.format('cells-index')}

## 本区流程差异（相对九步骨架）

{_START.format('manual')}
{_END.format('manual')}

## 改控制

- **区域级**：`tracking/{r}/config/settings.json`（仿真设置）、`tracking/{r}/config/thresholds.json`（阈值）。
- **组合级**：`tracking/{r}/config/cells.json`——只写覆盖值，每个覆盖在同级 `_evidence` 写证据（波号 / alpha id / 日期）；没有证据的覆盖校验不通过。改完先校验再重渲：

  ```bash
  $WQ_PY -m wqb.profiles check --region {r}
  $WQ_PY -m wqb.profiles render --region {r} --apply
  ```

- **锁定项**（任何层都不能放宽）：禁混信号、Mode B 主闸下限、决策表 D0-P、平台线、窗口白名单、点塔按平台类别、提交前用户确认、truncation 不作扫描维度——全文见 `$WQ_PY -m wqb.profiles explain` 末尾。
- **证据与历史**：[{r} profile](../wq-brain-ra-pipeline/references/regions/{r}.md)（入场裁决、红绿榜、证据附录）。
""".lstrip("\n")


def _region_panel(region: str) -> str:
    r = region.upper()
    cdir = config_dir_of(r)
    settings = _read_json(cdir / "settings.json")
    thresholds = _flat(_read_json(cdir / "thresholds.json"))
    prof = _profile(r)
    raw = prof["raw"]
    L: List[str] = []
    one = _clean(raw.get("one_liner") or "")
    L.append(f"**入场状态**：`{prof['entry_verdict']}`" + (f"　{one}" if one else ""))
    L.append("")
    if not settings:
        L.append(f"> 本区没有战役目录（`tracking/{r}/config/` 缺 settings.json）：开新区前先补 settings.json / thresholds.json，"
                 "见 INDEX「开新区检查表」。")
        L.append("")
    else:
        L.append("| 回测设置 | 值 | 来源 |")
        L.append("|---|---|---|")
        for k, v in settings.items():
            if not str(k).startswith("_"):
                L.append(f"| {k} | {_v(v)} | settings.json |")
        L.append("")
    mb = _mode_b(r)
    clamp = f"；被钳掉的原值 {_v(mb['clamped_from'])}" if mb.get("clamped_from") else ""
    L.append("| 阈值 | 值 | 来源 |")
    L.append("|---|---|---|")
    L.append(f"| Mode B 主闸（sharpe / fitness） | {mb['sharpe_min']} / {mb['fitness_min']} | {mb['source']}{clamp}（实时值含区域台账，看 explain） |")
    for k in _PANEL_THRESHOLDS:
        if k in thresholds:
            L.append(f"| {k} | {_v(thresholds[k])} | thresholds.json |")
    L.append("")
    lp = raw.get("loop_policy") or {}
    go = raw.get("gate_overrides") or {}
    if lp or go:
        L.append("**循环与闸门（profile front-matter）**")
        if lp.get("max_probes_per_wave") is not None:
            L.append(f"- 每波探针位上限：{_clean(lp.get('max_probes_per_wave'))}")
        if lp.get("fast_kill"):
            L.append(f"- 快判死：{_clean(lp.get('fast_kill'))}")
        for sc in lp.get("stop_conditions") or []:
            L.append(f"- 停止条件：{_clean(sc)}")
        if go:
            items = "、".join(f"{k}={_clean(v)}" for k, v in go.items())
            L.append(f"- 闸门特化（文档级）：{items}——代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判），按此执行由 agent 负责")
        L.append("")
    L.append("**平台事实**")
    for f in _platform_facts(r):
        L.append(f"- {f}")
    return "\n".join(L)


def _cells_index(region: str) -> str:
    r = region.upper()
    data = load_cells(r)
    cells = data.get("cells") or {}
    if not cells:
        return ("本区还没有组合文件（`tracking/{0}/config/cells.json` 不存在或为空）：所有类别跟区域缺省。"
                "有回测证据后跑 `$WQ_PY -m wqb.profiles sync-cells --region {0} --apply`。").format(r)
    verdict = _profile(r)["entry_verdict"]
    from .resolver import _cell_status
    L = ["| 类别 | 分组 | 状态 | 回测覆盖 | 阈值覆盖 | 回测 / RA 全过 | prod 已测（低于上限） | 判死 / 胜绩 | 分支文件 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for cat in sorted(cells, key=lambda c: -((cells[c].get("evidence") or {}).get("backtests") or 0)):
        c = cells[cat]
        ev = c.get("evidence") or {}
        bt = (c.get("backtest") or {}).get("overrides") or {}
        th = (c.get("thresholds") or {}).get("overrides") or {}
        bt_s = "、".join(f"{k}={_v(v)}" for k, v in bt.items()) or "—"
        th_s = "、".join(f"{k}={_v(v)}" for k, v in th.items()) or "—"
        L.append(f"| {cat} | {group_of(cat)} | {_cell_status(c, verdict)} | {bt_s} | {th_s} | "
                 f"{ev.get('backtests', 0)} / {ev.get('ra_clean', 0)} | {ev.get('prod_measured', 0)}（{ev.get('prod_clean', 0)}） | "
                 f"{len(ev.get('dead_ends') or [])} / {len(ev.get('wins') or [])} | [references/{cat}.md](references/{cat}.md) |")
    extra = []
    if data.get("unattributed_backtests"):
        extra.append(f"另有 {data['unattributed_backtests']} 条回测行没写数据集，无法归到组合")
    if data.get("unbound_registry_entries"):
        extra.append(f"{data['unbound_registry_entries']} 条判死 / 胜绩连类别也推断不出")
    if data.get("evidence_synced_at"):
        extra.append(f"证据于 {data['evidence_synced_at']} 只读汇总")
    if extra:
        L.append("")
        L.append("说明：" + "；".join(extra) + "。")
    return "\n".join(L)


# ---------------------------------------------------------------- 组合分支文件

def _cell_skeleton(region: str, category: str) -> str:
    r = region.upper()
    return f"""# {r} × {category}（组合分支）

> 回到 [{r} 区域流程](../SKILL.md) · [{r} profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/{r}.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region {r} --category {category}`

{_START.format('cell-panel')}
{_END.format('cell-panel')}

## 补充说明（手写）

{_START.format('manual')}
{_END.format('manual')}
"""


def _cell_panel(region: str, category: str) -> str:
    r = region.upper()
    cdir = config_dir_of(r)
    settings = _read_json(cdir / "settings.json")
    cell = cell_for(r, category, cdir)
    verdict = _profile(r)["entry_verdict"]
    from .resolver import _cell_status
    cid = card_of(category)
    card = _cards.card(cid)
    glob = _cards.global_section()
    ev = cell.get("evidence") or {}
    L: List[str] = []
    st = _cell_status(cell, verdict)
    L.append(f"**状态**：{st}{'（跟区域入场 ' + verdict + '）' if (cell.get('status') or 'auto') == 'auto' else '（' + _clean(cell.get('status_note')) + '）'}"
             f"　**分组**：{group_of(category)}　**类别卡**：{cid}")
    if cell.get("note"):
        L.append(f"\n**备注**：{_clean(cell['note'])}")
    if cell.get("datasets"):
        L.append(f"\n**涉及数据集**：{'、'.join(cell['datasets'][:20])}{' …' if len(cell['datasets']) > 20 else ''}")
    # 回测设置
    bt = cell.get("backtest") or {}
    ov, oe = bt.get("overrides") or {}, bt.get("_evidence") or {}
    L.append("\n### 回测设置（进仿真的值）\n")
    if settings:
        L.append("| 设置 | 值 | 来源 |")
        L.append("|---|---|---|")
        for k, v in settings.items():
            if str(k).startswith("_") or k in ov:
                continue
            L.append(f"| {k} | {_v(v)} | 区域 settings.json |")
        for k, v in ov.items():
            L.append(f"| {k} | {_v(v)} | **本组合覆盖**（区域值 {_v(settings.get(k))}；证据：{_clean(oe.get(k))}） |")
    else:
        L.append("本区没有 settings.json。")
    # 阈值
    th = cell.get("thresholds") or {}
    tov, tev = th.get("overrides") or {}, th.get("_evidence") or {}
    mb = _mode_b(r, category)
    L.append("\n### 阈值\n")
    L.append(f"- Mode B 主闸 sharpe / fitness：{mb['sharpe_min']} / {mb['fitness_min']}（{mb['source']}；下限锁生效，实时值看 explain）")
    if tov:
        for k, v in tov.items():
            L.append(f"- 本组合覆盖 {k} = {_v(v)}（证据：{_clean(tev.get(k))}）")
    else:
        L.append("- 其余阈值跟区域 thresholds.json（本组合无覆盖）")
    # 证据
    if ev:
        L.append(f"\n### 证据（{ev.get('synced_at')} 只读汇总）\n")
        L.append("| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |")
        L.append("|---|---|---|---|---|---|")
        L.append(f"| {ev.get('backtests', 0)} | {ev.get('ra_clean', 0)} | {ev.get('prod_measured', 0)} | "
                 f"{ev.get('prod_clean', 0)} | {len(ev.get('dead_ends') or [])} | {len(ev.get('wins') or [])} |")
        tops = ev.get("top_datasets") or []
        if tops:
            L.append("\n主要数据集（回测数）：" + "、".join(f"{t['dataset']}（{t['backtests']}）" for t in tops))
    # S1
    L.append("\n### S1 字段理解\n")
    hints = list(card.get("s1_hints") or [])
    L += [f"- {_clean(h)}" for h in hints] or ["- （类别卡未写）"]
    if card.get("windows"):
        L.append("- 窗口（类别卡，均在白名单内）：" + "；".join(f"{k} {'/'.join(str(w) for w in ws)}"
                                                    for k, ws in card["windows"].items()))
    # S2
    gen = cell.get("generation") or {}
    L.append("\n### S2 生成\n")
    for x in gen.get("use") or []:
        L.append(f"- **用**：{_clean(x)}")
    for x in gen.get("avoid") or []:
        L.append(f"- **避**：{_clean(x)}")
    for x in gen.get("notes") or []:
        L.append(f"- **说明**：{_clean(x)}")
    sks = gen.get("skeletons") or []
    if sks:
        L.append("- **已验证骨架**（证据见每行注释；照抄前先按本组合当前 prod 复核）：")
        L.append("")
        L.append("  ```text")
        for s in sks:
            L.append(f"  {s.get('text')}")
        L.append("  ```")
        L.append("")
        for s in sks:
            L.append(f"  - {_clean(s.get('text'))[:60]}… ← {_clean(s.get('evidence'))}"
                     + (f"；窗口说明：{_clean(s.get('window_note'))}" if s.get("window_note") else ""))
    if card.get("primitives"):
        L.append("- **类别通用原语**（类别卡，跨区）：")
        L += [f"  - {_clean(p)}" for p in card["primitives"]]
    for e in card.get("cross_region") or []:
        L.append(f"- **跨区结论**（{'/'.join(e.get('regions', []))}；{_clean(e.get('type') or '')}）：{_clean(e.get('what'))}"
                 f"（证据：{_clean(e.get('evidence'))}）{_CONST_OK}")
    for x in card.get("forbidden") or []:
        L.append(f"- **禁止**（类别卡）：{_clean(x)}")
    for x in GLOBAL_FORBIDDEN:
        L.append(f"- **禁止**（全局锁定）：{_clean(x)}")
    # S4
    s4 = cell.get("s4") or {}
    L.append("\n### S4 改进（按顺序试：组合 → 类别卡 → 全局）\n")
    n = 0
    for lv in s4.get("levers") or []:
        n += 1
        tag = "；禁外推（只在本区用）" if lv.get("no_extrapolate") else ""
        L.append(f"{n}. [组合] {_clean(lv.get('what'))}（证据：{_clean(lv.get('evidence'))}{tag}）{_CONST_OK}")
    for lv in list(card.get("s4_levers") or []) + list(glob.get("s4_levers") or []):
        n += 1
        scope = "类别卡" if lv in (card.get("s4_levers") or []) else "全局"
        L.append(f"{n}. [{scope}] {_clean(lv.get('what'))}（{'/'.join(lv.get('regions', []))} 复现：{_clean(lv.get('evidence'))}）{_CONST_OK}")
        if lv.get("precondition"):
            L.append(f"   - 前提：{_clean(lv['precondition'])}")
        if lv.get("note"):
            L.append(f"   - 注意：{_clean(lv['note'])}")
    for a in s4.get("avoid") or []:
        L.append(f"- **不要用**：{_clean(a.get('what'))}（{_clean(a.get('evidence'))}）{_CONST_OK}")
    for x in glob.get("notes") or []:
        L.append(f"- 提醒：{_clean(x)}{_CONST_OK}")
    # S5
    L.append("\n### S5 提交前\n")
    L.append("- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region "
             f"{r} --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）")
    L.append("- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；"
             "用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`")
    # 判死 / 胜绩
    deads = ev.get("dead_ends") or []
    if deads:
        L.append("\n### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）\n")
        L.append("| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |")
        L.append("|---|---|---|---|---|")
        for d in deads:
            text, mark = _evidence_text(d.get("text"))
            L.append(f"| {_clean(d.get('id'))} | {_clean(d.get('family'))[:60]} | {text} | "
                     f"{_clean(d.get('dataset') or '—')} | {d.get('bound')} |{_CONST_OK}{mark}")
    wins = ev.get("wins") or []
    if wins:
        L.append("\n### 胜绩\n")
        L.append("| 条目 | 机制 | 设置与骨架 | 数据集 | 归属 |")
        L.append("|---|---|---|---|---|")
        for w in wins:
            text, mark = _evidence_text(w.get("text"))
            L.append(f"| {_clean(w.get('id'))} | {_clean(w.get('family'))[:60]} | {text} | "
                     f"{_clean(w.get('dataset') or '—')} | {w.get('bound')} |{_CONST_OK}{mark}")
    return "\n".join(L)


# ---------------------------------------------------------------- 计划 / 执行 / 校验

def _regions(regions: Optional[List[str]]) -> List[str]:
    from wqb.config import REGIONS
    return [r.upper() for r in (regions or sorted(REGIONS))]


def plan(regions: Optional[List[str]] = None, seed_manual: Optional[Dict[str, str]] = None,
         seed_cell_manual: Optional[Dict[Tuple[str, str], str]] = None) -> List[Tuple[Path, Optional[str], str]]:
    """返回 (路径, 旧内容或 None, 新内容) 列表；不写盘。"""
    out: List[Tuple[Path, Optional[str], str]] = []
    for r in _regions(regions):
        d = skill_dir(r)
        p = d / "SKILL.md"
        old = p.read_text(encoding="utf-8") if p.exists() else None
        text = old if old is not None else _frontmatter(r) + "\n" + _skeleton(r)
        text = set_block(text, "region-panel", _region_panel(r))
        text = set_block(text, "cells-index", _cells_index(r))
        if old is None or get_block(old, "manual") in (None, ""):
            seed = (seed_manual or {}).get(r)
            if seed:
                text = set_block(text, "manual", seed)
        out.append((p, old, text))
        for cat in sorted((load_cells(r).get("cells") or {})):
            cp = d / "references" / f"{cat}.md"
            cold = cp.read_text(encoding="utf-8") if cp.exists() else None
            ctext = cold if cold is not None else _cell_skeleton(r, cat)
            ctext = set_block(ctext, "cell-panel", _cell_panel(r, cat))
            if cold is None or get_block(cold, "manual") in (None, ""):
                seed = (seed_cell_manual or {}).get((r, cat))
                if seed:
                    ctext = set_block(ctext, "manual", seed)
            out.append((cp, cold, ctext))
    return out


def apply(items: List[Tuple[Path, Optional[str], str]]) -> List[Path]:
    written = []
    for p, old, new in items:
        if old == new:
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(new, encoding="utf-8", newline="\n")
        written.append(p)
    return written


# ★ `references/` 下以 `_` 开头的 .md 是「跨类别补充文档」（如 `_field-profile.md`），
#   不是「区域 × 类别」的组合分支文件 ⇒ 孤儿检查必须跳过它们，否则跨类别文档永远报孤儿。
SUPPLEMENTARY_PREFIX = "_"


def _is_supplementary(ref_md) -> bool:
    """该 references/*.md 是否为跨类别补充文档（`_` 前缀）而非组合分支文件。"""
    return ref_md.name.startswith(SUPPLEMENTARY_PREFIX)


def check_structure(regions: Optional[List[str]] = None) -> List[str]:
    """轻量校验（测试用）：skill 与组合分支文件齐全、生成块标记在、无孤儿；区域面板里的回测设置与 settings.json 一致。

    不比对整块文字——thresholds.json 会被 `score_datasets --calibrate` 自动改写，整块比对会让别的工作流的
    提交无端变红；整块是否最新由 `$WQ_PY -m wqb.profiles check` 在步 9 核对。
    """
    problems: List[str] = []
    for r in _regions(regions):
        d = skill_dir(r)
        p = d / "SKILL.md"
        if not p.exists():
            problems.append(f"缺区域 skill：{p}")
            continue
        text = p.read_text(encoding="utf-8")
        for name in ("region-panel", "cells-index", "manual"):
            if get_block(text, name) is None:
                problems.append(f"{p}: 缺生成块 {name}")
        if f"name: {skill_name(r)}" not in text:
            problems.append(f"{p}: frontmatter name 不是 {skill_name(r)}")
        settings = _read_json(config_dir_of(r) / "settings.json")
        panel = get_block(text, "region-panel") or ""
        for k, v in settings.items():
            if not str(k).startswith("_") and f"| {k} | {_v(v)} | settings.json |" not in panel:
                problems.append(f"{p}: 面板里的 {k} 与 settings.json（{_v(v)}）不一致——跑 render --region {r} --apply")
        cats = set(load_cells(r).get("cells") or {})
        refs = d / "references"
        for cat in cats:
            cp = refs / f"{cat}.md"
            if not cp.exists():
                problems.append(f"缺组合分支文件：{cp}")
            elif get_block(cp.read_text(encoding="utf-8"), "cell-panel") is None:
                problems.append(f"{cp}: 缺生成块 cell-panel")
        if refs.is_dir():
            for f in refs.glob("*.md"):
                if _is_supplementary(f):
                    continue
                if f.stem not in cats:
                    problems.append(f"孤儿分支文件：{f}")
    return problems


def check(regions: Optional[List[str]] = None) -> List[str]:
    """生成块是否最新、组合文件是否齐、有没有孤儿分支文件；返回问题列表。"""
    problems: List[str] = []
    for p, old, new in plan(regions):
        if old is None:
            problems.append(f"缺文件：{p}")
        elif old != new:
            problems.append(f"生成块过期：{p}（跑 $WQ_PY -m wqb.profiles render --apply）")
    for r in _regions(regions):
        refs = skill_dir(r) / "references"
        cats = set(load_cells(r).get("cells") or {})
        if refs.is_dir():
            for f in refs.glob("*.md"):
                if _is_supplementary(f):
                    continue
                if f.stem not in cats:
                    problems.append(f"孤儿分支文件：{f}（cells.json 里已没有 {f.stem}；确认后删除）")
    return problems
