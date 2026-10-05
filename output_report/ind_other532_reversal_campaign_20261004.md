# IND REGULAR 挖掘战报 · other532 特质收益反转族

- **日期**：2026-10-03 夜 — 2026-10-04 凌晨
- **区域**：IND / TOP500 / D1（严格不转区）
- **目标**：10 颗可提交 REGULAR alpha。已交 4 颗（`akxXl7w1` / `d51eGdKY` / `E5RA8pRL` / `blOVO3Pp`），本轮目标是在配额重置前攒够候选。
- **配额状态**：REGULAR 4/4 已用满，ET 00:00（GMT+8 12:00）重置。

---

## 一、本轮核心突破：发现 IND 唯一 S>4 的活族

### 机制
`other532`（Specific Returns）= **Barra 因子模型已实现特质收益残差**。
**残差的短期反转在 IND 极强**——反转集中在极短历史（2–3 日）。

### 主腿（IS 全闸，`is.checks` 无 FAIL）

| alpha | 表达式 | S | F | ret | TO |
|---|---|---|---|---|---|
| `WjedMzPx` | `signed_power(rank(-divide(ts_sum(oth532_emerging_daily_specificreturn,3), ts_std_dev(·,120))),0.4)` | **3.79** | **3.07** | 19.6% | 0.298 |
| `RR6YJvj1` | `signed_power(rank(-ts_sum(oth532_asia_ase2_daily_specificreturn,3)),0.4)` | 3.75 | **3.08** | 20.3% | 0.300 |
| `j28XvGAQ` | `signed_power(rank(-divide(ts_sum(oth532_asia_ase2_daily_specificreturn,3), ts_std_dev(·,60))),0.4)` | 3.77 | 3.04 | 19.3% | 0.297 |
| `gJZKY0Jg` | `signed_power(rank(-ts_sum(oth532_emerging_daily_specificreturn,3)),0.4)` | 3.71 | 3.03 | 20.1% | 0.300 |

全部设定：`neutralization=STATISTICAL`、`decay=16`、`nanHandling=OFF`、`maxTrade=OFF`。

---

## 二、三条可迁移的定量规律

### 1. 累加窗梯度（S–TO 曲线）

| 窗 | 2 | 3 | 4 | 5 | 6 | 10 | 20 |
|---|---|---|---|---|---|---|---|
| S | **4.17** | 3.97 | 3.77 | 3.66 | 3.49 | 2.98 | 1.76 |
| TO | 0.47 | 0.40 | 0.35 | 0.32 | 0.30 | 0.23 | 0.17 |

- S 峰值在窗 2，但**触发 HIGH_TURNOVER 不可提交**；**窗 3 是 S/闸门最优点**。
- 窗 ≥10 换手继续降但 S 一起塌（1.76 且触发 LOW_ROBUST）⇒ **本族"低换手"不是免费的**。
- 窗口单调降 ⇒ 反转集中在极短历史，与日频反转文献一致。

### 2. decay 梯度（单变量，4 条冻结表达式 × 4 档）

| decay | 4 | 8 | **16** | 24 |
|---|---|---|---|---|
| S（emerging 窗3） | 4.12 | 3.97 | 3.71 | 3.38 |
| **F** | 2.54 | 2.86 | **3.03–3.08** | 2.85 |
| TO | 0.540 | 0.399 | **0.300** | 0.262 |
| 闸门 | ✗ HIGH_TURNOVER | ✓ | ✓ | ✓ |

- **decay=16 是峰顶**：TO 从 0.40 压到 0.30（−25%），**F 反升到全族最高**。
- decay=4 一律触发 HIGH_TURNOVER ⇒ 本族 decay 下界 8；decay=24 过犹不及。
- ★ **Fitness 存在内点最优（倒 U）**——S 单调降但 F 先升后降。扫 decay 时盯 F 不只盯 S。

### 3. 分母与其窗口都是旋钮

同为 decay=16 / emerging / 分子 `ts_sum(·,3)`：

