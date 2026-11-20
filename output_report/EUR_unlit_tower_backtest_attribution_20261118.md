# EUR 未点亮塔回测归因与对比实验（2026-11-18）

> 全程 EUR/D1/TOP2500/decay40/FAST/trunc0.08/nan ON/maxTrade ON（沿用已验证 N1NGbddg 档）。
> 机制模板：analyst7 修正广度强腿（EBI/EBT 科目）+ 未点亮塔小腿（1.2 权重 or 减法形式），
> 外层 `group_neutralize(..., market)` 保留幅度。all preflight_expressions PASS（无 unknown_fields）。

## 1. 批次账本（create_multi_simulation，并发上限 2）

| 批次 multisim_id | 机制 | 结果 |
|---|---|---|
| `3h2W8x5Ar4Vx9kuK3tdFwmr` | EBI 强腿 × 机构家数小腿 / EBI × insider 净买入小腿 | N1NGbddg ✅ / A1x7E3ae ✅ |
| `18WcVIh1f4ofcza1hC2WxlGs` | EBI × 机构市值流 / EBI × 机构股数流 | YPag967w ✅ / vRAvo8jA ✅(IS) |
| `12vc2J6Kb4gQ9xl15V2xctxl` | **DPS** 强腿 × 机构家数 / **GPS** 强腿 × 机构家数 | gJe50VQO ❌ S1.35/F0.76 / vRAvbwzG ❌ S1.44/F0.81 |
| `20XMei1G4rXa4x22ivr9mr` | **EBT updown** 强腿 × 机构家数 / × insider 净买入 | j2arKLJZ ⚠ 2Y1.58 边界 / LLKdYewm ✅(IS) |
| `1HqeAjeHq4xGbodzjWBOLSy` | EBI × socialmedia buzz / EBI × macro jobs | 6XMeWYa5 ❌ F0.99 / bladmWNN ❌ F0.98+sub |
| `230O1Rchv4nhayYixyxQxWh` | 同上但小腿权重 0.7（修 F） | 2r5NgWvY ✅(IS) / O0WxLVoq ✅(IS) |

## 2. 归因：为什么只有 EBI/EBT 强腿 + 家数/净买入小腿过闸

| 强腿科目 | 全期 S | 2Y | 判定 | 归因 |
|---|---:|---:|---|---|
| **EBI raisednum/num 4wks ago** | 1.69–2.22 | 2.17–2.29 | ✅ | 广度读数 + 2.1 次幂锐化头部，S/F/2Y 平衡最佳 |
| **EBT raisednum/(raised+lowered)** | 1.88–2.17 | 1.58–2.02 | ✅/⚠ | updown 比率读数，prod 更低但 2Y 在机构腿上贴线 |
| DPS raisednum/num | 1.35 | 1.58 | ❌ | S/F 三闸全败：DPS 修正事件稀疏，独立信号强度不足 |
| GPS raisednum/num | 1.44 | 1.25 | ❌ | 同上，且 2Y 崩 |

**小腿字段归因**（EBI 强腿固定，换小腿）：

| 小腿字段 | 塔 | S | F | 2Y | prod | 判定 |
|---|---|---:|---:|---:|---:|---|
| 机构家数不对称 (buyers−sellers)/holders | INSTITUTIONS | 1.69 | 1.05 | 2.17 | 0.6872 | ✅ |
| insider 净买入 ts_sum(top_buy−top_sell,63) | INSIDERS | 1.84 | 1.15 | 2.25 | 0.6604 | ✅ |
| 机构市值流 acquired−disposed / 总市值 | INSTITUTIONS | 1.73 | 1.07 | 2.29 | 0.6765 | ✅ |
| 机构股数流 acquired−disposed / 总股数 | INSTITUTIONS | 1.72 | 1.06 | 2.27 | 待测 | ✅(IS) |
| EBT updown × insider 净买入 | INSIDERS | 2.17 | 1.39 | 2.02 | 待测 | ✅(IS) |
| socialmedia buzz (@w0.7) | SOCIALMEDIA | 1.65 | 1.01 | 2.07 | 待测 | ✅(IS) |
| macro jobs active (@w0.7) | MACRO | 1.64 | 1.00 | 2.10 | 待测 | ✅(IS) |
| socialmedia buzz (@w1.0) | SOCIALMEDIA | 1.64 | 0.99 | 2.06 | — | ❌ F 0.99 擦边 |
| macro jobs active (@w1.0) | MACRO | 1.63 | 0.98 | 2.10 | — | ❌ F+sub 双败 |

**关键对比实验结论**：
1. **小腿权重 1.0→0.7 同时抬 F（0.99→1.01）与 sub（社交）/修 sub（宏观）** —— 降权让强腿稳定成分占比上升，与 EUR SOP §22「快腿降权抬 sub 比率」一致。
2. **换强腿科目（EBI→DPS/GPS）全灭** —— 不同科目的修正事件密度差异是主因，不是结构问题（与 SOP §8.1「科目天花板」一致）。
3. **EBT updown 读数 prod 天然更低**（updown 是比率，非广度），是破 prod 墙的备选强腿。

## 3. 淘汰记录（含外部证据）

- `news17/news46` 情绪极性分：本地历史 77 条 S<0.6，论坛取证（8 篇 BRAIN TIPS + 官方文档）确认关注度数（story_count）才是有效读数 → 本战役不碰极性分。
- `earnings6/socialmedia15/macro27-cov0.33`：coverage <0.85 或字段极薄，sub 闸结构性不可达 → 仅做小腿（vec_avg 聚合）不做主信号。
- `pv37` ATOM（O0WawXzg）：prod 0.578 ✅ 但 sub 0.80/limit 1.66 ❌（STATISTICAL 档高 S 不可交付）；与 `leaXWWx8`(rsk70) 正交但过不了自身 sub 闸 → 排除。

## 4. prod 取数阻塞记录（工程问题，非信号问题）

- 平台 prod 计算异步（1–5 分钟）+ 账号级单并发槽 + 本机 MCP 客户端 30s 硬上限 ⇒ check_correlation 多次 30s 超时；
- 连续 pending 触发账号级熔断（`correlation.unavailable.json`，600s 冷却）；已按 SOP §35 停止高频重试，等冷却后单进程串行重查。
- 已确认值（当日 MCP）：N1NGbddg 0.6872 / A1x7E3ae 0.6604 / YPag967w 0.6765 / e75x1vAl 0.5469 / 88Rx7beX 0.819❌ / d5WEm1LY 0.846❌（prod 漂移实例）/ O0WawXzg 0.578（sub 闸败）。
