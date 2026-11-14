# `vRAgNK3w` 四条改进方向 —— 实证验证报告

日期：2026-11-13 17:0x（GMT+8）｜状态：**未提交**｜共 3 批 30 条仿真 + 6 次只读预检 + 2 次 prod 实测 + 2 次 self + 6×6 互相关 + holdout 探针

> 来源：上一轮 `vRAgNK3w_forum_template_survey_20261113.md` 给出的四条改进方向。本轮**实际派批验证**，不是纸面建议。
> 基线：`group_rank(add(ts_mean(rsk70_mfm2_euetrd_anlystsn,504), multiply(ts_delta(rsk70_mfm2_euetrd_anlystsn,22), 0.18)), country)`
> 设置冻结：EUR / TOP2500 / delay1 / decay4 / SUBINDUSTRY / truncation 0.08 / nanHandling ON。

## 0 一句话结论

**四条方向全部实测：三条被否，一条（换 `ts_av_diff`）只做到「指标略厚、全闸通过」，但没有解决任何实质问题 —— 不正交（ρ≈0.99）、不改善近端衰减（holdout 0.63 vs 0.60）、不抬高预期 OS（0.66 vs 0.65）、prod 三颗齐平（0.6745 / 0.6788 / 0.6768）。维持 `vRAgNK3w` 为「补位候选」的原判，不建议为这四条方向改排序。**

| 方向 | 裁决 | 关键证据 |
|---|---|---|
| ① 快腿换 `last_diff_value` / `kth_element` | ❌ 否 | 5 条全崩到 S 0.52–1.48；`last_diff` 的 22 日与 250 日窗**逐位相同** ⇒ 快腿常数化，退化成纯慢腿 |
| ① 快腿换 `ts_av_diff` | △ 部分有效 | 收敛出 2 颗真全闸件，但见下「净收益」 |
| ② 快腿换低占用字段 / 两腿分组交叉 | ❌ 否 | 5 条 S 1.40–1.54、F 0.62–0.71，全掉 `LOW_FITNESS` |
| ③ 主信号换低 `alphaCount` 字段 | ❌ 否 | `market` S=0、`earnvar` −0.43、`cntadj` −0.23、`newssent` 0.92 ⇒ 504 日 `anlystsn` 慢腿是承重件 |
| ④ 等权 / 先验标准权重 | △ 部分有效 | 等权在原骨架与 `last_diff` 骨架全掉闸；`w=0.30` 配 `av_diff22` 全闸通过，但权重仍是网格挑的，`prior` 三问未解决 |

## 1 方向①：快腿算子替换（批 1，10 条）

论坛 `43412170117527`（25 赞）点名 `rsk70_mfm2_euetrd_anlystsn` 是阶梯字段，声称 `ts_delta` 会「测到 0 而非真实变化」，正解 `last_diff_value` / `kth_element` / `ts_av_diff`。

| 变体 | alpha | ops | S | F | 2Y | sub/lim | 未 PASS |
|---|---|---:|---:|---:|---:|---|---|
| `subtract(F, last_diff_value(F,22))` w.18 | `rK7XqLEj` | 6 | 0.52 | 0.17 | −0.27 | 0.29/0.27 | SHARPE / FITNESS / 2Y |
| 同上窗 250 | `MP6mEXqn` | 6 | **0.52** | **0.17** | **−0.27** | 0.29/0.27 | 同上（**逐位相同**） |
| `ts_av_diff(F,22)` w.18 | `j2ampXXE` | 5 | 1.82 | 0.92 | 1.59 | 1.00/0.95 | 仅 FITNESS |
| `ts_av_diff(F,250)` w.18 | `RReWOYYd` | 5 | **2.18** | **1.21** | **1.84** | 1.09/1.13 | 仅 SUB |
| 双 `kth_element` w.18 | `6XMOW11G` | 7 | 1.48 | 0.68 | 1.43 | 0.80/0.77 | SHARPE / FITNESS / 2Y |
| 单 `kth_element` w.18 | `wpogd1zp` | 6 | 1.40 | 0.62 | 1.34 | 0.78/0.73 | 同上 |
| `ts_delta(F,5)` 短窗对照 | `omaObvzv` | 5 | 1.67 | 0.81 | 1.55 | 0.90/0.87 | FITNESS / 2Y |
| `last_diff22` w.25 | `E5QJjbaR` | 6 | 0.54 | 0.18 | −0.27 | 0.30/0.28 | 三项 |
| `last_diff22` 等权 | `KPgao681` | 5 | 0.62 | 0.22 | −0.25 | 0.32/0.32 | 三项 |
| `ts_av_diff(F,66)` w.25 | `wpogd1J1` | 5 | 2.08 | 1.13 | 1.68 | 1.00/1.08 | 仅 SUB |

