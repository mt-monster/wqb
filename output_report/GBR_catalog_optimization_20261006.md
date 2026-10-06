# 本地 catalog 问题：根因与优化方案（2026-10-06 12:25）

> 起因：我上一轮报告「本地 catalog 被并发会话实时重写」。**该结论错误，已纠正。**

## 一、根因（三条，均实测）

### ① 跨区串号 —— 真凶（我自己的查询错，不是数据被改）
- `fields` 表**没有 region 列**，region 只能靠 `datasets.region_id` 关联。
- **同名数据集在最多 13 个区各有一个 dataset_id**：`model38` 就有 **9 个**
  （GBR=264 / KOR=1233 / ASI=1699 / IND=1381 / EUR=1518 / GLB=893 / HKG=711 / DEU=1059 / USA=1854）。
- 我第一次查 `LIKE '%star_val%'` **漏了 region 过滤** ⇒ 命中 GLB/EUR/DEU 的行，误判「GBR model38 有 star_val」；
  第二次带上 `region_id=7` 又查不到 ⇒ 被误读成「数据被并发改掉」。
- 更严重的是：**GBR 的 `model38`(id=264) 平台有 71 字段、本地 0 行**（模拟能跑通证明平台有）。

### ② 本地 catalog 严重不完整（比串号更严重）
`catalog-gaps --region GBR` 实测：**131 个数据集本地字段 = 0，缺口 13,158 个字段**（本地 GBR 仅 7,579）。

| 缺口 | 数据集 | 缺口 | 数据集 |
|---:|---|---:|---|
| 1772 | `analyst_consensus` | 592 | `analyst10` |
| 1172 | `model219` | 560 | `continuation_score` |
| 855 | `analyst_revision_horizons` | 449 | `global_seasonal_model` |
| 670 | `model230` | 436 | `model26` |
| **648** | **`multifactor_return_pred`** | 399 | `techindi_model` |

⇒ **此前「GBR 只有 2297 个可用字段」的覆盖普查，是在残缺 catalog 上做的，真实池更大。**

### ③ 并发写入本身**不是**问题（写侧本来就安全，无需改）
- `journal_mode = wal`（读写不互斥）；
- `src/wqb/db_write_lock.py` 已有**跨进程文件 token 写锁**（TTL 自愈 + 死 pid 回收 + 降级放行）；
- `_field_catalog.py` 写入是 **SELECT → UPDATE/INSERT**（merge-only，**无 DELETE**）。

## 二、优化方案（4 层，已落地为可运行命令）

| 层 | 针对 | 方案 | 命令（仓库外工具） |
|---|---|---|---|
| **P0 读侧强制 region** | 跨区串号 | 静态扫描 `FROM fields` 但缺 `region_id` 的查询 | `wqb_tools.py catalog-guard` |
| **P1 冻结快照** | 读数不可复现 | 导出区级 JSON 快照 + **sha256**，波次记录引用哪个快照 | `wqb_tools.py catalog-snapshot --region GBR` |
| **P2 缺口可见** | 不知道本地缺什么 | 列「平台 field_count > 本地行数」的数据集 | `wqb_tools.py catalog-gaps --region GBR` |
| **P3 定向补齐** | 字段缺失 | 走 MCP 补齐，**merge-only，绝不 DELETE** | `wqb_tools.py catalog-fill --region GBR --datasets X,Y` |

**验证（已通过）**
- `catalog-snapshot`：GBR datasets=205 / local_fields=**7,879** / sha=`aa196d2e8883`。
- `catalog-fill`：`multifactor_return_pred` **一次补入 300 个字段**（cov 0.32–0.48）。
- `catalog-guard`：首扫 **18 处**疑似缺 region 过滤（需逐条人工确认，含假阳性）。
- **`region_catalog` 已重建 + 守卫测试 8/8 通过**（见下节）。

## 二·补 「region_catalog」重建与守卫（决策 1，已完成）

`src/wqb/region_catalog.py` 与 `tests/unit/01_store_db/test_region_query_guard.py`
此前**只剩 `.pyc`**（源文件被清理删掉），而 `tools/rotation/region_whitelist.py`
**正在 `from wqb.region_catalog import RegionCatalog`** ⇒ 属**真实断链**。

**已重建**（接口从 `.pyc` 反推 + 按调用方契约对齐）：
`RegionCatalog` 提供 `region_map / region_id / dataset_ids / region_of_dataset /
dataset_names / fields / field_names / field_exists / datasets_by_tower / tower_summary /
explain`，**所有查询强制 region 作用域**；跨区重名不指定 region 时抛 `RegionAmbiguityError`
（**拒绝静默解析**，而不是猜一个区）。

