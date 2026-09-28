# Alpha 提交属性（name / color / tags）一致性审计

> 审计日期：2026-09-20 ｜ 范围：平台 ACTIVE alphas 实测 + 项目代码/skill 约定
> 结论：**当前有 5 类命名约定、3 种颜色语义、6 类标签语义并存，且 PPA 专有约定被无条件套用到全部提交**。

---

## 一、结论先行

| 维度 | 现状 | 问题 |
|---|---|---|
| **name** | 5 种互不兼容的形态并存，**过半为空** | 无法从名字反查来源/质量 |
| **color** | `GREEN` / `BLUE` / `None` 三种，语义未定义 | 同一颜色代表不同东西 |
| **tags** | 6 类语义混用，**PPA 专有 tag 被无条件打给普通提交** | 语义污染，筛选失真 |

**三个根因**（都在代码/文档里，不是偶发）：
1. `Claude/skills/worldquant-submit-alpha/SKILL.md` 把 **PPA 专有**的 `name=<prod值>` + `color=GREEN` + `tags=["PowerPoolSelected"]` 写成了**通用**提交模板；
2. `src/wqb/workflow/nodes/submit_alpha.py` 把 `color` 默认设为 `"GREEN"`、`tags` 默认设为 `["PowerPoolSelected"]` —— **任何**走该节点的提交都会被打上 PPA 标签；
3. `tools/super_build.py submit --name <PROD值>` 又引入了第三种 name 语义。

---

## 二、实测证据（平台 ACTIVE 抽样）

| alpha | 区域 | 类型 | name | color | tags |
|---|---|---|---|---|---|
| `pwRJmvP3` | IND | REGULAR | `'0.6498'` | GREEN | `['PowerPoolSelected']` |
| `wpZ1vYzY` | IND | REGULAR | `'0.6842'` | GREEN | `['PowerPoolSelected']` |
| `levk5JYN` | IND | REGULAR | `'0.5493'` | GREEN | `['PowerPoolSelected']` |
| `QPbjxMYw` | IND | **SUPER** | `'0.65'` | **None** | `[]` |
| `88j6b1JX` | IND | REGULAR | **None** | **None** | `[]` |
| `Grb67d6O` | IND | REGULAR | **None** | **None** | `[]` |
| `levk1d98` | IND | REGULAR | **None** | **None** | `[]` |
| `ZYbqREW1` | IND | REGULAR | **None** | **None** | `[]` |
| `wpjJK60l` | KOR | REGULAR | `'kor_w113_grp_sec'` | GREEN | `[]` |
| `rKjY5vGj` | ASI | REGULAR | `'asi_cnn3_divyild_value'` | GREEN | `[]` |
| `9qpQ0VQ2` | GLB | REGULAR | `'GLB_pred10d_country_268'` | GREEN | `[]` |
| `j2rrpVzO` | USA | REGULAR | `'ppa_hiring_trends_ILLIQUID'` | GREEN | `[]` |
| `vRvg7NzA` | USA | REGULAR | `'earn_sent_overall_grank_stat'` | **None** | `['earnings_sent','tabbit']` |
| `gJ8eVmNM` | USA | **SUPER** | `'gJ8eVmNM_SA_prod0.7149'` | **BLUE** | `[]` |
| `KmP73gj` | USA | REGULAR | `'MengTao'` | BLUE | `[]` |
| `9WkpwQq` | USA | REGULAR | `'MengTao'` | None | `['homework']` |
| `vRVNZqrz` | USA | REGULAR | None | None | `['RETIRE_20260912','RETIRE_20260919']` |
| `Xgojww1X` | EUR | REGULAR | None | GREEN | `['PowerPoolSelected']` |
| 多颗 USA | USA | REGULAR | None | BLUE | `[]` |

> 大量 ACTIVE 为 `name=None / color=None / tags=[]`（三属性全空）。

---

## 三、五类命名约定（互不兼容）

| # | 形态 | 实例 | 语义 | 出处 |
|---|---|---|---|---|
| 1 | **PROD 数值** | `0.6498` / `0.6842` / `0.5493` / `0.6999` / `0.637` / `0.6616` | 提交时的 PROD 相关值 | `worldquant-submit-alpha` skill + `super_build --name` |
| 2 | **`<region>_w<wave>_<family>`** | `kor_w113_grp_sec` / `asi_cnn3_divyild_value` / `GLB_pred10d_country_268` | 区域+波次+数据集族 | 手工（无代码痕迹） |
| 3 | **`<strategy>_<field>`** | `ppa_hiring_trends_ILLIQUID` / `earn_sent_overall_grank_stat` / `fnd93_expense_range_stat` | 策略族+字段 | 手工 |
| 4 | **`<alphaId>_SA_prod<值>`** | `gJ8eVmNM_SA_prod0.7149` | SUPER 专用复合名 | 手工 |
| 5 | **`MengTao`**（人名） | `KmP73gj` / `9WkpwQq` | 无语义 | 手工（早期） |
| — | **空** | 多数 | 无 | 从未设置 |

**问题**：
- 形态 1（纯数字）**极易过期** —— name 是提交时快照，后续 PROD 变化后名字就骗人；
- 形态 1 与形态 4 语义重叠但格式不同；
- 无法用一条正则区分"来源数据集"。

---

## 四、三种颜色语义（未定义）

| color | 出现场景 | 推测语义 | 问题 |
|---|---|---|---|
| `GREEN` | 走 skill/节点默认值 的提交 | "PPA 合格/推荐提交" | 但大量**非 PPA** 的普通 REGULAR 也是 GREEN → 语义失效 |
| `BLUE` | 集中在 USA 一批 + 两颗 SUPER | 疑似手工分批标记 | **项目代码中无任何 BLUE 痕迹** → 纯手工，无规范 |
| `None` | 原生 API 直提（如本会话 4 颗） | 未设置 | 与 GREEN 混用后，"有颜色"不再代表任何东西 |

