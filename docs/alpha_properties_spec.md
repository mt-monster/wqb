# Alpha 提交属性统一规范（v1.0）

> 制定日期：2026-09-20 ｜ 依据：**平台实测返回**（非臆造）
> 配套审计：`reports/alpha_properties_audit_20260920.md`

---

## 零、平台硬约束（实测得出，规范必须迁就它）

| 属性 | 平台行为 | 实测证据 |
|---|---|---|
| **`color`** | **硬枚举，仅 5 个合法值** | `GREEN`/`BLUE`/`RED`/`YELLOW`/`PURPLE` → 200；`ORANGE`/`PINK`/`TEAL`/`GRAY`/`BLACK`/`WHITE`/`NONE`/`CYAN`/`MAGENTA`/`BROWN` → **400 `"X" is not a valid choice.`** |
| **`tags`** | **零约束** | 30 个标签 ✅、100 字符标签 ✅、`a b`/`A/B`/`a.b`/`a:b`/`中文标签` 全部 ✅ |
| **`name`** | **零约束** | 256 字符 ✅ |
| `description` | ≥100 英文词（空则静默丢弃） | 既有约定 |

> ★ **结论**：平台只对 color 有约束，**tags/name 的一致性完全靠我们自己的规范** —— 这正是当前混乱的根因。

**平台侧完整可控属性**（`GET /alphas/{id}` 返回）：
`name` · `color` · `tags` · `hidden` · `favorite` · `regular.description`
（其余 `grade`/`classifications`/`category`/`origin` 由平台裁定，勿动）

---

## 一、color 规范（严格映射到平台 5 色）

**5 色必须各有明确、互斥的语义**，禁止把任一色当"默认值"用。

| color | 语义 | 使用条件 |
|---|---|---|
| **`BLUE`** | **已提交 · 待观察**（默认态） | 刚提交、OS 结果未出（通常 <90 天） |
| **`GREEN`** | **已提交 · 表现正常** | OS 已出且正常（OS sharpe ≥ 0.7 或与 IS 衰减比 ≥0.3） |
| **`YELLOW`** | **已提交 · 指标退化，待复核** | OS 明显弱于 IS、或 IS 指标下滑 |
| **`RED`** | **已提交 · 待退役** | 已打 `RETIRE_*` 标签，等控制台人工退役 |
| **`PURPLE`** | **PPA 通道专用** | 真实走 Power Pool 通道的 alpha |

**变更时机**：
- 提交成功 → 立刻设 `BLUE`
- OS 结果出来后 → 转 `GREEN` / `YELLOW`
- 决定退役 → 转 `RED` + 打 `RETIRE_<date>`

> ⚠️ 现状问题：`GREEN` 被当作 skill/节点的默认值，导致"有绿色"不再代表"表现正常"。**新规范下 GREEN 必须由 OS 结果挣得**。

---

## 二、name 规范

### 格式
```
<REGION>_<R|S>_<family>_<seq>
```

| 段 | 说明 | 取值 |
|---|---|---|
| `REGION` | 3 字母区域码 | `IND` `USA` `KOR` `DEU` `GBR` `EUR` `ASI` `GLB` `HKG` `MEA` `CHN` `JPN` |
| `R`/`S` | 类型 | `R`=REGULAR，`S`=SUPER |
| `family` | 数据集族 / 策略族（小写，≤18 字符） | `pvrevgate`、`analystrev`、`insiderflow` |
| `seq` | 两位序号 | `01`–`99` |

### 示例
```
IND_R_pvrevgate_01        # IND REGULAR，PV 反转+条件门，第 1 颗
IND_R_newssent_03
USA_S_35comp_01           # USA SUPER，35 组件
DEU_R_starminerev_02
```

### ❌ 明令禁止
1. **把 PROD 数值当 name**（`0.6498`/`0.6842`）—— 它是提交时快照，后续变了名字就骗人；
2. **用人名**（`MengTao`）—— 无语义；
3. name 里放与 tags 重复的信息。

> PROD 值是**会变的指标**，应放 `description` 或按需查平台，**不该固化进 name**。

---

## 三、tags 规范（命名空间式）

平台不限制，故我们用**前缀命名空间**保证可机读、可筛选。

### 3.0 先划清界限：平台已自带的，**不要用 tag 重复**

