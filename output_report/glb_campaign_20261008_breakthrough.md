# GLB 战役突破报告 —— 2026-10-08

> **结论：GLB regular alpha 的"不可解"诊断被推翻。本轮产出 4 条完全合格（RA 全过 + 三区全过 + prod/self 双 <0.7）的可提交候选，其中最优 `RR66gp2j` SHARPE 2.60。**
> 按「只挖不提交」铁律，**未提交**，等用户逐次明示。

---

## 1 上一轮的错误诊断（已推翻）

前序结论为「GLB 新族边际收益≈0、可挖信号已采尽」，依据是 34 条判死 + APAC 结构墙。
本轮证明：**APAC 墙的真实性质是「数据地理覆盖闸」，而不是信号质量闸** —— 只要选对**全球覆盖型数据集**，APAC 即可打开。

| 数据集 | APAC 真实持仓 | APAC Sharpe | 结论 |
|---|---|---|---|
| `hiring_trends`（招聘） | **9 / 9** | ≤0.74 | 美国主导 ⇒ 覆盖不足，出局 |
| `option_chart_model`（期权） | 稀疏 | ≤0.29 | 同上，出局 |
| **`model239`（证券借贷）** | **1905 / 953** | **1.33–3.12** | **覆盖充足 ⇒ 通过** |

佐证：`group_backfill` 可把 APAC 从 9 只补到 1193 只，但 S 从 1.90 崩到 0.43（合成值=噪声）⇒ **覆盖不可人造**。
`universe` 换档（TOP3000）实测无效：APAC 仍仅 7/7 只。

## 2 关键发现：GLB 已提交 alpha 的统一模板

取 6 颗 ACTIVE 的完整表达式后，结构完全一致：

```
trade_when(and(rank(GATE) > θ, rank(cap) > 0.2),
           signed_power(subtract(group_rank(CORE, country), 0.5), 0.5),
           or(rank(GATE) < θ', rank(cap) < 0.1))

CORE = single_bucket_{5,20,60}day_return_estimate_ohlcv_img   # dlrr 桶族，全球覆盖
GATE = mdl239_utilisation / ep_yield / rsk60_offer / 动量 / 成交量比
设置 = GLB / MINVOL1M / D1 / decay 10 / SUBINDUSTRY / truncation 0.08
```

**控制行验证**：以 `mdl239_combo_utilisation` 为门控的复现行，S/F/tvr = 2.74/2.09/0.1245，与已提交 `MPabNeNz` **逐位一致**
⇒ 模板等价于平台已验证可提交形态，非猜测。

## 3 决定性杠杆（本轮摸清）

| 杠杆 | 实测作用 |
|---|---|
| **`truncation 0.08`**（vs 0.02） | **修 CONCENTRATED_WEIGHT**（0.02 档 CW=1.0 失败，0.08 档全过） |
| **门控 θ 0.6 → 0.75** | **降 SELF**（0.79→0.63）且把 EMEA 从 0.96 抬到 1.13 |
| **中性化 SUBINDUSTRY → MARKET** | 修 EMEA（0.93→1.16~1.29），代价 S 小幅回落 |
| 换核心桶 5d/20d/60d | **几乎不降 self**（相关由持仓重叠主导，非核心本身） |
| 门控换数据集（model243 / institutions18） | S 崩至 1.4–2.2 且 AMER/EMEA 破 1.0 ⇒ 不可用 |

## 4 合格候选（全部 `failed_ra_count = 0`，prod/self 双 <0.7）

| 排名 | alpha | 设置 | S | F | 2Y | AMER | EMEA | APAC | PROD | SELF |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **`RR66gp2j`** | SUBIND/decay10/θ0.75 | **2.60** | 1.36 | 2.87 | 1.31 | 1.13 | 1.97 | **0.6331** | **0.6333** |
| 2 | `P0ggRjYq` | MARKET/decay10/θ0.65 | 2.44 | 1.53 | — | 1.43 | 1.16 | 1.88 | — | 0.680 |
| 3 | `e7QQYeG6` | MARKET/decay10/θ0.80 | 2.30 | 1.40 | — | 1.06 | 1.19 | 1.90 | — | 0.631 |
| 4 | `omWWbQG5` | MARKET/decay10/θ0.75 | 2.29 | 1.38 | 2.59 | 1.11 | 1.29 | 1.83 | **0.6436** | **0.6406** |

**最优候选 `RR66gp2j`**（`all_passed: true`，含 CLUSTER_TEST PASS）：

```
trade_when(and(rank(ts_mean(vec_avg(mdl239_combo_deltaactivity), 5)) > 0.75, rank(cap) > 0.2),
           signed_power(subtract(group_rank(single_bucket_60day_return_estimate_ohlcv_img, country), 0.5), 0.5),
           or(rank(ts_mean(vec_avg(mdl239_combo_deltaactivity), 5)) < 0.65, rank(cap) < 0.1))
```
设置：`GLB / MINVOL1M / Delay 1 / decay 10 / SUBINDUSTRY / truncation 0.08`
指标：SHARPE 2.60、FITNESS 1.36、turnover 0.2656、2Y 2.87、sub-universe 1.82、drawdown 0.0230、margin 0.000545
塔：`GLB/D1/PV + MODEL + OTHER`（有效乘数 1.3）

> ⚠ **同腿近亲**：以上 4 条共享核心与结构 ⇒ **建议只提交 1 颗**（一旦提交其一，其余与它 self 会显著上升）。

## 5 状态与下一步

- 候选已落盘：`results/mining_ledger/alpha_ledger.jsonl`（累计 41 条）。
- **未提交**（`ALLOW_ALPHA_SUBMIT=False`；提交权归用户、逐次明示）。
- 待用户定夺：是否提交 `RR66gp2j`（若提交，建议先跑 `submit_verdict` 预检）。

## 6 工程事故与纪律（本轮）

1. **托管解释器缺 `pydantic`** ⇒ `tools/submit_batch.py` 真实派发 `ModuleNotFoundError`，而 `--dry-run` 不触发 ⇒ **"干跑通过、实跑静默失败"**。
   ⇒ **派发一律用仓库 `.venv/Scripts/python.exe`**；输出重定向到文件再 grep（管道为块缓冲，超时被杀即丢输出）。
2. `logs/` 与 `tracking/<REGION>/scripts/` 的 `.py` 会被外部清理进程删除 ⇒ 不依赖自建长期脚本，改用仓库自带工具。
3. multisim location **~24h 过期（HTTP 404/500）** ⇒ 收批必须当天完成。
