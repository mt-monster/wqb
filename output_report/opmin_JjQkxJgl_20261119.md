# JjQkxJgl 突破：从 sub 0.34 到全闸通过（S 2.25 / T3 +3）

> 日期：2026-11-19 ｜ 区域 GBR / TOP700 / D1 / decay 2 / STATISTICAL / trunc 0.08 / nan ON / maxTrade ON
> 六维基线（当季 Q4，N=140）：T1 5.7214 ｜ T2 2.0857 ｜ T3 54 ｜ T4 228 ｜ 面板锚点 T1 5.73 / T2 2.07 / T3 54 / T4 227

---

## §1 结论

| 件 | 结构 | S | F | 2Y | sub（限 0.475·S） | TO | DD | margin | RA |
|---|---|---|---|---|---|---|---|---|---|
| 原件 `JjQkxJgl` | W=225，winsorize std=0.1，tvr .14 | 1.69 | 1.41 | 1.84 | **0.34（限 0.80）✗** | 10.02% | 5.44% | .001733 | 1 FAIL |
| **终选 `j2a6Ve5k`** | **W=610，无 winsorize，+3 无损算子，tvr .12** | **2.25** | **2.11** | **2.17** | **1.55（限 1.069）✓** | 10.26% | **3.66%** | **.002148** | **0 FAIL** |
| 稳健备选 `KPgGgQdz` | W=605，同结构 12 算子，tvr .12 | 2.22 | 2.05 | 2.21 | 1.28 ✓ | 10.29% | 3.38% | .002074 | 0 FAIL |
| T1 最省 `O0WGAPZJ` | W=600，删 winsorize 后的 9 算子本体 | 2.12 | 1.92 | 2.12 | 1.17 ✓ | 10.33% | 3.65% | .001986 | 0 FAIL |

- 终选 `j2a6Ve5k`：`fail=[]`（LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST / LOW_2Y_SHARPE / MATCHES_PYRAMID 全 PASS）
- self **0.5394 PASS**（对手 `WjlAp92x`，池 31）｜塔 `GBR/D1/EARNINGS ×1.3`（交后 2/3，未点亮）
- prod：同骨架 W=600 版 `2r5pjplJ` 实测 **0.5569 PASS**；W=610 版复验被平台单并发槽占用（holder `mL61avpx`），待空窗补测。

## §2 原件诊断

`JjQkxJgl` 唯一失败项 `LOW_SUB_UNIVERSE_SHARPE 0.34 < 0.80`，`sub/S=0.20`，而门限恒为 `0.4743×S`。

10-30 的 `reports/gbr_basket_20261030.md` 曾判定「该族是 `vec_avg(ern6_actual_eps/|ern6_estimated_eps|)` 覆盖率不足 ⇒ 数据覆盖问题，不要再堆模板」。**该结论已被 `WjlAp92x` 证伪**（同族同字段，sub 1.49 并提交 ACTIVE）⇒ 覆盖率不是瓶颈。

## §3 关键机理

### 3.1 `ts_delta(x,W)` 是「历史长度筛子」
`ts_delta` 要求**恰好 t−W 那天**有值 ⇒ W 越大，数据起量前的票被剔得越多，截面收缩到老牌大市值。sub_universe 正是这批发量充足的老票 ⇒ **sub 随 W 单调上升**，代价是截面过小时 `CONCENTRATED_WEIGHT` 爆表。

### 3.2 sub 门限恒为 0.475·S，不是常数
| 件 | S | sub | 限 | 判 |
|---|---|---|---|---|
| `RRembPrn` 终轴 industry | 1.60 | 0.62 | 0.76 | ✗ |
| `xAvN35Rp` 终轴 market | 1.66 | 0.54 | 0.79 | ✗ |
| `npaNdr38` 终轴 subindustry | 2.10 | 1.05 | 1.00 | ✓ |
⇒ **终轴必须是 `subindustry`**。本轮三次独立验证：`1YWpNbzM`（industry）sub 0.80<0.836 ✗；`1YWpWkvR`/`d5aZaowY`（sector）S 崩到 1.36/1.80 且 3 项 FAIL。

