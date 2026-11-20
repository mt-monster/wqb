# EUR 交付报告（ATOM 优先口径，2026-11-19 修订版）

> 用户 2026-11-19 更正交付物标准：**ATOM 优先**。本报告取代 `EUR_regular_alpha_delivery_20261118.md` 成为当前交付口径：
> **ATOM 区在前（先挖尽，0 颗）；regular fallback 区在后（10 颗，ATOM 穷尽举证后合规）**（AGENTS §7.7）。
> 全程 EUR/D1，未提交任何 alpha（提交须用户显式确认）。

## 1. ATOM 区（优先交付）：0 颗 —— 六塔逐一举证

六个未点亮塔（pv 2/3、insiders 2/3、earnings 1/3、institutions 0/3、socialmedia 0/3、macro 0/3，塔位实读 2026-11-19）**全部 ATOM 路径已穷尽**，无一可交付。证据分三类：

### 1.1 全闸可达但 prod 墙（最接近交付的一类）

| 数据集（塔） | 全闸 ATOM | S | F | 2Y | sub | RA | prod（新鲜实测） | 判定 |
|---|---|---:|---:|---:|---:|---|---:|---|
| earnings_sent_matrix（EARNINGS） | wpQjEAPl | 1.93 | 1.37 | 1.70 | 1.49 | 0 | 0.8713 ❌ | 信息源级 prod 墙 |
| earnings_sent_matrix | d5Wj0Nx2 | 1.90 | 1.35 | 1.81 | 1.44 | 0 | 0.8809 ❌ | 同上 |
| earnings_sent_matrix | **KPgNqaEk**（method1 首测） | **1.99** | **1.42** | **1.98** | 1.52 | 0 | **0.9229** ❌ | 同上 |
| earnings_sent_matrix | **78YN09n5**（method2 首测） | **1.91** | **1.36** | **1.82** | 1.43 | 0 | **0.8797** ❌ | 同上 |
| fund_holdings_panel（INSTITUTIONS） | zq378ELo | 1.64 | 1.05 | 2.61 | 1.17 | 0 | 0.8887 ❌ | prod 墙（九年数据已按用户 2026-11-19 放宽口径接受） |

- **sent_matrix 的墙是信息源级**（同一份电话会转录本的 4 种读数 prod 0.87–0.92）；唯一有效杠杆（换宇宙）量级 −0.03，缺口 0.18+ ⇒ **数学上不可达**，不再烧配额。7/7 字段全部实测。
- **fund_holdings_panel 的唯一缺口是 prod**（0.8887，缺口 0.19 > 杠杆上限 0.03）：2014 全年零持仓（数据 2015–2023 九年）**按用户 2026-11-19 放宽口径（近十年 → 最近九年、缺失仅限序列起点）已接受，数据层不再是排除理由**（见 `docs/experience/01_platform_gates.md` §16.2）。

### 1.2 信号层时效死（S/F/sub 可过、2Y 结构性不足）

| 数据集 | 最好臂 | S | F | 2Y | 读数 |
|---|---|---:|---:|---:|---|
| **pv47**（PV，EUR 首测 31 臂） | P052jb8J / wpoZwNK2 | 1.86 / 1.85 | **1.01 / 1.06** | **1.10 / 1.05** | 六维闭合、十年满仓，**2Y 天花板 1.05–1.27**；逐年定位 2018（S0.35）/2022（S0.87） |
| pv20（PV） | P05EONAK | 1.76 | 0.72 | 0.92 | TO 68%、F/2Y 双败 |
| pv37（PV） | aka7zrZx | 1.98 | 0.63 | 0.54 | F/sub/2Y 三败（2026-11-13 已闭合） |

### 1.3 信号本体不足 / 结构性排除

