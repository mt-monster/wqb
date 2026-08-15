# WebDataScope 挖掘指南(数据包 V0.10.9)

> 基于 `WebData_20260219_V0.10.9.zip` + `tools/webdata_quality.py` + WebDataScope 扩展 的完整用法盘点。
> 数据窗口:2022-02 → 2026-02 社区提交统计(16 个 region_delay 组合),160+ 数据集组合、39910 字段(USA_1)。

## 一、体系构成

| 部分 | 内容 | 作用 |
|---|---|---|
| 数据包 | `data/oth/info_data.bin`(16 区域社区统计)、`data/oth/osis_data.bin`(OS-only 快照)、`data/*.bin`(162 个字段级体检)、`dataSetList.json` | 社区先验 + 字段体检 |
| 分析工具 | `tools/webdata_quality.py`(11 个参数) | 本地离线分析,秒级出结果,不消耗平台额度 |
| 浏览器扩展 | `extensions/webdatascope`(WorldQuant Scope 1.5.0) | 平台侧实时展示字段体检/分布/ProdMemo |

数据格式:msgpack + zlib 压缩,每字段含 10 年逐年序列(CoverageRatio / IndicativePositiveRatio / IndicativeNegativeRatio / IndicativePositiveNegativeRatio / IntegerStatus / skenewss / kurtosis / frequency / yearly_distribution / LongCount / ShortCount)。

## 二、用法清单(按价值排序)

### A. 数据预处理 → 表达式自动生成(最大增量价值,已实测)
`--export-expr` 把字段体检直接转成可提交的 FASTEXPR,`--neut` 指定中性化:

```bash
python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip \
  --region USA --delay 1 --fields analyst11 \
  --export-expr tracking/expr_analyst11.json --neut subindustry
```

- 196 个字段全部自动产出候选表达式 + 理由 + 优先级 + metadata
- **规则引擎**(`field_inspect_to_expr`):
  - 覆盖率 <0.4 → 必包 `ts_backfill(F, 窗口, 0)`(否则 CONCENTRATED_WEIGHT)
  - |偏度|>2 → `signed_power(x, 0.5)`;峰度>8 → `winsorize(std=3)`
  - 单边恒正/负 → `rank(ts_delta(F, 窗口))` 对称化
  - 离散整数 → `group_rank(bucket(F,10))`
  - 稀疏事件(zero_inflated/point_mass)→ `trade_when(F!=0, rank(F), -1)` 门控
  - 通用兜底 → `rank(F, neut)`
- metadata 直接给参数:min_window / recommended_decay / recommended_truncation
- 配套 `check_expr_against_inspect` 可对任意已有表达式做**提交前硬性校验**(缺 ts_backfill / 缺 rank / 缺 trade_when 都会报违规),与 skill `alpha-expression-verifier` 联动。

### B. 时间窗口选择(数据驱动,非拍脑袋)
- **频率 → 窗口下限**(`_min_window`):daily≥10d、weekly≥5d、monthly≥21d、quarterly≥63d。`ts_delta`/`ts_mean` 窗口低于该值 = 采样噪声。
- **覆盖厂字形检测**:早年 CoverageRatio 低 → 近年高(>1.3×),提示数据商中途扩容,回测早年失真、勿用早年做历史验证。
- 字段级逐年序列(year 数组)可用于检查字段"近几年才有效"的时效性问题。

### C. 低竞争区域挖掘(已实测,机会最大)
info_data.bin 含 **16 个 region_delay**,均值差异巨大:

| region_delay | 均值 sharpe | 窗口 | 备注 |
|---|---|---|---|
| **IND_1** | **0.668** | 2025-11 起(新) | model243 1.085 / model77 1.024 / model110 0.932,提交量大(14 万) |
| **CHN_0** | 0.784 | 2022-11 起 | delay0 均值最高,提交少(4752) |
| **EUR_0** | 0.582 | 2022-12 起 | delay0 机会 |
| ASI_1 / EUR_1 / GLB_1 | 0.44–0.48 | 主流 | 竞争中等 |
| USA_1 | 0.358 | 2022-02 起 | 最卷(90 万提交) |
| TWN/HKG/JPN/KOR | 0.31–0.39 | 2023 起 | 覆盖极低,ProdCorr 风险低 |

用法:低均值区域 ≠ 没机会;恰恰是**均值高 + 提交少**的区域(CHN_0/IND_1)说明竞争小、社区验证样本还在积累。注意 IND_1 窗口仅 3.5 个月,警惕样本窗口偏短。

### D. 跨区域机会识别(已实测)
`--cross-region`:同数据集在多个 region 的 sharpe 差,|diff|>0.3 即 region-specific 潜力:

```bash
python tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip \
  --region USA --delay 1 --cross-region --top 10
```

