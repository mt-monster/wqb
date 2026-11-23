# mcr27 (macro27) · EUR / TOP2500 / D1 字段画像（2026-11-22 全字段普查）

> 类型 VECTOR · 33/33 字段全量拉取（complete=true）· category = **macro**（×1.2，塔位 2/3 剩 1 席）
> 采集：2026-11-22 · 数据 = LinkUp 招聘 postings（公司级 + bucket 级）

## 0. 可用性分层（全字段）

| 层 | 字段 | αC | cov | 语义 |
|---|---|---:|---:|---|
| **核心流量** | `mcr27_company_jobscreated` | 17 | 0.348 | 当期新建岗位数（**RReEEgwb 用字段**） |
| **核心流量** | `mcr27_company_jobsremoved` | 9 | 0.348 | 当期删除岗位数 |
| **核心存量** | `mcr27_company_jobsactive` | 547 | 0.348 | 当前活跃岗位数（**拥挤字段**） |
| **核心净额** | `mcr27_company_ajnet` | 7 | 0.348 | 净增岗位 = created − removed（**冷字段**） |
| 速度/时长 | `mean_days_job_active`(23)、`mean_days_job_closed`(24)、`avg_days_job_posting_active/closed`(21/10) | ≤24 | 0.348–0.43 | 挂岗时长（分母候选） |
| bucket 级 | `mcr27_bucket_daily_jobsactive/created/removed`(8/6/4)、`bucket_avg_days_*`(30/12) | ≤30 | 0.148 | ⛔ cov 0.148 太薄 |
| 布尔/标识 | verified_ds1-4、is_hosted/repost/sponsored、country、zip、unmapped、companyidmap、normalizedflag、break_flag | ~15 | — | ⛔ 无信号语义（门控/过滤可用） |

**画像结论**：可挖面 = 4 个公司级流量/存量字段（created/removed/active/ajnet）× 挂岗时长分母。机制假设：招聘扩张（净增 postings）→ 预期营收增长 → 正向信号；岗位撤销速度 → 负向信号。

## 1. 已验证机制

`RReEEgwb`（全闸 S2.18/F1.27/2Y2.62/sub1.54/RA-clean，**prod 0.8378 ❌ 撞近重复件**）：
`trade_when(ts_sum(vec_sum(mcr27_company_jobscreated),22)>0, group_zscore(ts_quantile(ts_backfill(divide(vec_sum(mcr27_company_jobscreated), add(vec_avg(mean_days_job_closed),1)),66),252), industry), -1)`
TOP2500/INDUSTRY/decay16。

**prod 撞墙归因**：jobscreated÷挂岗时长 单字段形态在 prod 池已有占位（直方图主体健康 + [0.5,0.6] 孤立桶 n=1 指纹）。

## 2. 第二形态探针（2026-11-22 本轮，multisim `OZ5qQ4SH4Ml8V21biyJt6ZR`，已完）

| 臂 | 机制 | S | F | 2Y | sub | 结论 |
|---|---|---:|---:|---:|---:|---|
| F created÷closed_days@subindustry | 原核换轴 | **2.27** | **1.28** | **2.49** | 1.49 | ★全闸 fRA=0，prod **0.7202**（差 0.02） |
| B removed÷closed_days | 撤岗速度 | 1.11 | 0.45 | 1.34 | 1.17 | 弱，invest 溃 |
| A ajnet÷active_days | 净增速度 | 0.00 | — | — | — | 全零（字段退化） |
| C rank(ajnet) | 秩化 | −0.47 | — | −1.23 | — | 反向无效 |
| D ts_delta(jobsactive,66) | 存量变化 | 0.38 | — | 0.98 | — | 弱 |
| E created÷num_jobs_active | 建岗率 | — | — | — | — | ⛔ UNITS：add(CSShare, 无量纲) 量纲坑 |

**KPgZvxwE prod 直方图**：主体健康（[-0.2,0.2] 占 99.4%）+ 孤立桶 [0.7,0.8] n=1 = 近重复件指纹。换 subindustry 轴已把 prod 从 0.8378→0.7202（−0.12），差 0.02 过线 ⇒ **一次罕见化扰动即可破墙**。

## 3. 第二波方向（**已取消——数据层排除优先于 prod 墙**）

