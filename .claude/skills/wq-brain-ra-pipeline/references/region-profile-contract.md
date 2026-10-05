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
| TWN | 有 profile，**没有** `tracking/TWN/` 目录 | 开新区前先补 `tracking/TWN/config/`（`settings.json` / `thresholds.json`）；当前 `probe-only` |
| MEA | `frozen` | 步 1 即拒；后门见 [`scenarios.md`](scenarios.md) 情景 RA-08 |
| AMR | `config.REGIONS` 有，profile 已于 2026-09-28 补建（`active`），`tracking/AMR/config/` 存在；平台档位实测见 profile | 已转为持续自我挖掘区（处女地 → active），走通用处女地模板（参照 ASI） |
| ALL | 平台 `get_platform_setting_options` 有（D1，LARGE / MEDIUM / SMALL），**不在** `config.REGIONS`；REGULAR 仿真返回 400「Region ALL is not available for simulation type REGULAR」（2026-09-19 当日实测，未复核） | 不是挖掘区，步 1 拒绝 |

区域清单与 profile / 战役目录的对齐表在 [INDEX §区域清单](../../INDEX.md)（权威是 `config.REGIONS`）。

## 5. datasets 精确层与漂移钩子（2026-10-01 落地）

**背景**：旧版 `datasets.green/red` 是自由文本（`analyst 系（评级/预期）`），无法机检——KOR 实证：profile 写着「烧不起配额、8 探针即判死」却 37 天未核对，跨区死族混进白名单。2026-10-01 全部 14 个 profile 一次性迁移为结构化形态（`tools/migrate_profile_datasets.py`，一次性工具，不留兼容层）。

**新形态**（green / red 各为条目列表；yellow 保持简单标量列表）：

```yaml
datasets:
  red:
    - datasets: [model109, model170]     # 数据集级（精确层）：id 必须落在 datasets.name（本区）
      reason: "已判死（ledger *_dead）"
    - scope: family                       # 族级：本来就不绑定单个数据集（如 glb_emotion）
      families: [chart_patterns, ai_ml]
      reason: "3 连死"
  green:
    - datasets: [other466]
      note: "registry win 层实证绑定"
```

**漂移钩子（profile 接回流水线的机制）**：`upsert_registry_empirical` 在 `layer ∈ {win, dead_end}` 写入成功后，自动跑一次 `wqb.profile_drift.check_profile_drift`，完整报告幂等写入 ledger 键 `profile_drift`，摘要（`needs_refresh` / `summary` / `hint`）随回写返回值带出。**fail-open**：检查失败只降级为提示，绝不阻断回写本体。

判定全部是集合运算（实现与判据表的唯一来源 = `src/wqb/profile_drift.py` 模块 docstring）：

- **high（触发 needs_refresh）**：`green_but_dead`（green 收录但 ledger `*_dead` 已整集判死）/ `red_but_won`（red 收录但 win 层有胜绩）
- **medium**：`green_but_family_dead`（green 收录但 dead_end 层有族级判死——族死 ≠ 整集死，人工核实）/ `unknown_dataset_ref`（引用不在本区 `datasets` 表）/ `dead_not_listed`（整集判死但 red 未收录）/ `win_not_listed`（胜绩未认领）
- **low**：`stale_last_verified`（last_verified 早于最近一次实证回写——提示复核，不构成 needs_refresh）

**两档死亡证据严格分开**：ledger `*_dead` = 整集判死（唯一无歧义）；registry `dead_end` 的 `payload.dataset` = 该集语境下某族死了。族级死**不**驱动 `dead_not_listed`（族死不妨碍 S0 选该集其它族）。

**纪律**：
- 钩子只报告，**永不自动改 profile**——修改永远人工复核后做，并 bump `last_verified`（§3 的禁批量规则不变）。
- 新增 win/dead_end 条目**必须**带 `payload.dataset`（canonical id，本区 `datasets.name` 内）才能进精确层；不带的记 `unbound_entries` 计数并提示——不补绑的条目永远停在 advisory 层（这是逼着补齐的杠杆）。
- 全区体检：`python tools/profile_drift_check.py --all`（`--write-ledger` 落台账）；退出码 1 = 存在 high 级冲突。
- 回归：`tests/unit/01_store_db/test_profile_drift.py`。

