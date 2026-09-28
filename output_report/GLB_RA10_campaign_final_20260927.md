# GLB D1 REGULAR Alpha 战役收官报告（目标：10 颗）

- 战役周期：2026-09-19 → 2026-09-27
- 区域/延迟：GLB / D1（平台仅支持 D1，无 D0 分支）
- 判定：**达成 ✓** —— GLB 平台 OS 池 **10 颗 REGULAR ACTIVE** + 1 颗 SUPER（A1NQ57NW，10 组件）

## 1. 10 颗 REGULAR ACTIVE 清单

| # | Alpha ID | 机制族 | S | F | tvr | 2Y | prod | self | 提交日 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | le3E3nM7 | ipv 尾盘 30m 成交价慢骨架反转 | 2.06 | 1.24 | 11.4% | 2.00 | 0.671 | 0 | 09-19 |
| 2 | gJboYLRl | ipv 价量相关反转（industry 轴/COUNTRY） | 2.67 | 1.13 | 41.6% | 2.85 | 0.665 | 0.228 | 09-21 |
| 3 | mLmxKN12 | ipv 尾盘 30m **高价路径**反转（country 轴/SUBIND） | 2.99 | 1.69 | 38.9% | 2.92 | 0.694 | 0.282 | 09-21 |
| 4 | d5bnE8jJ | dl20d × 尾盘量占比门控 | 3.62 | 1.49 | 44.6% | 4.10 | 0.631 | 0.188 | 09-21 |
| 5 | pwR8rdMg | dl20d × 12-1m 输家门控 | 3.81 | 3.06 | 15.1% | 3.93 | 0.601 | 0.601 | 09-22 |
| 6 | VkaXbmbG | dl20d × 借券费率门控 | 3.52 | 3.25 | 11.7% | 4.52 | 0.668 | 0.465 | 09-22 |
| 7 | MPakRYgz | dl20d × 高 EP yield 门控 | 3.15 | 2.25 | 13.6% | 2.69 | 0.660 | 0.660 | 09-23 |
| 8 | O0NoPARJ | dl20d × 低 EP yield 门控 | 2.31 | 1.35 | 14.7% | 1.93 | 0.619 | 0.619 | 09-23 |
| 9 | MPabNeNz | dl20d × 卖空利用率门控 | 2.74 | 2.09 | 12.5% | 3.31 | 0.675 | 0.675 | 09-24 |
| 10 | 9qpQ0VQ2 | techindi 10d 预测（**战役前存量**，08-04） | 2.68 | 1.35 | 24.0% | 1.75 | 0.776 | 0 | 08-04 |

本战役新增 9 颗（#1–#9），第 10 颗为战役前存量。全部 `failed_ra_count=0`、`checks.fail=[]`。

## 2. 两个出货机制（可复用）

**机制 A：intraday_pv_feats 尾盘反转（3 颗）**
- 铁律：信号**只在 MINVOL1M**，TOPDIV3000/TOP3000 全灭（32 条模型/分析师/新闻探针在 TOPDIV3000 下 |S|≤0.70，经典异象同样全平）。
- 快骨架 `ts_decay_linear(x, 5)` 是唯一能同时过 2Y 与 EMEA 的形态；`ts_backfill` 把 2Y 打到 0.07；`group_zscore` 比 `group_rank` 多 +0.1 fitness。
- 高价路径（`mean_high_price_return_30m_pre_close_2`）EMEA 天然过闸，成交价路径（`..._last_trade_...`）EMEA 0.58–0.93 在 9 种中性化下永不过——**字段选择比参数重要**。
- 不对称性：只有"不断创新高进入收盘"回吐（S2.99），低价路径镜像无信号（S0.37/2Y−1.14）——机制是追价回吐而非双向反转。

**机制 B：dl_riskfree_returns 20d CNN 预测 × 经济子域门控（6 颗）**
- 未门控 prod 0.77–0.84 撞墙（38 个结构/参数变体全部 0.76–0.87，单字段时序变换无解）。
- 门控模板 `trade_when(and(SUBSET, rank(cap)>0.2), signed_power(group_rank(X,country)−0.5, 0.5), or(SUBSET_exit, rank(cap)<0.1))` 把 prod 压到 0.60–0.67；6 个不同经济子域各得一颗。
- 六颗互相关 0.43–0.67（合法但同族），逐颗 `check_correlation(refresh=True)` + 分日提交。

