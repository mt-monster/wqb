# gate 6 闸判定细则（5 闸 + 闸6 批级多样性） + build_wave 选波规则

## gate.py：提交前 6 道闸（不过闸不烧配额）

缓存：`cache/gate_cache.json`，key = sha1(dataset + "\n" + expr)，幂等命中跳过。

### 闸1 语法
import alpha-expression-verifier 的 `ExpressionValidator` 直调（不是子进程）。路径解析顺序：`WQ_VALIDATOR_DIR` 环境变量 → 自动探测 `~/.qoder-cn/skills/alpha-expression-verifier/scripts` 等已知位置。**verifier 缺失时结果标 SYNTAX_UNKNOWN 显式报警，绝不静默放过。**

### 闸2 字段白名单
- 按 dataset 自动派生路径：catalog（`<region>_<ds>_fields.json`）优先 → legacy whitelist（`<region>_<ds>_field_whitelist.json`）兜底 → 都没有则报错并引导先跑 scan_fields。
- 表达式字段 = idents − KNOWN_OPS − GROUP_IDENTIFIERS − PRICE_VOLUME − DRIVER_ARGS；字段必须 ∈ verified 集合。

### 闸3 类型（数据驱动，非正则猜）
- catalog 有字段级 type 时：解析全部函数调用区间（fn_spans），**type==VECTOR 的字段其最内层包裹必须是 vec_***（vec_avg/vec_max/...），否则报 `[EVENT] 事件型字段必须经 vec_* 聚合`。
- MATRIX 数据集禁 vec_*（报 `[TYPE]`）。
- 无字段级 type（legacy 白名单）时退 strip 启发式（抹掉 vec_*(...) 区间后再查裸字段）。

**自动修复（`--fix`）**：VECTOR 数据集下加 `--fix` 会把裸用的 VECTOR 字段自动裹上 vec_* 聚合后再检测，幂等（已裹的不重复裹），报告含 `fixed_expr` 字段。聚合算子按字段语义选（字段名含 count/sum/num/vol/qty/amount/total → `vec_sum`，其余默认 `vec_avg`）。`--fix` 会改写表达式，故**禁用缓存**以免缓存键（原始表达式）与修复后结果不一致造成污染。修复器为工作区单一权威源 `tools/lib/vector_wrap.py` 的 `wrap_naked_vectors()`，被本 gate、工作区 `tools/gate.py`、MCP `fix_vector_fields` 工具、makeSomeGem 生成端四处复用。注意 `--fix` 只裹聚合不改信号逻辑，重要候选建议人工复核 `fixed_expr` 的 avg/sum 选择。

### 闸4 不可访问算子 + quantile arity + banned_patterns
- `ts_min/ts_max`：平台不可访问（语法合法但回测 ERROR 级联整批 CANCELLED）。**必须对表达式全部 idents 判定**——它们不在 KNOWN_OPS 里，对 ops_used 判定是死代码（KOR 历史教训）。
- `quantile` 仅 1 参：括号深度计数逗号；verifier 签名表允许 1-3 参是语法事实，**不要改 validator.py**，加严只在本层。
- banned_patterns：来自 catalog/whitelist，支持 `scope: vector_dataset`（MATRIX 数据集跳过该条）。

### 闸5 poison_patterns
平台级毒模式正则（toolkit config/platform_constraints.json）+ 区域级追加（战役 reference 的 generation_constraints）。当前平台级：`nested_three_leg_add`（嵌套三腿 add 致整批 CANCELLED，KOR record_poison bisect 实证；改写 add(add(a,b),c) 左结合）。

### 闸6 批级多样性（B 方案闭环：评估→执行强制，默认开启）
只对 **批级**（--file）生效；契约 = 台账 `diversity_audit_latest.next_round_injections`（`diversity_audit.py` 每次评估写入）。规则：
- **注入算子**：每批至少 `per_batch_min_operators`（默认 2）条使用 `required_operators` 之一；不达标报 `[DIVERSITY]` 并拒绝提交。
- **骨架配额**：每批 `skeleton_quota`（如 ratio≥1/event_gated≥1）逐项检查。
- **豁免**：`--batch-type repair`（修复/设置变体批冻结结构不变体）；或 `--skip-diversity-gate` 逃生（需在台账记录原因）。
- **效力与幂等**：`consumed_batches` 达 `expires_after_batches`（默认 10）契约自动失效；批内容 sha1 已消费则重跑闸门不重复计数；总闸全过才记账消费。
- **构建端**：`diversity_slots.py --campaign-dir <DIR>` 打印当前契约 + 算子占位模板，批次构建照做即可过闸。
- **对账**：下次 `diversity_audit` 输出 `injection_landing`（上一契约逐项落地/未落地），未落地项要么继续强制要么移出清单。
- **注入算子的经济学写法（KOR wave104 实证，勿为过闸装饰）**：优先把注入算子融进有经济学意义的结构，而不是生套：
  - `ts_corr(慢腿, 快腿, 20)` 共振腿：因子协同确认（预期漂移与短期模型同向时增强）；
  - `if_else(rank(快腿)>0.5, rank(快腿), 0)` 动量门控：快腿信号强时激活、弱时置零；
  - `group_zscore(慢腿, sector)` 行业相对强度：一算子同时满足注入算子 + group 骨架槽（双槽命中）。
