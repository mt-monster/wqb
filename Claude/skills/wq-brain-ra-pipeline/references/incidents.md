# 事故与教训登记（证据仓；正文只留规则，起因放这里）

> 旧 SOP 把「2026-xx-xx 新增 / 修正 / 事故」的叙述夹在规则里，规则被埋在起因后面（最长一个段落 ≈ 1000 字）。
> 现规则写在各步细则里、一条规则一句话；**起因、证据、当时的数字放这里**，每条指向「现在由谁拦」。
> 新增事故 = 在本表追加一行（编号递增），同时确认对应规则已落到代码或测试——**只写文档不算修复**。

| # | 日期 | 现象 | 根因 | 现在由谁拦 | 一句话教训 |
|---|---|---|---|---|---|
| I-1 | 2026-09-28 | KOR wave189 / 190 有 **7 条** `add(group_rank(腿A), group_rank(腿B))`（含 S=2.11 / F=1.80 / 2Y=1.89）全部漏过闸 5，属混信号调参，**已全部作废** | 文档写「`0.5*rank(A)+0.5*rank(B)` 均被闸 5 block」，**实现层是假的**：`_detect_weighted_mix_structural` 只拦「实参以 系数* 开头」的腿，明文豁免等权 `add(rank(a), rank(b))` <!-- lint:counterexample --> | 闸 5 毒模式 `equal_weight_leg_add`（结构判定 `_detect_equal_weight_leg_add`）、中缀 `+`（`infix_leg_sum`）、跨集价差（`spread_cross_dataset`），登记于 `platform_constraints.json` v1.6；`tests/unit/test_gate_equal_weight_leg_add.py`、`tests/unit/test_gate5_coverage_matrix.py`（含放行形态，防误伤：`add(abs(x),0.01)`、`add(ts_mean(x,22),ts_mean(x,66))`） | **门禁通过 ≠ 合规。**闸是兜底不是许可证；判合规先问「是不是两条独立信号腿相加」（步 7 §7.7） |
| I-2 | 2026-09-19 | IND pv103 尾盘反转 `mLm2xG1K`（S 3.83、IS 全过、prod 0.6997）先花约 1 小时做去相关变体，期间外部用户提交了同款，复查 prod = 1.0000，**整族封死** | 把「变体探索」放在「提交」之前 | D0-P 的 0.60–0.70 行：**不扩变体，当天进步 8**；`prod-first`（S3 收批后必调）把 prod 前移到扩批之前 | 同族第二颗的变体探索放在第一颗 ACTIVE 之后 |
| I-3 | 2026-09-26 | 3 颗候选因**只轮询不补发**悬空 > 24 h | 提交响应 ② / ③ 是「异步受理、结果未知」，被当成失败或忘了补发 | `submit_alpha` 节点内置四态处置（响应 ②/③ 且未翻 `ACTIVE` → 自动补发一次，仍卡记 `ASYNC_STUCK`）；四态表见 `worldquant-submit-alpha` | 「轮询查询失败」≠「提交失败」；判据只认 `status=ACTIVE` |
| I-4 | 2026-09-06 | S3 每次「启动成功」却**从未真跑**过 | 往命令里拼了不存在的 `--concurrency 7`：`pipeline.py` argparse exit 2，而 detached 启动器不看退出码 | `pipeline.py` 所有中止路径返回 rc = 2 且启动器据此判断；并发由 pipeline 内部锁定为 `min(7, 批数)`，`concurrency` 形参只是计划元数据（传非 7 只收 warning） | detached 任务必须校验退出码；干跑绿不等于能跑 |
| I-5 | KOR / fundamental17 首波 | 348 条产物里 **49.4%** 落在货币代码 / 汇率叉乘这类**非信号字段**上（语法全对、语义全废），而黑名单字段仅占全部字段 9.9%（37/373） | 跳过了语义归类；语法闸与 `gate.py` 都拦不住 | 闸 SEM（`wave_gate` 缺 `s1_semantic_<ds>` → exit 2；命中黑名单的表达式被剔出；`tests/unit/test_semantic_gate_failclosed.py`） | typed catalog 只回答「类型 / 覆盖」，不回答「这字段能不能当信号」 |
| I-6 | 2026-09-25 | 共享台账键 `s0_whitelist` **被整值覆盖**（细节未留档，只有 `upsert_ledger_key` 的 docstring 记了这一句） | `upsert_ledger_key` 缺省 `mode="replace"` = 整值覆盖，共享键被当成私有键写 | `upsert_ledger_key(..., mode="merge" \| "append")`（已有值类型不符即拒写，不静默覆写）；`s0_whitelist` 读取契约 `wqb.ledger_whitelist.normalize`（该键历史上有 5 种互不兼容形态） | 共享键增量写用 merge / append，禁整值覆盖 |
| I-7 | 2026-09 | EUR `continuation_score` 曾是 tier1 富矿，竞争者提交近同款后候选连带被生产池封锁：`le8Y68K2` 一夜 prod 0.6929 → 0.9932，全族归零 | 静态评分看不见「昨天还能打、今天已饱和」的动态 | S0 打分读 `saturated_datasets`（P2 降 `excluded`、P5 拍平 model 权重）；**写入方 = `campaign_intel.py mark-saturated`**（2026-09-29 补，此前该台账全仓库无写入方，反馈环是断的） | 反馈环要检查两端：有人读还要有人写 |
| I-8 | GBR | 跑满 **180 条**回测、max\|sharpe\| = 1.04、达标 0 | `diversity.signal_floor` 配置早就写好，但**零调用方** | 开波前 `signal_floor` 闸（2026-09-06 接线；整节缺失也 fail-closed） | 配置存在 ≠ 有人读；接线要有调用方证据 |
| I-9 | JPN w7 / w8 | 一条 `bucket()` 缺 range / 一个平台不认的字段，整批 8 条连坐；10 批丢 8 批 64 条 | 批内一条坏式 ERROR 会取消全部兄弟任务 | `pipeline.py` 连坐隔离（默认开）：定位坏式 → 回写 `expressions.status='fail'` → 其余表达式作重发批优先重发一次 | 不确定的字段 / 算子隔离到独立小批 |
| I-10 | GEM 无产出 | 报「no meta.json within 90s」，实为 LLM 通道 `402 Insufficient Balance`；**干跑（dry_run）显示 OK** | 报错误导；干跑只验命令构建，验证不了 LLM 可达 | 步 4 失败分支：先查 LLM 通道，不重试；旁路 = 手写 ideas md + `--ideas-file`（**手写 ideas ≠ 手写表达式**） | 干跑绿不证明 LLM 可达 |
| I-11 | HKG w4 | 七条里六条 `risk_neutralized_sharpe` 在 −0.33 ~ −0.57，raw sharpe 却非零 | 信号就是它声称的因子暴露，不是暴露之上的超额 | `review_wave.walls()/passes()` 的 `RN_EXPOSURE` 墙；步 7 §7.4 | 调参只会让暴露更纯 |
| I-12 | KOR | 选 risk70 做主攻集，跑完 **114 条**回测（best S = 0.87 / 0 near）才发现 IND / GLB 早有同集死路 | 死路查询是 region 作用域，系统性漏别区 | 步 1 §1.4 跨区死路检查；`s0-select` 的 `[跨区弱:…]` 标记 | 三区独立复现的负先验强于单区 S0 分数 |
| I-13 | GBR `intraday_pv_feats` | 整波退化为模板展开 | `workflow_feature_engineering` 产出的是确定性模板渲染（8 问框架 + `rank(ts_mean({f},66))`），被当 ideas 注入 GEM，GEM 一行 LLM 都不调 | 节点与 runner 主动跳过 `source ∈ {feature_engineering_node, standalone*}` 的文档；步 3 §3.4「仅人读、禁注入」 | 确定性模板不是 idea |
| I-14 | IND `intraday_pv_feats` | 价量相关反转连投 3 波 24 条（S 4.4–6.5、全 IS 过）后才查 prod = 0.79–0.92，整族报废；pv103 尾盘反转 8 条同理 | prod 检查排在链尾 | `prod-first`（S3 收批后必调）+ 闸 PF（骨架级死路预检，`--prod-family-gate` 默认开） | 先 prod 后 IS（信号强度 × 可打磨性 × prod 相关性三者不可兼得） |
| I-15 | 2026-09 | prod 墙 ≥ 6 套互相矛盾的处置学说并存（首探即判 / 串行探针 / 镜像稀释 / 组合腿救援 / 先 5 探针 / 区域预警线） | 各批次经验追加式合订，无总纲 | 决策表 D0-P（唯一一张）；区域 profile 不得另设预警线；DEC-07 | 同一情景只许一张表 |
