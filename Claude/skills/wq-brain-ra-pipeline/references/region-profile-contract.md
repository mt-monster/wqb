# 区域 Profile 契约（`references/regions/<REGION>.md`）

> 2026-09-29（skills 审查 RR-01 ~ RR-10）。旧版说 profile 的 front-matter「声明静态配置 / 闸门覆盖 / 循环策略」并「注入」各步骤；实测**只有一小部分键被代码读**，其余是给 agent 读的文档。
> 本文件放在 `regions/` 目录**外**（该目录里的每个 `.md` 都被测试当作一个区域 profile）。

## 1. front-matter：哪些键被代码读，哪些是文档

| 键 | 谁读 | 说明 |
|---|---|---|
| `region` | 测试 / 工具 | 必须 = 文件名（`test_profile_frontmatter_contract`） |
| `entry_verdict` | **代码**：`region_rotation.py` / `region_status.py` / `wqb_db_mcp.py`（正则 `^entry_verdict:`） | `active` / `probe-only` / `frozen`；默认含义见 [`step1-inventory.md`](step1-inventory.md) §1.1，profile 只写与默认不同的部分 |
| `priors`（front-matter 里的引号列表项与 `signal_families_exclude: [..]`） | **代码**：`assemble_priors._profile_fallback`，**仅在 DB KB 为空时**兜底 | ⚠ 该解析器把 front-matter 里**所有**以 `- "` 开头的引号列表项都当成 win 配方——别在 front-matter 里加无关的引号列表项 |
| 正文里的 `## priors` 段 | **代码**：GEM 的 `skeletons.load_region_priors`（≤ 2000 字符） | 没有该段时退化为取前 ≤ 8 条短 bullet |
| `one_liner` / `static` / `datasets` / `gate_overrides` / `loop_policy` / `empirical_anchor` | **文档**（agent 读了照办；代码不消费） | 遵守，但别指望闸会替你执行 |

`gate_overrides` 只写**与全局默认不同**的键（2026-09-29 起删除了等同默认的 `longcount_min: 80` 与 `prod_corr_early_warn: 0.7`——它们看起来像配置、实际什么都没覆盖）。
`cw_gate`（`WARN` / `FAIL`）是**文档级约定**：本地预判 CW（`CONCENTRATED_WEIGHT`）不过时，agent 按「只作提示」（`WARN`）还是「按失败处理」（`FAIL`，小宇宙放大 CW 问题、烧不起配额）；**代码不读它，平台对 CW 永远是 FAIL 检查**。
**不得**在 profile 里另设 prod 预警线改写决策表 D0-P（USA 的「0.6 即停扩换腿」已并入 D0-P 的 0.60–0.70 行）。

## 2. 正文固定模板（RR-05）

profile 正文按下面的顺序写，agent 想查「这个区能挖什么」时从上往下读：

1. **定位与实证依据**（一段话 + 最关键的一两个数字）
2. **硬规则**（含用户定案，注明日期）——最先读、最不能错过的部分
3. **流程变体（相对九步骨架）**——「步 N 注入」式小节，按步骤查区域差异
4. **配方 / 组腿**（已验证的结构，注明是否属于允许形态，见步 7 §7.7）
5. **避坑清单**
6. **证据附录**（按日期折叠：实验、表格、判死记录）

旧的 profile 按**写入时间序**追加（硬规则埋在证据之后）；IND 已按此模板重排，其余区域在下次被编辑时随手整理。

## 3. `last_verified` 的含义（RR-04）

`empirical_anchor.last_verified` = **最近一次内容核对**（通读正文与 front-matter 是否一致）的日期。**批量机械刷新不得改这个戳**——旧版 13 个 profile 里一半是同一天的批量戳（2026-08-25），掩盖了正文已被 09-19 用户定案改写而 front-matter 没跟上（IND 的 `green: [mdl177…]`）。

## 4. 区域缺口（RR-09）

| 区域 | 缺口 | 步 1 的行为 |
|---|---|---|
| HKG | （已补）`universe` 于 2026-09-29 从 `config.REGIONS` 回填为 `[TOP800, TOP500]` | 步 1 仍 `get_platform_setting_options` 复核；不再是缺口 |
| TWN | 有 profile，**没有** `tracking/TWN/` 目录 | 开新区前先补 `tracking/TWN/config/`（`settings.json` / `thresholds.json`）；当前 `probe-only` | <!-- lint:counterexample: 同上：开新区前置检查项，引用的是「待创建」的目录 -->
| MEA | `frozen` | 步 1 即拒；后门见 [`scenarios.md`](scenarios.md) 情景 RA-08 |
| AMR | `config.REGIONS` 有，profile 已于 2026-09-28 补建（`active`），`tracking/AMR/config/` 存在；平台档位实测见 profile | 已转为持续自我挖掘区（处女地 → active），走通用处女地模板（参照 ASI） |
| ALL | 平台 `get_platform_setting_options` 有（D1，LARGE / MEDIUM / SMALL），**不在** `config.REGIONS`；REGULAR 仿真返回 400「Region ALL is not available for simulation type REGULAR」（2026-09-19 当日实测，未复核） | 不是挖掘区，步 1 拒绝 |

区域清单与 profile / 战役目录的对齐表在 [INDEX §区域清单](../../INDEX.md)（权威是 `config.REGIONS`）。
