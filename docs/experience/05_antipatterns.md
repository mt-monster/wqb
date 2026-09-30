# 05 · 反模式与已证伪路径

> 来源：2026-09-05 ~ 09-29 工作日志实证提炼 ｜ 更新：2026-09-29
> 本文件是「**不要再走的路**」清单。每条都对应真实烧掉的配额/槽位。

---

## 1. ★ 组合形态违规（最高优先级）

### 禁令

**禁止把两条独立信号腿加权相加**，包括：
- `add(multiply(0.4, A), multiply(0.6, B))`
- `0.4A + 0.6B`
- **等权 `add(rank(A), rank(B))`**（= 0.5A+0.5B，**同属违规族**）
- 嵌套 `quantile(add(multiply(0.7,X), multiply(0.3,Y)))` 与镜像腿

**也禁止**靠增删腿数、或扫描混合权重去修不达标的信号。

> **事故**：2026-09-28 wave189/190 产出 7 条 `add(group_rank(腿A), group_rank(腿B))`，
> 其中 `QPbp025Q` 表面极漂亮（S=2.11/F=1.80/2Y=1.89）但同样违规，**已全部作废**。
> 根因：闸 5 结构判定只拦「实参以 `系数*` 开头」的腿，其文档与原 SOP **明文豁免等权** → 7 条全部漏网；
> 而 SOP 旧文案却写「`0.5*rank(A)+0.5*rank(B)` 均被闸 5 block」——**文档与实现不一致**。
>
> **永久修复四层**：① `gate.py` 新增 `_detect_equal_weight_leg_add`；② `platform_constraints.json` v1.4→**v1.5** 登记 poison `equal_weight_leg_add`；
> ③ 回归 `tests/unit/04_gates/test_gate_equal_weight_leg_add.py`（16 条）；④ SOP「组合形态合规」重写。
>
> **durable 教训**：判合规看**本质**（是否两条独立信号腿相加），不看是否命中正则；
> **文档里的安全承诺（「闸会 block」）必须与实现同源校验**，否则会形成"文档说安全→放心用→实际漏网"的假安全。
> **门禁通过 ≠ 合规**：闸是兜底，不是许可证。

### 正确替代

见 `02_signal_patterns.md §1`：Mode B（换字段组合/信号概念/算子几何/分组轴）+ 单信号结构化白名单。

---

## 2. 同族连提（自相残杀）

- **同族（共享 base signal）兄弟连续提交会系统性推高后来者的 prod/self**：
  - DEU 实证 SELF **0.8963 / 0.9553 / 0.9562** 三次
  - GLB 族 prod：`0mXA6jYG` 0.672→**0.8168**、`A1Nn2vPQ` 0.606→**0.7079**、`QPbEkvzw` 0.593→**1.00**
  - `LLNgdpw2` self 从 0.0 升至 0.647（因同族 `88jaV5lv` 提交）
  - KOR `wpZkk1Mp` 提交后兄弟 prod 0.6476→0.6791
- ⇒ **同族一次只提 1 颗**，且**入池即重排全池相关性**。
- **被顶超线的兄弟会自然回落（约 1 天）**，非永久饱和
  → 纪律是「一次 1 颗 + 等回落再提」，不是永久封族（GLB dl20d 族 09-22 顶高 0.81/0.71/1.0，09-23 回落 0.66~0.67 并成功提交）。
- 必须连提则按 **IS 强度降序** + 逐颗重测兄弟 prod。

---

## 3. 存量池上做参数微调抢救 = 已证伪

- **602 条抢救池**：236 条 IS 干净但**双闸无一能过**（SELF 普遍 0.53–0.99、PROD 有值者全在 0.81–0.86）
  → **出量唯一路径 = 新挖不同质信号**。
- **存量池补 SA 已全面证伪**：USA 12 结构、KOR 9 结构、EUR 6 颗、DEU 116 颗全部被拦，四区同病根
  → **靠调参无解，唯一出路是注入 ≥3 颗低 prod（<0.55）新血 REGULAR**，把池的 prod 分布整体左移。
- **IND SA 同池重组已证伪**：22 颗池实测 0.86–0.97，`self_gate` 降到 0.5 仍 0.86，降到 0.3 则组件不足 10。
- **照抄既有 SA 配置 = 克隆拦截**：KOR 照抄 `E5vwqXNK` → SELF 0.977；USA SELF 0.93 因 `KPGvRMg1` 已是同 nu 同评分的克隆。
- **参数微调族无法再用**：HKG 备选池 8 颗（shortinterest 溢价族参数/门控微调）SELF 全 0.78–0.99；`truncation` 扫描在小宇宙上零影响。

---

## 4. 「S 越高越好」「加大生成量」= 无终局价值

- gate 通过率 49.7% 已不是瓶颈，**prod 68% 淘汰才是**；端到端成功率 **0.10%**。
- **勿加大 S2 吞吐**（89.7% 未消化 + 32% 未过门禁，再生成只加深积压）。
- **抬 IS 门槛不能降风险**：负 OS 比例恒 ~22%（IS 三桶均 20–22%），`corr(IS, OS) = +0.092`。
- 全库 19,567 条表达式**仅 5.7% 被回测** → **瓶颈是"选得准"不是"挖得多"**。