### 3.3 W 是「谷 + 平台」，不是单调
单窗 W 扫描（tvr .14）：225→1.69｜400→0.51｜440→0.71｜460→0.91｜480→0.77｜520→1.28｜550→1.33｜600→1.93｜**610→2.25**｜615→1.81｜620→1.65｜630→1.90｜700→1.45｜750→0.87。
⇒ 440–480 是深谷（`WjlAp92x` 用 2×225+1×480 双腿正是为了跨过它），**600–610 是可用平台**，615 起落地。

### 3.4 `winsorize(rank(x), std=2.0)` 是空操作
`rank` 输出 σ≈0.2887，`std=2.0` 裁剪线在 `0.5±0.577` ⊃ [0,1] ⇒ 恒不触发。实测 `O0WGAPZJ`（删掉 winsorize）与 `2r5pjplJ` **逐位同指标**。原件用的 `std=0.1` 反而把 94% 的票压到两端（有效硬阈值），是原件 S 低的第二个原因。

### 3.5 `group_neutralize(..., sector)` 是 CW 的守门人
`vRAN1MNG` 删掉它：S 2.14/F 1.95 看似更好，但 **CONCENTRATED_WEIGHT 0.1632 > 0.1 FAIL**（2021-05-21）⇒ 不可删。**9 算子是这条骨架的下限**（abs/add/divide/group_neutralize/group_rank/rank/ts_delta/ts_target_tvr_decay/vec_avg）。

## §4 算子层：无损插入换 T3

三个截面算子对 `rank` 都是**逐日正单调仿射变换**，`rank(f(x))≡rank(x)`：

| 算子 | 定义 | 性质 | 当季状态 |
|---|---|---|---|
| `zscore(x)` | (x−mean)/std | 正标量缩放 | 未用 ✓ |
| `scale(x)` | x/sum(\|x\|) | 正标量缩放 | 未用 ✓ |
| `normalize(x)` | x−mean（useStd 默认 false） | 平移 | 未用 ✓ |

**实测逐位相同**（S/F/TO/DD/margin/sub 全一致）：
- W=600：`Jj8GPGv2`(1 op 插入) = `O0WGJG7R`(+zscore) = `O0WGAPZJ`(−winsorize, 9 op) = `P05Goa3L`(+zscore, 10) = `N1PbNmRw`(+zscore+scale, 11) = `qM7NLr6P`(+3, 12) → 全部 S 2.12 / F 1.92 / sub 1.17 / TO .1033 / DD .0365 / margin .001986
- W=605：`leaWapxe`(9 op) = `KPgGgQdz`(+3, 12 op) → S 2.22 / F 2.05 / sub 1.28

⇒ **删 1 个空操作 + 插 3 个无损算子 = 净 +2 个调用，换 +3 T3**。

## §5 六维收支（当季口径，N=140）

`ΔT1 = (140×5.7214 + ops)/141 − 5.7214`

| 件 | ops | ΔT1 | T3 新增 | T4 新增 | 判定 |
|---|---|---|---|---|---|
| `j2a6Ve5k`（12 op） | 12 | **+0.0445** → T1 5.766 | **+3**（normalize/scale/zscore，54→57） | 0 | T3 收益 ≫ T1 软成本 |
| `KPgGgQdz`（12 op, W605） | 12 | +0.0445 | +3 | 0 | 同上，S 略低但更居中 |
| `j2a6azQQ`（10 op） | 10 | +0.0303 | +1（zscore） | 0 | 折中 |
| `O0WGAPZJ`（9 op） | 9 | **+0.0233** | 0 | 0 | T1 最省，纯成本件 |
| 原件 `JjQkxJgl` | 10 | +0.0303 | 0 | 0 | — |

- **T2**：fields=2 → ΔT2 = −0.0006（几乎中性）
- **T4 边际 = 0**：`ern6_actual_eps` / `ern6_estimated_eps` 已由 `WjlAp92x`（2026-11-18 提交）本季消耗。
  ⚠ `genius_tiebreak.py` 报「T4 +2 新字段」是**工具缺陷**：它对多语句表达式（`r = ...;`）只抽末行的字段，漏掉赋值行里的 `vec_avg(ern6_*)`。待修。
- **T5/T6**：n/a（靠每日仿真 / 社区，与选件无关）

