# Osmosis 重排（平台权威源 + 实盘业绩加权）— 2026-10-09

## 实施内容（用户指令：先同步 OS 指标进库，再按真实实盘业绩重排）
1. `python tools/sync_platform_alphas.py` —— 全量同步平台 OS 池进本地库（本地台账 292、漏记 0；124 颗有 OS sharpe，167 颗平台尚未积累 OS 样本）。
2. 给 `tools/data-repair/osmosis_allocate.py` 新增 **`--source platform`** 模式：直接拉平台 OS 池、用平台 `is.prodCorrelation` 做 exclude（修掉 stale DB 的 prod 坑）、用平台 `os.sharpe`（并合并 DB 已 sync 的 `os_sharpe`）做权重代理，完全绕开本地库的存在性/prod 陈旧。
3. 重排：`--source platform --prod-policy exclude --prod-max 0.695`（review，仅写 plan，未 PATCH）。

## 新计划（平台权威，5 范围，含 GBR）
| Scope | n | 点数 | 占比 | 加权依据 |
|-------|--:|-----:|-----:|---------|
| IND D1 | 27 | 38501 | 38.5% | IS sharpe（无 OS） |
| USA D1 | 34 | 24035 | 24.0% | **20 颗按 OS sharpe**（avgOS 0.569），余 14 颗 IS |
| KOR D1 | 15 | 14623 | 14.6% | IS sharpe |
| MEA D1 | 18 | 13707 | 13.7% | IS sharpe |
| **GBR D1** | **10** | **9134** | **9.1%** | IS sharpe（**上一轮 4 范围漏掉，本次补回**） |
| **合计** | **104** | **100000** | 100% | |

## 旧计划（2026-10-09 0.695 刷新，DB 源，4 范围）对照
| Scope | n | 点数 | 占比 |
|-------|--:|-----:|-----:|
| IND D1 | 24 | 40050 | 40.1% |
| USA D1 | 18 | 25262 | 25.3% |
| KOR D1 | 17→15 | 17176 | 17.2% |
| MEA D1 | 19 | 17508 | 17.5% |
| 合计 | 76 | 99996 | — |

**差异**：新计划多覆盖 GBR（9.1%），IND 占比略降（40→38.5%），USA 颗数从 18 纠正为 34（DB 漏记 16 颗）、点数微调；总数 76→104（候选池更全）。

## 关键证据：平台源模式是必要的（DB 仍 stale）
本地 DB 用 `prod_correlation<0.695` 过滤的合格数 vs 平台真实：
- IND 24 vs **27**、USA 18 vs **34**、GBR 8 vs **10**、KOR 17 vs 15、MEA 19 vs 18。
- 根因：`sync_platform_alphas.py` 只给**缺失** alpha 回填 prod，不刷新**已存在** alpha 的 `prod_correlation`；而本地库的 prod 是旧的。平台源用平台权威 prod，正好避坑 → GBR 正确计入 10 颗。

## 诚实口径：OS 加权覆盖有限
- 合格候选中 `os_sharpe` 几乎为空：DB 124 颗有 OS 的都不在合格集（prod 高或被排除），平台列表 `os` 段仅 USA 回 20 颗。
- 因此本次重排 = USA 部分 OS 加权 + 其余 4 区 IS sharpe 加权。这是数据可达性上限（近期提交 alpha 平台未积累 OS 样本）。
- 要真正全量按 OS 业绩加权，需逐 alpha 调 `get_alpha_details` 拉 OS（100+ 次调用，性价比低，暂不做）。

## 下一步（待用户确认再执行）
- 当前 plan 已写 `results/osmosis_plan.json`（5 范围 / 104 颗 / 100000 点）。
- 落盘 PATCH（替换式分配：PATCH 计划内 + 零化非计划）需显式确认：
  `python tools/data-repair/osmosis_allocate.py --source platform --prod-policy exclude --prod-max 0.695 --apply`
  注：现成 `--apply` 仍依赖 `load_candidates_platform` 复算候选；零化步骤会用平台全量 ACTIVE REGULAR 作非计划集。

## 变体：排除 USA（用户 20:57 指令「先不给 USA 分配，都分配在其它区」）
- 给工具加 `--exclude-region`（逗号分隔；被排除区仍进零化集 → 拿 0 点）。
- 命令：`--source platform --prod-policy exclude --prod-max 0.695 --exclude-region USA`
- 结果（4 范围 / 70 颗 / 99997 点）：
  | Scope | n | 点数 | 占比 |
  |-------|--:|-----:|-----:|
  | IND D1 | 27 | 50684 | 50.7% |
  | KOR D1 | 15 | 19248 | 19.2% |
  | MEA D1 | 18 | 18041 | 18.0% |
  | GBR D1 | 10 | 12024 | 12.0% |
- USA 34 颗全部零化。点数从 USA 原 24% 按比例转移，IND 因 avg IS 最高(2.716) 拿最多。
- 当前 `osmosis_plan.json` 已写为此 4 范围变体（review，未 PATCH）。
