# GLB REGULAR Alpha 战役 — 阶段报告（S-PRE → S1）

- 日期：2026-09-19
- 区域 / 类型：GLB / REGULAR Alpha
- 目标：累计挖掘 **10 颗** REGULAR alpha
- 编排：`wq-brain-ra-pipeline` 九步流水线（S-PRE→S6）
- 用户硬约束：禁止优先选用已点亮塔对应数据集；优先未点亮塔或更低成本数据源
- **当前进度：1 / 10**

---

## 步 1（S-PRE）查表选区选集

### 触发条件
按 kickoff 模板步 1，在开战前完成区域先验盘点，避免重复已判死路径。

### 输入
`get_campaign_summary` / `get_dead_ends` / `get_dead_datasets` / `get_mining_yield` /
`get_ledger_key(region_kb)` / `get_region_config` / `campaign_intel s0-select`。

### 输出

| 项 | 实测值 |
|---|---|
| 波次 | 3 波全 closed（w1=PARTIAL / w2=FAIL / w3=FAIL），submit_ready=0 |
| 死路 | 12 条（覆盖 pv98、intraday_pv_feats、ai_news_scores、analyst_consensus、analyst10、fundamental23、sentiment22、institutions6、insider_agg_matrix、pv106、earnings3、other455） |
| 回测产出率 | **131 条 / 达标 0**（严格口径与宽松口径同为 0） |
| 历史最佳 | \|Sharpe\| 最高 1.39、fitness 最高 0.47 —— **1.58 / 1.0 硬闸从未被触及** |
| 积压 | 363 条表达式（gem 203 / pending 154 / selected 6），转化率 36%，232 条未消费 |
| 点塔状态 | **0 / 13 已点亮** |

### 关键发现：设置锁死在 0% 过闸格

GLB 当前设置正好落在 inventory 1000 样本的 0% 过闸格里：

| 维度 | 当前设置 | 实测过闸率 | 合法替代 | 实测过闸率 |
|---|---|---|---|---|
| universe | TOP3000 | **0%**(n=25) | TOPDIV3000 | **27.5%**(n=262) |
| neutralization | SUBINDUSTRY | **0%**(n=53) | STATISTICAL | **77.6%**(n=76) |
| decay | 4 | **0%**(n=15) | 2 | **90.9%**(n=22) |

字段族正证据 `probability` 64.5%(n=248)、`quantile` 45.2%(n=31)；负证据 `anl` 0%(n=108)、`analyst` 0%(n=44)。
胜绩配方 `group_rank(ts_rank(...), country)`（GLB 三区域 AMER/EMEA/APAC 检查依赖 COUNTRY 分组）。

### 异常信息
**停止规则 A 命中**（`campaign.py:1222`：回测 131 ≥ `yield_min_backtests`=100 且达标 0）→ 机械拒绝开波。
规则 B 未命中（最近 3 波为 PARTIAL/FAIL/FAIL，非全 FAIL）。

### 处置
用户确认放行 → 写 ledger `stop_rules_override`（至 2026-09-30，reason 记录「零产出归因于设置锁死而非信号空间穷尽」）
+ `settings.json` 全切 `TOPDIV3000 / STATISTICAL / decay 2`。

### 用户约束的落地效果
GLB/D1 平台实测 **0/13 塔点亮**，「优先未点亮塔」在本区**剔除 0 个**，属无效约束。
改用 **alphaCount 拥挤度**作为「低成本」判据（拥挤度直接对应 prod_corr 撞墙风险）。

---

## 步 1 前置：库存盘点（SOP 强制）

### 触发条件
SOP「先清库存，再开新挖」——实证数量级差异（跨四区 170 次新回测产出 0 条 vs 一次库存扫描产出 20 条）。

### 输出：235 条候选的严格复核

| 层 | 数量 |
|---|---|
| 原始候选（过闸率 23.5%） | 235 |
| 剔除 EMOTION `ohlcv_img` 族（实证 PROD 0.82–0.86 判死） | −181 |
| 剔除 `predicted_first_quantile_ten_day_return_*`（prod 0.9989 墙） | −30 |
| 非判死族 | 24 |
| 过 GLB 全硬闸（S≥1.58 / F≥1.0 / tvr 5–30% / 2Y≥1.6 / sub≥1.0） | 20 |
| **去重后独立字段组合** | **4** |

