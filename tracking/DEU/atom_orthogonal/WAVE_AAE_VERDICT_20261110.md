# DEU 第三席：波 AA/AB/AD 判死 + 平台批次故障分叉（2026-11-10 上午末）

## 一、波 AA / AB：整批 CANCELLED，但字段本身可用（平台批次限制，非表达式问题）

### 现象
| 波 | 内容 | preflight | 平台结果 |
|---|---|---|---|
| AA | other532（Barra 特质收益）加速度结构 ×10 | **valid: true, unknown_fields: [], unknown_soft: []** | status=ERROR，子任务全 CANCELLED |
| AB | other532/other47/pattern_scores 简单 `ts_mean` 结构 ×8 | 全绿 | 同样整批 ERROR/CANCELLED |
| AC | other532 加速度结构，**改用 `create_simulation` 单条** | — | **成功**：`Xg9dQYJm` S-0.41 / lc 204 / pyramid other |

### ★ 判据 MU（平台批次分叉，跨区通用）

**整批 CANCELLED 有两种根因，必须分叉排查**：

| 根因 | 特征 | 处置 |
|---|---|---|
| 表达式错误 | preflight 报 unknown_fields / unknown_soft | 修表达式 |
| **平台批次限制（偶发）** | **preflight 全绿但整批 CANCELLED** | **拆小批，或用 `create_simulation` 单条重派** |

**排查顺序**：① preflight 全绿？② 单条 create_simulation 能过？⇒ 平台批次问题。
**代价提示**：单条 create_simulation 约 30~40 秒/条，10 条串行必超时（实测 290s 只跑完 1 条）
⇒ 必须后台跑或分小批。

### other532 单条实测读数（Barra 特质收益）
| 表达式 | S | lc | 判定 |
|---|---:|---:|---|
| `group_rank(ts_mean(ts_backfill(oth532_global_daily_specificreturn,132),22), subindustry)` | -0.41 | 204 | 字段可用，覆盖满，但信号弱 |
| `-group_rank(...加速度结构...)`（264/132） | -0.09 | 212 | 加速度结构同样弱 |

**归因**：Barra 风险模型残差本身是**已剔除系统性暴露后的收益** ⇒ 它是「收益的残差」而非「新信息」；
其变化在 DEU 截面无独立定价力（残差动量在学术上有效，但在 DEU 小市值单国家市场不成立）。

## 二、波 AD：pattern_scores（K 线形态相似度，pv 类，504 字段 cov 0.96~1.0）—— 判死

10 条（S -0.31 ~ +0.52，2Y -1.73 ~ +1.73），全部判死，符号混乱。

| 候选 | S | 2Y | lc |
|---|---:|---:|---:|
| Xg9dQAlX | 0.52 | 0.39 | 193 |
| qMLQrJzA | -0.31 | 0.41 | 178 |
| d5WNVrmE | 0.26 | -0.34 | 202 |
| bl6eZ1MZ | 0.16 | 1.73 | 189 |
| 1YNrbALK | 0.11 | -0.49 | 204 |
| mLoERWA2 | 0.03 | -1.28 | 203 |
| WjOvQ2Xj | 0.00 | 1.29 | 180 |
| QPvwkpjG | -0.04 | 0.98 | 189 |
| e75XwZgE | -0.16 | -1.73 | 193 |
| 88RM9xrW | -0.21 | -1.07 | 193 |

**归因**：K 线形态相似度是**价格的函数**（同一段历史 K 线的几何相似度）
⇒ 与已判死的内置价格字段同源（波 W 判定 DEU 纯价格机制无定价力）⇒ 一致判死。
**判据 MV**：形态/技术指标类字段本质是价格的确定性变换 ⇒ 若同源的纯价格机制在该区无效，
不必单独再测形态类数据集（但本轮是首次实测，结论与波 W 自洽）。

## 三、本轮新增判据

| 编号 | 判据 | 要点 |
|---|---|---|
| MU | 整批 CANCELLED 的两种根因分叉 | preflight 全绿 ⇒ 平台批次限制 ⇒ 拆小批或 create_simulation 单条兜底 |
| MV | 形态/技术指标类字段 = 价格的确定性变换 | 纯价格机制无效的区，形态类不必再单独测 |
| MW | Barra 残差 = 已剔除系统暴露的收益 | 残差动量在学术上有效但 DEU 小市值单国家市场不成立 |

## 四、DEU 域内可交付上限（最终确认）

**4 颗**（2 颗已 ACTIVE + 1YNMAA8M 待授权 + E569ZE7L CONDITIONAL）。

未点亮塔已逐一实测或因无供数排除：insiders（波 Y）/ news（波 N·U·V）/ risk（波 N）/
institutions（早前）/ earnings·macro·option·socialmedia·imbalance（cov=0 或过稀疏）/
pv（波 AD 形态）/ other（波 AA·AE）⇒ **DEU 域内已无第 5 颗的机制空间**。

要往第 5 颗走，**必须放开「不得换 region」过程约束**（goal 明文，需用户修改）。
