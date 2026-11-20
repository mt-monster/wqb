# EUR 未点亮塔 ATOM 优先评估（2026-11-19 03:0x）

> 触发：用户指令「优先挖掘ATOM」。本轮在 EUR/D1 未点亮塔上做 ATOM 专项复攻，全部读数均为**本会话平台实测**。

## 0. 塔位实读（`get_pyramid_alphas`，EUR/D1）

| 塔 | 计数 | 状态 |
|---|---:|---|
| analyst 10 / news 3 / model 3 / fundamental 3 / other 3 / risk 3 / sentiment 3 / imbalance 3 | ≥3 | 已点亮 |
| **pv 2 / insiders 2 / earnings 1 / institutions 0 / socialmedia 0 / macro 0** | <3 | **未点亮（可打）** |

（ATOM 与常规均只能打后 6 类。）

## 1. 本轮最重要的三个发现

### 1.1 `create_multi_simulation` 通道当前整体失效（单条 `create_simulation` 正常）
- 同 10 条表达式 → 10/10 子任务 `status=FAIL`，无 error message。
- 换中性化（SUBINDUSTRY）、重新 `authenticate`（201 authenticated）后仍然 10/10 FAIL。
- 对照组：**同一条已知成功过的基线表达式**用 multisim 发 → FAIL；用单条 `create_simulation` 发 → 正常产出 alpha（`kqajW1kK`）。
⇒ 结论：**不是表达式/设置/凭据问题，是 multisim 派发通道故障**。本轮所有回测改用单条 `create_simulation` 完成。
（回退判据：`batch_status` 显示 children 全 FAIL 且 `lookINTO_SimError_message` 只回 `{"status":"FAIL"}` 无 detail。）

### 1.2 ★ `SLOW_AND_FAST` 档当前不可用，而「全闸 ATOM」正是该档产物
本地库里 insiders 塔（单数据集 `insider_agg_matrix`）有一组「看数字全闸」的纯 ATOM：

| alpha | 表达式 | S | F | 2Y | sub | TO | prod（11-05/06 实测） |
|---|---|---:|---:|---:|---:|---:|---:|
| `1YNWJq5m` | `group_rank(ts_sum(subtract(total_top_buy_shares, total_top_sell_shares), 63), industry)` | 2.10 | 1.11 | 1.91 | 0.93 | 4.5% | 0.7982（RA 失败 1） |
| `VkxN0mMJ` | 同上（decay 8） | 2.00 | 1.03 | 1.79 | 1.15 | 4.4% | **0.7647** |
| `d5WaO3Jg` | 同上 | 1.99 | 1.03 | 1.79 | 1.16 | 4.2% | **0.7622** |
| `d5WaO3Jj` | 同上（窗 66） | 1.97 | 1.01 | 1.67 | 1.16 | 4.2% | 未测 |
| `xArv58Am` | 加二级市场腿（同集内） | 1.97 | 1.01 | 1.67 | 1.15 | 4.4% | 未测 |

`VkxN0mMJ` 平台详情：EUR/TOP2500/D1、decay 8、**neutralization = SLOW_AND_FAST**、trunc 0.08、nan ON、maxTrade ON、`checks.fail=[]`、`pyramids.effective = 1`（纯 ATOM）。

**今天用单条通道复跑同表达式**：
- `SUBINDUSTRY` → `kqajW1kK`：**S 0.43 / F 0.14 / 2Y −0.21 / sub 0.21**（`risk_neutralized_sharpe=1.68`）
- `SLOW_AND_FAST` → 单条也未产出 alpha（创建即失败）

⇒ 两条硬结论：
1. **S2.00 是 `SLOW_AND_FAST` 这把「另一把尺子」的读数**（与 `STATISTICAL` 同性质，EUR SOP §8 已定「不可作交付依据」）；标准档（SUBINDUSTRY）下同一信号只有 **S0.43**。
2. 即使退回该档可用，这批 ATOM 的 **prod 已实测 0.762–0.798（撞 0.7 墙）**，本来就不可交付。

### 1.3 换信息源也救不了：pv37 机制臂实测
`pv37_downvolume`（coverage 1.0，αC 163）按 EUR SOP 记录的「成交量冲击比 + winsorize 甜点」构造：

`group_rank(ts_rank(winsorize(divide(pv37_downvolume, ts_mean(ts_delay(pv37_downvolume,1),120)), std=0.3), 66), subindustry)`（TOP2500/SUBINDUSTRY/d4）

