# 六件篮子最终验证（2026-11-10 20:5x）

## 互相关矩阵（threshold 0.7，years 4）

| | zq3eb7No | bl6AvMkN | RREPm361 | 1YNMAA8M | E569ZE7L | 1YWqzPGQ |
|---|---:|---:|---:|---:|---:|---:|
| zq3eb7No | 1 | 0.262 | **0.688** | 0.247 | 0.134 | 0.019 |
| bl6AvMkN | 0.262 | 1 | 0.281 | 0.513 | 0.131 | 0.112 |
| RREPm361 | 0.688 | 0.281 | 1 | 0.262 | 0.103 | 0.038 |
| 1YNMAA8M | 0.247 | 0.513 | 0.262 | 1 | 0.123 | 0.053 |
| E569ZE7L | 0.134 | 0.131 | 0.103 | 0.123 | 1 | 0.272 |
| **1YWqzPGQ** | 0.019 | 0.112 | 0.038 | 0.053 | 0.272 | 1 |

**结果**：`all_below_threshold = true` / `max_mutually_below_subset_size = 6`
⇒ **六件全部可共存**（用户全局标准：全对 <0.7）。

## ⚠ 提交前必查的一对

**zq3eb7No ~ RREPm361 = 0.6879（余量仅 0.012）**
- 两者同属 analyst7 预期族（RREPm361 是 zq3eb7No 的同族强化版）。
- 若平台池漂移，该值可能越过 0.7 ⇒ **提交 RREPm361 前必须用 compute_mutual_correlation 重算这一对**。
- 对照：1YNMAA8M ~ bl6AvMkN = 0.513、1YNMAA8M ~ rKRx2Alj = 0.695（后者是 OS 池件，余量 0.005）。

## DEU D1 塔位（2026-11-10 20:5x 实测）

```
institutions 1, insiders 0, model 3, news 0, other 2, analyst 6, pv 0,
earnings 0, fundamental 1, sentiment 1, risk 0, option 0, macro 0,
socialmedia 0, shortinterest 3, imbalance 0
```

- **已点亮（≥3）**：analyst 6、model 3、shortinterest 3
- **未点亮**：other 2（差 1）、fundamental 1、institutions 1、sentiment 1，其余 0
- ⇒ **提交 1YWqzPGQ（SHORT×OTHER）会让 other 从 2→3 点亮**

## 提交顺序建议（按风险从低到高）

| 序 | alpha | 风险点 | 前置动作 |
|---|---|---|---|
| 1 | **E569ZE7L** | 无（prod 0.5444 余量大、self 0.544、零负年） | prod refresh 即可 |
| 2 | **1YWqzPGQ** | 需 prod；会点亮 other 塔 | prod 终验 + 用户确认塔位 |
| 3 | **1YNMAA8M** | prod 0.6951 / self 0.6946 双贴线 | prod + self 双 refresh |
| 4 | **RREPm361** | prod 0.6881；**与 zq3eb7No 互相关 0.6879** | prod refresh + 与 zq3eb7No 互相关重算 |