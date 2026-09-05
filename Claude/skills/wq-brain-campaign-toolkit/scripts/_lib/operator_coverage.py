# -*- coding: utf-8 -*-
"""_lib/operator_coverage.py - 算子全覆盖滚动契约调度器。

2026-08-18 新增（用户需求：不止补 3 个欠用家族，要 102 真实算子全覆盖）：
  实战 EUR+GBR 836 表达式仅覆盖 22/102 算子（21.6%），rank 单点 95.9%。
  只补"当前欠用家族"是把一个盲区换成另一个局部；正确形态是【跨波滚动全覆盖】：
  以平台权威全集 VERIFIED_SAFE_OPERATORS(102) 为底账，每波强制配额给"最久未用/
  从未使用"的算子，自动跳过当前数据集不适用的算子，N 波后 102 个全覆盖。

设计（复用 explore_contract + 闸6 + L4 自学习闭环）：
  CoverageLedger      102 算子使用台账：total_uses / waves_since_use / best_sharpe
  applicable_ops      适用性过滤：无 VECTOR 字段跳过 vec_*，条件/元算子按需
  plan_coverage_wave  按遗忘度排序选本波 required_operators，调 issue_contract 签发
  update_from_results L4 回写：每个算子实测最佳 sharpe，沉淀算子级偏好

全覆盖节奏：默认每波强制 cover_per_wave 个欠用算子（遗忘度 top-N），
  单波不被覆盖拖累质量，跨波收敛到 102 全覆盖。
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_json, atomic_write
import rules as rules_mod

OP_RE = re.compile(r'\b([a-z][a-z0-9_]*)\s*\(')

# 算子适用性分类（决定在当前数据集/波是否可强制覆盖）
#   vec_*      需 VECTOR 字段（数据集无 VECTOR 字段时跳过）
#   conditional 条件/逻辑组合件（不作为主信号强制，按需自然出现）
#   meta       元/特殊算子（combo_a/self_corr 等，不进强制配额）
#   general    通用信号算子（强制全覆盖的主体）
_VEC_PREFIX = ("vec_",)
_CONDITIONAL = {"and", "or", "not", "in", "equal", "not_equal", "greater", "less",
                "greater_equal", "less_equal", "if_else", "trade_when", "is_nan"}
_META = {"combo_a", "self_corr", "generate_stats", "universe_size",
         "days_from_last_change", "last_diff_value", "kth_element"}

# 2026-09-04 新增：算子类别定义（与 wave_gate.py 闸6 对齐）
# 用于 plan_coverage_wave 的类别覆盖强制配额：确保每波 Logical/Group/Vector 至少各 1 个
OP_CATEGORIES = {
    "Logical": {"or", "and", "not", "is_nan", "less", "equal", "greater", "if_else", "not_equal", "less_equal", "greater_equal"},
    "Group": {"group_mean", "group_rank", "group_backfill", "group_scale", "group_count", "group_zscore", "group_std_dev", "group_sum", "group_neutralize", "group_cartesian_product"},
    "Vector": {"vec_min", "vec_count", "vec_sum", "vec_max", "vec_avg", "vec_stddev", "vec_range"},
    "Time Series": {"ts_corr", "ts_zscore", "ts_returns", "ts_product", "ts_std_dev", "ts_backfill", "days_from_last_change", "last_diff_value", "ts_scale", "ts_step", "ts_sum", "ts_av_diff", "ts_kurtosis", "ts_mean", "ts_arg_max", "ts_rank", "ts_ir", "ts_delay", "ts_quantile", "ts_count_nans", "ts_covariance", "ts_decay_linear", "ts_arg_min", "ts_regression", "ts_max_diff", "kth_element", "hump", "ts_delta"},
    "Cross Sectional": {"winsorize", "rank", "zscore", "scale", "normalize", "quantile"},
    "Arithmetic": {"add", "multiply", "sign", "subtract", "pasteurize", "log", "max", "abs", "divide", "min", "signed_power", "inverse", "sqrt", "reverse", "power", "densify"},
}

# 类别覆盖硬闸：每波必须覆盖的类别（Logical/Group/Vector 至少各 1 个）
_CATEGORY_GATE_REQUIRED = {"Logical", "Group", "Vector"}


def _ensure_src_path(hint_dir=None):
    """把 wqb 工作区 src/ 加入 sys.path（wqb.config / wqb.expression 所在）。

    toolkit 脚本默认只把 scripts/ 加入 sys.path，wqb 包在工作区 src/ 下。
    定位策略（按优先级）：
      1. 环境变量 WQB_WORKSPACE
      2. hint_dir（战役目录，如 tracking/EUR）上溯到含 src/wqb 的工作区根
      3. 从当前文件上溯（兜底，toolkit 与工作区同树时有效）
    """
    def _has_wqb(src):
        return os.path.isdir(os.path.join(src, "wqb"))

    cands = []
    ws = os.environ.get("WQB_WORKSPACE")
    if ws:
        cands.append(os.path.join(ws, "src"))
    # 从战役目录上溯（tracking/EUR -> 工作区根 -> src）
    if hint_dir:
        d = os.path.abspath(hint_dir)
        for _ in range(6):
            cands.append(os.path.join(d, "src"))
            nd = os.path.dirname(d)
            if nd == d:
                break
            d = nd
    # 从当前文件上溯兜底
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        d = os.path.dirname(d)
        if not d:
            break
        cands.append(os.path.join(d, "src"))
        cands.append(os.path.join(d, "wqb", "src"))
    for c in cands:
        if _has_wqb(c):
            if c not in sys.path:
                sys.path.insert(0, c)
            return c
    return None


def _verified_ops(hint_dir=None):
    """平台权威真实算子全集（102）。hint_dir=战役目录，用于定位工作区 src。"""
    _ensure_src_path(hint_dir)
    try:
        from wqb.config import VERIFIED_SAFE_OPERATORS
        ops = set(VERIFIED_SAFE_OPERATORS)
        if ops:
            return ops
    except Exception:
        pass
    # config 不可用兜底：从 diversity_enhancer 的 categories 并集取
    try:
        from wqb.expression.diversity_enhancer import OperatorQuotaManager
        OperatorQuotaManager()
        ops = set()
        for v in OperatorQuotaManager.OPERATOR_CATEGORIES.values():
            ops.update(v)
        return ops
    except Exception:
        return set()


def _extract_ops(expr):
    return set(OP_RE.findall(expr)) if isinstance(expr, str) else set()


def operator_kind(op):
    if op.startswith(_VEC_PREFIX):
        return "vec"
    if op in _CONDITIONAL:
        return "conditional"
    if op in _META:
        return "meta"
    return "general"


def applicable_ops(all_ops, has_vector=False, include_conditional=False, include_meta=False):
    """按当前数据集适用性过滤可强制覆盖的算子集。

    has_vector: 当前数据集是否含 VECTOR 字段（无则跳过 vec_*）。
    include_conditional/include_meta: 条件/元算子默认不进强制配额（它们是组合件/元操作，
      强行当主信号会产出无意义表达式），按需自然出现。
    """
    out = []
    for op in all_ops:
        k = operator_kind(op)
        if k == "vec" and not has_vector:
            continue
        if k == "conditional" and not include_conditional:
            continue
        if k == "meta" and not include_meta:
            continue
        out.append(op)
    return out


class CoverageLedger:
    """102 算子使用台账。主轨入库 ledger_kv（key=operator_coverage），文件为 DB 缺失兜底。"""

    def __init__(self, ctx):
        self.ctx = ctx
        self.path = ctx.path("reference", "operator_coverage.json")
        self.data = self._load()

    def _load(self):
        from wqb_store import get_store
        try:
            st = get_store(self.ctx)
            try:
                d = st.get_ledger(getattr(self.ctx, "region", None) or self.region_fallback(),
                                  "operator_coverage")
                if isinstance(d, dict):
                    return d
            finally:
                st.close()
        except Exception:
            pass
        if os.path.exists(self.path):
            try:
                return load_json(self.path)
            except Exception:
                pass
        return {"version": 1, "region": getattr(self.ctx, "region", None),
                "operators": {}, "waves_covered": 0}

    def region_fallback(self):
        if os.path.exists(self.path):
            try:
                return (load_json(self.path) or {}).get("region")
            except Exception:
                return None
        return None

    def save(self):
        from wqb_store import get_store
        try:
            st = get_store(self.ctx)
            try:
                st.upsert_ledger(self.region_fallback() or getattr(self.ctx, "region", None)
                                 or "?", "operator_coverage", self.data)
            finally:
                st.close()
        except Exception as e:
            print(f"[db] operator_coverage 入库异常（落文件兜底）: {e}", file=sys.stderr)
            atomic_write(self.path, self.data)

    def entry(self, op):
        return self.data["operators"].setdefault(
            op, {"total_uses": 0, "waves_since_use": 999, "best_sharpe": None,
                 "last_wave": None})

    def rebuild_from_candidates(self):
        """从 candidates/*.json 重建算子使用台账（幂等，全量重扫）。"""
        all_ops = _verified_ops(getattr(self.ctx, "dir", None))
        for op in all_ops:
            self.entry(op)  # 确保 102 全到账
        # 全量重扫 candidates，统计每个算子出现的表达式数 + 最近波次
        cdir = self.ctx.path("candidates")
        op_count = {}
        op_lastwave = {}
        wave_order = []
        if os.path.isdir(cdir):
            for fp in sorted(glob.glob(os.path.join(cdir, "*.json"))):
                fn = os.path.basename(fp)
                wave_order.append(fn)
                try:
                    d = load_json(fp)
                except Exception:
                    continue
                items = d if isinstance(d, list) else (
                    d.get("items") or d.get("candidates") or d.get("alphas") or [])
                if not isinstance(items, list):
                    continue
                for it in items:
                    if not isinstance(it, dict):
                        continue
                    code = it.get("code") or it.get("expression") or it.get("expr") or it.get("alpha")
                    for op in _extract_ops(code):
                        if op in all_ops:
                            op_count[op] = op_count.get(op, 0) + 1
                            op_lastwave[op] = fn  # sorted 序，最后一个即最近
        # 回写台账
        n_files = max(1, len(wave_order))
        for op in all_ops:
            e = self.entry(op)
            e["total_uses"] = op_count.get(op, 0)
            lw = op_lastwave.get(op)
            e["last_wave"] = lw
            if lw is None:
                e["waves_since_use"] = 999  # 从未使用
            else:
                e["waves_since_use"] = n_files - 1 - wave_order.index(lw)
        self.data["waves_covered"] = n_files
        self.save()
        return self

    def coverage_stats(self):
        """覆盖度统计：已用/总数、从未使用列表、按遗忘度排序。"""
        ops = self.data["operators"]
        used = [o for o, e in ops.items() if e["total_uses"] > 0]
        never = [o for o, e in ops.items() if e["total_uses"] == 0]
        return {"total": len(ops), "used": len(used), "never_used": sorted(never),
                "coverage_rate": round(len(used) / len(ops), 3) if ops else 0}

    # 家族优先级：破 CW 墙/信号维度关键家族优先（同等遗忘度下）
    _FAMILY_PRIORITY = {"group": 0, "ts_window": 1, "reduce": 2, "scale": 3,
                        "ts_rank": 4, "ts_fill": 4, "ts_shift": 4, "vector": 5,
                        "math": 6, "rank": 7, "cond": 8, "other": 9}

    def _family_of(self, op):
        if op.startswith("group_"):
            return "group"
        if op.startswith("reduce_"):
            return "reduce"
        if op.startswith("vec_"):
            return "vector"
        if op in ("ts_rank",):
            return "ts_rank"
        if op in ("ts_backfill",):
            return "ts_fill"
        if op in ("ts_delay", "ts_ir", "ts_returns"):
            return "ts_shift"
        if op.startswith("ts_"):
            return "ts_window"
        if op in ("rank", "quantile", "zscore"):
            return "rank"
        if op in ("normalize", "scale", "winsorize", "pasteurize"):
            return "scale"
        if op in _CONDITIONAL:
            return "cond"
        return "other"

    def most_forgotten(self, candidates_ops, n):
        """从候选算子集里按遗忘度取 top-N。

        排序键：从未使用(total_uses==0) 优先；其次 waves_since_use 越大越优先；
        同遗忘度按家族优先级（group/ts_window/reduce 等破 CW 墙关键家族优先），
        再按算子名字典序（稳定）。
        """
        def key(op):
            e = self.data["operators"].get(op, {})
            never = 1 if e.get("total_uses", 0) == 0 else 0
            fam_pri = self._FAMILY_PRIORITY.get(self._family_of(op), 9)
            return (-never, -e.get("waves_since_use", 999), fam_pri, op)
        return sorted(candidates_ops, key=key)[:n]


def _dataset_has_vector(ctx):
    """当前数据集是否含 VECTOR 字段（从 typed catalog / settings 推断）。"""
    # 优先：settings.dataset 对应 typed catalog 的 data_type
    try:
        ds = (ctx.settings or {}).get("dataset")
        if ds:
            cat_dir = ctx.path("reference")
            for fp in glob.glob(os.path.join(cat_dir, f"*_{ds}_fields.json")):
                cat = load_json(fp)
                for f in (cat.get("fields") or []):
                    if isinstance(f, dict) and str(f.get("type", "")).upper() == "VECTOR":
                        return True
    except Exception:
        pass
    return False


def plan_coverage_wave(ctx, wave_size=8, cover_ratio=0.4, cover_per_wave=None,
                       per_batch_min_operators=2, expires_after_batches=10, dry_run=False,
                       semantic=True, dataset=None, write_candidates=True,
                       auto_build_catalog=True, catalog_top_n=3):
    """规划本波算子全覆盖契约：按遗忘度选 required_operators 并签发 explore_contract。

    wave_size:       本波候选数（七槽填槽通常 8-24）。
    cover_ratio:     欠用池覆盖步进比例（默认每波推进欠用算子的 40%）。
    cover_per_wave:  显式指定本波覆盖算子数（覆盖 cover_ratio）。
    semantic:        True=语义驱动（默认）：可选池=可实例化算子（有经济含义），
                     实例化因子随契约 evidence + 落盘候选文件；False=裸算子池（旧行为）。
    dataset:         语义模式指定数据集 id（决定字段角色池）；缺省自动选锚点
                     （pick_anchor_dataset：单数据集用 settings.dataset，多数据集选
                     ranking tier1 里字段池最丰富的）。
    write_candidates: 语义模式是否把实例化因子落盘 candidates/<region>_coverage_exprs.json。
    返回契约 action（含 required_operators）+ 覆盖计划说明。

    优雅降级（region 无关）：语义模式但无 typed catalog / 字段池为空时，自动退回
    裸算子池（semantic 降级为 False），保证任何 region 至少能签裸契约。

    required_operators 是本波"应被覆盖"的欠用算子候选池；闸6 要求每批至少命中其中
    per_batch_min_operators 个。池给足选择空间，跨波滚动收敛到 102 全覆盖。
    语义模式下，池里每个算子都带一个有经济含义的实例化因子，build_wave 可直接消费。
    """
    ledger = CoverageLedger(ctx).rebuild_from_candidates()
    all_ops = _verified_ops(getattr(ctx, "dir", None))
    has_vec = _dataset_has_vector(ctx)
    factor_templates = {}
    anchor_reason = None
    degraded = False
    catalog_built = None
    if semantic:
        # 自动选锚点：dataset 缺省时从 ranking tier1 / typed catalog 选字段池最丰富的
        if dataset is None:
            dataset, anchor_reason = pick_anchor_dataset(ctx)
        # 无 catalog -> 自动懒建（用户：不降级，自动建）；失败才退降级兜底
        if dataset is None and auto_build_catalog:
            try:
                catalog_built = ensure_catalog(ctx, top_n=catalog_top_n)
                dataset, anchor_reason = pick_anchor_dataset(ctx)  # 建后重选锚点
                if dataset:
                    anchor_reason = f"懒建 catalog 后选锚点（{anchor_reason}）"
            except _CatalogBuildError as cbe:
                anchor_reason = f"懒建 catalog 失败（{cbe}），退降级"
        # 语义驱动：可选池 = 可实例化算子（三关过滤，保证有经济含义且能跑通）
        inst = instantiable_operators(ctx, dataset=dataset) if dataset else {}
        if not inst:
            # 优雅降级：无 typed catalog / 字段池空 -> 退裸算子池（懒建失败后的兜底）
            degraded = True
            semantic = False
            pool = applicable_ops(all_ops, has_vector=has_vec)
        else:
            pool = sorted(inst.keys())
            # ① 骨架入库（layer ② 的"单源真相"）：factor_templates 每条携带 {op, template, params} 骨架，
            # 消费端（build_wave）按当前波次数据集的字段角色池实例化；这是多样性闸的【主结构性保证】
            # ——确定性地把 required 算子注入候选池，不依赖 GEM 输出。GEM 侧 ③ 仅为 best-effort 次保障。
            # 同时保留锚点数据集实例化的具体表达式作 legacy 回退/审计。
            # 修复双重失效：(a) 锚点字段跨数据集撞 FIELD 闸；(b) 固定表达式被历史去重杀死。
            _sem = load_semantics()
            factor_templates = {}
            for op in pool:
                _s = _sem.get(op) or {}
                factor_templates[op] = {
                    "op": op,
                    "skeleton": True,
                    "template": _s.get("template", ""),
                    "meaning": _s.get("meaning"),
                    "category": _s.get("category"),
                    "params": {"windows": [20, 10, 60, 120, 5, 66]},
                    # legacy：锚点实例化具体表达式（无角色池时 build_wave 回退用）
                    "expr": inst[op]["expr"],
                    "fields": inst[op]["fields"],
                }
    else:
        # 裸算子池（旧行为）：仅适用性过滤
        pool = applicable_ops(all_ops, has_vector=has_vec)
    # 欠用算子池（从未使用 + 久未使用）：全覆盖的推进对象
    never_used = [op for op in pool if ledger.data["operators"].get(op, {}).get("total_uses", 0) == 0]
    # 本波覆盖数：显式 > 欠用池比例 > 保底 per_batch_min_operators；不超欠用池大小
    if cover_per_wave is None:
        n_cover = max(per_batch_min_operators, int(round(len(never_used) * cover_ratio)))
        n_cover = max(n_cover, min(12, len(never_used)))  # 默认每波至少推进 12 个（若欠用足够）
    else:
        n_cover = cover_per_wave
    n_cover = min(n_cover, len(pool))
    required = ledger.most_forgotten(pool, n_cover)
    
    # 2026-09-04 新增：算子类别覆盖强制配额（Logical/Group/Vector 至少各 1 个）
    # 与 wave_gate.py 闸6 对齐：确保每波候选池覆盖关键类别，避免 GEM 输出单一类别
    required_set = set(required)
    category_covered = set()
    for op in required:
        for cat, ops in OP_CATEGORIES.items():
            if op in ops:
                category_covered.add(cat)
                break
    
    # 检查缺失类别，从 pool 中补入该类别最久未用的算子
    missing_cats = _CATEGORY_GATE_REQUIRED - category_covered
    if missing_cats:
        # 按类别分组 pool 中未入选的算子
        pool_by_cat = {}
        for op in pool:
            if op in required_set:
                continue
            for cat, ops in OP_CATEGORIES.items():
                if op in ops:
                    pool_by_cat.setdefault(cat, []).append(op)
                    break
        
        # 对每个缺失类别，补入最久未用的算子
        for cat in sorted(missing_cats):
            candidates = pool_by_cat.get(cat, [])
            if not candidates:
                continue
            # 从该类别候选中取最久未用的 1 个
            best = ledger.most_forgotten(candidates, 1)
            if best:
                required.append(best[0])
                required_set.add(best[0])
                print(f"[category-coverage] 补入 {cat} 类别算子: {best[0]}")
    
    stats = ledger.coverage_stats()
    
    # 更新 plan 的类别覆盖信息
    plan_categories = {}
    for op in required:
        for cat, ops in OP_CATEGORIES.items():
            if op in ops:
                plan_categories.setdefault(cat, []).append(op)
                break

    plan = {
        "region": getattr(ctx, "region", None),
        "wave_size": wave_size,
        "cover_ratio": cover_ratio,
        "n_cover": n_cover,
        "required_operators": required,
        "has_vector": has_vec,
        "semantic": semantic,
        "anchor_dataset": dataset,
        "anchor_reason": anchor_reason,
        "degraded": degraded,
        "pool_size": len(pool),
        "skipped_not_applicable": sorted(set(all_ops) - set(pool)),
        "coverage_before": stats,
        "category_coverage": plan_categories,  # 2026-09-04 新增：类别覆盖明细
    }

    if dry_run:
        plan["issued"] = False
        plan["dry_run"] = True
        if semantic:
            plan["factor_templates"] = {op: factor_templates[op] for op in required}
        return plan

    # 签发 explore_contract（闸6 消费：每批至少 per_batch_min_operators 个 required 算子）
    # factor_templates 写入 action（get_active_contract 返回携带，build_wave 直接消费）；
    # evidence 只留审计信息（source/coverage_before 等）。
    rid = rules_mod.issue_contract(
        ctx,
        required_operators=required,
        skeleton_quota={},
        region=getattr(ctx, "region", None),
        per_batch_min_operators=per_batch_min_operators,
        expires_after_batches=expires_after_batches,
        exempt=("repair",),
        evidence={"source": "operator_coverage",
                  "semantic": semantic,
                  "anchor_dataset": dataset,
                  "anchor_reason": anchor_reason,
                  "degraded": degraded,
                  "coverage_before": stats,
                  "n_cover": n_cover,
                  "has_vector": has_vec},
        factor_templates={op: factor_templates[op] for op in required
                          if op in factor_templates},
    )
    plan["issued"] = True
    plan["contract_rule_id"] = rid

    # 语义模式：实例化因子落盘候选文件，作为 build_wave --file 输入源
    if semantic and write_candidates and required:
        exprs = []
        for op in required:
            ft = factor_templates.get(op)
            if ft and ft.get("expr"):
                exprs.append(ft["expr"])
        if exprs:
            out = ctx.path("candidates", f"{ctx.prefix}_coverage_exprs.json")
            payload = {"meta": {"source": "operator_coverage.semantic",
                                "contract_rule_id": rid,
                                "required_operators": required,
                                "region": getattr(ctx, "region", None)},
                       "expressions": exprs}
            # 主轨入库：语义覆盖候选入 expressions（status=coverage）；文件为导出/兜底
            try:
                from wqb_store import get_store
                st = get_store(ctx)
                try:
                    st.upsert_expressions(getattr(ctx, "region", None) or "?", "coverage",
                                          [{"expression": e, "status": "coverage"} for e in exprs],
                                          status="coverage")
                finally:
                    st.close()
            except Exception as e:
                print(f"[db] coverage 表达式入库异常: {e}", file=sys.stderr)
            atomic_write(out, payload)
            plan["candidates_file"] = out
            plan["candidates_count"] = len(exprs)
    return plan


def update_from_results(ctx, op_sharpe_map):
    """L4 回写：每个算子本波实测最佳 sharpe，沉淀算子级偏好。

    op_sharpe_map: {operator: best_sharpe_this_wave}。best_sharpe 取历史更优。
    """
    ledger = CoverageLedger(ctx)
    for op, sh in (op_sharpe_map or {}).items():
        if not isinstance(sh, (int, float)):
            continue
        e = ledger.entry(op)
        if e["best_sharpe"] is None or sh > e["best_sharpe"]:
            e["best_sharpe"] = round(float(sh), 4)
    ledger.save()
    return ledger.coverage_stats()


# ================= 语义模板驱动：有经济含义的算子全覆盖 =================
# 2026-08-18（用户：覆盖的算子组成的因子要有经济学含义，否则回测报错/没意义）。
# 核心：覆盖的载体是"算子×经济语义模板"，不是裸算子。每个模板绑定经济角色输入，
# 实例化时从当前数据集字段池匹配角色字段填充，保证产出的因子有站得住的经济逻辑。

_SEMANTICS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config", "operator_semantics.json")

# 角色 -> 关键词（字段 id/description 小写匹配，用于字段角色识别）
ROLE_KW = {
    "price": ["close", "open", "high", "low", "vwap", "price", "adj_close"],
    "volume": ["volume", "turnover", "amount", "shares_traded", "dollar_volume", "adv"],
    "returns": ["return", "ret_", "_ret", "daily_ret", "pct_change", "logret"],
    "volatility": ["volatility", "_vol", "realized_vol", "std_dev", "stdev", "variance"],
    "valuation": ["pe", "pb", "ps", "ev_", "enterprise_value", "book_to",
                  "earnings_yield", "dividend_yield", "valuation"],
    "fundamental": ["earnings", "sales", "revenue", "bookvalue", "cashflow", "fcf",
                    "ebitda", "margin", "asset", "liabilit", "equity", "income",
                    "profit", "debt", "fundamental"],
    "sentiment": ["sentiment", "news_score", "social", "buzz", "emotion", "nlp"],
    "analyst": ["analyst", "estimate", "revision", "target_price", "consensus",
                "recommendation", "starmine", "eps_est"],
    "model_score": ["model", "score", "alpha", "prediction", "signal", "factor",
                    "rank", "percentile", "likelihood", "probability"],
    # group 分组键（2026-08-19 补 cluster/kmeans/label/bucket 等离散分组标签关键词——
    # GBR other455 实证：kmeans_cluster 字段不含常规 group 关键词被兜底进 signal_any，
    # 导致 group_sum/ts_corr 等把分组键误当数值信号 x，报 unit ERROR "expected Unit[], found Unit[Group:1]"）
    "group": ["sector", "industry", "country", "region", "market_cap", "size_bucket", "group",
              "cluster", "kmeans", "_label", "_bucket", "category_id", "_cat", "quantile_group"],
}

# 角色回退链：模板需要的角色不可得时，可回退到更通用的角色
# （如 price 不可得 -> 用任意数值信号做时序统计，经济含义弱化为"信号动量"）
_ROLE_FALLBACK = {
    "price": ["signal_any"],
    "volume": ["signal_any"],
    "returns": ["price", "signal_any"],   # returns 可由 price 派生（外层包 ts_returns/ts_delta）
    "volatility": ["returns", "signal_any"],
    "valuation": ["fundamental", "signal_any"],
    "fundamental": ["signal_any"],
    "sentiment": ["model_score", "signal_any"],
    "analyst": ["model_score", "signal_any"],
    "model_score": ["signal_any"],
}

# 默认时间窗口候选（实例化 window 占位符）
_DEFAULT_WINDOWS = [20, 60, 120, 5, 10, 252]


def load_semantics():
    """加载算子语义模板库（102 算子 × 经济角色/含义/模板）。"""
    if os.path.exists(_SEMANTICS_PATH):
        try:
            return load_json(_SEMANTICS_PATH).get("operators", {})
        except Exception:
            pass
    return {}


def field_roles(fid, desc=""):
    """给单个字段打经济角色标签（可多个）。返回角色列表，兜底 signal_any。"""
    txt = (str(fid) + " " + str(desc or "")).lower()
    hits = [role for role, kws in ROLE_KW.items() if any(k in txt for k in kws)]
    return hits or ["signal_any"]


def dataset_role_pool(ctx, dataset=None):
    """指定数据集的"角色 -> 字段列表"映射（从 typed catalog 构建）。

    dataset: 显式指定数据集 id；缺省取 settings.dataset（单数据集战役）。
    返回 (role_pool, has_vector, all_fields)：
      role_pool: {role: [field_id, ...]}（按 coverage 降序）
      has_vector: 是否含 VECTOR 字段
      all_fields: 全部可用字段 id 列表
    """
    ds = dataset or (ctx.settings or {}).get("dataset")
    role_pool = {}
    has_vector = False
    all_fields = []
    if not ds:
        return role_pool, has_vector, all_fields
    cat_dir = ctx.path("reference")
    cat = None
    for fp in glob.glob(os.path.join(cat_dir, "*_fields.json")):
        try:
            d = load_json(fp)
        except Exception:
            continue
        if d.get("dataset") == ds or os.path.basename(fp).endswith(f"_{ds}_fields.json"):
            cat = d
            break
    if not cat:
        # 2026-08-25 DB catalog 回退：scan-fields 的产物落 CampaignStore（data/wqb.db），
        # 不一定有 reference 文件；无文件时读 DB typed catalog（同构 {dataset, fields}）。
        try:
            from _lib.wqb_store import load_catalog
            cat = load_catalog(ctx, ds) or None
        except Exception:
            cat = None
    if not cat:
        return role_pool, has_vector, all_fields
    flds = []
    for f in (cat.get("fields") or []):
        if not isinstance(f, dict):
            continue
        fid = f.get("id")
        if not fid:
            continue
        if str(f.get("type", "")).upper() == "VECTOR":
            has_vector = True
        cov = f.get("coverage", 0) or 0
        flds.append((fid, cov, f.get("description", "")))
        all_fields.append(fid)
    # 按 coverage 降序填充角色池
    flds.sort(key=lambda x: -x[1])
    for fid, cov, desc in flds:
        for role in field_roles(fid, desc):
            role_pool.setdefault(role, []).append(fid)
    return role_pool, has_vector, all_fields


def _pick_from_pool(pool, exclude):
    """从字段池取第一个未被 exclude 占用的字段；全被占用返回 None。"""
    for fid in (pool or []):
        if fid not in exclude:
            return fid
    return None


def _resolve_role(role, role_pool, exclude=None):
    """为模板角色选字段：先看直接角色，再按回退链，全程避开 exclude 已占用字段。

    exclude: 本模板已分配字段集合（跨占位符去重，避免 ts_corr(X,X) / add(X,X) 退化）。
    返回字段 id 或 None（该角色在避开 exclude 后无可用字段）。
    """
    exclude = exclude or set()
    if role in ("window", "scalar"):
        return None  # 由实例化处填常数
    if role == "group":
        # group 键：优先真实分组字段，否则退回平台内置分组（sector/industry）
        fid = _pick_from_pool(role_pool.get("group"), exclude)
        return fid or "sector"
    # 直接角色
    fid = _pick_from_pool(role_pool.get(role), exclude)
    if fid:
        return fid
    # 回退链
    for fb in _ROLE_FALLBACK.get(role, []):
        fid = _pick_from_pool(role_pool.get(fb), exclude)
        if fid:
            return fid
    # 最终兜底：任意信号字段（避开 exclude）
    any_pool = role_pool.get("signal_any") or sum(role_pool.values(), [])
    return _pick_from_pool(any_pool, exclude)


def instantiate_factor(op, role_pool, window=None, semantics=None):
    """按语义模板 + 当前角色字段池，实例化一个有经济含义的合法因子表达式。

    字段绑定策略（2026-08-18 修订，修复同字段退化 bug）：
      按模板占位符【出现顺序】逐个分配字段，维护 assigned 集合跨占位符去重：
      - 不同角色（ts_corr 的 price/volume）各自解析但避开已占用字段，避免同字段退化；
      - 同角色多占位符（add 的两个 signal_any）取该角色池的下一个可用字段；
      - 字段池耗尽无法去重时，允许重复并标记 degenerate（经济含义弱化，由调用方权衡）。

    返回 (expression, used_fields, meaning) 或 (None, reason, None)（不可实例化）。
    """
    sem = (semantics or load_semantics()).get(op)
    if not sem:
        return None, "no_semantics", None
    tpl = sem.get("template", "")
    # assigned 跟踪已分配字段：re.sub 按占位符出现顺序逐个调 _fill，天然保证
    # price/volume 先后与跨占位符去重（不同角色避开已占用，同角色取下一个）。
    assigned = set()
    degenerate = False
    consts = {"window": str(window or _DEFAULT_WINDOWS[0]), "scalar": "0.5"}

    def _fill(m):
        nonlocal degenerate
        role = m.group(1)
        if role in consts:
            return consts[role]
        fid = _resolve_role(role, role_pool, exclude=assigned)
        if fid is None:
            # 字段池耗尽：放宽去重约束，取该角色首选字段（允许重复，标记退化）
            fid = _resolve_role(role, role_pool, exclude=set())
            if fid is None:
                raise _RoleUnresolved(role)
            degenerate = True
        assigned.add(fid)
        return fid

    try:
        expr = re.sub(r'\{([a-z_]+)\}', _fill, tpl)
    except _RoleUnresolved as e:
        return None, f"role_unresolved:{e.args[0]}", None
    # degenerate=True 时表达式仍合法（同字段），仅经济含义弱化，交由闸5/回测裁决
    return expr, list(assigned), sem.get("meaning")


class _RoleUnresolved(Exception):
    """模板角色在字段池中完全无法解析（连放宽去重后也无字段）。"""


def instantiable_operators(ctx, dataset=None, semantics=None):
    """三关过滤，返回指定数据集可"有意义覆盖"的算子集。

    关 1 适用性：无 VECTOR 字段跳过 vec_*；条件/元算子默认不进强制池。
    关 2 语义可实例化：模板所需经济角色在字段池可得（含回退链）。
    关 3 闸5 兼容：实例化表达式过语法/字段白名单（复用 expr 工具，轻量校验）。
    返回 {op: {"expr":..., "fields":..., "meaning":...}}（可实例化算子 -> 因子）。
    无 typed catalog / 字段池为空时返回 {}（调用方负责优雅降级）。
    """
    semantics = semantics or load_semantics()
    role_pool, has_vector, all_fields = dataset_role_pool(ctx, dataset)
    if not all_fields:
        return {}  # 无 typed catalog / 无可用字段：语义模式不可用，优雅降级
    all_ops = _verified_ops(getattr(ctx, "dir", None))
    # 关 1：适用性
    pool = applicable_ops(all_ops, has_vector=has_vector)
    out = {}
    for op in pool:
        sem = semantics.get(op)
        if not sem:
            continue
        # vec_* 需 VECTOR 字段（关 1 已过滤，双保险）
        if sem.get("needs_vector") and not has_vector:
            continue
        # 关 2 + 关 3：实例化（角色可得即过语义关；实例化成功即过轻量语法关）
        expr, fields, meaning = instantiate_factor(op, role_pool, semantics=semantics)
        if expr is None:
            continue
        out[op] = {"expr": expr, "fields": fields, "meaning": meaning,
                   "category": sem.get("category")}
    return out


# ================= 通用化：自动选锚点 + 优雅降级（region 无关） =================
# 2026-08-18（用户：能力要通用，不限单个 region）。
# 多数据集战役（settings.dataset=None）需自动选"字段池最丰富"的数据集作实例化锚点；
# 无 typed catalog 的 region 优雅降级裸算子池，保证任何 region 至少能签裸契约。

def list_typed_datasets(ctx):
    """列出当前 region 所有有 typed catalog 的数据集 id（region 自适应前缀）。"""
    pref = (getattr(ctx, "prefix", None) or str(getattr(ctx, "region", "")).lower()) + "_"
    out = []
    for fp in glob.glob(ctx.path("reference", "*_fields.json")):
        b = os.path.basename(fp)
        if b.startswith(pref) and b.endswith("_fields.json"):
            out.append(b[len(pref):-len("_fields.json")])
    return sorted(out)


def _tier1_datasets(ctx):
    """从 ranking 取 tier1 数据集 id 列表（白名单）。无 ranking 返回 None。"""
    rp = ctx.ranking_path()
    if not os.path.exists(rp):
        return None
    try:
        d = load_json(rp)
    except Exception:
        return None
    items = d if isinstance(d, list) else (d.get("ranking") or d.get("datasets") or d.get("rows") or [])
    tier1 = [r.get("dataset", r.get("id")) for r in items
             if isinstance(r, dict) and str(r.get("tier", "")).lower() == "tier1"]
    return [x for x in tier1 if x]


def _ranking_row(ctx, dataset):
    """从 ranking 取某数据集的行（含 valueScore/tier/alphaCount 等）。无 ranking 或无此行返回 {}。"""
    rp = ctx.ranking_path()
    if not os.path.exists(rp):
        return {}
    try:
        d = load_json(rp)
    except Exception:
        return {}
    items = d if isinstance(d, list) else (d.get("ranking") or d.get("datasets") or d.get("rows") or [])
    for r in items:
        if isinstance(r, dict) and (r.get("dataset", r.get("id")) == dataset):
            return r
    return {}


def _dataset_field_kind(ctx, dataset):
    """判断数据集主导字段类型：'MATRIX' / 'VECTOR' / 'MIXED' / 'UNKNOWN'。

    读 typed catalog 字段 type 统计：vec>mat -> VECTOR；mat>vec -> MATRIX；
    相等（含全 0）-> MIXED；无 catalog -> UNKNOWN。
    锚点选择优先 MATRIX（VECTOR 字段需 vec_* 包裹，契约因子直接引用会触闸3）。
    """
    cat_dir = ctx.path("reference")
    pref = (getattr(ctx, "prefix", None) or str(getattr(ctx, "region", "")).lower()) + "_"
    cat = None
    for fp in glob.glob(os.path.join(cat_dir, "*_fields.json")):
        b = os.path.basename(fp)
        if not (b.startswith(pref) and b.endswith("_fields.json")):
            continue
        if b[len(pref):-len("_fields.json")] != dataset:
            continue
        try:
            cat = load_json(fp)
        except Exception:
            cat = None
        break
    if not cat:
        return "UNKNOWN"
    n_vec = n_mat = 0
    for f in (cat.get("fields") or []):
        if not isinstance(f, dict):
            continue
        t = str(f.get("type", "")).upper()
        if t == "VECTOR":
            n_vec += 1
        elif t == "MATRIX":
            n_mat += 1
    if n_vec == 0 and n_mat == 0:
        return "UNKNOWN"
    if n_vec > n_mat:
        return "VECTOR"
    if n_mat > n_vec:
        return "MATRIX"
    return "MIXED"


def pick_anchor_dataset(ctx, prefer_tier1=True, prefer_matrix=True):
    """自动选实例化锚点数据集（region 无关）。

    策略（2026-08-19 修订，GBR wave29 实证：原逻辑只按字段池丰富度选，误选 VECTOR 弱信号集 news104）：
      1. 单数据集战役（settings.dataset 有值）-> 直接用它；
      2. 候选池 = ranking tier1 ∩ typed catalog（无 ranking 用全部 typed）；
      3. prefer_matrix=True 时优先 MATRIX 数据集（VECTOR 字段需 vec_* 包裹，契约因子直接引用触闸3）；
         候选池无 MATRIX 才退到 MIXED/VECTOR；
      4. 同类型内按 valueScore desc（信号强度，ranking 提供）-> 可实例化算子数 desc（字段丰富度兜底）排序；
      5. 无任何 typed catalog -> None（调用方优雅降级/懒建）。
    返回 (dataset_id, reason)。
    """
    ds = (ctx.settings or {}).get("dataset")
    if ds:
        return ds, "settings.dataset（单数据集战役）"
    cands = list_typed_datasets(ctx)
    if not cands:
        return None, "no_typed_catalog"
    tier1 = _tier1_datasets(ctx) if prefer_tier1 else None
    # 候选池：tier1 ∩ typed 优先，无 tier1 用全部 typed
    pool = [d for d in (tier1 or []) if d in cands] or cands

    # 按字段类型分组：MATRIX 优先，MIXED 次之，VECTOR/UNKNOWN 兜底
    def _kind_rank(d):
        k = _dataset_field_kind(ctx, d)
        return {"MATRIX": 0, "MIXED": 1, "VECTOR": 2, "UNKNOWN": 3}.get(k, 3)

    def _value_score(d):
        r = _ranking_row(ctx, d)
        try:
            return float(r.get("valueScore") or 0)
        except Exception:
            return 0.0

    # 排序键：(类型优先级, -valueScore, -可实例化算子数)；prefer_matrix=False 时类型全同级
    scored = []
    for d in pool:
        kr = _kind_rank(d) if prefer_matrix else 0
        vs = _value_score(d)
        n = len(instantiable_operators(ctx, dataset=d))
        scored.append((kr, -vs, -n, d, n))
    scored.sort(key=lambda x: (x[0], x[1], x[2]))
    kr, neg_vs, neg_n, best, best_n = scored[0]
    best_vs = -neg_vs
    kind = _dataset_field_kind(ctx, best)
    src = "ranking tier1" if (tier1 and best in (tier1 or [])) else "typed catalog"
    return best, (f"{src} 优先 MATRIX 强信号（{kind}，valueScore={best_vs}，"
                  f"可实例化 {best_n} 算子）")


# ================= 通用化：无 catalog 自动懒建（不降级） =================
# 2026-08-18（用户：无 catalog 最好自动建，不要降级）。
# 懒建策略（plan_coverage_wave 发现无 typed catalog 时触发）：
#   1. 探可用数据集（score_datasets.fetch_all_datasets，GET /data-sets）
#   2. score() 打分排序取 top N（简化 tier1，复用现有评分逻辑）
#   3. 逐个 scan_fields 建 typed catalog（GET /data-fields）
# 网络/认证失败 -> 抛 _CatalogBuildError，由 plan_coverage_wave 捕获退降级裸模式兜底。

class _CatalogBuildError(Exception):
    """懒建 catalog 失败（网络/认证/平台错误），调用方退降级裸模式。"""


def _scripts_dir():
    """toolkit scripts/ 目录（scan_fields/score_datasets 所在），确保可 import。"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ensure_catalog(ctx, top_n=3, min_score=0.0, force=False):
    """无 typed catalog 时自动懒建（region 无关）。

    top_n:     建 catalog 的数据集数（按 score 降序取 top N，默认 3）。
    min_score: score 低于此值的数据集不建（默认 0 全建 top N）。
    force:     即使已有 typed catalog 也重建 top N（默认 False，有才跳过）。
    返回 {"built": [dataset_id...], "skipped": [...], "reason": ...}。
    失败抛 _CatalogBuildError（plan_coverage_wave 捕获退降级）。
    """
    existing = list_typed_datasets(ctx)
    if existing and not force:
        return {"built": [], "skipped": existing, "reason": "已有 typed catalog，跳过懒建"}
    # 确保 scripts/ 在 sys.path（scan_fields/score_datasets 在顶层）
    sdir = _scripts_dir()
    if sdir not in sys.path:
        sys.path.insert(0, sdir)
    try:
        from _lib.common import load_credentials
        from _lib.api import Api
        import scan_fields as sf
        import score_datasets as sd
    except Exception as e:
        raise _CatalogBuildError(f"依赖导入失败：{e}")
    # 登录 + 探可用数据集
    try:
        e, pw = load_credentials()
        api = Api()
        api.login(e, pw)
    except Exception as ex:
        raise _CatalogBuildError(f"API 登录失败：{ex}")
    try:
        all_ds = sd.fetch_all_datasets(api, ctx.settings)
    except Exception as ex:
        raise _CatalogBuildError(f"探测数据集失败：{ex}")
    if not all_ds:
        raise _CatalogBuildError("平台返回 0 个可用数据集")
    # score() 打分排序取 top N（简化 tier1）
    h = (ctx.thresholds or {}).get("dataset_health", {})
    scored = []
    for ds in all_ds:
        did = ds.get("id")
        if not did:
            continue
        fc = ds.get("fieldCount") or 0
        try:
            sc = sd.score(ds, fc, h)
        except Exception:
            sc = 0
        scored.append((did, sc))
    scored.sort(key=lambda x: -x[1])
    picked = [(did, sc) for did, sc in scored if sc >= min_score][:top_n]
    if not picked:
        raise _CatalogBuildError(f"无 score>={min_score} 的数据集可建 catalog")
    # 逐个 scan_fields 建 catalog
    built, skipped = [], []
    for did, sc in picked:
        try:
            raw = sf.fetch_fields(api, ctx.settings, did)
            cat = sf.build_catalog(ctx.settings, did, raw)
            try:
                from wqb_store import save_catalog
                save_catalog(ctx, cat)
            except Exception:
                atomic_write(ctx.catalog_path(did), cat)
            built.append(did)
        except Exception as ex:
            skipped.append(f"{did}(err:{ex})")
    if not built:
        raise _CatalogBuildError(f"scan_fields 全失败：{skipped}")
    return {"built": built, "skipped": skipped, "reason": f"懒建 top{top_n} catalog"}
