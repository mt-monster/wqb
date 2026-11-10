# DEU 战役交付更新（2026-11-10 上午）

> 本轮在既有 125 波基础上新增 **Wave A~L 共 11 波 / 110 条回测**，
> 解决两件事：①纠正一张已失效的提交授权 ②开出第三席（新机制族）。

---

## 一、交付件总表（本战役新挖）

| # | alpha_id | 数据集 | 塔 | 状态 | S | F | 2Y | TO | self | prod | 备注 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `zq3eb7No` | analyst7 | ANALYST | ✅ **ACTIVE**（用户已提交） | 2.01 | 1.28 | 1.64 | 0.2262 | 0.3641 | 0.6171 | afs 水平修正 |
| 2 | `bl6AvMkN` | analyst_factor_signals + predictive_starmine | MODEL+ANALYST | ✅ **ACTIVE**（用户已提交） | 1.61 | 1.36 | 2.15 | 0.1097 | 0.5137 | 0.6470 | afs+starmine |
| 3 | `1YNMAA8M` | analyst7 + analyst15 | MODEL+ANALYST | 🟡 **四闸全过，待授权** | 1.58 | 1.36 | 2.13 | 0.1337 | 0.6946 | 0.6951 | 全 sector 轴 + 跨源 |
| 4 | `E569ZE7L` | shortinterest3 | SHORTINTEREST | 🟡 **四闸全过 + CV 待裁定** | 1.68 | 1.21 | 2.27 | 0.1128 | 0.5444 | 0.5444 | 借券需求加速度反转 |

**⚠ 已撤回**：`mLovbnm2`（详见下节）—— 不得提交。

### 交付篮子正交性（threshold 0.7，19 颗全算）

`compute_mutual_correlation` → `all_below_threshold = true`，`max_mutually_below_subset_size = 19`

| 配对 | 互相关 |
|---|---:|
| 1YNMAA8M ~ E569ZE7L | **0.1227** |
| 1YNMAA8M ~ rKRx2Alj | 0.6946（最高） |
| E569ZE7L ~ xArzm3Mn | 0.5444（最高） |
| 1YNMAA8M ~ bl6AvMkN | 0.5128 |
| 1YNMAA8M ~ zq3eb7No | 0.2471 |
| E569ZE7L ~ Wje5K71x | 0.0411 |
| E569ZE7L ~ 2rmGAPqN | 0.0436 |

⇒ 三件新挖件 + 已提交件构成**完整独立集**，无相关超标。

---

## 二、★ 关键纠正：mLovbnm2 撤回提交授权

### 新证据
DEU OS 池在 **2026-11-09** 新增一件此前未纳入视野的 ACTIVE：

- **`rKRx2Alj`**（`DEU_R_anlrev3_01`，dateSubmitted 2026-11-09T13:18:39-05:00）
- 表达式：`multiply(group_rank(ts_sum(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector), group_rank(ts_sum(netprofit_y1_estimate_change_3mo, 50), industry), group_rank(ts_sum(mean_estimate_change_pct_f12m_ebitda_90d_3, 30), industry))`
- 指标：S1.95 / F1.80 / 2Y2.23 / TO0.1401 / prod0.6561 / self0.5634

### 后果

| 配对 | 互相关 |
|---|---:|
| **mLovbnm2 ~ rKRx2Alj** | **0.9966** |
| 1YNMAA8M ~ rKRx2Alj | 0.6946 |
| pwdLeeL6 ~ rKRx2Alj | 0.7008 |

**mLovbnm2 当前 self = 0.9966（阈值 0.7）⇒ 撞死，平台 Self Correlation 闸必然拦截。**
此前台账记录的 self 0.5620 是 rKRx2Alj 提交**之前**的旧值，已失效。

**处置**：`submit_staging_mLovbnm2.json` 已改写为 `STATUS: WITHDRAWN_DO_NOT_SUBMIT`，并记录碰撞详情。

### 连带结论：分析师修正三腿族结构性封死

IS 池 24 颗硬闸候选 self 全量重算（本地计算，零平台槽）：

