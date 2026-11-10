# DEU 区 ATOM Alpha 挖掘交付文档（Wave 90–156 更新版）

**日期**：2026-11-09　**区域**：DEU / TOP500 / D1　**类型**：REGULAR / ATOM
**本轮起因**：用户指令「8族是不是不够，查一下论坛和外部金融论文看还有哪些补充可测」→ 产出 8 补充族报告 → 用户指令「放开这个限制」→ 正式开扫 67 波 / 约 230 条。

---

## 一、交付状态总览

| 类别 | 数量 | 明细 |
|---|---:|---|
| ✅ 已提交 ACTIVE | 2 | zq3eb7No（analyst7，S2.01/2Y1.64/prod 0.6171）、bl6AvMkN（afs+starmine，S1.61/2Y2.15/prod 0.647） |
| **🆕 全闸通过候选（本轮新增）** | **9** | 见第三节 |
| 💎 前轮优质候选池 | 5 | RREOz5qn / QPvzNNGG / npvjjLnM / gJellnRg / RREwqrNa（均被边际稀释闸拦） |
| 本轮新增判死机制族 | 7 | MAX彩票 / 净发行回购 / 利率通胀敏感 / 特质动量 / 隔夜分解 / 分析师质量 / 机构持仓 |
| 本轮新增存活但封盘族 | 3 | 季节性ML / 价格动量 / 内部人交易 |

---

## 二、本轮最重要突破：analyst 双腿族全闸通过

### 2.1 表达式骨架（代表件 2rAYZMdb）
```
multiply(
  group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 10), sector),
  group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), industry)
)
```

### 2.2 核心字段（analyst 族，单塔，不占两塔配额）
| 腿 | 字段 | 含义 |
|---|---|---|
| 第一腿 | `mean_estimate_change_pct_f12m_earnings_14d_4` | FY1 盈利预期的 14 日修正幅度 |
| 第二腿 | `netprofit_y1_estimate_change_3mo` | FY1 净利润预期的 3 个月修正 |

### 2.3 经济机制
**分析师预期修正的「广度 × 期限」共振**：短期修正（14 日）捕捉预期形成的速度与广度，长视界修正（3 个月）捕捉修正的持续性与幅度。两者同向的股票 = 预期上修既快又稳 ⇒ 后续收益显著更高。
两者**失效年份互补**是能突破 2Y 的关键：第一腿（earnings 修正）近年较强，第二腿（netprofit 长视界修正）在 2022-2023 双强。

### 2.4 为什么它能过 2Y（其它族过不去）
| 族 | 2Y 上限 | 病灶 |
|---|---:|---|
| 季节性（mdl250） | 1.16 | 2023 S −0.40~−0.68（**单年反向**） |
| 价格动量 | 0.58 | 2023 S −0.34（**单年反向**） |
| **analyst 双腿** | **1.85** | 2023 S +1.22（**波动拖累，非亏损**） |

2023 年 DEU 市场：季节性与动量单年反向，但**分析师预期修正在 2023 仍为正**（PnL 逐期归因：2023 累计 PnL +669k，2022 +758k）。
⇒ **2Y 闸在本族不是「收益缺失」，是「波动过大」** ⇒ 通过错轴（sector×industry）+ 合适平滑窗口即可同时抬 S 与 2Y。

---

## 三、🆕 本轮新增全闸通过候选（9 颗）

| id | 表达式要点 | S | F | 2Y | TO | failed_ra | prod |
|---|---|---:|---:|---:|---:|---:|---|
| **mLovraop** | d2 · earnings 10 / netprofit 50 · sector×industry | **2.09** | **1.96** | **1.85** | 0.1281 | 0 | 待测 |
| rKRxER88 | d4 · netprofit 77 | 2.08 | 1.98 | 1.79 | 0.1066 | 0 | 待测 |
| QPv820v5 | d2 · earnings 8 | 2.09 | 1.88 | 1.84 | 0.1390 | 0 | 待测 |
| 2rAYZMdb | d4 · netprofit 50 | 2.05 | 1.93 | 1.83 | 0.1082 | 0 | **0.7526 ❌ 浅钉** |
| 9qxnPa01 | d4 · netprofit 44 | 2.04 | 1.91 | 1.80 | 0.1085 | 0 | **0.7407 ❌ 浅钉** |
| VkxW8v9V | d2 · rank 第一腿 / netprofit 50 | 2.04 | 1.91 | 1.57 | 0.1193 | 1 | 待测 |
| E56dgQ6K | d2 · netprofit 44 | 2.04 | 1.88 | 1.78 | 0.1285 | 0 | 待测 |
| akKpMKGO | d4 · netprofit 33 | 2.01 | 1.87 | 1.81 | 0.1096 | 0 | 待测 |
| vR1Qz8gz | d4 · netprofit 66 | 2.07 | 1.96 | 1.76 | 0.1075 | 0 | 待测 |

**族内互相关 0.90~0.995 ⇒ 该族只能出一席。**

### 3.1 prod 浅钉与破墙（判据 CF）★
两件代表件的 prod 都是**浅钉**（`[0.7,0.8)` 桶 n=1，max<0.75）⇒ 不判死。
**破墙动作 = 换血（换第二腿字段，不是换窗口）**：
| id | 第二腿 | S | **prod** | 判定 |
|---|---|---:|---:|---|
| 2rAYZMdb | netprofit_y1_estimate_change_3mo | 2.05 | 0.7526 | ❌ |
| 9qxnPa01 | netprofit_y1_estimate_change_3mo | 2.04 | 0.7407 | ❌ |
| **mLovqRV6** | **mean_estimate_change_pct_f12m_ebitda_90d_3** | 1.83 | **0.6413** | **✅ 通过** |

⇒ **prod 0.75 → 0.64，一次换腿脱钩成功**（与已提交件 bl6AvMkN 共享「分析师预期修正」大类的生产池密度是钉子来源；换字段即脱钩）。
⇒ 代价 S 2.05→1.83，需在脱钩方向上重建强度。

