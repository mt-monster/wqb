# S1/S2/S3 挖掘链路优化评估 v2（2026-09-17 14:30）

> 上轮v1（`ra_pipeline_s123_optimization_20260917.md`）的 7 条建议已大部分落地：
> 闸5 结构判定✓、窗口白名单机械化✓、catalog 闸✓、source/skeleton/exposure 写入链路✓、
> 补门禁规划器✓、prod_corr 落库工具✓、ideas_gen 归档✓。
> **本轮不重复旧结论**，用当日实测回答一个新问题：**已落地的修复真的接进实际流程了吗？**

## 0. 结论先行

**上轮的问题（规则没生效）已基本解决；现在的问题换成了三类：**

| # | 新问题 | 一句话证据 |
|---|---|---|
| A | ★★★ **修复接在了没有流量的支路上** | `skeleton`/`bucket`/`expected_exposure` 三列**全库 0 行**，而今天新增 3,187 条；真实落库入口（MCP 工具）**根本没暴露 source 参数** |
| B | ★★★ **S3 堵点在 EUR，不在 USA** | EUR 2,235 条 gated 只回了 44 条（**消化率 2%**），其中 1,891 条是 8/24-25 的陈货 |
| C | ★★ **USA 是信号质量问题，不是管道问题** | 近 7 天 582 次回测：sharpe 48% 为负、仅 2 条 ≥1.58、fitness 无一条 ≥1.0 → **0 达标** |

## 1. ★★★ 最重要发现：三列零数据 = 修复未接入实流

### 实测
```
expressions 总行=22,767
  source               非空=2,247   ← 全是 8 月 gem + 零星；今天 3,187 条新增**全 NULL**
  skeleton             非空=0
  bucket               非空=0
  selected             非空=22,767
  expected_exposure    非空=0
```
今天新增 3,187 条（最新 14:13），全部 `source=NULL`。

### 根因链（三步定位）
1. **实际生成链路**（提示词 `步 4`）：GEM headless runner 产出 `final_expressions.json`
   → **runner 自己完全不写 DB**（`run.py` 只在 355-360 行读 priors 快照）
   → 由 AI 调 **`mcp__wqb-db__upsert_expressions`** 落库（`brain-make-some-gem/SKILL.md:10` 引 `mcp__wqb-db__*`）。
2. **该 MCP 工具签名只有 5 个参数**（`wqb_db_mcp.py:906`）：
   `region / wave / expressions / dataset / status` —— **没有 `source`**。
   → 我上轮在 `store/_expressions.py` 加的 `source` 形参、`gem.py::_label_source`，
   在这条链路上**永远接不到值**。
3. **`gem_wave` 节点**（我修复写回的那个）**不在实际流程里**——提示词步 4 只跑 runner + build-wave，
   从不调 gem_wave；`registry.py` 里注册了但没有消费方。故 `skeleton`/`bucket` 恒空。
   另：`gem.py` 的 `_label_source` 位于 `detached` 分支的**等待路径**，若用 `launch_only`（1s 返回）则不执行。

### 影响
- 一切按 `source` 切分的生成质量统计**都看不到当前语料**（延续上轮结论）；
- `skeleton` 空 → **生成期骨架去重无法度量、也无法执行**（去重逻辑在被架空的节点里）；
- `expected_exposure` 空 → GEM 规则 7/8 仍不可验证（`gate._persist_exposure_map` 只在门禁跑到 exposure map 时才回填）。

### 修法（小改，高杠杆）
- `wqb_db_mcp.upsert_expressions` 增可选 `source` 形参（缺省 None 不改行为），并透传到 store；
- 该工具**顺带算 skeleton**（`wqb.expression.skeleton.structural_signature` 是纯函数、零成本）
  → 每一行入库即有骨架，去重与复用率立即可测；
- 提示词步 4 明确要求传 `source="gem_<mode>"`（phased/skeleton/single）。

## 2. S1：catalog 覆盖 70/93（缺 23）

| 区 | 白名单 | 缺 catalog |
|---|---|---|
| **JPN** | 12 | **10**（83%）|
| **GBR** | 11 | **6**（55%）|
| CHN | 3 | 1 |
| 其余 9 区 | — | 0 |

