# RISK 塔生产池墙：3/3 全灭（决定性判死）

> 实测时间：2026-10-29 20:23 – 21:05
> 来源：`prod_wait.py`（带锁真算 `b.get_production_correlation()`），结果已 `persist_correlation(source="platform_sync")` 落库

## 1. 三颗实测结果

RISK 塔原本是本会话最完整的资产 —— 三颗 `fRA=0`、**两两自相关全部 < 0.7**、`size=3 exact` 的可共存集。

| alpha | 机制 | S | F | TO | 2Y | SUB | invest_S | ratio | fRA | self-corr | **prod** | 判定 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `88RAN85m` | 平台 decay 8 + `ts_av_diff(rsk65_trsd_4mfte_mfm,252)` | 2.68 | 1.01 | 61.77% | 1.68 | 2.21 | 2.27 | 0.8470 | **0** | 0.4696 ✅ | **0.8971** | ❌ **BLOCKED** |
| `ZYQZEawY` | `ts_decay_linear` + `discount_store_retail_score` | 1.64 | 1.00 | 18.58% | 1.64 | 0.78 | 1.32 | 0.8049 | **0** | 未测 | **0.8817** | ❌ **BLOCKED** |
| `qMLbW8xP` | `short_interest_factor_score_2` + `ts_mean(x,22)` | 1.73 | 1.02 | 8.19% | 2.48 | 0.84 | 1.77 | 1.0231 | **0** | 未测 | **0.8325** | ❌ **BLOCKED** |

**三颗全部撞墙，prod 区间 0.8325–0.8971，极差仅 0.0646。**

## 2. ★ 核心发现：互相相关低 ≠ prod 相关低

这是本次最重要的一条认知，直接推翻了一条常用的乐观推理。

**三颗之间的两两相关（4 年 986 点，`compute_mutual_correlation`）**：

| | `88RAN85m` | `ZYQZEawY` | `qMLbW8xP` |
|---|---|---|---|
| `88RAN85m` | 1.0 | 0.652 | **0.0903** |
| `ZYQZEawY` | 0.652 | 1.0 | **0.1277** |
| `qMLbW8xP` | 0.0903 | 0.1277 | 1.0 |

`qMLbW8xP` 与另两颗的相关只有 **0.09 / 0.13**（几乎是正交的），`max_mutually_below_subset = size 3, exact` —— 从自相关视角看，这是**教科书级的多样化组合**。

**但对生产池的 prod 全部 0.83–0.90。**

**机理**：生产池里**同时**有这三类因子的海量变体 ——
- `88RAN85m` ≈ 特质残差反转（idiosyncratic residual reversal）
- `ZYQZEawY` ≈ 残差收益 % 的衰减版（`discount_store_retail_score` 实为「特质残差日收益 %」）
- `qMLbW8xP` ≈ 卖空因子分数

它们彼此不同（因为用了不同的风险模型/因子构造），但**三类机制在平台生产池里都已经饱和**。所以「互相不相关」只证明它们不是同一个 alpha，**不证明它们不是同一批拥挤机制的变体**。

## 3. ★ 族级外推规则（已验证）

| 族 | 成员 | prod | 极差 |
|---|---|---|---|
| `risk65` 残差 + `mfm` 风格因子 | `88RAN85m` / `ZYQZEawY` / `qMLbW8xP` | 0.8971 / 0.8817 / 0.8325 | **0.0646** |
| `shortinterest3` 费率族（历史） | `kqNRbvJP` | 0.8463 | — |

⇒ **一个族只要测出第一颗 prod > 0.80，同族其余候选的提交优先级直接降到最低，不值得逐颗花 90–240s 的 prod 时隙去验。**
⇒ 反过来：**先花一次 prod 测「族代表」再决定要不要量产该族**，比先量产再逐颗测省得多。

## 4. 对 RISK 塔的终局判断

| 候选 | 状态 |
|---|---|
| `88RAN85m`（★最佳，S 2.68 / 全闸通过） | ❌ prod 0.8971 |
| `ZYQZEawY` | ❌ prod 0.8817 |
| `qMLbW8xP` | ❌ prod 0.8325 |
| `P0oe533W`（fRA=0 替补，同 `rsk65_trsd_4mfte_mfm` 字段） | 按族级外推 ⇒ **预计同样撞墙，不测** |
| `xArMvoml` / `58ERJXN5` / `gJevaNVQ`（波 190，同族） | 同上，不测 |
| `ZYMzrnZv` / `vR101gVG` / `0mYoPb12` / `akKJa3gR` / `0mYoPl8v`（波 188 其他 decay 档） | 同上，不测 |

**⇒ RISK 塔通过 `risk65` / `mfm_model_output` 这两条路短期不可点亮。**
波 182–190 共 9 波、约 60 条回测的 IS 资产（含 3 颗 fRA=0 全闸候选）**全部因 prod 墙作废**。

**这不是参数问题，是机制选择问题**：RISK 类数据集（风险模型残差、风格因子分数）天生映射到生产池的公共因子，USA 区的生产池在这一层已极度饱和。

## 5. 方法论沉淀（写入主记忆）

1. **prod 是 USA 区当前最硬的约束，不是 IS 指标**。本会话累计 ~30 颗 IS 全闸或近闸候选，prod 实测的 4 颗（`88RAN85m` / `ZYQZEawY` / `qMLbW8xP` / `kqNRbvJP`）**全部 0.83–0.90**。
2. **低互相相关是必要不充分条件**。判「能不能提交」必须测 prod，不能用 mutual correlation 代替。
3. **族代表优先**：同族先测 1 颗，> 0.80 就全族封盘。
4. **转区或转数据集**：USA 的 RISK 类（risk65 / mfm_model_output / risk59 / shortinterest3）机制已饱和；相对空旷的是**低 alphaCount 的非价格类数据集** —— `board_gov_stats`（177）、`surname_concentration_total_personnel`（0）、`insider_agg_matrix`（8）、`web_traffic_engage`。
5. **低拥挤 ≠ 低 prod 墙**（`board_gov_stats` 的 prod 尚未测，必须在投入大量仿真前先测族代表）。
