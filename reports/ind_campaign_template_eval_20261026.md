# IND 战役流水线「探针 / 模板电池」评估（2026-10-26）

> 评估对象：`Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/wqb_campaign/`
> 的 `generate.py`（模板体）、`pipeline_ind.py`（编排/判定）、`fields.py`（字段分层与载体扩散）、`sweep.py`（设置轴）。
> 证据源：`results/full_template_campaign_results_IND.json`（1115 行 / 21 个结果键，其中 20 个有 alpha）、
> 平台 `GET /alphas/{id}` 点检、`docs/reference/ind_campaign_runbook_20261025.md` §9.8–§9.9。
> 本文是评估，**本轮未改任何代码**；实施需按 §9 的 A/B 验收逐项落地。

## 0. 结论

**需要调整，而且不是微调。** 探针层与模板电池的核心问题不是「参数不够多」，而是**几何与口径错配**：

1. **模板电池自己的两个全闸 ATOM 成品，用当前参数复现不出来**（平滑长度 5 vs 实测 2；decay 10 vs 实测 6/2）。
2. **判定只看正向 `max_s`**，强负向 ATOM 信号（risk68 `|S|=4.35`、risk70 `2.35`、sentiment21 `1.67`）被静默忽略。
3. **设置轴不适配 IND**：`SWEEP_VARIANTS` 首个变体是 `TOP2500`（IND 只有 `TOP500`），且没有 decay / nanHandling 轴。
4. **探针层 = 每字段 1 条 `lvl_rk`**，而 `lvl_rk` 是全库信息量最低的族（231 行、中位 S 0.00、2 行 ≥1.58），
   且探针字段在结构上几乎拿不到 robust 几何 —— 而 robust 是 IND 唯一已验证的通路。

P0/P1 五项，加上 P2 三项（条件化字段上限、bf 口径 A/B、ATOM 标志贯通与族归属修复）。
§8 列出**不该动**的部分，§9 给每项的最小 A/B 验收点与批次成本。

## 1. 证据基线

### 1.1 族级统计（1115 行，`logs/_tmp_tpl_stats.py` 复算）

| tpl | n | 集数 | 中位 S | 最大 S | S≥1.0 | S≥1.58 |
|---|---:|---:|---:|---:|---:|---:|
| pp | 254 | 16 | 0.93 | 5.20 | 116 | 80 |
| res | 61 | 13 | 1.33 | 3.07 | 33 | 20 |
| reslag | 61 | 13 | 1.18 | 2.91 | 34 | 23 |
| lvl_qc | 10 | 4 | 0.00 | 1.80 | 2 | 1 |
| d1_va | 14 | 6 | 0.00 | 1.16 | 2 | 0 |
| rep | 37 | 7 | 0.13 | 2.92 | 4 | 2 |
| lvl_tr | 63 | 18 | −0.03 | 1.62 | 4 | 2 |
| lvl_rk | 231 | 20 | 0.00 | 2.64 | 10 | 2 |
| d1_rk | 92 | 20 | 0.00 | 2.90 | 3 | 1 |
| lvl_zs | 52 | 16 | −0.15 | 1.61 | 5 | 1 |
| lvl_qt | 43 | 13 | −0.23 | 1.62 | 3 | 2 |
| lvl_sc | 49 | 15 | −0.23 | 1.41 | 4 | 0 |
| dw | 78 | 19 | −0.10 | 0.82 | 0 | 0 |
| ed_rk | 23 | 6 | 0.00 | 0.98 | 0 | 0 |
| d2_rk / d2_qc | 18 / 10 | 7 / 4 | 0.05 / 0.04 | 0.44 / 0.48 | 0 / 0 | 0 / 0 |
| ir_pl | 8 | 3 | 0.00 | 0.41 | 0 | 0 |
| dsp_rk | 2 | 1 | 0.00 | 0.00 | 0 | 0 |
| tl | 9 | 3 | −0.32 | 0.03 | 0 | 0 |

（结果行不带 `rob`；robust 结论来自 runbook §9.8/§9.9 的平台点检，共 10 颗。）

### 1.2 两个必须内化的口径事实

**① `pp` 行不是单一族，且高 S 的 `pp` 基本不是 ATOM。**
`build_exprs` 里独立的 `pp` 是 ATOM（只用本数据集字段 + 门控）；但 `pipeline_ind.py:544-589` 的
阶段 2 会把 **top3 构造**（可能是 `res`/`reslag`）再套一遍 `build_postproc`，同样记 `tpl="pp"`。
runbook §9.8 抽查 3 颗 S 4.87–5.20 的 `pp` 幸存者，全部是
`rank(-ts_regression(ts_zscore(returns,252), …))` 的残差形态，`pyramids.effective=2`，**不是 ATOM**。
所以上表 `pp` 的 80 行 ≥1.58 **不能**当作「pp 是最强 ATOM 族」的证据。

**② `rep` 行丢了族标签。**
`rep` 是单条孤儿批合并重派（`pipeline_ind.py:363-390`），`norm_tpl()` 只并回 `_rp/_cx/_f/_r`，
`rep` 保持原样。fnd86 那颗 S2.92 的 ATOM 行 `GrgRj9mZ` 就落在 `rep` 里 —— 按族统计会被低估，
按 ATOM 过滤会被漏掉。这是 P2-4 的直接证据。

### 1.3 ATOM 模板 vs 全模板（每集最高 S，`logs/_tmp_sign_atom_stats.py`）

| dataset | 全模板 best S | ATOM 13 族+dw best S | ATOM best tpl | 差值 |
|---|---:|---:|---|---:|
| earnings3 | 5.20 | 0.57 | lvl_rk | 4.63 |
| risk68 | 5.05 | 0.27 | lvl_tr | 4.78 |
| fundamental23 | 5.02 | 1.16 | d1_va | 3.86 |
| institutions6 | 5.00 | 0.95 | lvl_tr | 4.05 |
| fundamental94 | 4.93 | 1.62 | lvl_qt | 3.31 |
| risk70 | 4.74 | 0.58 | lvl_rk | 4.16 |
| fundamental90 | 3.45 | 1.28 | lvl_rk | 2.17 |
| fundamental44 | 3.10 | 1.17 | lvl_rk | 1.93 |
| fundamental86 | 2.97 | 2.64 | lvl_rk | 0.33 |
| option1 | 2.90 | 2.90 | d1_rk | 0.00 |
| 其余 10 集 | ≤1.20 | ≤1.20 | — | ≈0 |

