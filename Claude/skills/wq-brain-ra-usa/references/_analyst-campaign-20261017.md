# USA × Analyst 战役实证（campaign_20261017，15 波 / 60 条）

> 区域锁定 USA。**结论先行：analyst44 EPS 修正率通过全部 IS 闸，但 prod 0.7775 撞墙。**

## ★★★ 一、头号结论：USA 分析师族的瓶颈是 **prod**，不是 IS 指标

**最优候选 `78oX5VnQ`（EPS 修正率）实测**：

```text
quantile(group_rank(ts_av_diff(divide(subtract(vec_avg(anl44_2_eps_value), vec_avg(anl44_2_eps_prevalue)),
        add(vec_avg(anl44_2_eps_value), vec_avg(anl44_2_eps_prevalue))), 504), sector))
USA / TOP3000 / D1 / SECTOR / decay 10 / trunc 0.08
```

|        S |        F |       2Y |      SUB |     TO | returns | margin |   self-corr | **prod-corr** |
| -------: | -------: | -------: | -------: | -----: | ------: | -----: | ----------: | ------------: |
| **1.77** | **1.29** | **1.71** | **0.81** | 0.1195 |   6.66% | 11.2bp | **0.578 ✓** |  **0.7775 ❌** |

⇒ **IS 侧全部通过**（`submit_verdict`: `failed_ra=0 / failed_ppa=0 / hard_gate_warnings=[]`），  
`self-corr 0.578` 通过，**唯一阻断 = prod 0.7775 > 0.7**。  
⇒ 这与既有证据 `USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL`（E/P z prod 0.93）同源：  
**USA 分析师族已被生产池高度覆盖**。  
⇒ ★★ **「USA analyst 19 条回测 / RA 全过 = 0」的真正原因**：不是 IS 指标不行，是 prod 饱和。

## ★★★ 二、头号字段发现：`anl44_2_*_value` / `_prevalue` = **αC 0 的事件级修正配对**

`analyst44` 300 字段全 VECTOR，但真正可用的是 D2 事件流的配对：

| 指标                                                                                 |  cov(value) | cov(prevalue) |    revision 后 S |
| ---------------------------------------------------------------------------------- | ----------: | ------------: | --------------: |
| **eps**                                                                            |       0.958 |         0.953 | **1.77–1.80** ★ |
| sales                                                                              |       0.957 |         0.950 |            1.61 |
| netprofit                                                                          |       0.952 |         0.946 |            1.36 |
| ebit                                                                               |       0.940 |         0.930 |            1.22 |
| pretaxprofit                                                                       |       0.940 |         0.935 |            1.00 |
| ebitda / roe / nav / capex / bps / dps / grossmargin / netdebt / roa / cfps / epsr | 0.676–0.935 |   0.610–0.928 |       0.45–1.32 |

⇒ **17 个配对中只有 EPS 达标**（sales 差 3 闸，其余 S ≤ 1.36）。  
⇒ **EPS 是分析师真正修正的指标**，其他指标（ebit/ebitda/netprofit…）的修正率信号弱。  
⇒ **排除项**：`operatingprofit`(cov 0.21–0.31)、`tbvps`(0.37–0.39)、`ebitdaps`(0.40–0.42)、  
`fcfps`(0.50–0.53) **低于/临界 0.5 硬闸**；`*_lastactccy`/`*_coveredby` 是字符串语义；  
`best_pe_ratio` αC 399 极拥挤。

## ★★★ 三、机制裁决：analyst44 只有 **revision** 有信号

| 机制                                  |        最优 S |        2Y |  SUB | 判定                          |
| ----------------------------------- | ----------: | --------: | ---: | --------------------------- |
| **breadth**（`4wk_up/dn/chg/numest`） |    **0.30** | 0.50–1.11 | 0.36 | ❌ 判死（与既有 `BREADTH-DEAD` 一致） |
| **dispersion**（`*_stddev`）          | 0.98（三指标复合） |  **2.39** | 0.41 | ⚠ 2Y 极强但 S/SUB 不足           |
| **revision**（`value/prevalue`）      |    **1.80** |      1.71 | 0.81 | ★ IS 全闸                     |

⇒ **dispersion 值得注意**：2Y 高达 2.39（本族最高），但 S 仅 0.98 ⇒  
在 TO<0.125 下 fitness 不足。**若未来有更强的 dispersion 载体可复用此机制。**

## ★★★ 四、算子杠杆（analyst revision 族实测）

