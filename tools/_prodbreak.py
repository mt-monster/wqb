# -*- coding: utf-8 -*-
"""破 prod 墙 · 归因 + 对照实验（2026-10-27）

## 归因（基于今日 9 颗 prod 实测）
| alpha | 类别 | 结构 | S | prod |
|---|---|---|---|---|
| rKRpEMWo | MODEL | 三腿 pow .5 | 1.75 | **0.594** |
| P0oQoVQL | FUND+OTHER | 四腿 pow .5 | 2.11 | 0.7408 |
| QPvZEQXX | OTHER | 两腿 pow .5 | 1.93 | 0.7481 |
| zq3Kk39K | MODEL+FUND+OTHER | 三腿 pow .5 | 2.78 | 0.7508 |
| mLowboV5 | FUND | 两腿 pow .5 | 1.73 | 0.7971 |
| vROPXLNa | OTHER | 单腿 pow .7 | 1.91 | 0.8511 |
| VkdeWGgw | OTHER | 单腿 pow .7 | 1.69 | 0.9114 |

**共同点**：全部用 `signed_power(rank(ts_backfill(F,22)), 0.5)`（或 0.7）作归一。
0.5 次幂 = **压平分布** ⇒ 权重趋近等权 ⇒ 与生产池里"通用因子等权组合"持仓重叠最大。
⇒ **归因结论：L2 归一化层（0.5 次幂）是 prod 的共同放大器，而这一层从未在 prod 轴上扫过。**
（此前所有 prod 实验只改 L1 信息源 / 加腿，等价于换字段，故 prod 恒 0.74–0.80。）

论坛证据（MH33574 帖，141 赞，评论 YL61874）：
`signed_power(ts_zscore(A) − ts_zscore(B), 3)` 实测 **PC 0.9 → 0.64 且 Sharpe 基本不变**；
并明确指出 `signed_power(·,2)` 放大端部易触发 weight check ⇒ 用**奇次幂 ≥3**。

## 对照实验（一次一变量）
- **X1（L2 归一轴）**：只改幂次。p∈{1.0,1.5,3.0,5.0} 内层 + 外层立方（对去中心后的合成值）
- **X2（L4 正交轴）**：在 p=1.0 基线上各加一条正交化，与 `a_p10` 对比 ⇒ 干净隔离
  cap 分桶中性化（PV×FUND 合规）｜动量残差（论文 Blitz 2011）｜波动残差
"""
import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SUBMIT = os.path.join(ROOT, "tools", "submit_batch.py")
HARVEST = os.path.join(ROOT, "cache", "_harvest_safe.py")
CK = os.path.join(ROOT, "results", "_prodbreak_ck.json")
LEDGER = os.path.join(ROOT, "results", "_prodbreak_ledger.json")

sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
COMMON = dict(region="EUR", delay="1", truncation="0.08",
              nan_handling="ON", max_trade="ON", mode="FULL")

# --- 基线（mLowboV5 / QPvZEQXX 的原始字段） ---
F23_MAIN = "bank_assets_investment"
F23_VBTS = "fnd23_intfvalld1_vbts"
TI_MAIN = "tm_16_r1_r5_r10_rh_glb_d1_r5_q1"
TI_15 = "predicted_first_quantile_ten_day_return_15"


def sig(f, p="0.5"):
    return "signed_power(rank(ts_backfill(%s, 22)), %s)" % (f, p)


def two_leg(f1, w2, f2, p="0.5"):
    return "add(%s, multiply(%s, %s))" % (sig(f1, p), w2, sig(f2, p))


def outer(expr, center, p):
    """外层奇次幂：对去中心后的合成值取幂 ⇒ 权重集中到极端（论坛实证降 PC）。
    center = 各腿 rank 均值之和（两腿各 0.5 ⇒ 1.0；1+0.7 加权 ⇒ 0.85）。"""
    return "signed_power(subtract(%s, %s), %s)" % (expr, center, p)


