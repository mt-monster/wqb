# KOR/D1 战役阶段性总结（2026-08-16，wave22→wave35 / P1→P67）

## 一、目标与进度

目标：3 个不同数据集、风格迥异、全门槛过、可提交的 REGULAR alpha。
当前进度：**1/3**（`WjAxxZVk` ACTIVE，multi_source_model，multiply(rank(ts_decay_linear(short_horizon_hedge3_quantile1_5d_pred,10)),rank(short_term_seasonal_quantile1_20d_pred))）。

## 二、数据集判决表

| 数据集 | 判决 | 依据 |
|---|---|---|
| multi_source_model | ✅ 出第1个alpha | WjAxxZVk ACTIVE |
| dl_riskfree_returns | 🔒 候选池封存 | 20+全门槛过冠军全撞PROD墙0.82-0.92；结构/设置/中性化三维穷尽 |
| model170/307/243/144/37、event_stock_model、other545、sentiment23、shortinterest6、news_sentiment_dl、global_seasonal_model、mmp_nlp_sentiment、analyst_consensus、model68、ai_equity_alpha(初攻) | ❌ 判弱 | sh<1.25 或多式负向 |
| insider_feats | ⏸ 暂挂 | PROD0.78地板/2y/tvr三墙，候选池保留 |
| other455 | 🎯 下一目标 | 1500字段未侦察 |

## 三、关键成果

1. **战役最强指标** O0GjWqeY（sh2.44，INDUSTRY d10）；**战役最强综合** O0Gj6PqJ（sh2.83/fit3.39/2y2.48/RN2.55/margin39.5bp/tvr9%/ra=0/CW PASS，PROD 0.8211 族史最低）。
2. dl_riskfree 冠军池 20+：vRNbj8ar(2.30)、3qpOod1P(2.17)、N1bGNeQe(2.07)、E5GMpmAP(2.01)、N1bGNMJw(1.93)、6XpQGjJK(2.71)、1YpRGXPJ(2.45)…全部 PROD>0.82 墙。
3. decay 梯度实验：d6→d10→d14 = 0.8587→0.8469→0.8379，渐近 ~0.83，边际递减。

## 四、效率复盘（哪些烧了配额、哪些高效）

**低效模式（已规避）**：
- 盲目多发同骨架变体 → 改为"结构×设置"二维矩阵定点投放；
- ERROR 批误判为限流反复重发 → 连坐机制破解后一次定位；
- 全量字段拉取（1500字段）超时 → 改窄 search + 分页容错（本次修复）。

**高效模式（固化）**：
- 先探针单式定生死，再批量放大；
- multiply(rank(5d),rank(20d)) 跨 horizon 组合：指标与 PROD 双改善（0.84→0.82）；
- 提交前签名预检（字段白名单+算子白名单）杜绝连坐；
- 每 wave 台账即时回写，判死即停不恋战。

## 五、已沉淀记忆（可复用经验清单）

| 记忆ID | 经验 |
|---|---|
| df1d0607 | 批内ERROR式连坐取消兄弟任务；lookINTO_SimError_message下钻 |
| 413532d8 | PROD墙结构性：墙极薄(>0.7仅5-20/7.9万)时设置空间无法突破 |
| c097335f | PROD真杠杆与二次中性化无效结论 |
| ab912b00 | multiply(rank,rank) CW安全骨架 |
| af08beb9 | 三层门槛v2（回填带/未攻清单盲区） |
| 5f3425f1 | 提交前签名预检规则 |
| 067001c1 | 右嵌套三腿add平台Bug |
| 96122a23 | data-fields搜索分页offset+limit>100→400，需优雅降级 |

## 六、核心教训（本段新增）

1. **字段名后缀不对称**：KOR dl_riskfree 中 label3 系列带 `_2`、label0 系列不带；`ts_av` 不存在用 `ts_mean`。→ 提交前必须 get_datafields 实测核对，不凭模式猜。
2. **CANCELLED ≠ 限流**：整批 CANCELLED 优先怀疑批内坏式连坐，用 lookINTO 下钻子任务 raw.message 定位。
3. **PROD 墙判别先于扩批**：先查该数据集已提交 alpha 的 PROD 分布（>0.7 的个数），墙厚（>0.7 很多）才有突破空间；墙薄直接判结构性，早撤。
4. **工具层容错是战役基建**：分页400/429/401 都应有降级路径，否则单次触雷浪费整轮排查时间。

## 七、下一步（按优先级）

1. other455 侦察（1500字段：类型分布/coverage/用户数）→ 探针定生死；
2. insider_feats 三墙复攻（PROD0.78 地板最接近 0.7）；
3. ai_equity_alpha 二轮（翻转/聚合变体）；
4. 候选池 20+ 冠军在 PROD 墙松动时（平台重算）复检。
