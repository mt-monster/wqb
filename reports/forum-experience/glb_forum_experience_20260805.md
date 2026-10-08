# GLB（Global）因子挖掘论坛经验系统总结

> **数据来源**：WorldQuant BRAIN 中文社区论坛，2026-08-05 抓取。
> **采集方法**：直连 Zendesk Support（BRAIN Basic-Auth → SSO）抓取 HTML 搜索页 + 社区帖 JSON API，共检索 8 组关键词（GLB / 全球因子 / 分区域权重 / Power Pool / 中性化 / turnover / 点塔 / 冷门数据集），去重得 160 条命中，精读 22 篇高互动帖（含全文 + 评论）。
> **GLB 释义**：在 WQ BRAIN 中 GLB = **Global（全球）区域**，合法 universe 为 `TOP3000 / MINVOL1M / MINVOL10M / TOPDIV3000`；它是 Thematic Power Pool 的轮动主题之一（如 2 月 GLB TOPDIV3000、3 月 GLB all Risk factors）。社区中"GLOBAL"与"GLB"混用，**与"债券"无关**。

---

## 〇、GLB 区域特性速览（社区共识）

| 维度 | GLB 特性 | 社区依据 |
|---|---|---|
| 独有可视化 | 开启 Visualization 后可看 **"average size by country"**，按国家拆解持仓——其他区域无此视角 | 帖10（MAPC 全球第一） |
| 国家定向 | 可主观把 alpha 重点指向英国/澳大利亚/日本/北欧，value factor 易冲高 | 帖10 |
| 回测速度 | **明显偏慢**（"跑了快一天不到 1500"），社区多次呼吁恢复 8 槽 | 帖搜索命中"glb太慢"系列 |
| 同质化 | PV、Risk 类别 alpha 偏多，拥挤度高 | 帖14 评论 |
| SA 表现 | GLB 适合组低 prod 的 SuperAlpha（一作者 12 天 pc<0.3 的 SA 中 GLB 占 7 个） | 帖2 |
| 主题节奏 | Power Pool 主题按月轮动（TOPDIV3000 / all Risk factors 等），仅主题内 alpha 可参与，默认 1x 乘数 | 帖12 |
| fundamental turnover | 窗口对 turnover 极敏感：`ts_zscore(f,240)`→0.07；`ts_zscore(f,22)`→0.22；`ts_mean(f,240)`→0.016 | 帖6 评论 |

---

## 一、因子构建思路

### 1.1 ATOM 单字段哲学（GLB 首推）
MAPC 全球第一作者的核心方法（帖10）：
- **每次只用一个数据字段**，通过嵌套函数连续操作，配合对同一数据的加减乘除，最大化 datafield score。
- **优先选低流动性数据集**以优化 GLB 回测运行时间（GLB 本就慢）。
- 跑完后切换可视化模式，用 "average size by country" 判断国家定向（英/澳/日/北欧）。
- 提交前对所有 merged alpha 做**可视化必查**，确保按预设算法正确运行。

### 1.2 行业中性化残差模板（高泛用性）
帖3 给出出货量极高的通用模板：
```
ts_zscore(A, 63) - ts_zscore(group_neutralize(A, sector), 63)
```
- **三层内涵**：① ts_zscore 剥离时间趋势与量纲；② group_neutralize 剥离行业共性波动；③ 差值保留"同行业内个体相对差异"的纯 Alpha。
- 适用于市值/PE/PB/营收增速/ROE 等各类基本面与量价指标。
- **窗口选择**：63 天（约一季度）平衡稳定性与时效；低频基本面可用 126/252；analyst 类低频字段用 `ts_backfill(field, 22)` 比 `ts_zscore(field, 63)` turnover 更低（0.10 vs 0.15+）。
- **GLB 迁移建议**：EUR/GLB 行业分类更细，残差信号可能比 IND 更有区分度。

### 1.3 反转 + 收益率组合（V9 突破范式，skill 已收录）
`scale(rank(ts_zscore(...))) + scale(-rank(ts_zscore(returns, 42))) * 0.35`，returns 反转 >> close 反转，低 decay 配 returns 可把 IS_LADDER 顶到 2.0+。

### 1.4 跨区域映射复用（GLB ↔ 其他地区）
帖17 的 MCP 工作流，区域映射规则：
- `APAC → ASI`、`EMEA → EUR`、`AMER → USA`（反向亦可 GLB ← 其他地区）。
- 优先同 `dataset_id` 找字段；不可用则换同 `category` + 关键词语义搜索。
- 候选字段池 **3–8 个**，一次 multiSim 跑完。
- ASI 必须开 `max_trade=ON`；保持中性化/decay/delay 一致以保可比。

