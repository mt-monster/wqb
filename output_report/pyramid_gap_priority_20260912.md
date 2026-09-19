# 金字塔补塔优先级清单（VFT / 点亮双视角）

> 生成时间：2026-09-12　账号：**MT38799**（GOLD / CONSULTANT_APPROVED）
> 数据来源：平台 `pyramid-multipliers` 端点 + `get_user_alphas(OS)` + 逐 alpha `get_alpha_details` 的 `pyramids` 字段
> 口径：点亮 = 近 90 天该格 ACTIVE ≥3；覆盖 = 有 REGULAR 提交（VFT 的 S_P 分子）

## 1. 总览

| 指标 | 值 |
|---|---|
| 平台金字塔格子总数 | 212 |
| 已点亮（ACTIVE≥3） | **16** |
| 部分点亮（ACTIVE 1–2） | 14 |
| 完全空白（365 天零提交） | **182** |
| 有提交但近 90 天无 ACTIVE（沉寂） | 0 |
| VFT 覆盖 P | 30 / 212 = 0.142 |

### multiplier 分布（平台收益加成系数）

| multiplier | 格子数 |
|---|---:|
| 2.0 | 1 |
| 1.9 | 21 |
| 1.8 | 18 |
| 1.7 | 19 |
| 1.6 | 21 |
| 1.5 | 17 |
| 1.4 | 24 |
| 1.3 | 23 |
| 1.2 | 19 |
| 1.1 | 27 |
| 1.0 | 22 |

## 1.5 ⚠ 重大错配：MEA 不在平台金字塔体系内

| 项 | 值 |
|---|---|
| 212 格区域构成 | USA 31 / DEU 30 / GBR 30 / EUR 27 / CHN 20 / ASI 16 / KOR 15 / HKG 15 / IND 15 / GLB 13 |
| **MEA 格子数** | **0** |
| 本账号 MEA 投入 | **33 个 alpha**（ANALYST 14 + FUNDAMENTAL 11 + MODEL 4 + PV 3 + EARNINGS 1） |
| 占 365 天 REGULAR 提交 | **41%**（33/80） |

**结论**：MEA 属平台金字塔体系**外**区域 —— 投入既不计入点亮，也拿不到 multiplier 加成。
占四成的提交量投在零格子的区域，是 VFT 覆盖广度长期上不去的结构性原因之一。
（VFT 的 S_P 分子仍会把这 5 个 MEA 塔名算进去，属分子虚高；按 212 格口径的**有效覆盖仅 30/212 = 0.142**。）

### 区域 multiplier 分层（决定同等投入的回报）

| 区域 | 格子数 | multiplier 区间 | 当前状态 |
|---|---:|---|---|
| DEU | 30 | 1.4 ~ 2.0 | **最高档**，30 格全空白 |
| CHN | 20 | 1.1 ~ 1.9 | **次高档**，20 格全空白 |
| GBR | 30 | 1.0 ~ 1.9 | 高档，仅 D1 少量覆盖，D0 空白 |
| USA | 31 | 1.0 ~ 1.8 | 中高档，MODEL/FUNDAMENTAL 有覆盖 |
| EUR | 27 | 1.0 ~ 1.7 | 中档，MODEL/PV 有覆盖 |
| KOR | 15 | 1.0 ~ 1.7 | 中档，多类有覆盖 |
| HKG | 15 | 1.0 ~ 1.7 | 中档，SHORTINTEREST/PV 有覆盖 |
| GLB | 13 | 1.0 ~ 1.4 | **低档**，仅 OTHER 1 颗 |
| ASI | 16 | 1.0 ~ 1.4 | **低档**，仅零散覆盖 |
| IND | 15 | 1.0 ~ 1.4 | **低档**，MODEL 已 10 颗（重仓低回报区） |

## 2. ★ 一级优先：空白格 × 高 multiplier

零提交 → 任一 REGULAR 提交即刻让 VFT 的 S_P **+1/212**（约 +0.0047），且 multiplier 越高长期收益加成越大。

| # | 格子 | 类别 | multiplier | 建议 |
|---|---|---|---:|---|
| 1 | `DEU/D0/SENTIMENT` | Sentiment | **2.0** | 首次破冰，1 颗即计入覆盖 |
| 2 | `CHN/D1/OTHER` | Other | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 3 | `DEU/D0/INSTITUTIONS` | Institutions | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 4 | `DEU/D0/MODEL` | Model | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 5 | `DEU/D0/NEWS` | News | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 6 | `DEU/D0/OTHER` | Other | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 7 | `DEU/D0/PV` | Price Volume | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 8 | `DEU/D0/INSIDERS` | Insiders | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 9 | `DEU/D0/ANALYST` | Analyst | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 10 | `DEU/D0/RISK` | Risk | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 11 | `DEU/D0/SHORTINTEREST` | Short Interest | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 12 | `DEU/D0/FUNDAMENTAL` | Fundamental | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 13 | `DEU/D1/NEWS` | News | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 14 | `GBR/D0/MODEL` | Model | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 15 | `GBR/D0/NEWS` | News | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 16 | `GBR/D0/OTHER` | Other | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 17 | `GBR/D0/EARNINGS` | Earnings | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 18 | `GBR/D0/INSIDERS` | Insiders | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 19 | `GBR/D0/ANALYST` | Analyst | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 20 | `GBR/D0/SENTIMENT` | Sentiment | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 21 | `GBR/D0/SOCIALMEDIA` | Social Media | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 22 | `GBR/D0/FUNDAMENTAL` | Fundamental | **1.9** | 首次破冰，1 颗即计入覆盖 |
| 23 | `USA/D0/SENTIMENT` | Sentiment | **1.8** | 首次破冰，1 颗即计入覆盖 |
| 24 | `CHN/D0/SENTIMENT` | Sentiment | **1.8** | 首次破冰，1 颗即计入覆盖 |
| 25 | `CHN/D0/FUNDAMENTAL` | Fundamental | **1.8** | 首次破冰，1 颗即计入覆盖 |