`rc.explain("model38")` 实测输出（一眼看清跨区分布与本地缺口）：
```
'model38' 存在于 9 个区 —— 查询必须带 region：
  region   ds_id     平台字段     本地行    aCnt  category
  GBR        264       71       0   10407  MODEL     ← 平台有 71、本地 0（缺口）
  EUR       1518      145     145   56424  MODEL
  GLB        893      200     200    8514  MODEL
  ...
```

**守卫测试（8 项，全绿）** 分两道防线：
1. **行为层**：临时 DB 造「两个区各有同名 `model38`、字段不同」，断言
   区隔离、`field_exists` 区作用域、`dataset_ids`/`region_of_dataset` 正确、
   **跨区重名抛 `RegionAmbiguityError`**、未知区抛 `ValueError`。
2. **静态层（棘轮）**：扫全仓 `FROM fields` 是否带 region 过滤；
   **历史债进基线（11 条），新增一处立即失败** —— 既不阻断存量，又能防新代码再犯。


## 三、★ 关键工程发现：字段枚举必须走 MCP，不能直连

直连 `GET /data-fields?dataset.id=<name>` 在本环境**对 GBR 恒返回 0**（参数被忽略）⇒
我第一版补全脚本据此得出「6 个数据集在本区无字段」的**假结论**。
根因是 **漏了 `instrumentType=EQUITY`**。改用带全参数的**分页**直连后立刻拿到 300 字段
（`limit=50` 是平台单页硬上限；MCP `get_datafields` 另有 `max_fields=300` 硬截断）。

> **纪律：字段存在性/枚举只信「带 `instrumentType` 的分页直连」与平台 `validate_expressions`；本地 `fields` 表仅供粗筛。**

## 三·补 决策 3（第二轮）：**catalog 覆盖率前置体检**（已做）

上一轮只做了「快照带 sha」，覆盖率体检**没有**接进前置流程。本轮补做，且**修正了口径**：

| 口径 | 定义 | GBR 实测 | 评价 |
|---|---|---:|---|
| A（弃用） | 本地行数 < `datasets.field_count` | 38 个 / 18.5% | ❌ **10 个假阳性**（`field_count` 非区级口径）|
| **B（采用）** | **真盲区** = 该区数据集本地 `fields` **一行都没有** | **28 个 / 13.7%** | ✅ 直接对应"选集会漏" |
| **B′（可行动）** | 真盲区 − **平台已确认本区为空** | **0** | ✅ 这才是要拦的数 |

- **覆盖率（有字段的数据集占比）= 86.3%**，已随快照写入 `cache/catalog/GBR_latest.json.coverage`。
- 新增两条命令：
  - `catalog-coverage --region GBR --write-manifest`（体检 + 固化进 manifest）
  - **`catalog-gate --region GBR --max-blind 0`**（**退出码 2 = 拦截**，供选波/挖矿前置调用）
- `catalog-fill` 遇平台返回 0 时写入 `cache/catalog/_platform_empty_verified.json`
  （标为"本区已确认空"），**避免同一个门反复误报**。
- **已固化到 skill**：`wq-wave-preflight-dispatch` 新增 **§0.0.7 catalog 覆盖体检**，
  置于 §0.1「字段笛卡尔积清点」**之前** —— 因为后者的前提就是 catalog 完整。

**顺带发现的数据质量问题**：`datasets` 表混有**伪数据集行**
（`pv/model/other`、`model25+model38+behavior`、`model38_star_val`、`insider_matrix+pv30+analyst47`、
`_unknown`…），GBR **14 个** `field_count=0` 且本地无字段且平台返回 0
⇒ **"该区有 N 个数据集"的分母要扣掉它们（205 → 约 191）**。

## 四、待办（需用户裁决，我没擅自动手）

1. **重建两个被删文件**：`src/wqb/region_catalog.py`、`tests/unit/01_store_db/test_region_query_guard.py`
   —— 现均**只剩 `.pyc`**，这是防跨区串号的唯一自动防线。⚠ 写回仓库有再次被清理的风险。
2. **批量补齐 131 个数据集**（约 13k 字段）：MCP 路径有 **HTTP 429 限流**，需分批 + 退避重试。
3. **把「本地 catalog 覆盖率」纳入每轮选集的前置体检**（与 `catalog-snapshot` 的 manifest 一起固化）。

## 五、与我此前结论的关系

- 覆盖普查的**方法**（表达式反解 token 命中 fields）仍然有效，但**分母错了** ——
  待补全后应重跑：`catalog-fill` → `catalog-snapshot` → 重新统计已测/未测。
- 「派生分无效」等**机制判据不受影响**（那是仿真结论，与 catalog 完整性无关）。