# 基线 A：fundamental23 @ TOP2500（mLowboV5，S1.73 / prod 0.7971）
SET_A = dict(universe="TOP2500", decay="4", neutralization="FAST")
A_BASE_P05 = two_leg(F23_MAIN, "0.7", F23_VBTS)
# 基线 B：techindi_model @ TOPCS1600（QPvZEQXX，S1.93 / prod 0.7481）
SET_B = dict(universe="TOPCS1600", decay="4", neutralization="FAST")
B_BASE_P05 = two_leg(TI_MAIN, "1.0", TI_15)

PLAN = [
    # ===== X1：L2 归一层（幂次）—— 唯一在所有 9 颗候选上恒定、且从未在 prod 轴扫过的层 =====
    ("X1_struct", "fundamental23", SET_A, [
        ("a_p10", two_leg(F23_MAIN, "0.7", F23_VBTS, "1.0")),      # 线性三角权重（对照基准，用于 X2）
        ("a_p15", two_leg(F23_MAIN, "0.7", F23_VBTS, "1.5")),
        ("a_p30", two_leg(F23_MAIN, "0.7", F23_VBTS, "3.0")),      # 论坛主推：集中端部
        ("a_p50", two_leg(F23_MAIN, "0.7", F23_VBTS, "5.0")),
        ("a_out3", outer(A_BASE_P05, "0.85", "3.0")),              # 外层立方（原样保留 0.5 内层）
    ]),
    ("X1b_struct", "techindi_model", SET_B, [
        ("b_p10", two_leg(TI_MAIN, "1.0", TI_15, "1.0")),
        ("b_p30", two_leg(TI_MAIN, "1.0", TI_15, "3.0")),
        ("b_out3", outer(B_BASE_P05, "1.0", "3.0")),
    ]),
    # ===== X2：L4 正交轴（在 a_p10 基线上各加一条，与 a_p10 直接对比） =====
    # 论文依据：Blitz/Huij/Martens (2011) Residual Momentum —— 按残差收益排序，
    #   风险调整收益翻倍、波动大幅下降、不集中于极端与小盘 ⇒ 残差化是"去共同暴露"的正统手段。
    # USA 实测（MEMORY §12）：动量轴 Δprod −0.073 ≫ 波动 −0.032 > cap −0.010。
    ("X2_orth", "fundamental23", SET_A, [
        ("a_capneu", "group_neutralize(%s, bucket(rank(cap), range=\"0,1,0.1\"))"
         % two_leg(F23_MAIN, "0.7", F23_VBTS, "1.0")),
        ("a_momneut", "vector_neut(%s, rank(ts_mean(returns, 63)))"
         % two_leg(F23_MAIN, "0.7", F23_VBTS, "1.0")),
        ("a_volneut", "vector_neut(%s, rank(ts_std_dev(returns, 252)))"
         % two_leg(F23_MAIN, "0.7", F23_VBTS, "1.0")),
    ]),
]


# ===== X3~X6：最后两个未测轴（每变体独立 settings ⇒ 各成单条一批） =====
# 依据：A 型（fund23，mean 0.10）需把分布整体左移。size 暴露是最可疑的主成分
#   （cap 分桶中性化已把 S 从 1.49 拉到 2.16）。这里用**不改 ATOM**的两条 settings 轴验证：
#   ① universe 收窄到 TOP1200/TOP800 ⇒ 砍掉小盘尾，等价于"粗粒度 size 控制"，仍单数据集
#   ② neutralization 换档（NONE / CROWDING）⇒ 论坛"大幅变化靠中性化"，此前只测过 FAST
BANK1 = "signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.0)"
VBTS1 = "signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.0)"
OFC1 = "signed_power(rank(ts_backfill(fnd23_ofc, 22)), 1.0)"
CAPG = 'bucket(rank(cap), range="0,1,0.1")'