实测 `GET /alphas/{id}` 已原生返回（控制台亦可查）：

| 平台自带 | 字段 | 结论 |
|---|---|---|
| **塔归属** | `pyramids` / `pyramidThemes`（`IND/D1/PV` 等，含 multiplier） | ❌ **不要打 `TOWER_*`**（冗余） |
| 类型徽章 | `classifications`（`REGULAR:REGULAR` / `CLUSTER:CLUSTER`） | ❌ 不要打类型 tag |
| 生命周期 | `stage`（`IS` / `OS`） | ❌ 不要打阶段 tag |
| 区域/设置 | `settings.region` / `universe` / `delay` | ❌ 不要打区域 tag |
| 作者 | `author` | ❌ |
| PROD/SELF 数值 | `prod` / `is.checks` | ❌ 不要打数值 tag（会过期） |
| 收藏/隐藏 | **`favorite`(bool) / `hidden`(bool)** | ✅ **可一键筛，优于自定义 tag** |

> ★ 判据：**平台有的 → 不重复；`favorite`/`hidden` 能表达的 → 优先用原生布尔。**

### 3.1 真正值得打的标签（平台**没有**的维度）

按用途分三层：**必打 / 强烈推荐 / 按需**。

#### 第 1 层 · 必打（溯源自证，全部可自动生成）

| 标签 | 回答什么问题 | 例 | 生成方式 |
|---|---|---|---|
| `CH_REG` / `CH_PPA` / `CH_SUPER` | 走哪条通道 / 配额归因 | `CH_REG` | 提交时已知 |
| `SRC_<dataset>` | **这信号哪来的**（平台不显示 dataset！） | `SRC_insiders1` | 从队列/波次自动取 |

> ★ `SRC_` 是**信息增量最大**的一个 —— 平台完全不知道你的 alpha 用了哪个数据集，只有塔的**类别**（PV/ANALYST/NEWS…），没有具体数据集。

#### 第 2 层 · 强烈推荐（解决本仓已知痛点，可自动生成）

| 标签 | 解决的痛点 | 例 |
|---|---|---|
| **`W<wave>`** | 追溯"哪一波挖的"；波动复盘 | `W113` / `W62` |
| **`EXPRFAM_<family>`** | ★ **防同族自相残杀**（本仓 SELF 0.9+ 实证痛点）—— 组池/再挖时一眼看出同族 | `EXPRFAM_pvrevgate` |
| **`CORR_LOW`** | ★ **SA 组池时快速筛"双闸余量充裕"的组件** | PROD&nbsp;<&nbsp;0.55 且 SELF&nbsp;<&nbsp;0.45 |
| **`CORR_NEAR`** | ★ 标记"贴近红线"（PROD/SELF ∈ 0.65–0.70），提交前需复检 | 避免误用 | 
| `TOOL_<tool>` | 产出工具溯源（gem / tabbit / 手写 / probe） | `TOOL_gem` |

#### 第 3 层 · 按需（人工判断，平台无）

| 标签 | 用途 | 例 |
|---|---|---|
| **`RETIRE_<YYYYMMDD>`** | 退役留痕（API 无法退役，**唯一手段**） | `RETIRE_20260920` |
| `OS_WEAK` / `OS_NEG` | OS 衰减监控（本仓已有 5 颗负 OS 实证） | `OS_NEG` |
| `REVIEWED` | 人工复核通过留痕 | — |
| `TEMPLATE_RISK` | 模板化风险高（论坛经验：模板变体过拟合） | — |
| `EXP_<id>` | 实验编号（一组对照实验） | `EXP_sa20comp` |

### 3.2 防膨胀：一颗 alpha 最多 4–5 个 tag

> 控制台按 tag 筛，**tag 越多越难筛**。超过 5 个说明规范设计过度。

**推荐组合（普通 REGULAR，4 个）：**
```
CH_REG · SRC_<dataset> · W<wave> · EXPRFAM_<family>
```
需要时追加 `CORR_LOW` / `CORR_NEAR` / `RETIRE_*`。

### 3.3 自动 vs 人工分工

| 自动生成（可由提交/入队流程写入） | 人工判断 |
|---|---|
| `CH_*` · `SRC_*` · `W*` · `EXPRFAM_*` · `TOOL_*` · `CORR_*` | `RETIRE_*` · `OS_WEAK/NEG` · `REVIEWED` · `TEMPLATE_RISK` |

