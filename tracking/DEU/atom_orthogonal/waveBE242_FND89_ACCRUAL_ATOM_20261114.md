# BE242 fnd89 应计 ATOM 首波（2026-11-14）

> 用户指令：锁定 Fundamental，挖掘 ATOM。FUNDAMENTAL 12 集盘点后选 **fundamental89**（Accrual based Earnings Model，407 字段全 MATRIX）：
> 仅 20 臂历史（且多为跨集搭档腿，非 ATOM 内探）——六维判死闸下**远未到判死线**；
> 杠杆B 实证（反转×应计 multiply 2Y 1.47→1.77）证明应计轴携带正交 2Y 信息；
> Sloan 应计异象是跨市场稳健机制。fnd45 QA 面 78 臂已收敛（S≤1.04）不再加注。

## 一、设计（10 臂，单 multisim，并发 1/2）

**机制假设**：应计异象 = 高应计→低未来收益（负号）；现金流分量（Sloan-Jones）为正号。
**ATOM 合规**：全部字段 `fnd89_*` 单集；group 字段（sector/subindustry）豁免；
无 add()（连 SAME_DATASET_LEG_ADD warning 都不触发）；乘法/bucket 形态无权重自由度。

| # | 臂 | 结构 | 机制 |
|---|---|---|---|
| 1 | `group_rank(-ts_backfill(fnd89_asset_41_11, 66), sector)` | 单腿 | 流动资产应计/TA（Sloan 主口径，u8） |
| 2 | `group_rank(-ts_backfill(fnd89_asset_41_11, 66), subindustry)` | 单腿换轴 | 同 1，分组轴 D4 |
| 3 | `group_rank(-ts_backfill(fnd89_asset_41_31, 66), sector)` | 单腿换分母 | 应计/sales |
| 4 | `group_rank(-ts_backfill(fnd89_best11_d1_accum_4q, 66), sector)` | 单腿 | 4Q 累积应计比 |
| 5 | `group_rank(-ts_backfill(fnd89_best11_d1_current_t, 66), sector)` | 单腿 | 历史标准化 t 值（异常应计） |
| 6 | `group_rank(ts_backfill(fnd89_csjones_all_major_12, 66), sector)` | 单腿反号 | 现金流分量（Sloan 分解正侧） |
| 7 | `group_rank(-ts_backfill(fnd89_asset_51_11, 66), sector)` | 单腿 | 非流动资产应计 |
| 8 | `group_rank(-ts_backfill(fnd89_asset_61_11, 66), sector)` | 单腿 | 金融资产应计 |
| 9 | `group_rank(multiply(-ts_backfill(fnd89_asset_41_11, 66), ts_backfill(fnd89_best11_d1_current_t, 66)), sector)` | 乘法交互 | 应计水平×异常度（杠杆B 同集版） |
| 10 | `group_neutralize(group_rank(-ts_backfill(fnd89_asset_41_11, 66), sector), bucket(rank(ts_mean(ts_backfill(fnd89_asset_41_11, 66), 252)), range="0,1,0.05"))` | bucket 条件化 | 战役实证 eps_y1 形态移植 |

**设置**：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON/maxTrade OFF/FASTEXPR。

## 二、预检

- preflight_expressions(dataset_id=fundamental89)：valid=true，unknown_fields=[]（fnd89_asset_51_11 复查网络抖动，已在字段拉取中确认存在 u5）。

## 三、判读基准

- 与 fnd45 基线（S 0.96/2Y 1.73/sub 0.72）逐项对照；
- **核心 prod 探针纪律**：最佳 1-2 臂收割后立即 check_correlation(production, refresh=True)——prod 雷在核心不在搭档（FINAL_DELIVERY §三）；
- 符号指纹：衰减对称=机制在/符号错；单向=事件型。
- TO 预期低（季度更新 + ts_backfill66）；2Y 是 DEU 天然达标轴。

## 四、BE242 收割归因（multisim `45vd2A2ac4CYbOo131Rqdd5B`，10/10 COMPLETE）

按派发臂序（纪律：禁止按 alpha id 猜）：

| # | alpha | 臂 | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | O0WeXJ7J | CA应计/TA sector | 0.59 | 0.31 | 0.68 | 0.25 | 4.1% |
| 2 | KPgeMm7p | CA应计/TA subindustry | 0.58 | 0.28 | 0.69 | 0.17 | 3.8% |
| 3 | pwa0evPg | CA应计/sales | **0.72** | 0.42 | 0.39 | 0.32 | 4.1% |
| 4 | qM7bJEWP | 4Q累积应计 | 0.71 | 0.38 | 0.22 | 0.39 | 3.4% |
| 5 | oma20o6l | 历史t值 | 0.66 | 0.34 | 0.30 | 0.24 | 3.9% |
| 6 | LLKeY599 | 现金流分量(+) | 0.34 | 0.13 | **1.11** | 0.19 | 5.4% |
| 7 | 1YWvAjxW | 非流动应计 | 0.67 | 0.37 | 1.03 | 0.42 | 3.9% |
| 8 | VkNnbd65 | 金融资产应计 | 0.62 | 0.31 | 0.17 | 0.09 | 4.2% |
| 9 | P05emMZL | 乘法交互 | 0.40 | 0.17 | 0.27 | 0.11 | 4.1% |
| 10 | e7aAZ6bl | bucket条件化 | 0.23 | 0.08 | 0.05 | -0.02 | 9.9% |

**归因**：① 应计水平机制在 DEU TOP500 真实但弱（5 族单腿 0.59-0.72，无一破 1.0）；
② **2Y 是死结**（应计侧 0.05-0.69；ATOM 只看 2Y≥1.58，水平再修也无达标路径）；
③ 复合形态稀释铁律再现（乘法 0.40 / bucket 0.23 均低于对应单腿）；
④ 唯一绿芽 = 现金流分量 2Y 1.11（但 S 0.34，差距 +1.24，战役经验结构增益 +0.1-0.2 封顶 ⇒ 救援期望值过低，不加注）。
**fnd89 状态：PROVISIONAL（水平弱 + 2Y 死 + 现金流种子登记）**，不足六维判死线（D1 还差结构互异模板），但停止加注。