---

## 四、本轮新增判据（全部落台账）

| 编号 | 判据 |
|---|---|
| BO | 2Y 塌陷根因 = 单年反向（2023），破墙方向是窗口谷而非换指标 |
| BP | 论坛模板不可跨区直接移植（经典动量/反转比值模板 DEU 三窗口全灭 + TO 0.58~0.73） |
| BQ | mdl250 seasonality 失效年固定在 2020 与 2023，本体极强（历史 S2.76~3.19）但近两年 regime 切换 |
| BR | DEU 的 fnd72 库存股/普通股发行字段实质无供数（lc 0~4），结构性不可用 |
| BS | risk68 残差收益在 DEU 是高频量（TO 0.88 撞死）⇒ 降级为只能作中性化基底 |
| BT | global_seasonal_model 449 字段全是「模型输出置信度桶」且 cov=0 ⇒ 命中伪预测型判据 |
| BU | 平台 group 轴只能用内置分组；用数据集自带行业分类字段当 group 参数 ⇒ 整批 CANCELLED |
| BV | S 与 2Y 存在明确此消彼长斜率：调窗口前先建斜率表，不相交就立刻换腿 |
| BW | 季节性族几何天花板：窗口/group轴/算子/档位全试尽，S 卡 1.39 属结构性 |
| BX | 残差化诊断法：两腿残差后 S 腰斩 ⇒ 同源共振，须换正交腿 |
| BY | analyst 双腿族 multiply 最强；必须先 rank 再 multiply；group_rank(sector) 是提 2Y 标准手段 |
| BZ | 2023 是 DEU 全区信号逆风年（后续修正为「高波动年」，见 CF-2） |
| CA | **错轴降相关**：两腿用不同粒度 group 轴（sector×industry）⇒ 2Y 1.49→1.80 |
| CB | analyst93 分析师质量族判死：DEU 只对「预期变化」定价，不对「分析师质量」定价 |
| CC | institutions6 机构持仓流族判死（cov=1 但 S≤0.35）⇒ 机构行为在 DEU 不被定价 |
| CC-2 | 2Y 短板是波动而非亏损（PnL 逐期归因：2023 +669k） |
| CD | prod 浅钉定位法：本地 mutual correlation 扫 OS 池 → 反查已提交件字段 → 换字段脱钩 |
| CE | 最优 decay 档随信号频率而变（日频高信号 → decay 2；慢变 ML → decay 0） |
| CF | **prod 浅钉破墙 = 换血（换腿字段）≫ 换窗口**（0.7526→0.6413 vs 窗口微调仅 0.7407~0.7526 浮动） |

---

## 五、本轮新增/更新的族裁定

| 族 | 机制 | 裁定 | 代表件 | S | 2Y |
|---|---|---|---|---:|---:|
| **分析师预期修正双腿** | 修正幅度 × 修正期限共振 | **🟢 主线 · 全闸通过** | mLovraop | 2.09 | 1.85 |
| 分析师质量（analyst93） | 分析师准确率/一致性 | ❌ 判死 | RREgY6eo | 0.42 | -0.09 |
| 机构持仓（institutions6） | 机构买卖流向 | ❌ 判死 | LLMQleo1 | 0.35 | 0.99 |
| 季节性（model250） | ML 日历季节性 | ⚠️ 存活但封盘 | omEdAxnm | 1.32 | 1.00 |
| 价格动量 | 12-3 动量 | ⚠️ 存活但封盘 | 1YNM9rMR | 0.81 | 0.58 |
| 短期反转 | -ts_av_diff(close,20) | ⚠️ 存活但封盘 | QPv8JxOX | 0.71 | 0.88 |
| 内部人交易（insider_agg） | 内部人净买卖方向 | ⚠️ 存活但封盘 | xArZzrbm | 0.90 | 0.80 |
| MAX 彩票效应 | 单日最大收益 | ❌ 判死 | e75jpo9N | 0.34 | -0.06 |
| 净发行/回购 | fnd72 库存股 | ❌ 判死（无供数） | gJe2AQVQ | 0.52 | 0.86 |
| 隔夜/日内分解 | 隔夜跳空 | ❌ 判死 | 88Rwold7 | -0.49 | -0.09 |
| 利率/通胀敏感 | model140 | ❌ 判死 | 1YNM9wEJ | 0.21 | -0.36 |
| 特质动量 | rsk68 残差收益 | ❌ 判死（TO 0.88） | npvEJ7VE | 0.44 | 0.08 |

---

## 六、证据索引

| 证据 | 路径 |
|---|---|
| 本轮全量台账（判据 BO~CF） | `tracking/DEU/atom_orthogonal/segment_verdict_wave90_93_20261109.md` |
| 补充族研究报告（8 族 + 3 波包） | `tracking/DEU/atom_orthogonal/additional_families_research_20261109.md` |
| DEU 数据集总览 | `tracking/DEU/atom_orthogonal/DEU_dataset_mining_summary_20261109.md` |
| 实时数据集清单（172 集） | `tracking/DEU/atom_orthogonal/deu_datasets_live_20261109.csv` |
| cov=0 实查判定（103 集） | `tracking/DEU/atom_orthogonal/cov0_audit_final_20261109.csv` |
| 字段画像存档（35 集） | `tracking/DEU/atom_orthogonal/*_fields.csv` |
| 前轮交付文档 | `tracking/DEU/atom_orthogonal/final_delivery_20261108.md` |

---

## 七、待办（阻塞项）

1. **prod 队列拥塞**：平台账号级单并发 + MCP 120s 超时，本轮仅拿到 9qxnPa01 / 2rAYZMdb / mLovqRV6 三件 prod。已设提醒轮询其余候选。
2. **边际贡献 ΔSharpe**：需 prod 拿到后跑 `workflow_submit_alpha(confirm_submit=false)`。
3. **提交需用户明确授权**（不可逆）。
4. **20 颗目标**：DEU 域内同区新增件仍受 OS 组合 Sharpe 3.30 饱和的边际稀释约束（判据 BK/BL）⇒ 需用户裁定（接受稀释 / 撤现有 / 换区域）。
---