> 已实现的 `submit_queue` 已掌握 `region/expr/skeleton`，**`SRC_` / `EXPRFAM_`（骨架签名）可零成本自动生成**。

### 3.4 具体建议（回答"打哪些标签比较好"）

**每颗提交打这 4 个（自动）：**
```
CH_REG                ← 通道
SRC_<来源数据集>       ← 最有信息量
W<波次>               ← 追溯来源波
EXPRFAM_<骨架族>       ← 防自相残杀（可直接用 structural_signature 的族名）
```
**再加条件标签（自动/半自动）：**
- 双闸余量充裕 → `CORR_LOW`（SA 组池优先选这些）
- 贴近红线 → `CORR_NEAR`
**人工按需：** `RETIRE_<date>` / `OS_NEG` / `REVIEWED`

**示例（本会话已提交的 IND alpha）：**

| alpha | 建议 tags |
|---|---|
| `pwRJmvP3` / `ZYbqREW1` | `CH_REG` `SRC_analyst_flash` `EXPRFAM_analystrev` |
| `wpZ1vYzY` | `CH_REG` `SRC_ern3` `EXPRFAM_ern3gate` |
| `levk1d98` | `CH_REG` `SRC_imb5` `EXPRFAM_imb5gate` |
| `Grb67d6O` | `CH_REG` `SRC_news_headline` `EXPRFAM_newsgate` |
| `88j6b1JX` | `CH_REG` `SRC_institutions` `EXPRFAM_instnewsgate` |
| `QPbjxMYw`(SUPER) | `CH_SUPER` `SA_IND_20comp` |

### 3.5 过渡与兼容
- **`PowerPoolSelected`**：**PP 池成分开关**，来源分三类，**2026-11-10 全量复核后修正**。
  - **来源修正（推翻旧记「36 颗均为平台所打」）**：`results/ppa_tag_20261107/patch_tags.py` + `patch_results.json` 实证，11-07 我们曾按指令把 **13 颗** alpha 的 tags 改成 `['PowerPoolSelected']` only。2026-11-10 平台 `tag=PowerPoolSelected` 实查 **66/301 ACTIVE**：24 颗只有单标签（缺 `CH_*`/`SRC_*`，不合规）、28 颗 `CH_PPA`（真 PPA）、9 颗 `CH_REG`（平台自动追加）、5 颗其它。逐颗数据见 `results/ppa_tag_pool_20261110.json`。
  - **平台自动追加是有条件的**：提交后对有 PP 资格/命中当期主题的 alpha 自动打（`P0obGoQJ` 实证带标签），并非每颗必打（`rKRx2Alj` 提交后 8 分钟复查仍 `absent`）。`zq3eb7No` 无标签仍挂 `POWER_POOL_CORRELATION` ⇒ 旧记「无标签不出该项」作废。
  - **提交前绝不预置**：`_derive_tags` 把它从 keep 里剔除。带标签做 PATCH 会让平台按 `PURE_POWER_POOL_THEME` 检查本次提交，合法 REGULAR 可能被直接拒（外部实践者 quantforge-miner 明确记录该坑）。
  - **提交后按 PPA 政策处置**：`submit_alpha` Step 6 `tag_disposal` 回读平台 tags 并留痕（`kept` / `absent` + `pre_submit_has_ppa_tag`）。
  - **★ 以 CPPAP 为目标时，标签是核心杠杆**：标签决定哪些 alpha 计入 Combined Power Pool Alpha Performance；摘掉差货 = 直接提高组合表现，且**可逆**（官方帖 `33099321751447` + 论坛 `44230497234839` 实测加回后下一次刷新即生效）。旧记「清掉 = 放弃 CAP 四口径之一，取最大故损失≈0」只在**以 CAP 总分为目标**时成立；用户明确以 CPPAP 为目标时不成立。
  - **治理规范**：提交后**不要默认清**平台自动追加的标签；按质量治理池子——摘「margin<10bp 且 TO>0.15」的拖后腿件（论坛 `44230497234839`），**别摘**低换手边缘货（实测 BC 反掉 .053）；给未带标签的好货**追加**标签（总数≤5，只能在提交后）。一次只动一条、等约 6 小时刷新读 BC/AC 做对照。24 颗单标签用 `tools/alpha_properties.py normalize --apply` 补 `CH_*`/`SRC_*`（工具无条件保留 `PowerPoolSelected`）。完整方案见 `output_report/ppa_tag_governance_20261110.md`。
  - **`check_tags` 不再把它算违规**（2026-11-08 撤下），改走 `tag_notes` 信息项——否则审计会刷大量假告警，盖掉真正要修的缺 `CH_*` / 缺 `SRC_*`。
  - **★★★ 前置条件修正（2026-11-10 实测，优先于上面所有治理规则）**：标签只是**开关**，平台 `themes` 才是**当期资格**。实测给 `O07AMoKR` 补 `PowerPoolSelected` 后 `themes` 仍为 `[]`；摘掉 `JjeMlmXA` 的标签后 `themes` 仍含 `GLB/D1 Power Pool Nov'26` ⇒ **PATCH tags 不改变 themes**。全账户 301 颗 ACTIVE 仅 **1 颗**命中当期 Nov'26 主题，其余带标签货命中 Sept'26(10)/Oct'26(2)/Aug'26(1) 往期主题或无主题。
    ⇒ 判定顺序必须是 **`themes` 命中当期主题 → 再看标签 → 再看质量**；只有前两项都满足，摘/补标签才影响当期 CPPAP（论坛 `44230497234839`：「带了标签却没挂主题的，是类别不在这期里」；交满 5 条才够评奖）。
    ⇒ 因此**不要**无条件按「margin<10bp 且 TO>0.15」批量摘标签，也不要给无主题货批量补标签。11-10 两条实验（摘 `JjeMlmXA` / 补 `O07AMoKR`）已全部回滚，平台零净变化。主题扫描见 `results/ppa_theme_scan_20261110.json`，四步台账见 `results/ppa_tag_governance_log.jsonl`。
  - **★ 通道判定（2026-11-10 修正）**：`PowerPoolSelected` **不是 PPA 通道证据**。`submit_verdict_core.is_ppa_alpha` 与 `tools/alpha_properties.py normalize` 已改为只认 `type=PPA` 或 `CH_PPA` 标签；旧实现会把平台自动追加标签的 RA alpha 错判成 PPA，违反「只认 RA 全闸」。守护测试 `tests/unit/05_submit_quota/test_ppa_channel_vs_pool_tag_20261110.py`。