## 五、同批并行波（FUNDAMENTAL 继续锁定）

### BE244 fnd90 GAME 探针（multisim `dUqXNcGw5hWcIw13b1DKZjY`，10 臂）

fnd90=GAME（Governance/Accounting/Management/Equality，66 字段全 MATRIX，**零本地回测**）。
机制：财务质量复合分（Piotroski/O-score/Montier）+ 现金流质量（ICFROE/覆盖/波动）+ 资产效率。
臂序→机制：1 pscore+ / 2 现金流覆盖+ / 3 icfroe_5y+ / 4 ohlson− / 5 存货变化− / 6 GP/TA+
（Novy-Marx）/ 7 其他资产增长− / 8 现金流波动− / 9 递延收入变化+（订单池逻辑，符号待指纹校验）/
10 capex/sales−（过度投资）。

### BE245 fnd93 税探针 + digital_ad_spend 存在性（multisim `1ov9t21co4pv8RUBtC87EKa`，10 臂）

fnd93=Earnings Tax（46 字段 MATRIX）：税应计（账面税−现金税，Hanlon 盈余质量）+ 递延税 + 资产增长。
臂 1-8 fnd93：1 tax_accruals_51−（u6 最热）/ 2 _13− / 3 应计z− / 4 递延税费用比− / 5 费用z− /
6 资产增长−（u8/a10 Cooper）/ 7 YoY资产变化− / 8 递延税负债z−。
臂 9-10 digital_ad_spend 存在性探针（VECTOR 已 vec_avg 包裹，SUBINDUSTRY 下 longCount>0 即有数据；
⚠ 偏离 NONE 直读口径，只作存在性判断不作覆盖度读数）：9 advertising_spend_usd / 10 estimated_ad_impressions。

### 并发纪律

BE244+BE245 并发=2（用户约束），BE242 已终态不占额度。

## 六、BE244/BE245 收割归因（2026-11-14，20/20 COMPLETE）

### BE244 fnd90 GAME（multisim `dUqXNcGw5hWcIw13b1DKZjY`）——10 臂全灭

| # | alpha | 机制 | S | 2Y |
|---|---|---|---:|---:|
| 1 | 88NAWojv | Piotroski+ | 0.02 | -0.49 |
| 2 | XgaqZrb0 | 现金流覆盖+ | 0.08 | -0.84 |
| 3 | 78YOPA6O | ICFROE-5y+ | 0.09 | -0.37 |
| 4 | 9qlo5vWr | O-score− | -0.07 | -0.70 |
| 5 | P05eLWgx | 存货变化− | 0.28 | -0.48 |
| 6 | XgaqZrJ0 | GP/TA+ | -0.13 | -0.39 |
| 7 | 78YOPAoO | 其他资产增长− | -0.17 | 0.02 |
| 8 | O0WedYJp | 现金流波动− | 0.01 | -0.20 |
| 9 | RReXx3Ae | 递延收入变化+ | -0.07 | -0.88 |
| 10 | ZYaZV5m1 | capex/sales− | -0.42 | -0.95 |

**归因**：质量/操纵复合分族在 DEU TOP500 **零信号**（S ∈ [-0.42, +0.28]，2Y 全负或近零）——
成熟公开评分在大盘已被定价；符号翻转亦无出路（|S| ≤ 0.42）。
**fnd90：5 机制族 × 10 臂全灭，质量评分面判弱入档。**

### BE245 fnd93 税 + 广告存在性（multisim `1ov9t21co4pv8RUBtC87EKa`）

| # | alpha | 机制 | S | 2Y |
|---|---|---|---:|---:|
| 1 | e7aAMokO | tax_accruals_51− | 0.29 | -0.20 |
| 2 | akaJmqjw | tax_accruals_13− | 0.26 | 0.18 |
| 3 | E5Q3nXO9 | 应计z− | 0.26 | 0.33 |
| 4 | 9qlo5LY1 | 递延税费用比− | 0.22 | 0.13 |
| 5 | gJavNE6K | 费用z− | 0.47 | 0.18 |
| 6 | Jj8laZqO | 资产增长−（Cooper） | **0.53** | **0.95** |
| 7 | j2aLkbvo | YoY资产变化− | -0.19 | -0.22 |
| 8 | vRA0738Q | 递延税负债z− | 0.25 | -0.01 |
| 9 | 1YWv3Q9Q | 广告支出存在性探针 | -0.11 | — |
| 10 | LLKeoAj6 | 广告曝光存在性探针 | 0.33 | — |

**归因**：税应计族弱水平（0.22-0.29，与 fnd89 应计同形）；唯一种子 = **资产增长 0.53/2Y 0.95**
（今日 30 臂最佳 2Y，但 S 差 +1.05，水平路径无法闭合）；递延税/负债 z 全弱。
**fnd93：弱水平入档，资产增长种子登记。**

**digital_ad_spend 数据层排除**：探针臂 9 读数 longCount 25 / shortCount 25（仅 ~50/500 只覆盖），
CONCENTRATED_WEIGHT 0.5 vs limit 0.1 已挂 ⇒ 宽度塌缩，TOP500 内结构性不可用（数据层排除，非信号死）。

## 七、FUNDAMENTAL 锁定日终局（30 臂，2026-11-14）

| 数据集 | 今日臂 | 最好读数 | 处置 |
|---|---:|---|---|
| fnd89 应计 | 10 | 0.72（应计/sales）；2Y 全死 | PROVISIONAL，停止加注 |
| fnd90 GAME | 10 | 0.28；质量分全零 | 判弱入档 |
| fnd93 税 | 8 | 0.53/2Y 0.95（资产增长种子） | 弱水平入档，种子登记 |
| digital_ad_spend | 2 | lc 25/sc 25 + CW 挂 | **数据层排除** |
| fnd45 QA（前轮） | 78 | 0.96/2Y 1.73-1.88/prod 0.45 | 已穷尽，塔位储备 |

