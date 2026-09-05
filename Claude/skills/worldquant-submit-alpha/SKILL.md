---
last_verified: 2026-09-01
name: worldquant-submit-alpha
description: "通过 API 将 WorldQuant Brain alpha 真正提交（submit）到平台（不只是模拟 simulate）。 当用户对某个 WQ alpha id 说\"提交 alpha / submit / 上平台 / 落地\"时使用。覆盖关键坑： POST /alphas/{id}/submit 返回 201/200 但 status 因 regular.description 过短而永不翻转， 以及正确的嵌套 description PATCH 写法；并说明约 2 分钟的状态翻转延迟与轮询方法。★2026-09-01 新增「点塔优先提交规则」：提交前按金字塔点亮价值优选（点亮=该 catalog 近 90 天提交 ≥3 颗；跨 ≥3 catalog 的 alpha 不计；差 1-2 颗的塔一次提交即点亮，0 亮区域的单颗提交不算点亮）。"
layer: L5
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---







# WorldQuant Brain — 实际提交 Alpha 到平台

## 何时用
用户要把某个已模拟出的 alpha（已知 platform_id，如 `YPgAa3WR`）真正提交到 WQ
平台参与评审/进入 power pool。注意：很多脚本里的 `submit` 只是本地打标/记录，
并没有调用平台提交端点。本 skill 解决的是**真正落到平台**的那一步。

## 衔接协议
- **上游**：S5 提交层判定 `tools/submit_verdict.py`（SUBMITTABLE 且 type=REGULAR/PPA 单颗；IS 硬闸全 PASS、description 已按三段式补齐；brain-alpha-judge 参考评审可为点塔排序提供输入）。
- **本 skill 角色**：S5 落地执行——真正提交到平台并确认 status 翻转为 ACTIVE。
- **下游**：S6 `wq-backtest-monitor`（OS 表现监控；§14 台账回写 `wave_results` + `registry_empirical` 反哺 S-PRE）。

## 前置
- **MCP 优先**：平台交互首选 `mcp__wq-brain-http__*` 工具（自带重试/超时配置），禁止手写 requests 脚本。
- 凭据在 `world-quant-brain-mcp` 项目根目录的 `.env`：`CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（MCP 服务端自动加载）。
- 运行环境（仅 fallback 需要）：**`$WQ_PY`**。

## 提交流程（MCP 工具调用）

**推荐**：使用 `mcp__wq-brain-http__workflow_submit_alpha` MCP 工具（workflow 引擎快捷方式，含预检 + 属性设置 + 提交 + 状态轮询）：

```
# 完整提交流程（属性设置 + 提交 + 状态确认，confirm_submit=True 才真正 POST）
mcp__wq-brain-http__workflow_submit_alpha(
  alpha_id="<ALPHA_ID>",
  name="0.6525",  # prod correlation 值
  color="GREEN",
  tags=["PowerPoolSelected"],
  descriptions="Idea: <idea>\n\nRationale for data used: <rationale>\n\nRationale for operators used: <rationale>",
  confirm_submit=True,  # 默认 False 仅预检+查状态；True 才真正提交
  verify_timeout=180
)
```

**分步模式**（需逐步控制时）：

```
# 1) 设置属性（description 必须三段式，name 建议基于 prod correlation）
mcp__wq-brain-http__set_alpha_properties(
  alpha_id="<ALPHA_ID>",
  name="0.6525",  # prod correlation 值
  color="GREEN",
  tags=["PowerPoolSelected"],
  descriptions="Idea: <idea>\n\nRationale for data used: <rationale>\n\nRationale for operators used: <rationale>"
)

# 2) 提交（经 workflow 引擎，自带 IS 预检 + 状态轮询）
mcp__wq-brain-http__workflow_submit_alpha(alpha_id="<ALPHA_ID>", confirm_submit=True, force=False)
# force=True 跳过本地启发式预检

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
1. **静默丢弃（两类独立成因）**：`POST /alphas/{id}/submit` 返回 201/200 但
   `status` 始终 `UNSUBMITTED`、`dateSubmitted=None`。成因有二，必须分清：
   - (a) `regular.description` 过短/格式错 → 网关后端校验丢弃（前端只显示 WARNING
     不挡，但网关会丢）。补一个 >=100 字、格式合规的嵌套 `regular.description` 可救活。
   - (b) **任一硬 IS 闸门 FAIL**（如 `SELF_CORRELATION`、`PROD_CORRELATION`）→
     提交不被激活（同样 201 但 UNSUBMITTED）。**仅补描述救不了 (b)**，必须先
     `get_alpha_check` 确认所有硬闸门 PASS 才能提交。两类都表现为「201 但不翻转」，
     区别只能靠 IS check 定位。
   - 经验：硬闸门 FAIL 的提交尝试**不消耗每周额度**（status 保持 UNSUBMITTED、
     无 rejected 记录），探测性提交无成本。