| 算子/设置                                 |        S |        F |       2Y |      SUB |
| ------------------------------------- | -------: | -------: | -------: | -------: |
| `ts_zscore(ts_backfill(...,252),252)` |     1.09 |     0.46 |     1.61 |     0.32 |
| **`ts_av_diff(...,252)`**             | **1.54** |     0.75 |     1.57 |     0.42 |
| **`ts_av_diff(...,504)` + SECTOR**    | **1.77** | **1.29** | **1.71** | **0.81** |
| `ts_av_diff(...,756)`                 |     1.64 |     1.13 |     1.65 |     0.57 |
| `ts_av_diff(...,126)`                 |     1.11 |     0.47 |     1.52 |     0.31 |
| `winsorize(ts_av_diff,std=3)`         |     1.59 |     1.07 |     1.51 |     0.65 |
| 轴 market                              |     1.80 |     1.33 |     1.71 |     0.78 |
| 轴 subindustry                         |     1.66 |     1.09 |     1.56 |     0.66 |
| TOP2000                               |     1.48 |     0.76 |     1.70 |     0.69 |

⇒ ★★ **`ts_av_diff` 再次战胜 `ts_zscore`（+41%）** —— 第四次跨族验证该铁律。  
⇒ ★ **窗 504 是甜点**（252 的 SUB 0.42、756 的 SUB 0.57，均不如 504 的 0.81）。  
⇒ ★ **SECTOR 中性化 > 其它轴**（SUB 0.81 最高余量）。

## ★★ 五、`analyst7` 判弱：固定滞后窗口 vs 事件级配对

`analyst7` 300 字段全 MATRIX、cov 恒 0.5，修正配对为 `est_12m_*_mean` vs `_mean_4wks_ago`/`_3mth_ago`：

| 机制                 |    S |       2Y |  SUB |    TO |
| ------------------ | ---: | -------: | ---: | ----: |
| 4 周修正率             | 0.87 |     1.28 | 0.77 | 0.044 |
| 3 月修正率             | 0.91 |     1.07 | 0.59 | 0.029 |
| 广度（raised−lowered） | 0.95 | **1.57** | 0.45 | 0.094 |
| 分歧（std）            | 0.69 |     0.70 | 0.25 | 0.037 |

⇒ **全机制弱于 analyst44**（S ≤ 0.95 vs 1.77）。  
⇒ ★★ **判据（可迁移）：修正类信号用「事件级配对」（`value`/`prevalue`）优于  
「固定滞后窗口配对」（`mean`/`mean_4wks_ago`）** ——  
后者过平滑（TO 0.029–0.044），信号被窗口平均抹平。

## ★★ 六、论坛方法在 analyst 族的适用性

| 方法                      | 论坛来源                 | analyst 族实测                | 判定                         |
| ----------------------- | -------------------- | -------------------------- | -------------------------- |
| `rank_by_side`          | 70 票专帖（2Y 0.28→2.44） | **本账号无该算子**（103 算子核实）      | ⚪ 不可用                      |
| 中性化换 RAM/CROWDING（修 2Y） | LC69991 / ZZ47696    | RAM 使 2Y 1.71→**1.33**（反向） | ❌ **限高换手线（TO>0.2）**，低换手线无效 |
| 内层 `group_neutralize`   | ZZ47696（P²=P 铁律）     | 同粒度退化为恒等                   | ✅ 铁律成立                     |
| 拉长 `ts_backfill` 窗      | PY82964              | 本族用 `ts_av_diff` 窗 504 更好  | ⚠ 算子选择优先于窗口                |

## 七、本族判死 / 保留清单

**判死**：

- `analyst44` **breadth 全族**（`4wk_up`/`4wk_dn`/`4wk_chg`/`numest`）S ≤ 0.30
- `analyst44` **16 个非 EPS 指标的 revision**（S ≤ 1.36，2Y 多 ≤ 1.35）
- `analyst7` **全机制**（S ≤ 0.95）
- `analyst44` **dispersion 单独使用**（S 0.98，fitness 0.38 不足）

**保留（prod 墙待破）**：

- `analyst44` **EPS 事件级修正率** = `78oX5VnQ`（IS 全闸 + self 0.578 ✓，**prod 0.7775 ❌**）
- `analyst44` **EPS 分歧度** 2Y 2.39（机制有效，等更强载体）

## 八、下一步（prod 导向）

