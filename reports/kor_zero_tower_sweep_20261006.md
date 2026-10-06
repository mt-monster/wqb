# KOR/D1 「0 计数塔」全扫描报告

**日期**：2026-10-06 ｜ **区域/设置**：KOR / D1 / TOP600 / truncation 0.08
**触发**：用户指令「不要在已计数塔上回测」→ 系统扫过全部 12 个零计数塔

---

## 一、结论（一句话）

> **KOR/D1 的 12 个零计数塔已全部扫完，无一产出可提交 alpha。**
> 唯一高产的 KOR 数据集仍是 MODEL 塔的 `multifactor_return_pred`（已出 2 颗提交，2 条 hedge 腿用尽）。

---

## 二、12 个零计数塔战绩

| 塔 | 集数 | 已探 | 代表集 / 最强信号 | 最强 S | 死因 |
|---|---|---|---|---|---|
| **ANALYST** | 17 | 4 | `analyst39.anl39_roxlcxspeq` | **1.81** | **prod 族级拥挤 `n[0.7,0.8)=14`**（稳在 0.77，非单钉）|
| **RISK** | 7 | 1 | `risk70.rsk70_mfm2_asetrd_dsrt`（特质收益）| **2.01** | **TO 0.83**；hump 压到 0.69 后 **F 仅 0.78 < 1.0** |
| SENTIMENT | 6 | 2 | `sentiment23` / `sentiment21` | — | 覆盖度 0.26 / 0.475（太低）|
| PV | 18 | 3 | `continuation_score` / `pattern_scores` / `intraday_pv_feats` | 0.72 | 形态相似度 + 盘中特征**全灭**（1638 字段）|
| NEWS | 24 | 3 | `news7.news_mention_frequency_1` | 0.01 | 弱 |
| **OTHER** | 27 | 8 | `mmp_nlp_sentiment`（521 字段 vs7）| \|1.06\| | NLP 计数 \|S\|≈1.0 且 TO 0.51；比率结构更弱 |
| INSIDERS | 2 | 1 | `insiders5.insd5_tnc` | 0.57 | 弱 |
| INSTITUTIONS | 2 | 1 | `count_institutional_buyers_security` | −0.18 | 弱 |
| EARNINGS | 1 | 1 | `earnings3.ern3_pre_interval` | −0.47 | 弱 |
| IMBALANCE | 1 | 1 | `imbalance5.imb5_score` | 1.24 | 仅 2 字段；换中性化档**反而更弱**（0.70/0.39）|
| **MACRO** | 2 | 2 | `macro63.mcr63_membership` / `other106.ospi_*` | 0.47 | 指数成分 / 权重因子（**非方向性信号**）|
| **SOCIALMEDIA** | 2 | 2 | `socialmedia39.top5_people_also_watch_ticker_ii` | −0.52 | 共看代码 **ID 列表**（`vec_avg` 取 ID 无意义）|

---

## 三、本轮新增的 3 条通用判据

1. **`n[0.7,0.8)` 桶规模 = 族拥挤度**
   `0` 可提交 ｜ `1~3` 单钉可微调 ｜ **`≥8` 族级拥挤且 prod 中位 >0.70 ⇒ 判死**（`analyst39` 实证 n=14、prod 稳 0.77）。

2. **设置是骨架专属，禁跨族外推**
   `SECTOR/decay6/maxTradeON` 对 MODEL 的 `hedge×seasonal` 有效；重打到 `imb5`（1.24→0.77）与 `mmp`（1.06→0.51）**都更差**。

3. **本地 catalog 对新数据集不可信（双向）**
   `ml_factor_proj` 本地标 cov=1.0 / 333 字段，**平台完全不存在** ⇒ 报 `unknown variable` 并**连坐整批 CANCELLED**。
   ⇒ 陌生数据集**发批前必 `get_datafields` 实地核字段名**（离线三闸 `ensure_safe_for_dispatch` 不查存在性）。

---

## 四、工程侧

- 本会话自建脚本（`tracking/KOR/scripts/*.py`）被并发清理反复删除 ⇒ 已改为**内联执行**（`python - << EOF`），最稳。
- `wqb.expression.op_arity` 现行接口 = `ensure_safe_for_dispatch(exprs)`（抛 `ArityError`）；旧的 `check_unknown_operators` 已移除。
- 本会话新起 6 波（d121~d126），**全部无产出**（d121 因 `ml_factor_proj` 连坐 CANCELLED）。

---

## 五、当前 KOR 战况与出路

| 项 | 状态 |
|---|---|
| 已提交 | **3 颗**：`O08kz5Mv`(SHORTINTEREST) · `gJZR9XNm`(MODEL) · `0mre68gv`(MODEL) |
| 候选池 | **0**（此前 8 颗全废，见同族连提实测）|
| 塔计数 | `fundamental` 3（已点亮）/ `model` 2 / `shortinterest` 1 / **其余 12 塔全 0（已扫完）** |

**两条出路（都需用户拍板）**：
1. **回到 MODEL 塔**（已 2/3，**再 1 颗即点亮**）—— 直接、有产出，但违反「不要集中在已点亮塔」的指令；
2. **换区**（用户当前锁定 KOR）—— 结构性提升总产出，但属变更既定范围。
