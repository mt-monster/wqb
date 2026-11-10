# DEU 战役关键纠正与第三席开波（2026-11-10）

## 一、重大纠正：mLovbnm2 撤回提交授权

### 新证据
DEU OS 池在 2026-11-09 新增一件此前未纳入视野的 ACTIVE：

- **rKRx2Alj**（`DEU_R_anlrev3_01`，dateSubmitted 2026-11-09T13:18:39-05:00）
- 表达式：`multiply(group_rank(ts_sum(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector), group_rank(ts_sum(netprofit_y1_estimate_change_3mo, 50), industry), group_rank(ts_sum(mean_estimate_change_pct_f12m_ebitda_90d_3, 30), industry))`
- 指标：S1.95 / F1.80 / 2Y2.23 / TO0.1401 / prod0.6561 / self0.5634

### 后果
mLovbnm2 与 rKRx2Alj 骨架几乎同构（仅 ts_mean vs ts_sum 之差）：

| 配对 | 互相关 |
|---|---:|
| mLovbnm2 ~ rKRx2Alj | **0.9966** |
| 1YNMAA8M ~ rKRx2Alj | 0.6946 |
| pwdLeeL6 ~ rKRx2Alj | 0.7008 |

**mLovbnm2 当前 self = 0.9966（阈值 0.7）⇒ 撞死，无法提交。**
此前台账记录的 self 0.5620 是 rKRx2Alj 提交**之前**的旧值，已失效。

**处置**：撤回 mLovbnm2 的提交授权与 submit_staging 文件；不得提交。

## 二、IS 池 24 颗硬闸候选 self 全量重算（本地计算，零平台槽）

方法：`check_self_correlation`（local_calculation，不占平台相关性队列），threshold=0.7，
correlation_type='self'（排除 Power Pool），池大小 16（OS 全池 19，排除 PPA 3）。

| 候选 | S | 2Y | self | 判定 |
|---|---:|---:|---:|---|
| **1YNMAA8M** | 1.58 | 2.13 | **0.6946** | **唯一 PASS** |
| pwdLeeL6 | 1.67 | 2.14 | 0.7008 | FAIL（差 0.0008） |
| 58EXddXN | 1.60 | 2.34 | 0.7187 | FAIL |
| O0A3j5vd | 1.59 | 2.06 | 0.7252 | FAIL |
| j2Y7GZJE | 1.58 | 2.25 | 0.7232 | FAIL |
| 1YNMRqxK | 1.62 | 2.21 | 0.7239 | FAIL |
| bl6w12gp | 1.67 | 2.14 | 0.7455 | FAIL |
| A1VA8YEY | 1.71 | 2.38 | 0.7427 | FAIL |
| mLovW2Nx | 1.75 | 2.40 | 0.7461 | FAIL |
| WjO5xv2k | 1.80 | 2.39 | 0.7394 | FAIL |
| qMLRwbOP | 1.71 | 2.33 | 0.7438 | FAIL |
| QPv8prAK | 1.70 | 2.34 | 0.7569 | FAIL |
| RREgwZo1 | 1.70 | 2.35 | 0.7517 | FAIL |
| RREgwqPd | 1.79 | 2.45 | 0.7387 | FAIL |
| leAmYEPA | 1.94 | 2.08 | 0.8598 | FAIL |
| LLMQ5wZL | 2.03 | 2.06 | 0.9735 | FAIL（深撞） |
| 9qxnE3W9 | 1.77 | 2.18 | 0.9708 | FAIL（深撞） |
| 78LporN2 | 1.96 | 2.10 | 0.9909 | FAIL（深撞） |
| vR1QObrQ | 1.87 | 2.20 | 0.9857 | FAIL（深撞） |
| vR1QOAwQ | 1.92 | 2.11 | 0.9812 | FAIL（深撞） |
| 0mYJjPq8 | 1.91 | 2.15 | 0.9920 | FAIL（深撞） |
| 9qxnElY1 | 1.95 | 2.12 | 0.9925 | FAIL（深撞） |
| RREgAeMj | 1.91 | 2.10 | 0.9926 | FAIL（深撞） |
| mLovbnm2 | 1.94 | 2.18 | 0.9966 | FAIL（深撞） |

### 结论（判据 DB）
**分析师修正三腿族已被 rKRx2Alj 整体锁死。** 同族改窗口/改轴/改第三腿都无法把 self 压到 0.7 以下
—— 因为 rKRx2Alj 用的是同字段同族结构，族内任何变体的相关度都在 0.70~0.99。
⇒ 第三席**必须换机制族**，不能继续在分析师修正族里穷举参数。

### 方法论要点（判据 DC）
`check_self_correlation` 是**本地**计算，不占平台相关性槽（平台 prod 队列单并发、
常有 correlation_busy / retry_after 240）。**任何自相关筛查都应先走本地工具全扫，
只对本地 PASS 的极少数再花平台槽测 prod。** 本轮 24 颗本地全扫仅耗时数分钟。

## 三、1YNMAA8M prod refresh 终验

