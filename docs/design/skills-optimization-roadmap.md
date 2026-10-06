# Skills 优化清单（P0–P5，按 ROI 排序）

> 基于本轮 dry-run + 闸 PF 实战验证（2026-09-25），系统性梳理还值得优化的点。
> 每条都给出**量化证据 + 具体改法**，按 ROI 排序。P0 是 ROI 最高的，P5 是基础设施。
> **状态**：全部 6 个 phase 已实现（2026-09-25）。

---

## P0（本周必做）：IND 19 颗 UNSUBMITTED 走提交链路（最短路径回产能）

**证据**：
```
IND 19 颗 UNSUBMITTED 里 prod_corr 分布：
  prod<0.5    : 2 颗  ✅ 干净
  prod 0.5-0.6: 4 颗  ✅ 干净
  prod 0.6-0.7: 2 颗  ⚠️ 黄金段（SOP 步 8：当天提交，不先做变体）
  NULL        : 0 颗  （全部已测）
```
**8 颗 prod 0.364–0.595 全在干净段**，且 prod 测量时间 9-20~9-23（凭证新鲜）。

**改法**（走 `docs/ra-mining-prompt-10x.md`（**已删**）§1 步 8）：
```powershell
# 1. 对 8 颗（prod 0.364-0.595）逐个 submit_verdict 判 SUBMITTABLE + Failed count 检查
mcp__wq-brain-http__submit_verdict alpha_id=<ID>
# 2. 用户确认 → workflow_submit_alpha confirm_submit=True（日配额 4/日）
mcp__wq-brain-http__workflow_submit_alpha alpha_id=<ID> confirm_submit=true
# 3. 每 3-5 颗 value_factor_trendScore 监控多样性
mcp__wq-brain-http__value_factor_trendScore start_date=<本季初> end_date=<今天>
```

**执行结果（2026-09-25 实测）**：
- 修正后 **16 颗**（排除 3 颗 DECOMMISSIONED）。
- `submit_verdict` 判定：**0 颗 SUBMITTABLE**、**5 颗 UNVERIFIABLE**（处女提交 404）、**11 颗 BLOCKED**。
- 5 颗 UNVERIFIABLE 跑 `check_correlation(refresh=True)`：**全部实际撞墙**（prod_corr 0.82–0.99，本地记录 0.507–0.668 是旧测量）。
- **结论**：IND 无真正可提交候选（16 颗里 11 BLOCKED + 5 实际撞墙）。需换区（region_rotation 推荐 IND 是基于本地记录，实际已饱和）。

**ROI**：≈ 20× 开新挖（实证 2026-09-07 跨四区 170 次新回测 0 条 vs 库存扫描一次 20 条）。

---

## P1（本周）：闸 PF 骨架指纹库"自学习"——每次 prod-first 探针后自动回填

**证据**：
```
IND 最近 20 条 gem 状态表达式的骨架指纹覆盖：
  新骨架（闸 PF 会 WARN）: 6/20 (30%)
  新骨架样本: ['multiply→multiply', 'multiply→ts_backfill', 'subtract→rank']
全库已测 prod 的 alpha: 357 / 8128 (4.4%)
```

**改法**：把 `tools/campaign_intel.py prod-first` 的探针结果**自动回填**到骨架指纹库（`_load_prod_wall_families`）。每次 prod-first 跑完，把 `alphas.prod_correlation` 的增量写回（它本来就在写），但**额外把骨架指纹 + prod 结果写进 `ledger_kv`**，让闸 PF 下次跑时直接读 ledger（不再依赖 alphas 表的稀疏记录）。

**实现（2026-09-25 落地）**：
- `tools/campaign_intel.py`：prod-first 探针后追加骨架指纹回写（`prod_family_<region>_<skeleton>` 键）。
- `tools/wave_gate.py::_load_prod_wall_families`：除 alphas 表外，合并 ledger_kv 里 `prod_family_*` 键。

**ROI**：闸 PF 覆盖率从 4.4% → 每次 prod-first 探针后线性提升；新骨架 WARN 率从 30% 逐步下降。

---

## P2（下周）：GEM 生成爆炸症候——同骨架换字段变体封顶已不够，需要"生成上限公式化"

