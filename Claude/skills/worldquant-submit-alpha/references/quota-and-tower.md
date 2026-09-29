# 提交配额（ET 日历日）与点塔优选

> 本文是**提交配额模型**与**点塔优选规则**的唯一叙述（其他 skill 只引用：judge 的点塔提示、superalpha 的配额、INDEX 的配额口径均指向这里）。
> 只写规则与来源；证据链（2026-08-12 / 08-31 的三重实证等）属变更记录，不在正文。

## 1. 配额模型

- 每个 **ET（美东）日历日**：**REGULAR 4 + SUPER 1 + PPA（`POWER_POOL_SUBMISSION`）1**，三者**并行、互不占用**。**00:00 ET 重置**。
- 00:00 ET 换算成 GMT+8：**夏令时 12:00，冬令时 13:00**（美国 DST 2026-11-01 结束）。不要在文档里写死「12:00」——现值以 `python tools/quota_status.py`
  的输出为准（它由 `wqb.timeutil.et_reset_hour_gmt8` 计算；`pipeline.py` 的配额闸用同一口径）。
- 硬闸 FAIL 的 POST 不消耗配额（status 保持 `UNSUBMITTED`）。**但通过的 POST 就是真提交**，所以「失败不扣配额」只描述失败那一半，
  **不能拿来当零成本探测**（见 `submit-chain.md` §0）。

### 1.1 数据来源（各能回答什么）

| 要回答 | 用什么 | 注意 |
|---|---|---|
| 今天（ET）已提交几颗 | `python tools/quota_status.py`（列 `stage=OS`，按 `dateSubmitted` 数当前 ET 日） | **不区分** REGULAR / SUPER / PPA；零成本、不 POST |
| 某一类型的用量 / 上限 | POST 响应里 `REGULAR_SUBMISSION` / `SUPER_SUBMISSION` / `POWER_POOL_SUBMISSION` 的 `value` / `limit`（value 从 0 起；limit = 4 / 1 / 1） | 只有**发出 POST 才有**；`REGULAR_SUBMISSION: FAIL` 且 `value ≥ limit` = 当日用尽 |
| ✗ **不可用** | `GET /users/self/activities/submissions`（只有 yesterday / current / previous / ytd 快照，**没有 today**，`ytd.end` 停在昨天——2026-09-21 曾据此误判「今日 0 提交」）；`GET /alphas/submission-limit`（404）；`get_submission_quota` MCP 工具（已移除） | |

### 1.2 复检与撞墙

- **批量提交前 30 秒内复检一次**：用 `quota_status.py`（**不要**为复检再发一次 POST）。并行会话共用同一账号配额——2026-09-25 当日 4 REGULAR + 1 SUPER 被另一会话用光，本会话准备好的候选一颗未提。
- 撞墙（403 `REGULAR_SUBMISSION value ≥ limit`）= **配额用尽，不是候选缺陷**：停、**不判死候选**、记「待次日」、不重试。换日即恢复；SUPER / PPA 各自独立。

## 2. 点塔优选（多个候选都过闸时：提谁、按什么顺序）

**总准则：优先提能点亮「未点亮」金字塔塔的 alpha；同档内在塔 / 区域间轮转，再按绩效排序。**（CLAUDE.md：一座塔需要 3 颗点亮，尽可能多点塔，点塔要均匀。）

### 2.1 塔与点亮口径（三层，均经平台 / UI 实证）

1. **塔 = 平台 alpha 的 `pyramids[].name`**，形如 `IND/D1/RISK`（区域 / 延迟 / 数据集类别，带 multiplier）。
2. **点亮 = 该 catalog 下「近 90 天内提交」的 ACTIVE ≥ 3 颗**。窗口外的老 alpha 不计（实证：USA/FUNDAMENTAL 平台计 5 颗，其中 4 颗是 2025-09 ~ 2026-01 的老 alpha → UI 未亮）。
3. **跨 ≥ 3 个 catalog 的 alpha 不计点塔**（`pyramidThemes.effective`：1 塔→1、2 塔→2、**3 塔→0**）。挂 1–2 塔的每塔都算（含「搭车」副塔）。
4. **0 亮区域的单颗提交 ≠ 点亮**：GLB / HKG / DEU / ASI / GBR 全域 0 亮时，提 1 颗只是「打地基」（该塔 0→1），要凑满 3 颗同类才亮。「0 亮区域 = 点塔主战场」指挖矿主战场，不是「提 1 颗就点亮」。

权威入口：`python tools/campaign_intel.py pyramid --region <R> --delay <D>`（口径 `WINDOW_DAYS=90` / `EXCLUDE_MULTI=3` / `MIN_LIT=3`；平台 `status=ACTIVE` 全量 → 按 `pyramids` 逐个计数 → 剔跨 ≥ 3 catalog → 剔 90 天窗口外）。

### 2.2 排序（多候选时）

1. **一次点亮**：该塔现状 2/3（**差 1 颗**）的候选排最前——提交后恰好 3 颗。（"差 1–2 颗一次点亮" 是旧文的错误：差 2 颗的塔一次提交仍差 1 颗。）
2. 其次该塔现状 1/3（**差 2 颗**）：一次提交后 2/3，还要再来一颗。
3. 再次 0/3（**差 3 颗**，0 亮区域打地基）：要凑满 3 颗同类才亮。
4. **同档内先在塔 / 区域之间轮转**（不要连续把 3 颗都给同一区域或同一塔——「点塔要均匀」），轮转后仍并列者按 **fitness 降序，其次 sharpe**。
5. **区域是否「已过度提交」没有机器阈值**：不自行判断，把该区本季度已提交数（`campaign_intel.py pyramid` 输出）连同候选一并列给用户拍板。

### 2.3 候选将点亮哪座塔（预测；未提交 alpha 的 `pyramids` 恒为空）

- 本地 `alphas.dataset_id → datasets.category` → 拼 `{REGION}/D{delay}/{CATEGORY.upper()}`。
- 缺失时按**表达式字段反查** `fields` 表（多数票）。仍 UNKNOWN → **不预测**：标 `UNKNOWN`，不把它计入「一次点亮」的收益，交用户判断。
- 平台字段权威确认：单字段端点 `GET /data-fields/{field}?region=&universe=&delay=`（**没有 MCP 封装**；MCP 的 `get_datafields(search=…)` 是另一条列表路径，两者用途不同，本文不要求手写 GET，需要确认时优先 `get_datafields`）。

### 2.4 对表达式构造的反向约束（挖新候选时；细则在 S0 / S1 步骤）

想给某塔 +1：**纯单类别数据集 alpha 最干净**（挂 1 塔）；混 2 类挂 2 塔（各 +1）；**混 3+ 类 = 白提**（对点塔零贡献，不管指标多好）。选题阶段见 ra-pipeline 步 2。
