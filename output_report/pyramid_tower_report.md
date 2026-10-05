# 点塔潜力报告 (SUBMIT_LAYER_VERIFIED + READY)

> 数据源: submit_ready 表 (gate=SUBMIT_LAYER_VERIFIED, status=READY) + 平台实时金字塔 API
> 候选总数: 25 颗 | 生成时间: 实时

## 点塔规则速记
- **金字塔单元** = (数据类别 category, 区域 region, 延迟 delay)，如 `USA/D1/MODEL`。
- **multiplier** = 平台当前鼓励系数（越高越鼓励，提交后过 ACTIVE 拿到的加成越大）。
- **my_count** = 我当前在该单元已落地的 alpha 数（来自 pyramid-alphas）。`UNLIT=0` 表示该塔我尚未点亮，提交此 alpha 即点亮 → **点塔价值最高**；`PARTIAL=1~2` 仍在累积点亮；`LIT>=3` 已点亮，提交边际价值低。
- **点塔优先级** = multiplier × (UNLIT 3 / PARTIAL 1.2 / LIT 0.4)，再辅以 sharpe。

## 优先级排序（高价值点塔候选在前）

| 排名 | alpha_id | 名称 | 区域 | S | F | 2Y | 金字塔单元 | mult | 我方计数 | 塔状态 | 点塔价值 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WjAV89jG | — | GBR | 1.62 | 1.1 | 1.7 | GBR/D1/OTHER | 1.9 | 0 | UNLIT | 5.7 |
| 2 | A1G7o1EE | — | GBR | 1.61 | 1.13 | 1.64 | GBR/D1/PV | 1.8 | 0 | UNLIT | 5.4 |
| 3 | MPQVZRnk | ppa_v9_ret_w0.35_z42_d4 | USA | 2.23 | 1.44 | 2.12 | USA/D1/PV | 1.1 | 0 | UNLIT | 3.3 |
| 4 | vRNk56mz | — | GBR | 1.8 | 1.2 | 1.82 | GBR/D1/MODEL | 1.9 | 2 | PARTIAL | 2.28 |
| 5 | GrlqxwKx | — | GBR | 1.8 | 1.28 | 1.62 | GBR/D1/MODEL | 1.8 | 2 | PARTIAL | 2.16 |
| 6 | qMNMbeGj | 0.62 | ASI | 1.72 | 1.16 | 2.25 | ASI/D1/OTHER | 1.5 | 1 | PARTIAL | 1.8 |
| 7 | vRvg7NzA | earn_sent_overall_grank_stat | USA | 2.66 | 1.82 | 3.83 | USA/D1/EARNINGS | 1.3 | 2 | PARTIAL | 1.56 |
| 8 | rKjY5vGj | asi_cnn3_divyild_value | ASI | 2.01 | 1.36 | 2.88 | ASI/D1/MODEL | 1.3 | 1 | PARTIAL | 1.56 |
| 9 | 883WZJ1W | — | USA | 1.92 | 1.05 | 3.64 | USA/D1/EARNINGS | 1.2 | 2 | PARTIAL | 1.44 |
| 10 | O0xagXjd | fnd93_expense_range_stat | USA | 1.67 | 1.0 | 2.39 | USA/D1/FUNDAMENTAL | 1.1 | 1 | PARTIAL | 1.32 |
| 11 | wpjJK60l | kor_w113_grp_sec | KOR | 1.91 | 1.07 | 2.32 | KOR/D1/MODEL | 1.7 | 4 | LIT | 0.68 |
| 12 | WjAxxZVk | 0.6999 | KOR | 1.72 | 1.54 | 1.92 | KOR/D1/MODEL | 1.7 | 4 | LIT | 0.68 |
| 13 | e73Rw8qg | KOR_eps50_pretaxdown_blend_162 | KOR | 1.62 | 1.24 | 1.63 | KOR/D1/ANALYST | 1.7 | 5 | LIT | 0.68 |
| 14 | j2rrpVzO | ppa_hiring_trends_ILLIQUID | USA | 2.19 | 1.78 | 2.4 | USA/D1/OTHER | 1.5 | 3 | LIT | 0.6 |
| 15 | YPgAa3WR | ppa_usa_top3000_eur_value_rev_v39b | USA | 2.08 | 1.67 | 1.65 | USA/D1/OTHER | 1.5 | 3 | LIT | 0.6 |
| 16 | xAdL5vmN | 0.6697 | USA | 4.51 | 4.13 | 3.65 | USA/D1/MODEL | 1.4 | 4 | LIT | 0.56 |
| 17 | 6XpMb0aG | — | USA | 4.32 | 4.32 | 4.19 | USA/D1/OTHER | 1.4 | 3 | LIT | 0.56 |
| 18 | 1Ywx8ZpR | — | USA | 2.1 | 1.2 | 1.86 | USA/D1/MODEL | 1.3 | 4 | LIT | 0.52 |
| 19 | GrlGJnPJ | 0.685 | USA | 2.02 | 1.01 | 1.62 | USA/D1/MODEL | 1.3 | 4 | LIT | 0.52 |
| 20 | j2AXkdKO | — | IND | 3.61 | 2.38 | None | —(无金字塔单元) | — | — | N/A | 0 |
| 21 | 3qX3Mp6O | — | IND | 3.18 | 2.02 | None | —(无金字塔单元) | — | — | N/A | 0 |
| 22 | xA392Xpb | — | IND | 3.18 | 2.0 | None | —(无金字塔单元) | — | — | N/A | 0 |
| 23 | 3qX6wLJQ | — | IND | 3.07 | 2.34 | None | —(无金字塔单元) | — | — | N/A | 0 |
| 24 | KPGvRMg1 | 0.6944 | USA | 2.89 | 2.39 | 3.25 | —(无金字塔单元) | — | — | N/A | 0 |
| 25 | 3qX6wLkP | — | IND | 2.84 | 1.74 | None | —(无金字塔单元) | — | — | N/A | 0 |

## UNLIT 塔优先清单（点亮即拿满 multiplier 的候选）

- **WjAV89jG** (—) — GBR GBR/D1/OTHER mult=1.9 S=1.62 F=1.1
- **A1G7o1EE** (—) — GBR GBR/D1/PV mult=1.8 S=1.61 F=1.13
- **MPQVZRnk** (ppa_v9_ret_w0.35_z42_d4) — USA USA/D1/PV mult=1.1 S=2.23 F=1.44
