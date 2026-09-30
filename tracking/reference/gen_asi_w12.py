"""ASI w12 —— 换数据集（`quant_factor_lib`，credit-risk/model 类），双赢：换塔 + 换信号。

## 为什么（本轮结论）

ASI 的**尾盘反转族已被本项目自己占满**（1YZYj5QQ last60 + E5R56EbR last30，自相关下限 ~0.57~0.69），
继续在同一族里挖，self-corr 很难再 <0.7。必须换**信号概念**。

`quant_factor_lib`（category=**model**，32 字段全 **VECTOR**，valueScore **6.0**，users 仅 31）：
**信用风险 / 财务质量**信号，与价格反转在语义上完全正交：
- `qfl_cassie_qes_cassie_impliedalpha` —— 信贷模型推出的**隐含超额收益**（cov .72）
- `qfl_cassie_qes_cassie_score` / `qfl_cassie_qes_cassie_prelimcomposite` —— CASSIE 综合信贷评分（cov .84）
- `qfl_cassie_model_altman_zscore` —— Altman Z（破产概率，越高越安全）
- `qfl_cassie_model_ohlson_oscore` —— Ohlson O（越高越可能违约）
- `qfl_cassie_model_merton` / `qfl_cassie_model_chs_default` —— 违约距离 / 违约概率
- `qfl_cassie_qes_alter_insolvency_stress_1y/2y/9m` —— 前瞻性偿债压力
- `qfl_cassie_convention_current_ratio` / `quick_ratio` / `ocf_currliab` / `debt_equity` / `longdebt_equity`

**双赢**：① 换塔 → `ASI/D1/MODEL`（当前 **1**，差 2 颗）；② 换信号 → 与已提交的 PV 反转 alpha 天然低相关。

## 合规

- 单信号腿（一个信用/质量字段）→ 非混信号。
- VECTOR 字段须 `vec_avg()` 降维（参照已 ACTIVE 的 `qMNMbeGj`：
  `rank(ts_rank(ts_delta(ts_backfill(vec_avg(oth36_short_pos_in_shares), 200), 66), 250))`）。
- `ts_backfill(x, 200)` 处理非每日更新的申报数据（信用指标按季更新）。

## 方向假设（信用/质量类标准方向）
- 「越高越好」类（Z-score / Merton 距离 / 流动比率 / 隐含 alpha）→ **做多高分位** → `subtract(group_rank, 0.5)`
- 「越高越危险」类（O-score / 违约概率 / 偿债压力 / 负债率）→ **做空高分位** → `subtract(0.5, group_rank)`
两类都跑，让数据判定方向。
"""
import json
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "ASI", "candidates", "exprs_asi_w12.json")

VOL_SHARE = "rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22)))"
NEWS = "rank(ts_mean(normalized_news_article_count, 22))"
GATE = f"and({VOL_SHARE} > 0.5, {NEWS} > 0.3)"
EXIT = f"or({VOL_SHARE} < 0.3, {NEWS} < 0.2)"

# (tag, field, direction)  direction: +1 = 做多高分位, -1 = 做空高分位
FIELDS = [
    ("implalpha",  "qfl_cassie_qes_cassie_impliedalpha",            +1),
    ("cassiescore", "qfl_cassie_qes_cassie_score",                  +1),
    ("prelimcomp", "qfl_cassie_qes_cassie_prelimcomposite",         +1),
    ("altmanz",    "qfl_cassie_model_altman_zscore",                +1),
    ("ohlsono",    "qfl_cassie_model_ohlson_oscore",                -1),
    ("merton",     "qfl_cassie_model_merton",                       +1),
    ("chsdefault", "qfl_cassie_model_chs_default",                  -1),
    ("insolv1y",   "qfl_cassie_qes_alter_insolvency_stress_1y",     -1),
    ("currratio",  "qfl_cassie_convention_current_ratio",           +1),
    ("quickratio", "qfl_cassie_convention_quick_ratio",             +1),
    ("ocfcurrliab", "qfl_cassie_convention_ocf_currliab",           +1),
    ("debteq",     "qfl_cassie_convention_debt_equity",             -1),
    ("ltdteq",     "qfl_cassie_convention_longdebt_equity",         -1),
    ("extinsolv1y", "qfl_cassie_qes_alter_extreme_insolvency_stress_1y", -1),
]


def core(fld, direction, dec=22, group="country"):
    """VECTOR 降维 → 填补 → 平滑 → 横截面排名 → 零均值化。"""
    base = f"ts_decay_linear(ts_backfill(vec_avg({fld}), 200), {dec})"
    if direction > 0:
        return f"subtract(group_rank({base}, {group}), 0.5)"
    return f"subtract(0.5, group_rank({base}, {group}))"


exprs = []
seen = set()


def add(lab, e):
    if e not in seen:
        seen.add(e)
        exprs.append([lab, e])


# 1) 裸信号（不加门控）—— 信用/质量类慢信号，换手天然较低
for tag, fld, d in FIELDS:
    add(f"W12_raw_{tag}", core(fld, d))

# 2) 关键字段 + 已证门控（可同时挂 MODEL + SENTIMENT 两塔）
for tag, fld, d in FIELDS[:4]:
    add(f"W12_gate_{tag}", f"trade_when({GATE}, {core(fld, d)}, {EXIT})")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(exprs, f, ensure_ascii=False, indent=1)

print(f"written {len(exprs)} exprs -> {os.path.abspath(OUT)}")
for lab, _ in exprs:
    print(" ", lab)
