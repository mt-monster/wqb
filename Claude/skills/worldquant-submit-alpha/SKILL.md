---
last_verified: 2026-09-28
name: worldquant-submit-alpha
description: "通过 API 将 WorldQuant Brain alpha 真正提交（submit）到平台（不只是模拟 simulate）。 当用户对某个 WQ alpha id 说\"提交 alpha / submit / 上平台 / 落地\"时使用。覆盖关键坑： POST /alphas/{id}/submit 返回 201/200 但 status 因 regular.description 过短而永不翻转， 以及正确的嵌套 description PATCH 写法；并说明约 2 分钟的状态翻转延迟与轮询方法。★2026-09-01 新增「点塔优先提交规则」：提交前按金字塔点亮价值优选（点亮=该 catalog 近 90 天提交 ≥3 颗；跨 ≥3 catalog 的 alpha 不计；差 1-2 颗的塔一次提交即点亮，0 亮区域的单颗提交不算点亮）。"
layer: L5
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







# WorldQuant Brain — 实际提交 Alpha 到平台

## 职责边界

- **本 skill 负责**：**REGULAR 单颗 alpha 的真实提交**：`POST /alphas/{id}/submit`，处理四种响应形态①②③④与异步补发，以及 name/description/tags/color 属性规范
- **本 skill 不做**：**不处理 SUPER 组套**（→ `wq-brain-superalpha`）；**不覆盖 PPA**（PPA 属 web UI 手动流程，本 skill MCP 工具链只覆盖 REGULAR）；**不作提交判定**（判定 = `tools/submit_verdict.py` 模拟层 + 参考视图，最终以 POST 实测为准）；不改表达式
- **上游 / 下游**：上游 = 用户已确认的候选；下游 = `ACTIVE` alpha + S6 台账


## 何时用
用户要把某个已模拟出的 alpha（已知 platform_id，如 `YPgAa3WR`）真正提交到 WQ
平台参与评审/进入 power pool。注意：很多脚本里的 `submit` 只是本地打标/记录，
并没有调用平台提交端点。本 skill 解决的是**真正落到平台**的那一步。

## 衔接协议
- **上游**：S5 判定 `tools/submit_verdict.py`（模拟层 + 参考视图，最终以 POST 实测为准；SUBMITTABLE 且 type=REGULAR 单颗；IS 硬闸全 PASS、description 已按三段式补齐；brain-alpha-judge 参考评审可为点塔排序提供输入）。
- **本 skill 角色**：S5 落地执行——真正提交到平台并确认 status 翻转为 ACTIVE。
- **下游**：S6 `wq-backtest-monitor`（OS 表现监控；§14 台账回写 `wave_results` + `registry_empirical` 反哺 S-PRE）。

## 前置
- **MCP 优先**：平台交互首选 `mcp__wq-brain-http__*` 工具（自带重试/超时配置），禁止手写 requests 脚本。
- 凭据在 `world-quant-brain-mcp` 项目根目录的 `.env`：`CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（MCP 服务端自动加载）。
- 运行环境（仅 fallback 需要）：**`$WQ_PY`**。

## 提交流程（MCP 工具调用）

> **属性规范（2026-09-20 起强制）**：`name` / `color` / `tags` 必须遵循
> `docs/alpha_properties_spec.md`（仓库根相对路径），单一事实源为
> `src/wqb/alpha_properties.py`。
> - `color`：平台**仅接受 5 个值** `GREEN/BLUE/RED/YELLOW/PURPLE`（其余 400）。
>   **提交态默认 `BLUE`（待观察）；`GREEN` 须由 OS 结果挣得，禁当默认值。**
> - `name`：`<REGION>_<R|S>_<family>_<seq>`。**禁止用 PROD 数值**（提交时快照，会过期骗人）。
> - `tags`：`CH_<通道>` + `SRC_<数据集>` 必打，可选 `W<波次>` / `EXPRFAM_<族>` / `CORR_<档>`。
>   一颗最多 4–5 个。**`PowerPoolSelected` 仅真实 PPA 通道可用**（普通提交用 `CH_REG`）。
> - **平台已自带的不要重复打**：塔（`pyramids`）、类型、区域、作者、`stage`。

**推荐**：使用 `mcp__wq-brain-http__workflow_submit_alpha` MCP 工具（workflow 引擎快捷方式，含预检 + 属性设置 + 提交 + 状态轮询）：

```
# 【普通 REGULAR 提交】—— 默认形态