**结论**：FUNDAMENTAL 12 集中，DEU TOP500 内除 fnd45 QA 面（S 天花板 ~1.0）外，
应计/质量分/税三大族全部弱水平（≤0.72）且 2Y 不达标——**ATOM 的唯一放宽轴（2Y）恰是本类别的死轴**。
FUNDAMENTAL 塔 1/3 点亮缺口在本类别内无可见闭合路径。剩余未探面（AFL 行业 VECTOR、fnd1 履历、
fnd72 千字段、fnd22 单字段）全部带结构性负先验（宽度塌缩/非数值/单字段），期望值不足以再烧波次。

## 八、论坛取证（2026-11-14，4 帖 ok）

| 帖 | 关键证据 |
|---|---|
| 《慢速基本面怎么破 1.58》(JL59463, 43842103671575) | 慢速骨架 `-reverse(ts_min_diff(winsorize(ts_backfill(F,120),std=4),504))+group_neutralize(densify(subindustry))`（KOR model25 提交 S1.75）；**fnd89 应计 TWN 同骨架 +0.68 与我们 DEU 0.59-0.72 同量级**；2Y 卡点修法=缩外层均值窗 504→252→168（非 decay）；同经济腿只贡献 1 颗 |
| 《应计家族：五种算法一个故事》(WQ36745, 43691920040087) | 应计本质=利润里没收到现金的部分；naive/Jones/修正Jones/Yoon/营运资本 五口径=同一故事不同算法；**论坛建议多口径共识跑法（全部报警才是真信号）** |
| 《模板大师 TWN 测评》(HX56822, 43841706410263) | Sloan 做空骨架 `-group_rank(winsorize(ts_backfill(fnd89_major_32_11,120),std=4),industry)`：STATISTICAL 中性化 0.68/2Y0.82 **> SUBINDUSTRY 0.56**；"经济故事对但区域筹码结构封顶 0.5-0.8，非参数能救"；应计符号跨区翻转常态 |
| 《量化日记第十一季》(WL13229, 39156513806871 评论深处) | fnd89_asset_51_31（非流动应计/sales）曾入真实提交组合（+oth335+sector，基本面动量质量增强），selfCorr 0.274 / prodCorr 0.863 |

**论坛增量结论（相对 BE242）**：① ts_min_diff 偏离深度形态（应计动量）**未测**——BE242 只测了水平 rank/交互/bucket；
② STATISTICAL 中性化未测（TWN 上比 SUBINDUSTRY 高 0.12）；③ 2Y 修复杠杆=缩均值窗。但论坛同样证实 Sloan 应计
在亚洲区结构性封顶 0.5-0.8 ⇒ 任何后续波期望值仍需压低。

## 九、BE246/BE247 论坛骨架验证波（2026-11-14）

**设计来源**：§八论坛增量三条 × DEU 适配。骨架经济故事从「应计水平」换成「偏离深度」（应计/现金流相对自身
2 年低点的位置）= BE242 未测的信号轴；`-reverse(x)` 已化简为直接符号（reverse=-x 平台确认）。
**符号先验**：应计动量向上=恶化 ⇒ -ts_min_diff；现金流向上=改善 ⇒ +ts_min_diff（指纹校验）。

### BE246（multisim `j2rTh1Tt4mWbga1exKzjbMI`，SUBINDUSTRY，8 臂）

| # | 臂 | 变量 |
|---|---|---|
| 1 | `-ts_min_diff(winsorize(ts_backfill(asset_41_11,120),std=4),504)` | 主字段窗 504 |
| 2 | 同 1，窗 252 | 缩窗梯 |
| 3 | 同 1，窗 168 | 缩窗梯 |
| 4 | `+ts_min_diff(...csjones_all_major_12...504)` | 现金流种子 504 |
| 5 | 现金流窗 252 | 缩窗梯 |
| 6 | `-ts_min_diff(...major_32_11...504)` | 净利应计对照（TWN 0.68 字段） |
| 7 | `-ts_mean(ts_min_diff(...66),504)` | 外层均值形态（EUR 例） |
| 8 | 同 7 外层窗 252 | 2Y 修复梯 |

### BE247（multisim `3mKiCldxq5chcbGCYvdQMbG`，STATISTICAL，4 臂）

BE246 臂 1/4/6 同式 + TWN Sloan 水平骨架 `-group_rank(winsorize(ts_backfill(major_32_11,120),std=4),industry)`，
只换中性化=STATISTICAL——单变量隔离（对照 TWN：STATISTICAL 0.68 > SUBINDUSTRY 0.56）。

**预检**：preflight 报 unknown_fields=[ts_min_diff]——已甄别为字段提取器把算子误当字段的缺口形态
（规范核心 `_field_patterns.py` 白名单含 ts_min_diff + 论坛真实提交双重印证），非平台缺算子，放行。
major_32_11 在 DEU 存在性经 preflight 字段解析确认。

### ⚠ 首派全灭：ts_min_diff / ts_min 本账号不可访问（幽灵算子教训第三次复发）

- 第一派（`j2rTh1Tt4mWbga1exKzjbMI` + `3mKiCldxq5chcbGCYvdQMbG`）：12 臂平台 ERROR
  「Attempted to use inaccessible or unknown operator ts_min_diff」，1 臂连坐 CANCELLED——**论坛先例
  与本地白名单都证明不了本账号的算子可访问性**（算子可访问性是账号级属性）。
- 重建尝试 2（subtract+ts_min 等价式）：toolkit 静态闸派发前拦截「[INACCESSIBLE_OP] ts_min 平台不可访问」
  ——静态闸比 operator_audit 更严（audit 模式2 对含 ts_min 的 9 式报 safe=true，漏了）。
