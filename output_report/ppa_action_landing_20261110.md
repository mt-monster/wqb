# 「提高 CPPAP 可执行清单」落地报告 · 2026-11-10

> 触发：用户引用上一轮「3 提高 CPPAP 的可执行清单」并要求「帮我落地」。
> 重要前提：该清单写于 **02:4x 的 themes 实证纠错之前**。本轮把其中**仍成立**的判据全部编码成可执行工具，
> 把「摘 18 颗」做成受控的一键能力而**不擅自执行**，并逐条说明原因。

## 0 一句话结论

清单的**数字全对**（18 / 9 / 14 逐项复核吻合），但**前提错了**：全账户 301 颗 ACTIVE 里
只有 **1 颗**命中当期 `GLB/D1 Power Pool Nov'26` 主题，而这颗正是名单里要摘的 `JjeMlmXA`。
其余 17 颗摘了对当期 CPPAP **不起作用**（平台 `themes` 由类别/区域判定，PATCH tags 改不了）。
⇒ 落地为「判据工具 + 受控执行器 + 规范」，默认输出 **0 条可执行**；并保留一条精确命令供你决定。

## 1 逐条落地状态

| # | 清单原文 | 落地状态 | 产物 |
|---:|---|---|---|
| 1 | **该优先摘 18 颗**（margin<10bp 且 TO>0.15） | ✅ 判据已编码；⚠ **未执行**（默认 0 条），做成受控执行器 | `tools/gates/ppa_tag_apply.py` |
| 2 | **别摘 9 颗**（margin<10bp 但 TO≤0.15） | ✅ 编码为 `EDGE` 档，执行器永不选入 | `ppa_readiness.py::quality_band` |
| 3 | **必须留 14 颗锚**（margin≥15bp 且 TO≤0.15） | ✅ 编码为 `ANCHOR` 档，执行器永不选入 | 同上 |
| 4 | **治本：margin≥10bp（目标 15bp）加进挖掘闸门**；S/F>1、曲线不低头/尾年不差、每月 2 区+月底点塔 | ⚠ **落地为软标记 + 规范，未设硬闸**（与 `MEMORY.md` §8「margin 不是独立信息、两提案已否决」冲突，交你裁决） | `candidate_soft_flag()`、`docs/alpha_properties_spec.md` §3.6 |
| 5 | **边界**：tag 管理只保护 CPPAP；BC−AC 固定 .159–.177；本地 PnL 不可信 | ✅ 写入工具 `boundary` 字段与规范 | `ppa_readiness.py` |

## 2 数字复核（用最终平台态 + 台账校正后的 301 颗）

| 口径 | 清单值 | 复核值 | 一致 |
|---|---:|---:|---|
| 带标签 `WEAK`（该摘） | 18 | **18** | ✅ |
| 其中命中当期主题 | — | **1**（`JjeMlmXA`） | ★ 关键 |
| 带标签 `EDGE`（别摘） | 9 | **9** | ✅ |
| 带标签 `ANCHOR`（必须留） | 14 | **14** | ✅ |
| 全池带标签 | 66 | **66** | ✅ |
| 当期主题命中 / 评奖线 | — | **1 / 5** | ❌ 未达标 |

清单点名的几颗都在复核结果里：`JjeMlmXA` 2.66bp/.319、`gJboYLRl` 3.58bp/.416、
`A10wOvAe` F0.47、`xAY86Mkl` TO .550、`LL5VwgO1` 4.62bp/.377，
以及今日刚交的 `P0obGoQJ` 4.12bp/.291、`akK9ooZv` 4.59bp/.411。

## 3 新增工具

### `tools/gates/ppa_readiness.py`（只读判据）

```bash
python tools/gates/ppa_readiness.py                 # 离线快照优先，摘要 + 落盘
python tools/gates/ppa_readiness.py --id JjeMlmXA  # 单颗判定
python tools/gates/ppa_readiness.py --refresh      # 在线刷新（失败自动回退快照）
python tools/gates/ppa_readiness.py --json         # 机器可读
```

自动识别**年月最新**的 Power Pool 主题为当期主题（跨期可用），逐颗输出 `themes / 标签 / 质量档 / 动作`。
动作档：`NO_LEVERAGE`（无当期主题，改标签无效）｜`HOLD_LOW_COUNT`（当期池<5 条，摘货清零参赛资格）｜
`KEEP_TAG`｜`CONSIDER_ADD`｜`CONSIDER_REMOVE`｜`WATCH`。
内置 **台账校正**：`ppa_theme_scan_20261110.json` 采于两条实验生效期间，工具会按
`results/ppa_tag_governance_log.jsonl` 的最后状态覆盖 tags（本次校正 `JjeMlmXA` / `O07AMoKR` 两颗）。

当前实跑：