### 1.5 SuperAlpha 构建（GLB 低 pc 利器）
- **Selection = 筛选 + 打分函数**，按分排序取前 N（Selection Limit 30–100）。
- **Combo = 每日权重**：等权 `1`（新手首选）→ `combo_a(alpha,nlength=252,mode='algo1')` → 多 combo_a `signed_power(scale(w1)+scale(w2)+scale(w3),2)`。
- GLB 低 pc SA 实战 selection（帖2）：
  ```
  (1-prod_correlation)*(neutralization in [SLOW/FAST/STATISTICAL/...])
  *(prod_correlation<0.4)*(datafield_count<2)*(prod_correlation>0.27)*(turnover<0.35)
  ```
- 中性化偏好：GLB/ASI 低 pc SA 多用 **risk neutralize（STATISTICAL 为主）**。

---

## 二、数据处理流程

### 2.1 战役前置体检（不可跳过）
- 用 `get_datasets` 拉数据集级 `coverage / alphaCount / fieldCount / pyramidMultiplier`，过三条硬门槛：**coverage≥0.85、alphaCount≤50、fieldCount≥10**。
- GLB 合法 universe 仅 `TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000`，传错档位会 HTTP 500。
- PPA 主题期间务必确认数据集在当期 Power Pool 列表内（如 PV1 通常**不在** PPA，误用会失去 PPA 资格）。

### 2.2 字段级预处理（按 dataAna 10 指标定算子）
| 字段特征 | 推荐处理 |
|---|---|
| 低覆盖/断点 | `ts_backfill(66/120)` 填洞 |
| 强单边分布 | `rank(signed value)` 或两同构字段 `subtract` 取差 |
| 高偏度/高峰度 | `winsorize` / `signed_power(x,0.5)` / `rank` 降偏 |
| 整数计数类 | `rank`/`group_rank`/`bucket`，**勿用 ts_mean 平滑** |
| 极端值（GLB earnings 实战） | `if_else(x < threshold, nan, x)` 过滤后再处理（帖8：过滤 >-150 时 IS 最佳） |

### 2.3 GLB 国家维度处理
- GLB 多国家，原 alpha 若只做 INDUSTRY 中性化，到 GLB/EUR 会暴露 country bias → 显式加 country 分组。
- 用可视化 "average size by country" 识别某国家线偏离（帖8：EMEA 线 sharpe -0.35 提示异常值）。

### 2.4 MCP 工作流标准化（帖6/16/17）
六阶段：基线诊断（`get_alpha_details`）→ 信号拆解（解析 code + `get_datafields`）→ 字段检索 → 候选构建 → 批量 `create_multiSim` → 验证推广。把 AI 当**细分任务助手**（如专做降 turnover），成功率从 40% 显著提升，且 token 消耗可控。

---

## 三、特征工程技巧

### 3.1 降 Turnover 工具箱（社区最高频痛点）
核心关系：**return = turnover × margin**，高 turnover 压低 margin 与 fitness。
| 手段 | 说明 |
|---|---|
| 增大 decay | 提升信号一致性，但过大破坏信号 |
| `ts_decay_linear(x, n)` | 论坛首推，n=5/22/44/63，实测降 30–50% |
| `ts_target_tvr_decay(x, lambda_min, lambda_max, target_tvr)` | 直接定目标 turnover，GLB 实战把 tvr 1.17%→4.66%/8.14%，同时 prod corr 0.90→0.77（帖8） |
| `hump` / `ts_target_tvr_hump` | 对 Sub-universe Sharpe 更直接 |
| `tradewhen` | 加开平仓条件，市场平静时不交易 |
| `ts_decay_exp_window(signal,10,factor=0.5)` | 保留短期响应，比单纯提 decay 更有效 |

> **过拟合检验**：优化后看 IS/OS Sharpe 差值，IS 涨 OS 跌 = 已过拟合，回退。
> **GLB 窗口规律**（帖6 评论）：短窗口 zscore（22）可同时拿 HTVR 2x 乘数 + Power Pool 1x 乘数；multi-sim 把窗口 22/66/120/240 作为变体维度一趟覆盖。

### 3.2 升 Sharpe/Fitness
- `signed_power` 压缩信号提 fitness（帖14）。
- 残差差分（ts_zscore 差）提纯个体 Alpha（帖3）。
- group_neutralize 切换中性化维度改善 robust（帖14）。