| 数据集（塔） | 最好读数 | 判定 |
|---|---|---|
| institutions6（INSTITUTIONS） | **买家比例 GrmbwmmO S1.32/F0.67/2Y1.48/TO7.3%（40 臂 2026-11-19 新测；旧 S0.16 系家数变体）；prod 0.8257** | 限投（S/F 双缺口，F 数学约束不可破） |
| insider_agg_matrix（INSIDERS） | S 0.43 / F0.14 / 2Y−0.21（S2.0 仅存于不可用的 SLOW_AND_FAST） | 死 |
| earnings6（EARNINGS） | S 0.91 | 死 |
| socialmedia12（SOCIALMEDIA） | S 0.46 | 死 |
| pv13（PV） | rel_ret 关联溢出族 6 臂 \|S\|≤0.28 | 族级探针死 |
| macro10 / macro27 / socialmedia15 / insiders1 / insiders12 / pv109 / pv173 / pv87 / pv103 / pv149 / univ1 / univ2 / chart_return_model | 单标量无截面 / cov<0.5 / 元数据 / EUR 未注册 / 平台空集 | 结构性排除 |

**完整证据与臂数记录**见 [`EUR_atom_exhaustion_audit_20261119.md`](EUR_atom_exhaustion_audit_20261119.md)（本轮新增 43 臂全 COMPLETE + 2 次新鲜 prod 实测）。

## 2. ATOM 穷尽举证（§7.7 合规依据）

1. **六塔全数据集覆盖**：6 个未点亮塔共 30+ 数据集，逐一有读数（§1 表）；每类均有本会话或 2026-11-13/19 战役的平台实测，无「凭名字推断」。
2. **pv47 六维闭合**（唯一本轮新数据集）：D1 12+ 互异结构 / D2 2/2 字段 / D3 四矩全 / D4 四轴 / D5 两非线性 / D6 四配置——2Y 仍在 1.05–1.27 封顶。
3. **sent_matrix 7/7 字段全测**：4 颗全闸件 prod 0.87–0.92，信息源级墙数学不可达。
4. **fund_holdings 30/30 字段全测**：全闸除 prod（0.8887）；九年数据（2015–2023）按用户 2026-11-19 放宽口径接受，唯一缺口 = prod。
5. ⇒ 按用户 2026-11-17 裁定「ATOM 优先，实在没有 ATOM 就挖 regular」，**允许 regular fallback，且只许 gating/grouping/residual/ratio 四形态**。

## 3. regular fallback 区（10 颗，继承并复验）

10 颗跨集 regular 的完整明细（数据集/核心字段/算子逻辑/指标）见 [`EUR_regular_alpha_delivery_20261118.md`](EUR_regular_alpha_delivery_20261118.md) §1–§3。**本会话复验**（`batch_get_alpha_metrics` 10/10 平台打通、`failed_ra_count=0`、全部 UNSUBMITTED）：

| # | alpha | 塔 | S | F | 2Y | TO | prod（当日实测） | self |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | N1NGbddg | INSTITUTIONS | 1.69 | 1.05 | 2.17 | 5.14% | 0.6872 | 0.6595 |
| 2 | vRAvo8jA | INSTITUTIONS | 1.72 | 1.06 | 2.27 | 5.18% | 0.6781 | 0.6446 |
| 3 | leAXvaLn | INSTITUTIONS | 1.78 | 1.06 | 2.10 | 5.31% | 0.6951 | 0.6950 |
| 4 | A1x7E3ae | INSIDERS | 1.84 | 1.15 | 2.25 | 5.07% | 0.6604 | 0.6016 |
| 5 | RRemVOeb | INSIDERS | 1.84 | 1.15 | 2.22 | 5.07% | 0.6615 | 0.6014 |
| 6 | 2r5NgWvY | SOCIALMEDIA | 1.65 | 1.01 | 2.07 | 5.11% | 0.6785 | 0.6548 |
| 7 | e75x1vAl | PV | 1.72 | 1.20 | 2.03 | 6.34% | 0.5469 | 0.4228 |
| 8 | mL61avpx | PV | 1.78 | 1.24 | 2.13 | 6.92% | 0.5423 | 0.4367 |
| 9 | 58geG1P1 | PV | 1.79 | 1.25 | 2.17 | 6.93% | 0.5362 | 0.4342 |
| 10 | E56GgqLL | OTHER | 1.68 | 1.17 | 2.12 | 5.92% | 0.5524 | 0.4347 |