---

## 5. 已证伪的算子 / 端点 / 工具

### 算子（用了整批 ERROR/CANCELLED）

**幽灵算子 10 个**：`group_normalize` / `sigmoid` / `ts_decay_exp_window` / `ts_entropy` / `ts_max` / `ts_median` / `ts_min` / `ts_min_max_cps` / `ts_percentage` / `ts_skewness`；外加 **`negate`**（用 `multiply(-1, X)`）。

⚠ **论坛口径的幽灵算子列表不可信**：PPA 报告称 `ts_entropy`/`ts_skewness`/`s_log_1p` 是 ghost，但 94 赞原帖 T13 用 `signed_power(ts_entropy(f,144),0.618)` 自称已验证
→ **以本仓 `operators_verified.json`(103) + KB advisory 为准**。

**幽灵算子误标"已验证"**：`brain-datafield-exploration-general` 方法 5/6 自称「已验证」的 `ts_median` / `scale_down` 实测不存在 → **整批 CANCELLED**，一律用 `ts_mean` 替代。

### 端点（不要再去找）

| 用途 | 已证伪端点 | 正确替代 |
|---|---|---|
| VFT | `/users/self`、`/users/self/statistics`、`/users/self/activities/value-factor-trend`（均无或 404） | `GET /users/self/consultant` |
| 退役 alpha | `/alphas/{id}/retire`/`decommission`/`deactivate`/`withdraw`/`unsubmit`/`archive`/`hide`（全 404） | 打 `RETIRE_<YYYYMMDD>` 标签 |
| 配额 | `/alphas/submission-limit`、`/users/self/submission-limit`（404） | `tools/quota_status.py` |
| 相关性预检 | `POST /alphas/{id}/check`（405）、`recordsets/*`（404） | prod：`check_correlation`（只读 `GET correlations/prod`）；SELF：`check_self_correlation`。**不要用 POST submit 试探**——通过即真提交 |
| alpha 列表 | `GET /alphas`（405，无过滤有 1000 上限） | `GET /users/self/alphas` + status 翻页 |

### 失效引用

- `tracking/_submit_kit/_tower_map.py`、`_quota_now2.py` → 改用 `tools/campaign_intel.py pyramid` / `tools/quota_status.py`
- `create_multiSim`（**非真实工具**，6 处/3 文件）→ `create_multi_simulation`

### 失效候选 skill

| skill | 死因 |
|---|---|
| `field-quality` | 无入边，zip 实为目录，DEU 0 覆盖 |
| `news-sentiment` | 引用不存在的 `wqb research/settings/news-refresh-portfolio` CLI |
| `labs-data-analysis` | 无入边零产出 |
| `alpha-repair` | 仅配方，承接 optimization-v1 四节零命中、4 处悬空引用 |

- **hypothesis-first 是死路分支**：`data/hypothesis_catalog/` 仅 1~3 条（要求 ≥20）且**无生成器**，而 ra-pipeline 在模板挖尽时会自动路由进去 → 二选一：补生成器 or 摘掉该路由。
- **照抄 `wq-brain-ppa-mining` V9「突破版范式」必挂**——它本身就是加权混合（闸 5 block 项）却标为最佳参数。

---

## 6. 误判陷阱（会导致错误结论）

### 相关性

- **❌ 勿用 IS 层 checks 或 `GET /submit` 的 404 推断可提交性**（09-16 三颗误判"均可提交"，实际提交层全 FAIL）。
- **❌ 勿等 prod 端点**（不触发计算、单并发排队、高频 refresh 反效果）→ "**POST 即是验证**"。
- **❌ 勿信库内 prod 历史值**（三次实证过期：`le8Y68K2` 0.6929→0.9932、`3qX6wLJQ` 0.5171→0.9895、`6XjqLn3J` 0.6545→0.8803）。
- **❌ 勿用本地 PnL 互相关替代平台 prod**（`6XrJ5OvE` 本地 0.6732 vs 平台 0.996）。
- **❌ 勿用 SELF 低推断 PROD 能过**（两闸对象不同）；**❌ 勿用本地 SELF 判同族候选活**（对近期提交孪生体结构性失明）。
- **❌ 勿凭库内 prod 值判断可提交**：同一颗 alpha 在 `alphas` 与 `submit_ready` 两表 prod 冲突且常是 `alphas` 更旧
  → 按「现值低 = 已恢复」解读会**严重误判**。

### 塔级统计

- **❌ 不可用 `datasets.category` 推塔归属**（本地 KOR 47% ACTIVE 的 category=None，塔归属来自平台 pyramid 匹配）。
- **❌ 不可用 `date_submitted` 判提交**（全库仅 2.7% 非空）。
- **❌ 本地 `alphas` 表不能做塔级统计**，一律查平台 `get_pyramid_alphas`。

### 字段/数据集