2. **description 的 PATCH 形式**：用**嵌套** `{"regular": {"description": "..."}}`。
   用扁平的 `{"description": "..."}` 会被 `400 {"description":["Unexpected property."]}` 拒绝。
3. **翻转延迟**：提交成功后 `status` 不会立刻变，通常等 **2~3 分钟**才从
   `UNSUBMITTED` 翻转为 `ACTIVE`。轮询窗口要够长。
4. **提交后 IS check**：提交成功后再 `GET /alphas/{id}/check` 只会返回
   `ALREADY_SUBMITTED: FAIL`（代表不可重复提交），属正常，原 21 项闸门结果已锁定。
5. `GET /alphas/{id}/submit` 返回 `text/html`（前端 SPA 壳），不是 API，
   不要拿它判断提交结果。
6. **提交前必做平台 IS 核验（关键！）**：`scan` 的 `PASS_CHEAP` 本地判定**不会**
   评估 `SELF_CORRELATION` / `PROD_CORRELATION` 等硬闸门，易出现假阳性。批量提交前
   务必对每个候选 `get_alpha_check(id)`，确认 **无硬 FAIL**（尤其 `SELF_CORRELATION`
   阈值 0.7、`PROD_CORRELATION` 阈值 0.7）。self_corr 0.87~1.0 属结构性黏滞信号，
   无法靠补 description 救活，只能重挖低自相关变体。PASS_CHEAP ≠ 平台可提交。
7. 配额查询：`GET /alphas/submission-limit` 路径不存在（404），不要依赖它判断剩余额度；
   以实际 POST 返回与 `dateSubmitted` 落库为准。

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
1. **能一次点亮塔的优先**（该塔现状 ≥2/3，差 1-2 颗）：先查 `_tower_map.py` 或
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
  可复用 `tracking/_submit_kit/_tower_map.py`（WINDOW_DAYS=90 / EXCLUDE_MULTI=3 / MIN_LIT=3）。

### 对表达式构造的反向约束（挖新候选时）
- 想给某塔 +1：**纯单类别数据集 alpha 最干净**（挂 1 塔）；混 2 类挂 2 塔（两塔各 +1）；
  **混 3+ 类 = 白提**（对点塔零贡献，不管指标多好）。

## 验证清单
- `mcp__wq-brain-http__get_alpha_details` 返回 `status=ACTIVE`（或 SUBMITTED→ACTIVE）、
  `dateSubmitted` 非空 → 成功。
- 所有硬闸门此前已 PASS（ProdCorr<0.7、SelfCorr<0.7、LOW_SUB_UNIVERSE_SHARPE>=0.9 等）。
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
- 判断"今天 ET 日已用几颗"：拉 `/users/self/activities/submissions`（按日聚合记录）
  或本地 DB `alphas.date_submitted`（注意是 EDT 时区 `-04:00`）按当前 ET 日过滤。
- 可复用：`tracking/_submit_kit/_quota_now2.py`（activities 尾部 + 实时 alpha + DB ledger 三方核对）。


## 工具化纪律（tools/ 通用工具，勿再写一次性脚本）

提交层判定与批量提交一律走通用工具，**不要手写 `GET /alphas/{id}/submit` 或 `_submit_*.py`**：

```powershell
# 403 盲区的唯一可信判定入口（模拟态 + submit 双视图）
& $WQ_PY tools/submit_verdict.py --alpha-id <ALPHA_ID>

# 批量提交（多批规格走 --spec JSON 文件通道，避免引号事故）
& $WQ_PY tools/submit_batch.py --path <exprs.json> --region <R> --decay <D> --neutralization <N>
& $WQ_PY tools/submit_batch.py --spec <spec.json> --dry-run
```

配额口径：ET 日历日 **REGULAR 4/日 + SUPER 1/日**（00:00 ET=12:00 GMT+8 重置）；旧 48h 滚动口径已废止。剩余额度从 submit 响应 `REGULAR_SUBMISSION`/`SUPER_SUBMISSION` check 的 `value/limit` 读（value 从 0 起计数，limit=4/1）。
