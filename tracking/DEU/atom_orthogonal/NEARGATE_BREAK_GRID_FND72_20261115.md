# FND72 近闸件破闸网格（RREALzx0 / KPJmRpGN，2026-11-15）

> 用户指令：两颗近闸件查论坛、调参、全算子组合破闸。51 臂九批，全程 FAST 中性化（SUBINDUSTRY 三波 25 臂已证死）。

## 一、种子与前置

| 种子 | 表达式骨架 | S | F | 2Y | 初始缺口 |
|---|---|---:|---:|---:|---|
| RREALzx0 | 三腿乘：rank(ts_delta(q_ebit,240))×rank(ts_delta(176))×rank(ts_rank(1008))，group_rank(sector) | 1.42 | 0.95 | 1.43 | S/F/2Y 三闸 |
| KPJmRpGN | 同骨架，字段 q_is_oper_inc | 1.38 | 0.90 | **1.58** | S/F 两闸 |

- **prod 前置双净**（近闸纪律）：RREALzx0 0.6343 / KPJmRpGN 0.6265 ✅——扫参绿灯
- **论坛证据闸**：L2 双窗级联（skill lever-ladder：S+0.18/2Y+0.6）；73 赞帖 ebit/assets 比率化；30 赞帖 5Y 自身锚；31 赞帖 756 极值突破——全部入臂实测

## 二、九批网格（51 臂，按批序）

| 批 | 臂数 | 内容 | 关键发现 |
|---|---:|---|---|
| B1 | 9 | decay4 基线/比率化/zscore/tail×2/5Y 锚/SNR/窗 200/EBIT 对照 | **decay4 负杠杆**（S 1.38→1.33）；**比率化拉 2Y**（1.58→1.87）；tail 拉二 2Y |
| B2 | 5 | ts_max 等价族（用户指令不跳过）：ts_max_diff/ts_arg_max/ts_scale/ts_quantile | 全 1.20-1.32，弱于 tail 通道；**ts_max 平台不可访问**（静态闸拦截，幽灵家族第 4 员） |
| B3 | 8 | 比率×200/150 组合/轴扫描/ts_ir | **78Y0Pex8 破 S 闸 1.40/2Y 2.18**；subindustry 崩 sub（0.40）；industry -0.11 |
| B4 | 4 | decay2 微调 | decay 0/2/4 **单调负杠杆**确认，F 的 decay 路线关闭 |
| B5 | 10 | tail 带宽 0.05-0.25/窗 180-220/三腿 504-1260/std2-4/zscore | std3 峰 **1.43**（ZYaqJvPZ）；带宽 0.10 的 2Y **2.71**（e7agjZlJ）；zscore 全灭 |
| B6 | 3 | **hump 破 F**：hump=0.01/0.003 | **ZYaqO7dY hump=0.003：F 1.03✓ S 1.49**——四道闸破二 |
| B7 | 2 | hump=0.001 微调 | 0.001 差（1.42）——**hump 峰就在 0.003** |
| B8 | 5 | hump×带宽/窗位交叉 | **88NrmOVa hump003×240/176×std3：S 1.50**（窗位结论反转：hump 加持下 240/176 反超）；带宽 0.10×hump=0.005 → 2Y 2.83 |
| B9 | 5 | ts_ir 三腿/两腿/hump=0.004/带宽 0.12/窗 260 | ts_ir 全灭（1.07-1.13）；**mLaALJX2 带宽 0.12×hump003×240/176：S 1.50/F 1.04/2Y 2.30** 峰确认 |

## 三、终态与最优件

| 闸 | 读数 | 状态 |
|---|---|---|
| S | **1.50**（mLaALJX2 = 88NrmOVa）| **差 0.08，全维度到顶** |
| F | **1.04 ✓** | 已破 |
| 2Y | **2.30 ✓**（mLaALJX2） | 已破 |
| sub | 1.12 ✓ | 已破 |
| prod | **0.5444 ✅**（mLaALJX2 实测） | 已破，全族最净 |