```
当期主题 GLB/D1 Power Pool Nov`26｜命中 1 颗｜评奖线 5 条｜未达标
质量档 ANCHOR 115 / OK 40 / WATCH 42 / WEAK 82 / EDGE 22
动作档 NO_LEVERAGE 300 / HOLD_LOW_COUNT 1
```

### `tools/gates/ppa_tag_apply.py`（受控执行器，默认 dry-run）

```bash
python tools/gates/ppa_tag_apply.py                       # 干跑 → 0 条可执行
python tools/gates/ppa_tag_apply.py --add                # 干跑补标签 → 0 条
python tools/gates/ppa_tag_apply.py --confirm --limit 1  # 真正执行 1 条
```

六道安全阀：① `NO_LEVERAGE` 不处理；② `HOLD_LOW_COUNT` 不处理；
③ `ANCHOR`/`OK`/`EDGE` 永不摘；④ 默认 `--limit 1`（论坛：一次一条，等约 6h 读 BC/AC）；
⑤ PATCH 只发 `tags` + `regular.description` 原样回显，逐条回读验证 desc/name/color，失败自动回滚；
⑥ 全部动作写 append-only 台账。

## 4 如果你仍要照原清单执行 18 颗

```bash
python tools/gates/ppa_tag_apply.py \
  --allow-no-leverage --force-low-count --limit 18 --confirm
```

精确选出 **18 颗**（已验证，不多不少），其中包含 `JjeMlmXA`。执行前请知悉：

- 17 颗 `NO_LEVERAGE`：无当期主题，摘标签**对当期 CPPAP 零作用**（可逆，但也零收益）。
- 1 颗 `JjeMlmXA`：**当期唯一参赛货**，摘掉后当期池从 1 → 0；论坛「交满 5 条才够评奖」「条数越多 BC 越高」。
- 会把今日刚提交 `P0obGoQJ` / `akK9ooZv` 的 PP 标签摘掉；若它们后续被判定命中某期主题，就进不去了。
- 当前 `/consultant/boards/power-pool?user=MT38799` `count=0`，**没有 BC/AC 读数**，摘完无法验证涨跌。
- 全部可逆（加回标签下一次刷新生效），台账会留四步式记录。

我**没有执行**这条命令。你回一句「照旧摘 18 颗」我就跑；否则保持现状。

## 5 正道（真正提高 CPPAP）

标签治理对本账户几乎无杠杆。要提高 CPPAP 需要**新提交命中当期主题的高质量 alpha**：

- 当期主题 `GLB/D1 Power Pool Nov'26` ⇒ GLB/D1、**单一类别**（论坛：带 sector 分组会多算一个 PV 类，就不是单类别）；
- margin ≥10bp（目标 15bp）、TO ≤0.15、S/F>1、曲线不低头 / 尾年不差；
- 每月专注 2 个区域 + 月底点满塔（MZ45384：CPPAP 2.12 → 2.67）。

⚠ **margin 硬闸需你裁决**：`MEMORY.md` §8 有 124 颗 USA 真实 OS 实证「IS 指标全不预测 OS」，
margin 只是低换手代理（ρ(margin,−TO)=+0.922），两提案已否决。CPPAP 是**扣成本后组合 IR**，
口径不同，但把 margin 写进提交硬闸会大面积误伤 READY 队列（margin<8bp 占 62%）。
本轮只做**软标记**，未改任何挖掘闸 / `config.py`。

## 6 验证与回归

- `ppa_readiness.py` / `ppa_tag_apply.py` 三种模式干跑均通过；强制模式精确 18 条。
- 新增 `tests/unit/05_submit_quota/test_ppa_readiness_20261110.py`（8 项守护）。
- 修正 `test_submit_p0_20261027.py` 两处**报告字段**旧断言（`is_ppa` / `ppa_tag_only`）：
  它们把「带 PP 池标签 = PPA 通道」写死了，与 11-10 通道判定修正冲突；
  核心守护（`blocked` / `failed_ra` / `failed_ppa`）**一字未改**。
- **全量回归 632 passed / 11 skipped**（`05_submit_quota` + `02_workflow`）。
- 平台侧本轮**零改动**：未 PATCH 任何标签、未提交 alpha、未改提交开关。
- 平台直连当前仍限流（连续非 JSON 响应），工具默认走离线快照 + 台账校正，不受影响；
  08:45 的一次性只读复核自动化会再确认榜读数与标签最终态。

---

## 决策留痕（2026-11-10 03:10）

用户引用「如果你仍要照原清单摘 18 颗」标题后，先做了执行前**只读预演**（平台此时已恢复，ACTIVE 301 颗可读），确认：

- 18 颗精确清单无偏差；其中 17 颗 `NO_LEVERAGE`、1 颗 `HOLD_LOW_COUNT`（`JjeMlmXA`）。
- 2 颗是今日刚提交（`akK9ooZv` / `P0obGoQJ`）；6 颗摘完 `tags` 会变空。
- 榜 `count=0`，无 BC/AC 基线；一次 18 条还会破「一次只动一条」的对照纪律。

**用户决定：暂不执行，等 08:45 复核（推荐项）。**
⇒ 平台零改动，18 颗标签一颗未动；治理台账 `seq=5 action=decision_hold` 已留痕。
08:45 的一次性复核已补充约束：只读输出结论，**不得自行发起任何标签 PATCH**。