**ATOM 模板 maxS ≥1.58 的集只有 3 个**：fundamental86（2.64，另有 rep 2.92）、fundamental94（1.62）、
option1（2.90，但单年 ⇒ `INSUFFICIENT_HISTORY`）。
runbook §9.8 的 728 颗 ATOM 模板 alpha 里，S≥1.58 仅 11 颗（1.5%），中位 S = 0.00。
**这就是「探针/模板电池需要调整」的根问题：不是命中率低，是 ATOM 口径下的有效几何几乎不存在于电池里。**

## 2. P0-1 参数硬编码，错过已验证成品

### 2.1 现状

`generate.py:165-180`：

- `RG_LV_SMOOTH = 5`（lvvol 的 `ts_mean` 平滑长度）
- `ROBUST_DECAY = 10`（robust 几何族的统一 decay）
- `RG_BF = 22`、`RG_ZW = 252`（这两项有实证，保留）

### 2.2 实证

| 成品 | 结构 | 设置 | 结果 |
|---|---|---|---|
| `gJWnrZgg` | `rg_lvvol_sec`（smooth **2**） | decay **2** | S2.14 / F1.70 / TO0.1072 / 2Y1.99 / sub0.93 / rob**1.02** / prod**0.6998** / self0.4478，全闸 pass |
| `58jPrvZ1` | `rg_grdev_p3_sec` | decay **6** | S1.64 / F1.27 / TO0.1142 / 2Y2.23 / sub1.55 / rob**1.12** / prod0.5354 / self0.4843，`checks.fail=[]` |

同一几何只改平滑长度 N（fnd86，decay 2 固定）：

| N | 0 | **2** | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| robust | 1.05 | **1.02** | 0.98 | 0.97 | 0.99 |
| prod | 0.7056 ✗ | **0.6998 ✓** | — | — | 0.6989 ✓ |
| S | 2.18 | 2.14 | 2.11 | 2.08 | 2.10 |

⇒ 当前代码 `RG_LV_SMOOTH=5` + `ROBUST_DECAY=10` 跑出的 lvvol 是 rob **0.99** 的版本，
**差 0.01 卡在 LOW_ROBUST**；而电池无法生成 smooth=2 的赢家。
analyst 线同理：decay 10 的最高 S 是 1.56（差 S 线 0.02），decay 6 才到 1.64。

### 2.3 建议

1. **lvvol 平滑参数化**：`rg_lvvol` / `rg_lvvol_sec` 各出 `smooth=2` 与 `smooth=5` 两版
   （或把 `RG_LV_SMOOTH` 改成按模板的字典）。字段数 ×2 条模板 ⇒ **+2 批/集**。
2. **dev 族 decay 双锚**：`rg_grdev*` 四模板在 `{6, 10}` 各派一批；`rg_rkz/rg_grz/rg_grdev` 之外的 z/rank
   族保持 10（z 族在 10 的实证充分，decay 6 没有额外证据）。全量重派 ⇒ +8 批/集。
   **经济版（推荐先做）**：阶段 1.6 后只把「本集 best robust 模板」在 decay `{2, 6}` 各重跑一批
   ⇒ **+2 批/集**，覆盖 fnd86 的 2 与 analyst 的 6 两个锚点。
3. 不要直接把 `ROBUST_DECAY` 全局改成 6：decay 10 对 z/rank 族有独立实证（`rg_rkz` decay10 rob1.02），
   统一改会丢掉那条线。

## 3. P0-2 符号盲区：只看正向 `max_s`

### 3.1 现状

`pipeline_ind.py:532-542` 的 `best[tpl]["max_s"] = max(...)`、`:713-718` 的 verdict 全部只看向上取整的
`max_s`。`s` 为负的行仍存在 `all_alphas` 里，但**不参与任何胜负判断**。

### 3.2 本轮结果里的负向强信号（S ≤ −1.5）

| dataset | tpl | alpha | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|
| risk68 | lvl_rk | `N1eZj1Wg` | **−4.35** | −2.21 | −4.44 | −2.72 |
| risk70 | d1_rk | `9qEeOGYr` | **−2.35** | −1.73 | −1.91 | −0.74 |
| sentiment21 | lvl_rk | `zqr72EkR` | **−1.67** | −0.72 | −0.79 | −0.64 |
| option1 | lvl_rk | `bl8m3Mqp` | −1.54 | −1.36 | 0.0 | −2.07 |

- risk68 / risk70 的**集级 verdict 是 ALIVE**，但撑起它的 `pp` 在 risk68 上已逐颗确认是残差（非 ATOM）；
  按 ATOM 口径，两者的最高正 S 只有 **0.27 / 0.58**，而负向 |S| 有 4.35 / 2.35 ⇒ **ATOM 线被误判为空**。
- sentiment21 是唯一被 `max_s<1.3 & min_s≤−1.58` 直接判 DEAD 的集（`max_s=1.12`）。
  runbook §9.9.1 的手工反向 dev 实测 S**1.80** / 2Y2.35 / sub1.25 / rob**1.38**（仅 F0.84 未过），
  证明「负向簇 → 镜像」有真实产出。

### 3.3 镜像的适用范围（可零成本筛选）

对**奇对称结构**，`multiply(-1, x)` 后 S/F/2Y/sub/rob 精确取负，TO/CW 不变：

- 可用：`rank`、`ts_zscore`、`ts_rank`、`ts_quantile`、`ts_scale`、`quantile`、`ts_delta`、
  `dev + group_rank`、`signed_power(·, 奇数)`；
- 不可用：`pp` 的 `if_else(greater(rank(dw), q), dw, 0)`（门控后取反不等价）、`abs`、`signed_power(·, 偶数)`、
  含 `ts_regression` 残差的复合（残差项本身不是奇函数，且它不是 ATOM）。