- **`RETIRE_20260912` / `RETIRE_20260919`**：**一律不动**（退役留痕的唯一手段）。
- `homework` / `tabbit` 等旧 tag：保留，后续统一为 `TOOL_<x>`。

### 3.6 CPPAP 取向的提交端软标准（2026-11-10 落地）

- **判据顺序不可颠倒**：① 平台 `themes` 是否命中**当期** Power Pool 主题 → ② 是否带 `PowerPoolSelected` → ③ 质量档。只有前两项都满足，标签才影响当期 CPPAP（`themes` 由平台按类别/区域判定，PATCH tags 改不了）。
- **工具**：`tools/gates/ppa_readiness.py`（只读判据，离线快照优先 + 治理台账校正）、`tools/gates/ppa_tag_apply.py`（默认 dry-run，六道安全阀，需 `--confirm` 才写平台）。
- **质量档**：`ANCHOR`（margin≥15bp 且 TO≤0.15，必须留）｜`OK`（≥10bp 且 TO≤0.15）｜`WEAK`（<10bp 且 TO>0.15，论坛双判据的该摘候选）｜`EDGE`（<10bp 且 TO≤0.15，**别摘**，实测 BC 反掉 .053）｜`WATCH`。
- **★ margin 只是软标记，不是提交硬闸**：`MEMORY.md` §8 的 124 颗 USA 真实 OS 实证「IS 指标全不预测 OS」，margin 只是低换手代理（ρ(margin,−TO)=+0.922），设闸会误伤 62% READY 队列。`candidate_soft_flag()` 只产出排序信息、不拦截。CPPAP 虽是扣成本后组合 IR（口径不同），若要改成硬闸**须用户明确裁决**。
- **提交质量口径（论坛 `38846510482967` MZ45384）**：S/F>1、margin 目标 15bp / 最低 10bp、曲线不低头 / 尾年不差、每月专注 2 个区域 + 月底点满塔。
- **池治理纪律**：一次只动一条、等约 6h 刷新读 BC/AC，涨了留跌了加回；当期池 <5 条评奖线时**禁止摘货**（条数越少 BC 越低）；禁止用本地日 PnL 穷举挑组合。
- **边界**：tag 管理只保护 CPPAP，对 Combined/Selected 无效；BC−AC 差值固定 .159–.177 只能靠换货；本地 PnL 近似不可信。

