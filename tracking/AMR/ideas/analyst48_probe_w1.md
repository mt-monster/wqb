# analyst48 探针波 W1 —— 分红/股息 analyst 族（8 机制快判死）

**Dataset**: analyst48
**Region**: AMR
**Delay**: 1

> 战役纪律：AMR 新集 8 探针快判死（无 |S|>=0.5 即 dead_end）。每概念 1-2 字段、2-4 算子、
> 标准窗口（5/22/66/252）、禁 add(A,B) 加权混腿。黑名单 7 字段（日期/分类码）禁用。
> analyst48 = 主攻集（clean、低竞争 ac=87/uc=41、65 信号字段 100% 冷门）。

**Concept**: 股息率估值水平——12 个月股息率截面排名，高股息率 = 价值折价，long-run 均值回归
- **Implementation Example**: `group_rank(ts_mean({bp12m_yld}, 22), subindustry)`
- **Rationale**: 字段 anl48_bp12m_yld（12M 股息率）；Expected Exposure=价值/股息率；形状族 group_rank；时间尺度 22；分组轴 subindustry；算子数 3。

**Concept**: 分红健康度水平——当前分红健康度评分回填后截面排名，健康度高 = 分红可持续性强
- **Implementation Example**: `rank(ts_backfill({bdvd_curr_dvd_health}, 120))`
- **Rationale**: 字段 anl48_bdvd_curr_dvd_health；Expected Exposure=分红质量；形状族 rank+ts_backfill（低覆盖回填骨架）；算子数 2。

**Concept**: 分红增长动量——分红增长指标 66 日变化的 252 日时序排名，上调 = 基本面改善延续
- **Implementation Example**: `ts_rank(ts_delta({bedhgpd}, 66), 252)`
- **Rationale**: 字段 anl48_bedhgpd（分红增长系）；Expected Exposure=分红修正/增长；形状族 ts_rank；时间尺度 66/252；算子数 3。

**Concept**: 除息事件密度——除息事件 22 日均值的组内排名，除息密集 = 分红兑现节奏
- **Implementation Example**: `group_rank(ts_mean({dvd_xe}, 22), subindustry)`
- **Rationale**: 字段 anl48_dvd_xe（ex-dividend 事件）；Expected Exposure=分红事件节奏；形状族 group_rank；时间尺度 22；分组轴 subindustry；算子数 3。

**Concept**: 每股分红修正——最近每股分红 22 日变化的 252 日时序标准化，上调 = 预期改善
- **Implementation Example**: `ts_zscore(ts_delta({equity_dvd_sh_last}, 22), 252)`
- **Rationale**: 字段 anl48_equity_dvd_sh_last（每股分红最近值）；Expected Exposure=分红预期修正；形状族 ts_zscore；时间尺度 22/252；算子数 3。

**Concept**: 分红方向温度计——分红方向温度计读数截面排名，方向偏增 = 管理层分红意愿
- **Implementation Example**: `rank({bdvd_curr_dir_therm})`
- **Rationale**: 字段 anl48_bdvd_curr_dir_therm（分红方向温度计）；Expected Exposure=分红方向/管理层意愿；形状族 rank；算子数 1（复杂度预算下限代表）。

**Concept**: 股息率偏离——当前股息率相对 252 日均值的价差，向上偏离 = 相对折价加深（单一价差信号）
- **Implementation Example**: `subtract(rank({bp12m_yld}), rank(ts_mean({bp12m_yld}, 252)))`
- **Rationale**: 字段 anl48_bp12m_yld（复用，价差结构）；Expected Exposure=价值偏离；形状族 subtract 价差几何；时间尺度 252；算子数 3。

**Concept**: 3 年增长质量——3 年每股增长指标回填后组内排名，增长稳健 = 质量溢价
- **Implementation Example**: `group_rank(ts_backfill({edg3yr_g}, 120), subindustry)`
- **Rationale**: 字段 anl48_edg3yr_g（3 年增长）；Expected Exposure=增长质量；形状族 group_rank+ts_backfill；分组轴 subindustry；算子数 3。

## 语义多样性自查

- Expected Exposure：价值/分红质量/分红修正/事件节奏/预期修正/管理层意愿/价值偏离/增长质量 ≥3 ✓
- 字段族：valuation（C1/C7）、dividend health（C2）、dividend growth（C3）、event（C4）、per_share（C5）、direction（C6）、growth（C8）≥3 ✓
- 分组轴：subindustry（C1/C4/C8）、无轴（其余）≥2 ✓
- 时间尺度：22/66/120/252 + 横截面 ≥2 ✓
- 形状族：group_rank/rank/ts_rank/ts_zscore/subtract/ts_backfill ≥3 ✓（trade_when 0%）
- 算子数：1-3（≥3 个 ≤4 算子）✓