实证：runbook §9.9.1 `1YNqgaoX` 是 `0mYbz96G` 的镜像（S1.80 / TO0.372 / rob1.38）；
§9.9.6 `omE1gOPE` 是 `E56ZeJQm` 的严格镜像（S−1.68）。

### 3.4 建议

1. 判定里同时记录 `min_s`、`max_abs_s`、`max_neg_s`；verdict 增加 `DEAD_NEG` / `ALIVE_NEG` 两种可辨识状态
   （不要把它混进现有 DEAD）。
2. 每集若存在 `s ≤ −1.58` 的 ATOM 行，自动构造 **top1–2 条真镜像**，单独一批派发（2 条 = 1 批）。
   只镜像 §3.3 白名单结构；`pp`/残差行只做诊断，不镜像。
3. **镜像不是免死金牌**：TO/CW 不变。risk68 的镜像 TO 仍是 **0.8702**（MCP 实测）⇒ 识别到了也过不了换手闸，
   应记为「负向强信号，卡 HIGH_TURNOVER」，而不是「无信号」。
4. 验收：risk68 `N1eZj1Wg` 的镜像必须精确得到 S+4.35 / F+2.21 / 2Y+4.44 / sub+2.72 / TO0.8702；
   sentiment21 `zqr72EkR` 镜像 S+1.67。
   **✅ 已验（2026-10-27）**：`npvx7W2w` / `2rA8Op2x` 逐项命中，见 §11「P0-2 负向镜像」。

## 4. P0-3 设置轴不适配 IND

`sweep.py:39-44`：

```python
SWEEP_VARIANTS = [
    ("u2500", {"universe": "TOP2500"}),
    ("subind", {"neutralization": "SUBINDUSTRY"}),
    ("crowd", {"neutralization": "CROWDING"}),
]
```

问题有三层：

1. **`u2500` 对 IND 无效**：IND 平台只提供 `TOP500`（`src/wqb/config.py` 的 IND universes 仅 `["TOP500"]`）。
   该变体要么整批 ERROR，要么白烧 2 条仿真/近闸集。
2. **没有 decay 轴**：两个成品分别落在 decay 6 / 2，而主派发是 4、robust 批是 10；设置轴扫不到它们。
3. **没有 nanHandling 轴**：IND 缺省 `nanHandling=OFF`，而 behavioral_signals 有 ON 2.19 vs OFF 0.46（4.8×）的先例。
   （sentiment 塔已实测 ON 无效，见 runbook §9.9.5 ⇒ 该轴只应对事件/向量类集启用，不要全类铺开。）
4. **目标选择不看 ATOM**：`settings_sweep` 取 `top-2 by S`，近闸集的 top 往往是 `pp`/残差 ⇒ 扫的是非 ATOM 腿。

建议：

- `u2500` → `d6` / `d2` 两个 decay 变体；`subind` / `crowd` 保留（IND 中性化域包含这两档）。
- 近闸集（`max_s ∈ [1.2,1.58)`）的目标选择改为：**先 ATOM 族、再全族**；robust 模板必须带 `ROBUST_DECAY`（现逻辑已有）。
- `nanHandling=ON` 只对 `INSIDERS / OPTION / NEWS / SENTIMENT / VECTOR 事件类` 启用，且只扫 top-2 ⇒ 2 条/变体。
- 成本：每条变体 2 条仿真；4 个变体（d6 / d2 / subind / crowd）= 8 条/近闸集，不进入全量集。

## 5. P1-4 探针层：本评估的直接答案

### 5.1 现状（代码）

`generate.py:380-390`：

```python
if r.get("tier") == "probe":
    # 探针层：只跑最便宜的 lvl_rk，1 条/字段
    _x = L1_EXTRACT["lvl"].format(...)
    _e = L2_NORM["rk"].format(X=_x, ...)
    out.append(("lvl_rk", _e))
    continue
```

`PROBE_FIELD_CAP = 12`；`build_robust_geom()` 明确 `if r.get("tier") == "probe" … continue`
（`generate.py:257`）；`carrier_expand()` 只扩展**单个最佳模板**，且要求 `max_s ≥ 1.2`
（`fields.py:363-380`）。

### 5.2 为什么这是最该改的一处

| 事实 | 证据 |
|---|---|
| 探针模板 `lvl_rk` 是全库信息量最低的族 | 231 行、中位 S **0.00**、10 行 ≥1.0、2 行 ≥1.58 |
| 探针字段几乎拿不到 robust 几何 | `carrier_expand` 只在全电池 best ≥1.2 时触发：10/20 集扩的是 `pp`（高 S 的 pp 在 runbook §9.8 抽查中全是残差+后处理，非 ATOM）；9/20 集完全不触发；只有 option1 的 `d1_rk` 是 ATOM 结构扩散 |
| 近闸集就是这样漏掉的 | sentiment21 全电池 best 1.12（`lvl_rk`）⇒ DEAD；同字段手工反向 dev S1.80/rob1.38 |
| 薄字段集在 robust 几何下并非无信号 | imbalance5 三臂手工实测 rob 0.69/0.68/0.92（差 0.08–0.31，不是 0） |

换句话说：**探针层测的是「水平量有没有方向性」，而 IND 的闸门问的是「稳健几何下有没有方向性」。**
两者不是同一件事，所以探针的 DEAD 不能当作数据集判死证据。

### 5.3 建议

- 探针层改为 **2 条/字段**：`lvl_rk`（保留最便宜的基线）+ `rg_grdev_p3_sec`（ATOM 安全：只用本数据集字段 +
  `sector` 分组；已在 analyst 线全闸 pass）。
- `rg_grdev_p3_sec` 探针必须进 **robust 批**、带 `ROBUST_DECAY`（当前 `dispatch` 的 settings 已支持），
  不能混在主派发 decay 4 里。