def _bn(w_ofc, w_vb="0.7"):
    core = "add(add(%s, multiply(%s, %s)), multiply(%s, %s))" % (BANK1, w_vb, VBTS1, w_ofc, OFC1)
    return "group_neutralize(%s, %s)" % (core, CAPG)


def _cap(pw):
    core = two_leg(F23_MAIN, "0.7", F23_VBTS, pw)
    return "group_neutralize(%s, %s)" % (core, CAPG)


Z15 = "group_neutralize(add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.5), multiply(0.7, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.5))), bucket(rank(cap), range=\"0,1,0.1\"))"

P15 = "add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.5), multiply(0.7, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.5)))"

def _cp(pw, rng="0,1,0.1"):
    core = two_leg(F23_MAIN, "0.7", F23_VBTS, pw)
    return "group_neutralize(%s, bucket(rank(cap), range=\"%s\"))" % (core, rng)


def _cp2(pw, w_vb, rng="0,1,0.1"):
    core = two_leg(F23_MAIN, w_vb, F23_VBTS, pw)
    return "group_neutralize(%s, bucket(rank(cap), range=\"%s\"))" % (core, rng)


IABS_ = "fnd23_intfvalld1_iabs"
IADS_ = "fnd23_intfvalld1_iads"
FBDS_ = "fnd23_intfvalld1_fbds"
SEBV_ = "fnd23_intfvalld1_sebv"
SEDV_ = "fnd23_intfvalld1_sedv"


def _cap20(core):
    return 'group_neutralize(%s, bucket(rank(cap), range="0,1,0.05"))' % core


RISK68 = "risk68"