- **等价几何重建（第三派，过闸）**：ts_min_diff(x,d)=偏离自身低点 ⇒ 可访问替身：
  **ts_scale(x,d)**（自身 2 年区间位置 0-1，语义最贴近）/ **ts_av_diff**（距自身均值）/ **ts_zscore**（标准化偏离）。
- 教训固化：幽灵算子坑（记忆 platform-ops-pitfalls）第 3 次——判据顺序应为
  **toolkit 静态闸 > operator_audit 模式2 > 本地白名单/论坛先例**；preflight unknown 这次是对的。

### BE246c（multisim `4dce6mgTo5h8cc0jeCVsDCr`，SUBINDUSTRY，8 臂）· BE247c（`3pk2QDgQp4XGci71gfTTO5Mm`，STATISTICAL，4 臂）

| # | 臂（SUBINDUSTRY 8 臂） | 变量 |
|---|---|---|
| 1 | `-ts_scale(winsorize(ts_backfill(asset_41_11,120),std=4),504)` | 区间位置 504 |
| 2 | 同 1 窗 252 / 3 窗 168 | 缩窗梯 |
| 4 | `+ts_scale(...csjones_all_major_12...,504)` / 5 窗 252 | 现金流种子 |
| 6 | `-ts_scale(...major_32_11...,504)` | 净利应计对照 |
| 7 | `-ts_av_diff(...asset_41_11...,504)` | 距均值几何 |
| 8 | `-ts_zscore(...asset_41_11...,504)` | 标准化偏离几何 |

BE247c = 臂 1/4/6 同式 + TWN Sloan 水平骨架 `-group_rank(winsorize(ts_backfill(major_32_11,120),std=4),industry)`，仅换 STATISTICAL。

## 十、BE246c/BE247c 收割归因（12/12 COMPLETE）→ fnd89 关档

### BE246c（SUBINDUSTRY，按臂序）

| # | alpha | 几何 | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|
| 1 | qM7eKnoE | ts_scale asset_41_11 504 | 0.49 | 0.25 | 0.86 | 0.48 |
| 2 | 9qlgz9Le | ts_scale 252 | 0.20 | 0.06 | 0.50 | 0.11 |
| 3 | 6XMgnROO | ts_scale 168 | 0.13 | 0.03 | 0.73 | 0.25 |
| 4 | MP69jbm8 | ts_scale csjones+ 504 | 0.75 | 0.45 | 0.78 | 0.54 |
| 5 | j2aN5nmj | ts_scale csjones+ 252 | 0.59 | 0.32 | **1.02** | 0.34 |
| 6 | **A1xqRnKe** | **ts_scale major_32_11− 504** | **0.98** | **0.72** | 0.45 | 0.39 |
| 7 | O0WK1nad | ts_av_diff 504 | 0.54 | 0.31 | 0.99 | 0.39 |
| 8 | LLKOPnxa | ts_zscore 504 | 0.25 | 0.09 | 0.58 | 0.14 |

### BE247c（STATISTICAL）

| # | alpha | 几何 | S | 2Y | 对照臂(SUB) |
|---|---|---|---:|---:|---:|
| 1 | wpoX8L1l | ts_scale asset 504 | 0.56 | 0.31 | 0.49 |
| 2 | LLKOPk62 | ts_scale csjones+ 504 | 0.39 | 0.34 | 0.75 |
| 3 | E5QoZka1 | ts_scale major 504 | 0.84 | 0.22 | 0.98 |
| 4 | O0WK1omv | Sloan 水平 industry | 0.62 | 0.12 | — |

### 归因四条

1. **偏离深度形态无一致破 1.0**：最佳 = major_32_11 区间位置 0.98/F 0.72（fnd89 今日最高，勉强触及论坛「封顶 0.5-0.8」上沿）；现金流侧 0.75；av_diff 0.54；zscore 0.25。
2. **STATISTICAL 在 DEU 无一致增益**（对照对 0.98>0.84、0.49<0.56、0.75>0.39）——TWN 经验不跨区外推（跨区不外推铁律又一例）。
3. **缩窗梯反向**：504→252→168 单调恶化（0.49→0.20→0.13）——论坛「缩窗救 2Y」在 fnd89 上连 S 一起杀；2Y 最高 1.02 仍远低于 1.58。
4. **2Y 轴终判死**：22 臂 fnd89 今日 2Y 最高 1.02（csjones 区间位置 252），AT‌OM 唯一放宽轴无法达标。

### fnd89 判死档案（六维闸合规，PROVISIONAL → 终判死·信号层）

| 维度 | 证据 |
|---|---|
| D1 结构互异模板 ≥10 | 水平 rank(5 族)/乘法交互/bucket 条件化/ts_scale/ts_av_diff/ts_zscore/外层均值/多窗(504/252/168)——22 臂今日 + 20 臂历史 |
| D2 字段族自测 | asset_41/51/61 + best11 + csjones + major_32 六族全实测 |
| D3 矩全家 | 水平 ✓（BE242）/ 偏离动量 ✓（ts_scale/av_diff/zscore）/ 比值 ✓（/TA /sales /CA 分母）/ 二阶波动 ✓（fnd90_game_accruals_vol S 0.01 类别级） |
| D4 分组轴 ≥2 | sector / subindustry / industry（TWN 骨架） |
| D5 非线性 ≥1 | bucket 条件化（BE242 #10）+ winsorize/tail |
| D6 配置 ≥2 | SUBINDUSTRY × STATISTICAL × 多窗 × decay4 |

**终判死范围**：DEU/TOP500/D1 下 fnd89 信号层死——S 天花板 ~1.0（水平 0.72 + 偏离深度 0.98）、2Y 轴死（≤1.02 vs 闸 1.58）、论坛三条增量（ts_min_diff 骨架/缩窗/STATISTICAL）全部实测无解。判死依据=读数，不改写邻接数据集先验（跨区不外推）。

