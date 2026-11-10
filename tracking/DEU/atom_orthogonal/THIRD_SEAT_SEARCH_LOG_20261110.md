# DEU 第三席寻觅全日志（2026-11-10 下午）

> 目标：在 DEU 域内找到第三席（除已提交 2 颗 + 待授权 1 颗外）。
> 约束：CV 闸维持 0.60（不放宽）⇒ E569ZE7L 本轮不出货；region 固定 DEU；
> 禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL} 内部禁两两混合。

---

## 一、已出货可交付件（回顾）

| # | id | 族 | 状态 |
|---|---|---|---|
| 1 | zq3eb7No | analyst7（afs 水平修正） | ✅ ACTIVE |
| 2 | bl6AvMkN | analyst_factor_signals + predictive_starmine | ✅ ACTIVE |
| 3 | 1YNMAA8M | analyst7 + analyst15（全 sector 轴） | 🟡 四闸全过，待授权 |
| — | E569ZE7L | shortinterest3（借券需求加速度反转） | 🟡 四闸全过，CV 0.626 超线 ⇒ 本轮不出货 |
| — | mLovbnm2 | analyst7 三腿 | ❌ **已撤回**（与 rKRx2Alj 互相关 0.9966） |

---

## 二、第三席寻觅路径（14 波 / 约 135 条）

### 路径 A：fundamental6 季度财报族（goal 第 1 条指定方向）—— ❌ 封盘

| 波 | 内容 | 结果 |
|---|---|---|
| A | 单字段单窗口 ts_delta ×10 | 全灭 S 0.23~1.04 |
| B | 混合结构 | 整批 ERROR（fnd6_newq_revtq DEU 不存在） |
| C | 双窗口加速度 × target_tvr_decay ×10 | vR1QQ9ja S1.62 四闸，**prod 0.9389 深钉** |
| E | 参数族（换窗/换轴/换字段）×10 | YP1ee5zA S1.72 四闸，**prod 0.9728 深钉** |
| G | **换 8 个字段**（saleq/piq/ibq/ibmiiq/cheq/atq/seqq/cogsq）×10 | **全灭 S ≤ 1.23** |

**封盘归因**：信号高度集中在 `fnd6_newq_oiadpq`（营业利润-折旧后）；换字段后强度崩溃；
而 oiadpq + 240/176 组合已被 OS 池 Wje5K71x 占据（prod 0.9389 / 0.9728 深钉）。
论坛侧证：「fundamental被overused了」（21 赞）。

### 路径 B：shortinterest3 借券族 —— ✅ 机制成立但 CV 超线

| 波 | 内容 | 结果 |
|---|---|---|
| D | 借券**正向** ×10 | **全负**（-0.92~-1.59）⇒ 方向反了 |
| F | **符号翻转** ×10 | 出货 2 颗 |
| H | + ts_backfill 修 CW + 换轴 ×10 | 出货 j2Y7qlA5 S1.65 四闸（prod 0.5788） |
| I | 参数展开 ×10 | 出货 3 颗 |
| J | 稳健性修复变体 ×10 | 出货 3 颗（kqNAz9pP / 1YNMr08m / 9qxnNkeq） |
| K | 长窗对穷举 ×10 | 出货 E569ZE7L S1.68 四闸（prod 0.5444，CV 最优 0.626） |
| L | 精细窗口扫描 ×10 | 出货 7 颗（GrWZqQaJ S1.76 / wpQ08Nqx S1.74 …） |

**族容量终判**：族内 8+ 颗四闸全过，但彼此互相关 **0.758~0.901** ⇒ **该族最多出 1 席**。

**经济机制**：借券需求（borrow demand）抬升 = 做空/对冲需求拥挤 ⇒ 后续反转 ⇒ 做空借券需求抬升股。
学术支撑：Lou & Polk 2018 comomentum；short-interest skew 拥挤早期预警。

### 路径 C：sentiment / attention 族 —— ❌ 强度与覆盖不可兼得