**★ 反证论坛推论**：`last_diff_value` 的 22 与 250 日窗结果逐位相同（S/F/TO/2Y/sub 全部一致），说明「真实变化」这一腿几乎恒为常数，表达式退化为纯慢腿（S 0.52）。而原版 `ts_delta` 腿把 S 从 0.52 抬到 1.93 —— **这条腿在本字段、本窗口下有实质信号贡献，不是 0**。论坛那篇的警告适用于「250 日窗量今天 vs 250 天前」的长窗情形，不能外推到 22 日窗。这条是本轮最有价值的机制修正。

**唯一存活**：`ts_av_diff(x,d) = x − ts_mean(x,d)`（忽略 NaN）。它给出一条清晰的 **F ↔ sub 权衡**：短窗 22 保住 sub 比值 0.5495 但 F 只有 0.92；长窗 250 把 F 推到 1.21 但 sub/S 掉到 0.50（限 0.5206×S）。

## 2 方向②③④：换字段、分组交叉、标准权重（批 2，10 条）

| 变体 | alpha | S | F | 2Y | 未 PASS |
|---|---|---:|---:|---:|---|
| 快腿 `newssent`（αCnt 32,830） | `E5QJj0QP` | 1.54 | 0.70 | 1.29 | SHARPE/FITNESS/2Y |
| 快腿 `earnvar`（18,613） | `ZYaG8wX3` | 1.42 | 0.64 | 1.47 | 同上 |
| 快腿 `market`（16,208） | `KPgaoYVx` | 1.40 | 0.62 | 1.34 | 同上 |
| 两腿交叉 sector × country + `newssent` | `N1P9dWKp` | 1.52 | 0.71 | 1.61 | SHARPE/FITNESS |
| 两腿交叉 + `last_diff` | `akav02RR` | 1.47 | 0.69 | 1.17 | 三项 |
| 主信号 `market` | `d5aLM89J` | **0.00** | — | — | 六项全掉（信号为空） |
| 主信号 `earnvar` | `omaObwR5` | **−0.43** | −0.14 | −0.39 | 三项 |
| 主信号 `newssent` | `rK7Xq69J` | 0.92 | 0.26 | 0.81 | 四项 |
| 主 `market` + `last_diff` w.25 | `6XMOWPZp` | **0.00** | — | — | 六项全掉 |
| 主信号 `cntadj`（17,649） | `leaXn6E5` | **−0.23** | −0.07 | −0.16 | 四项 |

**结论**：论坛「换低占用字段降 prod」在本骨架上不可行 —— 这些 `rsk70_mfm2_euetrd_*` 是慢变暴露/风格因子，504 日均值几乎没有横截面区分度（两颗直接 S=0）。`anlystsn` 的 504 日水平腿是**承重件**，不能替换；「两腿分组交叉」（`44713280965527` 的铁律）也没能救回 F。方向②/③实证否掉。

## 3 批 3：`ts_av_diff` 窗 × 权重收敛（10 条）

| 窗 / 权重 | alpha | S | F | 2Y | sub/lim | sub/S | 未 PASS |
|---|---|---:|---:|---:|---|---:|---|
| 33 / 0.18 | `rK7XqMGo` | 1.89 | 0.98 | 1.67 | 1.02/0.98 | .5397 | FITNESS |
| **44 / 0.18** | **`P059RmzM`** | **1.95** | **1.02** | **1.71** | **1.03/1.01** | **.5282** | **全 PASS** ✅ |
| 88 / 0.18 | `Xga63Azx` | 1.99 | 1.05 | 1.68 | 0.99/1.03 | .4975 | SUB |
| 126 / 0.18 | `2r5dgoW8` | 1.99 | 1.06 | 1.78 | 0.98/1.03 | .4925 | SUB |
| 189 / 0.18 | `d5aLMrog` | 2.08 | 1.13 | 1.84 | 1.02/1.08 | .4904 | SUB |
| 44 / 0.25 | `QP0XxpgQ` | 2.03 | 1.09 | 1.68 | 1.03/1.05 | .5074 | SUB |
| 88 / 0.25 | `VkNJrb5G` | 2.11 | 1.15 | 1.73 | 0.99/1.10 | .4692 | SUB |
| **22 / 0.30** | **`Wjl8Z20O`** | **2.02** | **1.08** | **1.69** | **1.08/1.05** | **.5347** | **全 PASS** ✅ |
| 慢腿 `ts_zscore` 替换 | `YPaqVoJJ` | 1.24 | 0.62 | 0.18 | 0.43/0.64 | .3468 | 四项 |
| 外层 `group_zscore` 替换 | `Xga63Aex` | 1.39 | 0.69 | 1.15 | 0.61/0.72 | .4388 | 四项 |