PLAN += [
    # ===== Z_risk：RISK 塔（差 1 颗点亮）—— risk68 独有 `rsk68_residual_return`（**现成残差收益**）
    #   ⇒ 天然对应 Blitz/Huij/Martens (2011) 残差动量，不需要把风险暴露当 alpha 用。
    #   ⚠ 铁律：RISK 不能与 PV（returns/close/volume/cap/adv20）组腿 ⇒ 以下 6 条全部单数据集。
    ("Z1_risk_cs1600", RISK68, dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("rk_direct", sig("rsk68_residual_return")),
      ("rk_z63", "signed_power(rank(ts_zscore(ts_backfill(rsk68_residual_return, 22), 63)), 0.5)"),
      ("rk_m63", "signed_power(rank(ts_mean(ts_backfill(rsk68_residual_return, 5), 63)), 0.5)"),
      ("rk_m126", "signed_power(rank(ts_mean(ts_backfill(rsk68_residual_return, 5), 126)), 0.5)"),
      ("rk_volw", sig("rsk68_weight_volatility_short")),
      ("rk_lowbeta", "signed_power(rank(multiply(-1, ts_backfill(rsk68_beta, 22))), 0.5)")]),
    ("Z2_risk_top2500", RISK68, dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("rk2_direct", sig("rsk68_residual_return")),
      ("rk2_z63", "signed_power(rank(ts_zscore(ts_backfill(rsk68_residual_return, 22), 63)), 0.5)"),
      ("rk2_m63", "signed_power(rank(ts_mean(ts_backfill(rsk68_residual_return, 5), 63)), 0.5)"),
      ("rk2_lowbeta", "signed_power(rank(multiply(-1, ts_backfill(rsk68_beta, 22))), 0.5)")]),
    # ===== U2：把「分组中性化」用在 fund23 ⇒ **不同结构**（无 cap 桶），保 ATOM（分组字段豁免）
    # 现有 `1YNerr2X` 的结构是 cap 桶；本批去掉 cap、改用分组字段 ⇒ AST 不同 ⇒ 可能是第二席。
    # fund23 的 2Y 闸很强（2.42），保 ATOM 时走 2Y 而非 ladder。
    ("U2_fund_grp", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("uu_f_sector", "group_neutralize(%s, sector)" % two_leg(F23_MAIN, "0.7", F23_VBTS, "2.1")),
      ("uu_f_industry", "group_neutralize(%s, industry)" % two_leg(F23_MAIN, "0.7", F23_VBTS, "2.1")),
      ("uu_f_subind", "group_neutralize(%s, subindustry)" % two_leg(F23_MAIN, "0.7", F23_VBTS, "2.1")),
      ("uu_f_p15sub", "group_neutralize(%s, subindustry)" % two_leg(F23_MAIN, "0.7", F23_VBTS, "1.5"))]),
    # ===== U：分组字段中性化（保 ATOM —— memory §5 的 6 个豁免字段：
    #   country/exchange/market/sector/industry/subindustry ⇒ 不破 Single Dataset、不触发 IS_LADDER）
    # 依据：techindi 的幂次杠杆已被否证（pow1.5 0.7276 → pow2.1 0.7336，prod 反升），
    #   且 cap 桶会破 ATOM + ladder FAIL ⇒ 唯一剩下的结构轴 = 分组字段去均值。
    ("U1_tech_grp", "techindi_model", dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("uu_sector", "group_neutralize(%s, sector)" % two_leg(TI_MAIN, "0.7", TI_15, "1.5")),
      ("uu_industry", "group_neutralize(%s, industry)" % two_leg(TI_MAIN, "0.7", TI_15, "1.5")),
      ("uu_subind", "group_neutralize(%s, subindustry)" % two_leg(TI_MAIN, "0.7", TI_15, "1.5"))]),
    # ===== T：techindi 走**纯幂次轴**（保 ATOM，不加 cap —— cap 会破 ATOM 且 ladder FAIL）
    # 实测 S 对幂次极不敏感：pow1.0 → 1.95、pow1.5 → 1.90（仅 −0.05）⇒ 可推很高。
    # prod：pow1.5 → **0.7276**（0.7-0.8 仅 1 颗、0.6-0.7 10 颗）⇒ 需再降 0.028。
    # 论坛 YL61874 实测 `signed_power(·,3)` 外芯 PC 0.9→0.64 且 S 基本不变 —— 与此特性吻合。
    ("T_tech_pow", "techindi_model", dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("tt_p18", two_leg(TI_MAIN, "0.7", TI_15, "1.8")),
      ("tt_p21", two_leg(TI_MAIN, "0.7", TI_15, "2.1")),
      ("tt_p26", two_leg(TI_MAIN, "0.7", TI_15, "2.6")),
      ("tt_p30", two_leg(TI_MAIN, "0.7", TI_15, "3.0")),
      ("tt_p40", two_leg(TI_MAIN, "0.7", TI_15, "4.0"))]),
    # ===== R1：把 `1YNerr2X` 的破墙公式复制到**其它数据集**（用户要 10 颗，需要多塔）=====
    # 公式 = group_neutralize(add(sig(F_main, pow2.1), 0.7×sig(F_aux, pow2.1)), bucket(rank(cap),0,1,0.05))
    # ① OTHER 塔（差 2 颗）：techindi_model，主腿 tm_16，辅腿 ten_day_15，universe CS1600
    ("R1_tech", "techindi_model", dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("rr_tech_p21", _cap20(two_leg(TI_MAIN, "0.7", TI_15, "2.1"))),
      ("rr_tech_p18", _cap20(two_leg(TI_MAIN, "0.7", TI_15, "1.8"))),
      ("rr_tech_p15", _cap20(two_leg(TI_MAIN, "0.7", TI_15, "1.5")))]),
    # ② FUND 塔第 2/3 颗：换主腿字段（不同主腿 ⇒ 不同 prod 源），同公式
    ("R2_fund_multi", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("rr_iabs_p21", _cap20(two_leg(IABS_, "0.7", F23_VBTS, "2.1"))),
      ("rr_iads_p21", _cap20(two_leg(IADS_, "0.7", F23_VBTS, "2.1"))),
      ("rr_fbds_p21", _cap20(two_leg(FBDS_, "0.7", F23_VBTS, "2.1"))),
      ("rr_sebv_p21", _cap20(two_leg(SEBV_, "0.7", F23_VBTS, "2.1")))]),
    # ===== Q：pow2.1 × cap 桶粒度（两条已证有效的轴组合，之前未试）=====
    # 依据：直方图显示 >=0.7 的对手自 pow1.0 起恒为 1 颗，prod 下降全来自 0.5-0.7 区间收缩
    #   （pow0.5: 8210+556 → pow1.0: 444+9 → pow1.5: 101+5 → pow1.8: 43+2）。
    #   故「更细的 cap 桶」应继续压这一段 ⇒ pow2.1 + cap20桶 是最强组合候选。
    ("Q1_p21c20", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("qq_p21c20", _cp2("2.1", "0.75", "0,1,0.05"))]),
    ("Q2_p21c20v07", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("qq_p21c20v07", _cp2("2.1", "0.7", "0,1,0.05"))]),
    ("Q3_p21c5", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("qq_p21c5", _cp2("2.1", "0.75", "0,1,0.2"))]),
    ("Q4_p19v065", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("qq_p19v065", _cp2("1.9", "0.65"))]),
    # ===== P：cap 桶粒度 + truncation（pow1.9 已全过 IS，S1.93/F1.07/sub1.06-1.00）
    #   memory §3 把 truncation 列为「死参数」但只在 S 上验证过，prod 轴未测 ⇒ 一并补。
    ("P1_cap5", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("pp_cap5", _cp2("1.9", "0.7", "0,1,0.2"))]),
    ("P2_cap20", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("pp_cap20", _cp2("1.9", "0.7", "0,1,0.05"))]),
    ("P3_trunc04", "fundamental23",
     dict(universe="TOP2500", decay="4", neutralization="FAST", truncation="0.04"),
     [("pp_t04", _cp2("1.9", "0.7"))]),
    # ===== V：pow 阶梯补格 + pow2.1 双胞胎（RREMNM90 的 prod 取不到值 ⇒ 改权重造新 alpha）=====
    # 已知：pow1.8 → prod 0.7054（差 0.0054）｜pow2.1 → S1.87/F1.02（prod 取不到）｜pow2.4 → F0.96 ✗
    # ⇒ 甜点在 1.8–2.1，先补 1.9 / 2.0；同时造两个 pow2.1 双胞胎（vbts 0.8 / 0.75）。
    ("V1_p19", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("vv_p19", _cp2("1.9", "0.7"))]),
    ("V2_p20", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("vv_p20", _cp2("2.0", "0.7"))]),
    ("V3_p21v08", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("vv_p21v08", _cp2("2.1", "0.8"))]),
    ("V4_p21v075", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("vv_p21v075", _cp2("2.1", "0.75"))]),
    # ===== W：pow 外推收尾。pow1.5→prod 0.7218；pow1.8→**0.7054**（只差 0.0054）。
    #   Δ = −0.0164 / 0.3 幂次 ⇒ 继续推到 2.1 / 2.4；同时试 cap 桶边界内缩。
    ("W1a_p21", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("ww_p21", _cp("2.1"))]),
    ("W2_p24", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("ww_p24", _cp("2.4"))]),
    ("W1b_v08", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("ww_p18v08", "group_neutralize(add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.8), multiply(0.8, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.8))), bucket(rank(cap), range=\"0,1,0.1\"))")]),
    # ===== Z5/Z6：把 cap 桶**换成**另一个风险维度的桶（不叠加，控 op 预算）=====
    # 依据：cap 桶把 >0.6 对手砍到 6 颗、只剩 1 颗 >0.7；剩下的那颗可能挂在动量/波动维度上。
    ("Z5_mombkt", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("zz_mom", "group_neutralize(%s, bucket(rank(ts_mean(returns, 63)), range=\"0,1,0.1\"))" % P15)]),
    ("Z6_volbkt", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("zz_vol", "group_neutralize(%s, bucket(rank(ts_std_dev(returns, 252)), range=\"0,1,0.1\"))" % P15)]),
    # ===== Z：VkxVlL0A（pow1.5+cap，S2.03/F1.16/sub PASS/FAIL 空）prod 0.7218，
    #   直方图只剩 **1 颗** production alpha >0.70（0.7218）。只差 0.022。
    #   打法：不再动幂次（F 只剩 0.16 余量），改换中性化档 / 微调辅腿权重。
    ("Z1_stat", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="STATISTICAL"),
     [("zz_p15_stat", Z15)]),
    ("Z2_subind", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="SUBINDUSTRY"),
     [("zz_p15_subind", Z15)]),
    ("Z3_ind", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="INDUSTRY"),
     [("zz_p15_ind", Z15)]),
    ("Z4_pow18", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("zz_p18", "group_neutralize(add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.8), multiply(0.7, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.8))), bucket(rank(cap), range=\"0,1,0.1\"))")]),
    # ===== Y5：按"可加模型"外推 =====
    # 实测：pow0.5→1.0 单独 Δprod −0.0335 ｜ cap 中性化单独 Δprod −0.0253 ｜ 两者完全可加（和=0.0588）。
    # ⇒ 继续抬幂次同时保 cap 中性化，预期每档再 −0.03。
    # 代价：幂次压 S（1.73→1.49→1.31），cap 中性化抬 S（+0.67）⇒ 两者正好对冲，S 仍能守在 1.9–2.0。
    ("Y5_powcap", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("z_p15_cap", _cap("1.5")), ("z_p25_cap", _cap("2.5")), ("z_p30_cap", _cap("3.0"))]),
    # ===== Y4：sub 的 0.006 缺口。Y2 证明 vbts 权重 0.7→1.3 时 ratio 恒 0.508–0.517（门槛 0.520），
    #   而纯 ofc 版 ratio 0.83 但 S 仅 1.32 ⇒ 用**小权重 ofc** 抬复合 ratio，bank+vbts 保 S。
    # ===== Y1：cap 中性化的 pow0.5 版（X7 的 group_neutralize+bucket 在 pow0.5 基座上 ERROR×3，
    #   换三种写法绕：vector_neut 2-op 版 / densify / 不同 range 字面量）=====
    ("Y1_capvar", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("y_vneut", "vector_neut(%s, rank(cap))" % A_BASE_P05)]),
    # ===== Y2：a_capneu（S2.16 / sub 1.11 vs 1.12 / prod 0.7383）补 sub =====
    #   不动结构、只调 vbts（单腿 ratio 0.724 的抬 ratio 辅腿）权重；另试 ofc（ratio 0.94）。
    ("Y2_subfix", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="FAST"),
     [("y_ac_v09", "group_neutralize(add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.0), multiply(0.9, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.0))), bucket(rank(cap), range=\"0,1,0.1\"))"),
      ("y_ac_v11", "group_neutralize(add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.0), multiply(1.1, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.0))), bucket(rank(cap), range=\"0,1,0.1\"))"),
      ("y_ac_v13", "group_neutralize(add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.0), multiply(1.3, signed_power(rank(ts_backfill(fnd23_intfvalld1_vbts, 22)), 1.0))), bucket(rank(cap), range=\"0,1,0.1\"))"),
      ("y_ac_ofc", "group_neutralize(add(signed_power(rank(ts_backfill(bank_assets_investment, 22)), 1.0), multiply(0.9, signed_power(rank(ts_backfill(fnd23_ofc, 22)), 1.0))), bucket(rank(cap), range=\"0,1,0.1\"))")]),
    # ===== Y3：B 型（techindi, prod 0.7481, mean 0.005 单点同源）只走结构轴（OTHER 不能碰 PV）=====
    ("Y3_bstruct", "techindi_model", dict(universe="TOPCS1600", decay="4", neutralization="FAST"),
     [("y_b_hump", "hump(%s, hump=0.01)" % two_leg(TI_MAIN, "1.0", TI_15, "1.0")),
      ("y_b_gate", "trade_when(group_count(%s, industry) > 50, %s, 0)"
       % (two_leg(TI_MAIN, "1.0", TI_15, "1.0"), two_leg(TI_MAIN, "1.0", TI_15, "1.0"))),
      ("y_b_p15", two_leg(TI_MAIN, "1.0", TI_15, "1.5"))]),
    # ===== X7：cap 中性化的**干净 A/B** =====
    # X2 的 a_capneu 用了 pow1.0 基座（S1.49），与 mLowboV5（pow0.5, S1.73）两变量同改。
    # 结果 prod 0.7971 → 0.7383，且 0.7-0.8 对手 15 → 1、0.6-0.7 从 556 → 9 ⇒ **尾部被削平**。
    # 本批在 pow0.5 基座上单独加 cap 中性化 ⇒ 干净隔离；顺带试更细的 20 桶。
    ("X3_u800", "fundamental23", dict(universe="TOP800", decay="4", neutralization="FAST"),
     [("u800_base", A_BASE_P05)]),
    ("X4_u1200", "fundamental23", dict(universe="TOP1200", decay="4", neutralization="FAST"),
     [("u1200_base", A_BASE_P05)]),
    ("X5_none", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="NONE"),
     [("none_base", A_BASE_P05)]),
    ("X6_crowd", "fundamental23", dict(universe="TOP2500", decay="4", neutralization="CROWDING"),
     [("crowd_base", A_BASE_P05)]),
]


