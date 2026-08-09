# WorldQuant Alpha 挖掘方法知识库

> 本文档沉淀在项目中验证有效的信息挖掘方法、技巧与流程知识，形成可复用的知识体系。
> 所有方法均经实证验证（2026-08-01 至 2026-08-08），标注验证状态与适用条件。
> 用途：新战役启动参考、团队协作知识传递、避坑指南。

---

## 一、挖掘流程总览

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 0: 平台实时体检（不可跳过）                                  │
│  get_datasets → cov≥0.85 + alphaCount≤50 + fieldCount≥10        │
│  排序: pyramidMultiplier↓ → alphaCount↑ → coverage↓              │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: 字段级诊断 → 选预处理模板                                 │
│  MATRIX: winsorize(ts_backfill(F,120),std=4)                    │
│  VECTOR: winsorize(ts_backfill(vec_avg(F),120),std=4)           │
├─────────────────────────────────────────────────────────────────┤
│  Step 2: 一阶批量算子扫描（12算子×5窗口=60变体/字段）              │
│  prune 按字段前缀去重（每字段保留 top N）                          │
├─────────────────────────────────────────────────────────────────┤
│  Step 3: 二阶 group 包裹（group_rank/zscore/neutralize）          │
│  分组: sector/industry/subindustry/country(GLB)/bucket(rank)     │
├─────────────────────────────────────────────────────────────────┤
│  Step 4: 三阶 trade_when 事件工程                                  │
│  开仓事件: 量价条件 / ts_zscore / group_rank / ts_arg_max         │
│  退出事件: abs(returns)>0.1 或 -1                                  │
├─────────────────────────────────────────────────────────────────┤
│  Step 5: 闸门预检 + 提交探测                                       │
│  check_self_correlation → submit probe → /check prodCorr         │
└─────────────────────────────────────────────────────────────────┘
```

### 1.1 流程纪律

1. **体检先行**：开战役前必跑 `tools/eur_field_coverage.py` 或 `dataset_health_check.py`，三条硬门槛一票否决。
2. **整轮验证**：每轮超过 10 种不同结构后才考虑转向，不可 1-2 个字段就下结论。
3. **断点续跑**：所有回测脚本必须支持 checkpoint/resume，`V<NN>_FRESH=1` 强制全新。
4. **小批探测**：不确定算子隔离到独立小批次（避免级联 CANCEL）。
5. **提交探测零成本**：硬闸失败不消耗周额度，但浪费时间——先 5 个多样化探针再全量。

---

## 二、数据集选择方法

### 2.1 评分模型

```
score = pyramidMultiplier × valueScore × (1 / max(alphaCount, 1)) × coverage
```

- 高分 = 高倍率 + 高价值 + 低竞争 + 高覆盖。
- 实测最优：news_sentiment_nlp（KOR/HKG valueScore 9.0, alphaCount 0, pm 1.7-1.8）。

### 2.2 避坑清单（已验证无效的数据集）

| 数据集 | 区域 | 最优 sharpe | 失败原因 | 验证批次 |
|---|---|---|---|---|
| model30 (star_eps_surprise) | ASI | 1.49 | 去掉 liquidity filter 后天花板~1.49 | opt_b1 |
| model165 | GLB | 0.48 | MODEL 金字塔无信号 | b74 |
| model227/239 | GLB | — | MCP 超时悬空 | b87/b88 |
| sentiment23 | GLB | — | 8/8 FAIL DEAD END | b94 |
| sentiment26 | GLB | 0.77 | APAC 区域负 | GLB 批次 |
| risk60/65 | GLB/USA | 0.70 | 三区域均<1 | b86/GLB |
| model26 | GLB | 0.54 | 信号弱 | GLB 批次 |
| other460 | GLB | -0.08 | 分类标签非连续 | GLB 批次 |
| option8 | USA/D0 | 0.83 | IV 信号弱，需 SLOW_AND_FAST+差分 | 1批 |
| news21 | EUR | 0.72 | cov.53 过低 | EUR 战役 |
| insiders12 | EUR | — | cov.20 过低 | EUR 战役 |

### 2.3 跨区域误推荐陷阱

- `fundamental86/risk59/model216/fundamental94` 不是"0 字段"，而是 **EUR 区域根本不提供**；它们在 KOR 全部可用。
- 判定某数据集不可用前，**先换区域查一遍**。
- 离线包 ★★★/☆☆☆ 只代表离线匹配度，**严禁**据此推断平台数据可用性。

### 2.4 各区合法 universe / delay / neutralization（2026-08-09 平台实测固化）

> 来源：`OPTIONS /simulations`（InstrumentType=EQUITY），脚本 `tools/fetch_all_universes.py`，原始数据 `tracking/mining/platform_universes_all_regions.json`。

| 区域 | Delay | Universe | Neutralization 特色 |
|---|---|---|---|
| USA | 0,1 | TOP3000/TOP2000/TOP1000/TOP500/TOP200/ILLIQUID_MINVOL1M/TOPSP500 | 全11种，无COUNTRY |
| EUR | 0,1 | TOP2500/TOP1200/TOP800/TOP400/ILLIQUID_MINVOL1M/TOPCS1600 | 含COUNTRY |
| GLB | 1 | TOP3000/MINVOL1M/MINVOL10M/TOPDIV3000 | 含COUNTRY（三区域检查关键） |
| ASI | 1 | MINVOL1M/MINVOL10M/ILLIQUID_MINVOL1M/TOP500 | 含COUNTRY |
| CHN | 0,1 | TOP2000U | 无COUNTRY |
| HKG | 1 | TOP800/TOP500 | 无COUNTRY |
| KOR | 1 | TOP600 | 无COUNTRY |
| IND | 1 | TOP500 | 无COUNTRY |
| GBR | 0,1 | TOP700 | 无COUNTRY |
| DEU | 0,1 | TOP500 | 无COUNTRY |
| MEA | 1 | TOP400/TOP300 | **仅6种**（无STATISTICAL/FAST/SLOW等） |

**关键发现**：
- COUNTRY 中性化仅 EUR/GLB/ASI/MEA 支持——GLB 的三区域检查(AMER/EMEA/APAC)依赖 COUNTRY 分组。
- MEA 中性化选项最少（仅 NONE/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/COUNTRY），不支持 STATISTICAL/FAST/SLOW。
- USA 不支持 COUNTRY（单一国家无需）。
- Delay=0 仅 USA/EUR/CHN/GBR/DEU 支持；ASI/GLB/HKG/KOR/IND/MEA 仅 Delay=1。

---

## 三、算子使用技巧

### 3.1 预处理决策树

```
字段类型?
├─ MATRIX → winsorize(ts_backfill(F, 120), std=4)
├─ VECTOR → winsorize(ts_backfill(vec_avg(F), 120), std=4)
└─ 有界字段(如搜索热度) → 不需 winsorize（有害）
```

### 3.2 窗口选择规律

- **短窗口(5/22)**：2Y 好、sharpe 低 → 适合 D0（需 2Y≥2.69）。
- **长窗口(66/120/240)**：sharpe/fit 好、2Y 低 → 适合 D1。
- **甜点窗口**：搜索兴趣=92窗，analyst revision=60窗，fundamental=22→0.22 TVR / 240→0.07 TVR。
- **期限结构**：12m-1m=有效(+1.14)，36m-6m=反向(-0.62) → 短周期(1m~12m)动量效应。

### 3.3 中性化选择

| 区域 | 最优中性化 | 实测依据 |
|---|---|---|
| USA/D0 | STATISTICAL | search_interest: 2.47 > SLOW_AND_FAST 2.39 > FAST 2.32 > INDUSTRY 1.88 |
| EUR/D1 | INDUSTRY | STATISTICAL 2Y 仅 0.40 |
| KOR | SECTOR | 实测 0.562 |
| GLB | FAST | 9qpQ0VQ2 验证；CROWDING 不可用(连续 ERROR) |

**读取而非硬编码**：每个数据集有 dominant neutralization method 徽章（WebDataScope dataFlag.js），应读取后选择。

### 3.4 turnover 自适应 decay

```
if tvr > 0.7:  decay *= 4
elif tvr > 0.6:  decay = decay*3 + 3
elif tvr > 0.5:  decay *= 3
elif tvr > 0.4:  decay *= 2
elif tvr > 0.35: decay += 4
elif tvr > 0.3:  decay += 2
```

**验证**：decay 10→15 可提升 margin（4.57→5.04bp）；decay=4 比 decay=20 提升 sharpe +13-17%（model110）。

### 3.5 trade_when 事件工程模板

**开仓事件**（选一）：
1. `ts_corr(close, volume, 5) < 0` — 价量背离
2. `ts_mean(volume, 10) > ts_mean(volume, 60)` — 放量
3. `ts_zscore(returns, 60) > 2` — 极端收益
4. `group_rank(ts_std_dev(returns, 60), sector) > 0.7` — 高波动
5. `ts_arg_max(close, 5) == 0` — 近期新高
6. `ts_std_dev(returns, 5) > ts_std_dev(returns, 20)` — 波动放大
7. `rank(sentiment_field) > 0.75` — 情绪阈值（EUR mdl110 验证：2Y 0.93→1.35）

**退出事件**：`abs(returns) > 0.1` 或 `-1`（始终持有）。

**语法限制**：事件表达式**不支持 and 连接**（语法错误），用嵌套 if_else 替代。

### 3.6 关键算子效率对比

| 场景 | 最优算子 | 对比 | 结论 |
|---|---|---|---|
| 偏离信号(搜索兴趣) | ts_av_diff | ≫ ts_zscore/ts_mean/ts_delta | 偏离均值最强 |
| 水平信号(借贷利用率) | ts_mean | ts_av_diff 会洗掉信号 | 先诊断信号类型 |
| 外包装(sub_universe/2Y) | quantile | > rank | quantile 双达标 |
| GLB 三区域检查 | group_rank(country) | — | country 分组是关键 |
| 衰减加权 | decay_linear | — | 近权重高 |
| 降相关换壳 | group_zscore | > group_rank | 换壳比磨参数更有效 |

---

## 四、提交策略知识

### 4.1 提交决策树

```
alpha 通过 IS 闸门?
├─ 否 → 强化信号（stage2/3）或换数据集
└─ 是 → get_alpha_check(id) 读 IS 闸门
    ├─ PROD_CORRELATION 异步，首检可能空 → 重检
    ├─ PROD_CORR < 0.7?
    │   ├─ 是 → 提交（描述≥100字符三段英文）
    │   └─ 否 → 信号族过度相关，需降相关/换方向
    └─ SELF_CORR < 0.7?
        ├─ 是 → 提交
        └─ 否 → winner 周围 family 变 self wall，做更远 field-level move
