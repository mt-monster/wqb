# -*- coding: utf-8 -*-
"""模板族架构与表达式构造：L1 提取 × L2 归一交叉采样 + 载体扩散 + 后处理电池。"""
import os
import sys
import json
import re
import asyncio
import sqlite3
import subprocess
import collections
import time
from datetime import datetime

from .config import *            # noqa: F401,F403
from .config import _WQB_SCRIPTS_DIR  # noqa: F401

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from campaign_semantics import (  # noqa: E402,F401
    LIT_THRESHOLD, VIRGIN_AC, VIRGIN_VS, VIRGIN_MIN_COV, VIRGIN_COV_FLOOR,
    is_virgin, all_datasets, exposure_profile,
    NAME_META, is_name_metadata, classify_desc,
    FORM_FAMILIES, GATED_CATS, GATE_Q, POSTPROC_Q, PER_DIM, MIN_FIELDS_TOTAL,
    FULL_FIELD_CAP, BLACKBOX_FAMILIES, field_tier,
    FAMILY_EXPOSURE, EXPOSURE_VOCAB, EXPR_EXPOSURE, field_exposure_hint,
    CONCEPT_FAMILIES, CONCEPT_ZH, field_concepts, concept_families,
    PP_VOCAB, parse_preprocessing, load_s1_preprocessing, apply_preprocessing,
    _DESC_NOISE, clean_desc, _load_form_overrides, _load_llm_tags, LLM_CONF_MIN,
    FORM_EVIDENCE, field_form, print_form_audit,
)


# ---------------- 分层模板架构（2026-10-21 修复）----------------
# 修复：旧 8 族把 L1（信号提取）× L2（归一化）焊死（cs=zscore+power、rk=rank 不交叉），
# 且缺 L4（截面处理）层。现拆层：L1×L2 交叉采样为 12 族；L4 由阶段 2 后处理电池接管。
L1_EXTRACT = {
    "lvl": "ts_backfill({F}, {BF})",                                   # 水平
    "d1": "ts_delta(ts_backfill({F}, {BF}), {W1})",                     # 一阶差分
    "d2": "ts_delta(ts_delta(ts_backfill({F}, {BF}), {W1}), {W1})",     # 二阶差分
    "ed": "ts_decay_linear(ts_backfill({F}, 252), 63)",                 # 事件衰减
    "ir": "ts_ir(ts_backfill({F}, {BF}), {ZW})",                        # 信噪比
    "dsp": "ts_backfill(vec_stddev({FR}), {BF})",                       # 组内离散度（仅 VECTOR）
}
L2_NORM = {
    "rk": "rank({X})",
    "zs": "ts_zscore({X}, {ZW})",
    "qt": "ts_quantile({X}, {ZW})",
    "tr": "ts_rank({X}, {ZW})",
    "sc": "ts_scale({X}, {ZW})",
    # 2026-10-24 补：**截面**分位归一化（原矩阵只有时序 ts_quantile，缺截面版）。
    # 用户指出 + GEM 实证（EUR 3515 条里 quantile 使用率 3%）。
    # 对 discrete_rating（字段本身即百分位秩）语义匹配：截面重归一而非时序分位。
    "qc": "quantile({X})",
}
# 组合表（标定实证筛选）：(L1, L2)；va=波动调整特例；dw=L3 特殊结构
FAMILIES = [
    ("lvl", "rk"), ("lvl", "zs"), ("lvl", "qt"), ("lvl", "tr"), ("lvl", "sc"),
    ("d1", "rk"), ("d1", "va"),
    ("d2", "rk"),
    ("ed", "rk"),
    ("ir", None),
    ("dsp", "rk"),
    ("lvl", "qc"), ("d2", "qc"),
]

# ---------------- 零收益族退役（2026-10-27 P1-5；A/B #6 后收窄到只退役差分几何）----------------
# 第一版按 reports/ind_campaign_template_eval_20261026.md §6（20 集 · decay 4 旧几何）退役了
#   dw / ed_rk / d2_* / ir_pl / tl 五族，理由都是「0 命中 ≥1.0」。
# A/B #6（fnd86 · decay 10 · 3 字段 × 4 族，见报告 §11）把其中两条证伪：
#   ed_rk → S 1.48 / **2.91** / 1.31（average_score 那颗 2.91 只卡 robust，id 1YNkd1Xm）
#   dw    → S 1.10 / **2.48** / 0.82
#   ⇒ **level 几何的旧 decay-4 结论不可泛化到 decay 10**，两族一律恢复（连同 dw 回 BLACKBOX_FAMILIES）。
# 最终只退役差分几何：d2_rk / d2_qc 在 decay 10 下 6/6 <1.0（0.32/0.28/−0.17 与 0.43/0.35/−0.09），
#   与 §6 的 decay-4 结论同向 ⇒ 差分臂的零收益结论站得住。
# ir_pl / tl 未做 decay-10 复核，按「未证伪即保留」处理（结构面窄：ir_pl 只在 _force_full / other
#   形态出现；tl 只在 GATED_CATS 且已被 pp 覆盖）—— 不额外烧配额去证伪一个窄结构。
# 退役只作用于**默认笛卡尔积**，不是删除结构；FAMILIES 仍保留全集作审计分母
#   （sweep / pipeline `_all_tpl` 不受影响）。回退：WQB_LEGACY_FAMILIES=1 ⇒ 旧全量笛卡尔积
#   （模块级常量，长驻进程不热加载）。
RETIRED_FAMILIES = {
    "d2_rk": (),                    # 二阶差分在 IND 无收益（decay 10 复核 3/3 <1.0，max 0.43）
    "d2_qc": (),                    # 同上（decay 10 复核 3/3 <1.0，max 0.35）
}
LEGACY_FAMILIES = bool(os.environ.get("WQB_LEGACY_FAMILIES"))


