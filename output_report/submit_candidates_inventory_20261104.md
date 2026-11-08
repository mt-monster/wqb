# 各 Region 可提交候选 Alpha 盘点（2026-11-04 15:41 CST）

> 口径：**只挖不提交**，本清单仅为盘点，未执行任何提交动作。
> 交付闸 = REGULAR/SUPER 的 RA 全闸过 + `self < 0.7` + `prod < 0.7`（严格不等式）+ 未提交 + 读数 48h 内新鲜。
> 判定以**平台**为准（`batch_get_alpha_metrics` 的 `failed_ra_count` / `status`）；本地台账只作初筛。
> 数据源：`data/wqb.db`（`alphas` / `alpha_corr_cache` / `submit_ready` / `backtest_results`）+ 平台 `batch_get_alpha_metrics`。

---

## 0. 先说结论与三条硬约束

1. **平台 prod 端点今天下午起停摆**（最近一次成功 peek 02:14，之后 13h 无新值；6 颗候选 × 5 轮 `--peek` 全空体）。因此**所有「交付前终验」`check_correlation(refresh=True)` 现在都拿不到值**，本清单里的 prod/self 只能作为「排序/留档」，不能作为放行依据。
2. **SUPER 配额 = 账号级全局 1/ET 日**，今日已由 `A1V0eZne` 消耗 ⇒ 9 颗 SUPER 候选今日不可提。
3. **REGULAR 配额**今日已有多笔提交（`LLM93nGa` DEU、`vR1korEw` HKG 等），提交前须另查当日剩余额度。

---

## 1. A 档：平台实测双过 + 48h 内新鲜 + 平台 RA 0 fail + UNSUBMITTED（3 颗）

| Region | Alpha | S | F | 2Y | sub | TO | prod | self | 读数年龄 | 来源 | 风险 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **EUR** | `WjOAJWxd` | 2.36 | 1.61 | 2.67 | 1.28 | 0.0795 | **0.6806** | 0.6446 | 3.4h | platform_sync | prod 余量仅 **0.0194**，贴线 |
| **GLB** | `bl6qldJ6` | 2.59 | 1.02 | 2.02 | 1.52 | 0.3532 | **0.5421** | 0.2775 | 29.0h | check_correlation | 余量 0.158，**本档最稳**；F 1.02 贴线 |
| **HKG** | `N1N720Ao` | 1.87 | 1.55 | 1.62 | 1.46 | 0.0598 | **0.6888** | 0.0058 | 4.7h | check_correlation | prod 余量 **0.0112** 极贴线；且同族 `vR1korEw` 今日 11:38 已提交，而 self 读数取于 10:57（**早于提交**）⇒ **self 必须重测** |

平台复核：三颗均 `failed_ra_count=0` / `status=UNSUBMITTED`。

---

## 2. B 档：平台 RA 0 fail + 未提交，但 prod/self 为**本地估算**且已过 48h（GLB 5 颗）

| Alpha | S | F | 2Y | sub | TO | prod(本地) | self(本地) | 年龄 |
|---|---|---|---|---|---|---|---|---|
| `d5WqeQbx` | 2.71 | 1.43 | 2.68 | 1.64 | 0.0755 | 0.5846 | 0.4597 | 51.1h |
| `YP1rzw2J` | 2.95 | 1.77 | 2.17 | 1.67 | 0.1558 | 0.6119 | 0.4807 | 50.9h |
| `QPvJ6KVw` | 3.19 | 1.59 | 3.43 | 1.84 | 0.2897 | 0.6385 | 0.6120 | 51.1h |
| `Xg9rMdvl` | 2.44 | 1.47 | 2.69 | 2.22 | 0.1906 | 0.6512 | 0.5515 | 50.9h |
| `qML1x6vK` | 2.50 | 1.55 | 2.33 | 2.14 | 0.2742 | 0.6867 | 0.4267 | 50.9h |

`source=self_local` ⇒ **不是平台 prod 实测**，按 `wq-prod-corr-read` 判据只能排序、不能放行。
五颗彼此互测未复核，提交前须先跑 `compute_mutual_correlation` 剔同席，再对最终 1 颗做 prod 终验。

---

## 3. C 档：`submit_ready` 队列快照双过 + RA 干净 + 未提交（20 颗，读数时效未知）

`gate=SUBMIT_LAYER_VERIFIED`，但 prod/self 无 `checked_at`，**按纪律只能排序、不能放行**。按区：

| Region | 数量 | Alpha（prod 由低到高） |
|---|---|---|
| **IND** | 15 | `MPYogx0L` 0.3159｜`RREn5rEa` 0.3342｜`bl65Jk6l` 0.3464｜`npvM6WvE` 0.3486｜`E567pmkK` 0.4924｜`2rA0e6MN` 0.4926｜`58jPrvZ1` 0.5354｜`d5WAzegY` 0.5699｜`RREnK5R1` 0.5874｜`KPmvEYeE` 0.6162｜`kqJkPLeO` 0.6177｜`A1VMzqJg` 0.6431｜`E5VNe67L` 0.6643｜`JjP0Ja5l` 0.6651｜`mLYdVKap` 0.6757 |
| **USA** | 2 | `zqrgna91` 0.6877｜`N1eLE1de` 0.6916 |
| **DEU** | 1 | `MPY9VNY9` 0.5986 |
| **GBR** | 1 | `RR62bMje` 0.6573 |
| **KOR** | 1 | `LLZ6wZO2` 0.6762 |

