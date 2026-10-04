# -*- coding: utf-8 -*-
"""Mode B 资格线统一加载器与判定（2026-09-09 主闸+旁路结构落地）.

背景：2026-09-09 用户明令把 Mode B 资格线从「双标量闸门」（sharpe/fitness）
升级为「主闸 + 5 旁路 + 判死线」结构，并上收为 ledger_kv GLOBAL/mode_b_qualification
全局权威。区域 thresholds.json 的 mode_b_qualification 节改为 `$ref` 引用全局 +
`_overrides` 单字段覆盖。

本模块是所有消费点（judge.py / probe_batch_mode.py / mode_b_adaptive.py）的唯一
加载与判定入口，避免各处散落硬编码与重复 $ref 解析。

配置优先级（高 → 低；区域层只能改主闸 sharpe_min/fitness_min，旁路与判死线只来自 3/4）：
  1. 区域 ledger_kv  <region>/mode_b_qualification（自适应学习写的主闸值）
  2. 区域 thresholds.json 的 mode_b_qualification（_overrides 单字段覆盖；无 $ref 的旧结构直接读顶层
     sharpe_min/fitness_min）
  3. 全局 ledger_kv  GLOBAL/mode_b_qualification（权威主闸+旁路+判死线）
  4. 内置默认 _DEFAULT_GLOBAL（主闸 1.25/0.8）
  （2026-09-29 更正：此前 2/3 的先后与 load_mode_b_config 的实际覆盖顺序相反；由
  tests/unit/07_docs_skills/test_mode_b_qualification_doc.py 钉住。）
  0. 区域 × 类别组合（tracking/<R>/config/cells.json 的 thresholds.overrides 里
     `mode_b.sharpe_min` / `mode_b.fitness_min`，仅在调用方传 category 时生效）

下限锁（2026-10-04，用户把「资格线 sharpe≥1.25 且 fitness≥0.8」列为不可违反的纪律）：
  第 3/4 层（GLOBAL 台账 / 内置默认）的主闸就是下限。第 0/1/2 层只能把主闸往上收，
  写得更低的值在读取时被钳回下限，原值留在 `_clamped_from`（不写库、不改文件）。
  此前 7 个区的生效值低于下限（ASI/CHN/GBR/HKG/MEA 1.2/0.8、GLB/USA 1.0/0.6、EUR 区域台账
  自适应学到的 1.15/0.68），见 docs/plans/2026-10-04-ra-region-category-split.md §2.3。

判定模型：
  - 主闸：sharpe≥sharpe_min AND fitness≥fitness_min → 直接放行
  - 旁路 A-E：单项短板/2Y 强苗子，满足任一即放行并绑定 mode_b_action
  - 判死线：2Y<1.2 AND sharpe<主闸 AND fitness<主闸 → 判死（旁路不救）
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# 内置默认（与全局权威主闸一致；旁路/判死线的兜底在 _DEFAULT_GLOBAL）
_DEFAULT_MAIN = {"sharpe_min": 1.25, "fitness_min": 0.8}

# 全局权威兜底（ledger 不可读时的硬编码备份，与 GLOBAL/mode_b_qualification 同步）
_DEFAULT_GLOBAL: Dict[str, Any] = {
    "main_gate": {"sharpe_min": 1.25, "fitness_min": 0.8},
    "bypass_rules": {
        "A_robust_strong": {
            "condition": "robust_sharpe >= 1.0 AND sharpe >= 0.8",
            "robust_sharpe_min": 1.0, "sharpe_min": 0.8,
            "mode_b_action": "降 turnover / 换平滑几何（ts_mean/ts_decay_linear）",
        },
        "B_prod_corr_only": {
            "condition": "prod_corr >= 0.7 AND 其余维度全达标",
            "prod_corr_min": 0.7,
            "mode_b_action": "换字段组合 / 换信号概念（禁止调权重）",
        },
        "C_margin_strong": {
            "condition": "margin >= 0.0005 AND sharpe >= 1.0",
            "margin_min": 0.0005, "sharpe_min": 1.0,
            "mode_b_action": "找正交腿组合（跨周期/跨逻辑）",
        },
        "D_turnover_fixable": {
            "condition": "returns >= returns_median_of_dataset AND turnover > 0.7",
            "turnover_min": 0.7,  # returns 阈值动态标定
            "mode_b_action": "换平滑几何 / 降频 / 换聚合算子",
        },
        "E_2y_strong": {
            "condition": "two_year_sharpe >= 1.2 AND sharpe >= 0.8",
            "two_year_sharpe_min": 1.2, "sharpe_min": 0.8,
            "mode_b_action": "补短期腿（跨周期正交）或换中性化域提 IS",
        },
    },
    "hard_kill": {
        "two_year_sharpe_max": 1.2,  # 2Y < 此值才可能判死
        "_doc": "2Y 也弱且 S/F 双弱即判死；2Y 强（≥1.2）永不判死（走旁路 E）",
    },
}


def _thresholds_path(region: str) -> str:
    """区域 thresholds.json 路径（与 judge.py 现有约定一致）。"""
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..",
        "tracking", region, "config", "thresholds.json",
    ))


def _read_ledger(store, region: str) -> Optional[Dict[str, Any]]:
    if not store:
        return None
    try:
        v = store.get_ledger(region, "mode_b_qualification")
        return v if isinstance(v, dict) else None
    except Exception:
        return None


def _read_thresholds_file(region: str) -> Optional[Dict[str, Any]]:
    try:
        p = _thresholds_path(region)
        if not os.path.exists(p):
            return None
        with open(p, "r", encoding="utf-8") as f:
            mbq = json.load(f).get("mode_b_qualification", {})
        return mbq if isinstance(mbq, dict) else None
    except Exception as e:
        logger.warning(f"read thresholds.json mode_b_qualification for {region} failed: {e}")
        return None


def _gate_value(gate: Dict[str, Any], key: str) -> float:
    try:
        return float(gate.get(key, _DEFAULT_MAIN[key]))
    except (TypeError, ValueError):
        return float(_DEFAULT_MAIN[key])


def _read_cell_override(region: str, category: Optional[str]) -> Dict[str, float]:
    """区域 × 类别组合对主闸的覆盖（cells.json；缺文件 / 缺组合 / 解析失败一律返回空）。"""
    if not category:
        return {}
    try:
        from wqb.profiles.cells import cell_threshold_overrides
        ov = cell_threshold_overrides(region, category,
                                      config_dir=os.path.dirname(_thresholds_path(region)))
    except Exception as e:  # noqa: BLE001 — 组合覆盖是增强层，读不到不影响区域口径
        logger.warning(f"read cells.json mode_b overrides for {region}/{category} failed: {e}")
        return {}
    out = {}
    for k in ("sharpe_min", "fitness_min"):
        v = ov.get(f"mode_b.{k}")
        if v is not None:
            try:
                out[k] = float(v)
            except (TypeError, ValueError):
                pass
    return out


def load_mode_b_config(store, region: str = "KOR", category: Optional[str] = None) -> Dict[str, Any]:
    """加载本区域（可选：区域 × 类别组合）生效的 Mode B 完整配置（主闸 + 旁路 + 判死线）.

    解析顺序：
      1. 全局权威（GLOBAL ledger，缺省用 _DEFAULT_GLOBAL）——其主闸同时是**下限**
      2. 区域 thresholds.json 的 _overrides 单字段覆盖（主闸/旁路阈值）
      3. 区域 ledger 的主闸 sharpe_min/fitness_min 覆盖（自适应学习写入）
      4. 组合覆盖（category 非空时，读 cells.json）
      5. 下限钳制：低于第 1 步主闸的值钳回下限，原值记 `_clamped_from`

    返回结构：
      {
        "main_gate": {"sharpe_min": float, "fitness_min": float},
        "bypass_rules": {...},   # 5 条旁路（含数值阈值字段）
        "hard_kill": {"two_year_sharpe_max": float},
        "_source": str,          # 主闸值来源（调试用）
        "_floor": {...},         # 主闸下限（= 第 1 步的主闸）
        "_clamped_from": {...},  # 仅当有覆盖值低于下限时出现
      }
    """
    # 1. 全局权威基底
    base = _read_ledger(store, "GLOBAL") or _DEFAULT_GLOBAL
    cfg: Dict[str, Any] = {
        "main_gate": dict(base.get("main_gate") or _DEFAULT_GLOBAL["main_gate"]),
        "bypass_rules": dict(base.get("bypass_rules") or _DEFAULT_GLOBAL["bypass_rules"]),
        "hard_kill": dict(base.get("hard_kill") or _DEFAULT_GLOBAL["hard_kill"]),
        "_source": "GLOBAL_ledger" if _read_ledger(store, "GLOBAL") else "default",
    }
    floor = {k: _gate_value(cfg["main_gate"], k) for k in ("sharpe_min", "fitness_min")}

    # 2. 区域 thresholds.json 的 _overrides（单字段覆盖主闸）
    mbq_file = _read_thresholds_file(region)
    if mbq_file:
        overrides = mbq_file.get("_overrides") or {}
        # 兼容旧结构：无 $ref 时直接读 sharpe_min/fitness_min 作为主闸覆盖
        if "$ref" not in mbq_file:
            for k in ("sharpe_min", "fitness_min"):
                if mbq_file.get(k) is not None:
                    overrides.setdefault(k, mbq_file[k])
        for k in ("sharpe_min", "fitness_min"):
            if overrides.get(k) is not None:
                try:
                    cfg["main_gate"][k] = float(overrides[k])
                    cfg["_source"] = f"thresholds_override:{region}"
                except (TypeError, ValueError):
                    pass

    # 3. 区域 ledger 主闸覆盖（自适应学习写入，优先级最高）
    reg_ledger = _read_ledger(store, region)
    if reg_ledger:
        for k in ("sharpe_min", "fitness_min"):
            if reg_ledger.get(k) is not None:
                try:
                    cfg["main_gate"][k] = float(reg_ledger[k])
                    cfg["_source"] = f"region_ledger:{region}"
                except (TypeError, ValueError):
                    pass

    # 4. 区域 × 类别组合覆盖（cells.json，只在调用方给了 category 时读）
    cell = _read_cell_override(region, category)
    for k, v in cell.items():
        cfg["main_gate"][k] = v
        cfg["_source"] = f"cell:{region}/{category}"

    # 5. 下限钳制：任何覆盖层都只能把主闸往上收
    clamped = {}
    for k in ("sharpe_min", "fitness_min"):
        v = _gate_value(cfg["main_gate"], k)
        if v < floor[k]:
            clamped[k] = v
            cfg["main_gate"][k] = floor[k]
        else:
            cfg["main_gate"][k] = v
    cfg["_floor"] = floor
    if clamped:
        cfg["_clamped_from"] = clamped
        logger.info(f"mode_b main gate for {region}{'/' + category if category else ''} "
                    f"clamped to floor {floor} (overrides {clamped} from {cfg['_source']})")

    return cfg


def evaluate_mode_b(
    cfg: Dict[str, Any],
    *,
    sharpe: Optional[float] = None,
    fitness: Optional[float] = None,
    two_year_sharpe: Optional[float] = None,
    robust_sharpe: Optional[float] = None,
    margin: Optional[float] = None,
    turnover: Optional[float] = None,
    returns: Optional[float] = None,
    prod_corr: Optional[float] = None,
    returns_median: Optional[float] = None,
    other_dims_all_pass: Optional[bool] = None,
) -> Dict[str, Any]:
    """按主闸 + 旁路 + 判死线评估单个候选的 Mode B 资格.

    Args:
        cfg: load_mode_b_config 的返回
        sharpe/fitness/two_year_sharpe/robust_sharpe/margin/turnover/returns/prod_corr:
            候选实测指标（None 表示该维度无数据，对应旁路不命中）
        returns_median: 旁路 D 用——本数据集已测候选 returns 中位数（动态标定）
        other_dims_all_pass: 旁路 B 用——除 prod_corr 外其余维度是否全达标

    Returns:
        {
          "eligible": bool,          # 是否有 Mode B 资格
          "verdict": "main_gate"|"bypass"|"dead_end"|"no_qualify",
          "bypass": str|None,        # 命中的旁路名（A/B/C/D/E）
          "mode_b_action": str|None, # 绑定的修法方向
          "reason": str,
        }
    """
    main = cfg.get("main_gate") or _DEFAULT_MAIN
    s_min = float(main.get("sharpe_min", 1.25))
    f_min = float(main.get("fitness_min", 0.8))
    bypass = cfg.get("bypass_rules") or {}
    kill = cfg.get("hard_kill") or {}
    kill_2y = float(kill.get("two_year_sharpe_max", 1.2))

    # 主闸
    if sharpe is not None and fitness is not None and sharpe >= s_min and fitness >= f_min:
        return {"eligible": True, "verdict": "main_gate", "bypass": None,
                "mode_b_action": None,
                "reason": f"主闸达标 sharpe {sharpe:.2f}>={s_min} 且 fitness {fitness:.2f}>={f_min}"}

    # 旁路（按 A→E 顺序，首个命中即放行）
    def _hit(name: str) -> Dict[str, Any]:
        rule = bypass.get(name) or {}
        return {"eligible": True, "verdict": "bypass", "bypass": name,
                "mode_b_action": rule.get("mode_b_action"),
                "reason": f"旁路 {name} 命中：{rule.get('condition', '')}"}

    # A robust 强
    ra = bypass.get("A_robust_strong") or {}
    if (robust_sharpe is not None and sharpe is not None
            and robust_sharpe >= float(ra.get("robust_sharpe_min", 1.0))
            and sharpe >= float(ra.get("sharpe_min", 0.8))):
        return _hit("A_robust_strong")

    # B prod_corr 唯一短板
    rb = bypass.get("B_prod_corr_only") or {}
    if (prod_corr is not None and prod_corr >= float(rb.get("prod_corr_min", 0.7))
            and other_dims_all_pass is True):
        return _hit("B_prod_corr_only")

    # C margin 强
    rc = bypass.get("C_margin_strong") or {}
    if (margin is not None and sharpe is not None
            and margin >= float(rc.get("margin_min", 0.0005))
            and sharpe >= float(rc.get("sharpe_min", 1.0))):
        return _hit("C_margin_strong")

    # D turnover 可修（returns 动态中位数）
    rd = bypass.get("D_turnover_fixable") or {}
    if (returns is not None and returns_median is not None and turnover is not None
            and returns >= returns_median
            and turnover > float(rd.get("turnover_min", 0.7))):
        return _hit("D_turnover_fixable")

    # E 2Y 强
    re_ = bypass.get("E_2y_strong") or {}
    if (two_year_sharpe is not None and sharpe is not None
            and two_year_sharpe >= float(re_.get("two_year_sharpe_min", 1.2))
            and sharpe >= float(re_.get("sharpe_min", 0.8))):
        return _hit("E_2y_strong")

    # 判死线：2Y 也弱 且 S/F 双弱
    s_weak = sharpe is not None and sharpe < s_min
    f_weak = fitness is not None and fitness < f_min
    y_weak = two_year_sharpe is not None and two_year_sharpe < kill_2y
    if s_weak and f_weak and y_weak:
        return {"eligible": False, "verdict": "dead_end", "bypass": None,
                "mode_b_action": None,
                "reason": (f"判死：2Y {two_year_sharpe:.2f}<{kill_2y} 且 sharpe {sharpe:.2f}<{s_min} "
                           f"且 fitness {fitness:.2f}<{f_min}（三项同弱，旁路不救）")}

    # 不达主闸且无旁路命中（但也不判死——数据不足或单维度弱）
    return {"eligible": False, "verdict": "no_qualify", "bypass": None,
            "mode_b_action": None,
            "reason": f"不达主闸（sharpe<{s_min} 或 fitness<{f_min}）且无可行走旁路"}