def _family_enabled(fam, form):
    """族在该字段形态下是否允许产出。LEGACY 开关 ⇒ 全量回退旧笛卡尔积。"""
    if LEGACY_FAMILIES:
        return True
    allowed = RETIRED_FAMILIES.get(fam)
    return True if allowed is None else (form in allowed)


def _enabled_family_count(form):
    """某形态下「全交叉」会产出的族数（含 dw）—— 35% 安全阀的分母。"""
    n = sum(1 for l1, l2 in FAMILIES if _family_enabled(f"{l1}_{l2 or 'pl'}", form))
    return n + (1 if _family_enabled("dw", form) else 0)


_L1_LAYER = {"lvl": "lvl", "d1": "diff", "d2": "diff", "ed": "event", "ir": "level_ratio",
             "dsp": "disp"}


def ensure_l1_coverage(allow):
    """保证模板族并集覆盖 L1 的「水平」与「差分」两类；缺层则补（L2 用 rk，最便宜）。"""
    if not allow:
        return allow
    layers = {_L1_LAYER.get(f.split("_")[0]) for f in allow}
    out = set(allow)
    if "lvl" not in layers:
        out.add("lvl_rk")
    if "diff" not in layers:
        out.add("d1_rk")
    return out


# ---------------- 负向强信号镜像白名单（P0-2，2026-10-27）----------------
# 依据 reports/ind_campaign_template_eval_20261026.md §3.3：只有**奇对称**结构才谈得上
# 「反向信号」——`rank` / `ts_zscore` / `ts_rank` / `ts_quantile` / `ts_scale` / `quantile` /
# `ts_delta` / `dev + group_rank` / `signed_power(·, 奇数)`。命中白名单的族，把整条表达式
# 取反（`multiply(-1, code)`）后 S/F/2Y/sub/rob 精确取负、TO/CW 不变。
# ⚠ 排除清单（每条都有结构理由，不是嫌麻烦）：
#   `dw`         = 两个 rank 的**乘积**（偶）⇒ 取反内层不是同一个信号的反向
#   `pp`         = `if_else(greater(rank(dw), q), dw, 0)`：门控在取反后选的是另一批股票
#   `tl`         = tail 门控，同理
#   `dsp_rk`     = `vec_stddev` 非负（离散度没有「负值」）
#   `rg_lvvol*`  = `multiply(F, add(ts_std_dev(F,65),1))`：std 是偶函数，整式非奇对称
#   `res/reslag` = 含 PV `returns` 回归残差，**非 ATOM**（用户口径），且残差项本身不是奇函数
# 白名单只决定「值不值得派一条镜像批」；`mirror.py` 另有 ATOM 平台判据与换手记录。
MIRROR_TPL = (
    "lvl_rk", "lvl_zs", "lvl_qt", "lvl_tr", "lvl_sc", "lvl_qc",
    "d1_rk", "d1_va", "d2_rk", "d2_qc",
    "ed_rk", "ir_pl",
    "rg_rkz", "rg_grz", "rg_grz_ind", "rg_grz_p3",
    "rg_rkdev", "rg_grdev", "rg_grdev_ind",
    "rg_grdev_p3", "rg_grdev_p3_sec",
)


def is_mirror_tpl(tpl):
    """该模板族是否允许镜像（先剥派发后缀：`_cx` / `_f` / `_rp` / `_r`）。"""
    from .bad_tokens import norm_tpl
    return norm_tpl(tpl or "") in MIRROR_TPL


# ★★★★★ 2026-10-25：`ts_backfill` **不能用于事件型字段**（平台报
#   `Operator ts_backfill does not support event inputs`，整批 FAIL）。
#   KOR 的 news 系集全是事件流，导致首个集就连着 FAIL；EUR 也有 3 个 SIM_FAIL 同源。
#   开关：WQB_NO_BACKFILL=1 ⇒ 把 L1 模板里的 ts_backfill 全部剥掉（保留其余结构）。
#   为什么不在报错后自动拉黑算子：算子本身合法，是**输入类型**不兼容，
#   拉黑会误伤全库（EUR 已踩过，见 bad_tokens.PROTECTED_TOKENS）。
if os.environ.get("WQB_NO_BACKFILL"):
    L1_EXTRACT = {_k: _v.replace("ts_backfill({F}, {BF})", "{F}")
                      .replace("ts_backfill({F}, 252)", "{F}")
                      .replace("ts_backfill(vec_stddev({FR}), {BF})", "vec_stddev({FR})")
                  for _k, _v in L1_EXTRACT.items()}
    _orig_dw = None