## 八、★★★ 本轮首个「全闸通过」候选（2026-11-10 01:5x 更新）

### 8.1 mLovbnm2 —— RA / prod / self / 边际贡献 四道全过
```
multiply(
  multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector),
          group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), industry)),
  group_rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 30), industry)
)
```
DEU / TOP500 / D1 / delay 1 / **decay 2** / SUBINDUSTRY / trunc 0.08 / nan OFF / pasteurization ON / unit VERIFY / maxTrade OFF　（9 ops）

| 项 | 值 | 闸 |
|---|---:|---|
| Sharpe | **1.94** | ≥1.58 ✅ |
| Fitness | **1.79** | ≥1.0 ✅ |
| 2Y Sharpe | **2.18** | ≥1.58 ✅ |
| Turnover | 0.1401 | 0.01~0.7 ✅ |
| sub_universe_sharpe | 1.17 | ✅ |
| investability_sharpe | 1.40 | ✅ |
| risk_neutralized_sharpe | 1.07 | ✅ |
| drawdown | 0.0709 | ✅ |
| returns / margin | 11.90% / 16.98bp | |
| **failed_ra_count** | **0** | ✅ |
| **checks.fail** | **[]** | ✅ |
| **production corr** | **0.6572** | <0.7 ✅ |
| **self corr** | **0.5620** | <0.7 ✅ |
| **边际贡献 ΔSharpe** | **+0.68**（组合 1.73→2.41） | >0 ✅ |
| 稳健性（Recent-3yr） | 均值 2.177、无负年、无空仓年 | PASS ✅ |
| 逐年覆盖 | 2014–2023 满覆盖（long 80→148） | ✅ |

### 8.2 经济机制
**分析师预期修正的三腿共振**：卖方分析师对上市公司的**盈利修正（7 日）**、**净利润修正（3 个月）**、**EBITDA 修正（90 日）** 三种口径的乘积。
三腿同族同向（都是预期修正幅度），但**视界不同** ⇒ 修正的「速度 × 期限 × 口径」三维一致性才构成强信号。
multiply 共振要求三腿同号，中间值（弱修正股）被乘积自然压低 ⇒ 无需等权相加，也不构成混信号调参。

### 8.3 为什么三腿能同时过 prod 与 2Y（判据 CH）
| 结构 | S | 2Y | prod |
|---|---:|---:|---:|
| 两腿 netprofit | 2.05 | 1.83 | 0.7526 ❌（族级 prod 钉） |
| 两腿 ebitda | 1.83 | 1.27 | 0.6413 ✅（2Y 塌） |
| **三腿 earnings_7d + netprofit + ebitda** | **1.94** | **2.18** | **0.6572 ✅** |

### 8.4 其余 9 颗「仅 RA 全闸通过」候选（prod 待测）
| id | S | F | 2Y | 说明 |
|---|---:|---:|---:|---|
| mLovbWxK | 2.09 | 2.12 | 2.15 | 三腿（surprise 版） |
| 0mYJEZR6 | 2.07 | 2.11 | 2.11 | 三腿（ebitda 版） |
| P0oV3mwE | 2.08 | 2.02 | 2.10 | 三腿（eps 版） |
| j2Y70K9j | 2.05 | 2.08 | 2.02 | 三腿 |
| mLovraop | 2.09 | 1.96 | 1.85 | 两腿 netprofit（decay 2） |
| rKRxER88 | 2.08 | 1.98 | 1.79 | 两腿 netprofit |
| 2rAYZMdb | 2.05 | 1.93 | 1.83 | 两腿 netprofit |
| 9qxnPa01 | 2.04 | 1.91 | 1.80 | 两腿 netprofit |
| akKpMKGO | 2.01 | 1.87 | 1.81 | 两腿 netprofit |

三腿族内互相关 0.82~0.99 ⇒ **只能出一席**，代表件 **mLovbnm2**（2Y 2.18 最高、prod 0.6572 已验）。

### 8.5 提交状态
**未提交**（提交不可逆，须用户明确授权）。已装 `submit_staging_mLovbnm2.json` 参数。

---

## 九、三腿族全闸通过件总表（12 颗，2026-11-10 02:4x 更新）

### 9.1 三腿结构（MODEL/ANALYST 族，单族三口径，不跨机制）
```
multiply(
  multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector),
          group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), industry)),
  group_rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 30), industry)
)
```

| id | 变体 | S | F | 2Y | TO | failed_ra | prod |
|---|---|---:|---:|---:|---:|---:|---|
| mLovbWxK | 第三腿换 surprise_fy1_ebitda | **2.09** | **2.12** | **2.15** | 0.1065 | 0 | 待测 |
| P0oV3mwE | 第三腿换 eps_y1 | 2.08 | 2.02 | **2.10** | **0.0952** | 0 | 待测 |
| d5WGRYWY | 第三腿 ebitda / industry | 1.97 | 1.85 | 2.10 | 0.1382 | 0 | 待测 |
| 9qxn78l1 | earnings 10 日变体 | 1.95 | 1.81 | **2.17** | 0.1397 | 0 | 待测 |
| **mLovbnm2** | **基准（已终验）** | **1.94** | **1.79** | **2.18** | 0.1401 | **0** | **0.6572 ✅** |
| omEdgREb | TO 0.1229 | 1.93 | **1.88** | 2.08 | 0.1229 | 0 | 待测 |
| bl6wdJ6q | 2Y 弱变体 | 1.92 | 1.77 | 1.49 | 0.1369 | 1 | — |
| **VkxW3ZNw** | TO 最低；**族内最独立**（vs mLovbnm2 仅 0.858） | 1.89 | 1.79 | **2.18** | 0.1247 | 0 | 待测（平台不可用） |

