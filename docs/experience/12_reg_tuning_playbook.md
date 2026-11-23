# REGULAR 精调与平台工具实战手册（2026-11-21 整理，源 `.workbuddy/memory/MEMORY.md` §3.2–3.3）

> 本文件是 MEMORY.md §3.2–3.3 的全量载体。MEMORY.md 只留核心条目与本文件导航；**判据优先级：MEMORY.md 铁律 > 本文件 > 当日日志**。

---

## 一、表达式与参数（REGULAR 精调主战场）

### 1.1 参数精调必扫清单（2026-11-20 教训：漏扫导致错失最优件）
① **窗口类**（`ts_backfill` / `group_backfill` / `ts_av_diff` / `ts_mean` / `ts_delta`）
② `decay` ③ `truncation` ④ `neutralization`
⑤ **每个分组算子的「窗口 + std + 分组轴」**
⑥ 平滑层是否冗余（平台 `decay` vs 表达式内 `ts_decay_linear`）
⑦ 共有子式变量抽取
**「IS 最强」≠「参数已调完」。**

### 1.2 窗口类参数是六维零代价杠杆（11-21 三次实证）
- `group_backfill` 66→90（GBR inst1）：S 1.61→1.63、DD 6.00%→5.85%
- `group_backfill` 252→504（GBR imb）：IS 七项全改善、prod 余量 0.0098→0.0135
- `ts_backfill` 66→126→189（EUR macro27）：单调改善
**ops/fields 不变 ⇒ 不动 ATOM/Ladder 也不动六维 ⇒ 优先扫窗口再扫结构。**

### 1.3 IS 指标改善可能反向推高 prod（11-21 实证）
- GBR imb 的 `YPaaV0dA`（`ts_av_diff` 126→252）IS 四项更优，但 prod **0.7021 FAIL**（原件 0.6902）。
⇒ **「IS 更强」≠「可提交」；任何改动后必须重测 prod，不能沿用原件读数。**
- 多版本并存时按 prod 余量选（0.6865 > 0.6902 > 0.7021FAIL），但 **prod 只是必要条件，IS 也要平**。

### 1.4 变量抽取必用
- 重复子式双倍计数；**`a=...; <末行>` 多语句平台接受且赋值不计数**（实测 14→9 次、指标逐位不变）。
- ⚠ `preflight_expressions` **不解析多语句**（把变量名报成 `unknown_fields`）⇒ 直接用仿真验证，别被它挡住。
- 等价化简同样无损：`add(divide(a,2),divide(b,2))` → `divide(add(a,b),2)`（`divide` 2 次→1 次）。

### 1.5 平滑层冗余
平台 `decay` 与表达式内 `ts_decay_linear` 重复计平滑，**删后者常无损甚至更优**（GBR inst1：ops 7→6 且 S/F/sub/invest 全升）。
但删 `ts_zscore` / `ts_rank` 类尺度变换会杀 2Y，**不可删**。

### 1.6 CW（concentrated weight）两类成因
① **权重堆积类**——`ts_mean(group_rank(...), w)` 加**输出侧**有效（w∈[5,10]）。
② **截面稀疏类**（CW≈1/整数）——权重侧手段**逐位 no-op**，唯一解是让关键日截面 ≥11 只。
`truncation` 对 CW 恒零杠杆。

### 1.7 2Y＝时序分辨率的函数
`tvr` 抹平、`trade_when` 冻结 ⇒ `LOW_2Y` 与 `LOW_FITNESS` 互斥是**物理的**；
修 2Y 唯一手段 `winsorize(std=2)`（仅连续厚尾，对 rank 类输出是空操作）。

### 1.8 中性化轴 ↔ prod 反向（EUR/macro27 实证）
MARKET 0.812–0.819 ＞ INDUSTRY 0.746 ＞ **SUBINDUSTRY 0.696–0.698（地板）**。
同一族调 tvr(0.10–0.16) / 窗口 / `ts_rank` 都锁在 0.698±0.002
⇒ **prod 地板是数据集级，只有换信息机制（如 `trade_when`+`ts_quantile` → 0.534）或换轴才能破。**

