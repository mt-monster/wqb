# news54 · EUR / TOPCS1600 / D1 字段画像（快跳过）

> 类型 VECTOR · 40 字段 · cov 0.87–0.98 · category = **news**（×1.3）
> 采集：2026-11-06

## 快判结论：结构性不可用，跳过

字段目录拆成三类：
1. **时间戳**（`*_time` / `*_time_utc`，约 23 支）——UTC/本地宣布时间、录入时间、更新时间，无横截面信号语义
2. **自由文本**（`*_headline` / `*_situation`，6 支）——FASTEXPR 无法对字符串做数值算子
3. **元数据旗标/财年**（`cancelledflag` / `postponedflag` / `fiscalquarter` / `fiscalyear` / `mws54_factor`，约 11 支）——稀疏事件旗标或日历字段，单独无法构成 ATOM 主信号

论坛帖 WL13229 提到的 `future_event_headline_word_count` **本区字段清单不存在**（可能是其他 region/universe 或已下线）。

**裁决**：本集对 FASTEXPR ATOM 无可用主信号字段，按「结构性不可用」跳过，不计入覆盖闸缺口，不投入探针。
