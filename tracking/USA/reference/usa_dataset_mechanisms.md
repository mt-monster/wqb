# USA 数据集机制标注（S0 排序键 · P0-4）

> **机器读取**：本文件首个合法的 ` ```json ` 代码块由 `tools/campaign_intel.py s0-select` 读取
> （路径约定 `tracking/<REGION>/reference/<region_lower>_dataset_mechanisms.md`，实现见
> `_load_region_mechanisms`）。排序键第三层 = 机制层：
>
> | `classic_anomaly` | tier | 排序含义 |
> |---|---|---|
> | `true` | 0 | 有经济机制 + 属经典异象 ⇒ **优先** |
> | 未登记 / 已过期 | 1 | 未标注 ⇒ 保持原 `total_score` 次序 |
> | `false` | 2 | 明示「机制 ≠ 经典异象」⇒ 沉到未标注之后（须在 `evidence` 写明理由） |
>
> **判据来源**：`reports/usa_mining_history_review_20261023.md` §5 判据 A ——
> 「RA 全过率」衡量信号强度，交付卡口是「机制在生产池里拥不拥挤」，两者在 USA **反向**；
> 选集要问的是**机制是否经典异象**，不是数据集是否冷门。
>
> **纪律**：
> - 只登记**当期有证据**的集；`as_of` 早于 `review_after_days`（本文件 180 天）自动降为未标注（tier 1）。
> - 「经典异象」= 有可引用的经济机制（论文 / 教科书），**不是**「数据集冷门」。
> - 经典异象也可能拥挤（`risk60` prod 0.9917）⇒ 机制层只决定**先试谁**，
>   开波前仍必须走 `campaign_intel.py prod-probe`（P0-1）确认族未饱和。
> - 判死的集不用登记（先被 `usa_dead_datasets.md` 剔除）。

- **region**: USA ｜ **as_of**: 2026-10-23 ｜ **review_after_days**: 180

```json
{
  "region": "USA",
  "as_of": "2026-10-23",
  "review_after_days": 180,
  "source": "reports/usa_mining_history_review_20261023.md §5 / §7 / §11",
  "datasets": [
    {
      "dataset": "insider_agg_matrix",
      "mechanism": "内部人交易金额量级（insider trading / 内部人买入预示超额收益）",
      "classic_anomaly": true,
      "evidence": "Lakonishok & Lee (2001) + Cohen/Malloy/Pomorski (2012)；复盘报告 §7.3（USA 零回测、INSIDERS 塔未点亮）",
      "as_of": "2026-10-23"
    },
    {
      "dataset": "insider_matrix",
      "mechanism": "内部人交易（有符号 / 计数 / 金额）",
      "classic_anomaly": true,
      "evidence": "同上；复盘报告 §5/§11（族内 3/4 颗 prod<0.7，冠军 zqrGqVXo prod 0.8092 仍有相邻余量）",
      "as_of": "2026-10-23"
    },
    {
      "dataset": "earnings_sent_matrix",
      "mechanism": "PEAD 盈余公告后漂移（业绩超预期 → 价格延续）",
      "classic_anomaly": true,
      "evidence": "Ball & Brown (1968) / Bernard & Thomas (1989)；复盘报告 §11 优先级 3（earnings 塔差 2 颗点亮，×1.2）",
      "as_of": "2026-10-23"
    },
    {
      "dataset": "ai_equity_alpha",
      "mechanism": "平行模型对同一收益目标的预测分歧（非经典异象；信息源不同才成立）",
      "classic_anomaly": false,
      "evidence": "复盘报告 §7.1：prod 0.64-0.69 是唯一真交付路径，但 MODEL 塔已点亮 ⇒ 默认被塔位剔除；登记为 tier 2 防止 --include-lit 时误排到前排",
      "as_of": "2026-10-23"
    }
  ]
}
```

## 备注

- `insider_agg_matrix` 的 DB 行 `pyramid_multiplier=1.5` 是 **D0 值**，USA/D1/insiders 真值是 **1.1**
  ⇒ 塔位一律以平台 `recommend_datasets` 的 `pyramid_summary` 为准（S0 产物已带快照，P1-4）。
- 同一机制换数据集不等于换机制：`institutions18`（机构持仓）prod 0.9636 已判死
  ⇒ `fund_holdings_panel` 等同类集开波前必须先做 prod 探针，登记时会写进 `evidence`。