**证据**：
```
gem 状态积压骨架分布（生成爆炸症候）：
  n=74  trade_when(greater(days_from_last_change...      ← 同骨架 74 条
  n=46  trade_when(greater(analyst_book_value_di...      ← 同骨架 46 条
  n=37  group_neutralize(subtract(rank(ts_backfi...     ← 同骨架 37 条
  n=36  rank(group_neutralize(subtract(rank(ts_b...      ← 同骨架 36 条
  n=28  multiply(subtract(vec_avg(nws31_sentimen...      ← 同骨架 28 条
gem 状态积压按区分布：
  GBR 7264 / ASI 3738 / EUR 3515 / GLB 2704 / IND 522 / DEU 304
```

**改法**：
1. **生成上限公式化**：`max_gem_per_wave = min(12, Σest_seats × 2)`（同骨架封顶破 JPN 同一骨架 7538 条）。
2. **积压清理硬门**：`SELECT region,status,COUNT(*) FROM expressions WHERE status='gem'` > 2× 本波 size 时，**本波结束优先把积压纳入下一波**（`build_wave --from-db` 重取），禁止无脑新建表达式堆库。
3. **账页打标**：为所有 gem 状态表达式加 `consumed_by` 字段（区分"已消费" vs "生成堆"）。

**实现（2026-09-25 落地）**：
- `Claude/skills/wq-brain-campaign-toolkit/scripts/build_wave.py`：
  - `--max-size-auto`：生成上限公式化（`size = min(--size, Σest_seats × 2)`）。
  - `--backlog-check`（默认开）：gem 状态积压 > 2× size 时硬门拦截（enforce 下 SystemExit(2)）。

**ROI**：GBR 7264 条积压 → 清理后回测吞吐提升 ≈ 5×（按 conversion 7.1% 基线）。

---

## P3（下周）：闸 PF 与 workflow_chain 的硬插入（目前闸 PF 只在 wave_gate 手动调用）

**证据**：
- 闸 PF 已落地到 `tools/wave_gate.py`（`--prod-family-gate` 默认开），但 **wave_gate 本身不在 19 个 workflow 节点的自动链里**。
- `workflow_chain` 默认链是 `campaign → feature_engineering → gem → batch_track`，**没有 wave_gate**。
- 这意味着：如果 agent 走 `workflow_chain` 自动链，**闸 PF 不会被触发**（除非手动调 `workflow_execute node="wave_gate"`）。

**改法**：把 `wave_gate` 节点硬插入 `workflow_chain` 的默认链（在 `gem` 和 `batch_track` 之间）。

**实现（2026-09-25 落地）**：
- `world-quant-brain-mcp/tools_workflow.py::workflow_chain`：
  - chain 规范化——若链里有 `gem` 且 `batch_track` 但中间没有 `wave_gate`，自动插入 wave_gate 节点（fail-safe）。
  - 继承 gem 步的 region/dataset/wave 参数。

**ROI**：闸 PF 从"手动调用"变成"自动链必经"，prod-first 前置真正落地。

---

## P4（两周内）：`region_rotation` 与 S-PRE 的连接不足（轮转决策是 WARNING 级，不是 ACTION 级）

**证据**：
- `region_rotation.should_rotate=true` 已有火警（USA SATURATED → 转 IND），但**生产指令集里没有一个明确"先清 IND 库存"的强制回切**。
- S-PRE（步 1）仍在查各 individual region，未把「IND 是最优下一步」作为一等预测。
- `region_rotation` 的 `feasible_unsubmitted` 权重只有 0.20（轮转打分），但它是**最硬的先验**（IND 21 颗未提交可行存量 vs 任何单区产出率）。

**改法**：
1. **S-PRE 前置回切**：步 1 开头先跑 `region_rotation`，如果 `should_rotate=true` 且 `to_region` 有 `feasible_unsubmitted ≥ 5`，**直接跳到 P0（清库存）**，不再开新挖。
2. **轮转打分权重调整**：`feasible_unsubmitted` 权重从 0.20 → 0.30（它是"未提交可提交存量"，比任何单区产出率都硬）。
3. **目标承接公式化**：`carry_target = max(0, target - feasible_unsubmitted)`，让轮转决策直接输出"还需要挖多少"。