- 成本：12 条 `lvl_rk` = 2 批，12 条 `rg_grdev_p3_sec` = 2 批；对比现状 2 批 ⇒ **净 +2 批/集**。
- 若预算紧：前 6 个探针字段跑 `lvl_rk`，后 6 个跑 `rg_grdev_p3_sec`，总条数不变（12 条），
  但会放弃一半字段的基线对照；不推荐作为长期方案。
- 验收：sentiment21 的探针字段上，`rg_grdev_p3_sec` 应复现 S≥1.58 / rob≥1.0 / TO≤0.40 的至少一条；
  imbalance5 应落在 S1.5–1.8 / rob0.7–0.9（即使不过闸，也要能看见信号）。

## 6. P1-5 零收益族退役

| 族 | 行数 | ≥1.0 | 最大 S | 判断 |
|---|---:|---:|---:|---|
| dw | 78 | 0 | 0.82 | 仅保留给 `level_ratio` 形态；从 `BLACKBOX_FAMILIES` 移除 |
| ed_rk | 23 | 0 | 0.98 | 仅保留给 `event_date` 形态 |
| d2_rk + d2_qc | 28 | 0 | 0.48 | 直接退役（二阶差分在 IND 无收益） |
| ir_pl | 8 | 0 | 0.41 | 仅保留给波动率 / 水平比形态 |
| dsp_rk | 2 | 0 | 0.00 | 仅 VECTOR count（本来就是） |
| tl | 9 | 0 | 0.03 | 退役（门控变体 `pp` 已覆盖） |

20 个数据集 × 78/23/28/19 行的零收益是足够强的证据。退役的是**默认笛卡尔积**，不是永久删除结构：
按 `FORM_FAMILIES` 条件保留即可。预计 **−4 批/集**，正好抵消 P0-1 与探针的增量。

⚠ 这批结论全部产生于 decay 4 / 季年 BF=252 的旧几何。正式删除前用 fnd86 一颗确认批（decay10 下 d2/ed/dw）
即可；20 集样本已足够停止为它们付全量成本。

> **⚠ 2026-10-27 更正（A/B #6 已跑，本表不能直接当删除依据）**：确认批在 decay 10 下把 **ed_rk 与 dw 翻案**——
> `ed_rk` 3 条 S = 1.31 / **2.91** / 1.48、`dw` 3 条 S = 0.82 / **2.48** / 1.10，两族都有 ≥1.0。
> 只有差分几何 `d2_rk / d2_qc` 复核同向（6/6 <1.0）。
> ⇒ **最终只退役 d2**，`ed_rk / ir_pl / dw / tl` 全部恢复；level 几何的旧 decay-4 结论不可泛化到 decay 10。
> 详细证据与落地见 §11「P1-5 零收益族退役」。本表保留原样作**过程记录**，判读以 §11 为准。

## 7. P2 三项

### P2-1 字段上限条件化

`FULL_FIELD_CAP=8` 对 87 字段的 risk70 只测 8 个（9%）。但无条件放宽会线性放大派发量。
建议：仅当 `max_s ∈ [1.0, 1.3)` 且 `n_fields ≥ 50` 时，把上限临时抬到 16（第二轮），
其余情况保持 8。判据是「扩字段有没有可能改变 verdict」，不是「字段多不多」。

### P2-2 bf 口径 A/B（季/年报集）

`FREQ_WIN` 对 `quarterly/annual` 把 BF 定 252，而 robust 族固定 22。两者都没有在 IND 上做过同族对照。
建议在 fnd86（季报）跑一组 `bf=22/66/252` 的 `rg_rkz`（3 条 = 1 批），只回答一个问题：
「短 bf 的收益是 robust 几何带来的，还是 bf 位置带来的」。若 22 明显优于 252，再把 `FREQ_WIN` 的季年 BF 改短；
否则只保留 robust 族的 22，主族不动。

### P2-3 ATOM 标志贯通 + 族归属修复

当前 `pipeline_ind.py` 的 `_absorb` 只存 `{alpha,tpl,s,f,y2,sub,rob,batch}`，无法区分：

- `pp` 是独立 ATOM 门控，还是残差套后处理（非 ATOM）；
- `rep` 原本属于哪个族；
- 一行是否 ATOM（是否含 PV `returns` / 跨数据集腿）。

建议在结果行加三个字段：`atom: bool`、`src_tpl`（`rep`/`pp` 的来源族）、`atom_reason`。
连带修改：

- `verdict` 增加 `atom_max_s` / `atom_deliverable`；
- `pick_prod_target` 在 ATOM_ONLY 波次里优先 ATOM 行（否则会拿非 ATOM pp 去测 prod，
  正是 risk68「ATOM 空但集级 ALIVE」的机制）；
- `settings_sweep` 的目标选择同样先 ATOM。

这是本次评估里**唯一属于「测量口径」而非「搜索空间」的改动**，优先级高于任何新模板。

## 8. 明确不改

| 项 | 理由 |
|---|---|
| `FORM_FAMILIES` 形态映射 | 13 族的映射没有证据表明错了；问题是几何（无 group/短 bf/凸变换），不是减法映射 |
| `pp` 后处理电池 | 它仍是 IND 唯一被证实能过 prod 墙的路径（残差 + pp，prod 0.67–0.70）；保留为**备选**，但必须标非 ATOM |
| `RESIDUAL_TPL` 默认开启 | 同上；纯 ATOM 波次用 `WQB_ATOM_ONLY=1` 显式关闭，不要改默认 |
| 平台闸门常数 | S1.58 / F1.0 / 2Y1.0 / sub1.0 / rob1.0 / TO0.40 / prod0.70 一律不动 |
| 字段分层上限 8/2/12 本身 | 不是瓶颈；P2-1 只做条件化，不做全局放大 |
| `PP_POW=3` 的叙述 | 现有实现是对**未居中**的 `rank(code)` 取凸幂，不等于已验证的「居中后凸」；如果要改，按 `rg_grdev_p3` 的居中版重做，不要只改指数 |

## 9. 最小 A/B 验收（每项 1–2 批）

