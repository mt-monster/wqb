# KOR 战役启动案（2026-10-25）

## 用户指令（四条，全部落为硬约束）

| # | 指令 | 落地口径 |
|---|---|---|
| 1 | 找有潜力的数据集 | S0 排序 + 排除口径（见下） |
| 2 | 对近闸候选按 SOP 定向挖掘 | 六步纵深：体检→组装→归因→破闸→算子穷举→终验 |
| 3 | campaign 开波并发限制为 **2** | `WQB_GLOBAL_SLOTS=2`；在飞 ≤2；单批 ≤2 |
| 4 | 覆盖率**可动态调整**，但**十年都要有数据** | 取消固定 coverage 阈值；改用「2014–2023 逐年 PnL 非零」作准入闸 |

★ 相对旧 SOP 的最大改动：**第 4 条取代了「集级 coverage ≥0.8 / 处女地 ≥0.35」这条静态闸**。
低覆盖集不再一律排除，但**十年有数据是硬门**——缺年的集直接出局，不进 S1。

## S0 排除口径

排除项（命中即不入池）：
1. `dead=True`：`multi_source_model`、`acquisition_model`、`model170`
2. `tier=exclu`：`analyst_consensus`、`analyst_revision_horizon`
3. 平台锁定：`pv1`（`status=platform_enforced`，6.7 万 alpha）
4. 已判死族：`KOR-VALUE-QUALITY-SEEDS`（`registry_empirical` dead_end，85 个 value/quality 草稿）
5. 数据集级已提交 ≥3 颗（查 `get_submit_ready(region="KOR")`，不按塔排除）

## 候选池（tier1 + 低 alphaCount）

| 数据集 | 类别 | 字段 | aCnt | 选它理由 | 状态 |
|---|---|---:|---:|---|---|
| `predictive_starmine` | MODEL | 645 | 58 | 已测覆盖率仅 **7.2%**（373 base concept 只碰 27）；历史产出 prod **0.5437** | 待探针 |
| `ml_factor_proj` | OTHER | 333 | 16 | OTHER 塔差 2 颗；拥挤度极低 | 待探针 |
| `ai_factor_transfer` | MODEL | 20 | 12 | 最不拥挤（aCnt 12） | 备选 |
| `analyst_earnings_ibes` | MODEL | 28 | 6 | aCnt 仅 6 | 备选 |
| `model135` | MODEL | 137 | 39 | 中等规模、未深挖 | 备选 |

## 新增步骤 S0.5：十年数据存在性探针（本轮新增，因第 4 条要求）

**方法**：每集取 1 个高覆盖代表字段，跑 1 条最小仿真 `rank(F)`（KOR/TOP600/D1，STATISTICAL，decay 4，trunc 0.08），
再 `get_alpha_yearly_stats` 取 2014–2023 逐年 PnL。

**判定**：
- 逐年 `pnl != 0` 且 `longCount+shortCount > 0` ⇒ **有数据**
- 任一年 `pnl == 0` / 持仓为 0 ⇒ **该年无数据 ⇒ 整集出局**（不接受「后面几年有效」）
- 输出字段：`first_year / n_years / empty_years / min_yearly_sharpe`

**成本**：1 仿真 + 1 stats / 集。并发 2 ⇒ 每轮 2 集。

## 并发纪律（第 3 条）

- 在飞 ≤ **2**，不再沿用「campaign 7 / 单批 8」
- 探针与主批**不混跑**：探针跑完再发波动挖掘
- 每轮收割完再发下一轮，不做流水线叠加

## 发波三问（铁律 G，开波前必写）

**Wave 1（本轮）**
1. **继承**：S0 排序 + 十年探针结论（`predictive_starmine` 覆盖率 7.2%、历史 prod 0.5437）
2. **准入**：禁 `truncation` 扫描｜禁 `universe` 扫描（本区唯一 TOP600）｜禁单独扫 decay｜禁 `ts_ir` / `ts_target_tvr_hump`
3. **收窄**：4 集探针 → 存活集 ≤2 个进 S1；候选数后续每波 ≤ 上波 1/3

**已死轴（命中即禁入 quota）**：`truncation` 谱｜`universe` 谱｜单独 decay 谱｜同族已分优劣的平滑器窗口｜跨区配方照搬。

## 执行顺序

```
S0 排序（已完成，本地零成本）
  → S0.5 十年探针（并发 2，每轮 2 集）
  → S1 字段画像（0.1 质量先验 → 0.2 description 分类 → 0.3 五问）
  → S2 定向挖掘（铁律 H：先立机制，再组装）
  → S3 并发 2 回测
  → 归因 → 破闸 → 终验
```

## 阻断记录

- 2026-10-25 18:15 MCP 服务（`wq-brain-http`）宕机，HTTP 000，工具索引失效 ⇒ 已重启。
  影响：期间 `workflow_submit_alpha` 返回 `fetch failed`（但 `d5KJLqEw` 实际提交成功）。
