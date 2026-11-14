# IND 字段画像存档索引 · 2026-11-14

> 人工审计 → `reports/<主题>_<YYYYMMDD>.md`。机器索引 = `tracking/IND/reference/ind_field_profile_index_20261114.json`。

## 路径与命名规则（AGENTS.md §8.13）

| 产物 | 路径 | 命名 |
|---|---|---|
| 逐集 typed catalog（机器事实源） | `tracking/IND/reference/` | `ind_<dataset>_fields.json`（沿用 `ind_analyst45_fields.json` 既有名） |
| 逐集 8 列画像（人读） | `reports/dataset_experience/` | `ind_<dataset>_field_profile_<YYYYMMDD>.md` |
| 逐 category 总表 | `reports/dataset_experience/` | `ind_field_profiles_survey_<YYYYMMDD>.md` |
| 索引 | `tracking/IND/reference/` + `reports/` | `ind_field_profile_index_<YYYYMMDD>.json/.md` |
| 长期 SOP（不带日期） | `docs/experience/` | `*.md`，每条带证据 |

规则：路径纯 ASCII；文件纯 snake_case；人工报告日期 `YYYYMMDD` **作后缀**；`IND` 大写仅作区域码豁免；`reports/dataset_experience/` 是存量 snake_case 目录（S16 legacy 登记，不回改）；**禁止占用 `ind_<ds>_campain.md`**（生成器 + `step9_audit.py` 消费的既定名，AGENTS.md:1177）。

## 索引表

| dataset | cat | 字段 | MCP count | complete | 塔(当季) | 主信号字段 | verdict | catalog | 画像 |
|---|---|---:|---:|---|---|---|---|---|---|
| `institutions6` | INSTITUTIONS | 11 | 11 | True | 1(未亮) | 11 | PRIMARY | `tracking/IND/reference/ind_institutions6_fields.json` | `reports/dataset_experience/ind_institutions6_field_profile_20261114.md` |
| `sentiment21` | SENTIMENT | 105 | 105 | True | 1(未亮) | 4 | VALIDATE_FIRST | `tracking/IND/reference/ind_sentiment21_fields.json` | `reports/dataset_experience/ind_sentiment21_field_profile_20261114.md` |
| `earnings11` | EARNINGS | 35 | 35 | True | 2(未亮) | 0 | WEAK_MECHANISM | `tracking/IND/reference/ind_earnings11_fields.json` | `reports/dataset_experience/ind_earnings11_field_profile_20261114.md` |
| `model77` | MODEL | 23 | 23 | True | 3(已亮) | 0 | WEAK_MECHANISM | `tracking/IND/reference/ind_model77_fields.json` | `reports/dataset_experience/ind_model77_field_profile_20261114.md` |
| `other323` | OTHER | 11 | 11 | True | 4(已亮) | 0 | WEAK_MECHANISM | `tracking/IND/reference/ind_other323_fields.json` | `reports/dataset_experience/ind_other323_field_profile_20261114.md` |

## 对账

- 5 集 MCP `count == platform_count == 画像字段数`，全部 `complete=true`；合计 **185 字段**，无抽样。
- `model77` 例外：MCP 实读 23 字段 / cov 0.4001，DB `field_profile_full` 记 348 字段（旧版本），**以 MCP 实读为准**，DB 旧画像在本轮作废并写入风险说明。
- `ten_year_ok` 全部 `pending_baseline_probe`：阶段 D 基准探针用 `get_alpha_yearly_stats` 验 2014–2023 逐年 PnL，未过即换集。