**2026-11-22 逐年复核**：RReEEgwb `get_alpha_yearly_stats` 确认 2014–2020 七年 longCount=0，数据仅 2021–2023 三年 ⇒ 与 11-20 会话结论一致（3 年 < 近九年红线）。KPgZvxwE prod 0.7202 即使破 0.7 也被数据层拦 ⇒ **mcr27 整线关停**（平台补齐 EUR 历史后表达式档案可直接复活）。

原计划的罕见化扰动（ts_delta(22) 快腿 / ts_mean(504) / TOPCS1600 / add 双腿）不再投入配额。

## 4. ★ 2026-11-22 补测：MACRO 席专项（2r5exOvP / N1P8GQnX）+ 重复件陷阱

**新产出（全闸）**（TOP2500 / INDUSTRY / **decay 4** / trunc 0.0）：

| alpha | 轴 | 窗 | S | F | 2Y | sub | TO | prod | self |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **2r5exOvP** | **subindustry** | bf336/q168 | **2.77** | **1.13** | **3.03** | 2.44 | 38.8% | 0.768 ❌ | **0.7703**（撞 GrmmNzz0） |
| **N1P8GQnX** | **subindustry** | bf189/q168 | 2.73 | 1.11 | 2.98 | 2.41 | 38.9% | 0.7656 ❌ | — |
| O0Wgjrn7 | sector | bf189/q168 | 2.25 | 0.86 | 2.68 | 1.98 | 39.5% | — | — |
| RRePoVk0 | industry | bf189/q168 | 2.38 | 0.93 | 2.78 | 2.14 | 38.9% | — | — |
| mLaQNgrx | industry | bf252/q168 | 2.41 | 0.95 | 2.82 | 2.13 | 38.9% | — | — |
| XgaMxW2m | industry | bf189/q336 | 2.14 | 0.81 | 2.48 | 1.99 | 37.6% | — | — |
| ZYaN902Q | industry | bf189/q504 | 1.98 | 0.73 | 2.29 | 1.91 | 37.1% | — | — |
| 88NXZ3KV | industry（宽门控 ts_sum22） | bf189/q168 | 2.36 | 0.90 | 2.81 | 1.78 | 41.3% | — | — |

**★ 两条结论**：
1. **subindustry 轴是 mcr27 的最优轴**：S 2.25（sector）→ 2.38（industry）→ **2.73–2.77（subindustry）**，F 同步 0.86→0.93→**1.11–1.13**。
   ⇒ 该族在 subindustry 轴上首次同时过 S/F/2Y/sub 全闸（此前只卡 F）。
2. **★★ 重复件陷阱（EUR 实证，重要）**：账号内 `GrmmNzz0`（mcr27 created÷closed_days，**已提交**）与上述 2r5exOvP/N1P8GQnX **self 相关 0.7703** ⇒
   - 两颗新件的 prod 直方图都出现**同一个孤立桶 [0.7,0.8] n=1**（= 母件本身）⇒ prod 0.766/0.766；
   - ⇒ **同信息源的变体在本账号已占位后，prod 天花板 ≈ 0.76+**，参数/轴/窗全改无效（EUR skill §16 复现）。
   ⇒ **MACRO 席必须换信息源（不同机制核），不能换形态**。

**机制核清单（供后续换核）**：
| 核 | 字段 | 状态 |
|---|---|---|
| 招聘量/时长 | `mcr27_company_jobscreated` ÷ `mean_days_job_closed` | ⛔ 已占位（GrmmNzz0 已提交） |
| 撤岗量/时长 | `mcr27_company_jobsremoved` ÷ `mean_days_job_closed` | 🔄 批13 在飞 |
| 存量/时长 | `mcr27_company_jobsactive` ÷ `mean_days_job_active` | 🔄 批13 在飞 |
| 净增/时长 | `mcr27_company_ajnet` ÷ `mean_days_job_active` | ⚠ TOP2500 实测 S=0（全零），不可用 |

## 5. 禁区/注意

## 3. 禁区/注意

- ⛔ bucket 级字段 cov 0.148 全部排除
- ⛔ `mcr27_company_jobsactive` 裸值（aC547 拥挤，prod 先验差）
- cov 0.348 → 覆盖薄，信号若住小盘会放大 CW 风险（同 earnings6 教训）
