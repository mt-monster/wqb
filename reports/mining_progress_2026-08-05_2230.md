# WQ PPA 挖掘进展半小时报

**报告时间**：半小时报自动化触发（续 08-05 22:25 条目）
**监控视角**：机器级 Python 进程枚举为第一视角，v 日志仅作 scan_script 明细补充

---

## §1 Python 进程角度全量盘点

| 类别 | PID | 命令行 / 身份 | 线程 | 内存 | 累计CPU | 状态 |
|---|---|---|---|---|---|---|
| **MCP-SVC** | 95104 | `world-quant-brain-mcp/.venv/.../python.exe main.py` | 22 | 362.4 MB | — | **活跃**（回测宿主，port 8876 = True） |
| **MCP-SVC** | 43756 | 同上 `main.py` | 1 | 5.5 MB | — | 空闲（副实例） |
| EDITOR | 83024 / 87804 / 95368 | 空 cmdline / ms-python·jedi 语言服务 | 25×3 | 97/53/348 MB | — | 空闲（IDE 语言服务） |
| EDITOR | 3628 / 91788 / 91844 | 空 cmdline stub | 1×3 | 4/3.6/3.5 MB | — | 空闲（派生子进程） |

- **SCAN 进程**：0（无任何 `scan_*`/`tabbit_*`/`*_miner.py` 本地驱动在跑）
- **node.exe**：0（无 `host_labs` 等宿主）
- **关键结论**：回测宿主（MCP-SVC）健康在线，但**本地没有任何驱动脚本在喂任务** → 当前吞吐 = 0。瓶颈不在本地算力，而在平台侧闸门（prod_corr）与数据可用性。

---

## §2 逐任务并发模型 + 进度

### 2.1 EUR 战役（`/goal` 原目标）—— 已执行并**判定为死路**
来源：`tracking/mining/eur_track_conclusion.json` + `result_*_eur_b*.json`

| 项 | 值 |
|---|---|
| Track | EUR / TOP1200 / D1 / REGULAR / max_trade ON |
| 批次 | b1 model30（REVERSION_AND_MOMENTUM）、b2 model30（CROWDING）、b3 pv20（INDUSTRY）、b4 news21（REVERSION_AND_MOMENTUM） |
| 总回测 | 32 |
| 结果 | model30 sharpe 0.3–0.6 全灭；pv20 −0.06~0.36 全灭；news21 0.03–0.72 全灭 |
| **根因** | **数据包过期**（数据包 2026-02 与平台脱节）→ 预筛推荐集（fundamental86/risk59/model216/fundamental94）平台 0 字段；可用数据集信号全灭 |
| **结论** | **EUR 无达标候选（天花板 0.72）。等数据包更新或平台灌数据后重探** |

> 这意味着 `/goal` 设定的「挖 3 个分属不同数据集、彼此相关<0.4 的可提交 EUR alpha」目标，在当前数据状态下**物理上不可达成**。按你「不要提交 / 不要创建自动化」的约束，我未擅自新建任何战役或自动化，仅如实汇报该结论。

### 2.2 USA 战役 b107–b128 —— 已结束
来源：`tracking/mining/usa_campaign_summary_b107_b128.json`

| 项 | 值 |
|---|---|
| 范围 | 9+ 族 / 15 批（option40、other566、risk65、fundamental91、model239、sentiment21/other696、blends） |
| 强信号命运 | 所有 sharpe>1.5 的强信号均被 **prod_corr>0.7 封顶**（最佳 0.724，gap 仅 0.024） |
| set_alpha_properties | 4 个（LLGJMOGa sh2.08 / pwNOd9OX sh1.97 / WjA8Ov6x / 另一）满足「不含 prod_corr」闸门 |
| **可提交（prod_corr<0.7）** | **0 个** |
| 最近邻 | option40 系（A17oXw3g/QP9wR6WG sh2.03，prod_corr 0.724，但 ops=15 超标）；2rN3V7KP（prod_corr 0.744，ops=10 超标） |
| 去相关对 | pwNOd9OX ↔ VkGJ73eA 互相关 0.2（唯一 <0.4 对） |

### 2.3 KOR 实时结果（最近一次本地活动，08-05 16:21–22）
来源：`wqb-share-03/tracking/kor_*_results.json`（服务实时输出路径）