| 分母 | `ts_std_dev(·,20)` | `ts_std_dev(·,60)` | `ts_std_dev(·,120)` |
|---|---|---|---|
| S | 3.68 | 3.76 | **3.79** |
| F | 2.93 | 3.03 | **3.07** |

⇒ 分母窗要够长才能代表"常态波动"。这是"真变量常是分母"的第二层细化：**分母自己的窗口也是旋钮**。

---

## 三、已判死（省下重复试验）

| 形态 | 实测 | 结论 |
|---|---|---|
| 股本收缩（`ts_delta(number_of_issued_shares)`） | S −0.50 / −0.64 | **IND 判死**。论坛"回购减少股本提高每股权益"在 IND 不成立（回购少、稀释多） |
| 分析师分歧度（`stddev/mean`） | S −0.02 / −0.17 / +0.69(TO 1.235) | 判死 |
| `winsorize` 秩后裁剪 | S 掉 0.3–0.9 且触发 HIGH_TURNOVER | **本族禁裁剪**（与其他族的破 prod 经验相反）⇒ prod 若不过，先换分母/窗口 |
| `ts_rank(-x, 5)` 单期腿 | TO 0.86–0.88 + 5 项 FAIL | 判死 |
| `ts_corr(残差, 其均值)` | S 1.75 + LOW_ROBUST | 判死 |
| `ts_decay_linear` 平滑 | S 2.71–3.04 | 判死（优于让 decay 参数承担） |
| `group_zscore` | S 3.38–3.46 但 F 掉到 2.5x | 判死 |
| 月频残差（动量腿） | S 0.21 / −0.88 | 判死（**只有日频反转有效，动量腿无效**） |

---

## 四、待解决：prod 墙

**当前状态**：8+ 条 IS 全闸候选已就绪，prod/self 实测在平台侧排队计算中
（端点恒返回 200 空体，实测 >40min 未出结果）。

**风险预案**：
- 同族只交 1 颗（记忆：同族兄弟连提会顶高后来者 prod）。
- 本族 prod 若撞墙，旋钮优先级：**换分母窗口 → 换区域口径（ase2/global）→ 换外层分组轴**，
  **禁用 winsorize**（本族已实测破坏闸门）。
- wave104 已在跑 8 条"同机制不同几何"备选腿（口径×分母交叉、分子形态微调、subindustry/market 轴），
  主腿 prod 不过即可递补。

---

## 五、本轮新增工具

| 工具 | 用途 | 关键坑（已内建处理） |
|---|---|---|
| `logs/_harvest.py` | 稳健收割 multisim 子 alpha 指标 | 认证 429 自动退避；**`checks` 在顶层恒空，必须读 `is.checks`** |
| `logs/_corr.py` / `logs/_corr_long.py` | 直连轮询 prod/self | 平台算 prod 时连发 ProxyError/RemoteDisconnected 属正常噪声，必须捕获续轮 |
| `tools/ind_sim_submit.py` | IND 专用提交（settings 全显式） | 已加 CJK 行过滤（中文注释会让整批 children 连坐 CANCELLED） |

## 六、本轮沉淀的工程纪律

1. **payload 格式**：multisim 用 `regular: "<表达式字符串>"`；❌ `regular:{"code":...}` 和 `regular:[{"expression":...}]` 都报 `Not a valid string`。
2. **重试判定**：以 `submitted` 关键字判成功，一旦成功立即 break。`ind_sim_submit.py` 分批提交时"第一批成功+第二批 429"会导致重复提交。
3. **429 双类型**：认证 429 退避 240s；并发槽 429 退避 120–150s。
4. **成功码**：单条 multisim 可能返回 200 或 201，只判 `==200` 会把已受理的当失败并重发。
5. **VECTOR + ts_backfill**：推断为 wave99 全 FAIL 的根因（VECTOR 经 vec_avg 后进 ts_backfill 被拒），标记为高置信待验；VECTOR 稀疏填充改用 `group_backfill`。