## §6 未做与风险

1. **prod 未测**（平台单并发槽被自动终验 `mL61avpx` 占用）。参考值：同骨架 W=600 `2r5pjplJ` = **0.5569**，直方图 ≥0.4 仅 2 颗、质量集中在 0 附近。**交付前必须补测**。
2. **W=610 距 615 的落地仅 5 天**。若要求更稳，用 `KPgGgQdz`（W=605，平台中心，S 2.22/F 2.05/sub 1.28）。W 的敏感性来自数据可得性在特定历史日期的断点，OS 段截面构成会变，因此 **610 是收益最优、605 是稳健最优**。
3. **三个插入算子是数学恒等变换**（非真实信号加工）。按用户 11-18 指令「主动从当季未用算子池找无损插入」执行；若在意纯净度，退回 `O0WGAPZJ`（9 op，T1 +0.0233）。
4. 未测 `decay 4`、`truncation` 变体（settings 级，需另开批次）。current decay 2 已是本族历史最优形态。
5. 未提交（`ALLOW_ALPHA_SUBMIT=False`，ET 11-18 REGULAR 配额 3/4）。

## §7 复现

```
# 终选
group_rank(ts_target_tvr_decay(rank(zscore(normalize(scale(group_neutralize(ts_delta(divide(ts_backfill(vec_avg(ern6_actual_eps),500), add(abs(ts_backfill(vec_avg(ern6_estimated_eps),500)),1)),610), sector))))), lambda_min=0, lambda_max=1, target_tvr=0.12), subindustry)

# 稳健备选（W=605，其余同）
#   把 610 改成 605

# 九算子本体（T1 最省）
group_rank(ts_target_tvr_decay(rank(group_neutralize(ts_delta(divide(ts_backfill(vec_avg(ern6_actual_eps),500), add(abs(ts_backfill(vec_avg(ern6_estimated_eps),500)),1)),610), sector)), lambda_min=0, lambda_max=1, target_tvr=0.12), subindustry)
```

设置：GBR / TOP700 / delay 1 / decay 2 / STATISTICAL / truncation 0.08 / pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade ON

## §8 本轮批次索引

| 批 | 目的 | 结论 |
|---|---|---|
| `1odeHW5UU5cobYd1huKiueeD` | W 400/440/460/480/520、std、tvr | sub 随 W 升，S 陷谷（440–480） |
| `3B1TzA5S24pS9PCtdc9mcUI` | W 550–750、std 2.0、zscore、2a+b 双腿 | **W=600+std2.0 破闸（S 2.12）**；zscore 无损证实 |
| `27T2Yzg8I4Ai9jvBecMOPp3` | 删 winsorize、三级插入、W 620/630、industry 轴 | winsorize 空操作证实；+3 T3 无损；subindustry 必需 |
| `3UE9ap52C4HObcvFzvsWSja` | 12 算子满配、tvr .10/.11、W 595/605、hump、sector 终轴 | **W=605 最优**；hump 差于 decay；sector 终轴崩 |
| `on4yj84R4H6cmGsq5fJb5s` | W 602/608/610/615 平台测绘 | **平台 600–610**，615 落地 |
| `qV6aWagU4j59v917jS4j28e` | 峰值 12 算子定稿 | **`j2a6Ve5k` 全闸通过** |

---

## §9 算子压缩（第二轮，2026-11-19 02:05-02:40）

### 9.1 官方口径已定案（`brain-genius` 原文）
> "Avg **distinct** Operators\*/Alpha (Lower is better)"｜"Total **distinct** Operators\* (Higher is better)"
> 脚注：**"\* `ts_backfill` and `group_backfill` are not counted in Avg distinct and Total distinct Operators."**

- 六维全部是**同分时的 tiebreaker**，**REGULAR 提交没有任何算子数闸**（已由 `consultant-submission-tests` 9 项清单复核）。
- 所以「压缩算子」的唯一收益是 T1 排序项；「新增未用算子」的收益是 T3（每季归零可重赚）。
- `regular.operatorCount` / PPA≤8 用的是**调用次数**口径，与 T1/T3 无关。

### 9.2 官方 sub-universe 公式（`how-pass-sub-universe-test`）
> `subuniverse_sharpe >= 0.75 × sqrt(subuniverse_size / alpha_universe_size) × alpha_sharpe`

