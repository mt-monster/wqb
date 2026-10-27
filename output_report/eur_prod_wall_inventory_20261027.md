# EUR 战役盘点：瓶颈已从「S/F/2Y 不够」转为「prod 墙」

> 2026-10-27 ｜ 覆盖 `sentiment26` / `sentiment27` / `model25` / `model31` / `techindi_model` / `dl_riskfree_returns` 六条线
> 全部数据均为平台判定（`get_alpha_details` 的 `is.checks[]`）+ `check_correlation(refresh=...)` 实测

---

## 0 一句话结论

**EUR 已经能稳定产出「过完所有 IS 闸 + self 闸」的候选（今天 3 颗），但 prod 普遍落在 0.75–0.91（门槛 0.70）。**
瓶颈不是结构、不是窗口、不是字段选择，而是**该区域生产池对这类信号的覆盖已经饱和**。

---

## 1 六颗候选的最终状态：全部封闭

| # | alpha | 数据集 | code（缩写） | S | F | 2Y | sub | rob | self | **prod** | 死因 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `JjejYA3e` | sentiment26 | relpopularity1 + dw(3,66) + gate .85 | 1.60 | 1.18 | 1.92 | 1.21 | 0.98 | 0.275 | **0.7534** | prod |
| 2 | `vROPXLNa` | techindi_model | `signed_power(rank(bf(tm_16_r1_r5_r10_rh_glb_d1_r5_q1,22)),0.7)` | 1.91 | 1.25 | 2.05 | 1.36 | 0.91 | — | **0.8511** | prod |
| 3 | `VkdeWGgw` | dl_riskfree_returns | `signed_power(rank(bf(quantile_label_1bucket_5day_ohlcv_2,22)),0.7)` | 1.69 | 1.00 | 1.51⚠ | 0.97 | 1.08 | — | **0.9114** | prod |
| 4 | `kqJAPA2l` | model25 | `signed_power(rank(bf(mdl25_6v,22)),0.5)` | 1.85 | 1.28 | 1.58 | **0.87**/0.99 | 0.94 | 0.467 | 未测 | **sub** |
| 5 | `9qE5Ld6r` | model31 | `signed_power(rank(bf(star_eq_region_rank,22)),0.7)` | 1.86 | 1.26 | 1.58 | **0.87**/0.99 | — | 0.470 | 未测 | **sub** |
| 6 | `RREJewKz` | other335 | `signed_power(dw(oth335_combined_all_region_hedge),0.9)` | 1.83 | 1.03 | 1.67 | 1.19 | — | — | **0.8290** | prod |

死因分布：**prod 4 颗、sub 2 颗、S/F/2Y 0 颗**。
（第 3 颗的 2Y 是 `WARNING 1.51`，非 FAIL，但未过 1.58。）

**注意第 1、2、3 颗的平台 `FAIL` 列表为空**（只有 corr PENDING）—— 这是 EUR 历史上第一次出现「IS 闸全清」的候选。

---

## 2 prod 墙是普遍性的，不是选字段的问题

| 候选 | 字段机制 | 生产池直方图（>0.7 的对手数） |
|---|---|---|
| `JjejYA3e` | 网络相对热度（另类数据） | 0.7–0.8：1 颗 |
| `vROPXLNa` | 技术指标模型分（tm_16_*） | 0.8–0.9：1 颗 |
| `VkdeWGgw` | OHLCV 分位标签 | 0.9–1.0：1 颗 |
| `RREJewKz` | 多区域对冲综合分 | 0.8–0.9：1 颗 |

**三种完全不同的机制、四颗不同的字段，prod 全部落在 0.75–0.91，且形态都是「单点对手」。**
⇒ 不是「选到拥挤字段」，而是**这类信号在 EUR 生产池里的整体覆盖已经饱和**。

已试尽的三条真降法（memory §6）：

| 路径 | 具体 | 结果 |
|---|---|---|
| 改读数 | gate 0.80–0.925 / WS 2,3,5 / WL 66,126 / decay 0–16 / trunc 0.02–0.08 / universe 5 档 | 唯一过 S 的形态就是它本身 |
| 换字段 | sentiment26 试 9/19、other335 试 5/5 | 同族 Δ≤0.012（机制地板） |
| 改时机 | `trade_when` × 4（同集字段门控保 ATOM） | S 崩到 1.32–1.50 |

---

## 3 `sub_universe` 是字段常数：7 条轴全否证

`kqJAPA2l` / `9qE5Ld6r` 的 S/F/2Y/rob 全过，唯一 FAIL 是 `LOW_SUB_UNIVERSE_SHARPE 0.87 / limit 0.99`。
`limit = 0.535 × S`（EUR 实测），故需 `sub/S ≥ 0.535`。实测：

| 轴 | 变体 | S | sub | **sub/S** |
|---|---|---|---:|---:|
| 基准 | CS1600 / decay4 / trunc.08 / FAST | 1.86 | 0.87 | **0.465** |
| decay | 8 / 16 | 1.85 / 1.84 | 0.86 | 0.462–0.467 |
| truncation | 0.04 | 1.85 | 0.86 | 0.465 |
| universe | TOP2500 | 2.02 | 0.69 | **0.342** |
| universe | TOP1200 | 0.92 | 0.56 | **0.609**（S 崩） |
| group_rank | subindustry | 1.57 | 0.75 | 0.478 |
| group_scale | subindustry | 1.87 | 0.83 | 0.444 |
| neutralization | MARKET | 1.62 | 0.74 | 0.457 |

