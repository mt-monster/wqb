# wave288 · KOR news_sentiment_transfer 探针与判死（2026-11-06）

## 1. 数据集画像
- `news_sentiment_transfer`（category=sentiment，KOR 塔点亮数 **0**）
- 23 字段 / cov **0.9654** / 总 alphaCount 238 / userCount **129**
- **拥挤度极低**：单字段 aC 1–31、uC 1–25（最拥挤 `news_article_count` aC31/uC25）
- 字段族：①文章计数 ②primary/secondary 情绪统计量（avg/max/min/median/total/skew）③`sentiment_distribution_skewness_2` ④3 个 VECTOR（`news_sentiment_score`/`primary_sentiment_value`/`secondary_sentiment_value`，未使用）

## 2. 设置
- 卡：`STATISTICAL / decay4 / trunc0.08 / nanH OFF / maxTrade OFF`
- 实测追加：`REVERSION_AND_MOMENTUM` 档（参照 insiders 实证）

## 3. 批 A（STATISTICAL，8 条，`1CAdQP6z74wrbxv3HWfc05e`）
全部**取负方向**（`subtract(0.5, group_rank(...))`）→ 8/8 为负：

| alpha | S | TO | 模板 |
|---|---:|---:|---|
| `e75NOjgz` | **-0.84** | .1393 | ts_std_dev(level,22) 分歧度 |
| `E56Nwd01` | -0.73 | 1.14 | 分布偏度 |
| `mLod8veK` | -0.65 | 1.11 | max−min 分歧度 |
| `kqNv3Ak8` | -0.62 | .356 | 22d 情绪变化 |
| `ZYQgpJqx` | -0.32 | .288 | 66d z-score |
| `wpQ3RrO2` | -0.29 | .284 | 每股情绪强度 |
| `KPJvb1Yk` | +0.25 | .550 | 5d 关注度冲击 |
| `omERKdAm` | -0.12 | .293 | primary−secondary 双引擎背离 |

**归因**：全负 ⇒ 方向反了，原始正向才成立。**与 insiders5 方向相反**（insiders 是净增持反向，sentiment 是正向）。

## 4. 批 B（REVERSION_AND_MOMENTUM，8 条，原始方向，`2zMmLMakA50zaS514gBWa7vS`）

| alpha | S | F | TO | 模板 |
|---|---:|---:|---:|---|
| `RRE988kj` | **0.72** | 0.47 | **.0786** | **ts_mean(ts_std_dev(level,22),55) 平滑分歧度** |
| `RRE988az` | 0.26 | 0.04 | 1.22 | 分布偏度 |
| `QPvOVV2X` | 0.23 | 0.05 | .270 | 每股情绪强度 |
| `bl6JqqPq` | 0.22 | 0.03 | 1.19 | max−min 分歧度 |
| `e75N002J` | 0.10 | 0.02 | .221 | 分歧度×关注度（卡原语） |
| `akKennWw` | 0.09 | 0.01 | .269 | 情绪水平 |
| `N1NLrrg7` | -0.31 | -0.08 | .247 | 关注度水平 |
| `6XdZ99YY` | -0.56 | -0.19 | .287 | 双引擎背离×关注度 |

## 5. 结论：**判死（主信号）**
- 16 条结构互异模板（12 个骨架 × 两方向），**最高 S 0.72**，离 REGULAR 线 1.58 差 0.86。
- 与参考页跨区负先验一致：`sentiment.md`「新闻/情绪作主信号在多区同型全灭（robust 墙 / CW / 换手墙）」。
- 换手不是问题（冠军 TO 7.86%），**是信号本身弱**。
- 唯一亮点：55 天平滑把 TO 从 22% 压到 7.86% 且 S 从 0.10 提到 0.72 ⇒ 「平滑分歧度」方向正确但幅度不够。

**禁令**：`news_sentiment_transfer` 不再作主信号开波。作辅助/门控腿仍可，但需跨数据集组合。

## 6. 附：prod 相关性取不到的真因（本轮查清）
- 账号 prod 单并发槽被**另一路工作负载**（另一 MCP 实例 pid 75148）连续占用：先 `E56Nk0wL`、后 `omERn83n`（均属 RISK 战役提交验证线）。
- 证据：锁 token `logs/_dblock/correlation.lock.json` 的 `tag` 字段直读持有者；`logs/_dblock/correlation.inflight.json` 显示 pid 与 alpha。
- **不要杀 pid 75148**——那是另一条在跑的工作线。
- 直连 Python（`tools/prod_wait.py`）被系统代理 `127.0.0.1:7897` 阻断（ProxyError），**prod 只能走 MCP**；而 MCP 单次调用 120s 上限 < 平台 prod 计算耗时 ⇒ 取 insiders 候选 prod 结构性困难。
- `get_alpha_details` 的 `is.prodCorrelation` 对这两颗为空 ⇒ 平台从未成功算完过。
