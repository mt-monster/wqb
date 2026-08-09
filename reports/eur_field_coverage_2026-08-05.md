# EUR 数据集字段覆盖率实时核查报告

**生成时间**：2026-08-05
**工具**：`tools/eur_field_coverage.py`（新建，双通道）
**查询**：EQUITY / EUR / delay=1 / TOP1200
**数据来源**：WQ BRAIN 平台实时 API（非本地数据包）

---

## 一、核心结论

**此前"EUR 死路 / 数据包过期"的判断是错误的，需要撤回。**

EUR 战役失败的真实根因不是平台无数据，而是**数据集选择错误**：32 次回测全部消耗在 4 个低覆盖或高拥挤的劣质数据集上，而平台同期提供 **178 个数据集 / 38609 个字段**，其中 19 个满足"高覆盖 + 未拥挤"条件的数据集**从未被触碰**，7 个 alphaCount 为 0（零竞争）。

---

## 二、平台实况

| 指标 | 数值 |
|---|---|
| 可用数据集 | 178 |
| 可用字段总数 | 38,609 |
| coverage 均值 / 中位数 | 0.6616 / 0.6657 |
| coverage ≥ 0.90 | 35 个 |
| coverage 0.70–0.90 | 43 个 |
| coverage < 0.70 | 100 个 |

类别分布：model 49、other 37、pv 20、news 20、analyst 16、fundamental 14，其余为 sentiment/risk/insiders/earnings/institutions/macro/socialmedia/imbalance。

---

## 三、原战役用过的 4 个数据集——事后体检

| 数据集 | coverage | 字段数 | 用户数 | alpha 数 | 金字塔倍率 | 判定 |
|---|---|---|---|---|---|---|
| model30 | 0.713 | 77 | 174 | **4202** | 1.3 | 极度拥挤，prod_corr 几乎必然超标 |
| pv20 | 0.6915 | 1475 | 28 | 65 | **1.1** | 覆盖率偏低 + 最低倍率 |
| news21 | **0.5266** | 47 | 8 | 9 | 1.3 | 近半标的无数据，高 tvr 是必然结果 |
| insiders12 | **0.2008** | 8 | 11 | 15 | 1.2 | 覆盖率 20%，结构性不可用 |

四个样本无一满足 coverage ≥ 0.85。sharpe 天花板 0.72 是这个选择的直接后果，而非区域特性。

### 关于"平台 0 字段"的误判

原结论称 `fundamental86 / risk59 / model216 / fundamental94` 在平台上 0 字段，归因于数据包过期。实测结果：

- 这四个数据集在 **EUR 区域根本不提供**（不是 0 字段，是不存在）；
- 但它们在 **KOR 区域全部可用**，例如 `fundamental94` 有 215 字段、coverage 0.8558。

这是**跨区域误推荐**，与数据包新鲜度无关。等待数据包更新不会改变任何事情。

---

## 四、EUR 未开发机会排行（coverage ≥ 0.85 / alphaCount ≤ 50 / 字段 ≥ 10）

| 数据集 | coverage | 字段 | 用户 | alpha | valueScore | 倍率 | 类别 |
|---|---|---|---|---|---|---|---|
| **ml_factor_proj** | **1.0** | 333 | 0 | **0** | 5.0 | **1.5** | other |
| **news_sentiment_nlp** | 0.9134 | 23 | 0 | **0** | **6.0** | **1.5** | other |
| dl_riskfree_returns | 0.9429 | 133 | 6 | 14 | 4.0 | **1.5** | other |
| ai_factor_transfer | 1.0 | 20 | 0 | **0** | 4.0 | 1.3 | model |
| global_seasonal_model | 0.9886 | 449 | 0 | **0** | 5.0 | 1.3 | model |
| analyst_earnings_ibes | 0.9976 | 42 | 1 | 1 | 5.0 | 1.3 | model |
| price_signal_dl | 0.9729 | 28 | 1 | 2 | 5.0 | 1.3 | model |
| ai_equity_alpha | 0.8601 | 582 | 2 | 2 | 5.0 | 1.3 | model |
| model354 | 1.0 | 236 | 5 | 7 | 4.0 | 1.3 | model |
| continuation_score | 0.9924 | 560 | 0 | **0** | 5.0 | 1.1 | pv |
| pattern_scores | 0.9924 | 504 | 0 | **0** | 5.0 | 1.1 | pv |
| intraday_pv_feats | 0.9548 | 585 | 1 | 1 | 4.0 | 1.1 | pv |