def log(m):
    print(m, flush=True)


def submit(path, st):
    cmd = [PY, SUBMIT, "--path", path, "--region", st["region"],
           "--universe", st["universe"], "--delay", st["delay"], "--decay", st["decay"],
           "--neutralization", st["neutralization"], "--truncation", st["truncation"],
           "--nan-handling", st["nan_handling"], "--max-trade", st["max_trade"],
           "--simulation-mode", st["mode"]]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=ROOT)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
    except Exception as ex:
        log("  [submit] 异常 %s" % ex); return None
    m = re.search(r"/simulations/([A-Za-z0-9]+)", out)
    if not m:
        log("  [submit] 失败 %s" % out.strip().splitlines()[-3:]); return None
    return m.group(1)


def wait(sid, rounds=120, gap=15):
    from brain_api import brain_client
    for _ in range(rounds):
        try:
            j = brain_client.session.get("%s/simulations/%s" % (brain_client.base_url, sid),
                                         timeout=30).json()
        except Exception:
            time.sleep(gap); continue
        kids = j.get("children") or []
        if not kids:
            if j.get("status") == "COMPLETE":
                return True
            if j.get("status") in ("ERROR", "FAIL", "CANCELLED"):
                return False
            time.sleep(gap); continue
        sts = []
        for k in kids:
            try:
                kk = brain_client.session.get("%s/simulations/%s" % (brain_client.base_url, k),
                                              timeout=30).json()
                sts.append((kk or {}).get("status"))
            except Exception:
                sts.append(None)
        if all(x in ("COMPLETE", "ERROR", "FAIL", "CANCELLED") for x in sts):
            return True
        time.sleep(gap)
    return False


