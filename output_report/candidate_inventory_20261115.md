# 近十天候选因子全量盘点与「是否还值得提交」重判 · 2026-11-15 13:20 GMT+8

> **只读评估，零提交。** 只认 REGULAR / RA 全闸；判序＝台账 REJECT/DEAD → 硬闸 → 指标 → 塔边际 → 排序分。提交权归用户点名，agent 不自行 POST。
> 窗口：2026-11-05 00:00 ~ 2026-11-15 13:20 GMT+8。池 = 进入过提交评估链路的 alpha（`submit_*` / `robustness_*` 台账、47 颗全量评估、可靠清单、全篮子、IND 候选篮子、11-14/15 交付与日志点名），**共 197 颗**。不含近十天约 1.7 万条纯回测扫描件。

> **【13:56 状态更新】首推件 `bla2k0Jq` 已由用户点名提交、平台落地 `ACTIVE`**（`dateSubmitted` = ET 2026-11-15 00:53:32；`USA/D1/OTHER` 当季 2→3 点亮）。本表排序与判据是 13:20 的快照，其余结论不变；下一顺位 `e7aeJoEd` → `omEdka3v`。`58J72oQN` 与已提交件同抢 `USA/D1/OTHER` 席，该席已点亮 ⇒ **塔边际归零**，叠加 prod 余量 .0103 贴线，维持不提交。ET 11-15 REGULAR 配额现为 **1/4（剩 3）**。审计留痕见 `reports/robustness_20261115.md`（verdict `CONDITIONAL`，无 REJECT）。
>
> **【15:14 追加】次顺位 `e7aeJoEd` 经 op-min 优化后由更优变体 `O0Wkvqgd` 取代并已提交 `ACTIVE`**（`ts_backfill 20→10`；S **2.45** / F **1.83** / 2Y **2.22** / prod **.4741** / self **.4741**，稳健 **PASS**，`IND/D1/EARNINGS` 2→3 点亮、`IND/D1/PV` 11→12）。原件 `e7aeJoEd` 与其余 11 个消融/参数变体全部标 `SUPERSEDED`（同骨架互相关 ≥0.99）。**ET 11-15 REGULAR 现为 2/4（剩 2）**；⚠ **SUPER 配额今日已被 KOR `KPg60XNp` 用掉 1/1（非本轮操作）**。详见 `output_report/opmin_e7aeJoEd_20261115.md`。

## 0 结论

**197 颗 → S1 硬闸全过 16 / S2 待动作 31 / S3 硬闸否决 86 / S4 数据不足 23 / S0 已提交 32 / SX SA 线 9。**

**「潜在可提交的」里，现在仍值得提交的只有 6 席（按顺位）**：

| 顺位 | alpha | 区 | 判定 | 决定性理由 |
|---:|---|---|---|---|
| 1 | **`bla2k0Jq`** | USA | ✅ 值得，首推 | prod **.5138**（余量 .186）/ self **.2094** / **4 ops** / ATOM 单塔 1.4 / 方案D 放行 / 点亮 `USA/D1/OTHER` 2→3。唯一待办＝补稳健审计声明 |
| 2 | **`e7aeJoEd`** | IND | ✅ 值得 | prod **.5124** / self .5074 / robust 1.91 / 点亮 `IND/D1/EARNINGS` 2→3（本轮唯一载体） |
| 3 | **`omEdka3v`** | GBR | ✅ 值得 | prod .6026（11-15 01:18 重测，12h）/ self 实测 .4164 / 稳健 PASS / 方案D 放行 / 点亮 `GBR/D1/OTHER` 2→3。待三问答复核 |
| 4 | **`qM7eZoVO`** | IND | ✅ 值得（同席第二） | prod .5018 / robust 1.62，但与 `e7aeJoEd` 同抢 EARNINGS 席（ρ .6965），**两颗只点一座** |
| 5 | **`rK7Qm6ld`** | IND | ✅ 值得（无塔增量） | prod .5634 / self **.2514** / 7 ops / 零待办；`SENTIMENT` 1→2 不点亮 |
| 6 | **`6XdkW08J`** | GBR | ✅ 值得（备选） | S2.60/F1.95 全场最厚，prod .6267（11-15 09:57，3.4h 最新）/ 稳健 PASS；待三问，塔增量 0 |

**不值得提交（形式过闸但实质否决）**：`58J72oQN`（prod .6897，余量 **.0103**，贴线）、`RREPm361`（.6881 / 余量 .0119）、`MP69RYAk`（prod .6699 + self .6585 双贴线）、`3qj1eYdz`（.6962 / .6976 双贴线，prod 池膨胀高危）、`LL5Edbee`（self .6338 余量 .066）。按 `ZYa6x531` 缓存 .6964 → 回源 .9229 与 `YPMvZZvv` .6958 → .9499 两条前例，**贴线件不占配额**。

**一篮最优 4 席（点亮 3 座不同塔，互不冲突）**：`bla2k0Jq` → `e7aeJoEd` → `omEdka3v` → `rK7Qm6ld`。若已持有 IND 篮则第 4 席换 `6XdkW08J`。

S1 第 7–14 名属**合规后备**（稳健待声明 / 三问待答 / 塔增量 0 / 同席让位），不占优先配额；第 10、12、15、16 名因贴线明确判「不值得占配额」。S2 的 31 颗当前一律不可提交。

## 1 本轮一手复核（不是照抄旧清单）

| 项 | 实读结果 | 影响 |
|---|---|---|
| **配额** | 平台 OS 最近提交 = `A1xJdOmg` ET **11-14 07:27**；ET 11-15 00:00 后零提交（GMT+8 13:00 已过重置点） | **ET 11-15 REGULAR 0/4，剩 4 席**（旧结论「ET 11-14 剩 2 席」已翻篇）；SUPER 1/日未用 |
| **塔计数**（`get_pyramid_alphas` 当季） | USA/D1/OTHER **2**、USA/D1/EARNINGS 2、IND/D1/EARNINGS **2**、IND/INSTITUTIONS 1、IND/SENTIMENT 1、GBR/D1/OTHER **2**；DEU/OTHER 3 已亮、EUR/RISK 3 已亮 | 可新点亮 3 座：USA/OTHER、IND/EARNINGS、GBR/OTHER。USA/EARNINGS 虽差 1，但本池唯一 EARNINGS 候选 `vRAn3xkG` 已判死 ⇒ **本轮点不亮** |
| **self 毒化快筛** | 本轮 MCP 本地 OS 池实测 12 颗，`max_correlation` 全部 <0.7：bla2k0Jq .2094 / 58J72oQN .2966 / omEdka3v .4164 / 6XdkW08J .3393 / pwdd7Za6 .4158 / RREPm361 .3275 / e7aeJoEd .5074 / qM7eZoVO .5017 / rK7Qm6ld .2514 / MP69RYAk .6585 / LL5Edbee .6338 / 3qj1eYdz .6976 | 11-13~11-14 新增 5 颗 ACTIVE **未毒化**这批候选；唯一被毒化的是 `vRAn3xkG`（self **.9961** 撞已提交孪生 `A1xJdOmg`），全族封死 |
| **prod 缓存年龄** | 11-15 上午 5 颗 `platform_sync` 重测完成：6XdkW08J 09:57、mLaLllmK 08:51、pwdLp9z6 06:42、rKRx7v6m 10:27、omExeqLb 10:59；11-13 20:xx 那批现值 39~41h 仍 <48h；11-10/11-11 那批 88~250h 已作废 | 11-13 报告里「P2 待终验 10 颗」**已解封 5 颗**，其余按 fail-closed 归 S2，不得凭旧缓存放行 |

## 2 评估口径