DW_TPL = "multiply(rank(ts_mean(ts_backfill({F}, {BF}), {WS})), rank(ts_mean(ts_backfill({F}, {BF}), {WL})))"
if os.environ.get("WQB_NO_BACKFILL"):
    DW_TPL = DW_TPL.replace("ts_backfill({F}, {BF})", "{F}")
VA_TPL = "divide(ts_delta(ts_backfill({F}, {BF}), {W1}), add(ts_std_dev(ts_backfill({F}, {BF}), {ZW}), 0.0001))"


# ---------------- 残差化族（2026-10-25 接入）----------------
# IND 唯一被证实能过 prod 墙的配方（docs/reference/IND/institutions6_field_profile.md §2.1）：
#   rank(-ts_regression(ts_zscore(returns, W), ts_zscore(F, W), W, rettype=0))，W=252；decay=126
# wave232 实测该结构 10/10 RA 全过（E5VNe67L S3.20 / KPmvEYeE S3.07 / vRO9nG3w S2.90）。
# 增强轴（同文件 §2.3，均 RA failed=0）：字段滞后 21 天 2.98→3.10；W=252 最强（63 明显偏弱）。
# 合规：locked.py `mixed_signal_ban` 明确允许「第二个数据集只以条件 / 分组 / 残差入场」。
# ⚠ 窗口 21 不在 STANDARD_WINDOWS，按「带实测证据的例外」使用（§2.3 数据即证据）。
# ⚠ 该族必须用 decay=RESIDUAL_DECAY 派发：IND 基础 decay=4 复现不了实测结果
#   （wave232 的 10 颗全部 decay=126）⇒ 由 pipeline 单独一批派发，不混进主派发。
RESIDUAL_TPL = {
    "res": "rank(-ts_regression(ts_zscore(returns, 252), ts_zscore({X}, 252), 252, rettype=0))",
    "reslag": ("rank(-ts_regression(ts_zscore(returns, 252), "
               "ts_zscore(ts_delay({X}, 21), 252), 252, rettype=0))"),
}
RESIDUAL_DECAY = 126

# ★★★★★ 2026-10-26：用户口径「IND 优先挖掘 ATOM」。
#   ATOM = **单数据集形态**（只用本数据集字段）。残差族把 PV 的 `returns` 当回归自变量，
#   属跨数据集腿（组腿/残差），不算 ATOM —— 用户原话「kqJweZQz 不算吧，用了PV的returns」。
#   开关：WQB_ATOM_ONLY=1 ⇒ build_residual 返回空 ⇒ pipeline 的 `[res]` 段整段跳过，
#   只派发 FAMILIES 的单字段形态。缺省（未设置）= 旧行为，保留残差族。
#   ⚠ 默认关而非默认开：残差族是 IND 唯一被证实能过 prod 墙的配方（三颗 prod<0.7 的实证），
#   关它等于放弃一条已验证通路；是否只用 ATOM 由调用方按波次口径显式决定。
ATOM_ONLY = bool(os.environ.get("WQB_ATOM_ONLY"))


def build_residual(sel, cat=None):
    """残差化族：returns 对字段（reslag 变体再滞后 21 天）回归取残差后取反。

    只给非探针、非 skip、非 returns 自身的字段（探针层遵守 1 条/字段成本纪律）。
    VECTOR 字段先用 wrap() 聚合成截面量；矩阵字段原样进 ts_zscore。
    WQB_ATOM_ONLY=1 时整族跳过（该族含 PV 的 returns，不属 ATOM）。
    """
    if ATOM_ONLY:
        print("  [res] WQB_ATOM_ONLY=1 ⇒ 跳过残差化族（含 PV returns，属组腿非 ATOM）")
        return []
    out = []
    for r in sel:
        if r.get("tier") == "probe" or r.get("form") == "skip":
            continue
        if r["field_name"] == "returns":
            continue                       # returns 对自身回归退化
        X = wrap(r)
        _hint = field_exposure_hint(r, cat)
        for tpl, tmpl in RESIDUAL_TPL.items():
            e = tmpl.format(X=X)
            out.append((tpl, e))
            EXPR_EXPOSURE[e] = _hint if _hint != "value" else FAMILY_EXPOSURE.get(tpl, "other")
    return out