**窗口 44 / w0.18 与窗口 22 / w0.30 是仅有的两个「F≥1.0 ∧ sub/S≥0.521」交点**。两者都是 5 算子，与基线同算子数。再次印证 sub 是比值闸：窗 ≥88 时 S 越高，sub 限值同比抬高，反而过不了。

## 4 两颗全闸件的完整闭环

| 项 | 基线 `vRAgNK3w` | `P059RmzM` | `Wjl8Z20O` |
|---|---:|---:|---:|
| 快腿 | `ts_delta(F,22)×0.18` | `ts_av_diff(F,44)×0.18` | `ts_av_diff(F,22)×0.30` |
| 算子 | 5 | 5 | 5 |
| S / F | 1.93 / 1.01 | 1.95 / **1.02** | **2.02 / 1.08** |
| 2Y / sub(lim) | 1.66 / 1.01(1.00) | **1.71** / 1.03(1.01) | 1.69 / 1.08(1.05) |
| **prod（余量）** | **0.6745（.0255）** | 0.6788（.0212） | 0.6768（.0232） |
| self（本地） | 0.2062 | **0.1994** | 0.2015 |
| ΔSharpe | +0.28 | +0.29 | +0.31（`EUR:1:POWER_POOL`） |
| `submit_gate` | passed / failed_ra=0 | passed / 0 | passed / 0 |
| `mix_audit` | two_leg（需三问） | two_leg（需三问） | two_leg（需三问） |
| 稳健 | CONDITIONAL（CV .550） | **PASS**（CV .465） | CONDITIONAL（CV **.604**） |
| holdout 2019/20/21/22 | .82/.90/**.60**/.83 | .83/.95/**.63**/.85 | .78/.88/**.58**/.81 |
| 预期 OS（账户先验 ×.34） | 0.65 | 0.66 | 0.68 |
| 塔 | EUR/D1/RISK 2→3 | 同左 | 同左 |

**读法**：`P059RmzM` 在 F、2Y、self、ΔS、稳健 CV 上略优，`Wjl8Z20O` 在 S/F 上更厚；但差异全在噪声带内，两颗都没有改变上一轮判定的三个弱点。

**★ prod 的一处口径修正**：三颗 prod 实读为 **0.6745 / 0.6788 / 0.6768**，几乎完全相同。此前在同族 `ts_delta` 骨架里观察到的「权重越大 prod 越高」（w 0.18→0.6745、w 0.40 market→0.794）**不能外推到换了快腿算子的骨架**：这里 w 从 0.18 抬到 0.30，prod 只动 0.0023。⇒ prod 的主控变量是**字段拥挤度**（`anlystsn` alphaCount 115,082、userCount 2,445，risk70 全族最高；论坛 `42451774058007` 亦持此说），不是权重。四颗全闸件的 prod 余量都只有 0.021–0.026，属同一贴线带。

### 4.1 同席：不是新信号

6 颗变体 4 年日收益互相关 **0.9447–0.9923，最大独立集 = 1**：

| 对 | ρ |
|---|---:|
| `vRAgNK3w` ~ `P059RmzM` | **0.9912** |
| `vRAgNK3w` ~ `Wjl8Z20O` | **0.9883** |
| `P059RmzM` ~ `Wjl8Z20O` | 0.9916 |
| `vRAgNK3w` ~ `RReWOYYd` | 0.9479 |

⇒ 换快腿只是**同一个信号的重参数化**，不产生篮子正交增量；三颗只能留 1 颗。

### 4.2 近端衰减：唯一的改善在掉闸的那一颗

`tools/os_decay_probe.py` 四切点 Test/Train 比（列 = Test 起始年）：

