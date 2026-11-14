# GBR REGULAR Alpha 交付清单 v2（2026-11-14 campaign2 · 未点亮塔深挖轮）

**Region**: GBR · **Universe**: TOP700 · **Delay**: 1 · 用户口径：只挖 D1 未点亮塔类别主腿；已亮塔可作从腿；挖到六维证伪为止，不放宽约束凑数。
**本轮结果**：**新增交付 0 颗**；earnings6 与 order_book_imbalance 双主线六维证伪收口（PROVISIONAL 判死，带复活条件）。**既有篮子（8 颗，见 v1 manifest）仍是本区在约束下的全部可交付资产**。目标 20 颗在 GBR D1 未点亮塔约束下**确认知竭**（证据链见下）。

---

## 一、本轮波次总表（7 批 multisim × 8 臂 = 55 有效臂 + 1 平台拒）

| Wave | 数据集 | 批 | 机制面 | 结果 |
|---|---|---|---|---|
| W1 | earnings6 | 1（8臂） | SUE 纯 ATOM × 短窗结构（论坛半衰期假设） | 全灭（最高 0.68）；**短窗假设证伪** |
| W1 | earnings6 | 2（8臂） | SUE×久期腿（换腿解 self 假设）+ 纯 SUE 252d | 久期腿 0.31-0.41 证伪；纯腿 SUBINDUSTRY 反号 -0.65 |
| W1 | earnings6 | 3（8臂） | FAST 档复刻 × 轴变体 | **6/8 全闸（S 1.72-1.74，ra=0）**但 self 0.77-0.82 全撞 3qoGxkqZ |
| W1 | earnings6 | 4（8臂） | FAST 纯 SUE + 权重梯度 5:1/3:1 | 纯腿全灭（-0.44~-0.96）；权重×2.5 只降 self 0.004 |
| W2 | order_book | 5（8臂） | 暗池/碎片化份额比（dark/lit/bilateral/nonaddr） | 全灭（最高 0.50） |
| W2 | order_book | 6（8臂） | auction 价格族（竞价错位 bps）+ spread 族 | 全灭（最高 0.57） |
| W2 | order_book | 7（7臂+1拒） | 深度微观结构（fill_prob/rest_time/duration/EBBO 比率） | 全灭（最高 0.52）；notional 量纲陷阱 1 例 |

## 二、两个 PROVISIONAL 判死档案（六维举证全文见波次档案）

### earnings6（earnings 塔 0/3）
- **活机制唯一**：SUE(`actual−estimated`)×loaned 借券腿 @FAST/decay5/trunc0.1——IS 全闸（本轮复现 6 臂 S1.70-1.74/F1.05-1.10/2Y2.69-2.80/ra=0）。
- **双墙钉死**：self 地板 **0.7709-0.8211**（OS 池 `3qoGxkqZ` = pv103 主腿 + **同一条 loaned 腿**；权重 5:1 也不动）+ prod **0.8517**（refresh 实测）。换 industry/subindustry 轴无效（借券腿主导 PnL）、久期腿替换无效（0.31-0.41）、纯 SUE 任何档位反号。
- **复活条件**：OS 池 3qoGxkqZ 退役，或出现非 loaned 的合格从腿。
- **附带更正**：11-04 报告「earnings6 五年空窗」结论**已推翻**——`2rAo7mm8` 十年逐年全正无空窗（2014 lc430 起）；空窗只属于 `P0gbMLz7` 那条 divide 分母近零的特定表达式。

### order_book_imbalance（other 塔 2/3）
- **四字段族结构性封顶**：trade 分类 0.56 / 份额比 0.50 / auction+spread 0.57 / 微观结构 0.52——正反双向对称 ⇒ 与 analyst47 同型的封顶签名（读数信息量到位即封顶）。距 1.58 闸差 1.0+。
- 六维举证：≥30 有效结构、四大族全覆盖、矩全家、三轴、双向对照、双配置档（+11-11 四档）。判死范围 = 单集 ATOM 形态；跨塔组合腿未测（受 ≤5 配额约束让位）。