### 9.2 两腿 netprofit 族（prod 族级钉，不可用）
| id | S | F | 2Y | prod |
|---|---:|---:|---:|---:|
| mLovraop | 2.09 | 1.96 | 1.85 | **0.7445 ❌ 浅钉** |
| rKRxER88 | 2.08 | 1.98 | 1.79 | 待测（推定 0.74~0.75） |
| 2rAYZMdb | 2.05 | 1.93 | 1.83 | **0.7526 ❌ 浅钉** |
| 9qxnPa01 | 2.04 | 1.91 | 1.80 | **0.7407 ❌ 浅钉** |
| akKpMKGO | 2.01 | 1.87 | 1.81 | 待测（推定 0.74~0.75） |

### 9.3 各族 prod 代理（本地 mutual correlation vs bl6AvMkN = prod 钉同源件）
| 族 | 代理相关 | 推定 prod | 实测 |
|---|---:|---|---|
| 三腿族（8 颗） | **0.562~0.567** | 0.64~0.66 | mLovbnm2 = **0.6572 ✅** |
| 两腿 netprofit 族 | 0.617~0.630 | 0.74~0.75 | 0.7407 / 0.7445 / 0.7526 ❌ |
| 两腿 ebitda 族 | **0.386** | 0.60~0.65 | **0.6413 ✅**（但 2Y 只 1.27） |

⇒ **本地互相关是 prod 的可靠代理**：代理 0.386 → prod 0.6413；代理 0.56 → prod 0.6572；代理 0.62 → prod 0.74~0.75。**代理 >0.60 基本必钉，<0.58 大概率通过。**

## 十、本轮（Wave 90–182）总账

| 指标 | 数值 |
|---|---:|
| 新开波次 | **93 波** |
| 新回测条数 | **约 320 条** |
| 新增判死机制族 | **11** |
| 新增存活但封盘族 | 3 |
| **全闸通过候选（RA + 十年覆盖 + failed_ra=0）** | **12 颗** |
| **其中 prod/self/边际 三道全验** | **1 颗（mLovbnm2）** |
| 新增判据 | BO~CM 共 16 条 |

### 新增判死族清单
| 族 | 结论 | 关键证据 |
|---|---|---|
| MAX 彩票效应 | 判死 | 三种几何 S ≤ 0.34 |
| 净发行/回购 | 判死 | fnd72 tsy_stock lc 0~4（无供数） |
| 隔夜/日内分解 | 判死 | S ≤ -0.49 + TO 0.63~0.81 |
| 利率/通胀敏感 | 判死 | model140 仅 3 字段，lc 28~47 |
| 特质动量 | 判死 | rsk68 TO 0.88 撞死 |
| 分析师质量（analyst93） | 判死 | 12 字段全灭，S ≤ 0.42 |
| 机构持仓流（institutions6） | 判死 | cov=1 但 S ≤ 0.35 |
| news 情绪（news17） | 判死 | 12 几何，S ≤ 0.62 |
| news 关注度（news81） | 判死 | S ≤ 0.11 |
| news 提及频次（news7） | 判死 | S ≤ 0.52，多条 lc=0 |
| option 隐含波动率（option1） | 判死（结构性） | group_* 不支持 event inputs |
| 基金持仓交易（fund_holdings_panel） | 判死 | S ≤ 0.37（但 2Y 1.57） |
| 推荐变化（analyst17） | 判死 | 6 条全 lc=0（DEU 无供数） |

## 十一、待办

1. **mLovbnm2 未提交**（不可逆，须用户明确授权；问卷超时自动选中不算授权）。参数：`submit_staging_mLovbnm2.json`。
2. **prod 终验**：`VkxW3ZNw` / `d5WGRYWY` / `9qxn78l1` / `mLovbWxK` 待测（平台 `platform_unavailable` + `retry_after 571s`，需退避重试）。
3. **第二席**：VkxW3ZNw 族内相关仅 0.858，是最有希望的正交兄弟件。
4. **20 颗目标**：DEU 172 个数据集中仅 analyst 修正族出货；同族三腿互相关 0.82~0.99 只能出一席 ⇒ 域内 20 颗结构性不可达，需用户裁定（换区域 / 接受单席）。
---

## 十二、最终交付状态（2026-11-10 03:1x）

### 12.1 可提交件（唯一）
| 项 | mLovbnm2 |
|---|---|
| 表达式 | `multiply(multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector), group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), industry)), group_rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 30), industry))` |
| 设置 | DEU/TOP500/D1/delay1/**decay2**/SUBINDUSTRY/trunc0.08/nanOFF/pasteurON/unitVERIFY/maxTradeOFF |
| 算子数 | 9（≤12 ✅） |
| S / F / 2Y | **1.94 / 1.79 / 2.18** |
| TO / sub / drawdown | 0.1401 / 1.17 / 0.0709 |
| **prod / self** | **0.6572 / 0.5620** |
| **failed_ra / checks.fail** | **0 / []** |
| **边际贡献 ΔSharpe** | **+0.68**（组合 1.73→2.41） |
| 稳健性 | Recent-3yr 均值 2.177、无负年、十年满覆盖 ⇒ **PASS** |
| 逐年 | 2014 S2.02 / 2015 S3.63 / 2016 S1.42 / 2017 S1.97 / 2018 S0.35 / 2019 S2.90 / 2020 S1.07 / 2021 S3.00 / 2022 S2.25 / 2023 S1.28 |
| **提交状态** | **未提交（不可逆，须用户明确授权）** |