**结论：`sub/S ∈ [0.44, 0.48]`，除 universe 剪刀差外没有任何轴能动它。**
「故意降 S 让 limit 跟着降」也不成立 —— S 降时 sub 同比例降，比值不变。
要过 sub 只能改信号本质（加腿 / 换字段），等同重新挖。

---

## 4 `F` 轴的 86% 本来就不可达（这是今天最大的流程收益）

由 `F = S^1.5 × sqrt(vol/0.125)`（TO<0.125）反解：

```
S_req(F=1.0) = S × (1/F)^(2/3)
```

EUR 130 个集里：有 (S,F) 的 72 个 → **62 个（86%）F 轴不可达**、10 个可达（核实 region 后 9 个是 EUR）。

| 可达集 | cat | maxS | maxF | S_req | 余量 | 现状 |
|---|---|---:|---:|---:|---:|---|
| model28 | MODEL | 1.58 | 1.32 | 1.31 | +0.27 | 2Y 1.10，无望 |
| **model25** | MODEL | 1.86 | 1.26 | 1.59 | +0.27 | sub 0.87 ✗ |
| **techindi_model** | OTHER | 1.91 | 1.25 | 1.65 | +0.26 | prod 0.8511 ✗ |
| **model31** | MODEL | 1.86 | 1.24 | 1.61 | +0.25 | sub 0.87 ✗ |
| sentiment26 | SENT | 1.54 | 1.12 | 1.43 | +0.11 | prod 0.7534 ✗ |
| other335 | OTHER | 1.83 | 1.02 | 1.81 | +0.02 | prod 0.8290 ✗ |
| dl_riskfree_returns | OTHER | 1.69 | 1.00 | 1.69 | 0.00 | prod 0.9114 ✗ |
| fundamental1 | FUND | 0.77 | 0.99 | 0.78 | −0.01 | S 0.77，无望 |
| other315 | OTHER | 2.91 | 2.39 | 1.63 | +1.28 | 2 年样本，无效 |

**工具已落地**：`tools/sreq_precheck.py`

```bash
python tools/sreq_precheck.py --region EUR              # 分级：REACHABLE / HOPELESS / NO_SF
python tools/sreq_precheck.py --region EUR --verify     # 用平台 settings 核实 region（剔除跨区污染）
python tools/sreq_precheck.py --region EUR --dataset model25,sentiment26
```

典型省时案例：`analyst45` 的 S_req **1.87** 对实测上限 1.40 ⇒ 一眼判死，而今天为此白跑 3 批仿真。

---

## 5 两条可复用的新杠杆（有边界条件）

### 5.1 `group_scale(subindustry)` = 2Y + rob 双杠杆

`mdl25_6v` 实测：2Y **1.60 → 1.92（+0.32）**、rob **0.94 → 1.11（+0.17）**、S 持平（1.86→1.87）。
代价：F **−0.10**（1.26→1.16）、sub/S −0.02。
⇒ 与 memory §4「group_scale 是 2Y 稳定器」一致，但幅度（+0.32）比记录（+0.23）更大。
**适用条件：2Y 缺口而 F 有余量。**

### 5.2 短窗 WS 与门控甜点**不可跨集复用**

| 集 | WS 2 / 3 / 5 | 结论 |
|---|---|---|
| sentiment26 | 1.54（ws5）→ **1.60（ws3）** | WS=3 有效 |
| sentiment27 | **全部 1.40**（三档完全一致） | WS 完全无效 |

门控同理：snt26 上 0.85 是尖峰（0.875 掉 0.16），但这是该字段的性质，不能外推。

---

## 6 工程修复（3 项）

**① `wait()` 单仿真分支缺失（严重）**
单条表达式建的是**单仿真**（`children=0` + `status=COMPLETE`），原逻辑只在 `kids` 非空时返回 `True`
⇒ COMPLETE 也继续 sleep，**空转 27 分钟**，仿真早完成却收不到结果。已在 8 个探针脚本统一修。

**② `results` 文件跨区共用**
`full_template_campaign_results.json` 里 130 个集，其中 **74 个与 GLB 同名**，无法靠集名判断归属。
实例：`predictive_starmine` 的 S 2.34 那颗实际是 **GLB**（MINVOL1M / decay 12 / STATISTICAL）。
判别口径：alpha 的 `settings.universe`（EUR 与 GLB 的 universe 集合**交集为空**）。
`sreq_precheck.py --verify` 已内置该判定。

**③ 日志应写 `logs/_run/`**
`tools/retention.py::collect_logs` 只扫 `logs/` 顶层，子目录免疫回收。

---

## 7 下一步建议

**A. 已落地**：`tools/sreq_precheck.py`（零仿真，对所有区域生效）。

**B. 换区复现同一机制**（推荐）
`sentiment26` 的 relpopularity 机制在 EUR prod 0.7534，是三颗里最低的，说明它**最不拥挤**。
GBR / KOR / IND 的生产池与 EUR 完全不同 ⇒ 同一机制在那些区域可能直接 <0.70。
这是「换区域降 prod」，而不是「换字段降 prod」—— 后者今天已证明无效（同族 Δ≤0.012）。

**C. EUR 停投信号**
若 B 也不成，EUR 应暂停常规挖掘，只在出现「新机制类别」时才回到该区。
依据：9 个 F 可达集里已有 6 个完成 prod 实测，全部 0.75–0.91；剩余 3 个是样本无效（other315）或 S 天花板不足（model28 / fundamental1）。