def read(aid):
    from brain_api import brain_client
    try:
        j = brain_client.session.get("%s/alphas/%s" % (brain_client.base_url, aid), timeout=30).json()
    except Exception:
        return {}
    i = j.get("is") or {}
    out = dict(S=i.get("sharpe"), F=i.get("fitness"), TO=i.get("turnover"),
               ret=i.get("returns"), margin=i.get("margin"))
    for c in (i.get("checks") or []):
        n = c.get("name")
        if n == "LOW_2Y_SHARPE": out["Y2"] = c.get("value")
        elif n == "LOW_SUB_UNIVERSE_SHARPE":
            out["sub"] = c.get("value"); out["sub_limit"] = c.get("limit")
        elif n == "LOW_ROBUST_UNIVERSE_SHARPE": out["rob"] = c.get("value")
        elif n == "IS_LADDER_SHARPE": out["ladder"] = c.get("value"); out["ladder_lim"] = c.get("limit")
    out["fails"] = [c.get("name") for c in (i.get("checks") or []) if c.get("result") == "FAIL"]
    return out


def ids_of(sid, ds):
    try:
        out = subprocess.run([PY, HARVEST, sid, ds, "camp"], capture_output=True,
                             text=True, timeout=600, cwd=ROOT).stdout
    except Exception:
        return []
    return [m.group(1) for m in (re.match(r"\s*\+\s+(\w+)\s+S=", ln) for ln in out.splitlines()) if m]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--dump", action="store_true", help="导出全部表达式供 preflight 校验")
    a = ap.parse_args()
    if a.dump:
        ex = [e for _, _, _, lst in PLAN for _, e in lst]
        json.dump(ex, open(os.path.join(ROOT, "cache", "_prodbreak_exprs.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1)
        log("导出 %d 条 -> cache/_prodbreak_exprs.json" % len(ex))
        return
    if a.dry_run:
        for tag, ds, ov, ex in PLAN:
            log("%-14s %-16s n=%d  %s" % (tag, ds, len(ex), ov))
            for n, e in ex:
                log("   %-10s %s" % (n, e))
        return

    ck = json.load(open(CK, encoding="utf-8")) if os.path.isfile(CK) else {"done": [], "results": []}
    done = set(ck["done"])
    from brain_api import brain_client
    asyncio.run(brain_client.ensure_authenticated())

    for tag, ds, ov, ex in PLAN:
        if tag in done:
            log("### %s 已完成，跳过" % tag); continue
        st = dict(COMMON); st.update(ov)
        fn = os.path.join(ROOT, "cache", "_prodbreak_%s.txt" % tag)
        open(fn, "w", encoding="utf-8").write("\n".join(e for _, e in ex) + "\n")
        sid = None
        for t in range(3):
            sid = submit(fn, st)
            if sid:
                break
            log("  [retry] %s 第 %d 次失败，等 30s" % (tag, t + 1)); time.sleep(30)
        if not sid:
            log("### %s 三次均失败" % tag); continue
        log("### %s n=%d sim=%s" % (tag, len(ex), sid))
        if not wait(sid):
            log("  [warn] %s 未到终态" % tag); continue
        aids = ids_of(sid, ds)
        log("    收割 %d/%d" % (len(aids), len(ex)))
        if not aids:
            log("  [warn] 空收割 —— 查 sim 是否整批 ERROR"); continue
        for i, aid in enumerate(aids):
            d = read(aid)
            nm = ex[i][0] if i < len(ex) else "?"
            ck["results"].append(dict(tag=tag, dataset=ds, variant=nm, alpha=aid, over=ov, **d))
        ck["done"].append(tag)
        for p, obj in ((CK, ck), (LEDGER, ck["results"])):
            tmp = p + ".tmp"
            json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            os.replace(tmp, p)
        time.sleep(3)

    log("\n=== 破 prod 对照实验 ===")
    log("%-12s %-10s %6s %6s %7s %7s %7s %6s %s" % (
        "批", "变体", "S", "F", "2Y", "sub", "lim", "TO", "FAIL"))
    for r in sorted(ck["results"], key=lambda x: -(x.get("S") or -9)):
        log("%-12s %-10s %6.2f %6.2f %7s %7s %7s %6s %s" % (
            r.get("tag"), r.get("variant"), r.get("S") or 0, r.get("F") or 0,
            r.get("Y2"), r.get("sub"), r.get("sub_limit"),
            round((r.get("TO") or 0) * 100, 1),
            ",".join(x.replace("LOW_", "").replace("_UNIVERSE_SHARPE", "") for x in (r.get("fails") or [])) or "无"))


if __name__ == "__main__":
    main()
