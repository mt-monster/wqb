# -*- coding: utf-8 -*-
"""wqb.expression.op_arity 回归守护 —— 2026-09-07 hump 事故。

事故还原：``hump(x, 0.005)`` 通过了 wave_gate 的语法闸（"语法 8/8 PASS"），
平台却回 ``Invalid number of inputs : 2, should be exactly 1 input(s).``，
并因此 **CANCEL 掉整个 8 条 multisim**（id 2Vt1RwZw4KGcajcZxpWLyW）——
2 条畸形表达式烧掉 8 个槽位。

根因：catalog 签名 ``hump(x, hump = 0.01)`` 里的 ``=`` 标记 ``hump`` 为
**命名参数**（只能写 ``hump=0.005``）；对照 ``ts_decay_linear(x, d, dense =
false)``，``d`` 无 ``=`` 故可位置传参。旧闸只查括号平衡与字段存在性。

这些测试同时守两个方向：
- **该拦的要拦**：命名参数被当位置参数传（hump/rank/quantile/scale/tail/bucket）
- **不该拦的别拦**：``ts_backfill(x, 120)`` 这类合法位置写法（仓库有 2800+ 处
  历史实证），误杀会让整条挖掘流水线停摆
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "src"))

from wqb.expression.op_arity import (  # noqa: E402
    ArityError,
    check_expression,
    check_expressions,
    ensure_safe_for_dispatch,
    iter_call_sites,
    load_signatures,
    parse_definition,
)


# ---------------------------------------------------------------------------
# 1. 事故本体
# ---------------------------------------------------------------------------

def test_hump_positional_second_arg_is_rejected():
    """事故复现：hump(x, 0.005) 必须 FAIL（旧闸报 PASS，平台 CANCEL 整批）。"""
    errors = check_expression("hump(x, 0.005)")
    assert errors, "hump(x, 0.005) 必须被拦下——平台报 Invalid number of inputs : 2"
    joined = " ".join(errors)
    assert "hump" in joined
    # 报错要给出可直接照抄的修法，而不是只说"参数不对"
    assert "hump=0.005" in joined


def test_hump_named_form_passes():
    """正确写法 hump(x, hump=0.005) 必须放行。"""
    assert check_expression("hump(rank(close), hump=0.005)") == []


def test_hump_error_quotes_platform_message():
    """错误文案要带平台原话，便于把本地 FAIL 与平台回执对上号。"""
    (msg,) = check_expression("hump(close, 0.005)")
    assert "Invalid number of inputs : 2, should be exactly 1 input(s)." in msg


def test_hump_unknown_named_param_is_rejected():
    """拼错命名参数（humps=）也要拦——平台同样不认。"""
    errors = check_expression("hump(close, humps=0.01)")
    assert errors and "humps" in errors[0]


# ---------------------------------------------------------------------------
# 2. 同类命名参数陷阱（catalog 里 29 个算子带 `=`，hump 只是引爆的那个）
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("expr", [
    "rank(close, 2)",                     # rank(x, rate=2)
    "quantile(close, 0.5)",               # quantile(x, driver=, sigma=)  wave17Z 实证
    "winsorize(close, 4)",                # winsorize(x, std=4)
    "ts_decay_linear(close, 5, true)",    # dense=false 是命名参数
    "scale(close, 1, 1, 1)",              # scale/longscale/shortscale 全命名
    "tail(rank(close), 0.1, 0.9, 0.5)",   # lower/upper/newval 全命名
    "bucket(rank(cap), 5)",               # range=/buckets= 必须命名（见 docs/reference)
    "ts_rank(close, 22, 1)",              # constant=0 是命名参数
    "normalize(close, true, 0.5)",        # useStd/limit 是命名参数
])
def test_named_only_params_rejected_positionally(expr):
    assert check_expression(expr), f"{expr} 应被拦下（命名参数被当位置参数传）"


@pytest.mark.parametrize("expr", [
    "rank(close, rate=2)",
    "quantile(close, driver=gaussian, sigma=1.0)",
    "winsorize(close, std=4)",
    "ts_decay_linear(close, 5, dense=true)",
    "scale(close, scale=1, longscale=1, shortscale=1)",
    "tail(rank(close), lower=0.1, upper=0.9, newval=0.5)",
    'bucket(rank(cap), range="0,1,0.1")',
    "ts_rank(close, 22, constant=1)",
    "normalize(close, useStd=true, limit=0.5)",
])
def test_named_forms_pass(expr):
    assert check_expression(expr) == [], f"{expr} 是合法写法，不能误杀"


# ---------------------------------------------------------------------------
# 3. 反向守护：合法的位置写法绝不能误杀
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("expr", [
    # ts_backfill(x, lookback = d, k=1)：lookback 的默认值 d 是占位符不是字面量，
    # 因此仍可位置传参。仓库里 ts_backfill(x, 66) 有 2800+ 处历史实证。
    "ts_backfill(close, 120)",
    "ts_backfill(vec_avg(fld), 66)",
    "ts_backfill(close, 120, k=1)",
    "ts_mean(close, 22)",
    "ts_regression(close, open, 252, lag=0, rettype=2)",
    "group_rank(close, sector)",
    "group_backfill(close, sector, 66, std=4.0)",
    "trade_when(volume > 0, rank(close), -1)",
    "kth_element(close, 66, 2, ignore=\"NaN\")",
    "ts_quantile(close, 22, driver=\"uniform\")",
    # 变参算子：add/subtract/multiply/max/min 位置参数无上限
    "add(a, b, c, d)",
    "subtract(rank(a), rank(b), filter=true)",
    "max(a, b, c)",
    "multiply(a, b, c, filter=false)",
    # 中缀/多语句/嵌套：扫描器必须容忍
    "ts_mean(close, 22) + ts_mean(open, 22)",
    "x = ts_mean(close, 22); rank(x)",
    'group_neutralize(ts_zscore(close, 252), bucket(rank(cap), range="0, 1, 0.1"))',
    "if_else(close > open, 1, -1)",
    "ts_delay(close, -1)",
])
def test_valid_expressions_not_flagged(expr):
    assert check_expression(expr) == [], f"{expr} 是平台合法写法，误杀会拖停流水线"


def test_no_false_positives_on_accepted_alpha_corpus():
    """把闸跑过"平台已接受"的历史表达式，误杀率必须为 0。

    语料取 data/wqb.db 里拿到 alpha_id 的表达式——平台真跑通过，不可能是元数
    错误。DB 不在（CI 干净 checkout）则跳过。
    """
    import sqlite3

    db = REPO_ROOT / "data" / "wqb.db"
    if not db.is_file():
        pytest.skip("data/wqb.db 不存在（干净 checkout）")
    conn = sqlite3.connect(str(db))
    try:
        corpus = {
            e for (e,) in conn.execute(
                "select expression from alphas "
                "where expression is not null and trim(expression) <> ''")
        }
        corpus |= {
            e for (e,) in conn.execute(
                "select code from backtest_results where alpha_id is not null "
                "and code is not null and trim(code) <> ''")
        }
    finally:
        conn.close()
    if not corpus:
        pytest.skip("语料为空")
    sigs = load_signatures()
    # 已知 3 条脏数据：截断/串行的历史行（signed_power(0.5)M.40+e3.60 之流），
    # 任何语法检查都会拒，不算本闸误杀。
    flagged = [e for e in corpus
               if check_expression(e, sigs) and "(" in e and e.count("(") == e.count(")")]
    corrupt = [e for e in flagged if not e.rstrip().endswith(")")]
    real = [e for e in flagged if e not in corrupt]
    assert not real, f"对已被平台接受的表达式产生误杀: {real[:5]}"


# ---------------------------------------------------------------------------
# 4. 签名解析规则
# ---------------------------------------------------------------------------

def test_parse_definition_marks_literal_default_as_named_only():
    sig = parse_definition("hump", "hump(x, hump = 0.01)")
    assert sig.positional == ("x",)
    assert sig.max_positional == 1
    assert sig.named == ("hump",)


def test_parse_definition_keeps_placeholder_default_positional():
    """``lookback = d`` 的 d 是占位符（"你来填天数"），不是字面默认值。"""
    sig = parse_definition("ts_backfill", "ts_backfill(x,lookback = d, k=1)")
    assert sig.positional == ("x", "lookback")
    assert sig.max_positional == 2
    assert sig.min_positional == 1
    assert sig.named == ("k",)


def test_parse_definition_detects_variadic():
    sig = parse_definition("max", "max(x, y, ..)")
    assert sig.variadic and sig.max_positional is None


def test_parse_definition_unions_alternate_forms():
    """bucket 的 definition 有 range=/buckets= 两式，命名参数取并集。"""
    sig = parse_definition(
        "bucket",
        'bucket(rank(x), range=“0, 1, 0.1”, skipBoth=False, NaNGroup=False)\r\n'
        'or\r\nbucket(rank(x), buckets = “2,5,6,7,10”, skipBoth=False, NaNGroup=False)')
    assert set(sig.named) == {"range", "buckets", "skipBoth", "NaNGroup"}
    assert sig.max_positional == 1


def test_named_params_keep_declaration_order():
    """报错提示要按声明顺序对号入座（排序会给出 lower/newval/upper 的错建议）。"""
    sig = parse_definition("tail", "tail(x, lower = 0, upper = 0, newval = 0)")
    assert sig.named == ("lower", "upper", "newval")
    (msg,) = check_expression("tail(rank(close), 0.1, 0.9, 0.5)")
    assert "lower=0.1, upper=0.9, newval=0.5" in msg


def test_ts_decay_linear_contrast_with_hump():
    """任务书里的对照组：d 是位置参数，只有 dense 是命名参数。"""
    sig = parse_definition("ts_decay_linear", "ts_decay_linear(x, d, dense = false)")
    assert sig.positional == ("x", "d") and sig.named == ("dense",)


# ---------------------------------------------------------------------------
# 5. 调用点扫描
# ---------------------------------------------------------------------------

def test_iter_call_sites_handles_nesting_and_strings():
    sites = {s.name: s for s in iter_call_sites(
        'group_rank(ts_backfill(close, 66), bucket(rank(cap), range="0, 1, 0.1"))')}
    assert set(sites) == {"group_rank", "ts_backfill", "bucket", "rank"}
    # 字符串里的逗号不能被当参数分隔符
    assert len(sites["bucket"].positional) == 1
    assert sites["bucket"].named == [("range", '"0, 1, 0.1"')]


def test_comparison_operators_are_not_named_args():
    """``x == y`` / ``x >= y`` 不能被误判成命名参数。"""
    (site,) = [s for s in iter_call_sites("trade_when(a >= b, c, d)")
               if s.name == "trade_when"]
    assert site.named == [] and len(site.positional) == 3


# ---------------------------------------------------------------------------
# 6. 未知算子放行（幽灵算子归 operator_audit 管，本闸不双重误报）
# ---------------------------------------------------------------------------

def test_unknown_operator_is_skipped():
    assert check_expression("ts_median(close, 22, 3, 4)") == []


# ---------------------------------------------------------------------------
# 7. 批级接口
# ---------------------------------------------------------------------------

def test_check_expressions_reports_per_item():
    report = check_expressions(["hump(close, 0.005)", "ts_mean(close, 22)"])
    assert report["total"] == 2 and report["passed"] == 1 and not report["ok"]
    assert report["items"][0]["valid"] is False
    assert report["items"][1]["valid"] is True


def test_ensure_safe_for_dispatch_raises_on_the_incident_batch():
    """事故批的形状：8 条里混 2 条畸形 —— 发批前必须抛异常挡住整批。"""
    batch = ["ts_mean(close, 22)"] * 6 + ["hump(close, 0.005)", "hump(open, 0.01)"]
    with pytest.raises(ArityError):
        ensure_safe_for_dispatch(batch)


# ---------------------------------------------------------------------------
# 8. 签名表数据源
# ---------------------------------------------------------------------------

def test_catalog_snapshot_is_loadable_and_covers_hump():
    catalog = REPO_ROOT / "docs" / "reference" / "operators_catalog.json"
    assert catalog.is_file(), "docs/reference/operators_catalog.json 缺失（get_operators 快照）"
    payload = json.loads(catalog.read_text(encoding="utf-8"))
    names = {o["name"] for o in payload["results"]}
    assert {"hump", "rank", "quantile", "ts_backfill"} <= names
    sigs = load_signatures(str(catalog))
    assert sigs["hump"].named == ("hump",)


def test_notes_fallback_parses_operator_signatures():
    """离线兜底：docs/reference/operators_notes.md 也要能推出 hump 签名。"""
    notes = REPO_ROOT / "docs" / "reference" / "operators_notes.md"
    if not notes.is_file():
        pytest.skip("operators_notes.md 不存在")
    from wqb.expression.op_arity import _load_from_notes

    sigs = _load_from_notes(str(notes))
    assert sigs["hump"].named == ("hump",)
    assert sigs["hump"].max_positional == 1
    assert sigs["ts_decay_linear"].positional == ("x", "d")


# ---------------------------------------------------------------------------
# 9. verifier 手写签名表 vs catalog 的漂移看板
# ---------------------------------------------------------------------------

def test_verifier_table_hump_is_keyword_only():
    """alpha-expression-verifier 的手写表里 hump 必须标 keyword_only。

    这是事故的直接触发点：表里漏标，于是 PLY 闸放行 hump(x, 0.005)。
    """
    scripts = REPO_ROOT / "Claude" / "skills" / "alpha-expression-verifier" / "scripts"
    text = (scripts / "validator.py").read_text(encoding="utf-8")
    line = next(ln for ln in text.splitlines() if ln.strip().startswith("'hump':"))
    assert "keyword_only" in line, "hump 漏标 keyword_only —— 2026-09-07 事故复发"
