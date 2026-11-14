# ★★EAT 日历异象配方（DEU 专属，论坛 43184757918743）：earnings6 → S1.60 ATOM

> **这是本战役迄今最直接的可交付线索**（EARNINGS 塔未点亮 ⇒ 单数据集 ATOM，无禁混风险）。

## 一、最终配方（帖主生产级达标）

```
ts_min_max_cps(zscore(vec_sum(ern6_next_ed)), 380)
```

- 设置：DEU / TOP500 / delay1 / **decay 6** / **truncation 0.02** / **Neutralization = CROWDING** / pasteurization ON / unitHandling VERIFY；
- 平台指标：**S 1.60 / F 1.53 / TO 7.39% / Returns 11.40% / margin 30.85bp / DD 6.69%**；
- 算子数 **3**（vec_sum + zscore + ts_min_max_cps）。

## 二、机制（Johnson & So 2018 JFQA）

- **Earnings Announcement Timing 异象**：好消息早报（管理层提振股价）、坏消息迟报（用尽合规宽限期）；
- 欧洲（德国）披露排期弹性大 ⇒ 低拥挤度土壤；
- `ts_min_max_cps(x,d,f=2) = (ts_min(x,d)+ts_max(x,d)) - 2x`：
  排期严重拖延（x≈ts_max）→ 负 → 做空；排期大幅提前（x≈ts_min）→ 正 → 做多；
- 通用模板：`Alpha_Template = ts_min_max_cps(CS_Normalize(Vector_Agg(Event_Schedule_Field)), Lookback_Cycle)`；
  欧洲长周期披露建议 Lookback 360-400，美股 180-255。

## 三、三阶段演进（可复用的方法论）

| 阶段 | 变更 | S | F |
|---|---|---:|---:|
| V1 粗胚 | `ts_min_max_cps(vec_sum(ern6_next_ed),255)` | 0.85 | 0.70 |
| V2 截面提纯 | 前置 **zscore**（剔除财报季全市场排期群聚噪点，80%+ 个股同向刷新） | **1.56** | 1.44 |
| V3 周期校准 | 窗口 255→**380**（1 个日历年切在去年同期排期跳变边缘，边界噪点） | **1.60** | 1.53 |

**两条可迁移的规律**：
1. **事件日历类信号必须先做横截面 zscore**（消除季节性群聚），否则被宏观噪点淹没；
2. **窗口要跨自然年对齐**（欧洲半年报制度 ⇒ 1.5 年窗口 ≈ 5-6 个季度轮动）。

## 四、★对战役结论的修正

- 此前「earnings6 判死（S0.40，2014-2018 五年空窗）」**只针对 SUE 字段族**（earn6 实际/预期 EPS）；
  **日历排期字段 ern6_next_ed 是完全不同的机制**，且论坛实证 S1.60 ⇒
  **「字段族自测」纪律再次被验证：不能凭一个字段的判决封禁整个数据集**。
- 同时再次验证 **cov=0 ≠ 无数据**（earnings6 cov=0 却有数据；fnd90、risk72 同类）。

## 五、平台语法与闸门要点

1. `ts_min_max_cps(x, d, f=2)` 在 verifier 白名单内（alpha-expression-verifier/scripts/validator.py:159），**静态闸放行**；
   同族还有 `ts_min_max_diff(x,d,f=0.5)`；
2. MCP `preflight_expressions` 会把 ts_min_max_cps 误报为 unknown field（它自己的字段抽取不认这个算子）——
   **preflight 的 unknown 不等于平台不支持**；
3. **`nan_handling` 的合法值是 ON/OFF，没有 VERIFY**（Verify 是 unitHandling 的取值）——传 VERIFY 平台返回 HTTP 400 整批失败。

## 六、在飞验证（BE62 = WfCkM1PB4wKaL6AcZ76sKW，8 臂）

| 臂 | 变体 |
|---|---|
| 1 | 冠军复现 380 |
| 2 | 窗口 360 |
| 3 | 窗口 400 |
| 4 | 窗口 255（V2 对照） |
| 5 | 字段变体 ern6_4q（季度财报日） |
| 6 | 字段变体 ern6_board_of_directors_meeting（股东大会日） |
| 7 | 输入平滑 ts_mean22 |
| 8 | 外层 group_rank(sector) |

设置：decay 6 / trunc 0.02 / neutralization CROWDING / nan ON。

## 七、下一手（PEAD 快慢手线，帖子 43151941437463）

`alpha = ts_rank(ts_delta(ts_mean(F,10),1),20) - ts_rank(ts_delta(ts_mean(F,120),1),20)`
（F = 财报惊喜字段；decay 5；帖子称 FAST 中性化下 PC<0.7）
可用字段：ern6_actual_eps / ern6_estimated_eps / preliminary_eps_range_*（皆 VECTOR）。
## 八、★★BE62 结局：ts_min_max_cps 对本账号/本区域**不可用**（8/8 ERROR）

平台错误原文：`Attempted to use inaccessible or unknown operator "ts_min_max_cps"`。

- 这正是 toolkit `inaccessible_ops`（ts_min / ts_max 家族）在平台侧的镜像：**语法合法、verifier 白名单内，但平台侧拒绝**；
- 论坛帖作者的账号可用，我们的账号/DEU 区域不可用 ⇒ **EAT 极值偏离构造无法直接执行**；
- 教训：**论坛配方在复用前必须先用 1-2 臂最小探针验证算子可执行性**，不能整批 8 臂照抄（本次成本 = 1 个 multisim）。

## 九、替代路线：用可访问算子重建 EAT 机制（BE64 在飞）

- `ts_min_max_cps(x,d,f=2) = (ts_min+ts_max) − 2x` 的本质 = 「相对窗口极值中枢的偏离」；
- 可访问近似：`ts_zscore(x,d)`（相对窗口均值+波动的标准化偏离），保留帖子的两条方法论：
  ① **横截面 zscore 前置**（剔除财报季群聚噪点）；② **窗口跨自然年 360-400**；
- BE64 = 8 臂：窗口 252/360/380/504 + 快慢窗差 + 字段变体(4q / 股东大会日) + 分组轴。

## 十、平台语法第三坑

`nan_handling` 的合法值只有 **ON / OFF**，**没有 VERIFY**（Verify 是 unitHandling 的取值）——
传 nan_handling="VERIFY" 平台返回 HTTP 400 整批失败；本档案初版按帖子写的 Verify 也是错的（帖子自身标注可能有误）。