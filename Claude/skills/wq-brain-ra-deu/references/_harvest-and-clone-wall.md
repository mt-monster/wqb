# DEU 收割分诊与克隆墙（2026-11-21 战役实证）

> 回到 [DEU 区域流程](../SKILL.md)。本册只收 **2026-11-21 一轮战役实测**的收割分诊口径与克隆墙证据，
> 配套：结构杠杆册 [`_effective-levers.md`](_effective-levers.md)、篮子口径 [`_basket-and-atom.md`](_basket-and-atom.md)。
> 权威实测档案：`output_report/DEU_campaign_20261121.md`（战役报告）、`tracking/DEU/reference/datasets/sentiment27.md` §8（情绪族增量读数）。

---

## 一、收割分诊的**正确分母**：先按平台真实约束过滤，不是先按「塔位未点亮」

DEU 全池实测分诊（`data/wqb.db` 的 `alphas` 表，2026-11-21）：

| 过滤步骤 | 口径 | 剩余 |
|---|---|---:|
| 平台闸全过 | S ≥ 1.58 ∧ F ≥ 1.0 ∧ 2Y ≥ 1.58 | **925** |
| 平台塔数 | `pyramids.effective ≥ 1` ⇒ **≤2 塔**（≥3 塔 ⇒ effective = 0，`1YWnZ9rK`/`2r5MO67Z`/`vRA82ogA`/`6XM7ARLE` 全灭） | **484** |
| prod | prod < 门槛（见 `config.PRODCORR_CEILING`） | **28** |
| self-corr（本地 OS 池） | max < 0.70 | **17** |
| 篮内互相关（本地 39×39） | 全对 < 0.70 | **6** |

⇒ **先套 ≤2 塔再排序，能省掉 60%+ 的无效互相关计算**；「按塔位是否点亮」不是平台判据，**`pyramids.effective` 才是**。

## 二、收割顺序：prod 之后立刻做两个**本地零配额**闸

本轮 28 颗 prod 未超线候选（阈值见 `config.PRODCORR_CEILING`）的实测挂点分布：

| 闸 | 挂掉 | 成本 | 备注 |
|---|---:|---|---|
| **self-corr**（`check_self_correlation`，本地 OS 池） | **11 颗**（0.80–0.98，全是撞已提交件） | **零配额、零等待** | 挂点最重 ⇒ 应排在 prod 之后**立刻**做 |
| **篮内互相关**（`compute_mutual_correlation`，本地 PnL） | 9 颗 | 零配额 | 39×39 一次拉齐 |
| prod | **0 颗** | 平台单槽 + 熔断风险 | 本轮 28 颗 prod 全部未超线（阈值见 `config.PRODCORR_CEILING`） |

⇒ **推荐收割顺序：prod → self-corr（本地）→ 篮内互相关（本地）→ 逐年 longCount/pnl**。
把两个本地闸放在 prod 之后立刻做，可以在 1 次平台调用内砍掉大半候选。

## 三、克隆墙的三种指纹（本地 `compute_mutual_correlation` 一次拉齐即可识别）

| 指纹 | 实测 | 含义 |
|---|---|---|
| **同一 alpha 的两个 id** | `QPveY7Kg` ↔ `bl6OWZ2M` = **1.0000** | 平台对同表达式返回同 alpha；DB 里会留两个 id。**按 id 筛选会误当两个候选** |
| **同族同壳 + 换字段** | `XgaGb3J1` ↔ `0mPKr3bq` 0.9936；`GrmPOz05` ↔ `vRA82Ga3` 0.9690；`xArYWKgg` ↔ `zq3Ye20E` 0.9811 | 换壳不换信息 ⇒ 同一信息的多壳 |
| **撞已提交件** | `npvwXA8l`↔`xArzm3Mn` 0.9192、`zq3Ye20E`↔`LLM93nGa` 0.9828、`GrmPOz05`↔`2r5Lm3Jx` 0.9038、`VkNV0zqM`↔`2r5Lm3Jx` 0.8247 | `check_self_correlation` 的 `top_correlated` 会**直接指认源件** ⇒ 比读直方图快 |

⚠ **`self_correlation` 字段的实测值可能与本地 OS 池不一致**（本轮 `GrmPOz05` DB 记 0.3136，本地 OS 池实测 0.9038）⇒ **判 self 闸只认 `check_self_correlation` 的 `max_correlation`**，不认 `alphas.self_correlation` 列。

## 四、★「换字段」≠「换信息」：梯度在语义位上会收敛到同一 PnL