## 十一、检索覆盖审计（用户质询：fnd89/90/93 论坛+论文是否查过）与 fnd90/93 新增模板

**覆盖矩阵（2026-11-14 补齐后）**：

| 数据集 | 论坛 | 外部论文 |
|---|---|---|
| fnd89 | ✓ 4 帖精读（Sloan 骨架/慢速骨架/五算法/真实提交） | 间接（Sloan 1996/Jones 1991 内嵌算子族），判死时已算穷尽 |
| fnd90 | ✗ 当时未查 → **已补：154 赞 ARC/GLB 模板帖（43499065604247）**，fnd90 列为 2025-11 新集，描述含**「3 个月收益预测」成分**（⇒ `fnd90_qes_gamef_score` 疑似该成分，0 臂未测） | ✗ 未查 → 以教科书文献补（Piotroski 2000/Mohanram 2005/Novy-Marx 2013/QMJ/CHS 2004）：**质量分单腿在大盘弱是文献预期；Piotroski 正解=value×quality 交互（fnd90 内无估值腿，ATOM 下不可复制——结构性理由）** |
| fnd93 | ✗ 未查 → **已补：论坛零直接命中（no_result）** | ✗ 未查 → 教科书（Hanlon 2005 book-tax gap、Desai-Dharmapala 2009 治理交互——治理交互跨集，ATOM 内不可复制） |

**新增未测模板（fnd90，源自 ARC/GLB 帖 F1c/F3/F6 骨架 + 文献）**：SCORE 预测字段裸跑；F1c 滚动极值 `rank(ts_arg_min(ts_backfill(F,120),504))`；trade_when 自身波动门控；quality×自身动量条件化（QMJ 式，ATOM 内唯一可复制的条件化）；F6 `rank(ts_rank(F,242))`；F3 组内均值残差（group_median 幽灵→group_mean 替代）+ BE246 验证过的 ts_scale 区间位置移植。
**fnd93 新增**：税应计区间位置（-ts_scale 504）+ 一阶差（-ts_delta 66）——BE246 几何在 fnd93 未测。
**避坑情报（ARC/GLB 帖 §06）**：fundamental88/analyst11/model255 等「质量/ESG」名头集实为 RIC↔BBID 映射表 ⇒ **fnd22 同款映射描述，其 3 颗 ra_clean 大概率是映射表伪信号，永不复检**。
**fnd90 判弱 → 回退 PROVISIONAL；fnd93 弱水平维持 PROVISIONAL**，BE248 验证后定档。

## 十二、BE248 收割（论坛+论文新模板验证，10/10 COMPLETE）

| # | alpha | 模板 | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|
| 1 | wpoXpMg2 | SCORE（3月收益预测成分）裸跑 | -0.12 | -0.03 | -1.10 | 0.53 |
| 2 | E5Qo5XA1 | F1c 滚动极值 arg_min(pscore) | 0.70 | 0.43 | 1.05 | **0.95** |
| 3 | A1xq1MdY | trade_when 自身波动门控 | 0.83 | 0.54 | 1.07 | 0.53 |
| 4 | **O0WK0Evp** | **trade_when 分数上升门控（QMJ 式）** | **0.71** | 0.47 | **1.51** | 0.63 |
| 5 | 88Ng8dqv | F6 rank(ts_rank(cash_cov,242)) | 0.56 | 0.31 | -0.46 | 0.32 |
| 6 | WjlKj6mo | F3 组内均值残差 | 0.10 | 0.02 | -1.28 | 0.44 |
| 7 | YPaXPGdo | ts_scale cash_cov+504 | -0.05 | -0.01 | -1.46 | 0.49 |
| 8 | pwaQwA0q | ts_scale deferred+504 | -0.37 | -0.15 | -1.82 | 0.17 |
| 9 | bla7l5pZ | fnd93 税应计 -ts_scale | 0.06 | 0.01 | -0.02 | 0.08 |
| 10 | mLaeLMO2 | fnd93 税应计 -ts_delta66 | 0.10 | 0.02 | -0.53 | 0.17 |

**归因**：
- **★ 真绿芽（全战役最强结构发现）**：`trade_when(ts_delta(pscore,66)>0, group_rank(pscore,sector), -1)`（QMJ 式条件化）把裸 pscore（S 0.02/2Y −0.49）拉到 **S 0.71 / 2Y 1.51**——2Y 距闸 0.07，条件化杠杆 S+0.69、2Y+2.0。文献预期吻合：质量分单腿弱，条件化是正解。
- 自身波动门控（0.83/1.07）与 arg_min（0.70/1.05/sub 0.95）同为正增益；残差/ts_scale/F6 在 fnd90 无效。
- **fnd93 判弱入档**（不升终判死）：水平(8)+区间位置+一阶差(2) 全 ≤0.53；缺 D3 二阶波动与 D6 第二配置，但论坛 no_result + 论文交互（治理×税）跨集不可 ATOM ⇒ 实质关闭。
- SCORE 预测成分零信号（|S|≤0.12）。

## 十三、BE249 门控杠杆深挖（multisim `4qfm5mcF54oN8ANApwU7den`，8 臂）

沿 BE248#4 唯一活体结构展开：门控窗 22/132、分组轴 subindustry、group_zscore 形态、门控移植
（cash_coverage/icfroe_5y/grossprofit_asset）、ts_decay_linear 平滑。全 SUBINDUSTRY。

### 收割（8/8 COMPLETE，按臂序）

| # | alpha | 臂 | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|
| 1 | LLKOLGQe | gate22 pscore | **0.88** | 0.65 | 1.12 | 0.58 |
| 2 | e7ae73j6 | gate132 pscore | 0.53 | 0.31 | 1.34 | 0.29 |
| 3 | wpoXparv | gate66 pscore subindustry | 0.69 | 0.42 | 1.52 | 0.71 |
| 4 | zqdXqNlK | gate66 pscore group_zscore | 0.74 | 0.50 | 1.42 | 0.63 |
| 5 | O0WK0Glq | gate66 cash_cov | 0.82 | 0.58 | 0.54 | 0.67 |
| 6 | e7ae73X6 | gate66 icfroe_5y | 0.71 | 0.43 | 0.23 | 0.35 |
| 7 | **pwaQwN93** | **gate66 grossprofit_asset** | **0.75** | 0.49 | **1.71 ✓** | 0.47 |
| 8 | zqdXqkvK | gate66 pscore +decay10 | 0.70 | 0.46 | 1.52 | 0.62 |

