# DEU Fundamental ATOM 战役 · 类目终审报告（2026-11-07）

> 战役窗口：2026-11-07 04:33–05:27 · 派发 9 个 multisim 批次 · **110 条回测** · 并发全程 ≤2 · 全程 MCP 工具
> 交付口径：REGULAR 硬闸 S≥1.58 且 2Y≥1.58（用户 2026-11-06 确认）、sub 比例闸 0.474×S、prod/self ≤0.7、十年无连续空窗、算子 ≤12

## 一、终审结论

**在「DEU + Fundamental 类目 + 硬闸 S≥1.58/2Y≥1.58」的固定范围内，10 颗新 ATOM 结构性不可达。**

类目历史唯一一次全闸通过 = `Wje5K71x`（fnd6 oiadpq 加速度，S 1.73/F 1.37/2Y 1.87/prod 0.4305），**已于 2026-10-12 提交 ACTIVE(OS)**，其 prod+self 槽位已被占据。

## 二、五大机制面的天花板证据（本轮实测）

| 机制面 | 最佳构造 | S | 2Y | 卡点 | 已穷尽的杠杆 |
|---|---|---:|---:|---|---|
| fnd45 电话会 NLP | X3 正交三轴 rank 和（语调+数字密度+可读性，sector） | **0.99** | **1.89** | S 差 60% | 回填 66/252/504 × 组轴 4 种 × rank/zscore/decay/mean/winsorize/事件窗/rank积/正交合成 × 中性化 4 档 × tvr 限速移植 |
| fnd90 GAMES 质量 | cfc market group_rank | **1.02** | **0.42** | 2Y 差 1.16 | zscore/winsor/rank 3 几何同 S≈1.0（机制稳健）但 2023 信号死亡（逐年 S 0.01）系内禀；双腿合成稀释；动量轴死 |
| fnd6 点时财务 | oiadpq 六层配方 | 1.73✅ | 1.87✅ | **槽位已占**（已提交） | 第二梯队 piq 1.37/ibq 1.27 < 1.58；prod 刀锋 + 同骨架互斥 |
| fnd22 ESG KPI | vec_avg 水平 | 0.48 | 1.37 | S | 2 几何 |
| fnd17/86/89/93/72 | 历史探针 | <1.0 | — | 全灭 | 历史 8-20 探针 + 本轮复核 |

## 三、方法论产出（可跨战役复用）

1. **中性化四点曲线**（fnd45 语调族）：SUBINDUSTRY 0.99 > SLOW 0.86 > FAST 0.75 > STATISTICAL 0.51——STATISTICAL 的 techindi +31% 先例**不可跨信号迁移**。
2. **FAST 档扩书**：持仓数 27→190（书窄是 subindustry 分组成员数伪影而非数据缺失），但 S 不动 ⇒ 信号强度才是 S 瓶颈。
3. **平台 coverage 字段失真双向**：cov=0 的 fnd90 实有数据（lc 63-109）；cov=0.27 的 fnd45 日频真实覆盖仅 ~11%。
4. **rank 加法合成证伪**（fnd90 四字段 QMJ 0.64-0.68 不及单腿 0.86）；**正交异质轴合成有效**（fnd45 三轴 0.77→0.99）——合成价值取决于轴间经济正交性。
5. **tvr_decay×FAST 配方不可跨机制移植**（Wje5K71x → fnd45 全灭）。
6. 收割管线：batch_status（子代注册可滞后 ~55 分钟）→ harvest_multisim_alphas（指标在 a.metrics 嵌套）。
7. 逐年覆盖口径实测：fnd45/fnd90 十年无连续空窗（PASS），但信号时代分布两极（fnd45 后置 / fnd90 前置）。

## 四、可交付余量（均未达 REGULAR 线，按用户口径标注「不可提交」）

| 候选 | 数据集 | S | 2Y | sub | 缺口 |
|---|---|---:|---:|---:|---|
| `omEG5nk6` X3 正交复合体 sector | fnd45 | 0.99 | 1.89✅ | 0.81 | S/F |
| `LLMzan2n` X1 同核 industry | fnd45 | 0.98 | 1.88✅ | 0.80 | S/F |
| `KPJzjRx8` cfc winsor market | fnd90 | 1.02 | 0.42 | 0.96 | S/F/2Y |
| `vR1G3V0Q` cfc zscore market | fnd90 | 1.01 | 0.41 | 0.97 | S/F/2Y |

## 五、档案索引

- 字段目录：`tracking/DEU/atom_fundamental/fields/*.json`（12 集全量）
- 画像：`tracking/DEU/atom_fundamental/field_profiles_20261107.md`
- 设计稿：`wave_F1_design_20261107.md` / `wave_F6_design_20261107.md`
- 台账：`wave_F3_dispatch_20261107.json`（F1-F8 全程派发/收割/归因/覆盖体检）
- 历史参照：`output_report/DEU_fundamental_round2_20261013.md`（fnd6 六层配方 + 上限≈1 颗的结构性结论）