## 3. 二级优先：已提交但未点亮（ACTIVE 1–2）

边际成本最低——补到 3 颗 ACTIVE 即可点亮，同时巩固 VFT 覆盖不掉出窗口。

| # | 格子 | 类别 | multiplier | 当前 ACTIVE | 近90天提交 | 365天累计 |
|---|---|---|---:|---:|---:|---:|
| 1 | `GBR/D1/OTHER` | Other | 1.6 | **1** | 1 | 1 |
| 2 | `GBR/D1/PV` | Price Volume | 1.5 | **2** | 2 | 2 |
| 3 | `EUR/D1/OTHER` | Other | 1.5 | **1** | 1 | 1 |
| 4 | `ASI/D1/OTHER` | Other | 1.4 | **1** | 1 | 1 |
| 5 | `GLB/D1/OTHER` | Other | 1.3 | **1** | 1 | 1 |
| 6 | `EUR/D1/NEWS` | News | 1.3 | **1** | 1 | 1 |
| 7 | `ASI/D1/MODEL` | Model | 1.3 | **1** | 1 | 1 |
| 8 | `USA/D1/EARNINGS` | Earnings | 1.2 | **1** | 1 | 1 |
| 9 | `IND/D1/PV` | Price Volume | 1.1 | **2** | 2 | 2 |
| 10 | `USA/D1/PV` | Price Volume | 1.1 | **1** | 1 | 2 |
| 11 | `USA/D1/FUNDAMENTAL` | Fundamental | 1.1 | **1** | 1 | 4 |
| 12 | `USA/D1/INSTITUTIONS` | Institutions | 1.0 | **1** | 1 | 1 |
| 13 | `EUR/D1/RISK` | Risk | 1.0 | **1** | 1 | 1 |
| 14 | `ASI/D1/RISK` | Risk | 1.0 | **1** | 1 | 1 |

## 4. 区域视角

| 区域 | 格子数 | 已点亮 | 空白 | 近90天 ACTIVE | 最高 multiplier |
|---|---:|---:|---:|---:|---:|
| DEU | 30 | 0 | 30 | 0 | 2.0 |
| CHN | 20 | 0 | 20 | 0 | 1.9 |
| GBR | 30 | 1 | 27 | 6 | 1.9 |
| USA | 31 | 2 | 25 | 11 | 1.8 |
| EUR | 27 | 2 | 22 | 14 | 1.7 |
| KOR | 15 | 4 | 11 | 18 | 1.7 |
| HKG | 15 | 2 | 13 | 7 | 1.7 |
| GLB | 13 | 0 | 12 | 1 | 1.4 |
| ASI | 16 | 0 | 13 | 3 | 1.4 |
| IND | 15 | 5 | 9 | 27 | 1.4 |

## 5. 已点亮（不再投入）

按项目纪律，已点亮塔不再分配配额。

| 格子 | 类别 | multiplier | ACTIVE |
|---|---|---:|---:|
| `KOR/D1/MODEL` | Model | 1.7 | 4 |
| `KOR/D1/ANALYST` | Analyst | 1.6 | 5 |
| `KOR/D1/OTHER` | Other | 1.6 | 6 |
| `GBR/D1/MODEL` | Model | 1.6 | 3 |
| `HKG/D1/PV` | Price Volume | 1.5 | 3 |
| `USA/D1/OTHER` | Other | 1.4 | 3 |
| `KOR/D1/PV` | Price Volume | 1.4 | 3 |
| `IND/D1/OTHER` | Other | 1.4 | 3 |
| `IND/D1/ANALYST` | Analyst | 1.4 | 4 |
| `USA/D1/MODEL` | Model | 1.3 | 4 |
| `EUR/D1/MODEL` | Model | 1.3 | 6 |
| `HKG/D1/SHORTINTEREST` | Short Interest | 1.3 | 4 |
| `IND/D1/MODEL` | Model | 1.2 | 10 |
| `IND/D1/FUNDAMENTAL` | Fundamental | 1.2 | 3 |
| `EUR/D1/PV` | Price Volume | 1.1 | 5 |
| `IND/D1/RISK` | Risk | 1.0 | 5 |

## 6. 取用说明

1. **立即止损 MEA**：MEA 在 212 格体系中占 0 格，已投入 33 颗（41%）却既不计点亮
   也无 multiplier 加成。继续投入的边际收益为零。
2. **一级优先决定 VFT 上限**：每破冰一个空白格，S_P 直接 +1/212。
   若破冰 20 个，S_P 由 0.142 升至 0.236，分数可接近翻倍（S_A、S_H 不变时）。
3. **优先破冰 DEU / CHN / GBR**：三区 multiplier 达 1.4–2.0，是当前主力区域
   （IND 1.0–1.4、ASI 1.0–1.4、GLB 1.0–1.4）的 **1.3–1.7 倍**回报，且几乎全空白。
   IND/D1/MODEL 已投 10 颗却处最低 multiplier 档，属重仓低回报区，应降权。
4. **二级优先决定点亮数**：ACTIVE 1–2 的格子补到 3 即点亮，性价比最高
   （GBR/D1/PV、IND/D1/PV 均已有 2 颗，差 1 颗点亮）。
5. **命中率佐证**：近 90 天 77 个 REGULAR 提交**全部 ACTIVE**（77/77），
   说明选品与闸门纪律有效 —— 瓶颈不在质量，而在**投向分布**。