| 序 | 判据 | 阈值 / 说明 |
|---|---|---|
| 1 | 台账 | `REJECT` / `DEAD` / `DONE(被取代)` 优先于一切指标；append-only |
| 2 | 通道 | 只认 `type=REGULAR` 的 RA 全闸；SA/SUPER 单列 SX，不进排序 |
| 3 | prod | **<0.7 无豁免**；48h 内可信缓存直接过闸（用户 11-14 明令，不默认 `refresh=True`）；>48h / 无时刻一律 fail-closed；贴线（余量<0.02）提交前当刻 refresh |
| 4 | self | 本地 OS PnL 池实测 <0.7；提交孪生会瞬时把同骨架变体顶到 ≥0.99 |
| 5 | 算子数 | 只认 `regular.operatorCount` 平台实值，**≤8 才合格** |
| 6 | 方案 D | `performance_comparison` 硬闸＝ΔS<0 或 ΔF<0；配对判据＝ΔRet<0 ∧ (ΔTO>0 ∨ ΔDD>0)；force 不豁免 |
| 7 | 稳健 / 三问 | `PASS` > 无记录 / `CONDITIONAL`（后两者需 `robustness_audited=True` 显式声明）；2–3 腿需答三问 |
| 8 | 塔 | 点亮只认 `get_pyramid_alphas` 当季 ≥3；倍率按混类别最低档（木桶短板）；同席互相关 ≥0.7 让位 |
| 9 | 相对 prod（软偏好） | board `meanProdCorrelation` = **0.6396**（REGULAR 账户均值，n=232），低于基准 +5 分，不设硬闸 |

**排序分**（沿用 11-14 v3 十维，本轮加两项修正）＝终验闭环30 + prod余量20 + self余量15 + 稳健10 + 免三问5 + 塔边际10 + 质量5 + 算子5 + 相对prod5 + **ATOM 单塔8 / 双塔0** − **贴线惩罚**（prod≥.68 扣12、≥.69 再扣8、self≥.65 扣8）。贴线惩罚依据：`ZYa6x531` / `YPMvZZvv` 两次缓存回源漂移 +0.23~0.25。ATOM 加权依据：塔倍率木桶短板，IND 交付 5 颗全为 `PV+X` 双塔，倍率按 1.0/1.1 低档结算。

## 3 ★ S1 当前仍值得提交（16 颗，全量排序）

| # | alpha | 分 | 区 | S/F | ops | prod（缓存龄） | self | 稳健 | 方案D | 塔归属 → 当季 → 交后 → 新点亮 | 增量 | 待办 |
|---:|---|---:|---|---:|---:|---|---:|---|---|---|:---:|---|
| 1 | **`bla2k0Jq`** | **97.5** | USA | 1.80/1.25 | **4** | **.5138**（10.3h） | **.2094** | 无记录 | 放行 | `USA/D1/OTHER` 2→3 **点亮** | +1 | 稳健审计声明 |
| 2 | `qM7eZoVO` | 91.3 | IND | 1.90/1.42 | 7 | .5018（19.8h） | .5017 | robust 1.62 | 放行 | `IND/D1/EARNINGS` 2→3 **点亮** | +1 | 与 #3 同席 |
| 3 | `e7aeJoEd` | 90.5 | IND | 2.38/1.72 | 8 | .5124（20.8h） | .5074 | robust 1.91 | 放行 | `IND/D1/EARNINGS` 2→3 **点亮** | +1 | 与 #2 同席 |
| 4 | `rK7Qm6ld` | 82.6 | IND | 2.15/1.20 | 7 | .5634（20.3h） | .2514 | robust 1.04 | 放行 | SENTIMENT 1→2 否 / PV 11→12 已亮 | 0 | — |
| 5 | `omEdka3v` | 81.7 | GBR | 2.51/1.40 | 8 | .6026（12.0h） | .4164 | PASS | 放行 | SHORTINT 4→5 已亮 / **OTHER 2→3 点亮** | +1 | 三问 |
| 6 | `6XdkW08J` | 72.6 | GBR | 2.60/1.95 | 8 | .6267（3.4h） | .3393 | PASS | 放行 | SHORTINT 4→5 / MODEL 6→7，均已亮 | 0 | 三问 |
| 7 | `pwdd7Za6` | 63.9 | GBR | 1.69/1.04 | 8 | .6238（39.2h） | .4158 | 无记录 | 放行 | SHORTINT 4→5 / PV 4→5，均已亮 | 0 | 稳健声明；缓存近 48h |
| 8 | `LL5Edbee` | 63.8 | IND | 2.53/1.78 | 7 | .6327（21.9h） | .6338 | robust 1.28 | 放行 | INSTITUTIONS 1→2 否 / PV 已亮 | 0 | self 余量仅 .066 |
| 9 | `mLaLllmK` | 63.8 | EUR | 3.98/2.21 | 5 | .6579（4.5h） | .3014 | 无记录 | 放行 | OTHER 3→4 已亮 | 0 | 稳健声明 |
| 10 | `58J72oQN` | 61.1 | USA | 2.20/1.28 | 6 | **.6897**（11.5h） | .2966 | 无记录 | 放行(offset) | `USA/D1/OTHER` 2→3 **点亮** | +1 | **贴线，不值得优先** |
| 11 | `omExeqLb` | 60.6 | GBR | 2.43/1.78 | 8 | .6143（2.3h） | .4195 | 无记录 | 放行 | SHORTINT 4→5 / MODEL 6→7 已亮 | 0 | 稳健声明 + 三问 |
| 12 | `RREPm361` | 51.1 | DEU | 2.02/1.25 | 5 | **.6881**（40.9h） | .3275 | PASS | 放行 | ANALYST 6→7 已亮 | 0 | **贴线 + 三问** |
| 13 | `rKRx7v6m` | 49.9 | EUR | 3.22/2.14 | 7 | .6756（2.9h） | .4279 | CONDITIONAL | 放行 | SENTIMENT 3→4 / OTHER 3→4 已亮 | 0 | 稳健声明 + 三问 |
| 14 | `pwdLp9z6` | 49.6 | GBR | 2.26/1.19 | 8 | .6483（6.6h） | .4754 | 无记录 | 放行 | OTHER 2→3 点亮 | +1 | 与 #5 同席 ρ≥0.7 ⇒ **让位后备** |
| 15 | `MP69RYAk` | 46.7 | IND | 2.98/2.25 | 7 | .6699（21.3h） | .6585 | robust 1.70 | 放行 | INSTITUTIONS 1→2 否 | 0 | prod/self 双贴线 |
| 16 | `3qj1eYdz` | 22.3 | IND | 2.76/1.97 | 7 | **.6962**（21.6h） | **.6976** | robust 1.43 | 放行 | INSTITUTIONS 1→2 否 | 0 | 双贴线，**判高危不提交** |

**同席互斥矩阵（本轮必须处理）**：
- `USA/D1/OTHER`：`bla2k0Jq` ↔ `58J72oQN` 互相关 **−0.0561**（正交，可同篮），但只点一座 ⇒ **优先 bla2k0Jq**（prod 余量 18 倍、ops 4 vs 6、ATOM 单塔）。
- `IND/D1/EARNINGS`：`e7aeJoEd` ↔ `qM7eZoVO` ρ **.6965**（可同篮），只点一座 ⇒ 优先 `e7aeJoEd`（S/F/robust 更高）。
- `GBR/D1/OTHER`：`omEdka3v` ↔ `pwdLp9z6` ρ≥0.7 ⇒ `pwdLp9z6` 让位后备。

## 4 S2 待动作 / 待回源（31 颗，当前不可提交）

- **差一口气（prod 新鲜、仅缺手续）**：`vRAgNK3w`(EUR .6745/46.7h)、`Wjl8Z20O`(EUR .6768/44.2h)、`qMLJjleO`(GBR .6574/6.1h) —— 三颗均缺 `operatorCount` + 方案 D 边际 + 稳健 CONDITIONAL/无记录；缓存逼近 48h，**先补测再说**。
- **prod 缓存 >48h 作废，须 `refresh=True` 回源**：`Jj8qXO5m`(88h)、`2r5MqmVJ`(89h)、`d5apEYRx`(88h)、`rKRRjM51`(103h)、`WjOeNE6O`(124h)、`1YNMAA8M`(124h)、`vR11NmNr`(105h)、`leAnKOEA`(68h)、`leAgQPO5`(74h)、`KPJ1rG0j`(68h)、`N1P0odXg`(90h)、`88NbAJnl`(89h)、`leadbAKA`(90h)、`LLMzYrZe`(52h)。
- **11-05~11-10 老件（>120h，且多数缺 self/ops/方案D）**：`ZYQmolVx`、`RREOz5qn`、`rKRPAWv9`、`kqNAz9pP`、`E569ZE7L`、`N1NKzpRX`、`QPvbxjXw`、`QPvzNNGG`、`A1VGKqOe`、`mLovbnm2`、`ZYQXZj73`、`LLZ6wZO2`、`P0oR7vYw`、`omERn83n`。按「台账 5 天作废」实证，这批**不建议再投入终验算力**，除非对应塔席仍空且无新件。