```

### 4.2 PPA vs RA 提交路径

| 类型 | 闸门 | 提交通道 | 注意 |
|---|---|---|---|
| RA (常规) | Sharpe>1.58/Fit>1.0/Margin>5bp | MCP submit_alpha 或 web UI | MCP 预检 margin>15bp 误拦，web UI 接受~5bp |
| PPA (Power Pool) | Sharpe≥1.0/算子≤8/字段≤3/PC<0.5 | **仅 web UI**（当期活跃主题窗口内） | MCP submit_alpha 非 PPA 感知，照拦 |

### 4.3 提交探测协议

1. 从候选池按 sharpe 排序，选 5 个**最大化多样**样本（不同前缀×universe×neutralization）。
2. 逐个提交 + 轮询 `/check` 读 prodCorr。
3. 若 5 个全 FAIL prodCorr → 整族不可提交，停止盲目提交。
4. 若有 PASS → 按 PASS 样本特征扩展全量提交。
5. 429 限速 → 指数退避；批量提交触发账户级限速。

### 4.4 幽灵提交识别

- 现象：台账记 ACTIVE，但平台 `GET /alphas/{id}` 返回 HTTP 404。
- 原因：提交被静默丢弃但台账未更新。
- 处理：修正台账为 PHANTOM，标注"表达式本地已丢失，无法重新提交"。

---

## 五、回测效率优化

### 5.1 并发模型

```
客户端(串行 for 循环)
  └─ batch 1: POST multi-sim(8条) → 服务端 8路并行 → 轮询 COMPLETE → sleep 25s
  └─ batch 2: ...
  └─ batch N: ...