---

## 四、description 规范（沿用既有）

| 类型 | 要求 |
|---|---|
| REGULAR | ≥100 英文词**三段式**：idea（信号定义+经济逻辑） / 数据字段 / 操作符实现 |
| SUPER | selection + combo **两段**，各 ≥100 词；**勿用 `set_alpha_properties`（SUPER 必 400）**，走裸 PATCH |

> 空描述会被**静默丢弃**（无报错），提交前必须回读验证长度 >0。

---

## 五、落库约定（提交时一次性写全）

```python
from wqb.expression.skeleton import structural_signature

payload = {
    "name":   f"{REGION}_{'R' if type=='REGULAR' else 'S'}_{family}_{seq:02d}",
    "color":  "BLUE",                        # 提交即 BLUE（待观察），OS 出来再转 GREEN/YELLOW
    "tags":   [
        "CH_REG",                             # 通道
        f"SRC_{dataset}",                     # 来源数据集（平台不显示，信息增量最大）
        f"W{wave}",                           # 波次
        f"EXPRFAM_{expr_family}",             # 表达式族（防同族自相残杀）
    ] + (["CORR_LOW"] if prod < 0.55 and self < 0.45 else
         ["CORR_NEAR"] if max(prod, self) >= 0.65 else []),
    "regular": {"description": desc},         # ≥100 词三段式
}
```

**自动可生成**：`CH_*` / `SRC_*` / `W*` / `EXPRFAM_*` / `CORR_*` ——
`submit_queue` 已持 `region/expr/skeleton`，接入后**零成本自动打**。

**禁止**：
- ❌ `color` 默认 `GREEN`
- ❌ `tags` 默认 `["PowerPoolSelected"]`
- ❌ `name` 用 PROD 数值
- ❌ 打平台已自带的维度（塔 `TOWER_*`、类型、区域、作者）—— 冗余且挤占筛选条

---

## 六、落地检查清单（已于 2026-09-20 全部完成）

- [x] `src/wqb/alpha_properties.py`：**单一事实源**（`COLORS` 5 值枚举 / `build_name` / `build_tags` / `check_tags` / `resolve_source_dataset` 字段级解析）
- [x] `submit_alpha` 节点：`color` 默认 `BLUE`；`tags` 默认按规范自动生成（保留已有标签）
- [x] `worldquant-submit-alpha/SKILL.md`：PPA 专例 + 普通 REGULAR 示例；已同步 4 安装位
- [x] **存量规范化**：10 个区域 ACTIVE（115 颗）已 `--apply`（tags/color）；57 颗复原原 name + 68 颗补规范名
- [x] `tools/alpha_properties.py`（audit / normalize，默认 dry-run）
- [x] **修复两个严重事故**：
  - 🔴 `set_alpha_properties` 是**全量覆盖**接口（payload 无条件带 `name` 与 `regular.description`）→ 曾清空 115 颗 name、description 覆写为字符串 'None'。已改**最小字段 PATCH**；新增 `tools/restore_alpha_props.py` / `restore_today_5.py` 复原（57 name + 全部 REGULAR desc + SUPER selection/combo）。
  - 🔴 `SRC_` 曾用 `alphas.dataset_id`（波次主数据集，错）→ 已改 `fields` 表按表达式字段反查 + 管道字段剔除。
- [x] **关键工程教训**（已写入记忆）：
  - **PATCH 前先读接口定义是否含字段默认值** —— `set_alpha_properties` 的 `descriptions="None"` 默认值 = 事故根源。
  - **工具写平台前必须先看它对空值的行为**；**改缺省前先读测试**（`submit_alpha` dry-run 契约）。
  - name 推断必须**每颗唯一**（同族同源会撞名）。