### 3.3 降 Prod Correlation（PC>0.7 救援）
按帖14 优先级：开 max-trade → 切换股票池 → 调 decay → 调 ts 窗口 → 分组中性。若 family 长期卡同一窄区间（如 0.73x），说明已进入 crowded neighborhood，**尽早停手做结构位移**而非继续抛光（帖20）。

### 3.4 换壳不换字段（帖20 核心洞察）
当信号方向对但过不了最后几道门（margin/robust/ladder），优先做**结构等价但统计性质不同**的换壳：如 `group_rank` → `group_zscore` + final rank，字段不变、复杂度不变，但漏斗明显变顺。

---

## 四、回测验证方式

### 4.1 廉价闸门（PC 等待前）
- Sharpe ≥ 1.58；Fitness ≥ 1.00；TVR ∈ [5%, 20%]；Margin > 5bp；Returns > 4%（高于地区银行年化）。
- **近 2 年 Sharpe 必看**：指标漂亮但 2y sharpe 不达标 → 信号快失效，慎交（帖4）。
- **开 maxtrade 后表现**：Sharpe>1、Fitness>0.5 才算接近实盘（帖4）。
- **最大回撤**：不出现在近 3 年，且每年小回撤不能太高（帖4）。

### 4.2 IS-Ladder 阈值（D1，帖6）
Fail=1.59；2–5年≥2.38；6年≥2.22；7年≥2.06；8年≥1.90；9年≥1.74；10年≥1.59。

### 4.3 硬闸门（PC 等待后）
- PROD_CORRELATION < 0.70；SELF_CORRELATION < 0.50。
- **PPAC 隐蔽卡点**（帖11）：PPAC 规则豁免 Prod Correlation，但当 **Power Pool 相关性 > 0.5** 时，系统会"借用" Prod Correlation(>0.7) 名义 FAIL。真凶是 PP 相关性。`/check` 返回里 `POWER_POOL_CORRELATION` 是**有条件出现**的，IS 阶段即可提前判定够不够 PP 资格。
- **降级机制**：Power Pool alpha 优先级高于 regular，PP 检测不过会降级按 regular 再判一次（帖11 评论）。

### 4.4 提交质量基线（PPAC 全球第 11 实测，帖18）
Sharpe 1.93 / Returns 10.33% / Turnover 4.96% / **Margin 54.42‱** / Fitness 1.70；覆盖 7 个金字塔。**Margin 是拉开排名的关键**。

### 4.5 警告即硬伤
`LOW_ROBUST_UNIVERSE_SHARPE`、`IS_LADDER_SHARPE` 等 warning 在真实筛选里经常就是过不去，不要当小问题（帖20）。

---

## 五、实战踩坑与优化建议

### 5.1 七大反复踩坑（帖20 精炼）
1. **self/prod 过了 ≠ 进库**：margin/robust/ladder 任一不稳就远未完成。
2. **family prod 长期卡窄区间 → 尽早停手**：是 crowded neighborhood，微调是无效劳动。
3. **纯 settings 修法 = 按下葫芦浮起瓢**：修 margin 掉 robust，修 robust 冒 ladder → 优先怀疑壳本身不对。
4. **有效修复 = 换壳**：结构等价但统计性质不同（group_rank→group_zscore+rank）。
5. **winner 提交后周围 family 变 self wall**：不要做近邻修补，尽快做更远 field-level move。
6. **warning 不是小问题**：同种 warning 反复卡住 = 结构短板，及时止损。
7. **submitted 状态有滞后**：不要只信一个状态源。

### 5.2 GLB 专项踩坑
- **GLB 回测慢**：优先低流动性数据集 + multi-sim 批量，别单条死等。
- **GLB 国家偏差**：只做 INDUSTRY 中性化会暴露 country bias，加 country 分组或用 COUNTRY 中性化。
- **GLB PV/Risk 拥挤**：主动转向 analyst/news/option 等冷门类别（帖5 数据集分布可参考）。
- **GLB fundamental 低 turnover 陷阱**：长窗口（240）turnover 仅 0.016–0.07，可能过低影响 osmosis，需用 `ts_target_tvr_decay` 主动拉到 5–10%。

### 5.3 提交策略（combine 稳定第一，帖4/13）
- **精选 PPA 池**：按 RA 标准筛，保留有上升趋势的因子；PPA 池 combine 可手动增删 tag 控制。
- **多样性提交**：一个月专注两区域，月底前点完塔；引入 ASI/IND 提升pool多样性。
- **tag management**：为点塔硬交的难看 alpha，删 `PowerPoolSelected` 标签减小危害（权宜之计，非正道）。
- **避免给低换手因子赋高分**：低换手因子单日不触发交易，osmosis combine 表现差。