1. **探针阶段就跑 `check_correlation(refresh=True)`**，prod > 0.7 立即判死，不浪费算子扫。
2. **降 prod 的候选杠杆**（未测，按推测排序）：  
   换 universe（TOP1000/500 改变持仓集合）、`trade_when` 子集门控、与低相关字段 `vector_neut`。
3. **不要在同族磨窗口/轴**：这些只改 IS 指标，**不改 prod**。

---

## 九、★★★ prod 墙攻坚实证：prod 对什么敏感？（本轮最重要的机理发现）

在确认 `78oX5VnQ`（IS 全闸、prod 0.7775）后专项攻 prod，**形成双向墙**：

| 变体                          |        S |        F |        2Y |       SUB |    TO |              **prod** |
| --------------------------- | -------: | -------: | --------: | --------: | ----: | --------------------: |
| 基线（sector 轴）                | **1.77** | **1.29** |      1.71 |  **0.81** | 0.120 |            **0.7775** |
| **`hump(0.02)`**            |     1.52 |     0.97 |  **2.05** |      0.78 | 0.055 |          **0.7407** ★ |
| `hump(0.01)` / `hump(0.05)` |     1.52 |     0.97 | 2.03/2.05 | 0.78/0.77 | 0.055 | 同（**hump 值不敏感，固定代价**） |
| **二阶差分（加速度）**               |     1.54 |     1.11 |  **2.25** |      0.70 | 0.132 |          **0.8175** ❌ |
| `vector_neut(·,eps_numest)` |     0.76 |     0.45 |      0.72 |      0.22 | 0.078 |                     — |
| `trade_when(numest>10)`     |     0.71 |     0.40 |      1.59 |      0.66 | 0.037 |                     — |
| `trade_when(numest>3)`      |     1.49 |     1.04 |      1.71 |      0.71 | 0.101 |                     — |
| TOP1000+decay5              |     0.76 |     0.28 |      0.46 |      0.68 | 0.268 |                     — |

### ★★★★ 核心判据

> **prod correlation 只对「PnL 时序结构 / 持仓集合」的改变敏感，  
> 对「信号数学形式的改变」不敏感。**

- **换机制**（revision 水平 → 二阶差分）⇒ prod **升**到 0.8175  
  ⇒ 两者共享同一底层字段的一阶信息，PnL 日序列高度相似。
- **改交易时点**（`hump` 限制单日调仓）⇒ prod **降**到 0.7407  
  ⇒ PnL 时间路径被真正改变。
- **换宇宙/门控** ⇒ IS 崩塌（EPS 修正只在大中盘全覆盖池有功效）。

⇒ **降 prod 的正确方向：改「何时交易 / 交易什么」，不是改「如何计算信号」。**  
⇒ 本轮新增：**`hump` 是低换手族唯一可用的 prod 降杠杆**（TO 0.120→0.055），  
但**代价固定且不可回收**（S −0.25、F −0.32），且**降幅不足以过闸**（0.7407 仍 >0.7）。

### 双向墙结论

```
无 hump：IS 全闸（S1.77/F1.29/2Y1.71/SUB0.81）→ prod 0.7775 ❌
加 hump：prod 0.7407（仍 ❌）                    → S1.52/F0.97 ❌
```

⇒ **`analyst44` EPS 修正率在 USA 结构性不可提交**。  
⇒ 与 `USA-ANALYST44-BREADTH-DEAD-EP-PRODWALL`（prod 0.93）同族同病。  
⇒ ★ **「USA analyst 19 条回测 / RA 全过 = 0」的根因 = prod 饱和，非 IS 指标。**

## 十、方法学增补（写进本 skill 的通用规则）

1. **探针阶段就跑 `check_correlation(refresh=True)`**：prod >0.7 立即判死，  
   不要先花 20 条回测优化 IS——IS 再好也过不了 prod。
2. **prod 降杠杆优先级**（低换手 TO<0.15 族）：  
   `hump` > 换 universe（但常摧毁 IS）> `trade_when` 门控（常摧毁 IS）
   > **换机制（无效，甚至反向）** > `vector_neut`（摧毁信号）。
3. **`hump` 的行为特征**：hump 值 0.01/0.02/0.05 结果几乎相同（固定代价），  
   不需扫参；它把 TO 砍半、2Y 抬 0.3，但 S 掉 0.25、F 掉 0.32。
4. **修正类信号只用事件级配对**；固定滞后窗口（`_4wks_ago`/`_3mth_ago`）过平滑，信号被抹平。
5. **发批前逐条核对表达式互异性**（本轮误发 4 条相同表达式，浪费 3 槽）。