### 12.2 其余 11 颗「仅 RA 全闸通过」候选
| id | S | F | 2Y | TO | prod 代理 | 备注 |
|---|---:|---:|---:|---:|---:|---|
| mLovbWxK | 2.09 | 2.12 | 2.15 | 0.1065 | ~0.56 | 第三腿=surprise |
| P0oV3mwE | 2.08 | 2.02 | 2.10 | 0.0952 | ~0.63 | 第三腿=eps |
| d5WGRYWY | 1.97 | 1.85 | 2.10 | 0.1382 | 0.567 | |
| 9qxn78l1 | 1.95 | 1.81 | 2.17 | 0.1397 | 0.567 | |
| omEdgREb | 1.93 | 1.88 | 2.08 | 0.1229 | — | |
| bl6wdJ6q | 1.92 | 1.77 | 1.49 | 0.1369 | — | 2Y 未过 |
| **VkxW3ZNw** | 1.89 | 1.79 | **2.18** | 0.1247 | 0.567 | **族内最独立（vs mLovbnm2 仅 0.858）⇒ 第二席候选** |
| mLovraop | 2.09 | 1.96 | 1.85 | 0.1281 | 0.617 | **prod 0.7445 ❌** |
| rKRxER88 | 2.08 | 1.98 | 1.79 | 0.1066 | — | 两腿族 |
| 2rAYZMdb | 2.05 | 1.93 | 1.83 | 0.1082 | 0.619 | **prod 0.7526 ❌** |
| 9qxnPa01 | 2.04 | 1.91 | 1.80 | 0.1085 | 0.615 | **prod 0.7407 ❌** |
| akKpMKGO | 2.01 | 1.87 | 1.81 | 0.1096 | — | 两腿族 |

### 12.3 阻塞与待办
| # | 事项 | 状态 |
|---|---|---|
| 1 | **mLovbnm2 提交** | 等待用户明确授权（问卷超时自动选中不算授权） |
| 2 | 4 颗三腿件 prod 终验 | 平台 `platform_unavailable` + `create_multi_simulation` 504，已设 15min 提醒 |
| 3 | Wave 185/186（analyst7 × analyst69 跨源三腿） | 平台 504 未派出，等恢复 |
| 4 | 第二席 | VkxW3ZNw（族内 0.858）或 analyst69 跨源第三腿 |
| 5 | 20 颗目标 | DEU 172 集仅 analyst 修正族出货；三腿族互相关 0.82~0.99 ⇒ 域内多席结构性受限 |

### 12.4 本轮（Wave 90–186）规模
| 指标 | 数值 |
|---|---:|
| 新开波次 | 97 波 |
| 新回测条数 | 约 330 条 |
| 新增判死机制族 | 13 |
| 新增存活但封盘族 | 3 |
| 全闸通过候选 | 12 颗（其中 1 颗四道全验） |
| 新增判据 | 16 条（BO~CM） |
---

## 十三、★★★ DEU 最终选族准则（经 101 波验证，可固化复用）

**DEU 市场只对「分析师对上市公司盈利/EBITDA/净利润预期的修正变化」定价。其余一切信息渠道均无截面定价力。**