### 终局结论（FUNDAMENTAL 锁定日收官）

- **★ 首个 2Y 过闸件**：pwaQwN93 = `trade_when(ts_delta(GP/TA,66)>0, group_rank(GP/TA,sector), -1)`
  **S 0.75 / 2Y 1.71**——仅剩 LOW_SHARPE/LOW_FITNESS 两闸未过（failed_ra_count 2）。GP/TA 裸跑
  是 −0.13（BE244#6），门控杠杆 S+0.88、2Y+1.84。
- 门控杠杆普适性验证：pscore 全变体 2Y 1.12–1.52、GP/TA 1.71 ✓；S 天花板 0.75–0.88（gate22 最高 0.88）。
- **S 差距 ~0.7-0.8 仍为结构性**（战役经验封顶判断成立），但产出两个 **2Y 达标塔位储备**
  （pwaQwN93 / wpoXparv 1.52）——FUNDAMENTAL 类别从「全灭」升级为「塔位储备 ×2 + 可复用条件化杠杆」。
- **可复用杠杆 C（新入册）**：`trade_when(自身动量>0, group_rank(质量分, sector), -1)`——
  质量分族（GAME/评分类）通用的 S/2Y 双升条件化，DEU 实证 +0.7~0.9 S、+1.8~2.0 2Y。
- prod 未测（S 未达 1.58，无提交路径，不占相关性槽位）。

## 十四、杠杆 C 入册 + BE250 破闸深挖（2026-11-14）

**杠杆 C 已登记** `Claude/skills/wq-brain-ra-deu/references/_effective-levers.md`（A/B/C 全量，含边界与失效反例），
sync_skills 5 安装位零漂移 ✅。

**BE250（multisim `2EunF7fSK4BQcbAnNxlT5D`，10 臂，全 SUBINDUSTRY）**——破闸目标：门控件 S 0.75-0.88 → 1.58。
归因驱动变体（禁止盲扫）：

| # | 臂 | 归因假设 |
|---|---|---|
| 1 | gated GP/TA + gated pscore **等权加** | 两机制合成（S 叠加唯一实证路径=AS3；同集内替代尝试） |
| 2 | gated GP/TA × gated cash_cov **乘法** | 无权重自由度合成（杠杆B 同集版） |
| 3 | gated GP/TA + **signed_power 1.3** 锐化 | model238 实证锐化形态 |
| 4 | 门控阈值升级（Δ > 自身 252 均值） | 弱改善剔除 |
| 5 | **tail+winsorize** 包装 | institutions 1.71/2.79 形态移植 |
| 6 | **杠杆 A 双层中性化** on gated pscore | A 册迁移（单腿未证，实测边界） |
| 7 | gate22 on GP/TA | pscore 最优 S 窗移植 |
| 8 | gate66 GP/TA subindustry + decay10 | 最优轴 + 平滑组合 |
| 9 | **icfroe_3y** gated 裸测 | 1y/3y 窗未测（仅 5y 测过且失败） |
| 10 | gated GP/TA + gated icfroe_3y 等权加 | 盈利质量×现金回报合成 |

**同源 add 登记（闸5 豁免条件，臂 1/10）**：权重来源=等权（无调参）；腿间 corr<0.7 假设依据=
GP/TA（盈利质量）vs pscore（会计质量复合）vs icfroe_3y（增量现金流回报）为不同机制矩；
若实测腿相关 >0.9 则作废该臂解读。

（待收割）

### 收割（10/10 COMPLETE，按臂序）→ 破闸评估：**未破**

| # | alpha | 臂 | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|
| 1 | A1xqjl6E | GP/TA+pscore 等权加 | 0.49 | 0.23 | 1.12 | 0.84 |
| 2 | xAvXOjMJ | GP/TA×cash_cov 乘法 | 0.41 | 0.18 | 0.32 | 0.71 |
| 3 | 9qlgZXgq | sp1.3 锐化 | 0.75 | 0.53 | 1.69 | 0.57 |
| 4 | ZYakP7k3 | 阈值升级（Δ>自身均值） | 0.78 | 0.52 | 1.70 | 0.42 |
| 5 | **gJa7kj7v** | **tail+winsorize 包装** | **0.84** | **0.59** | **1.68** | 0.56 |
| 6 | WjlK17Kd | 杠杆A 双层中性化 | 0.70 | 0.45 | 1.69 | 0.70 |
| 7 | N1Pkx7kp | gate22 GP/TA | 0.70 | 0.44 | 1.57 | 0.47 |
| 8 | wpoXKjXY | subindustry+decay10 | 0.51 | 0.25 | **1.76** | 0.35 |
| 9 | 78Yg7jgv | icfroe_3y gated | 0.20 | 0.07 | 0.85 | 0.27 |
| 10 | LLKOV7Ov | GP/TA+icfroe_3y 加 | 0.21 | 0.07 | 0.49 | 0.44 |

**归因五条**：
1. **同源合成全灭**（等权加 0.49/0.21、乘法 0.41）——fnd90 内两腿同族，加/乘均稀释；闸5 登记的 corr<0.7
   假设在机制层面不成立（同族质量分），同源合成路径在 fnd90 内关闭。
2. **tail+winsorize 是唯一正增益**（+0.09 → 0.84/F0.59/2Y1.68，margin 0.8% 全波最高）——institutions
   形态在质量分族成立。
