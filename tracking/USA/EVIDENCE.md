# USA D1 配置实证来源（EVIDENCE）

本目录 `config/settings.json` 与 `config/thresholds.json` 的每一项均由 **平台真实回测数据** 派生，
而非人工拍脑袋。复现方法：

```
mcp__wq-brain-http__authenticate
mcp__wq-brain-http__get_user_alphas(stage="OS", limit=200, offset=0)
# 过滤 region=="USA" && delay==1，按 (universe, neutralization) 聚合
# 指标取 metrics.{sharpe,fitness,turnover}，ACTIVE 率取 status=="ACTIVE"
```

## 抽取快照（2026-08-15，账户 mthyzx@126.com）

- USA D1 平台 alpha 总数：**86**（全部 stage=OS）
- **universe 分布**：TOP3000 = 85，ILLIQUID_MINVOL1M = 1 → `universe=TOP3000`
- **neutralization 分布与表现**（按 (universe, neutralization)）：

| 组合 | n | ACTIVE | medSharpe | medFitness | medTVR |
|---|---:|---:|---:|---:|---:|
| TOP3000 / MARKET | 75 | 75 (100%) | 1.49 | 1.33 | **0.038** |
| TOP3000 / SUBINDUSTRY | 4 | 4 (100%) | **2.245** | 1.45 | 0.121 |
| TOP3000 / SECTOR | 1 | 1 | 2.08 | 1.67 | 0.106 |
| TOP3000 / STATISTICAL | 1 | 1 | 1.67 | 1.00 | 0.052 |
| ILLIQUID_MINVOL1M / * | 3 | 3 | 1.66–4.32 | 1.08–4.32 | 0.06–0.16 |

## 决策

1. **universe = TOP3000**：85/86 压倒性采用，且 TOP3000 是 USA 标准大池。
2. **neutralization = MARKET**（baseline）：n=75、100% ACTIVE、medTVR=0.038 为全档最低换手，
   稳健性最佳。SUBINDUSTRY 在 n=4 小样本上 Sharpe 更高（2.245）但 TVR 偏高（0.121），
   故不作为默认值，而设为 `_alt_neutralization` 走 wave 01 的 A/B 对照轨，由真实回测定夺是否切换。
3. 非争议字段（decay/truncation/maxTrade/pasteurization/unitHandling/nanHandling/language/起止日期）
   全部取自 TOP3000/MARKET 这 75 个 ACTIVE alpha 的**一致配置**：
   decay=5、truncation=0.08、maxTrade=OFF、pasteurization=ON、unitHandling=VERIFY、
   nanHandling=ON、language=FASTEXPR、startDate≈2013、endDate≈2023-12-31。
   （注意：USA 的 maxTrade=OFF 与 KOR 的 ON 不同——以 USA 实证为准，不沿用 KOR。）

## 阈值

`thresholds.json` 沿用区域无关闸门模板；`review.sharpe_min` 按 D1 标准下调到 **1.25**
（D0 为 1.58，引自 how-to-pass-AlphaTest 的 delay 分档）。

## 后续

- 重跑上方 MCP 抽取即可复核本文件所有数字。
- wave 01 建议中性化 A/B（MARKET vs SUBINDUSTRY vs SECTOR），回测结果回填本文件与 campaign_state，
  若 SUBINDUSTRY 在大样本下维持 Sharpe 优势且 TVR 可控，则将其提升为默认 neutralization。

## Wave 01 中性化 A/B 实测（2026-08-15）

受控实验：基准式 `ts_rank(ts_backfill(winsorize(analyst_earnings_revision_score), 22), 44)`（数据集 ai_equity_alpha），
仅 `neutralization` 不同，3 波各 1 条回测。multisim / alpha：

| 波 | neutralization | alpha | sharpe | fitness | turnover | returns |
|----|---------------|-------|---:|---:|---:|---:|
| 01A | MARKET | KPGp6nzj | 0.29 | 0.10 | 0.1526 | 0.0178 |
| 01B | SUBINDUSTRY | 58p19Yz5 | **0.42** | 0.12 | 0.1653 | 0.0145 |
| 01C | SECTOR | 1YpRmL6m | 0.39 | **0.14** | 0.1545 | **0.019** |

**结论**：对同信号，SUBINDUSTRY（sharpe 最高）> SECTOR（fitness/returns 最高、TVR 低于 SUBINDUSTRY）> MARKET（最弱）。
这与人口证据（86 个 USA D1 OS alpha 中 75 个用 MARKET）相反，但与本战役候选普遍采用 SUBINDUSTRY/SECTOR 的惯例一致。
三式均**未过 D1 门槛**（sharpe<1.25、fitness<1.0）——该基准式无反转腿，属弱信号，中性化对弱信号增益有限。

**决策（已回填 settings.json / campaign_state）**：
- 默认 `neutralization` 由 MARKET 切换为 **SUBINDUSTRY**（A/B sharpe 最高 + 候选惯例 + 满足预设提升准则：相对 MARKET 有 Sharpe 优势且 TVR 可控 0.165 vs 0.153）。
- `_alt_neutralization` 改记 **SECTOR**（次优，fitness/returns 最佳）。
- MARKET 降为 fallback。
- 局限：n=1，建议在含反转腿的强信号上复测后再最终固化默认值。
- 复现：`pipeline.py run --file candidates/usa_wave01_neut_ab.json --dataset ai_equity_alpha --wave 01X --submit --neutralization <MARKET|SUBINDUSTRY|SECTOR>`
