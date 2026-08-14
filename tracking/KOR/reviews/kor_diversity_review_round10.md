# KOR/D1 挖掘战役 — 第 10+ 轮回测多样性评估与 Skill 优化总结

日期：2026-08-14 ｜ 战役：KOR_D1_TOP600 ｜ 门槛：sharpe>1.58, fitness>1, 2y>1.6, margin>5bp, TVR 5–30%, RA 全过

## 一、回测轮次盘点（共 15 批 / 97 表达式）

| 波次 | 数据集 | 批数 | 表达式 | 设置 | 结果 |
|---|---|---|---|---|---|
| wave1 | pattern_scores | 6 | 49 | SECTOR d4 t0.08 | 49/49 COMPLETE，0 达标（best sh 0.70 omNG78w2） |
| wave2 | acquisition_model | 3 | 24 | STATISTICAL d8 t0.06 + SECTOR | 24/24 ERROR（ts_backfill 不支持 event） |
| wave2v2 | acquisition_model | 3 | 24 | 同上（去 backfill） | 24/24 ERROR（rank/ts_delta 等全部不支持 event） |
| wave3 | ml_factor_proj | 3 | 24 | STATISTICAL d8 t0.06 ×2 + SECTOR d4 t0.08 | 回测中 |

## 二、多样性量化评估

### 1. 操作符探索率
- 已使用：rank, subtract, add, multiply, ts_delta, ts_av_diff, ts_zscore, ts_rank, ts_delay, ts_backfill（10 个）
- FASTEXPR 常用算子池约 80+，**探索率 ≈ 12%**
- 盲区：ts_regression(.resid/.coef)、signed_power、trade_when、bucket、winsorize、scale、ts_decay_linear、paste_rank、group_neutralize 均未尝试
- wave3 起引入 ts_av_diff 双窗差（加速度）；若 sh<1.2 则下一轮补 ts_regression.resid 与 signed_power 风格

### 2. 字段探索率
- pattern_scores：49 表达式仅覆盖 ~12 字段（breakout/reversal/structure 族），探索率 <30%
- acquisition_model：15/15 字段 100% 探索但全废（event 类型）
- ml_factor_proj：333 字段仅用 15 个（4.5%），**零竞争字段储备极充足**（change_* 全族 alphaCount=0）
- 结论：字段是当前最不缺的资源，瓶颈在"字段类型预检"与"信号风格匹配"

### 3. 模板骨架多样性（8 种骨架）
| 骨架 | 波次 | 表现 |
|---|---|---|
| rank(F) 单因子 | w1,w3 | 基线 |
| subtract(rank(A),rank(B)) rank-diff | w1,w2,w3 | 论坛 KOR 1.76 同款 |
| ts_delta(rank(F),n) 动量增量 | w2,w3 | 待验证 |
| ts_av_diff 双窗差（加速度） | w2,w3 | 待验证 |
| ts_zscore 长窗标准化 | w1,w2,w3 | w1 失败 |
| 线性混合 0.5A+0.5B（CW-safe） | w1,w2,w3 | 待验证 |
| -rank(F) 逆向 | w1,w2,w3 | w1 best 即此骨架（sh0.70） |
| vec_* event 专用 | — | 未尝试（已放弃 event 数据集） |

### 4. 风格多样性（6 类）
- 动量/修正动量（eps revision、rating revision）✅ w3 主攻
- 盈余惊喜（real_earnings_surprise）✅
- 不确定性逆向（低 dispersion/stddev 做多）✅
- ML latent（mean vs log_variance 稳定性）✅ 全新风格，与任何已知信号正交预期高
- 突破/反转结构（pattern_scores）❌ 已证伪
- 流动性逆向（成交量下降）✅

### 5. 预处理
- decay=8/trunc=0.06（论坛 KOR 验证）为主批，SECTOR d4 t0.08 对照
- 未尝试：winsorize（bounded 字段跳过）、unit_handling=VERIFY 默认、nan_handling=OFF
- 风险点：change_* 字段本身是差分，再做 ts_delta 等于二阶差分，信噪比可能下降——batch3 作对照观察

### 6. 收益来源归因（预判）
- wave1 失败归因：pattern_scores 是已拥挤的技术形态信号（平台 alphaCount 高），KOR TOP600 下被 arb 掉
- wave3 预期归因：分析师修正/盈余惊喜 = 基本面信息扩散滞后（KOR 外资信息劣势更明显）；ML latent = 模型独占信号，alphaCount=0 无拥挤

### 7. 失效风险清单
1. **event 类型盲废**（已发生）：常规算子全报错 → 规则：新数据集先 get_datafields 看 type 列
2. STATISTICAL 中性化下信号消失（MARKET 中性化的翻版）→ batch3 SECTOR 对照兜底
3. change_* 差分字段稀疏 → coverage 1.0 已确认，风险低
4. PROD_CORR 墙：pattern_scores 若未来出达标 alpha，与现有 OS 池相关风险高；ml_factor_proj 零竞争风险低
5. 配额：REGULAR_SUBMISSION remaining=0 至 2026-08-15，达标 alpha 先做 submit_ready 验证不提交

## 三、Skill 优化要点（写回经验）

1. **强制类型预检**：设计表达式前必须 get_datafields 确认目标字段 type（MATRIX 才可用常规算子；event/VECTOR 只能 vec_*）。本地 verifier 只查语法，查不出类型兼容性——这是 wave2 浪费 48 次配额的根因
2. **MCP 参数名清单**：create_multi_simulation=alpha_expressions；get_multisimulation_children=multisimulation_location；search_forum_posts=search_query；read_forum_post=article_id
3. **get_datafields 分页 400**：search 命中 >100 时第 3 页 400；用更窄 search 词分批
4. **批量指标拉取**：get_user_alphas(stage=IS, region, start_date=T00:00Z) 一次拿全 metrics/ra/checks，禁止逐个 get_alpha_details
5. **KOR 设置经验**：TOP600 唯一可用 universe；SECTOR 为经验默认，但论坛证据 STATISTICAL+rank-diff 上限更高 → 双轨对照制
6. **数据集切换纪律**：模板穷尽（best<0.8 且 ≥40 表达式）+ 论坛无解 才允许切换；本战役 wave1→wave2→wave3 均符合
7. **零竞争优先**：alphaCount=0 字段族（ml_factor_proj change_*）优先于拥挤字段，PROD_CORR 风险天然低

## 四、下一步
- wave3 回测完成 → 同一门槛评审 → 达标者立即 robust/过拟合/SELF_CORR/PROD_CORR 校验
- 若 wave3 仍 0 达标：切白名单第 3 位 analyst_earnings_ibes（28 字段，MATRIX 需先验证 type）
