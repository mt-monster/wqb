# -*- coding: utf-8 -*-
"""brain-data-feature-engineering 的 headless CLI（S1-S3 特征工程流水线）。

被 wqb.workflow 的 feature_engineering 节点以子进程方式调用（wq_py() 解释器），
契约（见 src/wqb/workflow/nodes/feature_engineering.py::_run_feature_engineering_pipeline）：

    feature_engineering.py --region <R> --dataset <ID> --delay <0|1> \
        --universe <U> --category <C> --output <ideas_md_path>

产出：结构化 feature-engineering ideas markdown（字段画像 + 预处理决策 + 8 问特征概念
+ 字段白名单），供 S2 brain-make-some-gem 消费。

数据源：brain_api.brain_client.get_datafields（真实平台数据）。无凭据/无网络/无字段时
打印清晰错误到 stderr 并退出非零，节点据此上报失败（而非空文件误判成功）。

退出码：0 = 成功写入 ideas 文件；1 = 参数错误；2 = 平台数据获取失败。
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# brain_api 导入：优先直接 import（若已安装为包），否则从 MCP venv 解释器路径推导
# world-quant-brain-mcp 目录并加入 sys.path（feature_engineering 节点用 wq_py()
# 调用本脚本，sys.executable = <repo>/world-quant-brain-mcp/.venv/Scripts/python.exe）。
# ---------------------------------------------------------------------------

def _load_brain_client():
    try:
        from brain_api import brain_client  # noqa
        return brain_client
    except ImportError:
        pass

    # sys.executable -> .../world-quant-brain-mcp/.venv/Scripts/python.exe
    exe = sys.executable
    mcp_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(exe))))
    candidate = os.path.join(mcp_dir, "brain_api.py")
    if os.path.exists(candidate):
        if mcp_dir not in sys.path:
            sys.path.insert(0, mcp_dir)
        try:
            from brain_api import brain_client  # noqa
            return brain_client
        except ImportError as e:
            raise RuntimeError(f"brain_api import failed from {mcp_dir}: {e}")

    raise RuntimeError(
        "Cannot locate world-quant-brain-mcp/brain_api.py. "
        "Set WQ_PY to the MCP venv python, or install brain_api on sys.path."
    )


# ---------------------------------------------------------------------------
# 字段数据访问
# ---------------------------------------------------------------------------

async def _fetch_fields(brain, region: str, dataset_id: str, delay: int,
                        universe: str) -> List[Dict[str, Any]]:
    raw = await brain.get_datafields(
        instrument_type="EQUITY",
        region=region,
        delay=delay,
        universe=universe,
        theme="false",
        dataset_id=dataset_id,
        data_type="",
        search=None,
        filter_sharpe=False,  # 特征工程阶段不因 sharpe<0 过滤，保留全字段画像
    )
    if not isinstance(raw, dict):
        raise RuntimeError(f"get_datafields returned non-dict: {type(raw)}")
    results = raw.get("results") or raw.get("records") or []
    if isinstance(results, dict):  # 容错：某些版本嵌套 {results: {...}}
        results = results.get("results", [])
    return [f for f in results if isinstance(f, dict)]


def _fstr(field: Dict[str, Any], key: str, default: str = "") -> str:
    v = field.get(key)
    if v is None:
        return default
    if isinstance(v, str):
        return v
    return default


def _ftype(field: Dict[str, Any]) -> str:
    t = str(field.get("type") or field.get("dataType") or "MATRIX").upper()
    return t


def _coverage(field: Dict[str, Any]) -> Optional[float]:
    c = field.get("coverage")
    try:
        return float(c) if c is not None else None
    except (TypeError, ValueError):
        return None


def _field_id(field: Dict[str, Any]) -> str:
    return _fstr(field, "id") or _fstr(field, "name") or "unnamed_field"


def _classify_field_type(fid: str, ftype: str, desc: str) -> tuple:
    """2026-09-04 新增：字段类型分类 + 算子适配建议。
    
    返回 (field_type, operator_adaptation)。
    """
    fid_lower = fid.lower()
    desc_lower = desc.lower()
    
    # VECTOR 型（最高优先级）
    if ftype == "VECTOR":
        return ("VECTOR", "vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank")
    
    # 分类型（quantile_label/rank/class）
    if any(k in fid_lower for k in ["quantile_label", "rank", "class", "label", "bucket"]):
        return ("分类型", "rank/group_rank/ts_backfill；禁 ts_mean/ts_zscore")
    
    # 概率型（prob/class/probability）
    if any(k in fid_lower for k in ["prob", "probability", "likelihood"]):
        return ("概率型", "rank/subtract/if_else；禁 ts_mean/ts_delta")
    
    # 计数型（count/usd/num）
    if any(k in fid_lower for k in ["count", "num", "usd", "volume", "trx"]):
        return ("计数型", "ts_sum/trade_when/ts_backfill；禁 ts_delta/ts_max_diff")
    
    # 比率型（to_price/ratio/percentile）
    if any(k in fid_lower for k in ["to_price", "ratio", "percentile", "rate", "yield"]):
        return ("比率型", "rank/group_zscore/group_neutralize；禁 ts_mean/ts_delta")
    
    # 情绪型（sentiment/score）
    if any(k in fid_lower for k in ["sentiment", "score", "emotion"]):
        return ("连续数值型", "ts_mean/ts_delta/rank/ts_zscore/ts_corr；禁 ts_std_dev/ts_max_diff")
    
    # 默认连续数值型
    return ("连续数值型", "ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression；禁 ts_std_dev/ts_max_diff")


# ---------------------------------------------------------------------------
# 报告生成
# ---------------------------------------------------------------------------

def _int_metric(field: Dict[str, Any], key: str) -> int:
    """读取字段的整数型平台指标（alphaCount/userCount），缺失或非数值返回 0。"""
    v = field.get(key)
    try:
        return int(v) if v is not None else 0
    except (TypeError, ValueError):
        return 0


def _quality_score(field: Dict[str, Any]) -> float:
    """2026-09-09 D9 修复：字段质量先验评分。

    修复前 _pick 只按 coverage 排序，导致 8 个 Concept 全部围绕 coverage=1.0 的
    trivial 字段（如 iso_week_number 日历字段，零 alpha）。

    评分信号（按 brain-alpha-research-field-quality 的字段质量先验思想）：
    - alphaCount：平台已挖 alpha 数，是「该字段被验证有 alpha」的最强证据。
      取 log1p 压缩动态范围（alphaCount 可从 0 到数千）。
    - userCount：使用该字段的用户数，辅助信号（防止单用户自嗨）。
    - coverage：数据完整性门槛，仅作 tie-breaker，不作主排序键。

    alphaCount=0 不等于没 alpha（可能是处女地），但 alphaCount>0 是正面证据；
    在没有任何其他信息时，优先选已被验证的字段比赌处女地期望收益更高
    （EUR wave155 实证：6 个 alphaCount=0 字段 Sharpe 全部 ≤0.20）。
    """
    import math
    ac = _int_metric(field, "alphaCount")
    uc = _int_metric(field, "userCount")
    cov = _coverage(field) or 0.0
    # 主信号：log1p(alphaCount)；辅助：log1p(userCount) 权重减半；coverage 仅微调
    return math.log1p(ac) + 0.5 * math.log1p(uc) + 0.1 * cov


def _pick(fields: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    """按字段质量先验（alphaCount 主、userCount 辅、coverage 微调）取前 n 个。"""
    return sorted(fields, key=_quality_score, reverse=True)[:n]


def _pick_diverse(fields: List[Dict[str, Any]], n: int) -> List[Dict[str, Any]]:
    """2026-09-09 D9 修复：按质量先验选字段，但保证字段族多样性。

    修复前 8 个 Concept 全部用 top[0]/top[1] 两个字段（同族），造成伪多样性。
    本函数按「字段名第一个下划线前缀」分族，每族先取质量最高者，再按质量
    跨族轮转，直到凑满 n 个。这样 8 个 Concept 能覆盖尽可能多的不同字段族。
    """
    ranked = sorted(fields, key=_quality_score, reverse=True)
    seen_prefix: set = set()
    picked: List[Dict[str, Any]] = []
    # 第一遍：每族取质量最高者
    for f in ranked:
        fid = _field_id(f)
        prefix = fid.split("_", 1)[0] if "_" in fid else fid
        if prefix in seen_prefix:
            continue
        seen_prefix.add(prefix)
        picked.append(f)
        if len(picked) >= n:
            return picked
    # 第二遍：族不够时按质量补齐
    for f in ranked:
        if f in picked:
            continue
        picked.append(f)
        if len(picked) >= n:
            return picked
    return picked


def _fields_used(sel: List[Dict[str, Any]]) -> str:
    return ", ".join(f"`{_field_id(f)}`" for f in sel) or "（无字段）"


def _render_report(region: str, dataset_id: str, delay: int, universe: str,
                   category: str, fields: List[Dict[str, Any]]) -> str:
    now = datetime.now().isoformat()
    n = len(fields)
    matrix = [f for f in fields if _ftype(f) in ("MATRIX", "")]
    vector = [f for f in fields if _ftype(f) == "VECTOR"]
    group = [f for f in fields if _ftype(f) == "GROUP"]
    top = _pick(fields, min(8, n))

    # 预处理决策（供节点 regex 抽取：ts_backfill / group_zscore / group_rank / vec_）
    sparse = [f for f in fields if _coverage(f) is not None and _coverage(f) < 0.5]
    preprocess = []
    if sparse:
        preprocess.append("ts_backfill：对低覆盖率稀疏字段（{} 个）做时间序列回填".format(len(sparse)))
    if vector or group:
        preprocess.append("group_zscore / group_rank：对 VECTOR/GROUP 字段先截面聚合再中性化")
        preprocess.append("vec_ 向量包装：{} 个 VECTOR 字段需用 vec_* 算子读取".format(len(vector)))
    else:
        preprocess.append("group_zscore / group_rank：MATRIX 字段截面中性化（cross-sectional）")
    if not preprocess:
        preprocess.append("group_zscore / group_rank：截面中性化默认决策")

    lines: List[str] = []
    a = lines.append
    a(f"# {dataset_id} Feature Engineering Analysis Report")
    a("")
    a(f"- **Dataset**: `{dataset_id}`")
    a(f"- **Category**: `{category}`")
    a(f"- **Region**: `{region}`")
    a(f"- **Delay**: `{delay}`")
    a(f"- **Universe**: `{universe}`")
    a(f"- **Fields Analyzed**: {n}")
    a(f"- **Generated**: {now}")
    a("")
    a("---")
    a("")
    a("## Executive Summary")
    a("")
    a(f"本数据集提供 {n} 个字段（MATRIX {len(matrix)} / VECTOR {len(vector)} / GROUP {len(group)}），"
      f"覆盖 `{category}` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。")
    a("")
    a("## 字段画像（Field Inventory）")
    a("")
    a("| Field ID | Type | Coverage | Field Type | Operator Adaptation | Description |")
    a("|---|---|---|---|---|---|")
    for f in fields:
        c = _coverage(f)
        cov = f"{c:.0%}" if c is not None else "N/A"
        desc = _fstr(f, "description").replace("|", "/").strip()[:120] or "—"
        fid = _field_id(f)
        ftype = _ftype(f)
        # 2026-09-04 新增：字段类型标注 + 算子适配
        field_type, op_adapt = _classify_field_type(fid, ftype, desc)
        a(f"| `{fid}` | {ftype} | {cov} | {field_type} | {op_adapt} | {desc} |")
    a("")
    a("## 字段-算子适配表（Field-Operator Adaptation）")
    a("")
    a("| Field Type | Valid Operators | Forbidden Operators | Example |")
    a("|---|---|---|---|")
    a("| 连续数值型 | `ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression` | `ts_std_dev`（波动率无预测力）、`ts_max_diff`（加速脉冲失效） | `rank(ts_mean(surprise, 22))` |")
    a("| 分类型（quantile_label/rank） | `rank/group_rank/ts_backfill` | `ts_mean`（分类平均无意义）、`ts_zscore`（非连续分布） | `rank(ts_backfill(quantile_label, 66))` |")
    a("| 概率型（prob_class） | `rank/subtract/if_else` | `ts_mean`（概率平均稀释信号）、`ts_delta`（概率变化噪声大） | `rank(prob_class1) - rank(prob_class0)` |")
    a("| 计数型（count/usd） | `ts_sum/trade_when/ts_backfill` | `ts_delta`（计数变化=已反应）、`ts_max_diff`（加速脉冲失效） | `trade_when(count > 0, rank(x), NaN)` |")
    a("| 比率型（to_price/ratio） | `rank/group_zscore/group_neutralize` | `ts_mean`（比率平均无意义）、`ts_delta`（比率变化噪声） | `group_zscore(ratio, industry)` |")
    a("| VECTOR 型 | `vec_avg/vec_sum/vec_stddev/vec_range` + `ts_mean/ts_delta/rank` | 直接用 `ts_mean`（必须先聚合） | `rank(ts_mean(vec_avg(sentiment), 22))` |")
    a("")
    a("## 字段解构（Field Deconstruction）")
    a("")
    for f in top:
        fid = _field_id(f)
        desc = _fstr(f, "description").strip() or "无描述"
        a(f"### `{fid}`（{_ftype(f)}）")
        a(f"- **测什么**：{desc}")
        a(f"- **覆盖率**：{(_coverage(f) if _coverage(f) is not None else 'N/A')}")
        a(f"- **字段名语义**：`{fid}` 的命名前缀用于字段族聚类（S1 前缀扫描）")
        a("")
    a("## 预处理决策（Preprocessing）")
    a("")
    for p in preprocess:
        a(f"- {p}")
    a("")
    a("## 特征概念（8 问框架，模板化）")
    a("")
    questions = [
        ("Q1 稳定性/不变量", "ts_mean / ts_std_dev 度量字段的长期水平与稳定性"),
        ("Q2 变化", "ts_delta / ts_scale 捕捉变化率与动量"),
        ("Q3 异常", "zscore / ts_rank 识别截面与时间序列上的离群"),
        ("Q4 交互", "两字段 add/multiply 合成新含义，注意先各自中性化"),
        ("Q5 结构", "字段占比 / 比例关系（如 components 型字段）"),
        ("Q6 累积", "ts_sum / ts_decay_linear 累积与衰减记忆"),
        ("Q7 相对", "rank / group_rank 相对定位与归一化"),
        ("Q8 本质", "第一性原理直取原始字段，剥离过拟合包装"),
    ]
    for i, (q, hint) in enumerate(questions):
        sel = top[:2] if top else []
        a(f"### {q}")
        a(f"- **使用字段**：{_fields_used(sel)}")
        a(f"- **建议**：{hint}")
        a("")

    # ------------------------------------------------------------------
    # GEM 兼容 Concept 块（2026-09-04 落地）：S2 run_pipeline 硬性要求
    # **Concept** + **Implementation Example**（含 {真实字段名} 占位符）。
    # 占位符用字段白名单中的真实 id（非 {variable}），确保
    # normalize_template_placeholders 可匹配到数据集字段后缀。
    # ------------------------------------------------------------------
    a("## GEM 兼容模板（Concept Blocks）")
    a("")
    a("> 以下 Concept 块供 S2 `brain-make-some-gem` 直接消费（`--ideas-file` 注入）。")
    a("> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。")
    a("")
    if top:
        # 2026-09-09 D9 修复：8 个 Concept 改用 _pick_diverse 选 8 个不同族字段，
        # 每个 Concept 绑定一个不同的主字段（修复前全部围绕 top[0]/top[1] 两字段，
        # 在 global_seasonal_model 上退化为 8 个 iso_week_number 日历模板）。
        diverse = _pick_diverse(fields, 8)
        # 为每个 Concept 选一个配对字段（质量次高的不同族字段），用于 Q4/Q5 交互
        def _partner(exclude_id: str) -> str:
            for f in diverse:
                pf = _field_id(f)
                if pf != exclude_id:
                    return pf
            return exclude_id

        # 8 问框架 → 8 个可解析模板，每个绑定一个不同族的主字段。
        # 占位符必须是单花括号 {%s}（2026-09-09 D10 修复）：implement_idea.py
        # 用 Python str.format 渲染模板，{{x}} 是 format 的字面转义、字段永不
        # 替换 → 表达式残留花括号被 validator 拒 → expression_list=0。
        op_specs = [
            ("长期水平稳定（Q1）", "rank(ts_mean({%s}, 66))",
             "ts_mean 度量字段长期水平，rank 截面归一化"),
            ("变化动量（Q2）", "rank(ts_delta({%s}, 21))",
             "ts_delta 捕捉 21 日变化率，rank 截面归一化"),
            ("截面离群（Q3）", "rank(zscore({%s}))",
             "zscore 识别截面离群，rank 归一化"),
            ("交互（Q4）", None,  # 特殊处理：双字段
             "两字段各自 ts_zscore 中性化后 multiply 合成"),
            ("结构占比（Q5）", None,  # 特殊处理：双字段
             "divide 构造比例关系，rank 截面归一化"),
            ("累积衰减（Q6）", "rank(ts_decay_linear({%s}, 21))",
             "ts_decay_linear 累积记忆衰减，rank 归一化"),
            ("截面相对定位（Q7）", "group_rank(ts_backfill({%s}, 66), industry)",
             "ts_backfill 稀疏回填 + group_rank 行业内相对定位"),
            ("本质直取（Q8）", "rank({%s})",
             "第一性原理直取原始字段，rank 截面归一化"),
        ]
        for i, (label, tpl_fmt, mechanism) in enumerate(op_specs):
            f1 = _field_id(diverse[i]) if i < len(diverse) else _field_id(diverse[0])
            f2 = _partner(f1)
            if tpl_fmt is None:
                # Q4 交互 / Q5 结构：双字段模板
                if "Q4" in label:
                    tpl = f"rank(multiply(ts_zscore({{{f1}}}, 66), ts_zscore({{{f2}}}, 66)))"
                else:
                    tpl = f"rank(divide({{{f1}}}, {{{f2}}}))"
            else:
                tpl = tpl_fmt % f1
            name = f"{f1} {label}"
            a(f"**Concept**: {name}")
            a(f"- **Mechanism**: {mechanism}")
            a(f"- **Fields Used**: `{f1}`, `{f2}`")
            a(f"- **Implementation Example**: `{tpl}`")
            a(f"- **Direction**: High → long")
            a("")
    else:
        a("（无字段可生成模板）")
        a("")

    a("## 字段白名单（Field Whitelist）")
    a("")
    a("```")
    for f in fields:
        a(_field_id(f))
    a("```")
    a("")
    a(f"*Report generated: {now}*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def _parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="BRAIN 数据特征工程 headless CLI（S1-S3）")
    p.add_argument("--region", required=True)
    p.add_argument("--dataset", required=True, dest="dataset_id")
    p.add_argument("--delay", type=int, required=True)
    p.add_argument("--universe", required=True)
    p.add_argument("--category", required=True)
    p.add_argument("--output", required=True)
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv or sys.argv[1:])

    out_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    try:
        brain = _load_brain_client()
    except Exception as e:
        print(f"feature_engineering: brain_api load failed: {e}", file=sys.stderr)
        return 1

    try:
        fields = asyncio.run(_fetch_fields(
            brain, args.region, args.dataset_id, args.delay, args.universe))
    except Exception as e:
        print(f"feature_engineering: get_datafields failed: {e}", file=sys.stderr)
        return 2

    if not fields:
        print(
            f"feature_engineering: no fields for {args.region}/{args.dataset_id} "
            f"d{args.delay}/{args.universe}（检查 region/delay/universe 档位是否合法）",
            file=sys.stderr,
        )
        return 2

    report = _render_report(
        args.region, args.dataset_id, args.delay, args.universe, args.category, fields)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"feature_engineering: wrote {len(fields)} fields -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