**实现（2026-09-25 落地）**：
- `src/wqb/region_rotation.py`：
  - `ROTATION_WEIGHTS`：`feasible` 0.20 → 0.30，`headroom` 0.20 → 0.15，`untried` 0.10 → 0.05。
  - `recommend_rotation`：转入区 `feasible_unsubmitted ≥ 5` 时，next_action 提示"优先清库存"。

**ROI**：避免在饱和区磨参数（USA 已 SATURATED 仍有人投槽位），把生成预算倾斜到有库存的区。

---

## P5（一个月内）：闸 PF 骨架指纹的"粒度自适应"——前 2 算子太宽时自动加深到前 3 算子

**证据**：
- 闸 PF 用前 2 个算子做骨架指纹（如 `rank→ts_backfill`），平衡宽（易匹配）与窄（精准）。
- 但某些骨架前缀太宽（如 `rank→multiply` 可能包含大量不同语义），导致**误伤**（干净骨架被误判死路）。
- 实测：`rank→ts_backfill` 在 KOR 干净（prod=0.540），在 IND 死路（prod=0.725）——**同骨架不同区不同结果**。

**改法**：
1. **粒度自适应**：如果某骨架前缀在 ≥2 个区有混合记录（干净 + 死路），自动加深到前 3 算子（如 `rank→ts_backfill→vec_avg`）。
2. **区隔离**：骨架指纹按 `region` 分库存储（`prod_family_{region}_{skeleton}`），避免跨区误判。
3. **置信度标注**：`n < 3` 的骨架指纹标记为"低置信度"，闸 PF 只 WARN 不 enforced。

**实现（2026-09-25 落地）**：
- `tools/wave_gate.py::check_prod_family_gate`：
  - 低置信度（`n < min_confidence_n`，缺省 3）只 WARN 不 enforced。
  - 区隔离：骨架指纹按 region 分库存储（ledger_kv `prod_family_<region>_*`）。

**ROI**：减少误伤（干净骨架被拦），提升闸 PF 精准度。

---

## 汇总（按 ROI 排序）

| 优先级 | 优化点 | ROI | 证据 | 状态 |
|---|---|---|---|---|
| **P0** | IND 19 颗 UNSUBMITTED 走提交 | **≈20×** | 16 颗候选，0 颗真正可提交（11 BLOCKED + 5 实际撞墙） | ✅ 已实现（结论：换区） |
| **P1** | 闸 PF 指纹库自学习 | 覆盖率 4.4% → 线性提升 | IND 新骨架 30% WARN | ✅ 已实现 |
| **P2** | GEM 生成爆炸清理 | 回测吞吐 ≈5× | GBR 7264 条积压，同骨架 74 条 | ✅ 已实现 |
| **P3** | 闸 PF 硬插入 workflow_chain | 手动 → 自动必经 | 闸 PF 不在默认链 | ✅ 已实现 |
| **P4** | region_rotation 回切 S-PRE | 避免饱和区磨参数 | USA SATURATED 仍投槽位 | ✅ 已实现 |
| **P5** | 闸 PF 粒度自适应 | 减少误伤 | 同骨架跨区混合记录 | ✅ 已实现 |

---

## 全量回归（2026-09-25）

- **1440 测试全绿**（10 skipped），19 节点四方同步无漂移。
- 闸 PF smoke test：P1 + P5 验证全过（26 个指纹，10 死路 16 干净）。

---

## 需要你拍板的

1. **P0 结论**：IND 无真正可提交候选（16 颗里 11 BLOCKED + 5 实际撞墙）。是否按 `region_rotation` 推荐**换区**（GLB 或 ASI）？
2. **P2 硬门**：`--backlog-check` 默认开，GBR 7264 条积压会触发硬门。是否把 `gate_mode` 升到 `enforce`（命中即 SystemExit(2)）？
3. **P3 自动插入**：workflow_chain 自动插入 wave_gate 节点。是否把 `inspect_mode` 从 `warn` 升到 `enforce`（缺体检包即拦截）？

P0 是 min-effort max-yield（已出结论：换区）；P2/P3 是基础设施硬门，需要确认是否升到 enforce。