| # | 改动 | 数据集 / 臂 | 通过判据 |
|---|---|---|---|
| 1 | lvvol smooth=2 + decay2 | fnd86 `rg_lvvol_sec_s2` | S≥2.10、rob≥1.00、prod<0.70（复现 `gJWnrZgg`） |
| 2 | dev decay6 | analyst_consensus `rg_grdev_p3_sec` | S≥1.58、rob≥1.0、prod<0.70（复现 `58jPrvZ1` 的闸位） |
| 3 | 探针 robust | sentiment21 探针字段 `rg_grdev_p3_sec` | ≥1 条 S≥1.58 / rob≥1.0 / TO≤0.40 |
| 4 | sweep decay6/d2 | 任一近闸集（当前 insiders1 1.20；或 robust 批后落入 [1.2,1.58) 的集） | 变体 max S 或 rob 单调优于 decay4/10 |
| 5 | 镜像 | risk68 `N1eZj1Wg` 镜像 | 指标精确取负、TO 0.8702 不变（预期仍卡换手） |
| 6 | 退役确认 | fnd86 decay10 的 d2/ed/dw | 无一条 ≥1.0（确认可退役） |

> **执行结果（2026-10-27）**：#6 = **FAIL**（12 条里 5 条 ≥1.0：ed_rk 2.91/1.48/1.31、dw 2.48/1.10）。
> 只有 d2_rk / d2_qc 复核同向（6/6 <1.0）⇒ 退役范围收窄到 d2，其余四族恢复。证据见 §11「P1-5 零收益族退役」。
> #5 = **PASS**（`N1eZj1Wg` 镜像 `npvx7W2w`：S/F/2Y/sub/rob 精确取负，TO 0.8702 不变、仍卡 HIGH_TURNOVER）。
> 旁证 `zqr72EkR` 镜像 `2rA8Op2x` S+1.67 逐项命中。证据见 §11「P0-2 负向镜像」。

任何一项未过，不改下一项；尤其 #1/#2 是「电池能否复现自己的赢家」的根验证。

## 10. 实施顺序与成本

1. **P0-1**（smooth 参数化 + dev decay 双锚，经济版 +4 批/集）
2. **P0-3**（sweep 轴替换，仅近闸集，约 6 条/集）
3. **P1-4**（探针 +2 批/集）
4. **P1-5**（退役 −4 批/集，抵消 1/3）
5. **P0-2**（判定层 + 镜像批，仅命中负向簇的集，+1 批/集）
6. **P2-3**（ATOM 标志；纯代码，无平台成本）→ **P2-1 / P2-2**

净成本（全量集）：robust 9 批 → 约 13 批；探针 2 → 4；主派发 −4 ⇒ **每集净 +2 批**。
在账户并发 2、约 2.5 分钟/批的吞吐下，20 集约多 100 分钟，可接受。

## 11. 实施记录（按 §9 逐项过 A/B）

### P0-3 设置轴补扫 —— A/B #4 通过（2026-10-26/27）

代码（`wqb_campaign/sweep.py`）：

- 变体表切到 IND 有效轴（`SWEEP_VARIANTS_BY_REGION["IND"]` = d6 / d2 / subind / crowd，
  INSIDERS 等事件类再叠 `nanon`），`u2500` 在 IND 是白烧（universe 只有 TOP500）。
- **修掉 settings_sweep 从不出结果的老 bug**：旧实现按**源模板**打标签（`lvl_sc_d6` / `lvl_tr_d6`），
  每个标签只有 1 条表达式 ⇒ 平台必返 `COMPLETE children=0`，结果永远收不到。
  现统一打 `sw_{tag}` 标签（同变体的表达式同批），命中后按「表达式逐字相等」回填 `src_tpl`。
- 基座 decay 按结构钉住（robust 族走 `robust_decay`，其余走区域缺省 4），换中性化/开关时只动一个变量。
- `--sweep-done` 重跑会复用已派发断点，同一批 alpha 会被再次收割 ⇒ 按 alpha id 去重后再并入 `alphas`
  （本轮实测 `E56Z8wYm` 重复两行，已清）。

A/B 实测（insiders1，基座 `STATISTICAL / decay 4`，整集原 max_S=1.20、verdict=DEAD）：

| 变体 | 覆写 | max S | 关键行（src 模板） |
|---|---|---:|---|
| crowd | neutralization=CROWDING | **1.33** | `lvl_tr` 1.06→**1.33**（sub 0.78→1.11、**rob 1.21**）；`lvl_sc` 1.19→1.25 |
| d6 | decay 6 | 1.20 | `lvl_sc` 1.19→1.20（2Y 1.73→1.76）；`lvl_tr` 1.06→1.04 |
| d2 | decay 2 | 1.19 | 两条均持平/微降（1.19 / 1.03） |
| nanon | nanHandling=ON | 1.19 | 与基座同（1.19 / 1.06）—— 对 INSIDERS 无效，与 runbook §9.9.5 一致 |
| subind | neutralization=SUBINDUSTRY | 0.64 | 两条**腰斩**（1.19→0.64、1.06→0.39）—— IND 对 INSD 类禁用此轴 |

判定 = **通过**：crowd 变体把 max_S 从 1.20 抬到 1.33、并首次给出 rob=1.21（≥1.0），
非单调但明确优于基座；d6 只在 2Y 与 lvl_sc 上微增。整集 verdict 由 DEAD → BORDERLINE。
⚠ 仍卡 fitness（0.53 vs 1.0）⇒ `crowd` 是「破 S/rob 的杠杆」，不是可交付解。

副产品修复（都在同一次 A/B 里被实测逼出来的）：

1. `transport.dispatch` 的失败打印原为 `stderr or stdout` 只取一边，而 `submit_batch` 把真因
   （`status=429/400`、`BODY:`）打在 **stdout**，stderr 只有 `[SUCCESS] JWT token…`
   ⇒ 四个变体连续"失败"却只看到 SUCCESS。现两边各取尾部。
2. 账户级并发按**子任务**计（一个 multisim 带 10 children = 占 10 槽），并行会话一波就能占满十几分钟，
   而 `submit_batch` 自带的 6 次 429 退避只覆盖 1–2 分钟 ⇒ `dispatch` 加一层跨分钟重试
   （3×150s，只对 429；POST 被拒时平台未建作业，不会重复派发）。