3. **杠杆 A 单腿无效确认**（0.70 vs 0.71 baseline）——A 册边界「仅 MODEL 多腿结构」实测坐实。
4. **S-2Y 跷跷板再现**（decay10+subindustry：2Y 1.76 全类别最高但 S 0.51）；gate22 不迁移（0.70<0.75）。
5. icfroe_1y/3y/5y 全窗死（0.20-0.71）——增量现金流回报族在 DEU 无信号。

**终态**：fnd90 ATOM 破闸失败——S 平台 0.84-0.88（tail 形态 + 阈值升级为最优），2Y 轴已稳定过闸
（1.68-1.76），距 1.58 差 0.74 且剩余结构手段（合成/锐化/包装/窗/轴/平滑）全部实测。塔位储备
2Y 过闸件共 4 颗：gJa7kj7v(0.84/1.68)、ZYakP7k3(0.78/1.70)、9qlgZXgq(0.75/1.69)、pwaQwN93(0.75/1.71)。

## 十五、BE251–BE256 收官冲刺：fnd1 治理面（2026-11-14）

### BE251 存在性探针（`2aGZzH7n75iDaay9rexSjLd`，10 臂）

- **alpha_factor_lib：数据层排除**——臂 1-3 DD 71%/199%/83%、margin −0.5~−5.7%（超窄账户签名），
  行业 VECTOR 字段在 TOP500 宽度塌缩先验实证坐实；仅保险字段略宽仍弱（0.28）。
- **fnd1 治理面三活体**：CEO 任期 timerole 符号**翻转**（文献先验「壕堑」错，DEU 实证「经验」正：
  −1.26 → 翻正 S 1.26/2Y 1.35）；董事流失率稳定 0.81/0.97（DD 仅 6.7-7.1%）；股权激励对齐 +0.68。

### BE252 结构化（`3kPt5n6sU5ck9bfdy3HqkN6`，8 臂）

tail+winsorize 包装 = **wpoXmKGv S 1.35/F 0.97/2Y 1.61✅/sub 1.27**（全类别首次逼近）；双腿/三腿合成 1.11-1.21；
杠杆C 门控反而降（0.98——任期是单调 ratchet 变量，动量门控无意义，与 icfroe 同理）。

### BE253–BE256 网格收敛（8+8+8+6 臂）

**带宽曲线**（std2/sector）：none 1.26 → 0.30/0.70 1.30 → 0.25/0.75 1.35 → 0.20/0.80 1.46 →
**0.15/0.85 = 1.53（leaJqajl）** → 0.10/0.90 1.49 → 0.05/0.95 1.45。std3 等价（MP69Rjl6 1.53）；
decay5 无增益（1.52）；**decay=12（设置级）反而降**（1.43-1.49）；subindustry 轴降（1.28）；
director 变体降（1.43）。**prod 前置双测（用户令）**：wpoXmKGv 0.6805 ✅、gJa7A1k0 0.656 ✅——家族无 prod 雷。

### fnd1 终态（44 臂）

| 项 | 读数 |
|---|---|
| **峰值形态** | `tail(winsorize(group_rank(ts_backfill(vec_avg(fnd1_board_characteristics_filtered_timerole),250),sector),std=2),lower=0.15,upper=0.85,newval=0.5)` |
| **最优** | leaJqajl / MP69Rjl6 = **S 1.53 / F 1.21 / 2Y 1.95 / sub 1.05 / TO 2.9% / DD 7.0%** |
| **闸距** | **仅剩 LOW_SHARPE 一项，差 0.05**；prod 0.656✅（双测） |
| 网格维度 | 带宽 7 点×std 2 档×decay 表达式/设置级×2 轴×2 字段变体×3 复合×门控/位置形态——**全收敛，无信息增益残留** |

**判定**：fnd1 CEO 任期族 = **FUNDAMENTAL 类别最优近闸家族**（与 fnd89 的 2Y 死轴、fnd90 的 0.7 差距完全
不同性质——prod/2Y/F/sub 全过，只差 S 0.05，且 S 为 IS 事实不随池漂移）。网格已收敛 ⇒ 封顶 1.53，
**今日不再加注**；保留为最高优先候选家族，待新结构灵感（非参数）或跨族合成授权再启。

### FUNDAMENTAL 12/12 终态矩阵（2026-11-14 收官）

| 数据集 | 终态 |
|---|---|
| fnd45 | 穷尽（0.96 塔位 ×2） |
| fnd89 | 六维终判死 |
| fnd90 | 判弱；2Y 过闸塔位 ×4 |
| fnd93 | 实质关闭 |
| digital_ad_spend | 数据层排除 |
| fundamental22 | 映射表伪集排除 |
| **fnd1** | **近闸家族 1.53（差 0.05），prod 净，网格收敛封顶** |
| alpha_factor_lib | 数据层排除（宽度塌缩实证） |
| fnd72 | 浅探+强负先验（宽度 2-5），不再加注 |
| fnd6 | 浅探（主面 0.37 + ATOM 天花板 1.15） |
| fnd17 | 浅探（已标死，拥挤） |
| fnd86 | 近穷尽（7 字段 0 passed） |

## 十七、BE259–BE261 group_backfill 破闸（用户指令）→ **pwaQ0bx3 全闸通过，待用户确认提交**

### BE259 gBF 修 CW（`4x4SxXdnO5869uuv2mBMp37`，8 臂，用户指令「用groupbackfill可以解cw问题」）

- **裸 gBF 灾难**（臂 1/2/3/5/6 全灭，TO 47–60%）：gBF 填充值随组均值日漂移，慢变量变日频信号。
- **叠加形态成功**：`group_backfill(ts_backfill(vec_avg(F),250), sector, 250)` = KPgxRLG8 1.55/1.34/1.97——
  **CW 从 warning 0.25 修成 PASS**（用户配方命中，CW 破局手册第一解药再验证）。
- 臂 8 与 BE258#5 表达式全同，平台去重返回同 id（LLKOAn8m）。