### prod 实测（唯一绑定约束）

| alpha | 字段 | S | F | tvr | 2Y | prod | 判定 |
|---|---|---|---|---|---|---|---|
| **le3E3nM7** | `mean_last_trade_price_return_30m_pre_close_2` | 2.06 | 1.24 | 11.35% | 2.00 | **0.6708** | ✅ 可提交 |
| 88eE7WoW | `max/min_last_trade_price_60m_pre_close_2` | 1.96 | 1.54 | 11.30% | 3.37 | 0.8956 | ❌ prod 墙 |
| YPgOWZgR | `img_feature1_leapstar1batch1_day1` | 1.72 | 1.04 | 5.04% | 1.77 | 0.8802 | ❌ prod 墙 |
| d5Roda1j | `mean_estimate_change_pct_fy1_earnings_60d_4` | 1.66 | 1.06 | 6.42% | 2.12 | 0.8011 | ❌ prod 墙 |

**结论**：独立结构仅 4 个、可提交仅 1 颗 —— 不足以覆盖 10 颗目标，SOP 判据成立，进入新挖。
同时再次确认核心瓶颈是 **prod 墙**（4 颗里 3 颗撞），不是 IS 强度。

---

## 步 8（提前触达）：首颗提交

`submit_verdict` 判定 `le3E3nM7` 位于 SOP 规定的「prod 0.60–0.70 当天提交、先不做变体」区间，
用户确认后立即提交。

### 结果：**ACTIVE**（进度 1/10）

| 指标 | 值 |
|---|---|
| 表达式 | `-group_rank(ts_decay_linear(ts_backfill(mean_last_trade_price_return_30m_pre_close_2, 66), 34), industry)` |
| Sharpe / Fitness | 2.06 / 1.24 |
| Turnover / Returns / Drawdown | 11.35% / 4.5% / 3.57% |
| 2Y Sharpe / 子宇宙 | 2.00 / 1.18 |
| 三区域 AMER / EMEA / APAC | 1.43 / 1.02 / 1.16（全过 limit 1.0） |
| risk_neutralized_sharpe | **2.05**（≈ raw，真信号而非纯因子暴露） |
| PROD / SELF | 0.6708 / 0.0（均 PASS） |
| 设置 | MINVOL1M / D1 / decay 6 / COUNTRY / trunc 0.02 |
| 金字塔 | `GLB/D1/PV`，multiplier 1.0，**1/3 点亮** |
| 配额 | REGULAR_SUBMISSION value=2 / limit=4 |

### 副产物：死路结论被实证推翻

获胜字段属 **`intraday_pv_feats`**，而该集已被 `GLB-W02-INTRADAY-PV-TURNOVER-WALL` 判死。
实证表明判死范围应**收缩为该骨架**（wave02 `corr_*_with_slippage` 裸字段短窗，turnover >70%），
而非整个数据集 —— `ts_backfill(66) + ts_decay_linear(34) + group_rank(industry)`
把 turnover 从 >70% 压到 11.35%，**turnover 墙是骨架问题不是数据缺陷**。
已写 ledger `dead_end_amendment_intraday_pv_feats`，该集以 win-leg 重新纳入白名单并锁定骨架。

---

## 步 2（S0）数据集体检与白名单

### 触发条件
停止闸放行 + 设置切换完成 → `score_datasets` 双步（calibrate 写回阈值 → 打分产出排名）。

### 输出

- **calibrate**：实测 11 集 / 117 alphas；category 权重写回 `thresholds.json`
  （other 1.15 / pv 1.15；fundamental·insiders·institutions·analyst·earnings 0.9），拥挤甜区 ac 161–1719。
- **打分**：以 **TOPDIV3000** 重生成 141 集排名（旧榜锁 TOP3000，按 P3 守卫覆盖）。
- **点塔视角 Top**：news31、pv106、news73、other699、other296、other546、other315、other455、pv37、intraday_pv_feats。

### 锁定白名单（11 集）