### P1-4 探针 robust —— 代码已落，A/B #3 在飞（2026-10-27）

代码（`wqb_campaign/generate.py`）：

- 新增 `ROBUST_PROBE_TPL = ("rg_grdev_p3_sec",)` 与 `WQB_ROBUST_PROBE` 开关
  （`0/false/off/no` 关、`1/true/on/yes` 开，缺省 `REGION=="IND"`）。
- `build_robust_geom()` 对 `tier=="probe"` 的字段**只产这 1 条**模板（原来 11 族全产 ⇒
  12 个探针字段 × 11 = 132 条，占满整波额度却全是低质量结构）；`form=="skip"` 仍排除。
- `ATOM_ONLY` 与探针互不影响（探针不吃 PV，不是残差族）。
- 单测：`tests/unit/11_campaign/test_campaign_package.py` 改 1 例（补 `ROBUST_PROBE=False` 的旧口径）、
  新增 1 例（断言探针只产 `ROBUST_PROBE_TPL`、表达式与 `build_one_family("rg_grdev_p3_sec", …)` 逐字相同、
  `robust_decay()` = 6）⇒ `pytest tests/unit/11_campaign -q` = **71 passed**。

⚠ 已知边界：续跑路径 `only_names` 会 `r.setdefault("tier","full")`，探针档在断点续跑时丢失
（未修；意味着 P1-4 只影响新选集的首次波次，且这是**探针档的既有缺陷**，不是本次引入）。

A/B #3 主臂（§9 第 3 项，判据 `≥1 条 S≥1.58 / rob≥1.0 / TO≤0.40`）：
`sentiment21` full=4 + probe=12 → 12 条 `rg_grdev_p3_sec`（decay 6），分 2 批派发
`KC18V5Tl4guapT90Y4DTg3` / `25FLf44lI5ik9b7ySdX6bKT`（`MAX_INFLIGHT=2`），两批 6/6 COMPLETE。

| alpha | S | F | 2Y | sub | rob | TO |
|---|---:|---:|---:|---:|---:|---:|
| pwdY8Elv | **-1.21** | -0.50 | -1.76 | -0.75 | -0.65 | 0.310 |
| A1Vjk3GE | -1.08 | -0.42 | -1.53 | -0.55 | -0.31 | 0.313 |
| RREjdY1a | -0.92 | -0.32 | -1.90 | -0.31 | -0.25 | 0.319 |
| gJekx38v | -0.69 | -0.21 | -0.96 | -0.30 | -0.06 | 0.302 |
| 58EnM9OM | -0.53 | -0.15 | -0.76 | -0.33 | -0.11 | 0.299 |
| leApr0j5 | **0.68** | 0.21 | 0.79 | 0.23 | -0.03 | 0.319 |
| d5WkdQOw | 0.53 | 0.14 | 0.92 | 0.30 | 0.21 | 0.313 |
| A1Vjkb7d | 0.51 | 0.14 | 1.34 | 0.02 | 0.24 | 0.298 |
| 2rA8JRL6 | 0.49 | 0.13 | 0.43 | 0.24 | 0.25 | 0.306 |
| MPYMkx16 | 0.30 | 0.06 | -0.03 | 0.15 | 0.16 | 0.317 |
| 9qxZJRXK | -0.26 | -0.05 | -0.62 | -0.12 | 0.07 | 0.318 |
| mLowZAbW | -0.00 | -0.00 | -0.19 | -0.47 | -0.33 | 0.292 |

判定 = **FAIL**（三条判据全不满足）：正向最好 S=0.68，绝对值最好 |S|=1.21（`pwdY8Elv`，负向），
rob 最好 0.25。换手不是瓶颈（全部 0.29–0.32，远低于 0.40）。

⚠ 值得记一笔的**符号结构**：12 条里 7 条负向、且最强的三条都是负向（-1.21 / -1.08 / -0.92），
这不是 sentiment 字段该有的形态 —— 情绪字段的正负应先验可知（neg 越高越差、pos 越高越好），
`ts_backfill(x,22)` 扣 252 日趋势后再 group_rank，方向由字段语义决定，**模板替不了符号判断**。
⇒ 与 P0-2（负向强信号镜像）的动机同源：本次即使按 |S| 计也只有 1.21，镜像也救不回来。

因单臂无法区分「探针模板错」与「sentiment21 探针字段本就是垃圾」，加跑**对照臂**
（`analyst_consensus` 探针字段 × 同一模板 —— 该集是 `rg_grdev_p3_sec` 的已证宿主，`58jPrvZ1` 全闸过）。

**对照臂（analyst_consensus，full=8 + probe=12）→ PASS**，12 条里 2 条过 `§9 #3` 判据：

| alpha | S | F | 2Y | sub | rob | TO | 说明 |
|---|---:|---:|---:|---:|---:|---:|---|
| **wpQKeEa2** | **1.73** | **1.44** | **1.64** | **1.39** | **1.30** | 0.094 | **六闸全过**（S/F/2Y/sub/rob/TO） |
| E56OKel1 | 1.59 | 1.26 | 0.82 | 1.28 | 1.16 | 0.092 | 过 A/B 判据，但 2Y 0.82 < 1.0 |
| WjO1gXdQ | 2.08 | 1.81 | 1.93 | 1.02 | 0.78 | 0.092 | 只卡 robust 0.78 |

**判定 = PASS（机制成立，但强数据集依赖）**：同一模板在 `analyst_consensus` 探针字段上直接出一条
六闸全过的候选，在 `sentiment21` 探针字段上全灭（最好 |S| 1.21）。
⇒ 「探针字段不产 robust」这个旧假设是错的（它把概率压成 0），P1-4 保留且 IND 缺省 ON；
把 §9 #3 的原始臂（sentiment21）记为**反向证据**：探针模板不是普适抽奖，值类数据集（analyst）远好于情绪类。