# ---------------- robust 几何族（2026-10-26 接入）----------------
# 起因：IND 的 ATOM 候选全灭于 LOW_ROBUST_UNIVERSE_SHARPE（限值固定 1.0），
#   而旧模板库 13 族全是 L2_NORM(L1_EXTRACT(F)) 的**单调归一**链，一个 group 算子都没有，
#   且季/年报频率表把 backfill 钉在 252 ⇒ 结构性拿不到 robust。
# 实证（2026-10-26 平台实测，全部 ATOM effective=1，IND/TOP500/D1）：
#   rank(ts_zscore(ts_backfill(F,22),252)) decay=4  → robust 0.87 ✗
#   同式 decay=**10**                              → robust **1.02 ✓**（S1.61 F1.13 2Y2.96 sub1.26）
#   group_rank(ts_zscore(ts_backfill(F,22),252), sector) decay=10 → robust **1.01 ✓**（prod 0.7672 ✗）
#   rank(归一化趋势偏离) decay=10                   → robust **1.05 ✓** prod **0.6709 ✓**（S1.51 差 0.07）
# 三个杠杆与 fnd86 史册一致：短 bf(22) / group_rank(·, sector) / 连续量上凸变换。
# ⚠ decay 按结构分档（见下方 ROBUST_DECAY_BY_TPL / robust_decay()）：pipeline 按 decay 分组
#   单独派发（主派发是区域缺省 decay=4），见 stage 1.6。经载体扩散（carrier_expand）复用本族时
#   同样必须带 robust_decay(tpl)。
ROBUST_TPL = ("rg_rkz", "rg_grz", "rg_grz_ind", "rg_grz_p3",
              "rg_rkdev", "rg_grdev", "rg_grdev_ind",
              "rg_grdev_p3", "rg_grdev_p3_sec", "rg_lvvol", "rg_lvvol_sec")
RG_BF = 22          # 短 backfill（实证：< 季报发布间隔才拿得到新信息）
RG_ZW = 252         # 固定 z 窗口（不跟频率表走：季/年表会把 252 推到 504，实测 504 → robust 0.84 ✗）
# 波动缩放的水平项：x = ts_backfill(F * (1 + ts_std_dev(F, 65)), 22) 再平滑 RG_LV_SMOOTH 天。
# 实证（fnd86_earnings_score，IND/TOP500/D1/STATISTICAL）：
#   group_rank(ts_mean(x,2), sector) decay2 → S2.14 F1.70 2Y1.99 robust 1.02 ✓（成品 gJWnrZgg）
#   rank(ts_mean(x,5))               decay4 → S2.18 F1.75 2Y2.03 robust 1.06 ✓（CW WARNING）
#   group_rank(ts_mean(x,5),sector)  decay4 → S2.10 F1.65 2Y1.97 robust 0.99（CW PASS、prod 0.6989）
#   ⇒ 这是「水平类」字段唯一把 S 做到 2.0+ 的形状；平滑 2 + decay 2 才是全闸过的那个档。
RG_LV_STD = 65
# ★ 2026-10-26 修正：平滑档实测是 **2**，不是 5。IND 全闸 ATOM 成品 gJWnrZgg 的逐字 code 是
#   `group_rank(ts_mean(ts_backfill(multiply(F, add(ts_std_dev(F,65),1)),22), 2), sector)`，
#   decay=2 ⇒ S2.14/F1.70/2Y1.99/sub0.93/rob1.02（全闸过）。旧值 5 来自另一条 fnd86 探针，
#   在本电池里复现不出任何已提交/已过闸成品 ⇒ 按区域定档，env 可覆写。


def default_lv_smooth(region):
    """波动缩放项的平滑档：IND 实测 2（成品 gJWnrZgg）；其余区域沿用历史 5。"""
    return 2 if (region or "").upper() == "IND" else 5


try:
    RG_LV_SMOOTH = int(os.environ.get("WQB_RG_LV_SMOOTH") or default_lv_smooth(REGION))
except ValueError:
    RG_LV_SMOOTH = default_lv_smooth(REGION)
try:
    ROBUST_DECAY = int(os.environ.get("WQB_ROBUST_DECAY") or 10)
except ValueError:
    ROBUST_DECAY = 10
# ★ 2026-10-26：decay **不是全局常数**，按结构分档（逐颗平台实测，全部 ATOM/IND/TOP500/D1）：
#   z / rank / dev 三个非凸族 → 10（rg_rkz rob1.02、rg_grz rob1.01、rg_rkdev rob1.05）
#   居中凸族 rg_grdev_p3*    → 6（成品 58jPrvZ1：S1.64/F1.27/2Y2.23/sub1.55/rob1.12）
#   波动缩放水平族 rg_lvvol* → 2（成品 gJWnrZgg：S2.14/F1.70/2Y1.99/rob1.02）
# ⚠ 旧实现全局 10 ⇒ 凸族与 lvvol 族跑的是「未验证设置」，成品结构在电池里复现不出来。
#   分档**不增加批数**：dispatch 本就按模板分批，同 decay 的族仍合并成同批。
ROBUST_DECAY_BY_TPL = {
    "rg_grdev_p3": 6,
    "rg_grdev_p3_sec": 6,
    "rg_lvvol": 2,
    "rg_lvvol_sec": 2,
}


def robust_decay(tpl):
    """模板的实测 decay 档（剥 `_neg`/`_cx`/`_f`/`_rp` 后缀后查表）；未登记回落 ROBUST_DECAY。"""
    t = tpl or ""
    for suf in ("_neg", "_cx", "_f", "_rp"):
        if t.endswith(suf) and len(t) > len(suf):
            t = t[:-len(suf)]
            break
    return ROBUST_DECAY_BY_TPL.get(t, ROBUST_DECAY)
_rg_env = (os.environ.get("WQB_ROBUST_GEOM") or "").strip().lower()
if _rg_env in ("0", "false", "off", "no"):
    ROBUST_GEOM = False
elif _rg_env in ("1", "true", "on", "yes"):
    ROBUST_GEOM = True
