# USA/D1 ATOM 战役索引（2026-11-22）

> **状态：暂停（用户 2026-11-22 裁定「暂停」）**。本轮未提交任何 alpha，无后台任务，并发遵守「一波结束再派下一波」。
> 用户目标：固定 USA、排除已点亮塔、ATOM 优先、交付 **10 个通过验证的 regular alpha**。
> 约束：PV/MODEL/OTHER 不两两组腿；multi-sim 并发 ≤2、一波结束再派下一波；只在 MCP 前台执行。
> 本文件是战役级索引：数据集扫描 → 字段画像 → 机制/梯度 → 判死/停投 → 交付。

---

## 1. 平台塔位快照（`get_pyramid_alphas`，USA/D1，2026-11-22）

| 状态 | 塔 |
|---|---|
| **已点亮（≥3）** | MODEL 4 / ANALYST 6 / OTHER 5 / RISK 3 / EARNINGS 3 |
| **0/3 未点亮** | PV / FUNDAMENTAL / NEWS / SENTIMENT / MACRO / IMBALANCE / OPTION / SOCIALMEDIA |
| **1/3 未点亮** | INSIDERS / SHORTINTEREST / INSTITUTIONS |

**已点亮塔一律排除**（用户约束）；本波只在 0/3 与 1/3 塔内选集。

---

## 2. 类别扫描与数据集判定

| 类别 | 塔 | 平台集数 | 已测/已判死 | 本波动作 |
|---|---|---|---|---|
| PV | 0/3 | 12 | pv20/pv47/pv103/pv106/pv115/pv149/dl_volume_pred 已弱/封存 | **pv63**（16 字段 aC6–31）全字段探针 + 六机制 |
| FUNDAMENTAL | 0/3 | 7 | fnd13/22/25/35/69/110/other452 全测弱 | 不再投（11-21 已穷尽） |
| NEWS | 0/3 | 12 | news22/48/52/76/84/97/3/73/event_return 全否证 | 不再投（11-21 已穷尽） |
| SENTIMENT | 0/3 | 5 | sentiment1/7/26 弱/数据层排除 | sentiment27（17 慢变量）待扫 |
| OPTION | 0/3 | 4 | option3/9 标准档崩 | option6/option8 未测，但 aC 19k/236k 偏热 |
| SOCIALMEDIA | 0/3 | 3 | socialmedia8/12 全灭 | socialmedia5（13 字段）待扫 |
| MACRO | 0/3 | 6 | macro10/38/63/other551 全否证 | 不再投（macro4 单国无横截面） |
| IMBALANCE | 0/3 | 1 | imbalance5 2Y/TO 不过 | 不再投 |
| INSIDERS | 1/3 | 4 | insiders1/4/agg_matrix/board_gov 全测；queue 高 S 件 invest≈0 | 不再投（invest 墙） |
| SHORTINTEREST | 1/3 | 6 | shortinterest29/43/us_short_sale 弱；shortinterest3 prod 饱和 | **short_interest_pred** 全字段 + **shortinterest3** 机制梯度 |
| INSTITUTIONS | 1/3 | 4 | institutions18 prod sealed；institutions6 弱 | **institutions20** 全字段 + 比例机制 |

---

## 3. 数据集深挖结果

### 3.1 `short_interest_pred`（SHORTINTEREST 1/3）→ **PROVISIONAL（F 墙）**

- 全字段 10/10 探针：最强内核 `-rank(short_interest_predicted_change)` S1.49/2Y2.50/TO68.6%。
- L1 内核 10 臂：平滑把 S 砍到 ≤1.10，F ≤0.38。
- L2 换手 10 臂：`trade_when(z>1.0)` TO22.5%/S1.36/F0.47；hump 直接打没。
- L3 慢速 10 臂：慢速水平 S≤0.55；`change−prior_change` S1.45/F0.55/2Y1.23。
- **结论**：F≥1.0 需 ret/TO≥0.44（实测 0.122–0.34）⇒ 快信号 F 结构性不可达。画像见 `datasets/short_interest_pred.md`。

### 3.2 `shortinterest3`（SHORTINTEREST 1/3）→ **PROVISIONAL（prod 饱和）**

- 存量队列两颗（费率波动）MPYwqvLn / omE2vmZn：S1.74/F1.37–1.40/TO14–18%/2Y3.0–3.3/invest0.93–0.97/self0.30–0.33，**prod 0.7342 / 0.7793 超线**。
- 机制批 10 臂：新发现**费率离散度** `max−min` Grm9LXbZ S1.98/F2.53/TO6.19%/2Y3.11（仅 SUB 0.84 vs 0.86）。
- 梯度 10 臂：window66 版 LLK3denv **RA 全绿**（S1.95/F2.53/SUB0.92/invest0.826），但 **self 0.7135 + prod 0.9499 双挂**；market 分组版 prod 0.9091；vol-of-vol prod 0.8419。
- **结论**：4 条机制 prod 全部 0.73–0.95，直方图 [0.7,0.8) 383–470 颗 = 密墙 ⇒ 该集在 production 池无头寸空间。画像见 `datasets/shortinterest3.md`。

### 3.3 `institutions20`（INSTITUTIONS 1/3）→ **PROVISIONAL（比例机制弱 + 强机制 self 撞车）**