### 5.4 HTVR（高换手主题）要点（帖21）
- 基础门槛：turnover>20% 且 (HT returns ratio>0.75 或 Pnl realization<20)。
- 四子主题难度：After Cost(最易,65条) > Orthogonal(40) > Investable(22) > Liquid(最难,14)。
- 难主题可考虑跳过。SA 中用 `in(classifications,"HIGH_TURNOVER:XXX")` 筛选已交 theme RA。

### 5.5 数据集推荐（GLB 相关，帖19/5）
- **GLB D1 TOP3000**：ANL11、ANL14_part1/part2、ANL15（analyst 类，社区推荐）。
- PPA USA D1 热门：option22、option23、analyst4/7、fundamental6、news12、model26。
- 帖15 提供 40+ 基本面比率字段（ebit/assets、income/equity、cashflow_op/liabilities 等），可直接用于质量/估值/成长因子构造。

---

## 附录 A：精读帖子清单（22 篇）

| # | 标题 | 票数 | 评论 | 核心主题 |
|---|---|---|---|---|
| 0 | 如何拯救高turnover因子 | 176 | 24 | 降 turn 方法论 |
| 1 | 组sa时如何选取高质量因子 | 121 | 24 | SA selection 五步法 |
| 2 | 连续12天手搓出pc<0.3的SA | 112 | 33 | GLB/ASI 低 pc SA |
| 3 | 行业中性化残差信号IND模板 | 90 | 41 | ts_zscore 残差模板 |
| 4 | 全球combine第一经验 | 99 | 22 | 提交质量五原则 |
| 5 | PPA所有数据集及其字段 | 108 | 10 | USA D1 96 数据集分布 |
| 6 | 利用mcp优化GLB alpha | 93 | 24 | GLB 优化工作流 |
| 7 | Super Alpha 入门 | 73 | 35 | SA 理论与实操 |
| 8 | 借助Labs优化GLB alpha | 89 | 14 | GLB earnings 极端值+TVR |
| 9 | SAC ATOM第三分享 | 90 | 10 | SA selection+combo |
| 10 | MAPC全球第一GLOBAL数据处理 | 91 | 8 | GLB 单字段+国家定向 |
| 11 | PPAC Prod Correlation 报错 | 91 | 5 | PP 相关性隐蔽卡点 |
| 12 | 2月全球会议整理 | 78 | 13 | 主题/Power Pool 节奏 |
| 13 | Combined PPA 持续稳定 | 71 | 19 | tag management |
| 14 | PPA主题限制下点塔心得 | 70 | 17 | fail/warning 修正思路 |
| 15 | 豆包推荐用户数据集1 | 63 | 20 | 40+ 基本面比率字段 |
| 16 | MCP turnover优化精华版 | 69 | 12 | ts_decay_linear 工作流 |
| 17 | GLB→其他地区alpha工作流 | 70 | 10 | 跨区域映射 6 步 |
| 18 | PPAC全球第11提交因子 | 69 | 11 | 提交指标基线 |
| 19 | 数据推荐合集 | 44 | 28 | GLB/USA/CHN/ASI 数据集 |
| 20 | Regular点塔反复踩坑 | 63 | 8 | 七大踩坑+换壳论 |
| 21 | USA 3x High Turnover Theme | 62 | 6 | HTVR 四子主题 |

---

## 附录 B：可直接复用的表达式

**残差模板**：`ts_zscore(A, 63) - ts_zscore(group_neutralize(A, sector), 63)`

**降 TVR**：`ts_target_tvr_decay(signal, lambda_min=0, lambda_max=1, target_tvr=0.1)`

**SA selection（低 pc）**：`(1-prod_correlation)*(prod_correlation<0.4)*(datafield_count<2)*(turnover<0.35)`

**SA combo（多周期）**：`signed_power(scale(combo_a(alpha,40,'algo1'))+scale(combo_a(alpha,160,'algo1'))+scale(combo_a(alpha,252,'algo1')), 2)`

**GLB fundamental 窗口变体**：`ts_zscore(field, {22,66,120,240})` 一趟 multiSim 覆盖 HTVR 与非 HTVR。

---

*报告生成：2026-08-05，基于 22 篇论坛精读帖。原始数据见 `tracking/forum_glb_search.json`（160 条命中）与 `tracking/forum_glb_posts.json`（22 篇全文+评论）。*