```

- **最优 batch 档**：SIMS_PER_BATCH=8（multi(8)=86.1 α/hr vs single=54.3 α/hr，1.59× 加速）。
- **串行 batch 已匹配账号上限**：8 路 multi-sim 占满并发槽位，客户端串行非瓶颈。
- **要真正确证闲置槽位**：需受控并发压测（临时并行提交额外 batch 观察是否排队/429），但会干扰当前任务。

### 5.2 故障处理协议

| 故障 | 处理 | 验证 |
|---|---|---|
| 8子模拟全 ERROR | 重发相同表达式 | USA/D0 3次确认 |
| CROWDING 中性化全 ERROR | 跳过该中性化 | 连续2次重发仍失败 |
| fatal operator 级联 CANCEL | 隔离到独立小批次 | ts_entropy 案例 |
| 瞬态 "try again" | 拆成 5条/批 | e10a/e10b |
| 429 THROTTLED | 指数退避 | 账户级限速 |
| MCP 超时无 result | 检查 MCP 服务进程 | b87/b92/b93 悬空 |

### 5.3 MCP 会话管理

- MCP 会话须**串行**（并发争抢会串台）。
- 常驻 MCP(localhost:8876) 共享会话比直连 API 稳（规避沙箱 TLS 抖动）。
- MCP 服务持续向 `wqb-share-03/tracking/` 写结果（移走即再生），需改服务配置重定向。
- `world-quant-brain-mcp/` 重命名被服务派生进程锁目录阻塞，须维护窗口内停止全部派生进程后执行。

---

## 六、监控分析框架

### 6.1 进程监控标准流程

1. **机器级全量 Python 进程枚举**（第一视角）：
   ```powershell
   Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
   Select CommandLine, ThreadCount, WorkingSetSize, UserModeTime, CreationDate
   ```
2. 按命令行关键词分类：SCAN / MCP-SVC / WATCHDOG / EDITOR / OTHER。
3. **关键陷阱**：
   - 只用 `scan_v*` 过滤会漏掉非标准命名任务（如 `tabbit_option9.py`、`glb_pipeline.py`）。
   - `*_progress_*.log` 只是 scan_script 本地产物，**绝不能作为任务发现入口**。
   - MCP-SVC 是服务端回测宿主，其服务端任务须到 WQ BRAIN 控制台查看。
4. 对真正挖掘任务报：PID、启动时间、线程数、内存、累计 CPU 时间。

### 6.2 回测效率分析要素

- 读脚本确认并发配置：BATCH_SIZE / ThreadPool CONCURRENCY / 冷却秒数 / 数据集 / 账号。
- 读 checkpoint / results CSV 确认 done 数、候选数、最佳 Sharpe。
- 吞吐 = done / 已运行分钟；对比基准 multi(8)=86.1 α/hr。
- 判断是否跑在最大并发档、并发槽位是否闲置。
- 平台整体并发利用率：当前同时跑几个作业。

---

## 七、论坛研究方法

### 7.1 直连 Zendesk 通路（MCP 掉线时备用）

```
BRAIN Basic-Auth(POST /authentication) → JWT cookie
  → SSO(GET worldquantbrain.zendesk.com/access?brand_id=1500000894061)
  → HTML 搜索页(/hc/zh-cn/search?query=) [搜索API全404]
  → BeautifulSoup 解析 li.search-result-list-item
  → follow search-click 重定向得真实 post URL
  → JSON 读帖(/api/v2/community/posts/{id}.json + /comments.json)