`sentiment7 × sentiment27` 残差化族（骨架 `vector_neut(<snt7 关注度>, <snl27 中性化目标>)`）本轮产出 **6 颗 RA-clean 件**（S 1.84–1.94 / 2Y 2.18–2.46 / sub 1.05–1.19）：

| 中性化目标 | alpha | S | 2Y | 族内互相关 | vs ACTIVE `bl6OWZ2M` |
|---|---|---:|---:|---:|---:|
| `snl27_topranking` | `omaRkL82` | 1.94 | 2.46 | — | **0.9760** |
| `snl27_top50pctrankingavg` | `leaE9287` | 1.90 | 2.43 | 0.9996 | **0.9755** |
| `snl27_top75pctrankingavg` | `E5QNLEpr` | 1.89 | 2.42 | 0.9996 | — |
| `snl27_top50pctranking` | `0mPxawrK` | 1.88 | 2.39 | 0.9987 | — |
| `snl27_avgranking` | `akaeg7xR` | 1.88 | 2.39 | 0.9985 | — |
| `snl27_skewness` | `O0WR2L5Y` | 1.84 | 2.18 | 0.8029 | 0.7983 |

⇒ **6 颗只有 1 条独立信息，且已被 OS 池占位** ⇒ 全部撞 self-corr 0.70。
⇒ **梯度设计纪律**：同族字段冗余度高时，梯度必须换**信息源（数据集）**，换语义位无效。
（与 `sentiment27.md` §2.3「冗余度约 70%」相比更强：对**残差化用法**而言冗余度 **≥90%**。）

## 五、两条负杠杆（可复用）

| 换法 | Δ | 证据 |
|---|---|---|
| `snt7_all_languages_views` → `snt7_views` | ΔS **−1.11** | `N1PL2ZO7` S 0.79（RA 失败 3 项）⇒ 多语言合计是必需口径 |
| `ts_quantile` 窗 252 → 504 | ΔS −0.11 / Δ2Y **−0.37** | `akaegpOw` S 1.79 / 2Y 2.06 ⇒ 252 是上界 |
| 排名类字段裸用 | S **−0.13**（sub −0.45） | `snl27_avgranking` 裸用 `O0WR2767` ⇒ 档案「排名类须取负」首次实测确认 |
| 计数类字段裸用 | S 0.41 / **TO 0.015** | `snl27_totaldomains` 裸用 `akae8krv` ⇒ 规模代理 + 换手塌缩 |

## 六、平台 prod 相关性服务会**账号级熔断**（工具用法坑）

`check_correlation(correlation_type="production")` 连续 pending 会触发 `status = platform_unavailable` + `retry_after` 倒计时。

- 本轮实测：492 → 268 → 225 → 186 → 117 → 108 → 63 s **持续递减但始终未恢复**；
- **每次重试都会把冷却期重新拉长** ⇒ 熔断期内**不要重试**，改做零配额的本地闸（self-corr / 互相关 / 逐年）；
- `inflight = true` 时**不要重新触发计算**（会把自己顶成 busy），按 `retry_after` 隔时重查即可；
- 平台恢复正常后实测 `RREwqrNa` prod **0.6684 PASS**（98.6 s 算完），与 11-08 记录值**逐位一致** ⇒ 该件的 prod 指纹稳定。

## 七、★ ZCode 会话内 MCP 调用参数类型被压平（工具用法坑，非平台问题）

| 参数 | 类型 | 表现 |
|---|---|---|
| 整数 | `integer` | ✅ 正常透传（`delay: 1`、`decay: 4`、`years: 4`） |
| **浮点** | `number` | ❌ 被转成字符串 → `create_multi_simulation` 的 `truncation=0.08`（DEU 生产档）被拒（工具缺省 **0.0** ≠ 区域 `settings.json`）；`check_correlation` 的 `threshold` / `timeout_s` 同理 |
| **布尔** | `boolean` | ❌ 同上 → `get_datafields` 的 `filter_sharpe=false`（**用户硬红线：字段查询必用 false**）与 `check_correlation` 的 `refresh=True` 被拒 |
| 字符串 / 字符串数组 | `string` / `string[]` | ✅ 正常 |

**绕过办法（不改仓库、仍是 MCP）**：用 MCP 客户端（streamable-http）直连同一个 `main.py` 服务
（`http://127.0.0.1:8000/mcp`），参数类型就对了。本轮实测走该通道时平台回显
`truncation: 0.08 / decay 4 / neutralization: SUBINDUSTRY / nanHandling: OFF / unitHandling: VERIFY`
与 `tracking/DEU/config/settings.json` **逐字一致**。