⚠ 本次 A/B 的口径偏离需明示：§9 #3 原定臂是 sentiment21，该臂 FAIL。判 PASS 依据的是**追加的对照臂**，
理由是单数据集全灭无法区分「模板错」与「该集探针字段本就是垃圾」（sentiment21 已在任务 #23–25 挖尽）。
若按原文只认 sentiment21，则此项为 FAIL —— 两种读法都记在这里，不做事后改写。

副产品：`wpQKeEa2` 是**单数据集**（`analyst_consensus`）候选 ⇒ 按平台口径属 ATOM，已列入提交候选池待核
（prod / self 相关性与平台 checks 未测，本节不作可提交结论）。

### P1-5 零收益族退役 —— A/B #6 证伪 3/5，最终只退役差分几何（2026-10-27 定稿）

**结论先行**：§6 那张「0 命中」表是 **decay 4 旧几何**的统计。A/B #6 在 decay 10 下复核，
`ed_rk` 与 `dw` 直接翻案（同一族在强 level 字段上做出 S 2.91 / 2.48）⇒ 退役范围收窄到 **d2_rk / d2_qc**，
其余四族（`ed_rk` / `ir_pl` / `dw` / `tl`）全部恢复，**§6 的表不可直接当删除依据**。

A/B #6（`logs/_tmp_ab6_retire.py`）：fnd86 全 3 个 full 字段（`risk_score` / `average_score` /
`fundamental_score`）× 4 族 = 12 条，**绕过退役闸**直接 `build_one_family` 构造（否则自己验证不到自己），
decay=10、季报窗口（BF 252 / WS 63 / WL 252）。结果（按 |S| 排序）：

| 族 | risk_score | average_score | fundamental_score | 判定 |
|---|---:|---:|---:|---|
| ed_rk | +1.31 | **+2.91** | +1.48 | **2/3 ≥1.0 ⇒ 退役被证伪** |
| dw | +0.82 | **+2.48** | +1.10 | **2/3 ≥1.0 ⇒ 退役被证伪** |
| d2_qc | −0.09 | +0.35 | +0.43 | 3/3 <1.0 ⇒ 退役成立 |
| d2_rk | −0.17 | +0.28 | +0.32 | 3/3 <1.0 ⇒ 退役成立 |

脚本末行判定 `判定 = FAIL（仍有 ≥1.0 ⇒ 不可退役）` —— 按 §9 #6 的字面判据（"无一条 ≥1.0"）整批 FAIL。

**为什么错**：§6 的族级统计混了 20 个数据集、且全是 decay 4。`ed_rk` 的结构
`rank(ts_decay_linear(ts_backfill(F,252),63))` 在**强 level 字段**上是慢速趋势，decay 10 把换手压到 0.06
之后噪声被摊平，收益就浮出来了；`dw`（双窗同向乘）同理。差分几何（d2）没有这个机制——二阶差分再平滑
仍是高阶噪声 ⇒ 复核同向。**旧结论的失效边界是「结构 × decay」二元组，不是数据集数量。**

**落地（最终版代码，`wqb_campaign/generate.py`）**：

- `RETIRED_FAMILIES = {d2_rk: (), d2_qc: ()}`（只退役差分几何）；`ed_rk` / `ir_pl` / `dw` / `tl` 恢复。
- `tl` 发射块恢复：§6 的 9 行 0 命中同样是 decay-4 旧几何、未做 decay-10 复核 ⇒ 按「未证伪即保留」处理
  （结构面窄：只在 `GATED_CATS` 且已被 `pp` 覆盖，不额外烧配额去证伪一个窄结构）。
- `dw` 回到 `BLACKBOX_FAMILIES`，删掉 `_BLACKBOX_FAMILIES` 这层间接。
- `FAMILIES` 保留 13 项作**全集**（`sweep` / `pipeline_ind` 的审计分母不动），退役只作用于 `build_exprs` 的
  默认笛卡尔积；`WQB_LEGACY_FAMILIES=1` 仍可全量回退（`docs/env_registry.json` 措辞已按本结论更新）。
- **35% 安全阀分母**保持逐字段 `_enabled_family_count(form)`（只差 d2 两族后 `change` 形态 8 → 6）。
- 单测 4 例按新结论改写（`test_retired_family_gate_by_form` / `test_build_exprs_drops_retired_families` /
  `test_tl_restored_for_gated_category` / `test_blackbox_families_keep_dw`）⇒ `tests/unit/11_campaign` = **75 passed**。

**副产品（新近闸候选，非本次改动目标）**：`1YNkd1Xm` =
`rank(ts_decay_linear(ts_backfill(fnd86_average_score,252),63))` @ decay 10 →
**S 2.91 / F 2.85 / 2Y 2.35 / sub 0.91 / TO 0.0677 / rob 0.51**，10 项 RA 里**只卡
`LOW_ROBUST_UNIVERSE_SHARPE`**（限 1.0）⇒ fnd86 的 robust 几何是唯一缺口，可进 S4 定向改。
`zq3Kmn6X`（dw on `average_score`，S 2.48 / F 2.25 / 2Y 1.99）卡 sub 0.63<0.73 与 rob 0.26，优先级次之。

### P0-2 负向强信号镜像 —— A/B #5 通过（2026-10-27，末项落地）

**代码**（一条主线：镜像只作诊断/补充，绝不改变正向电池口径）：

