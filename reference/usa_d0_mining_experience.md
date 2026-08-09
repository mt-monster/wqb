# USA D0 挖掘经验总结（2026-08-05，31 批）

## 1. 平台关键事实

### D0 硬门槛（远高于用户直觉指标）
| 检查项 | D0 门槛 | 用户指标 |
|---|---|---|
| LOW_SHARPE | **2.69** | >1.58 |
| LOW_FITNESS | **1.5** | >1.0 |
| LOW_2Y_SHARPE | **2.69** | >1.6 |
| margin | >5bp | >5bp |

**D0 三指标结构性 trade-off**：窗口短→2Y 好、窗口长→sharpe/fit 好，极难同时满足。
D1 门槛才是 1.58/1.0/1.58（用户指标口径）。

### 批次级偶发故障（已确认 3 次）
`create_multi_simulation` 提交后 8 个子模拟全部 ERROR（"There was an error while running..."），
**重发相同表达式即成功**——非表达式问题。遇到先重发 1 次再怀疑表达式。
例外：CROWDING 中性化在 USA/D0 连续 2 次全 ERROR（重发仍失败）→ 该中性化不可用。

### 算子/语法
- `reverse(x)` 与 `-x` 等价；`-rank(...)` 前缀会被本地 check_batch 判为"无外层包装"，
  用 `reverse(rank(...))` 可正确识别外层（reverse 是平台标准算子）
- `ts_backfill(x, 60)` 位置参数可用（用户旧 alpha 验证）
- VECTOR 字段必须 `vec_avg(F)` 聚合后再用 ts_* 算子
- quantile 支持 `driver=cauchy|uniform`（默认 gaussian）；cauchy 明显弱于 gaussian/uniform

## 2. 数据集信号档案

### search_interest（OTHER 类，userCount 27 极冷门）——探索 19 批
- **主信号**：`relative_interest_score`（Google 搜索热度）
- **最优**：`group_rank(ts_av_diff(ts_backfill(vec_avg(relative_interest_score),60),92),industry)`
  @ TOP3000/STATISTICAL/decay10 = sharpe 2.47 / fit 1.40 / 2Y 2.70✓ / margin 6.4bp✓
- 窗口 44-220 单调性：sharpe/fit↑ 但 2Y↓；92 窗是甜点
- `ts_av_diff`（偏离均值）≫ ts_zscore/ts_mean/ts_delta 变体
- blend（ris-tecs/tcom 双字段）全部无效（1.88-1.95 < 单字段 2.47）
- winsorize 有害（有界字段无需截尾）；TOP1000/TOP2000 信号崩溃（大盘股无搜索兴趣）
- 中性化排名：STATISTICAL(2.47) > SLOW_AND_FAST(2.39) > FAST(2.32) > INDUSTRY(1.88) > SUBINDUSTRY(1.83)
- 结论：**差 D0 门槛 0.22/0.10，用户指标全达标**，可作为 D1 或降门槛候选

### shortinterest3（SHORTINTEREST 类，users 24 冷门）——探索 11 批
- **主信号**：`loan_utilization_ratio`（借贷利用率）——**水平信号**！ts_av_diff 变换会洗掉信号
- **最优**：`reverse(quantile(ts_mean(vec_avg(loan_utilization_ratio),44)))`
  @ TOP3000/STATISTICAL/decay10 = sharpe 1.95 / fit 1.33 / 2Y 3.36✓ / margin 18.5bp✓
- 信号方向：高借贷成本/高利用率 → 做空（负信号取反）
- **quantile 算子重大发现**：sub_universe 0.46→1.01✓、2Y 2.74→3.01✓（远超 -rank 版本）
- last_diff_value（距上次变化值）次优 1.78；ts_ir 1.28；group_neutralize 1.51；
  ts_scale/ts_product/ts_kurtosis/ts_returns/ts_corr/ts_arg_max 均 <1.0
