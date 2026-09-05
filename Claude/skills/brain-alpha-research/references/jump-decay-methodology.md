# GLB PPA 点塔方法论（jump_decay 算子）——论坛学习沉淀

> 来源：post 37877587810327《GLB区域使用ppa点塔》（YB44630, 2026-01-23, 15 votes, 14 comments）
> 学习时间：2026-08-05。原始存档：`tracking/forum_glb_ppa_pyramid.json`
> 状态：**jump_decay 权限未开放（当前账号 inaccessible）**——方法论先行沉淀，权限开放后按本档实验

## 1. 核心表达式（帖子模板）

```
jump_decay(ts_delta(x, 5), 3, sensitivity = 0.3, force = 0.05)
```

**语义**：先算 5 周期差值（判断 5 天内变化幅度），再用 jump_decay 过滤因跳空高开/低开、巨量/地量导致的异常差值——"保留有效趋势、过滤无效噪声"的保守型预处理组合。

**两个场景**：
1. 趋势跟踪：`ts_delta(close, 5)` → 过滤单日跳空导致的假趋势
2. 成交量异动：`ts_delta(volume, 5)` → 平滑解禁/巨量噪音，聚焦"持续的量能异动"

**作者评价**："这几个表达式的 sharpe 不是很高，但是整体趋势非常不错"——PPA 点塔看重趋势稳定性而非极限 sharpe（与论坛 robust 文章"Main 别冲太高"一致）。

## 2. 参数调优指南（作者详解）

| 参数 | 调大 | 调小 | 配合原则 |
|---|---|---|---|
| `d`（3→5→8） | 窗口更广，过滤短期小波动，对快速突变迟钝 | 窗口更窄，快速捕捉跳变，易误触发 | 调大 d 可配调小 sensitivity |
| `sensitivity`（0.3→0.1 敏感 / 0.8 保守） | 只识别大幅波动（50-80%+），过滤噪音 | 捕捉微小异常（10-20%），易误触发 | 调小 sensitivity 可配调小 force |
| `force`（0.05→0.5 强 / 0.01 弱） | 大幅修正异常值，数据更平滑（可能失真） | 接近原始数据，保留真实波动 | 三者配合调节，非独立调参 |

**核心原则**：先明确目标是"捕捉所有微小异常"还是"只关注极端异常"——作者默认 0.3/0.05 是"温和保守、不易出问题但未必最优"。

## 3. 权限状态与适配方案（2026-08-05 实测）

- **jump_decay 提交时语法通过、运行时拒绝**：`Attempted to use inaccessible or unknown operator "jump_decay"`——与帖子评论区一致（YB44630："应该权限还没开放"）
- 本地 grammar.py 已有 jump_decay 记录（"jump_decay": 1），paradigms.py 归入 _FILTER_POOL（hump/bucket/jump_decay/nan_mask 同组）
- **适配方案（已实测 GLB/TOPDIV3000/FAST）**：`winsorize(ts_delta(x,5), std=3)`（截断跳变）+ `ts_decay_linear(...,5)`（平滑）模拟——**结果无效**（sh -0.44~0.15，tvr 0.30-0.50 高换手，GLB 三区域子域全 fail）。跳变平滑无法用 winsorize 精确模拟（winsorize 是静态截断，jump_decay 是相对跳变检测）

## 4. 未来实验计划（权限开放后）

1. 原版模板：`jump_decay(ts_delta(close, 5), 3, sensitivity=0.3, force=0.05)` + ts_rank 包装
2. 参数网格：d ∈ {3,5,8} × sensitivity ∈ {0.1,0.3,0.5} × force ∈ {0.02,0.05,0.1}
3. 场景验证：close 趋势 / volume 异动 / 单数据集字段（非基础字段）差值
4. 区域：GLB（帖子场景）+ KOR（pv106 流动性差值——KOR sharpe 引擎的跳变过滤可能提升 2Y）

## 5. 关联

- [[asi-methodology]]（robust 达标四件套——"Main 别冲太高"同源思路）
- [[forum-template-library]]（模板库 A-E）
- [[backtest-experience-archive]]（GLB 三区域墙：b1-b7r 全验证）