| 角色 | 数据集 | 拥挤度 alphaCount | 覆盖 | 字段数 |
|---|---|---|---|---|
| **win 换腿** | intraday_pv_feats | — | 0.815 | 586 |
| Tier A 低拥挤 | other546 | 24 | 0.662 | 10 |
| | other699 | 66 | 0.776 | 14 |
| | other296 | 100 | 0.753 | 10 |
| | news73 | 133 | 1.000 | 22 |
| | other315 | 150 | 0.618 | 20 |
| | news31 | 181 | 0.826 | 44 |
| | model135 | 184 | 1.000 | 137 |
| Tier B（需 prod-first） | pv30 | 627 | 0.859 | 150 |
| | pv37 | 1429 | 1.000 | 80 |
| | sentiment21 | 1477 | 0.913 | 210 |

金字塔配额闸：非 MODEL 9 个、5 个 category → **PASS**。

### 异常信息
1. 首次 calibrate 因 `settings.json` 被改坏（JSON 残留旧串）崩在 `CampaignContext`；已修复并 `json.load` 校验通过。
2. **体检包缺口**：本地 `research-data/WebData_20260219_V0.10.9.zip` 不存在，
   `gen_field_inspect_packs` 报「数据包不存在」。GLB 现仅 6 个旧包（analyst15 / analyst47 / model106 / model109 / news87 / other432），
   **无一覆盖新白名单**。按 SOP 显式降级 `--inspect-mode warn` 并记台账 `s0_inspect_pack_gap`。
   代价：步 5 体检硬门本波不生效，低覆盖 / 厚尾 / 稀疏事件的预处理约束需人工复核。

---

## 步 3（S1）字段扫描

### 触发条件
白名单锁定 → 建 typed catalog（步 5 门禁的前置，缺目录 stage_gate 直接 FAIL）。

### 输出
`intraday_pv_feats` catalog：**586 字段，data_type 全 MATRIX**，已入库（fresh）。
其中 `pre_close` 族 70 个字段，coverage 0.998–0.9996，语义分组为
last_trade / bid / ask / high / low / vwap 的 30m 与 60m return，以及 trade_volume、bid_ask_size_ratio、slippage、price_modulo。

---

## 下一轮待办

1. **S1 补扫** Tier A 集：other546 / other699 / other296 / news73 / other315 / news31 / model135。
2. **S2 GEM 生成**：win 换腿 ≥2 槽（`intraday_pv_feats` 锁骨架
   `-group_rank(ts_decay_linear(ts_backfill(x, >=66), >=22), industry|country|market)`），
   其余按七槽分配（≥2 跨金字塔、弱探针最多 1 槽）。
   ⚠ 扩变体前**必须**先算本地 mutual correlation —— 同族兄弟变体 SELF 0.9+ 自相残杀，一族只留 1 颗。
3. **步 5b prod-first**：新信号族投入第二波前，先用 1–2 条骨架查 `check_correlation(production)`；
   prod ≥0.7 记 dead_end 换机制，0.60–0.70 直接进步 8 提交。
4. **补体检包**：更新 WebDataScope 导出包 → `gen_field_inspect_packs --region GLB` → 切 `--inspect-mode enforce`。

---

## 台账写入清单（本轮）

| key | 内容 |
|---|---|
| `stop_rules_override` | 放行理由 + settings 变更 + until 2026-09-30 |
| `s0_whitelist` | 11 集白名单 + universe 锁定 + win-leg 骨架约束 |
| `s0_dead_excluded` | 12 条判死集 + 超拥挤集 |
| `s0_lit_tower_check` | 0/13 点亮核验 |
| `s0_inspect_pack_gap` | 体检包缺口与降级决策 |
| `inventory_scan_20260919` | 235→4 的漏斗与 4 个种子 |
| `submit_log_20260919` | le3E3nM7 ACTIVE 全指标 |
| `dead_end_amendment_intraday_pv_feats` | 死路收缩修正 |


---

# 续挖阶段（23:32 – 00:15）：S1 补扫 → S2 → S3 → S4

## 步 3 续（S1 补扫）

| 数据集 | 字段数 | data_type |
|---|---|---|
| intraday_pv_feats | 586 | **MATRIX** |
| model135 | 137 | VECTOR |
| news31 | 44 | VECTOR |
| news73 | 22 | VECTOR |
| other315 | 20 | VECTOR |
| other699 | 14 | VECTOR |
| other546 | 10 | VECTOR |
| other296 | 10 | VECTOR |