## 3. 三条 prod 破墙路径（按有效性排序）

1. **子域门控**（唯一真正有效）：把信号限制在"它确实有效、而生产池不交易"的子集。前提：未门控基底 IS sharpe ≥2.5 且 fitness ≥1.5——risk68 基底 1.46，门控后仅 1.88/F0.68（本战役新增铁律）。
2. **变化率正交化**：ai_news 情绪水平 prod 0.70–0.76 → ts_delta 后 0.56，但 IS 强度掉到 1.3 过不了资格门。能过 prod 不能过强度。
3. **换中性化/轴**：±0.1 量级，单独使用无效（借券费率 23 个变体 prod 0.85–0.97）。

## 4. 穷尽性证据（registry dead_end 41 族）

全类别封死：pv（pv1/pv37/pv98/pv106/pv30/ipv 各子族）、model（32/135/238/239/243/264/28/36/138、techindi、tech_chart、chart_cnn、dl_riskfree 全族 139 条）、analyst（consensus/10/11/ARH）、fundamental（17/23/28/44）、news（17/23/31/52/73）、sentiment（21/22/26）、risk（60/68/70）、other（296/315/455/546/571/699）、macro、insider、institutions、earnings。

2026-09-27 收官日再探 4 个当时未封数据集，全部不达标：
- **risk68** 特定收益反转：未门控 max S1.46/F0.70，门控后 1.88/F0.68 → 判死。
- **other315** OTC 权益互换：|S|≤1.24，tvr 75–119%，CW 0.25–0.76（稀疏事件流做主信号必撞权重集中）→ 判死。
- **model264/model138** 基本面趋势概率：**发现新机制但强度不足** —— 模型预测"转差概率高"的股票未来跑赢（价值/逆向），符号取正；天花板 S1.40/F0.67/2Y2.35/tvr3.4%。留作 SuperAlpha 慢腿。

## 5. 工具根因修复（含回归测试）

| 事故 | 根因 | 修复 |
|---|---|---|
| `workflow_submit_alpha` 提交时把已设好的 name/description 清成 null（gJboYLRl） | 客户端无条件 PATCH 全字段 | `brain_mixin_correlation.build_alpha_properties_payload` 只发非 None 字段（对齐官方 ace_lib）；节点回写 `preserved`；`tests/unit/test_alpha_properties_patch_partial.py` |
| 跨金字塔门控波被闸2 误判"字段未验证"拦下 7/8 | 节点未透传 CLI 早有的 `--datasets` | `wave_gate` 节点新增 `datasets` 参数 + registry 声明；`test_run_logged_subprocess.py::test_wave_gate_node_passes_extra_datasets` |
| `workflow_execute(wave_gate)` 卡满 1800s（CLI <1s） | PIPE 捕获 + 不杀进程树 + 超时丢输出 | `_common.run_logged_subprocess`（日志文件 + 树杀 + tail），默认 600s |
| 死 pid 持有写锁拖住 3 条 pipeline 90–120s | 未校验持有者存活 | `db_write_lock` / `_lib/dblock` 加 `_pid_alive` 即时回收 |

> 注：`wave_gate` 节点的新参数需 MCP 服务重启后生效（服务缓存 `wqb.workflow`）；重启前走 CLI `tools/wave_gate.py --datasets`。

## 6. 下一步（按 ROI）

1. **换区域**：ASI 已落 3 颗（同门控模板），USA 队列 2 条 READY（np8VGNz3 / VkGJ73eA）。
2. **GLB 转 SuperAlpha**：已有 1 颗 SUPER；model264 镜像（tvr 3%/2Y 2.35）与快信号族正交，是优质慢腿。
3. **等新数据集**：GLB 单体 RA 在现有数据面上已证伪，新集上线再开。