## 5 S3 硬闸否决（86 颗，不值得提交）

> 一颗可同时命中多闸，下列分型计数之和大于 86。

| 否决类型 | 命中数 | 代表 |
|---|---:|---|
| prod ≥0.7（含终验推翻） | 35 | `88NmN37X` .9540 / `ZYa6x531` .9229 / `YPMvZZvv` .9499 / `ZYQv7j2Q` .8159 / `E5Q0On6m` .72 |
| `operatorCount > 8` | 26 | `E56GgqLL` 24 / `zq3Yrb3G` 15 / `leAmmre8` 9 / `Xg9dPpp0` 9 / `Jje6mrpO` 10 |
| 方案 D 硬拦 | 20 | `qM7KxkQV`、`d5a2vxzY`、`9qlz29Oe`、`ZYQ116ln`、`zqrgna91`、`N1eLE1de`（后两颗 IS 指标最强仍被拦） |
| 稳健台账 REJECT | 19 | `mL617YPx`、`9qxnYPjd`、`qMLOooX1` 等 |
| self ≥0.7 | 10 | `vRAn3xkG` **.9961**（撞 `A1xJdOmg`）/ `0mY5EZJv` .9954 / `xAvK6b0q` .9330 |
| 台账 DEAD / 被取代 | 12 | `MP6l68aa`（被 `58J72oQN` 零损失压缩取代）、`mLovqRV6`、`P05JM61x`、risk70 三族、earningscall 两族 |

## 6 S0 已提交 ACTIVE（32 颗，不可重复提交）

近十天提交集中于 EUR/DEU/KOR：`A1xJdOmg`(USA, ET 11-14 07:27)、`pwaQ0bx3`(DEU, ET 11-14 01:03)、`wpo8olA6`(DEU, ET 11-13 22:59)、`P059RmzM`(EUR, ET 11-13 04:43)、`d5a2aO7v`、`78Yk8VR1`、`E5QZ1NgJ`、`0mY1QPEv`、`O0W0w3P7`、`9qlZLVNd`、`XgaG2Vom`、`P0oolrZq`、`rKRx2Alj`、`zq3eb7No`、`GrW9OxmG`、`bl6AvMkN`、`bl6KwjwK`、`akK9ooZv`、`RRE5Mwkn`、`3qoGxkqZ`、`kqN92KpK`、`RRE9NkVj`、`leAEYLM8`、`6Xdo27P5`、`9qxdnV72`、`O0AJ3NEd`、`LLM5eAMn`、`omEMRpWb`、`RREnK5R1`、`3qompGeZ`、`3qoG6nEe`。
（SUPER 线 `Wjl6JJQO`、`E5Q7RGNR`、`e75avmq6`、`1YNjX03W`、`d5WGG5bg` 等另计，不在 RA 池。）

## 7 SX SA / SUPER 线（9 颗，不进 RA 排序）

**RA 是唯一可接受通道**；SA 定时任务只产方案文档、禁止 POST；且 SA 的 `is.checks` 无 `MATCHES_PYRAMID` ⇒ 不参与 pyramid 计数。本轮排序第一 `kqabOm7g`（GBR/SECTOR d3 l14，S4.53/F5.41/prod .6428/self .5291），次 `RReX6k6a`（DEU/R&M，S2.92/F2.91/prod .5514/self .5516）；`LLKq1dKL` 指标最高但 prod=self .6921 被余量闸拒。完整配方见 `output_report/SA_GBR_operator_full_scan_20261115.md` 与 `SA_cross_region_quality_20261115.md`。

## 8 S4 数据不足（23 颗）

仅台账留痕、无 prod/self/ops/评估行：`0mYJaWwG`、`1YWqzPGQ`、`2r50PAzJ`、`58EX15Nz`、`6XM87Zb7`、`786wl6b8`、`9qxn3MgK`、`A1VA5eXR`、`A1VAMwGl`、`Jj8w52Me`、`KPgKPRAx`、`RREgvX5a`、`akKp8zJ5`、`bl6wAWQq`、`blORMJwm`、`gJellnRg`、`kqNv1xRk`、`kqaE08PL`、`mLawVVZE`、`npvElm5q`、`npvjjLnM`、`vR1QGLbz`、`xArZ5mdW`。按 fail-closed 不进清单。

## 9 本轮推翻 / 更新的旧结论

| 项 | 旧（11-13/11-14 清单） | 本轮 | 影响 |
|---|---|---|---|
| 首推 | `omEdka3v`（v3 P1 第一） | **`bla2k0Jq`** | 11-14 才建件；prod 余量 .186、self .2094、4 ops、ATOM 单塔，全面优于旧首推 |
| P2 待终验 10 颗 | 全部 fail-closed，不可提交 | 5 颗 11-15 上午已重测解封 | `6XdkW08J`/`pwdLp9z6`/`mLaLllmK`/`omExeqLb`/`rKRx7v6m` 进 S1；其余 >48h 作废 |
| `RREPm361` self | DB 缓存 .6879（看着像贴线） | **实测 .3275** | 分散度风险解除，但 prod .6881 仍贴线 ⇒ 排 S1 末段、不优先 |
| 配额 | ET 11-14 REGULAR 2/4，剩 2 席 | **ET 11-15 0/4，剩 4 席** | 可一次性点 3 座塔 + 1 席质量件 |
| `vRAn3xkG` | 11-14 报告列为「已完全验证」 | **DEAD**（self .9961） | 提交孪生封死；同骨架未提交变体全族死 |
| 塔边际 | 11-13 认为 GBR/OTHER、DEU/OTHER 可点 | DEU/OTHER 已 3 点亮；新增 IND/EARNINGS、USA/OTHER 两席 | 塔增量重算，旧表作废 |
| `58J72oQN` | 11-15 结论「待用户点名」 | **不值得优先**（prod 余量 .0103） | 与 `bla2k0Jq` 同席，让位 |

## 10 纪律与产物

- **只挖不提交**：本报告是「可提交」判定，不含任何 POST；`ALLOW_ALPHA_SUBMIT=False`，提交权归用户点名。
- **提交前必做**：① 首推件补 `robustness_audited=True` 显式声明；② 贴线件 / 缓存 >39h 件当刻 `refresh=True` 终验；③ 2–3 腿补三问；④ 同席二选一；⑤ 按 ET 日历日确认剩余配额。
- **ΔS 禁跨区横比**；塔计数按季度重置、只认 `get_pyramid_alphas`；`MATCHES_THEMES` WARNING 属评奖资格，不属 RA 提交闸。
- 机读数据 `results/candidate_inventory_20261115.json`（197 行，含逐颗 blockers / todos / sources / 缓存龄）；全量表 `results/candidate_inventory_table_20261115.md`；脚本 `tools/candidate_inventory_20261115.py`（可重跑）。
- 数据源：`data/wqb.db`（`alphas` / `alpha_corr_cache` / `ledger_kv`）、`results/full_candidate_assessment_20261113.json`、`results/reliable_submit_list_20261113.json`、`results/full_basket_ranking_20261113.json`、`results/final_verify_*_20261113.json`、`output_report/{USA_regular_alpha_delivery,ind_campaign_delivery}_20261114.md`、`.workbuddy/memory/2026-11-{14,15}.md`，以及本轮 MCP 实读的塔计数 / OS 提交列表 / 12 颗 self 实测。

---

## 附录：全量 197 颗排序表

> 档序 S1 → S2 → S3 → S4 → S0 → SX；同档按排序分降序。prod 括号为缓存龄（小时），「旧/无时刻」按 fail-closed 处理。

