# KOR 因子挖掘完整流程与经验总结

> 适用范围：本文档系统梳理 WorldQuant BRAIN 平台的因子（Alpha）挖掘全流程，并以 **KOR（韩国股票区域）** 为典型区域贯通各环节。
> 说明：在本项目中，"KOR" 是 WQ BRAIN 的一个 **equity 区域**（region）而非独立框架；其挖掘流程与 USA / GLB / EUR / IND 等区域完全一致，仅部分 `universe / delay / neutralization` 配置与信号族略有差异。因此本文以"通用流程 + KOR 特例"的方式组织，结论对所有区域可复用。
> 资料来源：`docs/experience/*`、`docs/reference/*`、`mining/scripts/*`、`world-quant-brain-mcp/*` 及 `.workbuddy/memory/` 长期日志（2026-08-01 至 2026-08-14 实证）。

---

## 一、总体流程全景

```
Step 0  平台实时体检（不可跳过）
        get_datasets → cov≥0.85 & alphaCount≤50 & fieldCount≥10
        排序: pyramidMultiplier↓ → alphaCount↑ → coverage↓

Step 1  字段级诊断 → 选预处理模板
        MATRIX: winsorize(ts_backfill(F,120), std=4)
        VECTOR: winsorize(ts_backfill(vec_avg(F),120), std=4)
        有界字段: 不 winsorize

Step 2  一阶算子批量扫描（12算子 × 5窗口 = 60 变体/字段）
        按字段前缀去重，每字段保留 top N

Step 3  二阶 group 包裹（group_rank / group_zscore / group_neutralize）
        分组: sector/industry/subindustry/country(GLB)/bucket(rank)

Step 4  三阶 trade_when 事件工程（拉高 turnover、修复 2Y 衰减）

Step 5  闸门预检 + 提交探测
        check_self_correlation → submit probe → /check 读 prodCorr → 全量/停止

Step 6  组合（SuperAlpha）与落地
        selection(prod_correlation>0) + combo_a → 提交 ACTIVE
```

**纪律红线**：
1. 体检先行，不可跳过。
2. 每轮验证 > 10 种不同结构后才考虑转向，不可 1–2 个字段就下"无解"结论。
3. 所有回测脚本必须支持 checkpoint / resume（`V<NN>_FRESH=1` 强制全新）。
4. 不确定算子隔离到独立小批次，避免级联 CANCEL。
5. 提交探测零成本（硬闸失败不消耗周额度），但先 5 个多样化探针再全量。

---

## 二、Stage 0 — 原始数据获取与清洗

### 2.1 数据集体检（开战役前置硬门槛，一票否决）
| 门槛 | 阈值 | 处理 |
|---|---|---|
| coverage | **≥0.85** | <0.7 直接排除 |
| alphaCount | **≤50** | >1000 直接排除（过度拥挤） |
| fieldCount | **≥10** | 字段太少无法穷举 |

- 排序优先级：`pyramidMultiplier↓ → alphaCount↑ → coverage↓`。
- **数据集级体检走 `get_datasets`** 直接读取 `coverage/fieldCount/userCount/alphaCount/valueScore/pyramidMultiplier`，比逐字段聚合快约 2 个数量级。
- 工具：`tools/eur_field_coverage.py`（MCP+直连双通道）、skill 内 `dataset_health_check.py`。

### 2.2 区域优先级（实测）
| 区域 | 数据集数 | cov 均值 | 倍率档 | 结论 |
|---|---|---|---|---|
| HKG | 209 | 0.696 | **1.8** | 优先级最高 |
| KOR | 192 | 0.705 | 1.7 | 优先 |
| EUR | 178 | 0.662 | 1.3–1.5 | 倍率偏低 |
| GLB | — | — | — | Power Pool 活跃主题区 |

跨区域发现：同批优质集在 KOR/HKG 倍率 1.7–1.8，EUR 仅 1.5 → **HKG ≈ KOR > EUR**。

### 2.3 WebDataScope 三层数据诊断框架（清洗依据）
1. **字段级**（`dataAna.js` 10 指标）：frequency→时间窗口/backfill 间隔；Coverage→`ts_backfill(66/120)`；IntegerStatus→`rank/group_rank`；skewness/kurtosis→`winsorize/signed_power/rank`；point_mass/zero_inflated→`rank+winsorize` vs `spread→zscore`。
2. **数据集级**（`dataFlag.js`）：读取 dominant neutralization method 徽章（KOR 实测为 **SECTOR**，非 SUBINDUSTRY），**读取而非硬编码**。
3. **全局级**（`distribution.js`）：低竞争白空间发现；区分 `non_data`（真低竞争）vs `non_data_delay0`（多为数据不可用，非机会）。