- `check_correlation(refresh=True, correlation_type='production')` → **max_correlation 0.6951, PASS**
- 直方图：`[0.6,0.7]` 桶 n=2，无 `[0.7,0.8]` 深钉区 ⇒ 结构健康
- self（本地，当前 OS 池）0.6946 PASS
- 指标：S1.58 / F1.36 / 2Y2.13 / TO0.1337 / SU1.01 / failed_ra=0
- 状态：**当前唯一四闸全过、可提交的候选件**，但双闸余量各仅约 0.005，
  且与 rKRx2Alj 互相关 0.6946（贴线）⇒ 提交前必须再次 refresh 终验。

## 四、第三席开波：fundamental6 季度财报族

### 选族依据
1. goal 第 1 条明文：「切换到 Fundamental 下挖掘数据集逐一扫描」。
2. **fundamental 是 DEU 未点亮塔**（D1 计数 = 1，仅 Wje5K71x）。
3. OS 池先例证明 fundamental 有定价力且 prod 最干净：
   Wje5K71x S1.73 / prod**0.4305** / self0.1882 —— 全 OS 池 prod 最低。
4. OS 池还证伪了「DEU 只投分析师修正」这条旧准则：sentiment(bl6OWZ2M self0.031)、
   fundamental(Wje5K71x prod0.4305)、shortinterest(xArzm3Mn self0.264) 三族均已出货。

### fundamental 集供数盘点（字段画像 cov）
| 数据集 | 字段数 | DEU 供数 |
|---|---:|---|
| **fundamental6** | 197 | **cov 0.45~0.66 ✅ 唯一有数据** |
| fundamental1 | 124 | cov 全 0 ❌ |
| fundamental45 | 13 | cov 0.24~0.32 ❌（且被 Wje5K71x 口径外的语义） |
| fundamental72 | 1032 | cov 全 0 ❌ |
| fundamental86 | 8 | cov 全 0 ❌ |
| fundamental89 | 408 | cov 全 0 ❌ |
| fundamental90 | 67 | cov 全 0 ❌ |
| fundamental93 | 47 | cov 全 0 ❌ |
| fundamental22 | 2 | ❌ |

⇒ fundamental6 是 DEU 唯一有供数的 fundamental 集，197 字段（Compustat 季度/年度/半年）。

### 已派波次
- **Wave A（sim 1GUTfd45X4AX9gApqdYxOu9，COMPLETE）**
  10 条单字段 ts_delta 探针，全部 **S 0.23~1.04，ra_failed 3~4 闸**。
  结论：**单字段单窗口季度差分独立信号弱**（S 最高 d5WGMzZJ 仅 1.04，2Y 0.58）。
  ⇒ 必须走「双窗口加速度 × target_tvr_decay」结构（OS 已验证路线）。
- **Wave B（sim 2Bh3B46WQ4WkaR618dkc6WK4，ERROR/CANCELLED）**
  整批失败。原因：`fnd6_newq_revtq` 在 DEU 该 universe/delay 下不存在（preflight 只报 soft 警告，
  平台直接 CANCELLED 整批）—— **preflight 的 soft 警告必须当硬警告处理**。
- **Wave C（sim 8LgH62th4Vv8KC1exA7RgMs，已派出）**
  10 条照搬 Wje5K71x 已验证机制（`ts_target_tvr_decay(multiply(rank(ts_delta(f,240)),rank(ts_delta(f,176))),target_tvr=0.03)`）
  换字段/换窗口对/换轴展开；设置对齐：FAST 中性化 + nan ON + decay4 + trunc0.08。

### 字段级判据（判据 DD）
`fnd6_newq_revtq` 在 DEU TOP500/delay1 **不存在**；`fnd6_cptnewq_revtq` 存在（波 A 实测有数据）。
fundamental6 内 `newq_*`（季度）与 `cptnewq_*`（Compustat 季度）两族字段可用性不一致，
必须逐字段探针，不能靠命名推断。

## 五、平台/工具事实更新

- `lookINTO_SimError_message` 的参数名是 **`locations`**（复数数组），不是 `multisimulation_location`。
- `harvest_multisim_alphas` 返回的子 id 在 alpha 未生成前是 **simulation id**（404 on /alphas/{id}），
  必须等 status=COMPLETE 后再 harvest 一次才能拿到 alpha_id。
- MCP 客户端 session 不稳时，`search_forum_posts` 等工具会返回 `Error executing tool ...`
  （非 JSON）⇒ `mcp_call.ps1` 的 ConvertFrom-Json 会崩；此时改用直连 SSE 抓取原始 text。
- **静态闸拦整批**：一条表达式里混入西里尔字母（`fnd6_newq_invтq`）会让整批 10 条全部拒发。
  ⇒ 派发前必须本地扫非 ASCII 字符。

## 六、待用户裁定

1. **1YNMAA8M 提交授权**（当前唯一可提交件，双闸余量各 0.005，须 refresh 终验后再提交）。
   mLovbnm2 已撤回，不再需要授权。
2. **10 颗 vs 20 颗口径**：goal 标题写 20、第 4 条写 10。
   当前本战役新挖 3 颗（zq3eb7No / bl6AvMkN / 1YNMAA8M 待授权）。
3. **是否继续 DEU 深挖**：分析师修正族已封死；第三席走 fundamental6。
   若要继续往 10 颗走，需放开「不得换 region」过程约束（需用户修改 goal）。
