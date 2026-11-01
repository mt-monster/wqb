# GBR D1 analyst83 挖掘经验（电话会议语言数据 · 判死）

范围：2026-10-30。GBR/TOP700/D1 的 `analyst83`（电话会议 / earnings call 语言类，VECTOR）。
本文件记录 6 个结构互异模板 × 5 个机制族的全灭实证，**不外推**为「所有语言类数据无效」——
同源姊妹集 `fundamental45`（2 条探针全灭）与 `other384`（6 模板 + 1 变体全灭）另有独立文件，
三者合计 16 条回测 0 达标。

数据集画像（DB `datasets` 表实读，id=313）：category `ANALYST`、`field_count 383`
（其中 **345 个是 VECTOR**，MCP `get_datafields(data_type="VECTOR", filter_sharpe=False)`
实读 `complete=true / platform_count=345`）、`coverage 0.5312`、`alpha_count 148`、
`value_score 3`、`pyramid_multiplier 1.7`（ANALYST 塔在 GBR D1 的塔倍率）、`delay 1`。

## 判死结论（registry：`GBR-ANALYST83-CALLTRANSCRIPT-DEAD`，2026-10-30）

**6 个结构互异模板、5 个机制族全部未达硬闸**：

| 模板 / 机制族 | Sharpe | 距硬闸 1.58 |
|---|---:|---:|
| 语调水平（`vec_avg` 后的 tone 中枢） | 0.29 | 18.4% |
| 语调一阶变化（`ts_delta` / `ts_av_diff`） | 0.07 | 4.4% |
| 分歧度（`vec_stddev` 跨发言者离散） | −0.18 | 反向 |
| 覆盖度 / 披露密度（`vec_count`） | −0.18 | 反向 |
| 非线性极值（`vec_max` − `vec_min` 跨度） | −0.25 | 反向 |
| 中性语调占比（中性桶信息真空度） | −0.26 | 反向 |

**上限推演（决定性）**：最佳模板 `|S| = 0.29`、最佳 `R/TO = 0.095`
⇒ `F` 天花板 `= S · sqrt(R/TO) = 0.29 · 0.308 = 0.089`，即硬闸 `1.00` 的 **8.9%**。
Sharpe 差 5.4 倍、Fitness 差 11.2 倍，**不属于「骨架选错」而是「字段没有跨截面超额」**。

回测设置：`STATISTICAL` 中性化 + `decay 4` + `truncation 0.08`，universe `TOP700`，delay 1。

## 为什么判死是稳的（不是模板不够多）

1. **6 个模板互异性已过闸**：差异落在「水平 / 一阶差分 / 二阶离散 / 覆盖度 / 极值跨度 /
   分类占比」六个不同信息加工层，不是换窗口或换常数。
2. **最好的模板指向「水平」而不是「变化」** —— 而论坛 `43907846056599`（3 赞）的
   earnings-call tone 权威实证认为**语调变化反转向**、水平信息弱。两处结论一致：
   tone 的可用维度在变化项，而本集的变化项 S 仅 0.07。
3. **VECTOR 折叠没有救回来**：`vec_avg` / `vec_sum` / `vec_stddev` / `vec_range` /
   `vec_count` / `vec_max` / `vec_min` 七种折叠都试过，最好仍是 `vec_avg` 水平。
   论坛 `41420742165527` 提醒过「`vec_avg` 在稀疏场景易被单一高值主导」，但换成
   `vec_stddev` 后直接转负 ⇒ 不是折叠方式问题。
4. **同源三集交叉印证**：`analyst83`（6 模板）+ `fundamental45`（2 探针）+
   `other384`（6 模板 + 1 变体）= 16 条，0 达标，且失败方向一致（水平弱、变化更弱）。

## 后续边界

- **不再在 `analyst83` 上新增模板**。若未来重启，前提必须是「拿到新的经济假设」，
  而不是「再换一个骨架试试」——6 个结构互异模板全灭已经是数据集级结论。
- **不要把 VECTOR 折叠方式当杠杆**：本集七种折叠都试过，折叠不是瓶颈。
- **不要把 345 个字段当 345 个机会**：语言类字段高度共线（同一场电话会议的多种
  tone / 分类器 / 置信度切面），实际独立自由度远小于字段数。判「字段多」时先算
  桶间是否求和为 1（三分类 log-prob 只有 2 个自由度）。
- `analyst83` 的 `pyramid_multiplier 1.7` 是 GBR D1 最高倍率之一，容易诱使「为了倍率
  硬挖」——**倍率只放大已成立的信号，不制造信号**。
- 本集回测**未入 `backtest_results` 表**（`region='GBR' AND dataset='analyst83'` 实读 0 行），
  证据仅存于技能文档与 registry payload ⇒ 若后续要复用，先补 `upsert_backtest_rows`。

## 证据落点

- 判死条目：`registry_empirical` → `GBR-ANALYST83-CALLTRANSCRIPT-DEAD`
- 字段清单：`mcp__wq-brain-http__get_datafields(dataset_id="analyst83", region="GBR",
  universe="TOP700", delay=1, data_type="VECTOR", filter_sharpe=False)`
- 论坛模板：`43907846056599`（earnings-call tone，3 赞）、`41420742165527`（vec_avg 稀疏陷阱）
- 同源姊妹集：`gbr_fundamental45_campain.md`、`gbr_other384_campain.md`
- 外部文献（用于设计模板，非用于推翻判死）：Larcker & Zakolyukina 2012 JAR 50(2)、
  Mayew & Venkatachalam 2012 JF 67(1)、Li 2010 JAR、Loughran-McDonald 2011 JF 66(1)