实测 `aka7zrZx`：**S 1.98 / F 0.63 / 2Y 0.54 / sub 0.84（限 1.03）/ TO 58.2%** → F、sub、2Y 三闸同败。
与 SOP 记录一致：机制级把 2Y 抬到 0.5–0.6 已到顶，**离 1.58 仍差 1.0**；且 TO 58% 使 F 无法过 1.0。

## 2. 未点亮 6 塔的 ATOM 现状全表（合并本轮 + 本地战史，全部有读数）

| 塔 | 数据集 | ATOM 最好读数（标准档） | 卡在哪 | 结论 |
|---|---|---|---|---|
| institutions | institutions6（11 字段） | 中性化后 **S 0.16**；含 analyst 腿才 S2.2 但已非 ATOM | S 本体 | ATOM 死 |
| insiders | insider_agg_matrix（34 字段） | **S 0.43 / F 0.14 / 2Y −0.21**（标准档） | S+2Y 全灭；S2.0 仅存于不可用的 SLOW_AND_FAST | ATOM 死；且纯净买入 prod 0.76–0.80 |
| pv | pv37（251 字段） | **S 1.98 / F 0.63 / 2Y 0.54 / TO 58%** | F/2Y/TO | ATOM 近闸但结构性不足 |
| earnings | earnings6 | S 0.91（best） | S | 死 |
| socialmedia | socialmedia12（4 可用） | S 0.46；单看 2Y 曾 1.69 但 S 0.46 | S | 死 |
| macro | macro10（**仅 1 字段** `mcr10_value`，αC **1252**） | 从未测 | 字段极薄 + 极拥挤 | 未测即判「高成本低概率」，未投入 |

**唯一接近全闸的 ATOM 在已点亮塔**：`78YjvRRQ` = analyst7-only（`est_12m_ebi` 修正广度，无第二腿，effective=1）
→ **S 1.69 / F 1.05 / 2Y 1.56 / sub 0.88，checks.fail=[]**，只差 **2Y 0.02**。
但 analyst 塔已 10/3 点亮，按红线不进交付。

## 3. 结论

1. **EUR 未点亮塔上 ATOM 今日不可交付**：6 个塔逐一有读数，最好形态仍缺 2Y≈1.0 或 F≈0.4 或 S≈1.1，不是「差一点」而是**量级不足**。
2. **「ATOM 全闸」这一假象的来源已定位**：`SLOW_AND_FAST` 风险中性化线。该类读数与 STATISTICAL 同性质，不能与标准档比较、不能作交付依据（本次已把这条从 SOP 的 STATISTICAL 扩写到 SLOW_AND_FAST）。
3. **prod 是第二道不可越的墙**：即使把 insiders ATOM 的闸做通，纯净买入内核 prod 0.762–0.798 也过不了。
4. 因此交付仍以既有的 **10 颗 regular（analyst 强腿 + 未点亮塔小腿）**为唯一可行解；ATOM 优先已在流程上执行（先打 ATOM，再回退 regular）。

## 4. 若要继续推 ATOM，只剩三条路（按性价比排序）

1. **等 `SLOW_AND_FAST` 恢复并确认其口径**：若平台把该档定性为标准档（而非风险模型线），insiders ATOM 的 5 颗立刻可用——但 prod 0.76+ 仍需同时解决。
2. **macro10 单字段全形态穷举**：1 字段 × 时序/截面/掩码/非线性 ≈ 12 臂，成本低但 αC 1252 意味着 prod 大概率撞墙，预期收益低。
3. **换未点亮塔的数据集**（当前 6 塔合计数据集不足 10 个且多数 1–4 字段），必须先要用户授权新数据集，否则无新矿可挖。

## 5. 本轮产物

- 单条通道成功件：`kqajW1kK`（insiders 基线 SUBINDUSTRY 对照组，用于定位尺子差异）
- pv37 机制臂：`aka7zrZx`（F/2Y/TO 三败，已归因）
- multisim 故障证据：`WpsMy8ai5gbb5Tbv47Q9yA`（10/10 FAIL）、`34sPAR3hS58ybdDhBt5lvXB`（2/2 FAIL）、`wz1A1c4R4y78EWpyf8hBPt`（2/2 FAIL）、`1pzOmQ3jM4jTcu3kPioC2nZ`（2/2 FAIL）
- 未提交任何 alpha（全部 `UNSUBMITTED`）。
