---
last_verified: 2026-08-22
name: wqb-concurrency
description: "WorldQuant Brain 并发挖掘调优。触发词：并发调优/429 风暴/CONCURRENT_SIMULATION_LIMIT_EXCEEDED/ 回测大量 429/提交成功数极低/调线程数/调并发/调信号量/战役 pipeline 批量回测提交/ 最大化回测吞吐/槽位利用率。 核心方法：测定服务端并发上限 C，并把本地在飞数锁到 C，避免 429 风暴与孤儿模拟占槽； 含七槽填槽模式 SOP（7 批 multisim 同提保持槽位常满，每次挖掘必须执行）。 含台账闭环：每波结论写 WAVE_LEDGER.md/ledger.json，下一波设计强制以台账决策节为输入。"
layer: L3
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
agent_created: true
---







# WQ Brain 并发挖掘调优

WorldQuant Brain 的「并发模拟数」是**服务端硬性上限 C**，与本地开多少线程无关。
本地在飞回测数 = min(本地工作线程数, C)。超过 C 的提交会拿到 `429`，白白浪费重试。

## 衔接协议
- **上游**：S3 `brain-simAlphasinBatch-and-track`（及其执行后端 `wq-brain-campaign-toolkit` pipeline.py）——七槽填槽执行时以本 skill §8 为并发纪律唯一权威。
- **本 skill 角色**：横向纪律层（L3）——并发上限 C 测定、在飞数锁定、429 风暴与孤儿模拟防治；非流水线阶段，被 S3–S5 执行环节按需引用。
- **下游**：纪律落回调用方执行参数（批大小/并发数/批间隔），不产出独立工件。

## 1. 测定 C（别猜，实测）

> **演进注记（2026-08）**：本节的固定槽位 C=5 为 2026-07 旧测量；2026-08 更精细实测表明并发是 **Token-Bucket 模型：突发容量 C≈7、慢补充 ~1 令牌/20–40s**，详见 `wq-backtest-monitor` §6。配置基准以新模型为准（瞬时 ≤6 安全、批间 ≥45s）。本节阶梯实测方法仍然有效，可复测当前值。

1. **先停掉所有本地挖矿进程**，让"自己制造的孤儿"释放槽位（见第 4 节）。
2. 用**挖矿脚本里真实的 `SETTINGS`** 发阶梯提交。⚠️ 常见坑：`language` 必须用脚本里的值
   （通常是 `"FASTEXPR"`，不是 `"FAST"`；用错会 400 而非 429，测不出 C）。
3. 并发提交 N(≥C+3) 条极简表达式（如 `rank(close)`），间隔 0.2~0.3s。
4. 观察：**首批连续 `201` 接受数 = C**（第 C+1 条起 `429`）。
   - 429 报文形如 `{"detail":"CONCURRENT_SIMULATION_LIMIT_EXCEEDED"}` —— **不含数字**，无法从报文读限额，只能靠阶梯提交数出来。
   - `/users/self` 也**不含**并发/模拟限额字段（已全量遍历确认），别再查它。

## 2. 把本地在飞数锁到 C（关键修复）

信号量必须包住**整条** `run_backtest`（提交 `POST` + 轮询 `Location` 等待全程），
而**不只是 `POST` 那一瞬间**：

```python
def run_backtest(self, expr, settings, ...):
    with self._sub_sem:          # ← 提到最外层，覆盖 post + 轮询全程
        # POST /simulations ... 429 短退避重试（最多 ~40 次）
        # 轮询 prog_url 直到完成
        return {"platform_id": alpha_id, ...}
self._sub_sem = threading.Semaphore(C)   # C = 实测上限
```

若信号量只在 `POST` 处 `with`，轮询时信号量已释放 → 实际在飞数 = 工作线程数，
会超额提交、疯狂 429。这是最隐蔽的 bug。

## 3. 线程数设置

- 在飞数 = min(工作线程, C)。要打满吞吐，需 **工作线程 ≥ C**。
- 推荐：工作线程 = C+1（多 1 个缓冲线程，随时补位，保证 C 个槽位始终打满）。
- 例：实测 C=5 → 信号量=5，每数据集 3 线程 ×2 数据集 = 6 工作线程。

## 4. 🚨 孤儿模拟占槽（最阴的坑）

`TaskStop` / 强杀本地 Python 进程时，**服务端已提交的回测仍在跑**，它们一直占用
账户的 C 个槽位，导致新提交全部 429（t=0 就被占满）。

- 这些孤儿**无法查询也无法取消**（`GET /simulations` 405，`/users/self/simulations` 404），
  只能等它们**在服务端自己跑完**才释放（拥堵下每条数分钟）。
- 应对：`run_backtest` 对 429 做**频繁短退避重试**（`wait=min(20+attempt*8,45)s`，最多 ~40 次），
  **绝不因限流丢弃候选**；提交成功数会随孤儿释放而自然回升。