---

## ★★★★★ 十三、破 prod 墙的钥匙：`REVERSION_AND_MOMENTUM` 中性化（本战役头号结论）

### 13.1 实证：同一信号只换 neutralization

USA analyst44「eps−sales 修正背离 + hump + 756 窗 + market 轴」：

| neutralization | S | F | 2Y | SUB | TO | **prod** | 判定 |
|---|---:|---:|---:|---:|---:|---:|---|
| SECTOR | 1.77 | 1.21 | 2.03 | 0.77 | 0.095 | 0.703–0.720 | ❌ |
| STATISTICAL | 1.77 | 0.89 | 2.43 | 0.53 | 0.156 | — | ❌ IS 挂 |
| MARKET | 1.58 | 1.14 | 1.02 | 0.76 | 0.133 | — | ❌ 2Y 挂 |
| INDUSTRY | 1.85 | 1.15 | 2.02 | 0.59 | 0.097 | — | ❌ SUB 挂 |
| **REVERSION_AND_MOMENTUM** | **1.81** | **1.25** | **1.82** | **0.83** | 0.111 | **0.6481** | ✅ **全过** |

⇒ ★★★★★ **RAM 中性化一石三鸟**：S 最高档（1.81）+ SUB 高（0.83）+ **prod 最低（0.6481）**。
⇒ 机理：RAM 剥掉「反转/动量」风格暴露后，信号与生产池的分析师 alpha 重叠大幅下降；
  同时残余信号更「纯」（不靠动量/反转收益）⇒ sub-universe 表现更好。

### 13.2 本战役唯一全闸通过 alpha（`npAONOVa`）

```text
quantile(group_rank(hump(ts_av_diff(subtract(
    divide(subtract(vec_avg(anl44_2_eps_value), vec_avg(anl44_2_eps_prevalue)),
            add(vec_avg(anl44_2_eps_value), vec_avg(anl44_2_eps_prevalue))),
    divide(subtract(vec_avg(anl44_2_sales_value), vec_avg(anl44_2_sales_prevalue)),
            add(vec_avg(anl44_2_sales_value), vec_avg(anl44_2_sales_prevalue)))), 756), hump=0.01), market))
USA / TOP3000 / D1 / REVERSION_AND_MOMENTUM / decay 10 / trunc 0.08
```
**S 1.81 / F 1.25 / 2Y 1.82 / SUB 0.83 / TO 0.111 / returns 5.94% / prod 0.6481 / self 0.3861**
`failed_ra_count=0`（八闸全过）+ `all_passed: true`。ATOM 合规（单数据集 analyst44）。

### 13.3 ★★★ 可迁移铁律：prod 墙先换 neutralization，再换算子

> **USA 分析师族（以及所有高拥挤类别）破 prod 墙的第一杠杆 = 换 `REVERSION_AND_MOMENTUM` 中性化，
> 而不是继续磨算子/窗口/轴。**

判据（按优先级）：
1. **IS 全过但 prod 0.70-0.75** ⇒ 直接换 RAM 中性化重跑（成本 1 条 sim，本族实测 prod −0.055）。
2. **IS 全过但 prod >0.75** ⇒ RAM 可能仍不够，需换机制（本族加速度 prod 0.838 无救）。
3. **RAM 也不够** ⇒ 换数据集/类别（该信号与生产池深度重叠）。

### 13.4 本轮全部实证结论汇总（ analyst44，21 波 / 96 条本 session）

1. **修正率机制**：`(value−prevalue)/(value+prevalue)` + `ts_av_diff(756)` + hump 是本族最强骨架。
2. **背离机制**：eps−sales（盈利质量）唯一强配对；8 配对横扫结论。
3. **`hump` 参数不敏感**（0.01–0.05 同效）⇒ 不需扫参。
4. **`truncation` 对秩信号无效**（0.02/0.04/0.08 逐位相同）。
5. **TO<0.01 触发 LOW_TURNOVER 闸**（太慢也是罪）。
6. **两难墙**：SECTOR 族下 SUB 要低换手、prod 要高换手 ⇒ 无交叉点；
   **RAM 中性化同时解开两闸**。