else:
    ROBUST_GEOM = (REGION == "IND")     # 缺省：该族就是为 IND 的 robust 墙加的

# 探针层的 robust 探针（2026-10-26，reports/ind_campaign_template_eval_20261026.md §5）。
# 只跑 1 条**已验证 ATOM 安全**的结构：纯本数据集字段 + `sector` 分组，无跨集腿；
# `rg_grdev_p3_sec` 是 analyst_consensus decay6 全闸成品 58jPrvZ1 的逐字结构。
# 成本：探针字段 ≤12 ⇒ 12 条 = 2 批（对比现状 12 条 lvl_rk 也是 2 批 ⇒ **净 +2 批/集**）。
ROBUST_PROBE_TPL = ("rg_grdev_p3_sec",)
_pr_env = (os.environ.get("WQB_ROBUST_PROBE") or "").strip().lower()
if _pr_env in ("0", "false", "off", "no"):
    ROBUST_PROBE = False
elif _pr_env in ("1", "true", "on", "yes"):
    ROBUST_PROBE = True
else:
    ROBUST_PROBE = (REGION == "IND")
# VECTOR 字段默认剥 ts_backfill（平台报 event inputs 不支持，会连坐整批）；
# 实测可安全 backfill 的 VECTOR 数据集用本清单开除（逗号分隔数据集名）。
# ★ 2026-10-26：缺省纳入 `analyst_consensus` —— 全闸 ATOM 成品 58jPrvZ1 的逐字 code 就是
#   `ts_backfill(vec_avg(mean_flash_estimate_ebt_annual12), 22)`（S1.64/F1.27/2Y2.23/sub1.55/
#   rob1.12，checks.fail=[]）⇒ 该集 VECTOR 字段**确实**支持 backfill。旧缺省为空 ⇒ 一律剥掉，
#   成品结构在电池里复现不出来。
RG_BACKFILL_DS = {s.strip() for s in
                  (os.environ.get("WQB_RG_BACKFILL_DS")
                   or "analyst_consensus").split(",") if s.strip()}

# 后处理电池的幂次：0.7（凹）是历史缺省，但 fnd86 史册里实证有效方向是**凸**（≥1.5：
#   signed_power(·,3) 把 robust 从 0.9x 抬到 1.00）。凹变换压尾、凸变换放大极端值，
#   在「截面相对强弱」而非「时序连续 z」上跑 robust 时后者才有增益 ⇒ IND 缺省改凸。
try:
    PP_POW = float(os.environ.get("WQB_PP_POW") or ("3" if REGION == "IND" else "0.7"))
except ValueError:
    PP_POW = 3.0 if REGION == "IND" else 0.7


def _robust_expr(tpl, r, ds=None):
    """robust 几何族单体构造。调用点 ≤10（复杂度纪律；两个居中凸模板例外 12，见下）。

    平台侧 REGULAR 无算子数硬上限（只有 PPA 有 ≤8），故 12 调用点的成品仍可 FULL 仿真；
    战役 wave_gate 的闸1b-2「<10」只作用于走 wave_gate 的候选，rg 批由 dispatch 直发。
    """
    if tpl not in ROBUST_TPL:
        return None
    F = wrap(r)
    x = f"ts_backfill({F}, {RG_BF})"
    z = f"ts_zscore({x}, {RG_ZW})"
    # 归一化趋势偏离：除以 |ts_mean| 而非 std ⇒ 保留「水平高低」信息，
    # 这是 ATOM 里唯一把 prod 从 0.7672 压到 0.6709 的概念（z-only 同族 prod 0.7672）
    _m = f"ts_mean({x}, {RG_ZW})"
    dev = f"divide(subtract({x}, {_m}), add(abs({_m}), 1))"
    # 波动缩放水平项（VECTOR 默认不带 backfill，见下方 strip 约定）
    _nobf = bool(os.environ.get("WQB_NO_BACKFILL") or (
        r.get("field_type") == "VECTOR" and (ds or "") not in RG_BACKFILL_DS))
    _lvraw = f"multiply({F}, add(ts_std_dev({F}, {RG_LV_STD}), 1))"
    lv = f"ts_mean({_lvraw}, {RG_LV_SMOOTH})" if _nobf else \
        f"ts_mean(ts_backfill({_lvraw}, {RG_BF}), {RG_LV_SMOOTH})"
    body = {
        "rg_rkz": f"rank({z})",
        "rg_grz": f"group_rank({z}, sector)",
        "rg_grz_ind": f"group_rank({z}, industry)",
        "rg_grz_p3": f"signed_power(group_rank({z}, sector), 3)",
        "rg_rkdev": f"rank({dev})",
        "rg_grdev": f"group_rank({dev}, sector)",
        "rg_grdev_ind": f"group_rank({dev}, industry)",
        # 居中后再取凸幂：rank∈[0,1] 不居中时 signed_power 只是压前半段，
        # 居中到 [-0.5,0.5] 才真正「放大两端、压掉中间」，这是 analyst 族实证
        # S1.49→1.53 / robust 0.86→1.22 的那一步（旧 rg_grz_p3 是不居中的 z 版）。
        "rg_grdev_p3": f"signed_power(subtract(group_rank({dev}, industry), 0.5), 3)",
        # sector 轴版：同几何只把分组轴粗一档（industry→sector）。IND analyst_consensus
        # decay6 同批实测 S1.56→**1.64**、rob1.19→**1.12**、sub1.49→**1.55**、2Y1.85→**2.23**、
        # prod0.5354（成品 58jPrvZ1，全闸 pass）⇒ 粗轴同时抬强度并留足 prod 余量。
        "rg_grdev_p3_sec": f"signed_power(subtract(group_rank({dev}, sector), 0.5), 3)",
        "rg_lvvol": f"rank({lv})",
        "rg_lvvol_sec": f"group_rank({lv}, sector)",
    }[tpl]
    if _nobf:
        body = strip_backfill(body, F=F, FR=r["field_name"], BF=RG_BF)
    return body