CHN/DEU/EUR/GLB/HKG/IND/KOR/MEA/USA 全部齐备。缺集集中在 JPN/GBR——**且这两区的缺集在白名单里占多数**，
意味着它们的"开区"本身就不成立（catalog 闸③现在会把它们拦在开波前，这正是预期行为）。

**修法二选一**：① 对缺集跑 `scan_fields` 补 catalog（注意 JPN/DEU 无法用本地 WebData ZIP 生成，
需 WebDataScope 导出包）；② 把长期无法补齐的集**移出白名单**，让白名单反映真实可挖范围。

## 3. S2：生成质量——纪律生效了，但新的漏点出现

### 3.1 今日 3,187 条实测

| 指标 | 值 | 判读 |
|---|---|---|
| 加权混合（新结构判定） | **1 条 (0.0%)** | ★ 禁加权混合纪律**已完全落地** |
| 非白名单窗口（闸9 告警） | **845 条 (26.5%)** | ★ 比历史 21% 还高——窗口纪律**没有落地** |
| 骨架：唯一 462 / 复用率 6.9 | ≥8 大簇覆盖 **71.5%**，最大簇 56 条 | 比 8 月(12.6)有改善，但**同形状内仍重** |
| Top 骨架 | `divide(subtract(F,F),F)` ×56 / `divide(subtract(F,F),add(F,N))` ×50 | 结构交互形状对了，簇内过度复用 |

### 3.2 两个漏点
1. **窗口白名单只警告不阻断**（闸9）且提示词只写散文 → 生成端不遵守。既然"禁加权混合"能靠**硬 block** 落地，
   窗口纪律也应按同一模式处理（生成端对齐 + 必要时升 enforce）。
2. **骨架去重没接实流**（见 §1）：当前 71.5% 落大簇的状态，正是它本该抑制的。

### 3.3 USA 生成质量问题（非管道问题）
近 7 天 USA 回测 582 条：sharpe 48% 为负 / 33% 在 0-0.5 / 仅 2 条 ≥1.58；fitness 52% <0.5、**无一条 ≥1.0**。
→ 继续在 USA 加大生成只是烧槽位（今日 USA 仍生成 2,843 条，占全天的 89%）。

## 4. S3：真正的堵点

### 4.1 消化率（gated → backtested）
| 区 | gem | gated | backtested | 消化率 |
|---|---|---|---|---|
| **EUR** | 4,869 | **2,235** | **44** | **2%** ★ |
| IND | 554 | 309 | 175 | 36% |
| DEU | 1,198 | 66 | 171 | 72% |
| USA | 3,109 | 0 | 350 | — |
| JPN | 1,672 | 1 | 0 | 0% |

EUR 的 2,235 条 gated 里 **1,891 条创建于 8/24-8/25**（波 80/83/51-54），滞留 3 周以上；
而 EUR 近 7 天回测 173 条产出 22 达标（12.7%，max 2.09）——**EUR 不缺信号，缺的是消化**。

### 4.2 其余
- **prod_corr 覆盖 6.5%**（270/4,137）——落库工具已就绪，但"抽测→落库"未接进循环；
- **358 组 / 5,691 条**历史无门禁债（A 类 278 组 / 4,905 条命令已生成，待执行）；
- **度量缺口**：今日 s2_* 波的 `gate_results.report_json` 是 pipeline 式 schema（`passed=None`），
  门禁通过率**不可查**——这是漏斗只能按表达式条数推的原因。

## 5. 优先级建议（新）

| 序 | 动作 | 类型 | 风险 |
|---|---|---|---|
| ① | MCP `upsert_expressions` 暴露 `source` + 自动算 skeleton；提示词步 4 传值 | 小改 | 低（解锁全部度量）|
| ② | EUR 积压裁决：跑 A 类补门禁命令的 EUR 部分 + 8/24-25 陈货标 dropped 或优先消化 | 批量写 | 中（需确认）|
| ③ | 窗口纪律落地：生成端加约束 + 闸9 视情况升 enforce | 小改 | 低-中 |
| ④ | USA 生成止损：暂停 USA 新波，把槽位转 DEU/EUR（EUR 有 12.7% 达标率）| 策略 | 低 |
| ⑤ | prod_corr 接循环（每轮 S3 后 triage→persist）| 中 | 低 |
| ⑥ | JPN/GBR：补 catalog 或收缩白名单 | 中 | 低 |

**明确不建议**：继续加大 USA 的生成吞吐（0/582 的输出不值得更多槽位）。