### 2.4 各区合法 universe / delay / neutralization（2026-08-09 固化）
| 区域 | Delay | Universe | 中性化特色 |
|---|---|---|---|
| USA | 0,1 | TOP3000/2000/1000/500/200 + ILLIQUID_MINVOL1M/TOPSP500 | 全 11 种，无 COUNTRY |
| EUR | 0,1 | TOP2500/1200/800/400 + ILLIQUID_MINVOL1M/TOPCS1600 | 含 COUNTRY |
| **KOR** | **1** | **TOP600** | 无 COUNTRY，SECTOR 主导 |
| GLB | 1 | TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000 | 含 COUNTRY（三区域检查关键） |
| HKG | 1 | TOP800/TOP500 | 无 COUNTRY |
| IND | 1 | TOP500 | 无 COUNTRY |
| MEA | 1 | TOP400/TOP300 | 仅 6 种（无 STATISTICAL/FAST/SLOW） |

> **关键陷阱**：`universe` 传非法档位 → 平台 500（不是 400）；`GET /data-fields` 必须 `instrumentType+region+delay+universe` 四者齐全，缺 universe → 400。离线包 ★★★/☆☆☆ 仅代表离线匹配度，**严禁**据此推断平台数据可用性。

### 2.5 清洗实践
- MATRIX 字段：`winsorize(ts_backfill(F, 120), std=4)`。
- VECTOR 字段：必须先 `vec_avg / vec_max` 聚合再套 cross-section 算子（见 §四 算子签名陷阱）。
- 有界字段（如搜索热度）**不需 winsorize（有害）**。

---

## 三、Stage 1 — 特征工程

特征工程在本项目中体现为"**字段类型诊断 → 预处理决策 → 信号类型匹配**"三件事：

1. **字段类型分流**
   - MATRIX（截面矩阵）→ `winsorize(ts_backfill(F,120), std=4)`
   - VECTOR（事件序列）→ `winsorize(ts_backfill(vec_avg(F),120), std=4)`
   - 有界字段 → 直接 `rank`，跳过 winsorize
2. **信号类型诊断**（决定用何种算子，见 §四.6）
   - 偏离信号（搜索兴趣）→ `ts_av_diff` 远强于 `ts_zscore/ts_mean/ts_delta`
   - 水平信号（借贷利用率）→ `ts_mean`，套 `ts_av_diff` 会洗掉信号
3. **启发式表达式引擎**：`mining/scripts/mining_experience/heuristic_engine.py` + `rules.json` 以规则驱动批量生成候选表达式，替代 21 个复制粘贴的 `mine_v*` 版本；`mine_core.py` 进一步把"版本差异"收敛为 **数据**（候选列表 + 设置），统一 checkpoint/resume。
4. **字段收割**：`harvest_fields.py / harvest_fields_v2.py / harvest_usa.py` 按数据集拉取字段清单并打标，配合 `enum_mdl177.py` 枚举 mdl177 因子模型子字段。

---

## 四、Stage 2 — 因子生成（Alpha 构造）

### 4.1 三阶算子流水线
1. **一阶（12 个基础算子）**：`reverse/inverse/rank/zscore/quantile/normalize` + `ts_rank/ts_zscore/ts_delta/ts_sum/ts_std_dev/ts_mean/ts_arg_min/ts_arg_max/ts_scale/ts_quantile`。窗口 `[5,22,66,120,240]`。
2. **二阶（group 包裹）**：`group_neutralize/group_rank/group_zscore`。分组：`market/sector/industry/subindustry` + `pv13_*_sector` + `bucket(rank(...))`。
3. **三阶（trade_when 事件工程）**：开仓事件模板（价量背离、放量、极端收益、近期新高、情绪阈值等），能把 2Y 从 0.93 提到 1.35。

### 4.2 窗口选择规律
- 短窗口(5/22)：2Y 好、sharpe 低 → 适合 D0（需 2Y≥2.69）。
- 长窗口(66/120/240)：sharpe/fit 好、2Y 低 → 适合 D1。
- 甜点：搜索兴趣=92 窗，analyst revision=60 窗，fundamental=22。

