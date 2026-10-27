# USA 区域独有规则（rules/）

> **定位**：只放**USA 特有**的规则与纪律；九步通用正文在 `../wq-brain-ra-pipeline/SKILL.md`，不在此重复。
> **as_of**：2026-10-18 ｜ **真身纪律**：本目录是手写区，SKILL.md 的生成块重渲不会覆盖它；反之亦然。
> **与 SKILL.md 的分工**：SKILL.md 只留入口与摘要（体量目标 ≤250 行），细则一律放这里或 `../references/`。

| 文件 | 内容 | 性质 |
|---|---|---|
| [six-step-usa-override.md](six-step-usa-override.md) | 六步纵深骨架的 USA 覆盖项 + 改控制纪律 | 规则 |
| [gate-and-submit-discipline.md](gate-and-submit-discipline.md) | 本区闸门纪律（prod/SUB 两难墙、RAM·CROWDING 破墙、提交三条铁律、选集铁律） | 规则 |
| [signal-mining-workflow.md](signal-mining-workflow.md) | EUR 文章《signal_mining_workflow》的 **USA 区域化版**：EV 选集 → 维度地图 → 8 统计族 → 三维三闸 → 归因 → 四杠杆 → 全闸 → 判死存档 | 规则 |
| [../references/_unlit-tower-campaign-20261014.md](../references/_unlit-tower-campaign-20261014.md) | 未点亮塔横跨 6 数据集实证（16 波 / 64 条） | 实证 |
| [../references/_usa-mining-playbook-20261018.md](../references/_usa-mining-playbook-20261018.md) | 字段画像 × 适用模板 × 回测指标三段式手册 | 实证 |
| [../references/_analyst-campaign-20261017.md](../references/_analyst-campaign-20261017.md) | Analyst 攻坚战报（15 波 / 60 条，交付 2 颗 ACTIVE） | 实证 |

## 本区四条最硬的规则（背下来即可开工）

1. **最深最饱和的市场**：经典 `value` / `quality` / `book` 及其线性变体必死（book/value 单族 145 颗同族 ACTIVE）；
   选集白名单只能用「未点亮塔 × 低 alphaCount」筛——`score_datasets` 的 signal-score top20 全是 model 族，
   **按 score 排序等于往已点亮塔堆料**。
2. **分析师族瓶颈在 prod 不在 IS**：IS 八闸全过的变体十有八九撞 prod 0.70+；
   破墙第一杠杆是**换 neutralization 到 `REVERSION_AND_MOMENTUM`**，不是磨算子（详见 [gate-and-submit-discipline.md](gate-and-submit-discipline.md)）。
3. **回测前必查生效画像**：`$WQ_PY -m wqb.profiles explain --region USA --dataset <dataset>`；
   直接用 MCP 发仿真时按 explain 输出逐项传设置，**不要依赖工具缺省**（各入口缺省不同，换档等于换信号）。
4. **`exit 0` ≠ 过闸，判死要三闸 + 8 统计族**：`full_coverage_gate.py` 在 USA 有两处 **fail-open**——维度闸缺
   `field_profile_full` 行时 `SKIP`、模板族闸因 `expressions.family` 全 NULL 恒报 1/3 WARN、边界闸因缺
   `boundary_ops_usa.json`（`tracking/USA/reference/` 下，当前不存在）恒 PASS。退出码 0 只说明「没拦住」，不说明「检查过」。
   数据集级 `dead_end` 需「8 统计族全试 + 全波最强 |S| 低于判死线」；D15 的 fast_kill（8 探针无 |S|≥0.5）
   只到**字段 / 探针级**。详见 [signal-mining-workflow.md](signal-mining-workflow.md) 四、八两节。