- **bucket 语法限制（实证）**：`bucket(x, n)` 输出 `Unit[Group:1]`，`rank()`/`add()` 均不接受 → 闸1 报 `Incompatible unit` SYNTAX FAIL；bucket 不能与 rank 骨架组合，改用 if_else/ts_corr 满足同槽。
- **skeleton 槽判定速查**：含 `if_else(`/`trade_when(` → event_gated 骨架；含 `group_` → group 骨架；`skeleton_quota` 逐槽至少 1 条，与注入算子要求叠加（KOR 契约：注入 2 条 + event_gated 1 + group 1）。

退出码：0=全 PASS，1=存在 FAIL。

## build_wave.py：选波规则
1. **全历史去重**：对战役目录全部 `<region>_wave*_exprs.json` + `candidates/*.json` 建规范化（去空白）哈希集，重复候选直接丢弃（KOR 实测 92/854 重复 = 11% 配额浪费）。
2. **near-miss 加权**：reviews/*.json 的 near 池 + 台账 near_pool 中出现过的字段，含这些字段的候选排前。
3. **算子树分桶**：根调用 + 第一个函数参数作桶键（如 `rank>ts_av_diff`），轮转抽样每桶 ≤ `--per-bucket`（默认 8），避免 startswith 前缀碰撞。
4. **骨架配给**：skeleton 五分类（event_gated/group/ratio/linear_mix/single，优先级见 platform_constraints）按 `<region>_generation_constraints.json` 的 skeleton_quota 限量（linear_mix ≤50%，强制事件门控/group/ratio 骨架进候选——直击 CW 墙根因）。
5. **波内字段去重**：同一字段单波出现 ≤ `--max-field-repeat`（默认 3）。

输出 `candidates/<region>_wave<TAG>_exprs.json`，含 meta（去重数/桶规模/骨架分布），供 diversity_audit 与复盘消费。

## diversity_extract.py：单数据集多样性榨取

**核心思想**：先榨取单数据集的多样性，再进入多数据集阶段。通过 L1（字段多样性）→ L2（算子结构多样性）→ L3（参数空间多样性）三轮榨取，最大化单数据集的多样性产出。

### 流程
1. **数据集深度审计**：分析字段经济含义分组、算子树分桶、参数空间映射，生成多样性潜力报告。
2. **分轮次多样性生成**：
   - L1 字段多样性：不同经济含义的字段（valuation/growth/quality/momentum/sentiment/volatility/liquidity/size）
   - L2 算子结构多样性：同字段不同算子（ts_rank/ts_zscore/ts_delta/rank/zscore/quantile/normalize）
   - L3 参数空间多样性：同结构不同参数（ts_rank 的 window: 5/10/20/60/120/250）
3. **PPAC 矩阵计算**：基于回测结果计算两两 PPAC，更新多样性矩阵。
4. **多样性榨取效果评估**：结合结构多样性（算子熵/结构相似度/新颖度/覆盖率）和 PPAC 多样性（平均 PPAC/最大 PPAC/低 PPAC 比例），评估是否继续榨取或进入多数据集阶段。

### 用法
```bash
# 完整流程
python diversity_extract.py --campaign-dir <DIR> --dataset <ds> --rounds 3 --size 8

# 跳过审计（使用已有报告）
python diversity_extract.py --campaign-dir <DIR> --dataset <ds> --skip-audit

# 跳过生成（使用已有表达式）
python diversity_extract.py --campaign-dir <DIR> --dataset <ds> --skip-generation

# 跳过 PPAC 计算
python diversity_extract.py --campaign-dir <DIR> --dataset <ds> --skip-ppac

# 跳过效果评估
python diversity_extract.py --campaign-dir <DIR> --dataset <ds> --skip-evaluation
```

### 输出
- `reference/<region>_<ds>_diversity_potential.json`：多样性潜力审计报告
- `candidates/<region>_wave<TAG>_exprs.json`：各轮次表达式（TAG = D01/D02/D03/...）
- `reviews/<region>_diversity_matrix.json`：PPAC 矩阵
- `reviews/<region>_diversity_evaluation.json`：多样性榨取效果评估

### 决策逻辑
- **enter_multi_dataset**：单数据集多样性榨取充分（总表达式 ≥15 且低 PPAC 比例 ≥0.7 且新颖度 ≥0.8），建议进入多数据集阶段。
- **continue_extraction**：多样性榨取效果良好（总表达式 ≥10 且低 PPAC 比例 ≥0.6），建议继续榨取 1-2 轮。
- **adjust_strategy**：多样性榨取效果不佳（总表达式 <5），建议调整生成策略或更换数据集。

## review_wave.py：walls 诊断
- **missing ≠ fail**：指标缺失（None）不算败，单独标 `*_UNKNOWN`（2Y/MARGIN/TVR/FIT 各有 UNKNOWN 分支；平台未返回 LOW_2Y_SHARPE 时不能算 2Y 败）。
- 墙枚举：SHARPE / FITNESS / 2Y / MARGIN / TVR / CW（CONCENTRATED 映射）/ RA_OTHER / NO_DATA。
- candidates = 全门槛过；near = 未过但 sharpe > near.sharpe_min（附 walls 诊断）。
- `--write-ledger` 幂等回写台账 submit_ready / near_pool（同名去重）。