### 4.3 中性化按区域选（读取徽章，不硬编码）
| 区域 | 最优中性化 | 依据 |
|---|---|---|
| USA/D0 | STATISTICAL | search_interest: 2.47 > SLOW_AND_FAST 2.39 |
| EUR/D1 | INDUSTRY | STATISTICAL 2Y 仅 0.40 |
| **KOR** | **SECTOR** | 实测 0.562 |
| GLB | FAST | 9qpQ0VQ2 验证；CROWDING 不可用 |

### 4.4 已验证的 14 个论坛模板（高赞）
基础范式 `group_rank(ts_rank(eps,252),industry)`、Delta 反转 `-ts_delta(A,3)`、小而稳 `-A*ts_std_dev(A,30)`、杜邦/PEG/戈登 GGM、信念熵 `signed_power(ts_entropy(field,144),0.618)`（部分账户 `ts_entropy` 不可用，需 `ts_std_dev` 近似）、动量 `(close-open)/((high-low)+0.001)` 等。

### 4.5 关键算子评价
| 算子 | 评价 |
|---|---|
| **quantile** | ★★★ 外包装神器，sub_universe/2Y 双达标，强于 rank |
| **trade_when** | ★★★ 事件工程，解决 2Y 衰减、拉高 turnover |
| **ts_av_diff** | ★★ 偏离均值类最强 |
| group_rank(country) | ★★ GLB 三区域检查关键 |
| ts_scale/ts_product/ts_kurtosis/ts_returns/ts_corr | ✗ 无效（均 <1.0） |

### 4.6 算子签名陷阱（提交前必查，避免回测试错）
- **VECTOR 字段必须 `vec_*` 聚合**：`rank(vec_field)` 报 "Operator does not support event inputs"；正确 `rank(vec_avg(F))`。
- **`group_mean(x, weight, group)` 是 3 参**；加权均值用 `group_neutralize(x, group)`（2 参）。
- **幽灵算子**（平台不存在，会级联 CANCEL）：`ts_entropy / ts_percentage / ts_skewness / ts_median` 等 17 个；不要用 `hump`；`ts_regression(...).residual` 写法无效。
- 降相关技巧：同一字段 `vec_avg → vec_max` 实测可降 PC（论坛案例 0.7288→0.6967）。
- 提交流程防御：本地 `alpha-expression-verifier` 过语法 → 对照签名速查表 → 不确定算子单独小批试跑。

### 4.7 KOR 已落地样本
`e73Rw8qg`：`add(ts_rank(vec_avg(anl44_second_en_eps_value), 50), -ts_rank(vec_avg(pretaxprofit_estimates_down_4w), 22))` —— KOR 用 `anl44` 分析师数据 + `pretaxprofit_estimates_down` 做正向/反向组合（sharpe 1.62）。

---

## 五、Stage 3 — 因子检验（有效性 / 稳定性 / 相关性）

### 5.1 平台硬闸门体系
| 闸门 | 阈值 | 说明 |
|---|---|---|
| LOW_SHARPE (RA/D1) | >1.58 | 常规 Research Alpha |
| LOW_SHARPE (RA/D0) | **>2.69** | D0 远高于 D1 |
| LOW_FITNESS (D0) | **>1.5** | D0 极高 |
| LOW_2Y_SHARPE | D0>2.69 / D1>1.58 | 近两年衰减检测 |
| **PROD_CORRELATION** | **<0.7** | 与生产 book 相关性，**最致命硬闸** |
| SELF_CORRELATION | <0.7 | 与已提交 alpha 相关性 |
| LOW_TURNOVER | ≥0.01 | 换手率下限 |
| HIGH_TURNOVER | ≤0.7 | 换手率上限 |
| LOW_SUB_UNIVERSE_SHARPE | 达标 | 子宇宙一致性 |

**关键机制**：
- `PROD_CORRELATION` **异步计算**，提交后平台才计算，`/check` 可读出 prodCorr；首检可能返回空，**须以重检为准**（曾因首检 0 FAIL 误判，重检才暴露）。
- 提交返 201 但 status 停留 UNSUBMITTED = **静默丢弃**（原因：描述<100 字 或 PROD/SELF_CORRELATION>0.7）。
- GLB 三区域检查（AMER/EMEA/APAC 均需 >1）依赖 `country` 分组。