（完整 19 条见 `tracking/mining/field_coverage_EUR_d1_TOP1200.json`）

### 字段级下钻验证：ml_factor_proj

333 个字段全部为 `MATRIX` 类型，**coverage 全为 1.0**（mean = median = min = max = 1.0000），全部 userCount=0 / alphaCount=0。字段命名为标准因子变化率语义（`change_1y_eps_growth`、`change_12m_alpha`、`change_20d_volume_to_price_volatility` 等），可直接套用现有 PPA 模板。

这是一个满覆盖、零竞争、1.5 倍金字塔的数据集，优先级应列为最高。

---

## 五、跨区域附带发现：KOR 优先级高于 EUR

同步拉取了 KOR/TOP600/D1（192 个数据集，coverage 均值 0.7046，高于 EUR 的 0.6616）。同一批优质数据集在两区的收益参数差异显著：

| 数据集 | EUR 倍率 / valueScore | KOR 倍率 / valueScore |
|---|---|---|
| ml_factor_proj | 1.5 / 5.0 | **1.7 / 6.0** |
| ai_factor_transfer | 1.3 / 4.0 | **1.7 / 6.0** |
| analyst_earnings_ibes | 1.3 / 5.0 | **1.7 / 6.0** |
| price_signal_dl | 1.3 / 5.0 | **1.7 / 6.0** |

KOR 的 `ml_factor_proj` 仍只有 10 个 alpha，同样未饱和。若以金字塔收益为目标函数，**KOR 应排在 EUR 之前**。

---

## 六、工具说明：`tools/eur_field_coverage.py`

零第三方依赖（仅标准库），双通道设计：

- **MCP 通道（默认）**：复用常驻 `world-quant-brain-mcp` 服务（`127.0.0.1:8876`）已建立的稳定会话，规避沙箱到 `api.worldquantbrain.com` 的 TLS 抖动。
- **直连通道（`--mode direct`）**：用 `.env` 凭据自行 Basic Auth，对 429/5xx 与链路异常做指数退避重试（实测退避后成功）。

```bash
# 数据集级覆盖率
python tools/eur_field_coverage.py --region EUR --delay 1 --universe TOP1200

# 字段级下钻
python tools/eur_field_coverage.py --region EUR --universe TOP1200 --dataset-fields ml_factor_proj

# 换区域 / 走直连
python tools/eur_field_coverage.py --region KOR --universe TOP600 --mode direct
```

内置各区域合法 universe 白名单（非法档位在本地即报错，不再浪费一次 500）。EUR 合法档位：`TOP2500 / TOP1200 / TOP800 / TOP400 / TOPCS1600 / ILLIQUID_MINVOL1M`。

### 踩坑记录（API 实测约束）

1. `GET /data-fields` 必须 `instrumentType + region + delay + universe` 四者齐全；单独给 `dataset.id` 而不给 `universe` → 400 Invalid query。
2. `universe` 传该区域非法档位 → 500（不是 400）。
3. `get_datasets` 直接返回 `coverage / fieldCount / userCount / alphaCount / valueScore / pyramidMultiplier`，比逐字段聚合快约两个数量级，数据集级体检应优先走这条。
4. 直连 API 返回的 `category` 是 dict，MCP 返回的是 str，需归一化。

---

## 七、行动建议

1. **撤回** `tracking/mining/eur_track_conclusion.json` 的死路结论，以 `eur_track_conclusion_revised.json` 为准。
2. **建立开战役前置门槛**：coverage ≥ 0.85、alphaCount ≤ 50、fieldCount ≥ 10 三条硬性检查，不达标的数据集不消耗回测配额。这条规则若在 EUR 战役前执行，可直接避免那 32 次无效回测。
3. **重开 EUR 战役**，起点 `ml_factor_proj`（333 字段满覆盖零竞争）→ `news_sentiment_nlp`（valueScore 6.0）→ `global_seasonal_model`。
4. **优先考虑 KOR**：相同数据集倍率 1.7 vs EUR 1.5，且 KOR 已有 12 个 COMPLETE 未取回的仿真结果待处理。