def build_robust_geom(sel, ds=None, cat=None):
    """robust 几何族：全字段 × len(ROBUST_TPL) 结构，由 pipeline 按 robust_decay(tpl) 分组派发。

    ATOM 自洽：全部只用本数据集字段 + 允许的分组字段（sector / industry），无跨数据集腿。
    form=skip（元数据）一律排除。

    探针层（`tier=probe`）：2026-10-26 起默认只跑 `ROBUST_PROBE_TPL`（1 条/字段，+1 条成本），
    由 `WQB_ROBUST_PROBE` 控制（缺省 IND=ON、其他区域 OFF）。依据见
    `reports/ind_campaign_template_eval_20261026.md` §5：
    探针原用的 `lvl_rk` 是全库信息量最低的族（231 行、中位 S 0.00、仅 2 行 ≥1.58），
    而 IND 的闸门问的是「稳健几何下有没有方向」——sentiment21 全电池 best 1.12(lvl_rk)
    被判 DEAD，同字段手工反向 dev 却 S1.80/rob1.38 ⇒ 探针的 DEAD 不能当判死证据。
    """
    if not ROBUST_GEOM:
        return []
    out = []
    for r in sel:
        if r.get("form") == "skip":
            continue
        _is_probe = (r.get("tier") == "probe")
        if _is_probe and not ROBUST_PROBE:
            continue
        _hint = field_exposure_hint(r, cat)
        for tpl in (ROBUST_PROBE_TPL if _is_probe else ROBUST_TPL):
            e = _robust_expr(tpl, r, ds)
            if not e:
                continue
            out.append((tpl, e))
            EXPR_EXPOSURE[e] = _hint if _hint != "value" else FAMILY_EXPOSURE.get(tpl, "other")
    return out


FREQ_WIN = {  # backfill, short, long, zwindow, delta_win
    "daily":   (22, 5, 66, 126, 22),
    "weekly":  (66, 21, 126, 252, 21),
    "monthly": (66, 21, 126, 252, 21),
    "quarterly": (252, 63, 252, 504, 63),
    "semi-annual": (252, 126, 504, 504, 126),
    "annual":  (252, 126, 504, 504, 126),
    "unknown": (66, 21, 126, 252, 21),
}

DS_FREQ = {  # 从数据集画像推断
    "intraday_pv_feats": "daily", "pv1": "daily", "pv20": "daily", "pv13": "weekly",
    "pv87": "daily", "risk60": "daily", "risk68": "daily",
    "news17": "monthly", "news20": "monthly",
}


PROBE_FIELD_CAP = 12   # 探针层字段上限（每个只跑 1 条 lvl_rk）


def strip_backfill(code, F, FR, BF):
    """VECTOR / 事件型字段兼容改写：剥掉 ts_backfill，保留其余结构。

    2026-10-25 IND option1 实测：平台报
      `Operator ts_backfill does not support event inputs`
    且该 multisim 10 个子任务**全部 ERROR/CANCELLED（连坐）**。
    option1 全是 VECTOR 字段 ⇒ 对 VECTOR 字段改写成无 backfill 版本；
    矩阵字段行为不变（EUR 依赖 backfill 补稀疏，不能全局关，见 WQB_NO_BACKFILL）。
    """
    if not code or "ts_backfill" not in code:
        return code
    for _a in {F, FR}:
        code = code.replace(f"ts_backfill({_a}, {BF})", _a)
        code = code.replace(f"ts_backfill({_a}, 252)", _a)
    # dsp 模板的载体是 vec_stddev(FR)，不是 wrap(r) ⇒ 单独剥一次
    code = code.replace(f"ts_backfill(vec_stddev({FR}), {BF})", f"vec_stddev({FR})")
    code = code.replace(f"ts_backfill(vec_stddev({FR}), 252)", f"vec_stddev({FR})")
    return code