## 三、容量结论（对齐 v1 的如实说明）

- 前轮（11-08 普查 + 11-13/14 波次）已把 D1 九座未点亮塔 28 集 + other 塔重点集全部探针收口；本轮补齐了最后两个「未穷尽」标注（order_book 226 未测字段、ern6 复活路径），全部六维证伪。
- **GBR D1 未点亮塔在本轮约束（S≥1.58 + F≥1.0 + 2Y 分档 + self/prod<0.7 + 不换区）下的可交付增量 = 0**。既有 8 颗篮子（v1 manifest）就是当前约束下的全部。
- 剩余理论空间（均超出本轮口径，需用户另行拍板）：① D0 面（73 集全塔未点亮、28 真未探——用户已裁定本轮只考虑 D1）；② 跨塔组合腿配额放宽；③ OS 池借券腿占位退役后的 ern6 复活。

## 四、字段画像存档索引（本轮新增/更新）

| 文件 | 内容 |
|---|---|
| [tracking/GBR/reference/gbr_order_book_imbalance_fields.json](../../tracking/GBR/reference/gbr_order_book_imbalance_fields.json) | **新建**：240 字段全目录实拉（MCP get_datafields 全量），42 代表字段按 10 字段族归并，覆盖三档（0.4294/0.2028/0.1644-0.1671）+ 机制适用性标注 |
| [tracking/GBR/reference/gbr_earnings6_fields.json](../../tracking/GBR/reference/gbr_earnings6_fields.json) | 沿用（18 字段，本轮复核 type/cov/ac 无变化） |
| [data/dataset_assets/GBR_C2_self.json](../../data/dataset_assets/GBR_C2_self.json) / [GBR_C2_prod.json](../../data/dataset_assets/GBR_C2_prod.json) | 本轮 self/prod 快照（沿用 GBR_<批>_self/prod.json 命名惯例） |
| [reports/dataset_experience/gbr_unlit_campaign2_survey_20261114.md](gbr_unlit_campaign2_survey_20261114.md) | 本轮选集 survey（候选清单/排除表/审计门结论） |
| [tracking/GBR/waves/gb_campaign2_waves_20261114.md](../../tracking/GBR/waves/gb_campaign2_waves_20261114.md) | 本轮波次全档案（7 批读数+归因+六维举证） |
| [data/dataset_assets/GBR_coverage_audit_d1.json](../../data/dataset_assets/GBR_coverage_audit_d1.json) + [gbr_coverage_audit_20261114.md](gbr_coverage_audit_20261114.md) | 本轮覆盖审计门缓存与报告（177 集实拉，可开采池 65，真未探 0） |

## 五、调优经验摘要（本轮新增，跨区可复用）

1. **SUE 是配置层信号**：同表达式 SUBINDUSTRY -0.65 ↔ FAST +1.74（2.4 S 摆幅）；纯腿任何档位反号 ⇒ earnings 意外族在 GBR 的溢价只在「借券腿×FAST」组合里存在。
2. **self 墙归因三步法**：查 top_correlated 的 OS 件表达式 → 找共享腿 → 权重梯度测地板。本轮权重 2:1→5:1 只降 self 0.004 ⇒ 地板由共享腿钉死，参数不可达，立即停（不再扫结构）。
3. **论坛配方跨集不可移植**：「SUE 半衰期短窗」建议（USA earnings1 系实证）在 GBR ern6 稀疏事件 VECTOR 上反向毁灭（-0.36~-0.96）；窗口假设必须按字段更新频率重推。
4. **结构性封顶签名（收口判据）**：多字段族 × 多几何 × 双向全部收口在同一 S 区间（0.44-0.57）⇒ 读数信息量封顶，继续投入的期望产出为 0——比逐族判死快 3-4 批。
5. **notional 字段量纲陷阱**：`*_notional_value` 是 Unit[CSPrice]，与标量 add 会整批 WARNING 拒（本轮 1 臂）。
6. **判死档案的「复活条件」字段**：本轮两个判死都写了精确复活条件（OS 退役 / 新从腿出现），避免下轮 agent 重复投入时重踩。