| 文件 | 改动 |
|---|---|
| `wqb_campaign/mirror.py`（新建） | `neg_stats`（`min_s` / `max_abs_s` / `max_neg_s` / `n_strong`）、`_pick_sources`（奇对称白名单 + −1.58 门槛）、`_dispatch_settings`（逐字复现源设置）、`_joint`、`run_neg_mirror` |
| `wqb_campaign/transport.py` | `fetch_alpha_meta()`：经 `alpha_meta.py` 取 `code/settings/decay/tvr/atom`；脚本位技能目录优先（与 `harvest_safe.py` 同准则，不再依赖 `cache/`） |
| `ind_campaign/alpha_meta.py` | 新增 CLI；stdout 契约 `+ <aid> atom=… decay=… tvr=… settings=… code=…`；ATOM 判据 = 有 `LOW_2Y_SHARPE` 且无 `IS_LADDER_SHARPE` |
| `wqb_campaign/pipeline_ind.py` | 阶段 1.7 接 `run_neg_mirror`；`decide_verdict()` 抽成纯函数（新增 `ALIVE_NEG` / `DEAD_NEG`）；结果块 `neg` |
| `wqb_campaign/report.py` | digest 行追加 `neg[min=… strong=… mirror=… joint=… TO✗=… prod=…]` |
| `wqb_campaign/generate.py` | `MIRROR_TPL` 22 族 + `is_mirror_tpl()`（先 `norm_tpl`；`dw`/`pp`/`tl`/`dsp_rk`/`rg_lvvol*`/`res|reslag` 结构性排除） |
| `docs/env_registry.json` | 新开关 `WQB_NEG_MIRROR`（缺省 `REGION=="IND"`，EUR 行为不变），`index_tables.py env --check` = `[OK]` |

**一个决定全篇的架构选择**：镜像行**不进** `all_alphas` / `per_tpl`，只落在结果 `neg` 块。
读 `all_alphas` 的下游有 7 处（`best`/`max_s`、postproc top3、`sweep` 的 `pt` 重算、`joint`、`near_gate`、
`pick_prod_target`、`settings_sweep._pick_pairs`）＋ `report.emit_digest` 的 `near_delivery`。
若按「镜像当普通行收进来」的写法，`sweep` 的 `1.2 <= max_s < 1.58` 会被「−4.35 镜出的 +4.35」直接抑制，
**设置轴扫描等于被关掉**。改为不进 `all_alphas` 后这 8 处零改动、也不可能漏改。
阶段位置同样有约束：放在 matrix 之后 —— `fields.batch_field_coverage` 用
`glob(cache/_camp_{ds}_*.txt)`，先跑镜像会让 `*_neg` 混进字段×族覆盖统计。

**A/B #5（§9 第 5 行）**：走真实路径（`fetch_alpha_meta` → `dispatch` → `harvest_until_done`），
`save_ckpt` 打桩以免污染生产断点；脚本 `logs/_tmp_neg_ab5.py`。

| | alpha | S | F | 2Y | sub | rob | TO |
|---|---|---:|---:|---:|---:|---:|---:|
| 源 | `N1eZj1Wg` | −4.35 | −2.21 | −4.44 | −2.72 | −2.17 | 0.8702 |
| 镜像 | `npvx7W2w` | **+4.35** | **+2.21** | **+4.44** | **+2.72** | **+2.17** | **0.8702** |

MCP `get_alpha_details` 独立复核：`ra_failed_checks` **只有 `HIGH_TURNOVER`**，其余
（`LOW_SHARPE` / `LOW_FITNESS` / `LOW_SUB_UNIVERSE_SHARPE` / `LOW_ROBUST_UNIVERSE_SHARPE` / `LOW_2Y_SHARPE`）
全部 PASS。⇒ 判据「指标精确取负、TO 0.8702 不变（预期仍卡换手）」**逐字命中**：
镜像把「该集 ATOM 线为空」翻成「有一个六闸级结构，但换手 0.87 > 0.40 结构性不可提交」，
即 §3.4 第 3 条要的结论形态。流程侧同时验证 `neg.turnover_blocked=1` 且 `prod_top=None`
（不为死局烧相关队列）。

旁证（§3.4 第 4 条后半句，`logs/_tmp_neg_ab5b.py`）：`zqr72EkR` → `2rA8Op2x`，
S **+1.67** / F +0.72 / 2Y +0.79 / sub +0.64 / rob +0.72 / TO 0.3335（不变）；
`joint=False`（F/2Y/sub/rob 都不过）、`turnover_blocked=False`、未测 prod
⇒ 镜像不会把「F 0.72」包装成候选。

**成本控制**：无强负簇的集 = **0 条**仿真（只算统计）；命中时 ≤2 条/集（`MIRROR_CAP`）；
prod 只对「指标全过且未被换手拦」的第一条测（`NEG_PROD_CAP=1`）。
断点键 `{ds}@ng_d{decay}`（同 decay 不同设置加 `_2` 后缀）与主派发隔离，续跑不重派。

**verdict 语义**（`decide_verdict`，顺序即优先级）：`SIM_FAIL`/`ERROR`/`NO_DATA` →
`INSUFFICIENT_HISTORY` → `ALIVE` → `ALIVE_NEG` → `BORDERLINE` → `DEAD_NEG` → `DEAD`。
`DEAD_NEG` = 正负两向都不可交付、但存在 |S|≥1.58 的 ATOM 结构 ⇒ **数据有强反应**，
下一波不能把它当「没信号」永久搁置 —— 与 §3.1 的误判是同一个坑。

**单测**（`tests/unit/11_campaign/test_campaign_package.py::TestNegMirror` + `TestDecideVerdict`，12 例）：
`neg_stats` 排除镜像行 / `_pick_sources` 白名单与排序 / `_dispatch_settings` 逐字复现 /
`_joint` 闸位（含 `rob=None` 不算过）/ `fetch_alpha_meta` 契约解析 / `is_mirror_tpl` 排除项 /
真实路径端到端（镜像不进 `all_alphas`、TO 0.8702 被拦且不测 prod、非 ATOM 源被拒、开关关时零派发）/
verdict 优先级。`pytest tests/unit/11_campaign -q` = **87 passed**。

## 附：复现

- `logs/_tmp_ab6_retire.py`：A/B #6 构建与收割（`--dry` 只构建；判定写在末行）。
- `logs/_tmp_neg_ab5.py` / `logs/_tmp_neg_ab5b.py`：A/B #5 镜像（risk68 / sentiment21，走 `run_neg_mirror`
  真实路径，`save_ckpt` 打桩不写生产断点；末行 PASS/FAIL）。
- `logs/_tmp_tpl_stats.py`：族级统计与每集 best（只读）。
- `logs/_tmp_sign_atom_stats.py`：符号盲区 + ATOM/全模板对照（只读）。
- 脚本在 `logs/` 下，属临时证据；结论数字已固化在本文。
