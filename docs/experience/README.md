# WQ BRAIN 挖掘经验资料库

> 本目录是项目内**挖掘经验的权威沉淀区**。分两层：
>
> | 层 | 定位 | 文件 |
> |---|---|---|
> | **实证经验层**（本轮新增） | 从 `.workbuddy/memory/2026-09-05 ~ 09-29` 全部工作日志 + `MEMORY.md` / `RULES.md` 提炼的可复用规律，按主题分类 | `01` ~ `05` |
> | **方法论规则层**（既有） | 从外部复盘 + 本仓固化的判据与矩阵 | `fail_fast_rules.md`、`field_operator_pattern.md`、`region_template_kb.md` |
>
> **提炼口径**：只收"下次挖 alpha 还能用上"的规律（含实测数字、字段名、阈值），
> 丢弃一次性流水账（"跑了 N 批""提交了 M 颗"）除非它带出通用结论。
> 日志中标注 `durable` / `铁律` / `勿再犯` / `教训` 的条目**优先收录**。
>
> 生成时间：2026-09-29 ｜ 来源时段：2026-09-05 ~ 2026-09-29（25 份日志，约 6,400 行）

---

## 实证经验层索引

| 文件 | 主题 | 核心内容 |
|---|---|---|
| [01_platform_gates.md](01_platform_gates.md) | **平台规则与硬门槛** | 提交层四闸、SUB 比值律、配额、相关性取数、点塔口径、universe/中性化合法档位、幽灵算子与幽灵字段 |
| [02_signal_patterns.md](02_signal_patterns.md) | **信号 / 结构有效性规律** | 合规单信号结构、组合形态铁律、破闸旋钮（分组轴 / decay / 中性化）、IS→OS 衰减、漏斗真相 |
| [03_region_dataset.md](03_region_dataset.md) | **区域与数据集特性** | 12 区实测画像、已判死数据集清单、塔点亮状态、选区优先级 |
| [04_engineering.md](04_engineering.md) | **工程与流程纪律** | skill 单点写入、DB 写锁与裸连接守卫、闸 SEM、提交钩子、测试守护、并发会话纪律 |
| [05_antipatterns.md](05_antipatterns.md) | **反模式与已证伪路径** | 加权混腿禁令、同族连提、存量微调抢救、已证伪端点与算子、误判陷阱 |

---

## 方法论规则层索引（既有）

| 文件 | 主题 | 要点 |
|---|---|---|
| [fail_fast_rules.md](fail_fast_rules.md) | 无效努力七信号 + 可修复 / 结构性判定 | `classify_failure()` 判 `STOP_STRUCTURAL` / `RETRY_FIXABLE` / `INCONCLUSIVE`；机器实现 `_lib/rules.py`，人看层即本文 |
| [field_operator_pattern.md](field_operator_pattern.md) | 字段类型 × 算子类别适配矩阵 | EUR wave104-123 实证；VECTOR 聚合在 EUR 均值为负；Logical 类使用不足但均值最高 |
| [region_template_kb.md](region_template_kb.md) | 区域模板 KB | 区域级模板与参数基线 |

---

## 关联资料（目录外）

| 位置 | 内容 |
|---|---|
| `reports/dataset_experience/` | EUR D1 数据集战役经验（news46/50、fundamental17/23、other455/460、pv1），由 `brain-dataset-mining-experience` skill 管理 |
| `output_report/` | 各区域 candidate ideas 与战役报告（EUR/IND/USA/GBR/GLB 等） |
| `.workbuddy/memory/` | 原始工作日志（本资料库的上游来源） |
| `Claude/skills/brain-dataset-mining-experience/SKILL.md` | 数据集经验沉淀 skill（每波 S6 复盘回写） |
| `tracking/<REGION>/` | 各区台账：dead_ends、registry_empirical、ledger_kv、s0_whitelist |

---

## 使用约定

1. **新增经验优先落这里**，不要只写在会话日志里——日志会沉，分类库会沉淀。
2. **每条经验必须带证据**（实测数字 / 字段名 / alpha id），无证据的判据不入库。
3. **与代码同批更新**：改闸门 / 阈值 / schema 时，同步修订对应分类文件（参照 `04_engineering.md` 的"文档与代码谁先动另一侧必须跟改"）。
4. **季度归档**：超过 90 天且已被新结论取代的条目移入 `attic/`，保留可追溯。
