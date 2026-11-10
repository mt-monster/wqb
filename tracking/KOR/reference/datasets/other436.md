# other436 · KOR / TOP600 / D1 字段画像

> 类型 **VECTOR** · **3 个字段** · 覆盖率均 0.57 · 采集 get_datafields(filter_sharpe=false) 2026-11-08，complete=true
> 金字塔 category = **other**（未点亮塔 1/3）· 数据集名 Dividend model
> ⚠ 派发历史审计：字段前缀零命中 ⇒ 本战役 D2 波首次实测

## 0. 全字段清单（3/3，αC 降序）

| # | 字段 | αC | users | cov | desc |
|---|---|---|---|---|---|
| 1 | `oth436_divyld` | 7 | 7 | .57 | 股息率（可能年化，trailing/forward 未明；**only available for updates**） |
| 2 | `oth436_mktcap` | 6 | 4 | .57 | 市值（USD 或本币未明） |
| 3 | `oth436_disc` | **4** | 4 | .57 | **模型输出：公司削减/暂停/终止股息的预测概率 [0,1]** |

**读数**：aC 4–7 全战役最冷集之一；**全 VECTOR** ⇒ 任何标量算子前必须 vec_* 聚合（铁律 L；behavioral_signals 整批 ERROR 先例）。
"only available for updates" ⇒ 事件更新型，非事件日无值 ⇒ ts_backfill 必需 + 关注零膨胀。cov .57 低于 0.60 政策线，但目标明示覆盖率可动态调整 ⇒ 放行实测，CW/longCount 裁决。

## 1. 名 vs description 差异
| 名 | 实际 | 按名分类的错误 |
|---|---|---|
| `disc` | **dividend cut 概率**，不是 discount/discrete | 会误读为折价因子 |
| `divyld` | 仅更新日有值 | 会当日频连续字段裸用 ⇒ NaN 污染 |

## 2. 五问
1 存量概率评分（事件更新）；2 排序 ⇒ group_rank(sector)；3 强度（削减风险）；4 极冷 aC4；5 **事件稀疏** ⇒ vec_avg → ts_backfill(10)，门控备试。

## 3. 预处理决策
- **顺序铁律**：vec_avg 先聚合，ts_backfill 后回填（直接 ts_backfill(VECTOR) 报 event 错）
- mktcap 只作规模轴；divyld 作门控/对照

## 4. 机制（A-2）
- **谁被定价**：追逐股息的收益型散户对削减风险定价不足（dividend clientele + 粘性股利预期）；
- **为什么错**：削减公告负反应显著（信息含量假说；Jakarta cut/omission 实证负显著），公告前概率信号被忽视，公告后漂移；
- **修复期**：数周–数季（22/66/252）；
- **方向**：高 disc ⇒ 后续低收益 ⇒ 做空高 disc（subtract(0.5, group_rank)），正向臂对照（铁律 B）。
- **Boundary**：KOR 削减样本稀少可能无截面区分；VECTOR 更新稀疏 ⇒ longCount 实测裁决。

## 5. D2 波模板（10 结构互异，RAM/d4/trunc0.08）
空高cut/多高cut对照 · Δ22 · Δ66 · mean66 · zscore252 · yield正/反 · 规模残差 · yield门控
multisim `oycrP8Rf5fz9sLt6s672Le`（2026-11-08 派发，在飞）

## 6. 实测记录（D2 探针 2026-11-08，2/2 COMPLETE；整批10条曾瞬时 ERROR，2条探针跑通）

| 臂 | alpha | S | F | 2Y | TO | raF |
|---|---|---:|---:|---:|---:|---:|
| 做多高 cut 概率 | O0AXeZ5d | **0.53** | 0.27 | 1.29 | 0.081 | 3 |
| 做空高 cut 概率 | zq3namJO | −0.70 | −0.41 | −1.66 | 0.081 | 5 |

**判定：弱死**（|S| 天花板 0.70，缺口 0.88）。**方向与信号假说相反**：高削减概率股后续反而正收益（超跌反弹/已定价），削减概率非 KOR 可交易 alpha（同 acquisition_model 型，证实 roadmap 预判）。封盘。