| 区间 | 候选 | 结论 |
|---|---|---|
| PASS | 1YNMAA8M (0.6946) | 唯一存活 |
| 0.7008~0.7569 | pwdLeeL6 / 58EXddXN / O0A3j5vd / j2Y7GZJE / 1YNMRqxK / bl6w12gp / A1VA8YEY / mLovW2Nx / WjO5xv2k / qMLRwbOP / QPv8prAK / RREgwZo1 / RREgwqPd | 全超线 |
| 0.8598~0.9966 | leAmYEPA / LLMQ5wZL / 9qxnE3W9 / 78LporN2 / vR1QObrQ / vR1QOAwQ / 0mYJjPq8 / 9qxnElY1 / RREgAeMj / mLovbnm2 | 深撞 |

⇒ 族内改窗口 / 改轴 / 改第三腿字段 / 改第三腿数据集**全部无效**，
因为同族变体与族内既有件的相关度天然在 0.70~0.99。**必须换机制族**。

---

## 三、第三席：借券需求加速度反转（shortinterest3）

### 3.1 选族依据
1. goal 第 1 条明文指定「切换到 Fundamental 下挖掘数据集」⇒ 启动 fundamental 方向。
2. **fundamental 是 DEU 未点亮塔**（D1 计数 = 1，仅 Wje5K71x）。
3. OS 池先例：Wje5K71x S1.73 / prod **0.4305**（全池最低）/ self 0.188 ⇒ fundamental 有定价力且 prod 干净。
4. 论坛「fundamental被overused了」（21 赞）侧证生产池 fundamental 已拥挤。
5. OS 池证伪了旧准则「DEU 只投分析师修正」：sentiment / fundamental / shortinterest / institutions 四族均已出货。

### 3.2 fundamental6 方向的结论（封盘）

| 数据集 | 字段数 | DEU 供数 |
|---|---:|---|
| **fundamental6** | 197 | **cov 0.45~0.66 ✅ 唯一有数据** |
| fundamental1 / 45 / 72 / 86 / 89 / 90 / 93 | 124/13/1032/8/408/67/47 | cov 全 0 ❌ |

fundamental6 三波结果：
- **Wave A（单字段单窗口 ts_delta，10 条）**：全灭，S 0.23~1.04 ⇒ 单字段单窗口季度差分无效。
- **Wave C/E（双窗口加速度 × target_tvr_decay）**：
  - `vR1QQ9ja` S1.62 / F1.21 / 2Y2.03 / self0.3157 ✅ 四闸，**prod 0.9389 深钉**
  - `YP1ee5zA` S1.72 / F1.37 / 2Y1.71 / self0.3538 ✅ 四闸，**prod 0.9728 深钉**
  - 两件的深钉源 = 与 OS 池 Wje5K71x **同字段 `fnd6_newq_oiadpq` 同窗口对 240/176**。
- **Wave G（换 8 个字段：saleq/piq/ibq/ibmiiq/cheq/atq/seqq/cogsq）**：**全灭，S ≤ 1.23**
  ⇒ 信号高度集中 oiadpq 字段，该字段本身已被生产池占据 ⇒ **fundamental6 第三席封盘**。

### 3.3 shortinterest3 方向的突破

**归因转折点**：Wave D 10 条**全部负 Sharpe**（-0.92 ~ -1.59）—— 不是「无信号」而是**符号方向反了**。
翻转符号后（Wave F/H/I/K/L）出货 **11+ 颗四闸全过**。

**经济含义**：借券需求（borrow demand）抬升 = 做空/对冲需求拥挤 ⇒ 后续反转 ⇒ **做空借券需求抬升股**。

**可交付骨架（跨族通用）**：
```
-group_rank(
  ts_target_tvr_decay(
    multiply(
      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 264)),
      rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 132))
    ),
    target_tvr=0.03
  ),
  subindustry
)
```
设置：DEU / TOP500 / delay1 / decay4 / **neutralization FAST** / trunc 0.08 / nanHandling **ON** / maxTrade OFF / 10 算子

**CW 闸正解**：`ts_backfill(vec_avg(...), 132)` 把稀疏借券事件填稠密
⇒ CONCENTRATED_WEIGHT 从 FAIL 变 PASS，**且 S 不降反升**（1.59 → 1.65/1.68）。

### 3.4 候选排序（族内 8+ 颗四闸全过）