### 1.9 USA insider 骨架 decay↓ ⇒ prod↑ 单调
d5 .6188 / d4 .678✓ / d3 .7017✗ / d2 .7175✗ ⇒ **decay 4 唯一合法点**。

### 1.10 `ts_delta(x,W)`＝历史长度筛子（规模代理）
W 越大截面越小 ⇒ sub 虚高但 CW 易爆（GBR 480 为 CW PASS 唯一点）；
**任何「填平截面」动作都杀 sub**（→ .28–.42）⇒ 只能精调 W。

### 1.11 形态禁忌
- 等权相加 `add(rank(A),rank(B))` 触发混腿闸（Step1.2）。
- 乘法 `multiply(rank(A),rank(B))`：两腿 rank∈[0,1] 相乘压向 0 侧 ⇒ **损失一半排序信息、S 必降**（USA insiders 族实测 1.59→1.48）。
- **跨数据集辅助腿允许入场三式**＝`trade_when` 门控 / `bucket` 分组轴 / `neutralize` 残差（门控条件不算信号腿）。

### 1.12 分组轴扫描常被漏（11-21 实测）
内置轴（subindustry / industry / sector / market）＋ 数值分桶（`bucket(rank(cap),…)`）＋
`group_cartesian_product`（**只能细分组，不改截面方向、不增信息**）＋
同区 GROUP 型字段（如 `industrial_factor*_grouping*`、`principal_component_*`、`exchange`）。
⚠ **任何非内置 GROUP 字段引入即多一个数据集 ⇒ ATOM 失效 ⇒ 走 IS-Ladder，
而这类轴 2Y 常仅 1.2–1.4 < 1.58 ⇒ 新增硬 FAIL**（USA insiders 族 5 个 GROUP 轴全测，S 1.59→1.36–1.38）。

---

## 二、工具与平台

### 2.1 论坛查证（正路唯一）
- `search_forum_posts` **已于 11-20 整体退役**（Playwright 抓 Cloudflare 页，恒返 0 结果且 `success:true` 假信号；代码/注册/文档/配置全删；防回归闸 `tests/unit/08_forum_recon/test_forum_single_way_gate.py::test_retired_playwright_search_is_not_reintroduced`）。
- **正路 `search_forum_posts_local(keywords=[...], limit, max_pages)`**（Zendesk 列表端点 + 本地词命中率过滤）；读正文 `read_forum_post(article_id="<数字>")`；文档 `get_documentation_page(page_id)`。
- **文档=权威规则，论坛=假说须本区实测。**

### 2.2 平台坑
- `rank_by_side` / `is_not_nan` / `ts_median` / `ts_ir` **幽灵/不可用算子，勿用**——先查 `/operators`。
- `create_multi_simulation` 不校验字段；**2–10 条**（平台拒单元素数组；单仿真工具 2026-11-21 已从 MCP 层删除 ⇒ 探针也须 2 条）。
- **`run_selection` 筛标的不筛 alpha**；`sa_probe` 只数 ACTIVE。
- USA 的 selection 必须字面含 `(prod_correlation > 0)`。
- **`MATCHES_THEMES` 返回的是当期 theme 清单，不是该件的命中结果**（KOR 件也列出 USA theme）⇒ 主题资格只能按公告硬条件自查（USA + Delay-1 + TO 15–30%，11-09~12-06）。
- EUR/insiders：cov<0.7 一律 `nanHandling ON`；`total_*` 与 `avg_*` 在 `group_rank` 后等价 ⇒ 要广度必须 `divide` 后不 rank。

### 2.3 相关性槽
单并发；`correlation_busy` 多为他人/自动终验占槽（tag `prod_backfill(<id>)`），
**不是本任务失败，勿反复重试**；平台可触发账号级熔断（提示剩余秒数），按提示等。