```

限流：2-3s 间隔 + Referer + Accept: text/html + 406/429 指数退避。

### 7.2 高价值帖子挖掘

- 搜索关键词：alpha template / power pool / 信号构建 / 相关性 / 机器学习 / 因子 / 闸门。
- 投票数>20 的帖子优先精读。
- 提取模板时注意：算子可用性因账户/区域而异（如 ts_entropy 部分账户不可用）。
- forum_research.py 工具位于 `tools/forum_research.py`，用项目 .venv 运行。

### 7.3 论坛铁律

1. **低 prodCorr 是最宝贵资产**——直接拉升 Base、驱动 Genius 多样性。
2. PPA 提交时 prodCorr 豁免但受 PP 相关 ≤0.5 约束。
3. 换壳(group_rank→group_zscore)比磨参数更有效。
4. winner 提交后周围 family 变 self wall，需做更远 field-level move。
5. 低 pc SA 多用 STATISTICAL 中性化。

---

## 八、工具与脚本索引

> **项目运行环境**：项目无独立 .venv，所有工具统一使用 MCP 服务的 `.venv`（`world-quant-brain-mcp/.venv/Scripts/python.exe`）。
> 该 venv 是项目 .venv 的严格超集（42 包 vs 16 包），已包含工具所需的全部依赖（requests/bs4/dotenv/msgpack/pandas）。
> `requirements.txt` 保留为项目工具的依赖声明文档（MCP venv 已覆盖全部）。
> 如需重建：`python -m venv .venv && pip install -r requirements.txt`（但推荐直接复用 MCP venv）。

### 8.1 核心工具

| 工具 | 路径 | 用途 | 运行环境 |
|---|---|---|---|
| eur_field_coverage.py | `tools/` | 数据集体检（MCP+直连双通道） | MCP .venv |
| dataset_health_check.py | skill 内 | 数据集体检（随 skill 分发） | MCP .venv |
| forum_research.py | `tools/` | 论坛直连研究 | MCP .venv |
| fetch_all_universes.py | `tools/` | 全区域合法universe拉取固化 | MCP .venv |
| mcp_py | `tools/` | MCP 调用封装(urllib版) | MCP .venv |
| glb_batch_submit.py | `deliverables/tools/` | 批量提交+闸门判定 | MCP .venv |
| glb_pipeline.py | `glb_alpha_machine/` | GLB 多阶段挖掘流水线 | MCP .venv |
| mine_eur_mlfactor.py | `tools/` | EUR ml_factor_proj 批量仿真 | MCP .venv |
| webdata_quality.py | `tools/` | WebData 离线包质量分析 | MCP .venv(含 msgpack) |

> MCP .venv 路径：`D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe`（Python 3.13.8，42 包）

### 8.2 WQ API 封装

- `WqApiSimple`（wd_lib_wrapper.py）：get_alpha_details/get_alpha_check/submit。
- 位于 `C:\Users\MENGTAO\Desktop\E3\quant\worldquant_alpha\`（独立 WQ 工程，有自己的 .venv）。
- 系统 python `D:\softwares\vnpystudio\python.exe` 仅作 fallback（MCP .venv 不可用时）。

### 8.3 MCP 工具（49个）

关键工具：authenticate / create_simulation / create_multi_simulation / submit_alpha / get_datafields / get_datasets / check_correlation / get_user_alphas / search_forum_posts / read_forum_post / set_alpha_properties。

激活：WorkBuddy 连接器管理页对 `wq-brain` 点 Trust。

---

## 九、经验教训汇总（避坑清单）

### 9.1 致命错误（已验证，勿再犯）

1. **EUR 战役 32 次无效回测**：没跑体检就选了 4 个劣质数据集 → 体检先行，不可跳过。
2. **42 个 GLB emotion 族盲提交**：全是 PROD_CORRELATION 死路 → 先 5 个探针再全量。
3. **PROD_CORRELATION 误判**：首检返回 0 FAIL，重检才暴露 → 须以重检为准。
4. **ts_entropy 级联 CANCEL**：一个 fatal operator 取消整个 20 条 multisim → 隔离不确定算子。
5. **跨区域误推荐**：fundamental86 在 EUR "0字段" 实际是区域不提供 → 换区域查一遍。
6. **MCP submit_alpha 非 PPA 感知**：合法 PPA 也被常规闸门拦 → PPA 走 web UI。
7. **PPA 区域主题轮动**：非活跃区域提交报 "does not match" → 先看铃铛确认当期主题。

### 9.2 效率陷阱

1. 只用 `scan_v*` 过滤进程 → 漏掉非标准命名任务。
2. 日志作为任务发现入口 → 漏掉 MCP 宿主。
3. 批次级偶发 ERROR 当表达式问题 → 先重发 1 次。
4. CROWDING 中性化重发 → 直接跳过（连续失败）。
5. 并发争抢 MCP 会话 → 串行调用。

### 9.3 信号构建陷阱

1. 水平信号套 ts_av_diff → 洗掉信号（借贷利用率是水平信号）。
2. 有界字段 winsorize → 有害（搜索热度无需截尾）。
3. 事件表达式用 and 连接 → 语法错误，用嵌套 if_else。
4. 短窗口用于 D1 → 2Y 好但 sharpe 低；长窗口用于 D0 → sharpe 好但 2Y 低。
5. winner 周围 family 盲提交 → self wall，做更远 field-level move。

---

## 十、待验证方向

- [ ] GLB stage2 group 残差能否突破 |sharpe| 0.52 上限。
- [ ] GLB stage3 trade_when 能否解决 turnover 0.01-0.125 过低问题。
- [ ] news_sentiment_nlp 三区零竞争数据集的实际挖掘效果。
- [ ] 受控并发压测确证账号并发槽位上限。
- [ ] PPA 主题轮动时间表预测（Competition board API）。
- [ ] 信念熵模板替代算子（ts_std_dev 近似）的效果验证。