| alpha | 2019 | 2020 | **2021** | 2022 |
|---|---:|---:|---:|---:|
| `vRAgNK3w` | .82 | .90 | **.60** | .83 |
| `j2ampXXE`（av22） | .83 | .96 | .61 | .85 |
| **`RReWOYYd`（av250）** | **.88** | **.98** | **.76** | .81 |
| `wpogd1J1`（av66 w.25） | .76 | .86 | .60 | .77 |
| `P059RmzM` | .83 | .95 | .63 | .85 |
| `Wjl8Z20O` | .78 | .88 | .58 | .81 |

**长窗 `ts_av_diff(250)` 确实把 2021 切点从 0.60 抬到 0.76**（预期 OS 0.74），但 `RReWOYYd` 的 sub 1.09 < 限 1.13，`submit_gate` 实测 `blocked=True, failed_ra=1`（`LOW_SUB_UNIVERSE_SHARPE` 硬门）。**能过闸的两颗，衰减一点没改善；能改善衰减的那颗，过不了闸。** 这是本轮最干净的一处结构性死结。

### 4.3 塔

`get_pyramid_alphas` 当季 `EUR/D1/risk = 2`（未亮）⇒ 交任一颗 2→3 **点亮，边际 +1**，与基线完全相同，不是新增收益。倍率 `EUR/D1/RISK = ×1.0` 仍为 EUR D1 垫底。三颗同席，第二颗起塔增量归零。

## 5 净结论与建议

1. **四条方向验证了「论坛建议 ≠ 本骨架可用」**。最反直觉的一条：`last_diff_value`/`kth_element` 把信号打死，反而证明原 `ts_delta` 腿有效；论坛关于阶梯字段的警告不能照搬。
2. **没有一条方向解决用户上一轮关心的 OS 坍塌问题**：全闸件 holdout 0.63/0.58 vs 0.60，预期 OS 0.66/0.68 vs 0.65，全部同席 ρ≈0.99，prod 也齐平在 0.675 附近。换快腿算子只搬动了 F 与 sub 之间的权衡，没有触碰信号本体。
3. **`prior` 三问仍未解决**：`w=0.18`、`w=0.30`、窗 44/22 都是本轮 30 条网格里挑出来的，回答不了「回测前由逻辑钉死」。换到 0.30 只是让数字更像标准值，审计性质没变。
4. **维持排序不变**：`vRAgNK3w` 仍是「补位候选」，篮子里 `wpo8olA6`（DEU OTHER ×1.8）/ `omEdka3v`（GBR OTHER ×1.6）/ `ZYQ116ln`（KOR PV ×1.4）优先级更高。若三颗高倍率件已交、要补第 4 席 Quantity，`P059RmzM` 可作为 `vRAgNK3w` 的等价替代（稳健 PASS 略好），但**不构成升级**。
5. **若继续挖这一族**，别再扫 w/窗口：唯一有实证希望的路线是让 `av_diff(250)` 的 sub 过闸（例如换 sub-universe 结构或引入快腿显著度过滤），而不是继续在 F↔sub 之间挪。除此之外建议换数据集。

ET 2026-11-13 04:02：REGULAR **0/4 剩 4**、SUPER 0/1。**本轮未提交任何 alpha。**

## 6 工程记录

- **`kth_element` 的 `k` 必须命名传参**：`kth_element(F,250,1)` 被 `op_arity.ensure_safe_for_dispatch` 拦下（`[KWARG] k 必须命名传参`，否则平台回 `Required attribute "k" must have a value` 并**连坐 CANCELLED 整批**）。正确写法 `kth_element(F,250,k=1)`。
- 三批均先单独写 `results/op_coverage_signoff.jsonl` 再派发（G6 在 PreToolUse 检查，写签核与派发放同一条 `&&` 命令会被拦）。覆盖率分别 10.7% / 8.3% / 8.3%。
- 判闸一律逐项查 `result == 'PASS'`：`RReWOYYd`、`j2ampXXE` 的 `fails=[]` 但 `submit_gate` 实测 BLOCKED（模拟层 WARNING 在提交层升级 FAIL）；`LOW_FITNESS` / `LOW_SUB_UNIVERSE_SHARPE` 都会降级 WARNING。
- `Wjl8Z20O` prod：带锁 22 次探测 / 243s 全 `pending`（`platform_retry_after=1.0` 是平台无效值），按纪律**不重触发**，改一次无锁 `--peek`，**11 秒后出数 0.6768**。再次印证 11-10 的经验：触发一次后停手、用 peek 低频等，比反复重触发有效。
- 三颗 prod 实读值均已 `set_corr_cache` 入权威表且 `source='prod_peek'`（vRAgNK3w 0.6745 @14:35、P059RmzM 0.6788 @16:57、Wjl8Z20O 0.6768 @17:06）；两颗新件稳健台账已写入 `ledger_kv`（`robustness_P059RmzM` = PASS、`robustness_Wjl8Z20O` = CONDITIONAL）。