- ⚠️ 探测并发时自己提交的探针回测也会变成孤儿，释放前会占满槽位、让后续 mining 初期全 429——
  这是自找的延迟，耐心等其释放即可，**不要再 TaskStop**（会制造更多孤儿）。

## 5. 判定卡住的三类根因

| 现象 | 根因 | 对策 |
|---|---|---|
| `rank(close)` 也卡 0.1%~0.35% 进度零进展 | WQ 全局集群拥堵（排队） | 只能等集群缓解；缩短 `testPeriod` 仅降单任务算力、不降排队 |
| 提交全 429、接受数 0 | 孤儿模拟占满 C 个槽 | 429 耐心重试等孤儿释放 |
| 提交全 400 | `SETTINGS` 非法（如 language/unitHandling 互斥） | 用脚本真实 SETTINGS 复测 |

## 6. 凭据加载

- 账号凭据在 `.env`（`WQ_USERNAME`/`WQ_PASSWORD`），加载用 `load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))` —— 后台任务 cwd 不一定是项目目录，绝不能依赖 `cd` 或 `os.path.abspath(".")`。

## 7. 战役场景：参数化退避

战役目录（`tracking/<REGION>/`）内的正式 wave 回测走七槽填槽模式（第 8 节）；退避/熔断参数化实现由 toolkit `pipeline.py` 内部提供（20s/*1.5/120s 封顶/60min 挂起熔断/360min 超时，thresholds.json `poll` 节可覆盖）。

## 8. 🌟 七槽填槽模式（2026-08-25 更新：5→7，基于 Token-Bucket 模型 C≈7 实测）

**实证**：7 个 multisim（各 8 条）同时提交全部被接受且 ~90 秒同步 COMPLETE，连续多波 0 ERROR/0 连坐。旧"多批 multisim 会 CANCELLED"的结论实为批内坏表达式连坐所致，四重门禁后已可安全并行。Token-Bucket 模型实测突发容量 C≈7，慢补充 ~1 令牌/20–40s。

**SOP**：
0. **台账同步门（执行层硬门）**：提交任何新波批次前，必须先运行 toolkit 的 `check_ledger_sync.py` 校验台账一致性：
   ```powershell
   $WQ_PY `
     ../.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/check_ledger_sync.py `
     --campaign-dir tracking/<REGION>
   ```
   返回 0 方可继续；返回 1 需先修复不同步项。配合时序规则：**创建批次文件时同步在台账登记批次表（标在飞，multisim id 提交后回填）**，回收后补结论——这样新批在飞期间门禁也能自洽 PASS。
1. **提交前门禁**：每批表达式先过 gate 闸预检（见 `wq-brain-campaign-toolkit` `gate.py`）或等价的 expr_lint 工具，确认算子签名/字段白名单+coverage/单位语义合规，杜绝批内 ERROR 连坐。
2. **7 批同提**：`mcp__wq-brain-http__create_multi_simulation`（`validate_fields=false` 避免预检超时、异步模式）每轮同时提交 7 批 × 8 条；**禁止串行"提交→等完→再提"**（槽位利用率仅 ~14%）。
3. **统一轮询**：`mcp__wq-brain-http__lookINTO_SimError_message` 批量查 7 个 multisim 状态 → 取 children → alpha id → `mcp__wq-brain-http__get_alpha_details` 逐 ID 拉完整详情（含 checks 数组）做闸门筛选。**不用 `get_user_alphas`**：它按时间排序拉摘要列表，无法保证目标 ID 全在里面且可能不含完整 checks。
4. **写波结论（台账，强制阻断）**：每波回收筛选后立即追加一节到 `tracking/<REGION>/WAVE_LEDGER.md`（批次表/闸门结论/结构性发现/判死证据/多样性快照），同步更新 `tracking/<REGION>/ledger.json`（判死清单/骨架登记/最佳候选）。**台账唯一写入入口是这两个文件**：禁止把波结论写进 `runs/` 散件 txt 替代台账（散件只作批次表达式/原始证据）；未写台账不得提交下一波。判死与结构性墙当场写入，不等周期。每 10 波做一次全量多样性评估（算子/字段探索率、骨架与风格多样性、预处理分布、收益归因、失效风险）独立成章，并据此优化 skills。
5. **即收即补**：任一批 COMPLETE 立即回收筛选，空槽当轮补新批，保持 7 槽常满；单轮吞吐 ×7。
6. **台账驱动选波（强制输入）**：下一波批次设计前必须先读 `WAVE_LEDGER.md` 最新「下一波决策」节与 `ledger.json` 的 `wave*_directives`/`exhausted_skeletons`/判死清单；禁止凭上轮对话记忆选波，禁止重发已饱和骨架或判死数据集的表达式。批间差异化（不同数据集/字段族/decay/中性化）以台账多样性快照中的补盲项为准。

**注意**：提交配额（ET 日历日 REGULAR 4/日 + SUPER 1/日）与回测并行槽位是两个独立机制；本模式兼容第 1 节演进注记的令牌桶模型（7 批 multisim 仅耗 7 令牌、瞬时 ≤7 安全包络内）。