- FAST 中性化降 sharpe（1.82→0.99）；SLOW_AND_FAST 更差（0.64）
- 结论：**信号天花板 ~2.0，差 D0 门槛 0.74**，短借数据稀疏是主因

### option8（OPTION 类，users 高饱和）——1 批放弃
- IV 期限结构（30-360 差）、IV 水平/动量全部 <0.83，D0 门槛不可及
- 参考 D1 经验：option 类需 SLOW_AND_FAST + ivcall-ivput 差分才有效

## 3. 操作符探索率统计（用户已用 vs 新发现）

用户已用：rank/ts_mean/ts_sum/ts_delta/ts_rank/ts_backfill/group_rank/ts_av_diff/
ts_zscore/zscore/winsorize/ts_decay_linear/signed_power/subtract(+add/multiply/trade_when 禁用)

**新算子探索（全部平台接受）**：
- ✅ 有效：**quantile**（sub/2Y 大幅改善）、**last_diff_value**、ts_ir（中）、group_neutralize（中）
- ❌ 无效：ts_scale、ts_product、ts_kurtosis、ts_returns、ts_corr、ts_arg_max、normalize、
  group_zscore、group_std_dev、log、bucket（弱）

## 4. 方法论沉淀
1. **先验水平 vs 变化**：借贷成本/利用率是水平信号；搜索兴趣是偏离信号——先诊断再套模板
2. **quantile 是"外包装神器"**：sub_universe/2Y 双达标，比 rank 更强
3. **批次纪律**：8 并发 multisim；偶发 ERROR 重发即可；CROWDING(D0) 直接跳过
4. **D0 现实**：门槛 2.69/1.5 极高，单数据集达标难；满足用户指标(1.58/1.0/1.6)的候选
   可作为 D1 或提示用户降门槛
5. **点塔进度**：USA/D0/OTHER（2.47 候选）、USA/D0/SHORTINTEREST（1.95 候选）接近点亮

## 5. GLB 区域补充（2026-08-06 追加）

### GLB 已验证成功配方（用户 9qpQ0VQ2 同款，prodCorr 0.776 已提交）
```
group_rank(ts_rank(ts_backfill(winsorize(F, std=5), 60), N), country)
```
- 配置：**GLB/TOPDIV3000/D1/FAST/decay10/trunc0.04/nan OFF/maxTrade ON**
- **country 分组是 GLB 三区域检查（AMER/EMEA/APAC 均需 >1）的关键解法**
- techindi6_2 字段 @250窗 = 2.35/1.12/2Y 2.13/ra=0；@300窗/decay15 = 2.18/1.09/margin 5.04bp/ra=0
- 与已提交 _41 字段自相关 0.0（字段级去相关可行）

### GLB 提交门槛真相
- **submit_alpha 工具预检要求 margin > 15bp（误拦）**，但平台实际接受 ~5bp
  （用户已提交 9qpQ0VQ2 margin=5.06bp ACTIVE）→ 网页端手动提交即可
- margin 提升手段：decay 10→15（4.57→5.04bp）；历史 b16 记录 4.98bp 差 0.02bp 失败

### GLB 无效数据集档案（信号天花板，均 <1.1 不达标）
| 数据集 | 类别 | 最优 sharpe | 失败点 |
|---|---|---|---|
| sentiment26（网站流行度） | sentiment | 0.77 | APAC 区域负（COUNTRY 中性化翻正但天花板低） |
| risk60（证券借贷） | risk | 0.70 | 三区域均 <1 |
| model26（StarMine ARM） | model | 0.54 | 信号弱 |
| other460（DL 预测） | model | -0.08 | 分类标签非连续 |
| tech_chart_model（图表预测） | model | 1.09 | AMER/EMEA 区域 <1 |
| model243 已在 IND 成功 | model | 2.75(IND) | GLB 未试 |

### 批次级偶发 ERROR 规律再确认
批 44/45 首次提交 8 全 ERROR（"error while running"），重发即成功；
"Your simulation probably took too much resource" = 真问题（model26 364 字段 + ts_backfill 全历史超限，去掉 backfill 解决）。