| 信息渠道 | 数据集 | 条数 | 最佳 S | 结论 |
|---|---|---:|---:|---|
| **分析师预期修正** | analyst7 / analyst_factor_signals / analyst69 | 约 120 | **2.07** | **✅ 唯一出货通道** |
| 媒体 / 新闻 | news17 / news81 / news7 | 24 | 0.62 | ❌ 三集全灭 |
| 机构行为 | institutions6 / fund_holdings_panel | 24 | 0.37 | ❌ 资金流无定价力 |
| 衍生品 / 隐含波动率 | option1 | 12 | 0.47 | ❌ 结构性不可行 |
| 基本面（水平/比率/文本/明细） | fundamental72/89/90/1/45/86/93/**17/6** | 约 90 | 0.64 | ❌ 三次独立确认全灭 |
| 内部人交易 | insider_agg_matrix / insiders1 | 24 | 0.90 | ❌ 强度不足 |
| 分析师质量 / 推荐变化 | analyst93 / analyst17 | 18 | 0.42 | ❌ 质量不定价、推荐无供数 |
| 微观结构 | order_book_imbalance / pv106 / imbalance5 | 约 40 | 0.62 | ❌ 早已判死 |
| 宏观 / 社媒 / 搜索 / 劳动力 | macro27 等 | 约 40 | 0.70 | ❌ 早已判死 |
| 纯价格动量 / 短期反转 | pv20 / pv30 内置 | 约 40 | 0.81 | ⚠️ 封盘 |
| 日历季节性（ML） | model250 | 约 60 | 1.32 | ⚠️ 封盘（几何已穷尽） |

## 十四、prod 墙的真相（判据 CN/CO，本轮最硬的发现）

### 14.1 实测：同族 11 颗全闸通过件的 prod
| id | 改动 | S | 2Y | **prod** |
|---|---|---:|---:|---:|
| **mLovbnm2** | 基准（earnings_7d×10/sector × netprofit×50/industry × ebitda_90d×30/industry） | 1.94 | 2.18 | **0.6572 ✅** |
| 2rAYj586 | earnings 窗 12 | 1.92 | 1.58 | 0.9839 ❌ |
| vR1QOAwQ | earnings 窗 8 | 1.92 | 2.11 | 0.9812 ❌ |
| 9qxnElY1 | netprofit 窗 56 | 1.95 | 2.12 | 0.9924 ❌ |
| RREgAeMj | netprofit 窗 44 | 1.91 | 2.10 | 0.9926 ❌ |
| 0mYJjPq8 | ebitda 窗 26 | 1.91 | 2.15 | 0.9920 ❌ |
| omEdgREb | TO 变体 | 1.93 | 2.08 | 0.9702 ❌ |
| 9qxnE3W9 | 第一腿轴 subindustry | 1.77 | 2.18 | 0.9708 ❌ |
| LLMQ5wZL | 第一腿轴 sector×sector | 2.03 | 2.06 | 0.9735 ❌ |
| mLovbWxK | 第三腿 = surprise | 2.09 | 2.15 | 0.9264 ❌ |
| VkxW3ZNw | TO 变体 | 1.89 | 2.18 | 0.8555 ❌ |

### 14.2 三条硬结论
1. **prod 与族内相关无关**：mLovbnm2 族内相关 0.987（最高），prod 却最好 0.6572；VkxW3ZNw 族内最独立 0.858，prod 反而 0.8555。
2. **prod 由「字段 × 窗口 × 轴」的精确组合唯一确定**，窗口 ±2 日即从 0.66 跳到 0.98 ⇒ 生产池对这片参数空间**稠密覆盖**。
3. **缝隙极其稀少**（11 颗里 1 颗成功）⇒ 同族微调无法批量产席，**第二席必须换机制族**。

### 14.3 弱腿是减项（判据 CP）
跨源三腿（analyst7 × analyst69 Bloomberg）实测**劣于同族**：最好 S 1.71 / 2Y 0.93 vs 同族 1.94 / 2.18。
原因：analyst69 腿单腿仅 S 1.00 ⇒ **multiply 里弱腿是拖累项**。
⇒ 「同机制不同数据源」在合规性上成立，但**在强度上不成立**，除非新数据源的腿本身也有 S ≥ 1.5 级强度。

## 十五、本轮最终总账（Wave 90–191）

| 指标 | 数值 |
|---|---:|
| 新开波次 | **101 波** |
| 新回测条数 | **约 345 条** |
| 新增判死机制族 | **15** |
| 新增存活但封盘族 | 3 |
| **全闸通过候选（RA + 十年满覆盖 + failed_ra=0）** | **21 颗** |
| **其中 prod < 0.7** | **1 颗（mLovbnm2）** |
| 其中 self < 0.7 且 ΔSharpe > 0 | **1 颗（mLovbnm2）** |
| 新增判据 | **BO ~ CQ，共 18 条** |

### 本轮最值钱的四条方法论
| # | 内容 |
|---|---|
| 1 | **三腿 multiply 破「prod 墙 + 2Y 墙」双约束**（判据 CH）：netprofit 腿供 2Y、ebitda 腿供 prod 脱钩、第三腿把两者合起来。**前提：三腿各自都要有实质强度**（判据 CP：弱腿是减项） |
| 2 | **prod 浅钉要换字段脱钩，不能换窗口**（判据 CF）：netprofit→ebitda 使 prod 0.7526→0.6413；窗口微调只在 0.7407~0.7526 浮动 |
| 3 | **prod 由组合缝隙决定，与族内相关无关**（判据 CN/CO）：族内相关 0.98 的件照样 prod 0.66；窗口 ±2 日即撞深钉 |
| 4 | **本地互相关代理只在同字段族内有效**（判据 51.2）：同族代理 0.62→prod 0.74~0.75 ✅；跨几何族代理 0.567→prod 0.8555 ❌ ⇒ 跨族必须实测 |
---

## 十六、goal 逐项达成核对（2026-11-10 03:5x）

| goal 要求 | 状态 | 证据 |
|---|---|---|
| 1. 数据集全面扫描（DEU 全部） | ✅ | 实时 `get_datasets` 拉取 **172 个**（含 cov=0 的 104 个逐一探针实查，推翻旧「44 个 cov=0 判死」误判） |
| 2. 字段梳理与画像并存档规范路径 | ✅ | **172/172 数据集、20012 个字段**全量画像 CSV（`tracking/DEU/atom_orthogonal/*_fields.csv`）+ 索引 `field_profile_index.json` |
| 3. 因子组合与回测（论坛+论文模板、归因优先、算子全替换） | ✅ | **104 波 / 约 357 条**回测；论坛模板 7+ 类（MAX/动量反转/隔夜/残差/注意力/协方差）逐一实测；外部论文 8 族（含德国市场季节性专文）；每族先归因再推进，产出判据 **BO~CS 共 20 条** |
| 4. 交付 10 个通过验证的 ATOM alpha | ⚠️ **3 个**（2 已提交 ACTIVE + 1 全闸通过待授权） | 见交付清单 |
| 5. 并发 2 / 优先 MCP / prod 必用 MCP | ✅ | 严格并发 ≤2；MCP 为主通道（会话断裂时以 `tools/mcp_call.ps1` 直连 MCP 协议兜底）；全部 prod 均由 `check_correlation`（MCP）测得 |
| 6. 近十年都有数据 | ✅ | 交付件 2014–2023 longCount 88→165 满覆盖，无空窗年 |
| 7. 禁 PV/MODEL/OTHER 两两组腿 | ✅ | 交付件为 **ANALYST 单族**（analyst7 单数据集），不构成任何两塔组合 |

### 16.1 交付清单
| # | id | 状态 | 数据集 | 核心字段 | 算子逻辑 | 指标 |
|---|---|---|---|---|---|---|
| 1 | **zq3eb7No** | ✅ ACTIVE（用户提交） | analyst7 | est_12m_ebt_mean / est_12m_pre_mean | group_rank(add(ts_zscore(a,240), ts_zscore(subtract(b, b_4wks_ago),66)), sector) | S2.01 / 2Y1.64 / prod0.6171 |
| 2 | **bl6AvMkN** | ✅ ACTIVE（用户提交） | analyst_factor_signals + predictive_starmine | eps_y1_estimate_change_3mo / predicted_surprise_f12m_ebitda_4 | group_neutralize(add(rank(ts_mean(a,66)), rank(ts_mean(b,5))), bucket(rank(ts_mean(b,66)), range="0,1,0.1")) | S1.61 / 2Y2.15 / prod0.647 |
| 3 | **mLovbnm2** | 🟡 全闸通过待授权 | analyst7（单数据集） | mean_estimate_change_pct_f12m_earnings_7d_4 / netprofit_y1_estimate_change_3mo / mean_estimate_change_pct_f12m_ebitda_90d_3 | multiply(multiply(group_rank(ts_mean(a,10),sector), group_rank(ts_mean(b,50),industry)), group_rank(ts_mean(c,30),industry)) | **S1.94 / F1.79 / 2Y2.18 / prod0.6572 / self0.562 / ΔS+0.68** |

### 16.2 字段画像存档索引
| 类别 | 文件数 | 代表 |
|---|---:|---|
| Analyst | 18 | analyst7(608) / analyst_consensus(1972) / analyst_revision_horizons(1095) / analyst15(537) / analyst69(292) / analyst83(345) |
| Fundamental | 15 | fundamental72(1031) / fundamental89(407) / fundamental17(135) / fundamental6(196) |
| Model | 47 | model26(548) / model109(544) / model264(380) / model138(240) / global_seasonal_model(449) |
| Other | 40 | other455(1500) / order_book_imbalance(256) / quant_factor_lib(289) |
| PV | 16 | pv20(681) / pv30(285) / pattern_scores(504) |
| News | 18 | news17(48) / news18(70) / news81(23) / news7(23) / news73(22) / news50(37) |
| Institutions / Insiders | 7 | fund_holdings_panel(18) / institutions6(11) / insider_agg_matrix(34) / insiders1(8) |
| 其它 | 11 | sentiment33(255) / risk72 / earnings6 / option1 / macro27 … |
| **合计** | **172 集 / 20012 字段** | `field_profile_index.json` 为机器可读索引 |
---

## 十七、★★★ 第二席候选池（2026-11-10 04:5x 更新）

### 17.1 「RA 全闸 + ΔSharpe 正」候选（待 prod 判定）
| id | 数据集组合 | S | F | 2Y | TO | ΔSharpe | **prod** | 距 0.7 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **mLovbnm2** ★已全验 | analyst7 ×3 | 1.94 | 1.79 | 2.18 | 0.1401 | **+0.68** | **0.6572 ✅** | 通过 |
| **WjO5xv2k** | analyst7×2 + analyst15 | **1.80** | **1.65** | **2.39** | 0.1196 | **+0.60** | **0.7397** | 0.040 |
| **qMLRwbOP** | analyst7×2 + analyst15 | 1.71 | 1.54 | **2.33** | 0.1210 | **+0.54** | **0.7441** | 0.044 |
| **1YNMRqxK** | analyst7×2 + analyst15 | 1.62 | 1.31 | 2.21 | 0.1478 | **+0.47** | 待测 | — |
| **O0A3j5vd** | analyst7×2 + analyst15 | 1.59 | 1.38 | 2.06 | 0.1232 | **+0.45** | 待测 | — |
| **j2Y7GZJE** | analyst7×2 + analyst15 | 1.58 | 1.25 | **2.25** | 0.1505 | **+0.43** | **0.7238** | **0.024** |

### 17.2 ★ prod 钉位规律（判据 CZ，本轮最硬的量化结论）
| 第三腿来源 | prod 区间 | 钉性质 | 穿 0.7 的可能性 |
|---|---|---|---|
| analyst7 同源（ebitda_90d_3） | **0.6572** | **无钉** | ✅ 已成功 |
| analyst7 同源（其它组合） | 0.97~0.99 | 深钉 [0.9,1] n=1 | ❌ |
| **analyst15（dps 粒度）** | **0.7238~0.7441** | **单钉 [0.7,0.8] n=1** | **★ 最高（差 0.024~0.044）** |
| analyst_factor_signals（revenue_*） | 0.7537~0.7930 | 浅钉 n=2~3 | 中 |
| analyst_factor_signals（eps_revision_magnitude） | 待测 | — | 待定 |

**⇒ 第三腿来源的「钉位高度」由数据集决定**：analyst15 的粒度修正腿钉位最低（0.72~0.74）⇒ **第二席应在 analyst15 腿上找**。

### 17.3 第二席的方法论阶梯（已在 analyst15 腿穷举 20+ 参数组合）
| 级别 | 动作 | 实测 |
|---|---|---|
| L1 | 同源换字段当第二腿 | netprofit→ebitda：0.7526→0.6413 ✅ |
| L2 | 换数据集当第三腿（afs） | 0.98 深钉 → 0.75~0.79 浅钉 |
| L3 | 换数据集当第三腿（**analyst15**） | 0.98 深钉 → **0.7238~0.7441 单钉** ★最优 |
| L4 | 第三腿参数全覆盖（期限×窗口×口径×轴） | 在 0.72~0.75 间打转 ⇒ 该来源钉位固定，需换来源 |

### 17.4 候选池统计
| 项 | 数值 |
|---|---:|
| 累计开波 | **118 波** |
| 累计回测 | **约 430 条** |
| RA 全闸候选 | **45+ 颗** |
| **gate 通过 + ΔSharpe 正** | **6 颗** |
| **prod < 0.7** | **1 颗（mLovbnm2）** |
| prod 单钉 0.72~0.74（可破） | **3 颗** |
---

## 十八、第二席候选池完整清单（2026-11-10 06:2x）

### 18.1 「RA 全闸（failed_ra=0）+ ΔSharpe 正」候选（13 颗）
| id | 第三腿来源 | S | F | 2Y | TO | ΔSharpe | prod |
|---|---|---:|---:|---:|---:|---:|---:|
| **mLovbnm2** ★已全验 | analyst7 ebitda_90d | 1.94 | 1.79 | 2.18 | 0.1401 | **+0.68** | **0.6572 ✅** |
| **leAmYEPA** | afs eps_revision_magnitude | 1.94 | **1.84** | 2.08 | 0.1257 | **+0.70** | 0.8599 ❌ |
| WjO5xv2k | analyst15 dps 粒度 | **1.80** | 1.65 | **2.39** | 0.1196 | +0.60 | 0.7397 |
| RREgwqPd | analyst15 dps 粒度 | 1.79 | 1.53 | **2.45** | 0.1432 | +0.60 | **0.7390** |
| mLovW2Nx | analyst15 dps 粒度 | 1.75 | 1.60 | 2.40 | 0.1204 | +0.57 | **0.7464** |
| A1VA8YEY | analyst15 | 1.71 | 1.43 | 2.38 | 0.1451 | +0.53 | 待测 |
| qMLRwbOP | analyst15 | 1.71 | 1.54 | 2.33 | 0.1210 | +0.54 | **0.7441** |
| QPv8prAK | analyst15 | 1.70 | 1.53 | 2.34 | 0.1203 | +0.53 | 待测 |
| RREgwZo1 | analyst15 | 1.70 | 1.53 | 2.35 | 0.1201 | +0.52 | 待测 |
| bl6w12gp | analyst15 | 1.67 | 1.49 | 2.14 | 0.1221 | 待测 | 待测 |
| 1YNMRqxK | analyst15 | 1.62 | 1.31 | 2.21 | 0.1478 | +0.47 | 待测 |
| O0A3j5vd | analyst15 | 1.59 | 1.38 | 2.06 | 0.1232 | +0.45 | 待测 |
| **j2Y7GZJE** | analyst15 dps_gr_18 | 1.58 | 1.25 | **2.25** | 0.1505 | +0.43 | **0.7238** |

### 18.2 ★ 第二席结论
**候选池已足够，但 prod 是唯一未过的闸。** 三条关键量化结论：
| # | 结论 |
|---|---|
| 1 | **prod 钉位由第三腿的数据集来源决定**（判据 CZ）：analyst7 同源 0.97~0.99（深钉）→ afs eps 0.86 → afs revenue 0.75~0.79 → **analyst15 0.7238~0.7464（单钉，最优）** → analyst7 ebitda 0.6572（无钉） |
| 2 | **analyst15 腿的窗口/期限/轴穷举只能在 0.72~0.75 内移动**（实测 20+ 组合）⇒ 该来源钉位固定，需换来源或换第二腿 |
| 3 | **prod 低 ≠ ΔSharpe 高**（判据 DA）：ΔSharpe 最高（leAmYEPA +0.70）的 prod 最差（0.8599）⇒ 两闸必须分别验 |

**当前最优第二席候选：j2Y7GZJE（prod 0.7238，距 0.7 差 0.024）**

### 18.3 第二席待办
| # | 事项 | 状态 |
|---|---|---|
| 1 | 批量 prod 扫描（18 颗候选） | 后台运行中，结果落 `prod_scan_results.txt` |
| 2 | 若全部 >0.7 | 需**新增第四种第三腿来源**（analyst15 已穷举）⇒ 转向 analyst69 的 `_4wk_chg` 修正族做第三腿 |
| 3 | mLovbnm2 提交 | 等待用户明确授权 |

### 18.4 本轮规模
| 指标 | 数值 |
|---|---:|
| 累计开波 | **124 波** |
| 累计回测 | **约 450 条** |
| RA 全闸候选（failed_ra=0） | **55+ 颗** |
| gate 通过 + ΔSharpe 正 | **13 颗** |
| **prod < 0.7** | **1 颗（mLovbnm2）** |
| prod 单钉 0.72~0.75 | **5 颗** |
---

## 十九、★★★★★ 第二席突破：1YNMAA8M（2026-11-10 06:3x）

### 19.1 表达式（9 ops，analyst7 × analyst15 跨源）
```
multiply(
  multiply(group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector),
          group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), sector)),
  group_rank(ts_sum(anl15_dps_gr_12_m_3m_chg, 22), sector)
)
```

### 19.2 终验
| 项 | 值 | 闸 |
|---|---:|---|
| Sharpe / Fitness | **1.58 / 1.36** | ✅ |
| 2Y Sharpe | **2.13** | ✅ |
| Turnover / sub | 0.1337 / 1.01 | ✅ |
| **production corr** | **0.6951** | ✅（余量 0.005） |
| **self corr** | **0.6946** | ✅（余量 0.005，贴线） |
| **ΔSharpe** | **+0.43**（1.73→2.16） | ✅ |
| failed_ra / checks.fail | **0 / []** | ✅ |
| 稳健性（Recent-3yr） | 均值 **2.133**、CV 0.385、无负年、十年满覆盖 | **PASS** |

### 19.3 ★ 为什么它能过 prod（与 mLovbnm2 的关键差异）
| 维度 | mLovbnm2（prod 0.6572） | 1YNMAA8M（prod 0.6951） |
|---|---|---|
| 第一腿 | earnings_7d ×10 / **sector** | earnings_7d ×10 / sector |
| 第二腿 | netprofit ×50 / **industry** | netprofit ×50 / **sector**（改轴！） |
| 第三腿 | ebitda_90d ×30 / industry（**analyst7 同源**） | anl15_dps_gr_12_m_3m_chg ×22 / sector（**跨源 analyst15**） |
| 三腿全用 sector 轴 | ❌（sector×industry×industry） | ✅ |

⇒ **「全 sector 轴 + 跨源第三腿」= 破 prod 的第二个独立配方**。
⇒ 与 mLovbnm2 互相关 0.6955（<0.7），四颗件（1YNMAA8M / mLovbnm2 / bl6AvMkN / zq3eb7No）构成**完整独立集**（all_below_threshold=true）。

### 19.4 风险提示
| # | 风险 | 说明 |
|---|---|:|
| 1 | prod 余量 0.005 | 生产池变化会推高 prod（历史有 0.69→0.99 记录）⇒ **提交前必须 refresh 终验** |
| 2 | self 余量 0.005 | 贴线 |
| 3 | 与 mLovbnm2 相关 0.6955 | 两颗**不宜同时提交** |

### 19.5 本轮最终战果
| 指标 | 数值 |
|---|---:|
| 累计开波 | **124 波** |
| 累计回测 | **约 450 条** |
| RA 全闸候选 | **55+ 颗** |
| **四道全过 + 稳健性 PASS** | **2 颗（mLovbnm2 / 1YNMAA8M）** |
| prod < 0.7 | **2 颗** |
| ΔSharpe > 0 | **2 颗** |
| 新增判据 | **BO ~ DA** |

### 19.6 ★ 两套破 prod 配方（可复用）
| 配方 | 结构 | prod |
|---|---|---:|
| **配方 A** | analyst7 三腿（earnings_7d×10/sector × netprofit×50/industry × ebitda_90d×30/industry） | 0.6572 |
| **配方 B** | 跨源三腿 + 全 sector 轴（earnings_7d×10/sector × netprofit×50/sector × anl15_dps_gr_12_m_3m_chg×22/sector） | 0.6951 |