7. **`ts_av_diff` 第五次跨族取胜**（vs `ts_zscore`，+41%）。
8. **prod 与机制经典度正相关**：水平背离 0.70 < 秩背离 0.75 < 纯修正 0.78 < 加速度 0.84。
9. **加速度 prod 0.838 无救**（二阶导是生产池最拥挤的分析师信号）。
10. **秩背离 prod 0.754** ⇒ RAM 化后待测（在飞）。

---

## ★★★★★ 十四、任务达成：10 个全闸 ATOM alpha（2026-10-18 交付）

完整清单与构造逻辑见 `tracking/USA/campaign_20261017/05_final_delivery_10_alphas.md`。

### 交付配方（可复现）

```text
quantile(group_rank(hump(ts_av_diff(SIGNAL, W), hump=0.01), AXIS))
USA / TOP3000 / D1 / {REVERSION_AND_MOMENTUM | CROWDING} / decay {10 | 20} / trunc 0.08
```
- SIGNAL = 背离：`subtract(divide(sub(v(eps_value),v(eps_prevalue)),add(...)), divide(sub(v(sales_value),v(sales_prevalue)),add(...)))`
- SIGNAL = 加速度：`ts_delta(<背离>, 252)`
- SIGNAL = 秩背离：`subtract(rank(eps_rev), rank(sales_rev))`
- W ∈ {504, 756}，AXIS ∈ {sector, market}

### ★ 机制 × 中性化适配矩阵（实测）

| 机制 | RAM | CROWDING | SECTOR |
|---|---|---|---|
| 水平背离 | ✅ prod 0.648-0.698 | ✅ prod 0.644-0.675 | ❌ 0.703-0.72 |
| 背离加速度 | ✅ prod 0.689-0.698 | ❌ 0.772 | ❌ 0.838 |
| 秩背离 | ✅ prod 0.642 | ✅ prod 0.676 | ❌ 0.754 |

⇒ **换机制时必须重测中性化适配**（加速度只认 RAM，水平背离两者皆可）。

---

## ★★★★★ 十五、提交实证（2026-10-18）：2 个 ACTIVE + 三条铁律

### 15.1 已提交（base payment 导向选择链）

| alpha | name | 机制 | F | PC | self | 状态 |
|---|---|---|---:|---:|---:|---|
| `gJWoaJqv` | USA_R_ANALYST_03 | 背离加速度 d252/504/market/RAM/d20 | **1.27** | 0.6978 | 0.5803 | **ACTIVE/OS** |
| `kqJLawqP` | USA_R_ANALYST_04 | 秩背离 756/market/CROWDING | 1.11 | 0.6757 | 0.6445 | **ACTIVE/OS** |

### 15.2 base payment 最大化选型标准（论坛实证，替代「按 returns」的错误直觉）

> **高 fitness + 低 PC（prod correlation）= base payment 版本答案**；self-corr < 0.3 是 BP>1.5 的强信号；
> `returns` 只影响 OS 特许权使用费、不影响 BP 档位；VF（Value Factor）是账号级乘数、同批候选无差异。

实操链：`F×(1−PC) 粗排 → robustness Phase B/C → 提交时 PC 重测 → self 互残检查 → 提交`。

### 15.3 ★★★★ 三条提交层铁律（本次实证）

1. **MCP `workflow_submit_alpha` 的 `fetch failed` ≠ 未提交**：实测 POST 已送达、flip 在 ~240s 后完成；
   早期（<2min）查到的 UNSUBMITTED 是翻转未完成。**fetch failed 后等满 flip 窗口再判；
   换路径重试前必须复查**（否则 403 重复提交）。
2. **提交即改变相关格局**：新 alpha 同时进 prod+self 两池，同族候选相关度暴涨（0.70→0.98）。
   ⇒ 同族批量提交**必须逐个来**，每提交一个即重测剩余候选 PC+self，互残 >0.9 放弃。
3. **PC 只向上漂**（生产池单调增长）：同日早→晚实测全部 +0.01~+0.29。
   ⇒ 提交前必须重测 PC；「早上过线」不构成下午可提交的依据。

### 15.4 同族互残的结构性上限（本数据集）

analyst44 的三种机制变体（水平背离/加速度/秩背离）在 PnL 层高度共线：
同机制互相关 0.98、跨机制 0.68-0.94（秩背离 vs 水平背离 0.94）。
⇒ **单数据集同族最多提交 2-3 个**，第 N 个必被 self 闸顶爆。
要凑更多提交数必须换数据集/机制族（Analyst 类别已尽：analyst44 挖尽、analyst7 判死、analyst_consensus 已点亮被排除）。