## 7 产物

| 文件 | 内容 |
|---|---|
| `results/batch_vRAgNK3w_fix{1,2,3}_*.txt` | 三批 30 条表达式 |
| `results/_vRAgNK3w_fix_batches.json` / `_fix_b3.json` | 逐条指标与逐项闸门 |
| `results/_vRAgNK3w_fix_holdout*.json` | 多切点 holdout 与账户 OS 先验 |
| `results/prod_wait_P059RmzM.json` / `prod_peek_Wjl8Z20O.json` | prod 实读落盘 |
| `tools/os_decay_probe.py` | 上一轮建的可复用探针（本轮直接用） |
| `output_report/vRAgNK3w_forum_template_survey_20261113.md` | 四条方向的来源 |

---

# §8 追加：17:44 用户点名提交 `P059RmzM` ⇒ ACTIVE（未重复提交）

用户在 17:57 再次发出同一指令；幂等复核确认 17:44 已提交成功，**未重复 POST**。

| 项 | 值 |
|---|---|
| alpha / 名称 | `P059RmzM` / `EUR_R_risk70_levelchange_01` |
| 状态 | **ACTIVE**，`stage=OS`，`type=REGULAR`，BLUE |
| dateSubmitted | 2026-11-13T04:43:47-05:00（ET） |
| 提交路径 | `201 async_accepted → verify ACTIVE` |
| `submit_gate` | passed / `failed_ra=0` / `failed_ppa=0`；稳健 PASS |
| `prod_snapshot` | 闸门 0.6788 / 平台冻结 0.6788，**delta 0.0**（终验闭环） |
| 平台回填 self / prod | **0.2146** / 0.6788（本地 self 0.1994，以平台为准） |
| ΔSharpe | +0.29（`EQUITY:EUR:1:POWER_POOL`），`dilutive=false` |
| 配额 | ET 11-13 **REGULAR 1/4，剩 3** |
| tags | `CH_REG` / `SRC_risk70` / `W20261113`（`PowerPoolSelected` 已清） |
| `os.checks` | 全 PENDING，真 OS 待出 |

**三问 `prior` 如实答「否」**：`mix_audit two_leg` 要求回答 holders / polarity / prior，其中 prior 问「组合方向与权重是否在回测前钉死」。本件 w=0.18 与窗 44 来自本轮 30 条网格，因此答案明确写为「否，不能如实答是……属于参数拟合，此为本件已知缺陷」。闸只校验每条 ≥8 字符、不做语义判定，故 `narrative_ok=true` 放行；**这不等于官方 overfitting 口径合规**。同一披露已写进三段式 description 第三段（含 holdout 2021 切点 0.63、预期 OS ≈0.66、CLUSTER_TEST 1.04 WARNING）。

**平台在提交后自动追加 `PowerPoolSelected`**（与 11-11 `9qlZLVNd` 相同形态，节点本次只记录未清）。已按「只认 RA」政策用 `set_alpha_properties` 移除；复核 tags 恢复三条、`type` 仍 REGULAR、`ppa_channel=false`。注意该工具必须同时带完整 descriptions，否则报 `descriptions cannot be the literal string 'None'`。

## ★ 塔计数未按预期点亮（如实记录）

提交前预测 `EUR/D1/RISK` 2→3 点亮。实测：

- 提交后 17:46 与 17:5x 两次 `get_pyramid_alphas` 复查，EUR/D1 `risk` **均为 2**，与提交前一致；
- 平台返回 `ra.pyramid_short = "risk"`、`MATCHES_PYRAMID effective=1 / multiplier=1.0`、归属仍是 `EUR/D1/RISK`；
- OS 池前 50 颗中带该归属的只有本次 `P059RmzM` 一颗。

⇒ **不能宣称这次点亮了新塔**。可能原因：塔计数按季度/按已通过 OS 的 ACTIVE 口径异步刷新，或本次归属尚未计入；需次日复查。倍率 ×1.0 本就是 EUR D1 垫底，即使计入，真实收益也只是计数 +1，不影响「本件不是高质量新增信号」的判断。

**本地库已对齐**：`alphas.status=ACTIVE` + prod 0.6788 / self 0.2146 回填；`submission_ledger` 补记 EUR / REGULAR / ACTIVE / quota_used=1。