mcp__wq-brain-http__workflow_submit_alpha(
  alpha_id="<ALPHA_ID>",
  name="IND_R_pvrevgate_01",        # <REGION>_<R|S>_<family>_<seq>，勿用 PROD 数值
  color="BLUE",                     # 提交态=待观察；GREEN 要等 OS 结果
  tags=["CH_REG", "SRC_insiders1", "W113", "EXPRFAM_insgate"],
  dataset="insiders1",              # 给了这些则 tags 可留空自动生成
  wave="113",
  expr_family="insgate",
  descriptions="Idea: <idea>\n\nRationale for data used: <rationale>\n\nRationale for operators used: <rationale>",
  confirm_submit=True,              # 默认 False 仅预检+查状态；True 才真正提交
  verify_timeout=180
)
```

```
# 【PPA（Power Pool）提交】—— 本 skill MCP 工具链不覆盖 PPA，勿经 MCP 提交。
# 合法 PPA 必须走平台 web UI 手动提交（见下方「★ PPA 通道」节）。
```

**分步模式**（需逐步控制时）：

```
# 1) 设置属性（description 必须三段式）
mcp__wq-brain-http__set_alpha_properties(
  alpha_id="<ALPHA_ID>",
  name="IND_R_pvrevgate_01",
  color="BLUE",
  tags=["CH_REG", "SRC_insiders1", "W113"],
  descriptions="Idea: <idea>\n\nRationale for data used: <rationale>\n\nRationale for operators used: <rationale>"
)

# 2) 提交（经 workflow 引擎，自带 IS 预检 + 状态轮询）
mcp__wq-brain-http__workflow_submit_alpha(alpha_id="<ALPHA_ID>", confirm_submit=True, force=False)
# force=True 仅限人工确认后显式豁免（跳过 submit_gate + robustness_audited 两道 fail-closed 闸），留痕于 workflow 记录

# 3) 确认状态翻转
mcp__wq-brain-http__get_alpha_details(alpha_id="<ALPHA_ID>")
# 成功标志：status == "ACTIVE"（或 "SUBMITTED" 后转 "ACTIVE"），dateSubmitted 有值
```

### Fallback：手写脚本（仅 MCP 不可用时）
**警告**：手写脚本必须处理 `Retry-After` 头 + 指数退避，禁止固定退避（30+15s×n 会连续 429 空转）。

注：代码块中尖括号内容（如 `<ALPHA_ID>`、`<FIELD>`）为占位符，使用时替换。
```python
import os, time, requests
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv(r"world-quant-brain-mcp/.env")
s = requests.Session()
s.auth = (os.environ["CREDENTIALS_EMAIL"], os.environ["CREDENTIALS_PASSWORD"])
BASE, AID = "https://api.worldquantbrain.com", "<ALPHA_ID>"

# 1) 必须先补一个合规的 regular.description（关键！否则提交被网关静默丢弃）
desc = ("PPA alpha on USA TOP3000 EQUITY. Signal = rank(group_zscore("
        "ts_zscore(ts_backfill(<FIELD>, 66), 189), industry)). "
        "<数据来源与逻辑说明，>=100 字，说明信号/数据/中性化/周期>")

# PATCH with Retry-After + exponential backoff
for attempt in range(12):
    r = s.patch(urljoin(BASE, f"alphas/{AID}"),
                json={"name": "ppa_xxx", "regular": {"description": desc}, "color": "GREEN"})
    if r.status_code in (200, 201, 202):
        break
    if r.status_code == 429:
        retry_after = int(r.headers.get("Retry-After", 30))
        time.sleep(retry_after + attempt * 10)
    else:
        r.raise_for_status()
assert r.status_code in (200, 201, 202)

# 2) 提交
r = s.post(urljoin(BASE, f"alphas/{AID}/submit"))   # 期望 200/201/202
assert r.status_code in (200, 201, 202)