| # | alpha | 档 | 区 | S/F | ops | prod（缓存龄） | self | 稳健 | 方案D | 塔边际 | 分 | 结论 |
|---:|---|---|---|---:|---:|---|---:|---|---|:---:|---:|---|
| 1 | `bla2k0Jq` | S1 | USA | 1.80/1.25 | 4 | 0.5138 (10.3h) | 0.2094 | NO_RECORD | 放行 | +1 | 97.5 | 稳健审计/显式声明 |
| 2 | `qM7eZoVO` | S1 | IND | 1.90/1.42 | 7 | 0.5018 (19.8h) | 0.5017 | robust 1.62 | 放行 | +1 | 91.3 | 可提交 |
| 3 | `e7aeJoEd` | S1 | IND | 2.38/1.72 | 8 | 0.5124 (20.8h) | 0.5074 | robust 1.91 | 放行 | +1 | 90.5 | 可提交 |
| 4 | `rK7Qm6ld` | S1 | IND | 2.15/1.20 | 7 | 0.5634 (20.3h) | 0.2514 | robust 1.04 | 放行 | 0 | 82.6 | 可提交 |
| 5 | `omEdka3v` | S1 | GBR | 2.51/1.40 | 8 | 0.6026 (12.0h) | 0.4164 | PASS | 放行 | +1 | 81.7 | 混腿三问答复核 |
| 6 | `6XdkW08J` | S1 | GBR | 2.60/1.95 | 8 | 0.6267 (3.4h) | 0.3393 | PASS | 放行 | 0 | 72.6 | 混腿三问答复核 |
| 7 | `pwdd7Za6` | S1 | GBR | 1.69/1.04 | 8 | 0.6238 (39.2h) | 0.4158 | NO_RECORD | 放行 | 0 | 63.9 | 稳健审计/显式声明 |
| 8 | `LL5Edbee` | S1 | IND | 2.53/1.78 | 7 | 0.6327 (21.9h) | 0.6338 | robust 1.28 | 放行 | 0 | 63.8 | 可提交 |
| 9 | `mLaLllmK` | S1 | EUR | 3.98/2.21 | 5 | 0.6579 (4.5h) | 0.3014 | NO_RECORD | 放行 | 0 | 63.8 | 稳健审计/显式声明 |
| 10 | `58J72oQN` | S1 | USA | 2.20/1.28 | 6 | 0.6897 (11.5h) | 0.2966 | NO_RECORD | 放行(offset) | +1 | 61.1 | 稳健审计/显式声明 / prod 贴线，提交前当刻 refresh=True |
| 11 | `omExeqLb` | S1 | GBR | 2.43/1.78 | 8 | 0.6143 (2.3h) | 0.4195 | NO_RECORD | 放行 | 0 | 60.6 | 稳健审计/显式声明 / 混腿三问答复核 |
| 12 | `RREPm361` | S1 | DEU | 2.02/1.25 | 5 | 0.6881 (40.9h) | 0.3275 | PASS | 放行 | 0 | 51.1 | 混腿三问答复核 / prod 贴线，提交前当刻 refresh=True |
| 13 | `rKRx7v6m` | S1 | EUR | 3.22/2.14 | 7 | 0.6756 (2.9h) | 0.4279 | CONDITIONAL | 放行 | 0 | 49.9 | 稳健审计/显式声明 / 混腿三问答复核 |
| 14 | `pwdLp9z6` | S1 | GBR | 2.26/1.19 | 8 | 0.6483 (6.6h) | 0.4754 | NO_RECORD | 放行 | 0 | 49.6 | 稳健审计/显式声明 / 混腿三问答复核 |
| 15 | `MP69RYAk` | S1 | IND | 2.98/2.25 | 7 | 0.6699 (21.3h) | 0.6585 | robust 1.70 | 放行 | 0 | 46.7 | 可提交 |
| 16 | `3qj1eYdz` | S1 | IND | 2.76/1.97 | 7 | 0.6962 (21.6h) | 0.6976 | robust 1.43 | 放行 | 0 | 22.3 | prod 贴线，提交前当刻 refresh=True |
| 17 | `vRAgNK3w` | S2 | EUR | —/— | — | 0.6745 (46.7h) | 0.2062 | CONDITIONAL | 未测 | 0 | 54.5 | 稳健审计/显式声明 / operatorCount 未取 |
| 18 | `Wjl8Z20O` | S2 | EUR | —/— | — | 0.6768 (44.2h) | 0.2015 | CONDITIONAL | 未测 | 0 | 54.3 | 稳健审计/显式声明 / operatorCount 未取 |
| 19 | `qMLJjleO` | S2 | GBR | 2.27/1.43 | — | 0.6574 (6.1h) | 0.4997 | NO_RECORD | 未测 | 0 | 51.0 | 稳健审计/显式声明 / operatorCount 未取 |
| 20 | `ZYQmolVx` | S2 | EUR | 2.48/1.19 | — | 0.5276 (247.5h) | — | PASS | 未测 | 0 | 41.4 | prod 缓存 247.5h>48h 作废，须回源 |
| 21 | `RREOz5qn` | S2 | DEU | 1.72/1.31 | — | 0.5834 (136.0h) | — | PASS | 未测 | 0 | 35.5 | prod 缓存 136.0h>48h 作废，须回源 |
| 22 | `rKRPAWv9` | S2 | GBR | 1.76/1.07 | — | 0.3998 (166.4h) | — | NO_RECORD | 未测 | 0 | 33.7 | prod 缓存 166.4h>48h 作废，须回源 |
| 23 | `kqNAz9pP` | S2 | DEU | 1.61/1.16 | — | 0.5154 (126.0h) | — | NO_RECORD | 未测 | 0 | 32.1 | prod 缓存 126.0h>48h 作废，须回源 |
| 24 | `E569ZE7L` | S2 | DEU | 1.68/1.21 | — | 0.5444 (125.8h) | — | CONDITIONAL | 未测 | 0 | 29.3 | prod 缓存 125.8h>48h 作废，须回源 |
| 25 | `N1NKzpRX` | S2 | KOR | 1.82/1.45 | — | 0.5469 (216.7h) | — | NO_RECORD | 未测 | 0 | 29.3 | prod 缓存 216.7h>48h 作废，须回源 |
| 26 | `Jj8qXO5m` | S2 | EUR | 1.74/1.03 | 8 | 0.6663 (88.3h) | 0.2447 | NO_RECORD | 放行 | 0 | 29.0 | prod 缓存 88.3h>48h 作废，须回源 |
| 27 | `2r5MqmVJ` | S2 | EUR | 1.74/1.03 | 8 | 0.6740 (89.0h) | 0.2393 | NO_RECORD | 放行 | 0 | 28.2 | prod 缓存 89.0h>48h 作废，须回源 |
| 28 | `QPvbxjXw` | S2 | GBR | 1.87/1.14 | — | 0.5794 (166.4h) | — | NO_RECORD | 未测 | 0 | 25.8 | prod 缓存 166.4h>48h 作废，须回源 |
| 29 | `QPvzNNGG` | S2 | DEU | 1.70/1.30 | — | 0.6777 (117.4h) | — | PASS | 未测 | 0 | 21.1 | prod 缓存 117.4h>48h 作废，须回源 |
| 30 | `A1VGKqOe` | S2 | GLB | 2.95/1.76 | — | 0.6408 (238.0h) | 0.5651 | NO_RECORD | 未测 | 0 | 20.8 | prod 缓存 238.0h>48h 作废，须回源 |
| 31 | `rKRRjM51` | S2 | IND | 3.34/2.65 | 7 | 0.6752 (102.6h) | 0.6516 | PASS | 放行 | 0 | 19.0 | prod 缓存 102.6h>48h 作废，须回源 |
| 32 | `WjOeNE6O` | S2 | EUR | 2.90/1.85 | 5 | 0.6411 (124.1h) | 0.6411 | NO_RECORD | 放行 | 0 | 16.9 | prod 缓存 124.1h>48h 作废，须回源 |
| 33 | `vR11NmNr` | S2 | IND | 3.29/2.58 | — | 0.6740 (104.8h) | 0.6617 | PASS | 未测 | 0 | 16.6 | prod 缓存 104.8h>48h 作废，须回源 |
| 34 | `d5apEYRx` | S2 | EUR | 1.77/1.05 | 8 | 0.6887 (88.2h) | 0.2315 | NO_RECORD | 放行 | 0 | 14.8 | prod 缓存 88.2h>48h 作废，须回源 |
| 35 | `leAnKOEA` | S2 | EUR | 2.05/1.39 | — | 0.6476 (68.1h) | — | CONDITIONAL | 未测 | 0 | 14.3 | prod 缓存 68.1h>48h 作废，须回源 |
| 36 | `mLovbnm2` | S2 | DEU | 1.94/1.79 | — | 0.6572 (131.5h) | — | NO_RECORD | 未测 | 0 | 13.6 | prod 缓存 131.5h>48h 作废，须回源 |
| 37 | `ZYQXZj73` | S2 | GBR | 1.78/1.16 | — | 0.6524 (166.4h) | — | NO_RECORD | 未测 | 0 | 13.5 | prod 缓存 166.4h>48h 作废，须回源 |
| 38 | `leAgQPO5` | S2 | GBR | 2.16/1.18 | — | 0.6866 (74.4h) | 0.1061 | CONDITIONAL | 未测 | 0 | 13.3 | prod 缓存 74.4h>48h 作废，须回源 |
| 39 | `LLZ6wZO2` | S2 | KOR | 1.99/1.53 | — | 0.6762 (166.6h) | — | NO_RECORD | 未测 | 0 | 11.5 | prod 缓存 166.6h>48h 作废，须回源 |
| 40 | `leadbAKA` | S2 | EUR | 1.67/0.96 | — | 0.6713 (89.6h) | — | NO_RECORD | 未测 | 0 | 11.4 | prod 缓存 89.6h>48h 作废，须回源 |
| 41 | `88NbAJnl` | S2 | EUR | —/— | — | 0.6740 (89.4h) | — | CONDITIONAL | 未测 | 0 | 9.6 | prod 缓存 89.4h>48h 作废，须回源 |
| 42 | `P0oR7vYw` | S2 | EUR | 2.28/1.61 | — | 0.6881 (137.6h) | — | PASS | 未测 | 0 | 8.5 | prod 缓存 137.6h>48h 作废，须回源 |
| 43 | `LLMzYrZe` | S2 | DEU | 1.61/1.16 | — | 0.6697 (51.9h) | 0.6697 | CONDITIONAL | 未测 | 0 | 4.8 | prod 缓存 51.9h>48h 作废，须回源 |
| 44 | `omERn83n` | S2 | KOR | 1.62/1.23 | — | 0.6898 (212.2h) | — | CONDITIONAL | 未测 | 0 | -2.2 | prod 缓存 212.2h>48h 作废，须回源 |
| 45 | `1YNMAA8M` | S2 | DEU | 1.58/1.36 | 8 | 0.6951 (123.9h) | 0.6946 | PASS | 放行 | 0 | -6.5 | prod 缓存 123.9h>48h 作废，须回源 |
| 46 | `KPJ1rG0j` | S2 | EUR | 1.96/1.49 | — | 0.6957 (68.2h) | — | NO_RECORD | 未测 | 0 | -10.5 | prod 缓存 68.2h>48h 作废，须回源 |
| 47 | `N1P0odXg` | S2 | ? | —/— | — | 0.6964 (89.5h) | — | NO_RECORD | 未测 | 0 | -12.6 | prod 缓存 89.5h>48h 作废，须回源 |
| 48 | `6XMmE0EL` | S3 | EUR | 2.35/1.02 | 5 | 0.6529 (4.0h) | 0.2488 | NO_RECORD | 阻断 | 0 | 45 | 方案D 硬拦 |
| 49 | `78L5GaeZ` | S3 | EUR | 3.02/2.35 | 10 | 0.6662 (-0.3h) | 0.4608 | NO_RECORD | 放行 | 0 | 45 | ops 10>8 |
| 50 | `9qlz29Oe` | S3 | DEU | 1.86/1.34 | 12 | 0.4700 (8.2h) | 0.4556 | CONDITIONAL | 阻断 | 0 | 45 | ops 12>8 / 方案D 硬拦 |
| 51 | `Jje6mrpO` | S3 | GBR | 2.37/1.58 | 10 | 0.5565 (14.1h) | 0.3285 | NO_RECORD | 放行 | 0 | 45 | ops 10>8 |
| 52 | `LLM0e20m` | S3 | GBR | 1.75/1.17 | 11 | 0.5386 (22.4h) | 0.4041 | NO_RECORD | 放行 | 0 | 45 | ops 11>8 |
| 53 | `N1P02YwL` | S3 | EUR | 1.81/1.43 | 9 | 0.6073 (41.7h) | 0.5909 | NO_RECORD | 阻断 | 0 | 45 | ops 9>8 / 方案D 硬拦 |
| 54 | `Xg9dPpp0` | S3 | GBR | 1.97/1.44 | 9 | 0.4000 (13.6h) | 0.2787 | NO_RECORD | 放行 | 0 | 45 | ops 9>8 |
| 55 | `ZYa6x531` | S3 | EUR | 1.74/1.01 | 8 | 0.9229 (24.9h) | 0.1987 | PASS | 放行 | 0 | 45 | prod≥0.7 |
| 56 | `rKRx0M2m` | S3 | GBR | 2.29/1.56 | 11 | 0.6232 (9.2h) | 0.4433 | NO_RECORD | 放行 | 0 | 45 | ops 11>8 |
| 57 | `MP6l68aa` | S3 | USA | 2.20/1.28 | — | 0.6897 (5.0h) | 0.2955 | NO_RECORD | 未测 | 0 | 43.1 | DONE(被 58J72oQN 零损失压缩取代) |
| 58 | `mL617YPx` | S3 | EUR | 1.82/1.25 | 14 | 0.5421 (146.5h) | 0.4504 | REJECT | 阻断 | 0 | 39.0 | 稳健台账 REJECT / ops 14>8 |
| 59 | `ZYQ116ln` | S3 | KOR | 1.86/1.10 | 3 | 0.6981 (24.5h) | 0.2124 | CONDITIONAL | 阻断 | 0 | 38.9 | 方案D 硬拦 |
| 60 | `zqrgna91` | S3 | USA | 2.67/1.66 | — | 0.6877 (14.0h) | — | PASS | 阻断 | 0 | 38.8 | 方案D 硬拦 / 方案D：ΔF −0.01 ∧ (ΔRet −0.0007 ∧ ΔTO +0.0095) 配对双恶化；prod .6877 贴线 |
| 61 | `E56GgqLL` | S3 | EUR | 1.68/1.17 | 24 | 0.5524 (旧/无时刻) | 0.4347 | NO_RECORD | 放行 | 0 | 38.4 | ops 24>8 / prod 缓存 999.0h>48h 作废，须回源 |
| 62 | `leAmmre8` | S3 | GBR | 2.97/1.40 | 9 | 0.6887 (10.8h) | 0.4498 | NO_RECORD | 放行 | 0 | 33.0 | ops 9>8 |
| 63 | `RREGX1kd` | S3 | GBR | 1.65/1.09 | 9 | 0.5940 (123.0h) | 0.3688 | NO_RECORD | 放行 | 0 | 31.7 | ops 9>8 / prod 缓存 123.0h>48h 作废，须回源 |
| 64 | `9qxnNkeq` | S3 | DEU | 1.66/1.18 | — | 0.5327 (126.0h) | — | REJECT | 未测 | 0 | 30.4 | 稳健台账 REJECT / prod 缓存 126.0h>48h 作废，须回源 |
| 65 | `qME6VWbj` | S3 | EUR | 1.76/1.07 | 5 | 0.6609 (旧/无时刻) | — | PASS | 阻断 | 0 | 26.6 | 方案D 硬拦 / prod 缓存 999.0h>48h 作废，须回源 |
| 66 | `xArjE96W` | S3 | EUR | 2.28/1.45 | 14 | 0.5907 (旧/无时刻) | — | NO_RECORD | 阻断 | 0 | 25.2 | ops 14>8 / 方案D 硬拦 |
| 67 | `88NmN37X` | S3 | DEU | 1.79/1.53 | 9 | 0.9540 (41.0h) | 0.9540 | PASS | 放行 | 0 | 21.0 | prod≥0.7 / self≥0.7 |
| 68 | `N1eLE1de` | S3 | USA | 2.63/1.54 | — | 0.6916 (14.0h) | — | CONDITIONAL | 阻断 | 0 | 20.3 | 方案D 硬拦 / 方案D：ΔRet −0.0026 ∧ ΔTO +0.0071；稳健 CONDITIONAL；prod 余量 .0084 全池最薄 |
| 69 | `E56XvX90` | S3 | USA | 1.75/1.13 | — | 0.7519 (18.4h) | — | NO_RECORD | 未测 | 0 | 18.7 | DEAD：prod 0.7519（risk70 族） / prod≥0.7 |
| 70 | `E5Q0On6m` | S3 | USA | 1.74/1.09 | — | 0.7200 (17.4h) | — | NO_RECORD | 未测 | 0 | 18.7 | prod≥0.7 / prod 0.72 超线（差 0.02），被 STATISTICAL 换档件取代 |
| 71 | `P0od2pOp` | S3 | USA | 1.61/1.18 | — | 0.8192 (18.1h) | — | NO_RECORD | 未测 | 0 | 18.7 | DEAD：prod 0.8192（earningscall 情绪族地板） / prod≥0.7 |
| 72 | `YPMvZZvv` | S3 | USA | 1.79/1.06 | — | 0.9499 (14.0h) | — | NO_RECORD | 未测 | 0 | 18.7 | prod≥0.7 / 陈旧 prod .6958 → refresh .9499 撞墙（14 天漂移 +0.25） |
| 73 | `pwdAPALb` | S3 | USA | 1.75/1.16 | — | 0.7541 (18.4h) | — | NO_RECORD | 未测 | 0 | 18.7 | DEAD：prod 0.7541（risk70 三重 bucket 族全灭） / prod≥0.7 |
| 74 | `6Xd7A5V7` | S3 | USA | 1.77/1.01 | — | 0.7672 (13.8h) | — | NO_RECORD | 未测 | 0 | 18.6 | DEAD：prod 0.7672（earningscall 情绪族） / prod≥0.7 |
| 75 | `d5a2vxzY` | S3 | DEU | 1.60/1.08 | 12 | 0.6039 (100.5h) | — | CONDITIONAL | 阻断 | 0 | 18.2 | ops 12>8 / 方案D 硬拦 |
| 76 | `Jj8VQwoe` | S3 | DEU | 1.65/1.24 | 12 | 0.6124 (100.5h) | — | CONDITIONAL | 阻断 | 0 | 17.5 | ops 12>8 / 方案D 硬拦 |
| 77 | `xAvK6b0q` | S3 | KOR | —/— | — | — | — | PASS | 未测 | 0 | 17.0 | DEAD：self 实测 0.9330 撞 E5QZ1NgJ（11-10 旧表误记 PASS） |
| 78 | `vRAn3xkG` | S3 | USA | 1.97/1.09 | — | 0.9961 (14.6h) | 0.9961 | NO_RECORD | 阻断 | 0 | 16.8 | DEAD：self 0.9961 撞已提交孪生 A1xJdOmg；方案D 硬拦 / prod≥0.7 |
| 79 | `qM7KxkQV` | S3 | DEU | 1.72/1.34 | 11 | 0.9346 (12.5h) | 0.9346 | PASS | 阻断 | 0 | 15.9 | prod≥0.7 / self≥0.7 |
| 80 | `mLovqRV6` | S3 | DEU | 1.83/1.50 | — | 0.6413 (132.5h) | — | NO_RECORD | 未测 | 0 | 14.9 | DEAD：2Y 1.27 硬闸 WARNING，该族 46 变体全判死 / prod 缓存 132.5h>48h 作废，须回源 |
| 81 | `0mY5EZJv` | S3 | ? | —/— | — | 0.6462 (181.0h) | — | NO_RECORD | 未测 | 0 | 12.4 | DEAD：self 实测 0.9954 撞 ACTIVE bl6AvMkN / prod 缓存 181.0h>48h 作废，须回源 |
| 82 | `RREwqrNa` | S3 | DEU | 1.65/1.17 | — | 0.6684 (158.2h) | — | REJECT | 未测 | 0 | 11.9 | 稳健台账 REJECT / prod 缓存 158.2h>48h 作废，须回源 |
| 83 | `2rAYpJKx` | S3 | DEU | 1.94/1.79 | — | 0.9966 (23.0h) | 0.9966 | NO_RECORD | 未测 | 0 | 11.3 | prod≥0.7 / self≥0.7 |
| 84 | `bl6eELlZ` | S3 | DEU | 1.85/1.44 | — | — | — | REJECT | 未测 | 0 | 9.0 | 稳健台账 REJECT |
| 85 | `1YNrQMr6` | S3 | DEU | 1.77/1.32 | — | — | — | REJECT | 未测 | 0 | 8.9 | 稳健台账 REJECT |
| 86 | `78LeWrZ5` | S3 | DEU | 1.76/1.33 | — | — | — | REJECT | 未测 | 0 | 8.9 | 稳健台账 REJECT |
| 87 | `LLM0Ww9a` | S3 | DEU | 1.78/1.36 | — | — | — | REJECT | 未测 | 0 | 8.9 | 稳健台账 REJECT |
| 88 | `VkxAVL6Y` | S3 | DEU | 1.78/1.36 | — | — | — | REJECT | 未测 | 0 | 8.9 | 稳健台账 REJECT |
| 89 | `zqdvb0YE` | S3 | DEU | 1.72/1.34 | 9 | — | — | NO_RECORD | 放行 | 0 | 8.9 | ops 9>8 |
| 90 | `3qo8MGbN` | S3 | DEU | 1.71/1.24 | — | — | — | REJECT | 未测 | 0 | 8.8 | 稳健台账 REJECT |
| 91 | `ZYQOGpR0` | S3 | DEU | 1.67/1.25 | — | — | — | REJECT | 未测 | 0 | 8.8 | 稳健台账 REJECT |
| 92 | `E569Xd91` | S3 | DEU | 1.61/1.16 | — | — | — | REJECT | 未测 | 0 | 8.7 | 稳健台账 REJECT |
| 93 | `Jje6Kd9x` | S3 | DEU | 1.64/1.17 | — | — | — | REJECT | 未测 | 0 | 8.7 | 稳健台账 REJECT |
| 94 | `LLMv6joe` | S3 | DEU | 1.65/1.17 | 15 | — | — | NO_RECORD | 放行 | 0 | 8.7 | ops 15>8 |
| 95 | `WjOvmAZx` | S3 | DEU | 1.62/1.14 | — | — | — | REJECT | 未测 | 0 | 8.7 | 稳健台账 REJECT |
| 96 | `akKqLq56` | S3 | USA | 1.72/1.09 | — | — | — | NO_RECORD | 未测 | 0 | 8.7 | DEAD：prod 0.7034（risk70 族） |
| 97 | `gJenzYRO` | S3 | DEU | 1.66/1.19 | — | — | — | REJECT | 未测 | 0 | 8.7 | 稳健台账 REJECT |
| 98 | `6Xd57QjE` | S3 | DEU | 1.59/1.10 | — | — | — | REJECT | 未测 | 0 | 8.6 | 稳健台账 REJECT |
| 99 | `Xg9dEjY1` | S3 | DEU | 1.55/1.07 | — | — | — | REJECT | 未测 | 0 | 8.6 | 稳健台账 REJECT |
| 100 | `O0AlvGL7` | S3 | DEU | 1.38/0.90 | — | — | — | REJECT | 未测 | 0 | 8.4 | 稳健台账 REJECT |
| 101 | `QPvwdGxK` | S3 | DEU | 1.38/0.90 | — | — | — | REJECT | 未测 | 0 | 8.4 | 稳健台账 REJECT |
| 102 | `P05JM61x` | S3 | DEU | 1.46/0.79 | — | — | — | NO_RECORD | 未测 | 0 | 8.3 | DEAD：平台 4 项 FAIL（S1.46/F.79/ladder1.36/sub.61） |
| 103 | `xAvK73Qg` | S3 | DEU | 2.04/1.77 | 11 | 0.7410 (0.8h) | 0.7410 | CONDITIONAL | 放行 | 0 | 6.3 | prod≥0.7 / self≥0.7 |
| 104 | `WjOAJWxd` | S3 | EUR | 2.36/1.61 | 10 | 0.6806 (265.0h) | 0.6446 | NO_RECORD | 阻断 | 0 | 1.4 | ops 10>8 / 方案D 硬拦 |
| 105 | `9qxnYPjd` | S3 | KOR | 1.58/1.41 | — | 0.7025 (134.4h) | — | PASS | 未测 | 0 | -1.2 | prod≥0.7 / prod 缓存 134.4h>48h 作废，须回源 |
| 106 | `6XMmNmjP` | S3 | EUR | —/— | — | 0.7998 (92.1h) | — | PASS | 未测 | 0 | -3.0 | prod≥0.7 / prod 缓存 92.1h>48h 作废，须回源 |
| 107 | `JjeNJ00O` | S3 | EUR | 2.60/1.35 | 10 | 0.6813 (旧/无时刻) | — | NO_RECORD | 阻断 | 0 | -5.8 | ops 10>8 / 方案D 硬拦 |
| 108 | `VkxWmpYG` | S3 | EUR | 2.15/1.49 | 11 | 0.6800 (68.1h) | — | NO_RECORD | 阻断 | 0 | -5.8 | ops 11>8 / 方案D 硬拦 |
| 109 | `1YNjqknX` | S3 | EUR | 3.37/1.84 | — | 0.9700 (242.4h) | 0.9700 | PASS | 未测 | 0 | -7.9 | prod≥0.7 / self≥0.7 |
| 110 | `QPvx8M1W` | S3 | KOR | 1.67/1.54 | — | 0.8935 (53.0h) | 0.8935 | PASS | 未测 | 0 | -9.0 | prod≥0.7 / self≥0.7 |
| 111 | `leAmYEPA` | S3 | DEU | 1.94/1.84 | — | 0.8599 (127.5h) | — | NO_RECORD | 未测 | 0 | -10.7 | prod≥0.7 / prod 缓存 127.5h>48h 作废，须回源 |
| 112 | `WjO5xv2k` | S3 | DEU | 1.80/1.65 | — | 0.7397 (127.7h) | — | NO_RECORD | 未测 | 0 | -10.9 | prod≥0.7 / prod 缓存 127.7h>48h 作废，须回源 |
| 113 | `mLovW2Nx` | S3 | DEU | 1.75/1.60 | — | 0.7464 (127.2h) | — | NO_RECORD | 未测 | 0 | -10.9 | prod≥0.7 / prod 缓存 127.2h>48h 作废，须回源 |
| 114 | `QPv8prAK` | S3 | DEU | 1.70/1.53 | — | 0.7574 (127.1h) | — | NO_RECORD | 未测 | 0 | -11.0 | prod≥0.7 / prod 缓存 127.1h>48h 作废，须回源 |
| 115 | `RREgwZo1` | S3 | DEU | 1.70/1.53 | — | 0.7520 (127.1h) | — | NO_RECORD | 未测 | 0 | -11.0 | prod≥0.7 / prod 缓存 127.1h>48h 作废，须回源 |
| 116 | `RREgwqPd` | S3 | DEU | 1.79/1.53 | — | 0.7390 (127.4h) | — | NO_RECORD | 未测 | 0 | -11.0 | prod≥0.7 / prod 缓存 127.4h>48h 作废，须回源 |
| 117 | `qMLRwbOP` | S3 | DEU | 1.71/1.54 | — | 0.7441 (127.8h) | — | NO_RECORD | 未测 | 0 | -11.0 | prod≥0.7 / prod 缓存 127.8h>48h 作废，须回源 |
| 118 | `A1VA8YEY` | S3 | DEU | 1.71/1.43 | — | 0.7429 (127.0h) | — | NO_RECORD | 未测 | 0 | -11.1 | prod≥0.7 / prod 缓存 127.0h>48h 作废，须回源 |
| 119 | `1YNMRqxK` | S3 | DEU | 1.62/1.31 | — | 0.7246 (127.0h) | — | NO_RECORD | 未测 | 0 | -11.2 | prod≥0.7 / prod 缓存 127.0h>48h 作废，须回源 |
| 120 | `E56jA0AP` | S3 | KOR | 1.58/1.41 | — | 0.7264 (135.3h) | — | CONDITIONAL | 未测 | 0 | -11.2 | prod≥0.7 / prod 缓存 135.3h>48h 作废，须回源 |
| 121 | `O0A3j5vd` | S3 | DEU | 1.59/1.38 | — | 0.7260 (127.5h) | — | NO_RECORD | 未测 | 0 | -11.2 | prod≥0.7 / prod 缓存 127.5h>48h 作废，须回源 |
| 122 | `YP1zY8EM` | S3 | EUR | 2.02/1.02 | — | 0.7290 (185.3h) | — | NO_RECORD | 未测 | 0 | -11.2 | DEAD：prod 0.729 超线 + CLUSTER_TEST WARNING / prod≥0.7 |
| 123 | `d5Wvpmbx` | S3 | KOR | 1.82/1.25 | — | 0.9081 (167.9h) | — | CONDITIONAL | 未测 | 0 | -11.2 | prod≥0.7 / prod 缓存 167.9h>48h 作废，须回源 |
| 124 | `j2Y7GZJE` | S3 | DEU | 1.58/1.25 | — | 0.7238 (127.8h) | — | NO_RECORD | 未测 | 0 | -11.3 | prod≥0.7 / prod 缓存 127.8h>48h 作废，须回源 |
| 125 | `A1xZ7kNW` | S3 | DEU | 1.75/1.01 | — | 0.8377 (69.0h) | — | NO_RECORD | 未测 | 0 | -11.4 | prod≥0.7 / prod 缓存 69.0h>48h 作废，须回源 |
| 126 | `O0WOK0Wg` | S3 | EUR | 1.68/1.06 | — | 0.8518 (68.1h) | — | NO_RECORD | 未测 | 0 | -11.4 | prod≥0.7 / prod 缓存 68.1h>48h 作废，须回源 |
| 127 | `ZYQv7j2Q` | S3 | GBR | 2.64/1.57 | 8 | 0.8159 (84.7h) | 0.8159 | PASS | 放行 | 0 | -11.5 | prod≥0.7 / self≥0.7 |
| 128 | `N1NGbddg` | S3 | EUR | 1.69/1.05 | 12 | 0.6872 (68.1h) | 0.6595 | NO_RECORD | 阻断 | 0 | -13.6 | ops 12>8 / 方案D 硬拦 |
| 129 | `zq3Yrb3G` | S3 | EUR | 2.87/1.65 | 15 | 0.6872 (旧/无时刻) | 0.6873 | NO_RECORD | 放行 | 0 | -13.6 | ops 15>8 / prod 缓存 999.0h>48h 作废，须回源 |
| 130 | `YP1baJrv` | S3 | EUR | 2.23/1.19 | 9 | 0.6999 (旧/无时刻) | — | NO_RECORD | 阻断 | 0 | -16.0 | ops 9>8 / 方案D 硬拦 |
| 131 | `qMLOooX1` | S3 | KOR | 1.94/1.74 | — | 0.9608 (68.9h) | 0.9608 | REJECT | 未测 | 0 | -18.7 | 稳健台账 REJECT / prod≥0.7 |
| 132 | `akKGqOmx` | S3 | KOR | 1.92/1.16 | — | 0.8736 (127.3h) | 0.8736 | NO_RECORD | 未测 | 0 | -19.2 | prod≥0.7 / self≥0.7 |
| 133 | `O0A6Qz7p` | S3 | GBR | 2.18/1.52 | 10 | 0.6984 (128.1h) | 0.6780 | NO_RECORD | 放行 | 0 | -22.8 | ops 10>8 / prod 缓存 128.1h>48h 作废，须回源 |
| 134 | `0mYJaWwG` | S4 | DEU | 1.64/1.30 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 135 | `1YWqzPGQ` | S4 | DEU | 1.59/1.10 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 136 | `2r50PAzJ` | S4 | DEU | 1.83/1.46 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 137 | `58EX15Nz` | S4 | DEU | 1.90/1.79 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 138 | `6XM87Zb7` | S4 | DEU | 1.87/1.06 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 139 | `786wl6b8` | S4 | IND | 3.86/2.57 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 140 | `9qxn3MgK` | S4 | DEU | 1.86/1.73 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 141 | `A1VA5eXR` | S4 | DEU | 1.75/1.61 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 142 | `A1VAMwGl` | S4 | DEU | 1.36/1.35 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 143 | `Jj8w52Me` | S4 | DEU | 1.67/1.16 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 144 | `KPgKPRAx` | S4 | ? | —/— | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 145 | `RREgvX5a` | S4 | DEU | 1.49/1.26 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 146 | `akKp8zJ5` | S4 | DEU | 1.87/1.74 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 147 | `bl6wAWQq` | S4 | DEU | 1.66/1.47 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 148 | `blORMJwm` | S4 | GBR | 1.91/1.24 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 149 | `gJellnRg` | S4 | DEU | 1.73/1.34 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 150 | `kqNv1xRk` | S4 | KOR | 1.62/1.50 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 151 | `kqaE08PL` | S4 | ? | —/— | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 152 | `mLawVVZE` | S4 | ? | —/— | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 153 | `npvElm5q` | S4 | DEU | 1.85/1.76 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 154 | `npvjjLnM` | S4 | DEU | 1.89/1.52 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 155 | `vR1QGLbz` | S4 | DEU | 1.64/1.30 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 156 | `xArZ5mdW` | S4 | DEU | 1.67/1.47 | — | — | — | NO_RECORD | 未测 | 0 | 0 | 稳健审计/显式声明 / self 缺实测 |
| 157 | `0mY1QPEv` | S0 | EUR | 3.76/2.32 | — | 0.6339 (121.8h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 121.8h>48h 作废，须回源 |
| 158 | `3qoG6nEe` | S0 | IND | 4.45/3.67 | — | 0.4708 (202.0h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 202.0h>48h 作废，须回源 |
| 159 | `3qoGxkqZ` | S0 | GBR | 2.48/1.33 | — | 0.6729 (166.4h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 166.4h>48h 作废，须回源 |
| 160 | `3qompGeZ` | S0 | GBR | 4.42/4.27 | — | 0.6221 (146.1h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 146.1h>48h 作废，须回源 |
| 161 | `6Xdo27P5` | S0 | KOR | 1.68/1.30 | — | 0.6393 (202.6h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 202.6h>48h 作废，须回源 |
| 162 | `78Yk8VR1` | S0 | DEU | 1.68/1.21 | — | 0.5444 (115.1h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 115.1h>48h 作废，须回源 |
| 163 | `9qlZLVNd` | S0 | EUR | 2.04/1.04 | — | 0.5889 (96.6h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 96.6h>48h 作废，须回源 |
| 164 | `9qxdnV72` | S0 | EUR | 1.84/1.01 | — | 0.6806 (201.4h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 201.4h>48h 作废，须回源 |
| 165 | `A1xJdOmg` | S0 | USA | 1.92/1.04 | — | 0.5265 (16.9h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE |
| 166 | `E5QZ1NgJ` | S0 | KOR | 1.86/1.74 | — | 0.6192 (116.0h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 116.0h>48h 作废，须回源 |
| 167 | `GrW9OxmG` | S0 | DEU | 1.62/1.56 | — | 0.6635 (179.7h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 179.7h>48h 作废，须回源 |
| 168 | `LLM5eAMn` | S0 | EUR | 3.48/1.95 | — | 0.6652 (242.9h) | 0.2318 | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 242.9h>48h 作废，须回源 |
| 169 | `O0AJ3NEd` | S0 | EUR | 2.91/1.36 | — | 0.6557 (238.8h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 238.8h>48h 作废，须回源 |
| 170 | `O0W0w3P7` | S0 | EUR | 2.72/1.15 | — | 0.6403 (106.9h) | 0.0984 | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 106.9h>48h 作废，须回源 |
| 171 | `P059RmzM` | S0 | EUR | 1.95/1.02 | — | 0.6788 (44.4h) | 0.1994 | PASS | 未测 | 0 | 0 | 已提交 ACTIVE |
| 172 | `P0obGoQJ` | S0 | ASI | 3.06/1.39 | — | 0.5973 (163.2h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 163.2h>48h 作废，须回源 |
| 173 | `P0oolrZq` | S0 | GLB | 3.45/2.37 | — | 0.6578 (108.4h) | 0.5680 | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 108.4h>48h 作废，须回源 |
| 174 | `RRE5Mwkn` | S0 | GBR | 2.15/1.41 | — | 0.4744 (166.3h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 166.3h>48h 作废，须回源 |
| 175 | `RRE9NkVj` | S0 | KOR | 1.76/1.63 | — | 0.6605 (210.5h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 210.5h>48h 作废，须回源 |
| 176 | `RREnK5R1` | S0 | IND | 2.82/2.04 | — | 0.5874 (233.7h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 233.7h>48h 作废，须回源 |
| 177 | `XgaG2Vom` | S0 | EUR | 1.75/1.05 | — | 0.6744 (87.9h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 87.9h>48h 作废，须回源 |
| 178 | `akK9ooZv` | S0 | GBR | 3.10/1.48 | — | 0.6282 (145.8h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 145.8h>48h 作废，须回源 |
| 179 | `bl6AvMkN` | S0 | DEU | 1.61/1.36 | — | 0.6470 (159.1h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 159.1h>48h 作废，须回源 |
| 180 | `bl6KwjwK` | S0 | GBR | 1.89/1.06 | — | 0.4582 (166.3h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 166.3h>48h 作废，须回源 |
| 181 | `d5a2aO7v` | S0 | DEU | 1.66/1.36 | 8 | 0.5451 (48.8h) | — | PASS | 数据缺失 | 0 | 0 | 已提交 ACTIVE / prod 缓存 48.8h>48h 作废，须回源 |
| 182 | `kqN92KpK` | S0 | KOR | 1.91/1.21 | — | 0.6196 (183.3h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 183.3h>48h 作废，须回源 |
| 183 | `leAEYLM8` | S0 | KOR | 1.93/1.72 | — | 0.6856 (209.4h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 209.4h>48h 作废，须回源 |
| 184 | `omEMRpWb` | S0 | IND | 2.45/1.85 | — | 0.3862 (233.6h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 233.6h>48h 作废，须回源 |
| 185 | `pwaQ0bx3` | S0 | DEU | 1.60/1.40 | — | 0.6821 (23.4h) | — | PASS | 未测 | 0 | 0 | 已提交 ACTIVE |
| 186 | `rKRx2Alj` | S0 | DEU | 1.95/1.80 | — | 0.6561 (131.2h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 131.2h>48h 作废，须回源 |
| 187 | `wpo8olA6` | S0 | DEU | 1.65/1.27 | 8 | 0.6306 (25.4h) | 0.5784 | PASS | 放行 | 0 | 0 | 已提交 ACTIVE |
| 188 | `zq3eb7No` | S0 | DEU | 2.01/1.28 | — | 0.6171 (159.2h) | — | CONDITIONAL | 未测 | 0 | 0 | 已提交 ACTIVE / prod 缓存 159.2h>48h 作废，须回源 |
| 189 | `1YNl3p5R` | SX | USA | 2.61/2.38 | — | 0.6011 (6.5h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
| 190 | `78Y01lrZ` | SX | ? | —/— | — | 0.6605 (6.4h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
| 191 | `GrWjwp8Q` | SX | GBR | 3.07/3.08 | — | 0.6705 (2.4h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
| 192 | `LLKq1dKL` | SX | ? | —/— | — | 0.6921 (6.5h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
| 193 | `N1N2WRXo` | SX | GBR | 3.49/3.25 | — | 0.6867 (2.4h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
| 194 | `RReX6k6a` | SX | DEU | 2.92/2.91 | — | 0.5514 (6.7h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
| 195 | `Wjl6JJQO` | SX | EUR | 6.13/4.69 | — | 0.6413 (27.6h) | — | NO_RECORD | 未测 | 0 | 0 | 已提交 ACTIVE |
| 196 | `kqabOm7g` | SX | GBR | 4.53/5.41 | — | 0.6428 (1.9h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
| 197 | `xAvMbRll` | SX | EUR | 3.17/2.45 | — | 0.6281 (6.5h) | — | NO_RECORD | 未测 | 0 | 0 | SA 线，不进 RA 排序 |