### 2.4 提交节点坑
`workflow_submit_alpha` 偶报 `transport_error: Semaphore bound to a different event loop`，
节点会 `async_resubmit` → 201 accepted → verify ACTIVE；**不要手动重试**。

---

## 三、2026-11-21 夜：USA insiders1 窗口×decay 双向验证（`kqNb1g5d` → `VkNzob9G`）

### 3.1 ★★★★ prod 由「信号速度」驱动，可双向调节

同一骨架只动窗口/decay，prod 单调响应：

| 变体 | S | F | 2Y | prod | 判定 |
|---|---:|---:|---:|---:|---|
| `ts_zscore` 252 / decay 5（原件） | 3.32 | 3.29 | 3.65 | 0.6972 | ✓ 余量 .0028 |
| `ts_zscore` 126 / decay 5 | 4.04 | 4.16 | 4.31 | **0.7275** | ✗ |
| `ts_sum` 11 / decay 5 | 3.83 | 3.92 | 4.63 | **0.8482** | ✗ |
| **`ts_zscore` 168 / decay 6** | **3.67** | **3.73** | **3.98** | **0.6913** | **✓ 余量 .0087** |
| `ts_zscore` 168 / decay 6 → self | — | — | — | **0.5959** | ✓（原件 .6835） |

- **→ 加速（`ts_zscore`↓ 或 `ts_sum`↓）⇒ prod↑**；**← 减速（decay↑）⇒ prod↓**。
- 与 §1.9「USA insider 骨架 decay↓⇒prod↑ 单调」是**同一机制的两个方向**，已双向验证。
- ⇒ **prod 贴线时，第一动作是 `decay`↑，不是换字段**（零代价、不动六维/ATOM）。

### 3.2 ★★★★ 本族两个「零杠杆」旋钮（不必再扫）

- **`ts_backfill` 窗口 66 / 120 / 189 三档结果逐位相同**（S 3.32 / F 3.29 / 2Y 3.65 / DD .0550 完全一致）⇒ 该族字段覆盖率极高，backfill 窗口无信息增量。
- **`bucket` 步长 0.05 / 0.1 / 0.2 三档 S/F/2Y 完全一致**，只有 DD 第 4 位小数变化。
⇒ **省掉这两类扫描，把预算集中在 `ts_zscore` / `ts_sum` / `decay`。**

### 3.3 ★★★ 甜点定位法：二维网格（窗口 × decay）

单维扫描会错过「IS 升 + prod 降」的交点。本例：
- decay 5 × zscore 126 ⇒ IS 最强但 prod 破线
- decay 6 × zscore 252 ⇒ prod 安全但 IS 无改善
- **decay 6 × zscore 168 ⇒ 两者兼得**（S +0.35 / F +0.44 / 2Y +0.33，prod 余量 ×3，self 余量 ×6）

⇒ 规则：**IS 改善件一旦 prod 破线，不要立刻放弃，先加 `decay` 一档再扫窗口。**

### 3.4 ★★★ `MATCHES_THEMES` 在 USA 是真判定，不是清单展示

此前记「`MATCHES_THEMES` 返回当期 theme 清单而非该件命中结果」——本次实测修正：
`VkNzob9G`（USA/D1，TO **17.11%**）返回 **PASS**，命中两个主题并给出合计倍率：

| theme | 倍率 |
|---|---:|
| `Qy2rjZy` USA/D1 turnover 15...30% Theme | **2.0** |
| `V4Jjqj4` USA/D1/INSIDERS Pyramid Theme | **1.1** |
| **合计 `MATCHES_THEMES.multiplier`** | **3.89** |

⇒ **TO 落在 [15%, 30%] 的 USA/D1 件有 ×2.0 主题乘数**，叠加塔类别主题 ×1.1。这是 base 的免费放大器，**选件时应把 TO 压进 15–30% 区间**。
（旧记录描述的混淆应是被同一响应里并列的**未命中** theme 条目误导：本件另有一条 `GLB/D1 Power Pool Nov'26` 是 `WARNING`，那条才是"清单展示"。）