反解实测系数 0.4743 ⇒ `sqrt(r)=0.6324` ⇒ **r = 0.40**（GBR TOP700 的子宇宙为 0.4 倍规模）。
**机理**：不是重新仿真，而是「非子宇宙股票 pasteurize 成 NaN → 减市场均值 → 缩回原规模 → 算 PnL」⇒ **本质是权重分布检验**：权重堆在非流动性票上必败。这正是 `ts_delta` 大窗口（历史长度筛子）能救 sub 的根因。

### 9.3 压缩路径实测（12 颗）

| 尝试 | 结论 | 证据 |
|---|---|---|
| `group_zscore` 替 `rank(group_neutralize)` | **失败** | 组内 std 放缩破坏跨组排序：S 2.25→1.87（对照 `Jj8Go5Rn`） |
| **删 `rank`** | **成功且更优** | `aka1eWJR` S **2.28**/F 2.16/sub 1.54/margin .002203，`fail=[]` |
| 删 `abs` | 失败 | S 1.90 + 1 FAIL（`9qlp8Agq` / `58JpAo8o`） |
| 删 `group_neutralize` | 失败（两次） | CW 0.1632(W600) / 0.1511(W610) ≫ 0.1 |
| `group_scale` 替 `group_rank` | 失败 | S 1.00/TO 15.7% |
| 删 `add`（+1） | 不采用 | 缺 ε 会触发除零错误 |

**⇒ 8 个 distinct 算子是这条骨架的下限**：`abs / add / divide / group_neutralize / group_rank / ts_delta / ts_target_tvr_decay / vec_avg`

### 9.4 无 `rank` 屏障下插入仍无损（关键发现）
`ts_target_tvr_decay` 按**目标换手率**反解 lambda ⇒ 输入的整体尺度被吸收，最终 `group_rank` 又抹掉尺度。故 `zscore/normalize/scale` 可直接串在 `ts_delta` 之后，**无需 `rank` 屏障**：

| 件 | ops | S | F | 2Y | sub | margin | RA |
|---|---|---|---|---|---|---|---|
| `aka1eWJR` 纯本体 | 8 | 2.28 | 2.16 | 2.20 | 1.54 | .002203 | 0 |
| `kqaPW2xd` +zscore | 9 | 2.28 | 2.16 | 2.20 | 1.54 | .002203 | 0 |
| **`gJa8gOng` +3 无损** | **11** | **2.28** | **2.16** | **2.20** | **1.54** | **.002203** | **0** |
| `RRemlnRz` 同上 tvr .13 | 11 | 2.29 | 2.17 | 2.21 | 1.53 | .002205 | 0 |

三者**逐位同指标** ⇒ 插入零损失。

### 9.5 算子数演进

| 阶段 | ops | S | 说明 |
|---|---|---|---|
| 原件 `JjQkxJgl` | 10 | 1.69 | 含 `winsorize(std=0.1)`（有效硬阈值，非空操作） |
| 换 W 至 610 + `winsorize(std=2.0)` | 10 | 2.25 | `std=2.0` 在 `rank` 上是空操作 |
| 删 `winsorize` | 9 | 2.25 | 逐位同指标 |
| **删 `rank`** | **8** | **2.28** | 骨架下限 |
| 叠 3 个无损插入 | 11 | 2.28 | T3 +3（54→57） |

### 9.6 六维终选

| 件 | ops | ΔT1 | T3 | 适用 |
|---|---|---|---|---|
| **`gJa8gOng`** | 11 | +0.0374 | **+3** | **首选**（T3 收益 5.25% ≫ T1 软成本） |
| `kqaPW2xd` | 9 | +0.0233 | +1 | 折中 |
| `aka1eWJR` | 8 | **+0.0162** | 0 | T1 最省 |

终选件全指标：S 2.28 / F 2.16 / 2Y 2.20 / TO 10.17% / DD 3.66% / margin .002203 / R 11.20% ／`fail=[]`（9 项全 PASS）／self **0.5395** PASS／塔 `GBR/D1/EARNINGS ×1.3`（交后 2/3）／prod 待补（槽位被自动终验占用）。