**最优件 mLaALJX2**：
```
hump(tail(winsorize(group_rank(multiply(multiply(
  rank(ts_delta(divide(fnd72_s_pit_or_is_q_is_oper_inc, fnd72_s_pit_or_bs_q_1_bs_tot_asset),240)),
  rank(ts_delta(divide(...,240 同式),176))),rank(ts_rank(divide(...),1008))),sector),std=3),
  lower=0.12,upper=0.88,newval=0.5),hump=0.003)
```
S 1.50/F 1.04/2Y 2.30/sub 1.12/TO 16.3%/DD 6.4%/margin 0.96bp/prod 0.5444/failed_ra=1（仅 LOW_SHARPE）

备选：88NrmOVa（带宽 0.15，同 S 1.50/2Y 2.04）；vRA9K5Zw（带宽 0.10，S 1.44/2Y 2.83——2Y 最深备胎）；ZYaqO7dY（hump 首破 F 的 1.49/2.34）。

## 四、维度收敛判据（S 侧全扫）

decay（0/2/4 单调负）· 轴（sector 峰）· std（3 峰，2/4 双向回落）· tail 带宽（0.12-0.15 峰，0.05/0.10/0.25 回落）· 窗位（240/176 峰，180/200/220/260 回落）· 三腿（1008 峰，504/1260/ts_ir 回落）· 极值等价族（4 算子全弱）· zscore/SNR/5Y 锚（灭）——**双向回落证峰，非单调未尽**。

## 五、结论

两颗近闸件从 S 1.38-1.42 / F 0.90-0.95 / 2Y 1.43-1.58 推进到 **S 1.50 / F 1.04✓ / 2Y 2.30✓ / prod 0.5444✓**。四道 RA 闸破三，唯一残余 LOW_SHARPE 差 0.08——**S 1.50 是该动量族在 DEU 的信号层天花板**（≥3 轮卡同一结构性闸，止损规则触发）。非参数问题：正杠杆已全叠加（比率化+std3+tail+240/176+hump0.003），剩余路径只有跨族合成（Regular alpha 路线）或换核心。

**杠杆入册清单**（对照读数齐全）：
1. **hump=0.003 破 F 闸**（0.90→1.04；0.001/0.01 双向回落证峰）——免费换手压缩器在此族上 S 还 +0.07（1.43→1.50）
2. **decay 对动量信号单调负杠杆**（0/2/4：1.40/1.28/1.33）——L5 杠杆的反模式边界：动量信号与慢变量相反
3. **比率化（÷tot_asset）拉 2Y +0.29-0.72**（1.58→1.87-2.30）且不损 S
4. **ts_max 等价族排序**：tail(0.12-0.15) > ts_quantile/ts_scale/ts_max_diff/ts_arg_max（1.20-1.32）
5. **ts_max 平台不可访问**——幽灵算子家族第 4 员（ts_min_diff/ts_min/ts_max）

---

## 六、事后更正（2026-11-15，S0 复核槽追加，不回改上文正文）

- **§三 表格里 mLaALJX2 的 `margin 0.96bp` 是单位误读**。平台原值 `metrics.margin = 0.000955`，全仓换算是 `margin_bp = margin × 10000`（`Claude/skills/wq-brain-campaign-toolkit/scripts/metrics_cache.py:117`、`tools/verdict/candidate_health_card.py:141`）⇒ 正确读数 **9.55 bp**。
- **同表自相矛盾可作旁证**：`RREALzx0` 的 `margin = 0.000898` 在本档被记作「8.98bp」，用的是 ×10000；mLaALJX2 的 0.000955 却按 ×1000 读成 0.96bp。
- **结论不变**：margin 不是 RA check，本档「四道闸破三、唯一残余 LOW_SHARPE」的判断仍成立；更正只影响「要不要再设计一条提 margin 的臂」——**不需要**（9.55bp 已 ≥ 5bp 线）。
- 更正来源：`tracking/DEU/regular_tower/S0_TOWER_SCAN_20261115.md` §9.1 与 §11.8.3。