### 5.2 IS vs OS（稳定性检验）
- 124 个有 OS 数据样本中：OS>IS 约 10 个（极简价量、`ts_sum` 累积）；OS≈IS 约 30 个（`group_rank(ts_rank(...))` 稳定模板）；**OS 显著衰减约 80+ 个**（`FIELD*ts_std_dev(FIELD)` 动量/反转型）。
- **抗衰减模式**：`group_rank(ts_rank(FIELD,60), group)`、长期 `ts_sum(FIELD,252)` + 分层中性化、`-rank(ts_sum((close-low)/(high-close),3))`、`ts_std_dev+group_neutralize`。
- **高衰减（避免）**：`-FIELD*ts_std_dev(FIELD,N)`（IS 高但 OS 衰减严重）、`vector_neut(a,b)`（高 IS 但 OS 普遍不及预期）、异质波动率 `group_mean(ts_std_dev)-ts_std_dev`。

### 5.3 相关性检验工具
- `check_correlation` / `check_self_correlation`（MCP）：提交前预检。
- `mining/scripts/mine_corr.py`：拉取一组 alpha 的**日频 PnL 两两相关系数**，验证"互不相关"（用于组合前去冗余）。
- 42 个 GLB emotion 族实测 prodCorr 0.82–0.86（>0.7），**100% 被 PROD 硬闸挡掉** → 同族盲提交是死路。

---

## 六、Stage 4 — 因子筛选与组合

### 6.1 单 Alpha 筛选
- 通过 IS 闸门 → `get_alpha_check(id)` 读 IS 闸门（注意 PROD 异步）→ prodCorr<0.7 且 selfCorr<0.7 → 提交。
- prodCorr≥0.7 → 信号族过度相关，需降相关/换信号方向。
- selfCorr≥0.7 → winner 周围 family 变 self wall，做更远 field-level move。

### 6.2 SuperAlpha（组合层）
- **工作流**：`selection` 表达式从 OS 池自动筛选组件 + `combo` 组合（type=SUPER）。
- **成功配方**（USA `gJ8eVmNM` / `KPGvRMg1` ACTIVE）：
  - `selection = (prod_correlation > 0)`（USA 硬性要求，从全池自动筛正相关 alpha，因子暴露极度分散，绕过手动 children 的 prod_corr 墙）。
  - `combo = combo_a(alpha)`（唯一可靠组合算子）。
  - 至少 **10 个组件**（selection 结果须 ≥10）；`componentActivation=IS`；`startDate=2014-01-01, endDate=2023-12-31`；description ≥100 字符。
  - **关键杠杆**：中性化用 **SUBINDUSTRY**（非 MARKET）是把 PROD_CORRELATION 压到 0.7 下的决定性因素（MARKET 下地板 ~0.7169，SUBINDUSTRY 后 0.6944）。
- **失败教训**：手动指定 10 个 children（prod_corr 0.897）、`(color=="BLUE")` 筛选（0.907）、`selection='1'`（0.946）均因组合后 prod_corr>0.89 被拒；`reduce_avg/combo_a` 单侧负号报 "single expression" 错误；`(sharpe>X)` 非可用变量。
- **提交流程**：`submit_alpha(force=True)` → 常返 201 异步 → 再调一次直接回带 PROD/SELF 值的 verdict（403=FAIL 带 value，200="IS checks passed"=全过）。命名用 prodCorr 最大值（如 `0.6944`）。

### 6.3 组合不可行的约束（重要）
- 非 USA 区域（KOR/MEA/IND 等）组件池高度同质（value/quality 因子），任意子集组合 ~0.9 相关 → SuperAlpha **硬性要求 ≥10 合格组件**，当前非 USA 区域均不满足，路线封死；唯一解锁＝挖 novel 信号族凑齐组件池。

---

## 七、Stage 5 — 落地应用（部署 / 提交 / 监控）

### 7.1 提交流程
1. 提交前：`get_alpha_check(id)` 读 IS 闸门（PROD 异步，首检可能空）。
2. 提交：`POST /alphas/{id}/submit`，**描述须 ≥100 字符**（三段英文：idea / 数据字段 / 操作符）。
3. 提交后：轮询 `/check` 读 prodCorr/selfCorr，分类 SUBMITTED / DROP_PRODCORR / DROP_SELFCORR。
4. 限速：429 THROTTLED 需指数退避；批量提交触发账户级限速。