| 批次 | sim 状态 | alpha 数 | 表达式特征 | 指标 |
|---|---|---|---|---|
| kor_ttm_blend_b7r | 8× COMPLETE | 9qpQn8A2, wpaVr3n5, O0Gv3Rbg, ZYELJgjZ, kqP5Avng, zqNzVg5E, rK2mx9Am, e73JjNLO | `subtract(ts_rank(anl39_*), reverse(group_rank(ts_rank(average_spread_slippage), sector)))` | **未取回** |
| kor_other323_b5c | 2× COMPLETE | d5ZwzEgg | `subtract(group_rank(ts_rank(average_spread_slippage,44),sector), ts_rank(vec_avg(oth323_esor),22))` | **未取回** |
| kor_other323_b5d | 2× COMPLETE | YPvdzWmM | 同上（SECTOR 中性化） | **未取回** |

- 共 **12 个 COMPLETE sim**，但 result 文件仅含 `status/alpha_id/settings/expression`，**不含 sharpe/fitness/prod_corr** → 需经 `get_user_alphas` 拉取指标后才能判定闸门。
- 驱动进程已退出（SCAN=0），这 12 个 alpha 处于**「完成待取回」**状态，与历史 b87/b92/b93 同一模式。

### 2.4 历史可提交候选（待你手动提交）
- `xAdL5vmN`（b86–b94 时代篮子 #2 ✅）：当时判定 prod_corr<0.7 可提交，至今**仍未提交**（你要求手动提交）。

---

## §3 回测效率结论

1. **当前瞬时吞吐 = 0 α/hr**：无本地驱动在跑。MCP 宿主（PID 95104，22 线程，port 8876 存活）空闲待命，多模拟 8 并发能力未被利用。
2. **历史基准**：b86–b94（USA）共 7 批 48 sim，**0 通过闸门（0%）**；预算约 302/300 已超支，仅 1 个可提交（xAdL5vmN）。
3. **真实瓶颈非算力**：
   - EUR：数据过期 → 信号全灭（非并发问题）；
   - USA：prod_corr 天花板 0.724 → 强信号被平台相关性闸门封死（非并发问题）；
   - KOR：sim 已跑完但指标取回 backlog 未清（流程断点，非算力）。
4. **建议**：提高总吞吐**不能靠加本地并发**。优先级应为：① 清 KOR 12 个 alpha 的 `get_user_alphas` 取回 backlog；② 对 KOR 达标项走 test robust + 严格过拟合测试；③ EUR 静候数据包刷新；④ USA 仅 option40/fundamental91 距 prod_corr 门槛 0.02–0.07，可等新主题/新数据包后微调重战。

---

## §4 `/goal` 战役设定请求的落地状态

- 原请求要求「设置好 EUR 战役属性、禁用 trade_when/add/multiply、multi_create_simulate 8 并发、每 10 轮多样性评估、不要提交、不要创建自动化」。
- **实际落地**：该 EUR 战役**已被执行并得出结论**（见 §2.1），过程遵循了 REGULAR / max_trade ON / D1 / 多数据集轮探的设定；但因**数据包过期导致 0 候选**，无属性可固化、无 alpha 可提交。
- 我**未创建任何新自动化任务**（遵守约束），也未自动提交。
- 「每 10 轮回测多样性评估」属驱动脚本内逻辑，EUR 轮次在耗尽模板多样性前已被数据失效截断，故未触发完整 10 轮评估闭环——这本身也是「数据集信号全灭」结论的佐证。

---

## §5 行动项（供你决策）

| 优先级 | 项 | 说明 |
|---|---|---|
| 🔴 高 | KOR 12 alpha 指标取回 | `get_user_alphas` 拉 kor_ttm_blend_b7r / kor_other323_b5c / b5d 的指标，判定是否过闸 |
| 🔴 高 | 提交 xAdL5vmN | 历史唯一确认可提交 alpha，待你手动提交 |
| 🟡 中 | KOR 达标项 robust + 过拟合测试 | 取回后若有 sharpe>1.58 且 prod_corr<0.7 者，按 /goal 流程测试 |
| 🟡 中 | USA option40/fundamental91 微调 | 距 prod_corr 0.7 仅 0.02–0.07，等新数据包/新主题后重战 |
| ⚪ 低 | EUR 重探 | 等数据包更新或平台灌数据（fundamental86/risk59 等恢复字段） |
| ⚪ 低 | MCP 目录重命名 world-quant-brain-mcp→mcp | 此前因服务锁目录暂缓，需干净维护窗口执行 |