| 候选 | 窗口对/轴 | S | 2Y | 10y CV | 3y CV | 负年 | prod | self |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **E569ZE7L** | 264/132 sub | **1.68** | 2.27 | **0.507** | **0.626** | **0** | 0.5444 | 0.5444 |
| GrWZqQaJ | 264/154 sub | 1.76 | 2.77 | 0.538 | 0.640 | 0 | — | — |
| 9qxnNkeq | 264/88 sub | 1.66 | 2.69 | 0.618 | 0.665 | 0 | 0.5327 | 0.5327 |
| 1YNrqG9X | 264/132 sub tvr.04 | 1.72 | 2.28 | 0.530 | 0.680 | 0 | — | — |
| wpQ08Nqx | 264/132 sector | 1.74 | 2.63 | 0.587 | 0.791 | 0 | — | — |
| E56d9xnP | 66/44 market | 1.56 | 3.10 | 0.737 | 1.112 | 1 | — | 0.4228 |
| j2Y7qlA5 | 132/88 sub | 1.65 | 2.72 | 0.663 | 1.035 | 1 | 0.5788 | 0.5788 |
| pwd9qYlq | 132/88 sector | 1.59 | 2.90 | 0.704 | 0.869 | 0 | — | 0.5239 |
| qMLQK9lZ | 66/44 sub | 1.63 | 3.03 | 0.689 | 1.107 | 1 | — | 0.5620 |

**E569ZE7L 为族代表**（3y CV 最优 + 无负年 + 10y CV 最低 + 10y 均值最高）。

### 3.5 E569ZE7L 逐年覆盖（2014–2023 全覆盖）

| 年 | PnL | Sharpe | Fitness | longCount |
|---|---:|---:|---:|---:|
| 2014 | 733,898 | 1.72 | 1.23 | 158 |
| 2015 | 904,678 | 2.23 | 1.86 | 169 |
| 2016 | 237,410 | 0.62 | 0.26 | 182 |
| 2017 | 811,510 | 2.40 | 1.90 | 200 |
| 2018 | 740,430 | 1.83 | 1.38 | 198 |
| 2019 | 135,065 | 0.37 | 0.12 | 206 |
| 2020 | 916,285 | 2.34 | 2.05 | 223 |
| 2021 | 204,973 | **0.55** | 0.22 | 285 |
| 2022 | 1,227,073 | 2.64 | 2.57 | 299 |
| 2023 | 765,349 | 1.88 | 1.44 | 277 |

近十年每年都有数据，longCount 158 → 299 单调上升，**无负年**。

### 3.6 ★ 卡点：稳健性 CV 闸

既定硬约束：**Recent-3yr CV_Sharpe ≥ 0.60 ⇒ REJECT；放宽入口仅限用户明确指令。**

E569ZE7L 近三年 CV = **0.626 ≥ 0.60 ⇒ 按字面 REJECT**（第二名 GrWZqQaJ 0.640，8 个窗口变体全落 0.626~0.808）。

**根因（数据环境特性，非选样问题）**：2021 年德国借券市场几无波动（借券评级变化信号信息量不足），
2022 年极端反弹。8 个窗口变体在 2021 年**全部退化**（0.18~0.55），说明该年借券数据本身信息量不足。

**处置选项**：
1. 用户明确授权放宽 CV 闸至 0.65 ⇒ E569ZE7L 立即可提交（其余四闸 + prod/self + 覆盖全过）；
2. 维持 CV 闸 ⇒ 借券族不出货，继续找别的机制族做第三席。

---

## 四、本轮方法论沉淀（Agent Memory）

1. **自相关筛查必须走本地工具全扫**（`check_self_correlation` 零平台槽）——24 颗数分钟扫完。
2. **OS 池会漂移，昨日的 self 结论今天可能作废** —— 发现 OS 新增件须立即重扫待提交清单。
3. **族被「自己人」锁死时穷举参数是无效功** —— 族内变体 self 全 ≥0.7 ⇒ 结构性封盘，换机制族。
4. **「族内只投 X」准则要用 OS 池实证推翻** —— 不能凭本轮回测的临时结论固化规则。
5. **preflight 的 soft 警告必须当硬警告** —— 否则整批 CANCELLED。
6. **子 alpha id 在回测完成前是 simulation id** —— 且 `lookINTO_SimError_message` 参数名是 `locations`（复数）。
7. **借券/拥挤度类信号方向必须实测** —— 全负 ⇒ 方向反了，翻转符号重测（最高产补救）。
8. **CW 闸在借券族同样用 ts_backfill 解** —— 应作默认写法而非事后补救。
9. **族内同源候选的容量上限由互相关决定，不是 prod** —— prod 宽不代表能多交。
10. **「双窗口加速度 × target_tvr_decay」是财报/借券类稀疏数据的通用可交付骨架**。
11. **CV 闸超线先拆「单年拖累」vs「机制性不稳」** —— 年度敏感可修，机制性才判死。