实测发现:pv30(USA 0.339 vs CHN 1.702)、fundamental86(EUR 1.09 vs USA 0.014)、model144(IND 0.676 vs USA -0.469)。**同一字段逻辑换区域可能从平庸变优秀**——这是 alpha 移植的主要来源。注意 t_count 过低(<20)的对比不可信。

### E. 字段级先验与反用(已实测)
`--field-top N` 输出社区提交最多的字段(质量先验最高):
- 高 alphaCount 字段(mdl110_score 11 万次):社区反复验证可提交,组合/中性化先验最丰富
- **反用**:低 alphaCount 但 sharpe 高的字段(如 star_val_industry_rank sharpe 0.748) = 差异化机会;极少有人用的字段/数据集 = 低质量,但**新字段(接近零提交)可能是尚未被发现的信号**——用字段体检验证质量后值得试挖

### F. 中性化选择(逐区域差异巨大,已实测)
- USA_1 最优 **STATISTICAL**(0.461);GLB_1 最优 **REVERSION_AND_MOMENTUM**(0.583);KOR 常 SECTOR 优
- 每数据集/每字段都有独立的最优中性化(neut.dataset / neut.datafield),`best_neuts` 输出前三
- **切勿照搬其他区域的顺序**——工具明确警告
- 甜点区 + 中性化可靠度(count≥20 且 osis_count≥20)双重过滤,避免小样本误判

### G. OS 退化检测(鲁棒性,已实测)
IS+OS sharpe vs OS-only sharpe,差 >0.15 标记退化(如 GLB 的 analyst83 -0.453、fundamental45 -0.339):
- 退化的数据集=IS 好 OS 崩,优先排除
- 稳健(差≤0.15)= 过拟合风险低,放心挖
- 注意选择性偏差:OS 高于 IS+OS 是正常现象(通过筛选才进 OS),不是反向信号

### H. 综合挖掘推荐(--recommend,已实测)
`mining_recommendations` 打分 = sharpe × 甜点区(100–3000 未饱和 ×1.3 / >30000 饱和 ×0.5)× OS 退化惩罚(0.5)× 中性化可靠度(+10%):
实测 GLB 推荐:model239(1.091)、sentiment26(1.057)、news66(0.916)、news54(0.901)……**按表从上到下挖即可**,已自动排除低质量与退化数据集。

### I. 类别级机会
isos.category:earnings/news OS sharpe 0.586/0.575(高于整体),macro/sentiment/socialmedia 等类别提交少但 sharpe 不差 → 冷门类别差异化。

### J. 字段组合建议(field_combine_hints)
基于分布形状互补自动提示:
- 稀疏事件字段(点质量/零膨胀)× 连续字段 → `trade_when(事件, 信号, -1)` 事件门控
- 截尾 × 稀疏 → 互补组合,结构性去相关
- 双连续字段 → `rank(A) - rank(B)` 双信号去相关
- concentrated 字段慎作主信号,作辅助/门控

### K. 平台侧(扩展)联动
WebDataScope 扩展在平台上直接展示字段体检/分布(dataAna/dataFlag/distribution.js),挖字段时实时看 CoverageRatio 与分布,与本地工具互补;ProdMemo 追踪已提交 alpha 的生产表现,形成"挖-测-提-追"闭环。

## 三、局限与坑

1. **IND/TWN/HKG/AMR 无字段级体检 bin**(仅社区统计),表达式生成/字段体检只对 USA/EUR/CHN/GLB/ASI/JPN/KOR 覆盖的组合可用。
2. **GLB 体检覆盖仅 5 个数据集**(GLB_TOP3000),GLB 想挖新字段需回平台 `get_datafields` 复核 coverage。
3. **Windows 编码坑**:`--export-expr`/`--json-out` 写出的 JSON 是 **GBK 编码**(open 未指定 encoding),Python 消费需 `encoding="gbk"`;终端输出中文在 UTF-8 终端会乱码(建议 `PYTHONIOENCODING=utf-8` 仅影响 stdout 打印,不影响文件)。
4. **样本量陷阱**:cross-region 里 t_count<20 的对比、field-top 里 count<50 的字段,可信度低,需在平台复核。
5. **窗口时效**:数据窗口截至 2026-02,IND_1 仅 3.5 个月;新区域数据更新后应重新生成快照。
6. `--fields` 与 `--export-expr` 依赖 dataSetList.json 的精确匹配,数据集名不存在于该 region 时输出 0 字段(先确认 `--region` 匹配)。

## 四、推荐挖掘工作流

```
1. --recommend 拿综合推荐表(GLB/USA/IND 各跑一次)
2. 对推荐数据集跑 --fields X(看字段体检/组合建议)
3. --export-expr 自动生成候选表达式,或手写后用 check_expr_against_inspect 校验
4. --cross-region 找可移植的 region-specific 机会
5. 用 MCP validate_expressions 预检字段存在性 → create_multi_simulation 批量回测
6. 提交后扩展 ProdMemo 追踪 OS 表现,定期用 osis_data.bin 复核是否退化
```