- 已知边界（如实声明）：10 颗实为 3 个机制族（EBI 修正广度 ×6 / fnd72 现金流质量 ×3 / fnd72×OTHER ×1），族内互相关 0.80–0.9986；真正互相关 <0.7 的最大子集 = 3 颗。单颗硬闸全部独立通过。
- 组合合规：PV/MODEL/OTHER 之间零两两组合；受限类跨类组合 4 个（PV×FUNDAMENTAL 3 + OTHER×FUNDAMENTAL 1）≤ 5。
- 逐年满仓：抽验 5 颗覆盖 4 个数据族，2014–2023 longCount/shortCount 全 >0。

## 4. 字段画像存档索引（本轮新增 2 份）

| 数据集 | 全字段数 | 画像档案 | 完整性闸 |
|---|---:|---|---|
| institutions6 | 11 | `tracking/EUR/reference/profiles/eur_institutions_institutions6_profile_20261118.md` | PASS 11/11 |
| insider_agg_matrix | 34 | `tracking/EUR/reference/profiles/eur_insiders_insider_agg_matrix_profile_20261118.md` | PASS 34/34 |
| fund_holdings_panel | 30 | `tracking/EUR/reference/profiles/eur_institutions_fund_holdings_panel_profile_20261119.md` | PASS 30/30 |
| earnings6 + earnings_sent_matrix | 73 | `tracking/EUR/reference/profiles/eur_earnings_earnings6_earnings_sent_matrix_profile_20261119.md` | PASS 73/73 |
| **pv47** | **2** | `tracking/EUR/reference/profiles/eur_pv_pv47_profile_20261119.md` | **PASS 2/2** |
| **pv13** | **73** | `tracking/EUR/reference/profiles/eur_pv_pv13_profile_20261119.md` | **PASS 73/73** |

命名规则 `eur_<category>_<dataset>_profile_<YYYYMMDD>.md`，索引 `tracking/EUR/reference/profiles/README.md`；原始目录 JSON `tracking/EUR/reference/eur_<dataset>_fields.json`（本轮新增 `eur_pv47_fields.json`、`eur_pv13_fields.json`）。

## 5. 本次调优经验摘要（2026-11-19 ATOM 轮新增，可复用）

1. **prod 墙的信息源级判定**：同一数据集的多种读数（sent_matrix 的 prob 组合 / method1 / method2）换读数后 IS 全闸（S1.90–1.99）但 prod 同墙（0.87–0.92）⇒ **判「信息源级拥挤」而非「形态不佳」**，别再换算子。
2. **prod 破墙杠杆的量化上限**：形状改造 0.015/维、换宇宙 −0.03 ⇒ **缺口 >0.10 即数学不可达**；只有换信息源（另一个数据集）才可能。
3. **2Y 时效定律再确认（pv47）**：六维闭合 + 十年满仓 + S/F/sub 全可过，2Y 仍封顶 1.05–1.27；逐年定位 2018/2022 熊市年 ⇒ **2Y 是信号时效闸，不是形态闸**（SOP #4 跨数据集复现）。
4. **TOPCS1600 的族向依赖**：对 pattern 族是 prod 解药（−0.03），对 pv47 反转族是**毒药**（2Y 1.06→0.47、S 1.94→1.60）⇒ 宇宙选择必须逐族实测。
5. **残差动量符号不可移植**：Blitz(2011) 残差动量在 EUR pv47 上 **S −0.32（方向反了）**，同字段短窗反转 S1.9 ⇒ 跨区/跨读数先跑方向对照臂。
6. **经济关联 lead-lag 在 EUR 日频已被套利**：pv13 rel_ret 族 6 臂 |S|≤0.28（cov 0.44–0.69，稀疏）⇒ 关联溢出类机制不投入。
7. **全字段探测闸对新数据集即捕即用**：pv13 平台实读 **73 字段**，本地 `datasets` 表旧快照只记 3 ⇒ 画像必须以平台 `get_datafields` 全量拉取为准（本闸 73/73 PASS）。

## 6. 提交纪律

本轮**未提交任何 alpha**（10 颗 fallback 全 UNSUBMITTED，43 个新探针件未提交）。提交前须：用户显式确认 + `check_correlation(refresh=True)` 当场终验 prod 漂移 + `submit_verdict` 不 BLOCKED + `workflow_submit_alpha(confirm_submit=True)`。