### 7.2 RA vs PPA 提交路径
| 类型 | 闸门 | 通道 | 注意 |
|---|---|---|---|
| RA（常规） | Sharpe>1.58 / Fit>1.0 / Margin>5bp | MCP submit_alpha 或 web UI | MCP 预检 margin>15bp 误拦，web UI 接受 ~5bp |
| PPA（Power Pool） | Sharpe≥1.0 / 算子≤8 / 字段≤3 / PC<0.5 | **仅 web UI**（当期活跃主题窗口内） | MCP submit_alpha 非 PPA 感知，合法 PPA 也照拦 |

- PPA 区域主题轮动：平台按赛季开放某区域/主题，非活跃区域报 "does not match any Power Pool Theme"；先看平台右上角铃铛确认当期主题。
- PPAC 隐蔽卡点：PP 相关性>0.5 时系统借 PROD_CORRELATION 名义报 FAIL。

### 7.3 监控与效率
- **进程监控第一视角 = 机器级全量 Python 进程枚举**（`Get-CimInstance Win32_Process -Filter "Name='python.exe'"`），按命令行分类 SCAN / MCP-SVC / WATCHDOG / EDITOR / OTHER。陷阱：只用 `scan_v*` 过滤会漏非标准命名任务（如 `tabbit_option9.py`、`glb_pipeline.py`）；`*_progress_*.log` 绝不能作为任务发现入口；MCP-SVC 是服务端回测宿主，其任务须到 WQ BRAIN 控制台查看。
- **并发模型**：`SIMS_PER_BATCH=8` 一次 POST 提交 8 条 multi-sim，服务端 8 路并行；batch 间客户端串行（已匹配账号并发上限，吞吐瓶颈在 simulation 时长本身）。基准：multi(8)=86.1 α/hr vs single=54.3 α/hr（1.59×）。
- **故障处理**：8 子模拟全 ERROR → 先重发 1 次（多为瞬态）；CROWDING 中性化连续 2 次重发仍失败 → 跳过；fatal operator 级联 CANCEL → 隔离独立小批；瞬态 "try again" → 拆 5 条/批。
- **断点续跑**：checkpoint `results/<task>_checkpoint.json`，原子写 `os.replace(tmp, path)`；只把拿到 pid 的算"已完成"；`V<NN>_FRESH=1` 强制全新；离线用 fake `WqApiSimple` 桩三遍验证 fresh/resume/partial。

---

## 八、关键经验、常见陷阱与最佳实践

### 8.1 致命错误（已验证，勿再犯）
1. **EUR 战役 32 次无效回测**：没跑体检就选了 4 个劣质数据集 → 体检先行，不可跳过。
2. **42 个 GLB emotion 族盲提交**：全是 PROD_CORRELATION 死路 → 先 5 个探针再全量。
3. **PROD_CORRELATION 误判**：首检返回 0 FAIL，重检才暴露 → 须以重检为准。
4. **ts_entropy 级联 CANCEL**：一个 fatal operator 取消整个 20 条 multisim → 隔离不确定算子。
5. **跨区域误推荐**：fundamental86 在 EUR "0 字段" 实际是区域不提供 → 换区域查一遍（它在 KOR 可用）。
6. **MCP submit_alpha 非 PPA 感知**：合法 PPA 被常规闸门拦 → PPA 走 web UI。
7. **PPA 区域主题轮动**：非活跃区域报 "does not match" → 先看铃铛确认当期主题。

### 8.2 效率陷阱
- 只用 `scan_v*` 过滤进程 → 漏非标准命名任务。
- 日志作任务发现入口 → 漏 MCP 宿主。
- 批次级偶发 ERROR 当表达式问题 → 先重发 1 次。
- CROWDING 中性化重发 → 直接跳过。
- 并发争抢 MCP 会话 → 串行调用。

### 8.3 信号构建陷阱
- 水平信号套 `ts_av_diff` → 洗掉信号（借贷利用率是水平信号）。
- 有界字段 winsorize → 有害（搜索热度无需截尾）。
- 事件表达式用 `and` 连接 → 语法错误，用嵌套 `if_else`。
- 短窗口用于 D1 / 长窗口用于 D0 → 2Y 与 sharpe 错配。
- winner 周围 family 盲提交 → self wall，做更远 field-level move。

### 8.4 最佳实践（论坛铁律 + 实证）
- **低 prodCorr 是最宝贵资产** —— 直接拉升 Base、驱动 Genius 多样性。
- **换壳（group_rank→group_zscore）比磨参数更有效** —— 降相关首选。
- **trade_when 是 2Y 衰减与 turnover 的结构性解法**（不只是调参）。
- **quantile 外包装强于 rank**（sub_universe/2Y 双达标）。
- **简单模板抗衰减**：`group_rank(ts_rank(FIELD,60), group)` 过拟合风险最低。
- **MCP 会话常驻**（localhost:8876）共享会话比直连 API 稳（规避沙箱 TLS 抖动）。