**win 换腿 `intraday_pv_feats` 是白名单里唯一 MATRIX 集** —— 其余 7 个低拥挤集全为 VECTOR，需 `vec_*` 算子，尚未触碰。

## 异常信息：积压闸拦截

`assemble-priors` 被第三道闸拦下：conversion=0%、pending+gated 42%。核对后 363 条积压中 **323 条属判死集**，
唯一非判死是 `s2_intraday_pv_feats_d1` 的 40 条（corr_* 短窗族）。已写 `backlog_gate_override` 放行。
信号天花板闸 PASS（max|sh|=0.85 / 2 批，floor 0.5）。

## 步 4（S2）GEM 两轮均空转

`phased` 产出 336 条、`skeleton` 产出 39 条，**零条 pre_close、零条 win 骨架**。
根因：字段池 30 个虽含 5 个 pre_close，但 `field_whitelist` 过滤把它们剔除（s1 报「32 个模板字段不在绑定池」）。
→ GEM 前置依赖 `s2_field_pool` 与 `field_whitelist` 对齐；换主攻字段簇必须先修绑定池，否则 GEM 空转。

改用 win 配方直写（`upsert_expressions`，source=win_recipe）：8 条
`-group_rank(ts_decay_linear(ts_backfill(<pre_close_field>, 66), 34), industry)`，
字段跨 8 种语义（last_trade / bid / ask / vwap / high / low return、trade_volume、bid_ask_size_ratio），
per-item settings 跟 win（MINVOL1M / COUNTRY / decay6 / trunc 0.02）。门禁 8/8 PASS。

## 步 6（S3）回测：8/8 COMPLETE

| alpha | Sharpe | Fitness | Turnover |
|---|---|---|---|
| E5pYL2rP | **1.89** | 1.11 | 11.40% |
| RRbqKv2g | 1.83 | 1.05 | 11.40% |
| 6Xj3J2RP | 1.61 | 0.91 | 9.29% |
| JjNY12gn | 1.44 | 0.77 | 11.32% |
| blbVnKo6 | 1.38 | 0.72 | 11.25% |
| 78N0M2xv | 1.21 | 0.49 | 9.95% |
| npdYQXnd | 0.22 | 0.06 | 2.09% |
| N1aq32np | −0.43 | −0.17 | 9.70% |

**turnover 全部 9–11.5%** —— 再次证实 turnover 墙由骨架解决（原判死骨架 >70%）。

## 步 7/8（S4）判定：两条最强均 BLOCKED

| alpha | AMER | EMEA | APAC | 2Y | 判定 |
|---|---|---|---|---|---|
| E5pYL2rP | — | **0.44** | **0.92** | **1.06** | BLOCKED |
| RRbqKv2g | — | **0.77** | **0.98** | **1.29** | BLOCKED |
| le3E3nM7（对照·已 ACTIVE） | 1.43 | 1.02 | 1.16 | 2.00 | PASS |

### ★ 瓶颈迁移

GLB 的绑定约束已由 **prod 墙**（库存 3/4 撞）迁移到 **三区域检查 + 2Y 墙**（新挖 8/8 撞）。
三区域检查要求 AMER / EMEA / APAC 子宇宙各自 sharpe ≥ 1.0，全球组合极易在 EMEA / APAC 塌方。
`le3E3nM7` 是 pre_close 族中唯一同时过三区域 + 2Y 的组合 —— 换字段即失去区域平衡。

## 当前进度

**1 / 10 ACTIVE**（le3E3nM7）。今日剩余 REGULAR 配额 4。

## 下一轮方向（按期望排序）

1. pre_close 族继续换字段，但**优先挑 EMEA / APAC 覆盖高的字段**（volume / size_ratio 类比 price return 类区域更均衡）。
2. 换 group 维度（country / market 分组替代 industry）改善区域平衡。
3. 修 `s2_field_pool_intraday_pv_feats` 绑定池后重跑 GEM，让其真正装配 pre_close 骨架。
4. Tier A 的 7 个 VECTOR 集是全新信号空间，尚未触碰。