def build_one_family(tpl, r, freq, ds=None):
    """把指定族的结构套在某个字段上（载体扩散用）。"""
    if tpl in ROBUST_TPL:
        # robust 几何族：bf/zw/decay 全部固定，不吃 freq 窗口表 ⇒ 派发方负责带 robust_decay(tpl)
        return _robust_expr(tpl, r, ds)
    BF, WS, WL, ZW, W1 = FREQ_WIN.get(freq, FREQ_WIN["unknown"])
    F, FR = wrap(r), r["field_name"]

    def _fin(x):
        return strip_backfill(x, F=F, FR=FR, BF=BF) if r.get("field_type") == "VECTOR" else x

    if tpl in RESIDUAL_TPL:
        # 载体扩散到 residual 结构：用同一 W=252/lag 变体，派发方负责带 decay=126
        return _fin(RESIDUAL_TPL[tpl].format(X=F))
    if tpl == "dw":
        return _fin(DW_TPL.format(F=F, BF=BF, WS=WS, WL=WL))
    if tpl == "pp":
        # pp 不是独立模板，而是「dw 结构 + 0.85 稀疏门控」（sentiment26/wp99v7qv 的成品形态）
        dw = DW_TPL.format(F=F, BF=BF, WS=WS, WL=WL)
        return _fin(f"if_else(greater(rank({dw}), 0.85), {dw}, 0)")
    if tpl.endswith("_pl"):
        l1, l2 = tpl[:-3], None
    elif "_" in tpl:
        l1, l2 = tpl.split("_", 1)
    else:
        l1, l2 = tpl, None
    if l1 not in L1_EXTRACT:
        return None
    if l2 == "va":
        return _fin(VA_TPL.format(F=F, BF=BF, ZW=ZW, W1=W1))
    x = L1_EXTRACT[l1].format(F=F, FR=FR, BF=BF, ZW=ZW, W1=W1)
    if l2:
        x = L2_NORM[l2].format(X=x, ZW=ZW)
    return _fin(x)


def wrap(r):
    if r["field_type"] != "VECTOR":
        return r["field_name"]
    return f"vec_sum({r['field_name']})" if r["sem_type"] == "count" else f"vec_avg({r['field_name']})"


def build_postproc(code):
    """对最佳构造套后处理电池（稀疏化 / 分组 / 压缩 / tvr）。"""
    out = []
    # ⚠ 统一用 tpl="pp"：若按变体名分组（pp_sp/pp_gr/pp_spw），后两者各只有 1 条 ⇒
    #   落成单条批 ⇒ COMPLETE children=0 收不到结果（2026-10-22 实测）。同一 tpl 会合并成一批。
    for q in POSTPROC_Q:
        out.append(("pp", f"if_else(greater(rank({code}), {q}), {code}, 0)"))
    out.append(("pp", f"group_rank({code}, market)"))
    out.append(("pp", f"signed_power({code}, {PP_POW:g})"))
    return out


