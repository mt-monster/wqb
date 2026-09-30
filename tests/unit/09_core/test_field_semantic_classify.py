# -*- coding: utf-8 -*-
"""`tools/field_semantic_classify.py` 归类口径回归测试（2026-09-28）。

守护两处**已发生的误杀**（都是「靠名字/裸名词判语义」造成的）：

  ① `is_` 子串 → 把 **Income Statement** 字段当布尔标志
     实证：`oth466_is_ebit_oper_q`（EBIT Operating Income，users=248）等 39/177（22%）
     被误杀，且被杀的恰是全集 users 最高的利润表核心字段。

  ② 裸 `\bindicator\b` → 把**技术分析指标**当布尔标志
     实证：model109 的 Bollinger Bands / Negative Volume Index / **Altman Z-score** /
     Chaikin Money Flow / Money Flow Index / Stochastic Oscillator 描述均含 "indicator"，
     51/539 被误判。

正确口径：名字规则只认**无歧义强标识符**（gvkey/cusip/isin/exrate/currency_code/日期…）；
布尔标志必须由**显式布尔措辞**判定（"indicator denoting whether" / "equals 1" /
"dummy variable" / "1 if … 0 otherwise"），仅出现 indicator/flag 名词不算。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "field_semantic_classify.py"


def _load():
    spec = importlib.util.spec_from_file_location("_fsc", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_fsc"] = mod
    spec.loader.exec_module(mod)
    return mod


# ---- ① Income Statement 不得被当标志位 ----

def test_income_statement_fields_are_signal():
    """is_ = Income Statement 的核心利润表字段必须是信号字段。"""
    fsc = _load()
    cases = [
        ("oth466_is_ebit_oper_q", "EBIT (Operating Income)"),
        ("oth466_is_ptx_inc_norm_q", "Normalized Income Before Taxes"),
        ("oth466_is_consol_net_inc_q", "Net Income - Consolidated"),
        ("oth466_is_gross_inc_q", "Gross Profit"),
        ("oth466_is_basic_eps_cont_ops_q", "Basic EPS Before Abnormal Items"),
    ]
    for name, desc in cases:
        cat, label = fsc.classify(desc, name)
        assert cat is not None, f"{name}（{desc}）被误判为非信号：{label}"


def test_technical_indicators_are_signal():
    """indicator = 技术分析指标（Bollinger/Altman/MFI…）不得被当布尔标志。"""
    fsc = _load()
    cases = [
        ("mdl109_altman1983", "Altman's Z-score using the 1983 revised formula, "
                              "an updated bankruptcy risk and financial distress indicator"),
        ("mdl109_bb", "Bollinger Bands, a technical analysis indicator constructed from "
                      "a moving average and standard deviation"),
        ("mdl109_ifm", "Money Flow Index, a volume-weighted momentum indicator"),
        ("mdl109_os", "Stochastic Oscillator, a momentum indicator comparing a particular "
                      "closing price to a range of prices"),
    ]
    for name, desc in cases:
        cat, label = fsc.classify(desc, name)
        assert cat is not None, f"{name}（{desc[:50]}）被误判为非信号：{label}"


# ---- 真正的标志位/标识符仍必须被拦 ----

def test_true_flags_and_identifiers_still_blocked():
    """真布尔标志与强标识符必须仍被拦（收紧不能过头）。"""
    fsc = _load()
    blocked_cases = [
        ("us_equity_retail_sector_flag",
         "Indicator denoting whether a U.S. company operates primarily in the retail sector"),
        ("us_equity_korea_country_flag",
         "Indicator denoting whether a U.S. company is primarily domiciled in Korea"),
        ("pricing_currency_code_ras1", "Pricing currency code"),
        ("fnd17_1_usdtorepexrate", "Exchange rate from reporting currency to USD"),
        ("transaction_currency_code", "Three-letter ISO currency code of the transaction"),
        ("insd1_gvkey", "Compustat Global Company Identifier (Global Value Key)"),
        ("insd5_recent_dt", "Most recent transaction date"),
    ]
    for name, desc in blocked_cases:
        cat, label = fsc.classify(desc, name)
        assert cat is None, f"{name} 应被拦为 {label}，实际判为信号字段 {cat}"


def test_two_cues_required_for_flag_description():
    """仅出现 indicator/flag 名词（无布尔措辞）不得判为标志位。"""
    fsc = _load()
    cat, _ = fsc.classify("A price momentum indicator used for timing", "mdl109_mom")
    assert cat is not None, "裸 indicator 名词不应触发标志位判定"
    cat2, _ = fsc.classify("Trading flag recorded when a corporate action happens", "x_trade_flag")
    assert cat2 is not None, "裸 flag 名词不应触发标志位判定"