| 波 | 内容 | 结果 |
|---|---|---|
| M | sentiment27（Tranco）单腿 ×10 | 全灭，符号混乱（真噪声） |
| O | snt7（Wikipedia）单腿 ×8 | 全灭 S ≤ 0.77，符号混乱 |
| P | snt7 × snl27 双腿 vector_neut ×8 | S 1.12~1.22（结构有效，强度不足） |
| Q | 波 P + ts_ir 窗口 22→33 ×8 | **wpQ0prQY S1.78 四闸全过**，但 2014-2018 空窗 + self 0.7412 ⇒ 判死 |
| R | 覆盖探针（snl27 单腿 5 条） | snl27 longCount 155~157（满覆盖）⇒ **空窗根因 = snt7 起始年 2019** |
| S | snl27 内部双腿 ×10 | 全负（S -0.19~-0.67）⇒ 方向反 |
| T | 符号翻转 ×10 | 全正但弱（S 0.11~0.67）⇒ 强度不足 |

### 路径 D：news / risk 族 —— ❌ 判死

| 波 | 内容 | 结果 |
|---|---|---|
| N | news104 + risk60 ×10 | 全灭 S ≤ 0.60，符号混乱 |
| V | news50 面板型字段（mws50_vea 91日事件量 / ess / ens …）×10 | 全灭 S -0.42~+0.23，符号混乱；**longCount 161~221 覆盖好 ⇒ 排除覆盖因素，信号本身无效** |
| U | news18 独特字段（analyst_recommendation_change / days_since_similar_event …）×10 | 收批中 |

---

## 三、本轮沉淀的判据（全部写入 Agent Memory）

| 编号 | 判据 | 要点 |
|---|---|---|
| DB | OS 池漂移使旧 self 结论失效 | 发现 OS 新增件须立即重扫待提交清单 |
| DC | 自相关筛查走本地工具全扫 | `check_self_correlation` 零平台槽，24 颗数分钟 |
| DD | 族被自己人锁死时穷举参数无效功 | 族内变体 self 全 ≥0.7 ⇒ 结构性封盘 |
| DE | 「族内只投 X」准则要用 OS 池实证推翻 | 不得凭本轮临时结论固化规则 |
| DF | preflight 的 soft 警告当硬警告 | 否则整批 CANCELLED |
| DG | 子 alpha id 在完成前是 simulation id | `lookINTO_SimError_message` 参数名是 `locations`（复数） |
| MG | 族级判死看符号一致性 | 全正=强度不足 / **全负=方向反（翻转重测）** / 混合=真噪声 |
| MH | 同机制已有出货源时新源直接判死 | risk60 vs shortinterest3 |
| MI | 事件型数据须先 backfill 转面板 | cov 高 ≠ 可用（news104 cov 0.963 全灭） |
| MJ | **覆盖空窗根因 = 数据源起始年** | ts_backfill 造不出历史；多腿一腿晚则整件空窗 |
| MK | 复刻已出货骨架不要拆腿单测 | 腿间正交化贡献大部分信号（S 0.77→1.22） |
| ML | attention 类数据强度与覆盖可能不可兼得 | snt7 强但 2019 起；snl27 弱但满覆盖 |
| MM | 族内候选排序完整判据链 | 覆盖 → 硬闸 → self → 族内互相关 → prod |

---

## 四、当前状态与下一步

**可交付**：3 颗（2 颗已 ACTIVE + 1 颗 1YNMAA8M 待授权）。
**待授权**：1YNMAA8M（prod refresh 0.6951 PASS / self 0.6946 / 18-19 独立集 / ΔS+0.43 / submit_gate passed）。
**备用**：E569ZE7L（借券族代表，四闸全过 + 满覆盖 + 无负年，**仅 CV 0.626 超线 0.60**）。

**未测完的候选方向**：
- news20 / news38（news 塔仍 0 颗）
- other47 / other532（OTHER 禁混集合内，仅可与集合外组腿）
- pattern_scores（504 字段 cov 1.0，伪预测型风险）
- 内置价格字段（close/open/high/low/vwap/returns/adv20 不属任何数据集）—— 纯价格机制不绑数据集

**约束提醒**：DEU 域内要往 10 颗走，必须放开「不得换 region」过程约束（goal 明文，需用户修改）。