- **❌ 不可用 DB `fields` 表判定字段存活**（幽灵字段 `change_6m_rating_revision` 在 fields 表仍标有效，实跑报 unknown 整批取消）→ 用 `validate_fields` 或实跑探针。
- **❌ 勿把"零竞争"当机会**：DEU `other699` users 0–1、coverage 0.506，best|S| 仅 0.48 → **users=0 只是"无人用"的弱先验**。
- **❌ 勿对已点亮塔的数据集优先投入**（浪费配额）；点塔优先 UNLIT/PARTIAL 差 1 颗的塔。
- **❌ 选区必须回落到 S1 字段级覆盖审计**：`recommend_datasets → campaign_intel s0-select` **不校验区域字段覆盖率**（DEU top3 字段级 coverage 全 0.0，同区他集 0.63–0.98）→ 否则烧 S2/S3 槽位。
- **幽灵字段 alpha 判死、不进候选池**（`mLjnnzKE`/`xAj77zlg`/`blj0mgPK`/`1Yw33mO6`）：提交层 `COMPILE_ERROR`，**不可提交**（旧 ledger 误记为"可提交但不可复现"）。
  → 判死要落在 `alphas` 表（`disposition='DEAD'` + `dead_reason='GHOST_FIELD…'`），打在 `submit_ready` 上静默影响 0 行。

### 语义归类（2026-09-28 两处误杀）

| # | 缺陷 | 实证代价 | 正解 |
|---|---|---|---|
| ① | `is_` / `_flag$` / `_code$` 用**未锚定子串**匹配 | `oth466_is_ebit_oper_q`（**Income Statement** EBIT，users=**248**）等 **39/177（22%）**被当布尔标志误杀，且被杀的恰是 users 最高的利润表核心字段 | 名字规则只留**无歧义强标识符**（gvkey/cusip/isin/exrate/currency_code/日期）；标志位改由**描述文**判定 |
| ② | 裸 `\bindicator\b` / `whether` 描述匹配 | model109 的 Bollinger Bands / **Altman Z-score** / Money Flow Index 等 **51/539** 被当布尔标志误杀 | 必须出现**显式布尔措辞**：`indicator denoting whether` / `equals 1` / `dummy variable` / `1 if … 0 otherwise`；裸名词不算 |

→ **字段语义判定不能只看名字**（缩写歧义：`is` = Income Statement vs `is_` 标志；`indicator` = 技术指标 vs 布尔指示）。

### 其他误判

- **❌ 勿用 `grep -rl` 计数做清理决策**（系统性高估引用，如 `mcp_config.json` 10 处"引用"全是指向 HOME 的同名文件）→ 用真路径核验。
- **❌ 勿把"零竞争"当机会**；**❌ `--inspect-mode enforce` 绝不能全局开**（fail-closed，会把缺包区每一波全拦死）。
- **❌ 干跑只能验证语法与计划，验证不了取值正确性**（`--apply` 后回读平台才发现标签错）。
- **❌ 审计必须直接调用被审计函数**，不能只读文档/只读 SQL；**任何"违规率"数字必须先用真闸/真解析器抽样校验**（13.3%→4.5%、76%→25%，两次都差 3 倍）。
- **❌ 报数前必须确认读的是对的键**（`s0_ranking` 读 `ranking` 而非 `datasets`，误判过 JPN/DEU 空排名）。
- **❌ forum 认证/环境故障 ≠ 论坛无解**：`tools/forum_recon.py` 曾把 `_live_session()` 异常直接落 `_record_negative`，而 SKILL 集成点把 `found=false` 当作「论坛无解」取证
  → **会把活路误判死**，且错误条目进 **7 天 TTL 缓存**被长期回放。正解：故障落 `found=None`/`status=error`（退出码 3 = 未取证，与 2 = 确认无解严格区分）、错误不进缓存、判死闸四态 fail-closed。
- **❌ 探测必须选"目标值 == 当前值"的字段**：把 `PATCH {"hidden": False}` 当幂等探测结果真改了状态（`kGzKZzl` True→False）。

---

## 7. 已证伪不必再试（清单）

| 对象 | 结论 |
|---|---|
| IND SA 同池重组 | 22 颗池 0.86–0.97，self_gate 0.5 仍 0.86，0.3 则组件不足 10 |
| IND `insiders1`（两波共 28 条） | 0 达标 |
| GBR `fundamental6` / `fundamental72` / `macro27` | 结构性无超额 / fast_kill |
| DEU `risk60` / `other699` / `option1` / `pv20` / `fundamental17` | 全灭 / 空集 |
| GLB EMOTION `ohlcv_img` 族 / `predicted_first_quantile_ten_day_return_*` | PROD 0.82–0.86 / 0.9989 墙 |
| 跨区 risk70（因子载荷） | 三区独立复现死族 |
| KOR fundamental17（202 条 / >10 种结构） | S 天花板锁死 ~1.30，判死 |
| 存量池参数微调抢救 | 236 条 IS 干净但双闸无一能过 |
| 加权混合任何形态 | 闸 5 block |
| 幽灵算子 / 幽灵字段 alpha | 整批 CANCELLED / COMPILE_ERROR |