---

## 五、待用户裁定（三项）

### 1. 提交授权
| 件 | 状态 | 建议 |
|---|---|---|
| **1YNMAA8M** | 四闸全过，prod refresh 0.6951、self 0.6946、18/18 独立集 | 可提交；但双闸余量各 0.005，提交前必须 refresh 终验 |
| **E569ZE7L** | 四闸全过 + prod 0.5444/self 0.5444 + 无负年 + 10y 覆盖满 | 需先裁定 CV 闸 |

**不建议两颗同时提交** —— 1YNMAA8M 与 rKRx2Alj 互相关 0.6946 已在贴线，
再叠加 E569ZE7L 虽与两者都低（0.1227 / 0.128），但 1YNMAA8M 的 self 余量会被推高风险。

### 2. 稳健性 CV 闸口径
- 维持 0.60 ⇒ 借券族本轮不出货；
- 放宽至 0.65 ⇒ E569ZE7L 可提交（族内最优、唯一无负年）。

### 3. 目标数字口径
goal 标题写「20 个」、第 4 条写「10 个」。当前本战役新挖 **3 颗**
（zq3eb7No / bl6AvMkN 已 ACTIVE，1YNMAA8M 待授权），加上 E569ZE7L 为 4 颗。

### 4. 是否继续 DEU 深挖 / 是否放开 region
- 分析师修正族封盘、fundamental6 封盘、借券族可出 1 席；
- DEU 域内要往 10 颗走，需放开「不得换 region」过程约束（goal 明文，需你修改）。

---

## 六、本轮波次清单

| 波 | sim id | 主题 | 结果 |
|---|---|---|---|
| A | 1GUTfd45X4AX9gApqdYxOu9 | fundamental6 单字段单窗口 ts_delta ×10 | 全灭 S≤1.04 |
| B | 2Bh3B46WQ4WkaR618dkc6WK4 | fundamental6 混合结构 | 整批 ERROR（fnd6_newq_revtq DEU 不存在） |
| C | 8LgH62th4Vv8KC1exA7RgMs | fundamental6 双窗口加速度 ×10 | 1 颗四闸（vR1QQ9ja，prod 深钉） |
| D | 59ePVbYL596czfEWLYaZwQ | shortinterest3 借券正向 ×10 | 全负 ⇒ 方向反，归因转折点 |
| E | 9Z2Nz2vz5aXcCzAoCdXcfV | fundamental6 参数族 ×10 | 1 颗四闸（YP1ee5zA，prod 深钉） |
| F | 2Kfx681VD4WAayU10UdQcl81 | shortinterest3 符号翻转 ×10 | 2 颗出货 |
| G | 34ObXdaCG4lG8TPucF5UGlI | fundamental6 换 8 字段 ×10 | 全灭 S≤1.23 ⇒ 封盘 |
| H | 4Bc6zL1JO4WPbEckzxBTcVo | 借券 + backfill CW 修复 ×10 | 1 颗四闸（j2Y7qlA5） |
| I | g2SLU4U84yVbOqif5NM1Mf | 借券参数展开 ×10 | 3 颗四闸 |
| J | 12VyLB52i4Z58ZKUtKec41O | 稳健性修复变体 ×10 | 3 颗四闸 |
| K | 2z1pZ83ZW4FXbP73jIVhRTm | 借券长窗对穷举 ×10 | 2 颗四闸（E569ZE7L） |
| L | 35h9D89i44R2bqwFMLcMKQr | 精细窗口扫描 ×10 | 7 颗四闸 |

累计：**137 波 / 约 565 条回测**（本轮新增 11 波 / 110 条）。

---

## 七、相关文件

- `CRITICAL_CORRECTION_20261110.md` —— mLovbnm2 撤回 + 24 颗 self 全量重算 + fundamental6 盘点
- `SEAT3_9qxnNkeq_profile.md` / `SEAT3_j2Y7qlA5_profile.md` —— 第三席候选档案
- `submit_staging_1YNMAA8M.json` / `submit_staging_E569ZE7L.json` —— 提交参数（待授权）
- `submit_staging_mLovbnm2.json` —— 已标记 WITHDRAWN_DO_NOT_SUBMIT
- `final_delivery_20261109.md` —— 上一轮交付文档
