#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""近闸 alpha 算子平替实验：从平台权威设置+表达式生成变体计划。

输入：硬编码的 20 个父 alpha（get_alpha_details 实测设置，2026-09-30 拉取）
输出：cache/opswap_plan.json（parents + variants，per-variant 完整 settings）
"""
import json
import re
from collections import Counter

PARENTS = {
    "78NgP5OQ": dict(region="IND", universe="TOP500", delay=1, decay=4, neutralization="STATISTICAL", truncation=0.08, nan="OFF", mt="OFF",
        code="rank(divide(ts_delta(ts_backfill(vec_avg(mean_flash_estimate_eps_annual12_3), 22), 66), add(abs(ts_delay(ts_backfill(vec_avg(mean_flash_estimate_eps_annual12_3), 22), 66)), 0.01)))",
        gate="SUB", gap=0.6, fail=["LOW_ROBUST_UNIVERSE_SHARPE 0.77/1.0"]),
    "d5bERLmX": dict(region="ASI", universe="MINVOL1M", delay=1, decay=12, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(rank(ts_mean(news_article_count, 22)) > 0.5, signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)), 0.5), rank(ts_mean(news_article_count, 22)) < 0.4)",
        gate="2Y", gap=0.6, fail=["IS_LADDER_SHARPE 1.57/1.58 y5", "LOW_ROBUST_UNIVERSE_RETURNS 0.0539/0.0545"]),
    "LLNgdJ6n": dict(region="ASI", universe="MINVOL1M", delay=1, decay=12, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(rank(ts_mean(news_article_count, 22)) > 0.5, signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)), 0.4), rank(ts_mean(news_article_count, 22)) < 0.4)",
        gate="2Y", gap=0.6, fail=["IS_LADDER_SHARPE 1.57/1.58 y5", "LRUR 0.0535/0.0538"]),
    "RRb2oVgo": dict(region="ASI", universe="MINVOL1M", delay=1, decay=12, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(and(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, rank(ts_mean(normalized_news_article_count, 22)) > 0.3), signed_power(subtract(group_rank(subtract(probability_label4_5quantile_20day_ohlcv, probability_label0_5quantile_20day_ohlcv), country), 0.5), 0.5), or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, rank(ts_mean(normalized_news_article_count, 22)) < 0.2))",
        gate="2Y", gap=0.6, fail=["IS_LADDER_SHARPE 1.57/1.58 y4"]),
    "3qXa26XN": dict(region="ASI", universe="MINVOL1M", delay=1, decay=12, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(rank(adv20) > 0.5, signed_power(subtract(group_rank(ep_yield_pct_smest_f12m, country), 0.5), 0.5), rank(adv20) < 0.4)",
        gate="S", gap=0.6, fail=["LRUS.WITH_RATIO 1.3/1.41", "LRUR 0.0422/0.0511", "LOW_SHARPE 1.57 warn"]),
    "88jKRbRz": dict(region="GLB", universe="MINVOL1M", delay=1, decay=6, neutralization="INDUSTRY", truncation=0.05, nan="OFF", mt="OFF",
        code="multiply(-1, group_zscore(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 5), country))",
        gate="SUB", gap=0.7, fail=["LOW_GLB_EMEA_SHARPE 0.58/1 (ra)"]),
    "LLNlP3lM": dict(region="GLB", universe="MINVOL1M", delay=1, decay=10, neutralization="COUNTRY", truncation=0.02, nan="OFF", mt="OFF",
        code="-1*group_rank(ts_decay_linear(corr_last_trade_price_with_volume, 5), industry)",
        gate="F", gap=1.0, fail=["LOW_FITNESS 0.99/1.0", "LOW_GLB_EMEA_SHARPE 0.92/1"]),
    "omL3gKEb": dict(region="ASI", universe="MINVOL1M", delay=1, decay=10, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(rank(ts_mean(normalized_news_article_count, 22)) > 0.5, signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)), 0.6), rank(ts_mean(normalized_news_article_count, 22)) < 0.4)",
        gate="F", gap=1.0, fail=["LOW_FITNESS 0.99/1.0"]),
    "58zarnp5": dict(region="ASI", universe="MINVOL1M", delay=1, decay=12, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(and(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, rank(cap) > 0.1), signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)), 0.5), or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, rank(cap) < 0.05))",
        gate="F", gap=1.0, fail=["LOW_FITNESS 0.99/1.0"]),
    "9qja8ZXr": dict(region="ASI", universe="MINVOL1M", delay=1, decay=12, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(and(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, rank(cap) > 0.1), signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)), 0.4), or(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3, rank(cap) < 0.05))",
        gate="F", gap=1.0, fail=["LOW_FITNESS 0.99/1.0"]),
    "O0Ndjl2v": dict(region="ASI", universe="MINVOL1M", delay=1, decay=6, neutralization="SUBINDUSTRY", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.35, signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)), 0.5), rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3)",
        gate="F", gap=1.0, fail=["LOW_FITNESS 0.99", "LRUS.WR 2.14/2.3", "LRUR 0.0514/0.0544"]),
    "QPb2EQQX": dict(region="ASI", universe="MINVOL1M", delay=1, decay=10, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 5), country)), 0.5)",
        gate="2Y", gap=1.3, fail=["LOW_2Y_SHARPE 1.56/1.58"]),
    "MPabLepr": dict(region="GLB", universe="MINVOL1M", delay=1, decay=15, neutralization="SUBINDUSTRY", truncation=0.08, nan="OFF", mt="OFF",
        code="signed_power(subtract(group_rank(ts_mean(vec_avg(region_relative_rank_score), 22), country), 0.5), 0.5)",
        gate="S", gap=1.3, fail=["LOW_SHARPE 1.56 warn", "LOW_GLB_EMEA 0.66 (ra)"]),
    "O0Nbp2Xv": dict(region="ASI", universe="MINVOL1M", delay=1, decay=10, neutralization="COUNTRY", truncation=0.08, nan="ON", mt="ON",
        code="signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 5), country)), 0.7)",
        gate="2Y", gap=1.3, fail=["LRUS.WR 1.89/1.92", "LOW_2Y 1.56 warn"]),
    "YPb3YL0l": dict(region="ASI", universe="MINVOL1M", delay=1, decay=6, neutralization="SUBINDUSTRY", truncation=0.08, nan="ON", mt="ON",
        code="-group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)",
        gate="2Y", gap=1.3, fail=["LRUS.WR 1.98/2.15", "LRUR 0.0459/0.0489", "LOW_2Y 1.56 warn"]),
    "KPNAZZok": dict(region="ASI", universe="MINVOL1M", delay=1, decay=10, neutralization="SUBINDUSTRY", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, signed_power(subtract(0.5, group_rank(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 4), country)), 0.7), rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) < 0.3)",
        gate="2Y", gap=1.3, fail=["IS_LADDER 1.56 y2", "LRUS.WR 2.07/2.27", "LRUR 0.052/0.0565"]),
    "LLNbPZq6": dict(region="IND", universe="TOP500", delay=1, decay=4, neutralization="STATISTICAL", truncation=0.08, nan="OFF", mt="OFF",
        code="rank(ts_zscore(ts_backfill(vec_avg(mean_flash_estimate_reportednet_annual12_2), 22), 252))",
        gate="SUB", gap=1.7, fail=["LOW_ROBUST_UNIVERSE_SHARPE 0.72/1.0"]),
    "2rwn9zxN": dict(region="GLB", universe="MINVOL1M", delay=1, decay=6, neutralization="REVERSION_AND_MOMENTUM", truncation=0.02, nan="OFF", mt="OFF",
        code="multiply(-1.0, group_zscore(ts_decay_linear(mean_last_trade_price_return_30m_pre_close_2, 5), country))",
        gate="SUB", gap=1.7, fail=["LOW_GLB_EMEA 0.69 (ra)"]),
    "d5bEP7bx": dict(region="ASI", universe="MINVOL1M", delay=1, decay=12, neutralization="SECTOR", truncation=0.08, nan="ON", mt="ON",
        code="trade_when(and(rank(adv20) > 0.4, rank(cap) > 0.4), subtract(group_rank(ep_yield_pct_smest_f12m, country), 0.5), or(rank(adv20) < 0.3, rank(cap) < 0.3))",
        gate="S", gap=1.9, fail=["LOW_SHARPE 1.55/1.58", "LRUS.WR 1.3/1.4", "LRUR 0.0534/0.0612"]),
    "kqon3M3O": dict(region="GLB", universe="MINVOL1M", delay=1, decay=10, neutralization="SUBINDUSTRY", truncation=0.08, nan="OFF", mt="OFF",
        code="subtract(group_rank(ts_mean(vec_avg(mdl239_shortlasso30d), 5), country), 0.5)",
        gate="S", gap=1.9, fail=["LOW_SHARPE 1.55 warn", "LOW_GLB_EMEA 0.64 (ra)"]),
}

SCALE_SAFE = {"ts_mean": "ts_decay_linear", "ts_decay_linear": "ts_mean"}
SCALE_CHANGE = {"ts_zscore": "ts_rank", "ts_rank": "ts_zscore",
                "group_zscore": "group_rank", "group_rank": "group_zscore",
                "zscore": "rank", "rank": "zscore"}
CMP = (">", "<", "=")


def find_calls(expr, name):
    pat = re.compile(r"\b" + re.escape(name) + r"\s*\(")
    out = []
    for m in pat.finditer(expr):
        open_i = expr.index("(", m.start())
        depth, i = 0, open_i
        while i < len(expr):
            if expr[i] == "(":
                depth += 1
            elif expr[i] == ")":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        out.append((m.start(), i))
    return out


def feeds_comparison(expr, close_i):
    j = close_i + 1
    while j < len(expr) and expr[j] in " \t":
        j += 1
    return j < len(expr) and expr[j] in CMP


def swap_variant(expr, src, dst):
    calls = find_calls(expr, src)
    if not calls:
        return None, 0, 0
    scale_changing = src in SCALE_CHANGE
    new = expr
    replaced = skipped = 0
    for start, close_i in reversed(calls):
        if scale_changing and feeds_comparison(expr, close_i):
            skipped += 1
            continue
        open_i = expr.index("(", start)
        new = new[:start] + dst + new[open_i:]
        replaced += 1
    if replaced == 0:
        return None, 0, skipped
    return new, replaced, skipped


def main():
    variants = []
    for pid, p in PARENTS.items():
        for table in (SCALE_SAFE, SCALE_CHANGE):
            for src, dst in table.items():
                new, n, sk = swap_variant(p["code"], src, dst)
                if new and new != p["code"]:
                    variants.append({
                        "parent": pid, "region": p["region"], "gate": p["gate"],
                        "gap_pct": p["gap"], "swap": src + "->" + dst,
                        "n_sites": n, "skipped_sites": sk, "expression": new,
                        "settings": {k: p[k] for k in ("region", "universe", "delay", "decay",
                                                       "neutralization", "truncation", "nan", "mt")}})
    dedup = {}
    for v in variants:
        k = (v["region"], v["settings"]["universe"], v["settings"]["neutralization"], v["expression"])
        if k not in dedup:
            dedup[k] = v
    variants = list(dedup.values())

    bad = [v for v in variants if v["expression"].count("(") != v["expression"].count(")")]
    print("variants:", len(variants), "paren-unbalanced:", len(bad))
    print("swap dist:", dict(Counter(v["swap"] for v in variants)))
    print("group (nan,mt):", dict(Counter((v["settings"]["nan"], v["settings"]["mt"]) for v in variants)))
    with open("cache/opswap_plan.json", "w", encoding="utf-8") as f:
        json.dump({"parents": PARENTS, "variants": variants}, f, ensure_ascii=False, indent=1)
    print("saved cache/opswap_plan.json")
    for v in variants:
        print("  %-10s %-28s sites=%d skip=%d | %s" % (
            v["parent"], v["swap"], v["n_sites"], v["skipped_sites"], v["expression"][:100]))


if __name__ == "__main__":
    main()