---

## 五、六类标签语义（混用）

| tags | 语义 | 评价 |
|---|---|---|
| `[]` | 无 | 多数 |
| `['PowerPoolSelected']` | **PPA 专有**（Power Pool 通道） | ⚠️ **被无条件套用到普通 REGULAR**（见根因 2） |
| `['PowerPoolSelected','MEA']` | PPA + 区域 | 同上污染 |
| `['earnings_sent','tabbit']` | 数据集族 + 来源工具 | 合用途，但无规范 |
| `['RETIRE_20260912']` / `['RETIRE_20260919']` | 退役留痕（API 无法退役的替代） | ✅ 这是**有设计**的合法用法 |
| `['homework']` | 来源标记 | 随口起名 |

**关键污染**：`PowerPoolSelected` 是**通道标识**（决定走 PPA 独立配额），不是"质量好"的标签。
被打到普通 REGULAR 上后：
- 控制台按该 tag 筛"PPA 候选"会**假阳性**；
- 与真实 PPA 候选混淆，影响配额归因。

---

## 六、根因（可执行修复点）

### 根因 1：`src/wqb/workflow/nodes/submit_alpha.py`
```python
color: str = "GREEN",          # 第 34 行：所有提交默认 GREEN
...
if tags is None:
    tags = ["PowerPoolSelected"]   # 第 60-61 行：所有提交默认打 PPA 标签
```
→ **这是污染的主要来源**。任何走 `workflow_submit_alpha` 的普通提交都会变成 `GREEN + PowerPoolSelected`。

### 根因 2：`Claude/skills/worldquant-submit-alpha/SKILL.md`
```
name="0.6525",  # prod correlation 值
color="GREEN",
tags=["PowerPoolSelected"],
```
示例被当成**通用模板**（第 43-45、58-60 行）。未见"仅 PPA 适用"的限定说明。

### 根因 3：`tools/super_build.py submit --name`
`--name` 描述为 "命名约定：PROD 最大值，如 0.6944" → 引入第二套数值命名。

### 其他
- `BLUE` / `MengTao` / `<region>_w<wave>_<family>` 在**代码中无任何痕迹** → 全部手工，无规范约束。

---

## 七、建议的统一规范

### name：`<REGION>_<TYPE>_<family>_<seq>`
```
IND_R_pv_rev_gate_01      # REGULAR, IND, pv 反转腿 + 条件门
IND_S_20comp_065          # SUPER, 20 组件, prod 0.65
```
- 必含**区域码 + 类型（R/S）+ 数据集族**；
- **不把 PROD 数值放进 name**（会过期）→ 放到 tags（见下）。

### color：语义化四色（复用平台调色板）
| color | 语义 |
|---|---|
| `GREEN` | 已提交且 OS 表现正常 |
| `BLUE` | 已提交、待观察 / 新批次 |
| `YELLOW` | 已提交但 IS 指标退化，待评估 |
| `RED` | 已标记退役（配合 `RETIRE_*` tag） |

> **禁止**把 GREEN 当作"默认值"。

### tags：三段式
| 前缀 | 用途 | 例 |
|---|---|---|
| `SRC_` | 来源数据集族 | `SRC_insiders1`、`SRC_news17` |
| `CH_` | 通道 | `CH_PPA`（仅真实 PPA 用）、`CH_REGULAR` |
| `W_` | 波次/工具 | `W113`、`TOOL_tabbit` |
| `RETIRE_<date>` | 退役留痕（保留现约定） | `RETIRE_20260920` |

**关键**：`PowerPoolSelected` 只在**真的走 PPA 通道**时打；建议改名 `CH_PPA` 以消除歧义（历史 tag 保留不动）。

---

## 八、修复清单（按优先级）

| # | 动作 | 文件 | 风险 |
|---|---|---|---|
| 1 | `tags` 默认改为 `None`（不打任何标签），由调用方显式指定 | `src/wqb/workflow/nodes/submit_alpha.py:60-61` | 低 |
| 2 | `color` 默认改为 `None` 或 `BLUE`，不再默认 GREEN | 同上 `:34` | 低 |
| 3 | SKILL.md 示例明确标注"**仅 PPA 适用**"，并补一段普通 REGULAR 的示例 | `Claude/skills/worldquant-submit-alpha/SKILL.md:43-60` | 低 |
| 4 | `super_build --name` 改为可选，默认自动生成规范名 | `tools/super_build.py` | 中 |
| 5 | 新增 `tools/alpha_properties.py`（批量规范化存量 name/color/tags，dry-run 默认） | 新文件 | 中 |
| 6 | 把本规范写入 `tools/README.md` + 相关 SKILL.md | 文档 | 低 |

> 改动 1/2/3 是**止血**（防止新增污染），改动 5 才是**追溯清理**存量。

---

## 九、存量盘点（需人工决策）

- **三属性全空**：多数 ACTIVE（约半数以上）→ 可批量补规范名 + `CH_REGULAR`；
- **误挂 `PowerPoolSelected` 的普通 REGULAR**：见于 `pwRJmvP3` / `wpZ1vYzY` / `levk5JYN` / `Xgojww1X` 等 → 建议保留（删除 tag 不影响已提交状态）但**新提交不再打**；
- **`MengTao` 命名**：2 颗，建议改名；
- **`RETIRE_*` 标签**：**不要动**（是退役留痕的唯一手段）。