### BE260/261 带宽×std×gBF 合成网格（16 臂）→ 三颗 RA 全过

zscore 带宽曲线（gBF 形态）：±0.85→1.49 / ±0.9→1.55 / **±0.95→1.57-1.60（峰）** / ±1→1.56-1.57 / ±1.05→1.49-1.51 / ±1.1→1.48。
std3 在 gBF 形态略正（±1.05：std3 1.51 > std2 1.49）。

| alpha | 形态 | S | F | 2Y | sub | failed_ra |
|---|---|---:|---:|---:|---:|---:|
| **pwaQ0bx3** | **gBF ±0.95 std4** | **1.60** | **1.40** | **2.01** | **1.25** | **0** |
| 9qlgo58K | gBF ±0.95 std3 | 1.59 | 1.38 | 1.97 | 1.24 | **0** |
| QP0meRzK | gBF ±0.95 std3 + decay5 | 1.58 | 1.37 | 1.96 | 1.22 | **0** |

**pwaQ0bx3 表达式**：`tail(winsorize(group_zscore(group_backfill(ts_backfill(vec_avg(fnd1_board_characteristics_filtered_timerole),250),sector,250),sector),std=4),lower=-0.95,upper=0.95,newval=0)`

### 五道闸判定（pwaQ0bx3，§7.5 链）

| 闸 | 结果 |
|---|---|
| ①台账排除 | ✅ fnd1 全新面 |
| ②RA+塔位 | ✅ failed_ra_count=0；pyramids DEU/D1/FUNDAMENTAL ×1.8 |
| ③近十年 | ⚠️ 2014 pnl −17.6K（−0.09%，首年爬坡微亏）不满足严格 pnl>0；其余 9 年全正，lc/sc 十年全 >0 |
| ④prod / self | **prod 0.6821 ✅（严格<0.7，直方图健康）**；self-corr 全池计算超 30s 客户端窗（未决） |
| ⑤篮内互相关 | ✅ **max 0.1385**（vs Jj8VQwoe），18 颗全矩阵 all_below=0.7 |

**submit_verdict：UNVERIFIABLE（非 BLOCKED）**——failed_any=0、硬闸 warning 空；放行条件 = prod<0.7（✅已实测）+ 用户确认。
wq-alpha-gate-push-op-min skill 覆盖检查：③杠杆（带宽网格）/④压缩（6 算子零冗余全承重）/⑤设置（decay/trunc 已扫）均已执行；
self-corr 全池计算超时未决，间接证据（prod 直方图 + 篮内 0.14）指向低相关。

**状态：✅ 已提交（用户 2026-11-14 会话内原话「确认」）——平台 status=ACTIVE，stage=OS（起 2024-01-01），dateSubmitted 2026-11-14，name=DEU_R_alpha_01（自动），color=BLUE。平台自算 selfCorrelation=0.1904（此前本地全池计算超时的疑虑解除）。篮子 17 → 18/20，缺口 2。**
robustness 审计链：brain-alpha-robustness Phase B/C PASS（soft_flags: CV_Sharpe 0.44 / max-min 3.42 / ops 6 / 2014 flat），台账 `robustness_pwaQ0bx3` 已落，报告 `reports/robustness_20261114.md`。备份件 9qlgo58K/QP0meRzK 同族 >0.99 标 SUPERSEDED。

## 十六、BE257/BE258 非参数结构取证 → **3q0gZE0N 临界可提交**（2026-11-14）

### BE257 新结构（`3RALY3fWm5bYcy2TsN5GSfP`，10 臂，论坛 no_result + 倒 U 文献驱动）

| # | 臂 | S | 发现 |
|---|---|---:|---|
| 4 | **group_zscore 量级形态** | **1.38/F1.08/sub1.32** | **rank 扔掉的量级信息有效**（25y vs 8y CEO）|
| 3 | −vec_min 翻正 | +1.21 | **新血多=好**（与直觉相反）|
| 2 | −vec_stddev 翻正 | +0.84 | 任期分散=多样性=好 |
| 1 | vec_max（最长者=CEO）| 1.17 | 弱于 vec_avg（平均值信息量大）|
| 7/8 | ×激励/×流失 乘法 | 0.68/−0.23 | fnd1 合成乘法也稀释（铁律三证）|
| 9 | ts_zscore 动量 | 0.68 | ratchet 变量确认 |

### BE258 zscore+tail（`44m5cC32q5gm9eWhasZfYRI`，8 臂）→ **临界破闸**

| # | alpha | 臂 | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|
| 1 | **3q0gZE0N** | **zscore+tail ±1（std2）** | **1.56** | **1.46** | **2.01** | 1.28 |
| 2 | e7aeon1J | ±0.8（std3）| 1.48 | 1.28 | 1.79 | 1.38 |
| 3 | kqae2n8L | ±1.2（std2）| 1.33 | 1.23 | 1.77 | 0.98 |
| 5 | LLKOAn8m | vec_min+tail | 1.36 | 1.00 | 1.47 | 0.91 |

**3q0gZE0N = `tail(winsorize(group_zscore(ts_backfill(vec_avg(fnd1_board_characteristics_filtered_timerole),250),sector),std=2),lower=-1,upper=1,newval=0)`**
- **平台 get_alpha_details：checks.fail = []（空）**——LOW_SHARPE（1.56 vs 1.58，差 0.02）与 CW（0.25 vs 0.1）均在 **warning 层**；
  LOW_FITNESS/LOW_2Y/SUB/CLUSTER/TO/MATCHES_PYRAMID 全部 **pass**；
  longCount 89/shortCount 91（健康覆盖），margin 0.75%，DD 8.0%，returns 10.9%。
- ⚠ 提交层风险预记：CW 0.25>0.1 为 warning，按 MP6OgoPr 战例「WARNING 被资格门升级阻断」先例，
  最终以 submit_verdict 判定为准（否决权威，只能拦不能放）。
- prod 探针（近闸纪律）：待测（槽位排队中）。
