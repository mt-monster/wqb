# Power Pool Alpha（PPA）提交 · 论坛经验总结

> 触发：尝试用 MCP `submit_alpha` 提交 EUR PPA `A1G6QpOQ`(T10v_12_1) 被拦，遂搜论坛总结 PPA 提交真实规则。
> 搜索 `power pool` 命中 10 帖，精读 3 篇（EUR 提交失败 / 主题不匹配 / power pool 时间变更）。

## 一、论坛实证（逐帖）

### 帖1 ·「power pool alpha无法提交」(SL49683, EUR TOPCS1600, 0 评)
- 提问：warning 必须解决才能提交 pure power pool alpha 吗？`daily osmosis rank` 如何生成？`themes not match` 如何理解？
- 无回复（说明该坑社区也常答不上来）。

### 帖2 ·「Pure Power Pool submission does not match any Power Pool Theme.」(JY35270, 0 评, 3 评论) ★★★
- 现象：USA/EUR/ASI 的 alpha 提交都报 "does not match any Power Pool Theme"，前两天还能提交。
- **关键评论（SF94303）**："最近 ppa 做了区域限制，会轮动，今天开始是 glb"
  → **PPA 提交存在「轮动的区域主题」闸门**：只有当前活跃区域（如某天 GLB）的 PPA 能提交；非活跃区域的 alpha 提交即报主题不匹配。

### 帖3 ·「关于 Power pool 问题」(MY22315, 0 评, 1 评论)
- 提问：哪里看 power pool 时间变化表？
- **关键评论（KJ42842）**："右上角铃铛"
  → **Power Pool 主题/区域轮动变更通知在 WQ BRAIN 平台右上角铃铛（通知中心）查看**。

### 补充（搜索摘要可见）
- 「使用ChatGPT更新Power Pool Alpha描述」(FD69320, **61 赞**)：PPA 提交必须填 idea/数据字段/操作符 三段英文描述，用 ChatGPT 辅助可提升质量与通过率。
- 「Power Pool Competition拿奖…USA D1 Fast Dataset Power Pool 拿到第二」(XW90844)：Power Pool 按 **Competition/赛季** 组织，主题（GLB / USA D1 Fast / …）随赛季轮动，数据可从 `api.worldquantbrain.com/competitions/consultant/boards/power-pool` 取。
- 「power pool现在真是有点滥用了」(QQ68782, 27 赞)：筛选后 `not in power pool` 大幅减少 → 印证 PPA 池有严格准入/轮动。

## 二、核心经验教训（6 条）

1. **【最致命】PPA 提交有「轮动区域主题」闸门。** 平台按赛季把 Power Pool 开放给某一区域/主题（如今天 GLB），只有该活跃主题的 PPA 才能提交。EUR/USA/ASI 的 alpha 在非对应窗口提交必报 "does not match any Power Pool Theme"。→ 提交前必须先确认**当前活跃主题是否含你的区域**。

2. **"does not match any Power Pool Theme" 的根因 = 区域/主题不在当前窗口。** 不是 alpha 表达式错，而是时序/区域不匹配。前两天能提交、今天不能，正是因为主题轮动了。

3. **主题轮动通知看平台「右上角铃铛」。** 没有公开的静态"时间表"，变更通过站内通知推送；也可从 Competition board API 推断当前赛季主题。

4. **PPA 描述三段是硬性要求**（idea / 数据字段 / 操作符），建议用 ChatGPT 生成（61 赞帖最佳实践）。我们已对 `A1G6QpOQ` 通过 `set_alpha_properties` 预置 `descriptions` 三段英文 + `tags=["PowerPoolSelected"]` + `color=GREEN`。

5. **PPA 闸门 ≠ 常规 alpha 闸门，且 MCP `submit_alpha` 工具只认常规闸门。**
   - 平台侧 PPA 准入（较宽）：Sharpe≥1.0、算子≤8、字段≤3、PC<0.5（来自前期 templates 报告）。
   - 但 MCP `submit_alpha` 实测套用**常规 RA 闸门**：Sharpe>1.3 / Fitness>0.75 / Margin>15bp，对合法 PPA 也照拦，**且打 PowerPoolSelected 标签后仍不切换** → **MCP 通道无法提交任何 Sharpe<1.3 的 PPA**。

6. **Power Pool 以 Competition/赛季组织，主题随赛季轮动**（GLB、USA D1 Fast 等），leaderboard 与顾问界面同入口。

## 三、对我们 T10v_12_1(A1G6QpOQ, EUR) 的修正结论

之前给的 3 个选项需修正——**即使走 web UI，EUR PPA 也只在「EUR 是当期活跃 Power Pool 主题」时才能提交**：

- 现状：`ppa_failed=false`（合规 PPA）、本地 powerpool 自相关 0.0（过）、描述/标签已预置。
- 阻碍链：① MCP `submit_alpha` 常规闸门拦（Sharpe1.14<1.3）；② 即便换 web UI，**若当期活跃主题不是 EUR**（如恰为 GLB），仍会报 "does not match any Power Pool Theme"。
- 因此提交成功的两前提：**(a) 区域闸门达标（Sharpe/Margin 过常规 MCP 闸 或 走 web UI）；(b) EUR 处于当期 Power Pool 活跃主题窗口**。

## 四、行动建议

1. **先看铃铛确认当期 Power Pool 主题**：登录 WQ BRAIN → 右上角铃铛，确认当前是否开放 EUR（或 GLB 等含 EUR 的主题）。
2. **若 EUR 当期开放**：
   - 最简：web UI 直接提交 `A1G6QpOQ`（已预置 PPA 属性）。
   - 若想走 MCP：需先把 Sharpe→1.3+/Fit→0.75+/Margin→15bp+（Margin 最难，~2.6×）。
3. **若 EUR 当期未开放**：等轮动到 EUR 窗口再提交；或转挖**当期主题区域**（如 GLB）的 PPA。
4. **凑齐 3 个去相关 PPA**：同主题窗口内，用 T10 期限结构族扫 decay/中性化，或换当期主题区域数据集（如 news_sentiment_nlp）补另外 2 族。

## 五、待办
- [ ] 查平台铃铛确认当期 Power Pool 活跃主题/区域。
- [ ] 据主题窗口决定：web UI 提交 / 强化至过 MCP 闸门 / 转挖当期主题区域 PPA。
- [ ] 更新 `wq-brain-ppa-mining` skill：补「轮动区域主题闸门」与「MCP submit_alpha 非 PPA 感知」两条铁律。