⚠ 另注：`compute_mutual_correlation` 的 `threshold` 也是浮点 ⇒ 走常规通道只能吃默认 0.5，
本轮用 0.7 是走 MCP 客户端通道。

## 八、平台队列拥塞时的读数纪律

- multisim 长时间停在 `progress 0.35` = **排队**（不是失败）；`batch_status` 在 children 注册前显示 `child_count: 0`；
  用 `lookINTO_SimError_message` 读父对象可拿到 `children` 列表。
- **不要在 0.35 时重发**（重发 = 重新排队）。
- `batch_status` 对**单发仿真**（非 multisim 父对象）会报 `parent COMPLETE but children empty` ⇒ **不是错误**，
  用 `lookINTO_SimError_message` 取 `alpha` 字段。
- 收割 404 兜底顺序照旧：`batch_status` → children 的 8 位 alpha id → `batch_get_alpha_metrics` + `get_alpha_details`。

## 九、跨区移植的正面/负面信息（本轮新例）

| 形态 | 源区 | DEU 实测 | 结论 |
|---|---|---|---|
| 内部人「金额 ÷ 股数」比值（`top_directional_significant_value_1(1260d) ÷ (total_top_buy_shares − total_top_sell_shares)(84d)`） | EUR 已交付（`Grl9wPb3` S 1.89 / prod 0.5322 / self 0.1268） | `2r59xRvw` **S 0.37 / 2Y −0.41**（分母窗 126 → S 0.12） | **形态不迁移**（跨区不可外推窗口与方向）——但 **self-corr 仅 0.038** ⇒ **机制在 DEU 与 OS 池完全正交**，是干净的**新信号位储备**，缺的是强度杠杆 |
| 拥挤空头 ⇒ 挤压（正向） | 论坛 si3 三帖 | inst25 探针四臂一致为负（crowding −0.22 / concentration −0.28 / activity −0.27）⇒ 正向 S 0.22–0.28；最佳 T10 S 0.61 | **方向成立、强度不足**（数据集级死） |
| 内部人买入 > 卖出 | JMZ 2003 / 论坛 | 本轮 `insider_agg_matrix` 全字段体检 **10/34 已回**：买类字段 S **+0.16 ~ +0.28**、卖类字段 S **−0.10 ~ −0.28** ⇒ **方向在 DEU 复现**；但 lc/sc 仅 **39–69 / 500** ⇒ **覆盖薄**是本集强度上限的根因 | 方向可用、覆盖是瓶颈 |

## 十、本区未点亮塔的可产出面（2026-11-21 复核后的终态）

| 塔 | 数据集 | 终态 |
|---|---|---|
| INSTITUTIONS | `institutions25` / `institutions6` / `fund_holdings_panel` / `institutions4` / `institutions1` | **5 集全判死**（详见 `_basket-and-atom.md` 与战役报告 §5.4）——**「机构类」在 DEU 不是可产出的面**（结构事实） |
| INSIDERS | `insiders1`（PROVISIONAL，S 1.30–1.37）、`insider_agg_matrix`（死 + PROVISIONAL 双标） | 单集天花板 < 1.58 ⇒ **ATOM 单集出不来** |
| SENTIMENT | `sentiment7` / `sentiment27` | 残差化族被 OS 池占位（§四）⇒ 塔位已满 |
| NEWS | `news20`/`news17`/`news18`/`news50`/`news38`/`news104` | 数据集级死；其余 11 集 cov 0.0 |
| PV | `intraday_pv_feats`（主字段 prod 0.8377 墙；兄弟字段本轮 sweep S 1.28/1.35 ⇒ **只有主字段有信号**）、`pv20`（本轮 IBES S 0.82/0.84 ⇒ **IBES 面在 DEU 无定价力**）、`pv109`/`pv29`/`pv30`/`pattern_scores`/`pv1` | 死 / 自测否决 |
| RISK | `risk60`（S 0.90，2Y 0.83）、`risk68`（S 1.45，**2Y 0.83**）、`risk71`/`risk72`/`risk88` | 死 |
| EARNINGS / MACRO / OPTION / SOCIALMEDIA / IMBALANCE | `earnings6`/`earnings_sent_matrix`/`macro27`/`option1`/`socialmedia12`/`imbalance5` | **字段覆盖率全 0.0 ⇒ 数据层排除** |

⇒ **严格「排除已点亮塔数据集」口径下，DEU 新增可交付数 = 0**。未点亮塔里能出信号的面已全部判死或被 OS 池占位；
不能出信号的面是数据层排除。**这不是工作量不足，是前几周战役已把可达面收敛完。**