---

## 九、可复用优化思路

1. **turnover 自适应 decay**（按 tvr 反推 decay）：`tvr>0.7→decay*4; >0.6→decay*3+3; >0.5→decay*3; >0.4→decay*2; >0.35→+4; >0.3→+2`。验证：decay 10→15 提升 margin 4.57→5.04bp；decay=4 比 20 提升 sharpe +13–17%。
2. **margin 提升**：长 decay（10→15）+ FAST 中性化。
3. **2Y 衰减修复**：trade_when 事件工程（EUR mdl110 验证 2Y 0.93→1.35）。
4. **降 prodCorr**：① 换壳 group_rank→group_zscore；② SA 组合层用 SUBINDUSTRY 中性化（单 alpha 无效，仅组合层有效）；③ 同字段 vec_avg→vec_max。
5. **GLB 三区域检查**：`group_rank(ts_rank(ts_backfill(F,60),N), country)`。
6. **SuperAlpha 绕墙**：`selection=(prod_correlation>0)` 从全 OS 池自动筛选，因子暴露极度分散。
7. **数据集评分模型**：`score = pyramidMultiplier × valueScore × (1/max(alphaCount,1)) × coverage`，优先高倍率+高价值+低竞争+高覆盖。
8. **代码架构收敛**：`mine_core.py` 把 21 个 `mine_v*` 版本差异收敛为"数据（候选 + 设置）"，统一 checkpoint/resume，杜绝版本爆炸。
9. **提交探测协议**：按 sharpe 排序选 5 个最大化多样样本（不同前缀×universe×neutralization）先探针，全 FAIL 即停，避免盲提交浪费时间。

---

## 十、工具与脚本索引

| 工具 | 路径 | 用途 |
|---|---|---|
| eur_field_coverage.py | `tools/` | 数据集体检（MCP+直连双通道） |
| dataset_health_check.py | skill 内 | 数据集体检（随 skill 分发） |
| webdata_quality.py | `tools/` | WebData 离线包质量分析（msgpack） |
| fetch_all_universes.py | `tools/` | 全区域合法 universe 拉取固化 |
| mine_core.py | `mining/scripts/` | 参数化 Alpha 挖掘模板（checkpoint/resume） |
| mine_corr.py | `mining/scripts/` | 日频 PnL 两两相关性验证 |
| heuristic_engine.py + rules.json | `mining/scripts/mining_experience/` | 规则驱动批量表达式生成 |
| harvest_fields.py / harvest_usa.py | `mining/scripts/` | 字段收割与打标 |
| glb_pipeline.py | `glb_alpha_machine/` | GLB 多阶段挖掘流水线 |
| glb_batch_submit.py | `deliverables/tools/` | 批量提交 + 闸门判定 |
| create_super_alpha.py / super_alpha_tool.py | `world-quant-brain-mcp/` | SuperAlpha selection+combo |
| forum_research.py | `tools/` | 论坛直连研究（Zendesk 通路） |

> **运行环境**：统一使用 MCP 服务 `.venv`（`world-quant-brain-mcp/.venv/Scripts/python.exe`，Python 3.13.8，42 包）；MCP 服务监听 `0.0.0.0:8876`，端点 `http://localhost:8876/mcp`，49 个工具，激活需对 `wq-brain` 点 Trust。

---

## 十一、待验证方向

- [ ] GLB stage2 group 残差能否突破裸字段 |sharpe| 0.52 上限；stage3 trade_when 能否解决 turnover 0.01–0.125 过低。
- [ ] news_sentiment_nlp 三区零竞争数据集（valueScore 9.0、alphaCount 0）的实际挖掘效果。
- [ ] 受控并发压测确证账号并发槽位上限。
- [ ] PPA 主题轮动时间表预测（Competition board API）。
- [ ] 信念熵模板替代算子（`ts_std_dev` 近似）效果验证。
- [ ] 非 USA 区域 novel 信号族挖掘，以解锁 SuperAlpha（≥10 合格组件）。

---

*本文档整合自项目经验总纲、WQ Alpha 挖掘方法知识库、已提交 Alpha 经验总结，及 `mining/`、`world-quant-brain-mcp/` 实际代码，覆盖 2026-08-01 至 2026-08-14 全周期实证。*