# 3) 轮询（status 翻转有 ~2 分钟延迟，别只等几秒就判失败）
for _ in range(36):   # 最多 3 分钟
    d = s.get(urljoin(BASE, f"alphas/{AID}")).json()
    if d.get("status") and d.get("status") != "UNSUBMITTED":
        break
    time.sleep(5)
# 成功标志：status == "ACTIVE"（或 "SUBMITTED" 后转 "ACTIVE"），dateSubmitted 有值
```

## 关键坑（必读）
1. **POST 的 4 种响应形态（2026-09-26 实测重写；此前本节把 ②③ 误诊为「description 过短」）**：

   | # | 响应 | 含义 | 处置 |
   |---|---|---|---|
   | ① | `200` + `{"success":true,"reason":"IS checks passed","checks":[…]}` | **明确通过** | 轮询至 `status=ACTIVE` |
   | ② | `201/202`「Accepted (async); IS checks still computing」 | **异步受理**（客户端只等 60s：`_poll_submit_until_resolved` 6×10s 即放弃） | 等 4 分钟；`get_alpha_details` 查 `status` 仍 `UNSUBMITTED` → **re-POST 补发** |
   | ③ | `200` + 「Non-JSON submit response」+ **空体** | **异步受理、结果未知** | 同 ②：**必须补发**，**不得当成失败** |
   | ④ | `403` + JSON `{"is":{"checks":[…]}}` | **失败**，但**零成本**且回带**全量 checks 与真因** | 读唯一 FAIL 项定位（见下条） |

   实证（2026-09-26）：`O0GjWqeY` / `2rpX85Ax` / `np8VGNz3` 走 ②③ 后未被补发 → 悬空 `UNSUBMITTED` >24h。
   **`regular.description` 过短是另一条独立成因**（网关静默丢弃，需补 ≥100 字合规嵌套描述），勿与 ②③ 混为一谈。

2. **403 的真因读法（2026-09-26 实测）**：403 体里 `is.checks` 的 **`result` 有三种**——`PASS` / `WARNING` / `PENDING`，
   外加 `FAIL`。**`PENDING` ≠ `FAIL`**：`SELF_CORRELATION` / `PROD_CORRELATION` 未算完时就是 `PENDING`，
   **不挡提交**，不要据此判死。真正拦阻的是 `FAIL` 项，最常见的有两种：
   - **`REGULAR_SUBMISSION: FAIL value=4 limit=4`** —— **ET 日配额用尽**（非候选缺陷！换日即失效，
     `SUPER` / PPA 的 `POWER_POOL_SUBMISSION` 是各自独立通道）；
   - 任一硬指标 `FAIL`（如拟合/换手/子宇宙）—— 这才是候选本身的问题。
   `PASS_CHEAP` / 模拟层干净 **都不能替代**这一步 POST 实测。
2. **description 的 PATCH 形式**：用**嵌套** `{"regular": {"description": "..."}}`。
   用扁平的 `{"description": "..."}` 会被 `400 {"description":["Unexpected property."]}` 拒绝。
3. **翻转延迟**：提交成功后 `status` 不会立刻变，通常等 **2~3 分钟**才从
   `UNSUBMITTED` 翻转为 `ACTIVE`。轮询窗口要够长。
4. **提交后 IS check**：提交成功后再 `GET /alphas/{id}/check` 只会返回
   `ALREADY_SUBMITTED: FAIL`（代表不可重复提交），属正常，原 21 项闸门结果已锁定。
5. **`GET /alphas/{id}/submit` 在本平台恒返回 `404` + 空体——不要用它做任何判定**（2026-09-26 实测：
   对未提交的 `O0GjWqeY` 与**已 ACTIVE 的** `MPabNeNz` 同样 404）。历史文档对此有三种互相矛盾且都错的
   说法（"text/html SPA 壳" / "403 盲区唯一权威" / "可直接走 POST"）；**真相是：提交层的信息只存在于
   `POST` 响应里**（四种响应形态①②③④，见第 1 条）。据此也修正一点：`tools/submit_verdict.py` 的
   提交层视图走的就是这个恒 404 的 GET，故其 403 分支是**死代码**，对处女候选只会给 `UNVERIFIABLE`
   （不构成可提交依据，见 ra-pipeline 步 1）——**真闸只能靠 POST**。
6. **提交前必做平台 IS 核验（关键！）**：`scan` 的 `PASS_CHEAP` 本地判定**不会**
   评估 `SELF_CORRELATION` / `PROD_CORRELATION` 等硬闸门，易出现假阳性。核验读
   `get_alpha_details(id)` → `is.checks`（**没有** `get_alpha_check` 这个工具，旧文档名是错的），
   确认 **无 `FAIL`**（`WARNING`/`PENDING` 不挡）。self_corr 0.87~1.0 属结构性黏滞信号，
   无法靠补 description 救活，只能重挖低自相关变体。PASS_CHEAP ≠ 平台可提交。
7. **提交路由已 fail-closed 前置（2026-09-29 P0，`submit_alpha` 节点强制）**：
   `workflow_submit_alpha`（或 `submit_alpha` 节点）在真正 POST 之前，会自动跑两道闸——
   ① `submit_gate`：`is.checks` 里模拟层 `FAIL` / 提交层硬闸 `WARNING`（LOW_SHARPE/LOW_FITNESS/
   LOW_2Y_SHARPE）/ WebDataScope `Failed RA/PPA≠0`（= brain-alpha-robustness Phase B.0 硬门），
   任一命中即拒绝提交（`force=True` 仅限人工确认后显式豁免，留痕于 workflow 记录的 plan/steps 字段）；② `robustness_audited=True` 显式声明（补齐
   Phase B/C 逐年归因），`confirm_submit=True` 时缺省拒绝。**不是靠 Agent 记得调 robustness，
   而是不声明就提交不出去。** 预检失败/无 `is.checks` 也 fail-closed 阻断（不再放行）。
8. 配额查询：`GET /alphas/submission-limit` 路径不存在（404），不要依赖它判断剩余额度。
   **REGULAR 余量的唯一可靠来源 = `POST /alphas/{id}/submit` 响应里 `REGULAR_SUBMISSION` 的
   `value/limit`**（value 从 0 起计数，limit=4；`SUPER`=1、PPA `POWER_POOL_SUBMISSION`=1 各自独立）；
   `activities/submissions` **缺 `today` 字段、不可用于当日判断**。辅助：`tools/quota_status.py`
   （按 `stage=OS` 的 `dateSubmitted` 数当日颗数，但**不区分类型**，会与 SUPER 混计）。
   ⚠ **并行会话消耗同一账号配额**——2026-09-25 当日 4 REGULAR + 1 SUPER 全被另一会话用光，
   本会话准备好的候选一颗未提。批量提交前 30 秒内必须复检一次。

## ★ 点塔优先提交规则（2026-09-01 用户定案，提交前必读）

**总准则：优先提能点亮「未点亮」金字塔塔的 alpha；同档内按绩效（fitness 降序）排序。**
这条规则用于「多个候选都过闸时提谁、按什么顺序」的优选把关。

### 塔与点亮口径（三层，全部经平台/UI 实证）
1. **塔 = 平台 alpha 的 `pyramids[].name`**，形如 `IND/D1/RISK`（区域/延迟/数据集类别，带 multiplier）。
2. **点亮 = 该 catalog 下「近 90 天（一个季度）内提交」的 ACTIVE ≥3 颗**。
   实证：USA/FUNDAMENTAL 平台计数 5 颗但 4 颗是 2025-09~2026-01 老 alpha → UI 未亮；
   USA/PV 计数 3 颗（含 2 颗老）→ UI 未亮。**窗口外老 alpha 不计数**。
3. **跨 ≥3 个 catalog 的 alpha 不计点塔**（平台 `pyramidThemes.effective` 实证：1 塔→1、
   2 塔→2、**3 塔→0**）。挂 1-2 塔的 alpha 每塔都算（含"搭车"副塔，平台认可）。
4. **★ 0 亮区域的单颗提交 ≠ 点亮**：GLB/HKG/DEU/ASI/GBR 全域 0 亮时，提 1 颗只是
   "打地基"（该塔 0→1），**要凑满 3 颗同类提交才点亮**。"0 亮区域 = 点塔主战场"是指
   挖矿主战场，不是"提 1 颗就点亮"。

### 提交优选排序（多候选时）
1. **能一次点亮塔的优先**（该塔现状 ≥2/3，差 1-2 颗）：先跑 `python tools/campaign_intel.py pyramid --region <R> --delay <D>` 或
   `tools/submit_verdict.py` 拿每塔当前颗数，找「差 ≤2 颗」的塔 → 对应候选排最前。
2. 其次**该塔现状 1/3（差 2 颗）** 的候选。
3. 再次**0/3 需凑 3 颗**（0 亮区域打地基）的候选。
4. 同档内按绩效：**fitness 降序，其次 sharpe**。
5. 已过度提交的区域（如 MEA 本季度）**不提交**，候选只罗列交用户拍板。

### 候选将点亮哪座塔（预测，未提交 alpha 的 pyramids 恒为空）
- 本地 `alphas.dataset_id → datasets.category` → 拼 `{REGION}/D{delay}/{CATEGORY.upper()}`
- 缺失时**表达式字段反查** `fields` 表（多数票）；仍 UNKNOWN 则按该区域未亮类别保守判断，
  别硬说"新塔"（本地 fields 缺 USA/部分 IND/KOR 字段）。
- 平台字段权威确认：`GET /data-fields/{field}?region=&universe=&delay=`（单字段端点；
  列表接口带 search 会返回 `["Invalid query"]` 不可用）。
- 已点亮塔统计：平台 `status=ACTIVE` 全量拉取（响应键 `results`）→ 按 `pyramids` 逐个
  计数（dual-dataset 对两塔各 +1）→ 剔跨 ≥3 catalog → **剔 90 天窗口外** → ≥3 点亮。
  权威入口 = `python tools/campaign_intel.py pyramid --region <R> --delay <D>`（口径 WINDOW_DAYS=90 / EXCLUDE_MULTI=3 / MIN_LIT=3）。
  （2026-09-26 审计：旧文档指向的 `tracking/_submit_kit/_tower_map.py` 与 `_quota_now2.py` **整个目录都不存在**，已改为真实工具。）

### 对表达式构造的反向约束（挖新候选时）
- 想给某塔 +1：**纯单类别数据集 alpha 最干净**（挂 1 塔）；混 2 类挂 2 塔（两塔各 +1）；
  **混 3+ 类 = 白提**（对点塔零贡献，不管指标多好）。

## 验证清单
- `mcp__wq-brain-http__get_alpha_details` 返回 `status=ACTIVE`（或 SUBMITTED→ACTIVE）、
  `dateSubmitted` 非空 → 成功。
- 所有硬闸门此前已 PASS（平台硬线：ProdCorr<0.7、SelfCorr<0.7；内部从严线：LOW_SUB_UNIVERSE_SHARPE≥0.9——平台判据是公式 `≥0.75×sqrt(子域/全域)×sharpe`，见 `brain-how-to-pass-alpha-test`）。
  WARNING（描述长度/格式/主题）不挡提交，但描述过短会导致上面的静默丢弃。

## SuperAlpha（type=SUPER）提交
单颗 REGULAR 的提交见上。若要把 **≥10 颗同区域已 ACTIVE 的 REGULAR alpha** 合成为一颗 SUPER alpha，
完整方法论（selection/combo 语法、neutralization 逐区扫描杠杆、`mcp__wq-brain-http__workflow_submit_alpha(confirm_submit=True, force=True)` 两次取 verdict、组件前置、
`mcp__wq-brain-http__run_selection` 误区）见独立 skill **`wq-brain-superalpha`**。要点：
- SUPER 需 `selection` + `combo` 两段表达式，**description 用裸 PATCH 写入**：
  `PATCH /alphas/{id}` body 只带 `{"selection":{"description":...},"combo":{"description":...}}`，
  各 **≥100 英文字**；`set_alpha_properties` 对 SUPER 必 400（无条件带 regular 字段）。
- `combination(alpha(...))` 现已不可用，必须用 selection+combo 工作流。
- 提交同样受 ET 日历日配额限制（REGULAR 4 颗/ET 日 + SUPER 1 颗/ET 日；硬闸门 FAIL 不消耗配额，属零成本探测）。
- SUPER alpha **不点塔**（pyramids 恒为空），点塔只看 REGULAR。

## 不要在已提交 alpha 上重跑
已提交后 `POST /submit` 幂等返回 200，但会浪费额度/产生混乱。确认
`dateSubmitted` 已落库即停。

## 提交前 ET 日历日配额闸（2026-09-01 定案，推翻"48h 滚动"旧记）
配额模型 = **REGULAR 4 颗/ET 日历日 + SUPER 1 颗/ET 日历日**，**00:00 ET（= 12:00 GMT+8）重置**。
三重实证：①08-12 一次 48h 内提交 6 颗全成功→证伪 48h 滚动；②08-31 08:5x ET 平台报
`REGULAR_SUBMISSION=1`（当时 ET 日内仅 1 颗，24h 滚动应为 2）→证伪 24h 滚动；③平台注释
`daily_remaining` 明确 = 本地日上限 4/day。
- `get_submission_quota` MCP 工具已于 2026-08-25 移除，**不要依赖它**。
- 剩余额度从 submit 响应 `REGULAR_SUBMISSION` / `SUPER_SUBMISSION` check 的 `value/limit` 读
  （value 从 0 起计数，limit=4/1）；硬闸 FAIL 的提交**不消耗**配额（status 保持 UNSUBMITTED）。
- 当日 REGULAR 真值唯一认 POST 响应 `REGULAR_SUBMISSION.value/limit`；`activities/submissions` 缺 `today` 字段，不可用于当日判断。
- 可复用：`python tools/quota_status.py`（按 `stage=OS` 的 `dateSubmitted` 数当日颗数；**不区分 REGULAR/SUPER**，
  只作辅助），当日 REGULAR 真值仍以 POST 响应 `REGULAR_SUBMISSION.value/limit` 为准。

### ★ PPA 通道（POWER_POOL_SUBMISSION，1/ET 日，2026-09-12 补全）

PPA 是**独立日配额**（`POWER_POOL_SUBMISSION` limit=1/ET 日），与 REGULAR 4/日、SUPER 1/日**并行不互占**——每天先提 PPA 那颗是既定纪律。但它有两条关键约束（2026-09-12 从 `brain-alpha-robustness` 上浮，此前散落导致通道长期零使用）：

1. **MCP `submit_alpha` 不是 PPA 感知的**：它内置常规 RA 闸（实测 Sharpe>1.3 / Fitness>0.75 / Margin>15bp），对合法 PPA 照拦（打 `PowerPoolSelected` 标签重试仍拦）。即**自动化通道无法放行 Sharpe<1.3 的合法 PPA**。
2. **合法 PPA（Sharpe≥1.0 / 算子≤8 / 字段≤3 / PC<0.5）必须走平台 web UI 提交**，且仅在**当期活跃 Power Pool 主题窗口**内（主题轮动看平台右上角铃铛；`MATCHES_THEMES`=PASS 才受理）。非活跃区域提交报 "does not match any Power Pool Theme"。

提交流程：提交前本地 `brain-calculate-alpha-selfcorr-quick` 算 PPAC（≤0.5 才走 PPA 通道）→ web UI 手动提交 → 回写 submission_ledger（submission_type=`PPA`）。


## 工具化纪律（tools/ 通用工具，勿再写一次性脚本）

提交层判定与批量提交一律走通用工具，**不要手写 `GET /alphas/{id}/submit` 或 `_submit_*.py`**：

```powershell
# submit_verdict = 模拟层 + 参考视图（最终以 POST 实测为准；GET /submit 恒 404 勿用于判定）
& $WQ_PY tools/submit_verdict.py --alpha-id <ALPHA_ID>

# 批量提交（多批规格走 --spec JSON 文件通道，避免引号事故）
& $WQ_PY tools/submit_batch.py --path <exprs.json> --region <R> --decay <D> --neutralization <N>
& $WQ_PY tools/submit_batch.py --spec <spec.json> --dry-run
```

配额口径：ET 日历日 **REGULAR 4/日 + SUPER 1/日 + PPA 1/日（`POWER_POOL_SUBMISSION` 独立配额）**（00:00 ET=12:00 GMT+8 重置）；旧 48h 滚动口径已废止。剩余额度从 submit 响应 `REGULAR_SUBMISSION`/`SUPER_SUBMISSION` check 的 `value/limit` 读（value 从 0 起计数，limit=4/1）；PPA 不走本工具链（见上节）。