> 已排除：`submit_ready` 里 EUR 三颗（`6XAe27eL`/`Grge2lN3`/`rKd5lAo8`）**10/20–21 已提交**；GLB 8 颗 `LOW_GLB_EMEA_SHARPE` RA 未过；本地标 `[]` 但平台实测 RA 有失败的 `pwdl3OPx`(1) / `E56YX80G`(2，且 investability_ratio −0.14)。

---

## 4. D 档：SUPER（SA 组合线）9 颗，全部平台 RA 0 fail / UNSUBMITTED

| Region | Alpha | 槽位 | S | F | prod | 席判据 |
|---|---|---|---|---|---|---|
| USA | `Xg9WNRg8` | TOP2000 SLOW cp3 | 4.74 | 4.10 | 0.6493 | 与 `A1V0L9KQ` 互测 **0.5777** ⇒ USA 唯一可共存 2 席 |
| USA | `A1V0L9KQ` | TOP1000 SLOW cp3 | 2.90 | 2.03 | 0.6331 | 同上 |
| EUR | `A1V0LZkg` | TOPCS1600 FAST cp1 | 4.53 | 3.89 | 0.6391 | 与 `9qx9aAa2` 互测 **0.7909**（子集关系）⇒ 同席，二选一 |
| EUR | `9qx9aAa2` | TOP2500 FAST cp1 | 4.83 | 3.99 | 0.6699 | 同上 |
| IND | `2rAOGKow` | TOP500 **SLOW** cp3 | 4.43 | 3.58 | 0.6097 | 与 `mLoqx1v1`(FAST) 互测 **0.8677** ⇒ 同席，**选 SLOW** |
| IND | `mLoqx1v1` | TOP500 FAST cp1 | 4.52 | 3.66 | 0.6509 | 淘汰（同席） |
| KOR | `9qxVG66r` | TOP600 SLOW cp7 | 3.95 | 4.55 | 0.6370 | KOR 仅 1 个可新增席 |
| GLB | `GrWdQNq0` | TOP3000 SLOW l15 cp3 | 3.51 | 1.58 | 0.5864 | GLB 仅 1 席 |
| DEU | `QPv3Ww9p` | TOP500 SLOW cp3 | 2.13 | 1.60 | 0.6923 | prod 余量 0.0077，极贴线 |

**⇒ SA 席 = `region` × `selection 表达式`，不是 region × universe × 中性化族。**
按实测互斥阈值（>0.9 硬同席｜0.7–0.9 平台互斥｜<0.5 真新席），9 颗里实际可新增约 **6–7 席**：
USA 2、EUR 1、IND 1、KOR 1、GLB 1、DEU 1。且 SUPER 每日只放 1 颗，须分日、每日先提 prod 更低者。

---

## 5. 按 Region 汇总

| Region | A 档 | B 档 | C 档 | SUPER | 备注 |
|---|---|---|---|---|---|
| EUR | **1** | 0 | 0 | 2（同席→1） | `WjOAJWxd` prod 贴线 |
| GLB | **1** | 5 | 0 | 1 | `bl6qldJ6` 最稳；GLB 另有 8 颗 RA 未过已排除 |
| HKG | **1** | 0 | 0 | 0 | `N1N720Ao` self 需重测（同族今日新提交） |
| IND | 0 | 0 | 15 | 2（同席→1） | C 档数量最多但读数全无时效 |
| USA | 0 | 0 | 2 | 2（可共存 2 席） | |
| DEU | 0 | 0 | 1 | 1 | |
| GBR | 0 | 0 | 1 | 0 | |
| KOR | 0 | 0 | 1 | 1 | |
| **ASI** | 0 | 0 | 0 | 0 | **今日结案：prod 死穴 0.9965**；READY 仅 `0mXexOw6` 且 prod/self 未测 |
| CHN / JPN / AMR / MEA | 0 | 0 | 0 | 0 | **MEA 平台已关闭**（`Region MEA is not available.`），不可新建 |

---

## 6. 建议的下一步（按性价比）

1. **先补平台服务可用性**：prod 端点恢复后，才谈得上任何「终验」。
2. **优先复核 A 档 3 颗**：
   - `bl6qldJ6`（GLB，余量 0.158）最值得先做 `check_correlation(refresh=True)`；
   - `N1N720Ao` 必须先重测 self（同族 `vR1korEw` 今日已提交）；
   - `WjOAJWxd` prod 余量 0.019，按「prod 贴线优先低 prod 变体」判据，风险偏高。
3. **B/C 档先用免费层剔同席**：`compute_mutual_correlation`（本地，不占槽）+ `check_correlation(refresh=False)` 命中缓存；**禁止**把 `refresh=True` 当批量筛选器。
4. **SUPER 线分日排队**：账号级 1/ET 日，按 prod 升序逐日提；同席的 EUR/IND 二选一。
5. 提交前逐颗确认：当日 REGULAR/SUPER 配额、48h 保鲜、`investability`（`E56YX80G` 已因负值剔除）。

---

## 7. 数据来源与可信度说明

- `alpha_corr_cache.source`：`platform_sync` / `check_correlation` = 平台实测；`self_local` / `prod_artifact` / `prod_first_screen` = 本地估算或快照，**只能排序**。
- `submit_ready` 表 READY 共 184 行，其中 prod/self 双过 41 行；排重（已提交 / RA 未过 / 平台复核失败）后剩 20 行，即 C 档。
- 平台 `get_user_alphas(stage=IS, type=REGULAR)` 总数 10000，无法逐页扫；故采用「本地精确初筛 → 平台 `batch_get_alpha_metrics` 复核」两阶段，符合「判定只走平台」。
- 本地 `ra_failed_checks` 与平台 `failed_ra_count` 存在分歧（已剔除 2 颗），**一律以平台为准**。