- 全字段 17/17 探针：仅无描述的 `inst20_ra_*` 有 |S| 0.5–1.1（CW 失败，不入选型）。
- L1 比例 10 臂：exempt share 族 S≤0.22；venue spread S1.11/F0.24/TO63.7%；short share level S0.61。
- 唯一强机制（做空占比双 zscore）撞自家 OS `akKW0Lax`（self 0.80–0.96）。画像见 `datasets/institutions20.md`。

### 3.4 `pv63`（PV 0/3）→ **PROVISIONAL（signal-short）**

- 16/16 字段探针：水平量 |S|≤0.46（全为规模代理）。
- 六机制：trade/dollar imbalance 反号后 S0.93/0.94 但 TO 62.9%、2Y −0.71；OFI/报价压力 S≤0.66。
- **结论**：PV 塔 0/3 仍未找到可交付机制。画像见 `datasets/pv63.md`。

### 3.5 未亮塔新面全部穷尽 → 本轮 0 交付

| 数据集 | 塔 | 臂数 | 结局 |
|---|---|---|---|
| short_interest_pred | SHORTINTEREST 1/3 | 30 | F 墙（PROVISIONAL） |
| shortinterest3 | SHORTINTEREST 1/3 | 22 | prod 密墙 0.73–0.95（PROVISIONAL） |
| institutions20 | INSTITUTIONS 1/3 | 27 | 比例机制弱 + 强机制 self 撞车（PROVISIONAL） |
| pv63 | PV 0/3 | 26 | signal-short（PROVISIONAL） |

---

## 4. 交付清单（未亮塔 only）

| # | alpha | 数据集 | 塔 | S | F | TO | 2Y | invest比 | prod | self | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — | — | — | **0 颗** |

**结论：在「排除已点亮塔 + 全闸（S≥1.58/F≥1.0/TO5-30%/2Y≥1.58/invest≥0.70/prod<0.70/self<0.70/RA=0）」约束下，
USA/D1 未亮塔面已无可交付 alpha。** 与 2026-11-21 全量穷尽结论一致。

### 4.1 若放宽「排除已点亮塔」：已亮塔有 7–8 颗全闸存量件（可直接补到 10）

| alpha | 塔 | S | F | TO | 2Y | invest比 | prod | self | RA |
|---|---|---|---|---|---|---|---|---|---|
| `zqrgna91` | MODEL（已亮） | 2.67 | 1.66 | 0.1579 | 1.68 | 1.011 | 0.6877 | 0.287 | 0 |
| `9qxLOPxr` | MODEL | 2.69 | 1.67 | 0.1592 | 2.24 | 1.011 | 0.6835 | 0.287 | 0 |
| `6XdvLPd5` | MODEL | 2.65 | 1.63 | 0.1606 | 2.13 | 1.011 | 0.6852 | — | 0 |
| `N1eLE1de` | MODEL | 2.63 | 1.54 | 0.1409 | 2.07 | 0.951 | 0.6916 | 0.275 | 0 |
| `akKq92aO` | MODEL | 2.62 | 1.53 | 0.1419 | 2.07 | 0.947 | 0.6970 | — | 0 |
| `9qWpQlO9` | ANALYST（已亮） | 1.78 | 1.05 | 0.0619 | 1.69 | 1.079 | 0.6982 | 0.409 | 0 |
| `mLaJ1Zq5` | EARNINGS（已亮） | 1.77 | 1.11 | 0.0718 | 3.35 | 0.791 | 待测 | — | 0 |
| `xAvb03mp` | MODEL（11-21 遗留） | 2.65 | 1.64 | 0.158 | 1.61 | 1.015 | 0.6875 | 0.352 | 0 |
| `9qlW0R6e` | MODEL（11-21 遗留） | 2.66 | 1.43 | 0.227 | 3.50 | 0.985 | 0.6771 | 0.432 | 0 |

⚠ 这些全部落在**已点亮塔**（MODEL/ANALYST/EARNINGS），按当前约束不可交付；
放宽后需补 prod refresh + 互相关（MODEL 族内部可能同族，需两两 <0.5 筛）。

---

## 5. 方法学沉淀（可复用）

1. **F 公式是快信号的结构墙**：`F = S·√(ret/max(TO,0.125))` ⇒ 要 F≥1.0，S1.5 时需 ret/TO≥0.44。
   日频流量类（预测变化、surprise）实测 ret/TO 仅 0.07–0.14，平滑降 TO 会同步砍 ret ⇒ 不可救。
   ⇒ **选集先看信号速度**：慢变量（借贷/持仓/月度排名）才是 F 友好面。
2. **prod 墙先看直方图形态**：单钉（[0.7,0.8) n≤5）可试变体；密墙（n≥100）换窗口/分组轴无效，
   实测 shortinterest3 四条机制全部 0.73–0.95。
3. **self 撞车优先于 prod**：本地 self 零配额、秒级；先跑 self 再烧 prod 槽。
4. **队列存量件必须全量复扫**：前 20 条之外的 39 条里有 10+ 条全指标件（多数在已亮塔/SUPER）。
5. **ATOM 单集多字段组合合法**（同集 add/multiply），但跨集组腿仍禁。
