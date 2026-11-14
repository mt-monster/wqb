# DEU 每波最小循环骨架（ATOM 战役实测，2026-11-14）

> 回到 [DEU 区域流程](../SKILL.md)。本文件只收 **DEU 类别挖掘战役的每波循环差异**；
> 九步流水线权威在 `wq-brain-ra-pipeline`，提交链/判死闸/waiver 一律链 AGENTS.md 对应小节（§3.5/§7.5/§7.6/§8.1.2），**不复制正文**。
> 一次性事件（论坛取证、当日覆盖矩阵、数据集终态矩阵）**不入本文件**——数据集终态的运行期真相源是 DB，
> 查询用 `mcp__wqb-db__get_dead_datasets` / `get_mining_yield` / `wave_results`，勿在本文件落终态值。

## 每波循环（≤10 臂，multi-sim 串行）

```
S0 盘点选集 → S1 字段确认与臂表设计 → 预检（硬步骤）→ multi-sim 派发 → 收割归因 → 判定（继续/精修/判弱/换集）
```

### S0 盘点选集【每换集/开类一次】

- 分母 = 平台 `/data-sets` 全表实取（**不是**本地台账，AGENTS §8.11）；排除已收敛/伪集/数据层排除面，排除依据查 DB 不查文档记忆。
- 判死档/dead 标记**不得单独作排除依据**（AGENTS §7.5）；选定目标集核对判死六维闸距离（AGENTS §7.6）。
- 换集必须出具理由（用户执行约束）。

### S1/S2 臂表设计

- 字段级确认存在性（get_datafields 全量拉取），探针臂 VECTOR 用 vec_avg 包裹——⚠ SUBINDUSTRY 下 longCount>0 只作**存在性判断**，不作覆盖度读数。
- 每波 ≤10 臂；机制优先（单腿换轴/换分母/反号/乘法交互/bucket 条件化），符号先验按机制定、收割时指纹校验。
- ATOM 自检：单集、group 字段豁免、无跨集 add；同集 add 走 SAME_DATASET_LEG_ADD 登记制（权重来源 + 腿 corr<0.7）。

### 预检【派发前硬步骤】

- `preflight_expressions(dataset_id=…)` 全臂过 → 判据顺序：**toolkit 静态闸 > operator_audit 模式2 > 本地白名单**（`src/wqb/store/_field_patterns.py`；operator_audit 模式2 有漏报先例）。
- 平台 ERROR / `[INACCESSIBLE_OP]` 连坐 → **等价几何重建**回预检（先例：ts_min_diff/ts_min 不可访问 → ts_scale/ts_av_diff/ts_zscore）。
- 全同表达式平台返同 id → 派发前查重。

### 派发与收割

- ★ **multi-sim 并发 ≤2、相关性账号级单槽**——账号级红线，⚠ 只有文档约束、没有代码闸（有代码背书的只有 execute_chain 不可逆守卫 / submit_verdict / region gates / PRODCORR_CEILING）。
- **臂序 = 收割归因键**：按派发顺序逐臂核对，禁止按 alpha id 猜（BE225 wpoVAZr1 误读战例）。
- harvest 404 兜底与队列入库见 AGENTS §8.2（不复制）。
- 收割后逐臂归因写波次文档（命名规则见战役根目录惯例）。

### 近闸 prod 前置 + 网格精修

- 近闸（S≥1.2 或距任一硬闸 ≤0.4）先 `check_correlation(production, refresh=True)` 再扫参——详见 [['_effective-levers']] 通用纪律。
- 网格精修有界 ≤3 轮；**收敛封顶判据**：带宽/std/decay/轴全维度扫完且 S 不再抬升（fnd1 44 臂实例：1.53 平台即封顶）。
- 全闸通过（failed_ra=0 且 prod < 见 `config.PRODCORR_CEILING` 且篮内互相关<0.7）→ 停在「待用户确认」，提交 POST 不在自动流程内。

### 若要自动化

波次循环的判断密集环节（归因、判死、取证、提交确认）不可脚本化；结构上可自动化的只有
「单派发员/单相关性员子代理串行化账号级约束」——见 `.zcode/workflows/deu-category-mine.dwf.ts`（harness 实验草稿）。
写自动化前先读 AGENTS §3 双轨同源：写进文档 ≠ 流程会读。