def build_exprs(sel, freq, cat=None, ds=None, _force_full=False, pp_map=None):
    """分层生成：L1 提取 × L2 归一化 交叉 + L3 双窗（零收益族按 RETIRED_FAMILIES 收窄）。

    2026-10-24 起叠加三层（借鉴 brain-data-feature-engineering skill）：
      ① 字段透明度分档 —— 黑盒字段不信形态分类，走「无先验多样族」BLACKBOX_FAMILIES；
      ② preprocessing 受控词表 —— `pp_map[字段]` 命中则给字段原子套预处理（有序）；
      ③ Expected Exposure —— 每条表达式记暴露到 `EXPR_EXPOSURE`，供数据集末统计。
    """
    BF, WS, WL, ZW, W1 = FREQ_WIN.get(freq, FREQ_WIN["unknown"])
    pp_map = pp_map or {}
    out = []
    _gated = (cat or "").upper() in GATED_CATS
    for r in sel:
        FR = r["field_name"]
        # ② 收益来源先验：字段语义优先（探针层也要用，否则 12 条探针全被错标成 value）
        _hint = field_exposure_hint(r, cat)
        if r.get("tier") == "probe":
            # 探针层：只跑最便宜的 lvl_rk，1 条/字段（成本 ≈ 剩余字段数 × 1）
            # VECTOR 字段必须用 vec_* 包裹且不能 backfill（2026-10-25 IND option1 实测）
            _Fp = wrap(r)
            _x = L1_EXTRACT["lvl"].format(F=_Fp, FR=FR, BF=BF, ZW=ZW, W1=W1)
            _e = L2_NORM["rk"].format(X=_x, ZW=ZW)
            if r.get("field_type") == "VECTOR":
                _e = strip_backfill(_e, F=_Fp, FR=FR, BF=BF)
            out.append(("lvl_rk", _e))
            EXPR_EXPOSURE[_e] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("lvl_rk", "other")
            continue
        _form = r.get("form") or field_form(r, ds)
        r["form"] = _form
        if _form == "skip":
            continue
        # ② 透明度分档：黑盒 ⇒ 不信形态减法；半透明/透明 ⇒ 仍信 FORM_FAMILIES
        _tier = r.get("ftier") or field_tier(r, cat, ds)
        r["ftier"] = _tier
        if _tier == "blackbox":
            # 黑盒：机制驱动。概念推不出才退回校准过的固定多样族
            _cf = concept_families(r, cat, ds)
            _allow = ensure_l1_coverage(_cf if _cf else set(BLACKBOX_FAMILIES))
            _gated_f = True               # 黑盒也开 pp 门控（实测 pp 是 other 形态最强族）
        else:
            _allow = None if _force_full else FORM_FAMILIES.get(_form)
            if _allow is None and not _force_full:
                # form=other ⇒ 形态分类器失效，用概念补（2026-10-24）
                _cf = concept_families(r, cat, ds)
                if _cf:
                    _allow = _cf
            # ★ L1 覆盖保证：补上缺失的时间导数层（治「形态≠导数层」的系统性盲区）
            _allow = ensure_l1_coverage(_allow)
            _gated_f = _gated
        # 概念留痕：汇报与后续校准都要用
        r["concepts"] = field_concepts(r, cat, ds)
        # ② preprocessing：只对受控词表命中的字段生效（自由文本已在 parse 阶段丢弃）。
        #   在族内套，以便跳过与模板自身 L2 重复的归一（如预处理说 rank 而模板就是 rank）。
        F0 = wrap(r)
        _toks = pp_map.get(FR)
        _is_vec = r.get("field_type") == "VECTOR"
        if _is_vec and _toks:
            # VECTOR/事件字段不接受 ts_backfill ⇒ 预处理里的 backfill 令牌必须摘掉
            _toks = [t for t in _toks if t != "backfill"]
        for l1, l2 in FAMILIES:
            _fam = f"{l1}_{l2 or 'pl'}"
            if _allow is not None and _fam not in _allow:
                continue
            # P1-5：零收益族退役闸（只对差分几何 d2_* 生效；level 族经 A/B #6 已恢复）
            if not _family_enabled(_fam, _form):
                continue
            if l1 == "dsp" and r["field_type"] != "VECTOR":
                continue
            F = apply_preprocessing(F0, _toks, FR, BF, ZW, l2) if _toks else F0
            if l2 == "va":
                x = VA_TPL.format(F=F, BF=BF, ZW=ZW, W1=W1)
            else:
                x = L1_EXTRACT[l1].format(F=F, FR=FR, BF=BF, ZW=ZW, W1=W1)
                if l2:
                    x = L2_NORM[l2].format(X=x, ZW=ZW)
            if _is_vec:
                x = strip_backfill(x, F=F, FR=FR, BF=BF)
            out.append((_fam, x))
            EXPR_EXPOSURE[x] = _hint if _hint != "value" else FAMILY_EXPOSURE.get(_fam, "other")
        _Fdw = apply_preprocessing(F0, _toks, FR, BF, ZW, None) if _toks else F0
        if (_allow is None or "dw" in _allow) and _family_enabled("dw", _form):
            _dw = DW_TPL.format(F=_Fdw, BF=BF, WS=WS, WL=WL)
            if _is_vec:
                _dw = strip_backfill(_dw, F=_Fdw, FR=FR, BF=BF)
            out.append(("dw", _dw))
            EXPR_EXPOSURE[_dw] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("dw", "other")
        # 稀疏门控一等模板（之前只在 build_postproc 对 top3 生效 ⇒ sentiment26 的 pp 只覆盖 2/19 字段）
        if _gated_f and (_allow is None or "pp" in _allow):
            _dw = DW_TPL.format(F=_Fdw, BF=BF, WS=WS, WL=WL)
            _pp = f"if_else(greater(rank({_dw}), {GATE_Q}), {_dw}, 0)"
            if _is_vec:
                _pp = strip_backfill(_pp, F=_Fdw, FR=FR, BF=BF)
            out.append(("pp", _pp))
            EXPR_EXPOSURE[_pp] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("pp", "other")
            # tl（单窗 tail 门控）与 pp 同源。§6 的「9 行 0 命中、max 0.03」是 decay 4 旧几何，
            # A/B #6 只证伪了 level 族的退役 ⇒ 按「未证伪即保留」恢复（见 RETIRED_FAMILIES 注释）。
            _m = (f"rank(ts_mean({_Fdw}, {WS}))" if _is_vec
                  else f"rank(ts_mean(ts_backfill({_Fdw}, {BF}), {WS}))")
            _tl = f"tail({_m}, lower=0, upper={GATE_Q}, newval=0)"
            out.append(("tl", _tl))
            EXPR_EXPOSURE[_tl] = _hint if _hint != "value" else FAMILY_EXPOSURE.get("tl", "other")

    # 安全阀（2026-10-23）：形态映射只做「减法」，但减错会丢族。
    # 判据：非探针字段的规模若被压到全交叉的 <50%，说明分类器在该集上不可信 ⇒ 退回全交叉。
    # 分母按各字段形态分别算（P1-5 后「全交叉」已因族退役变窄，仍用 len(FAMILIES)+1 会误报）。
    _nonprobe = [r for r in sel if r.get("tier") != "probe" and r.get("form") != "skip"]
    if not _force_full and _nonprobe:
        _expect = sum(_enabled_family_count(r.get("form")) for r in _nonprobe)
        # 阈值 35%：正常的 level_ratio(8/12)/count(3/12) 映射本就会压到 50% 左右，
        # 用 50% 会频繁误触（news20 实测 44/96 被误判）。35% 只拦真正的病态收窄（如 16/98）。
        if len(out) < 0.35 * _expect:
            print(f"  [form] ⚠ 映射后仅 {len(out)}/{_expect} 条（<35%）⇒ 该集分类不可信，退回全交叉")
            return build_exprs(sel, freq, cat=cat, ds=ds, _force_full=True, pp_map=pp_map)
    return out
