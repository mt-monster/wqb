# news50（mws50_*，RavenPack RPNA 新闻情绪）字段画像 —— DEU/TOP500/D1 —— 2026-11-03

**来源**：MCP `get_datafields`（内建通道 Session not found，走 `tools/mcp_http_caller.py` 兜底；args=`tracking/DEU/_mcp_reads/news50_fields_args.json`）。
**定位**：§86 真新鲜 6 集之一（NEWS category，非 trio 塔）；纯单数据集 ATOM = 零组合配额。

## 总量与拥挤度
- **37 个字段，全 VECTOR**，coverage 统一 **0.7644**（集级覆盖）。
- 拥挤度全库最低档：alphaCount 合计 **65**、**14 字段零使用**；最挤的也仅 ens_similarity_gap=8 / ess=7 / ens=6 / vea=6。
- 对照：other47 为 0–6；news50 同属「没人挖过」的新鲜面。

## 字段家族（按机制归类）
| 家族 | 字段 | 机制角色 |
|---|---|---|
| **事件情绪分（分类器）** | acb(公司行动) / bam(M&A) / bee(盈利评估) / ber(盈利发布) / ghc_lna(分析师建议变动) / aes(91d 正负比) / qcm / qep / qmb / ssc / vea | **信号腿**——分类器情绪分，可做事件型 alpha |
| **核心情绪** | ess（0–100 粒度情绪） | **主信号腿**（最通用） |
| **事件新颖性** | ens / ens_elapsed / ens_key / ens_similarity_gap + 全球族 g_ens* | **时效/衰减机制**——novelty decay、旧闻钝化 |
| **影响预测** | nip（0–100，未来 2h 市场影响预测） | **条件侧**（GBR news50 N9 实证：nip 放条件侧 gate 0.74，放信号侧迁移到 news104 剩 0.28） |
| **元数据/分组轴** | category / group / topic / type / sub_type / news_type / property / relevance / country_code / maturity / position_name / product_key / evaluation_method / time / rp_story_event_count / rp_story_event_index | **gate / group / bucket 专用**，不得当信号腿（类别卡禁令） |

## 波次设计前必办（纪律）
1. **先加载 `brain-alpha-research-news-sentiment`**（字段 5 家族分类 × 6 桶配对设计）再组模板池（≥10 互异）。
2. **机制先查论坛 + 论文**：RavenPack ESS/NIP/ENS 的公开因子定义与方向先验（novelty→动量延续 vs 旧闻反转）。
3. **量纲**：全 VECTOR ⇒ 数值位一律 `vec_avg`/`vec_sum` 包裹；分类器分数 0–100 水平型用 `group_rank(raw, g)`（水平型禁逐股 ts 归一化）；事件型稀疏字段降换手用 trade_when / ts_delta（禁 decay_linear 当降 TO 杠杆）。
4. 覆盖口径：逐年 longCount/pnl 判「连续多年空窗」；leading-gap 待用户裁定（在册 4 例）。

## 补录：关键字段口径（description 全文）
- **ssc**：0–100 整体故事情绪综合分（composite）——最通用主信号腿。
- **qcm**：多分类器加总情绪分（BMQ+BEE+BCA+ANL-CHG，取故事中最相关公司）。
- **qep**：PEQ 分类器，按文章词/短语的全球股票情绪分。
- **qmb**：社论/评论分类器分（equities 包）。
- **vea**：**91 天事件量**（非中性事件计数，ESS≠50）——注意力/量能机制（与 other47 流量同角）。
- **aes**：**91 天正负事件比**（ESS>50 为正 / 非中性事件）——情绪质量比率机制（同 other47 T5 净额比率角）。
- **relevance**：实体-故事相关度 0–100——**gate/加权字段**，低相关实体事件应被门控剔除。
- **rp_story_event_count / _index**：单故事的实体事件总数/序位——故事广度上下文，宜作 gate 不作信号腿。

**机制箱补全**（信号腿四箱 + 条件箱）：①情绪水平（ess/ssc/qcm/qep/qmb/分类器分）②情绪比率（aes）③量能/注意力（vea、rp_story_event_count）④新颖性衰减（ens 族、g_ens 族）＋条件箱（nip 条件侧、relevance 门控、taxonomy 分组轴）。

- 交叉 GBR 经验：news50 的「nip 影响预测信息在条件侧」是已验证机制；S 判死不跨数据集迁移、prod 判死在家族内——DEU 重新开机制。
## 机制取证（2026-11-03，用户纪律：用机制前查论坛+论文）

**外部论文 2 锚**：
1. 《ESG新聞情緒對股價之影響》（政大论文，RavenPack 数据）：新闻情绪与股价**同向**；**负面冲击 > 正面**（非对称）⇒ 情绪水平正向先验 + 负向侧加权（asymmetric payoff）。
2. 《News-based investor disagreement and stock returns》（Springer, RAS 2025）：新闻期**量-波弹性=投资者分歧代理**，分歧**负向预测**横截面收益；且**用 RavenPack relevance 分数筛个股专属新闻** ⇒ ①分歧机制箱（vea×波动交互）方向=负 ②relevance 门控有学术出处。

**BRAIN 论坛 4 帖**：
| 帖 | 要点 | 对本集的启示 |
|---|---|---|
| 《寻找阿尔法：新闻与社交媒体》KP26017 | RPNA 字段用法：qcm 类字段→relevance 角色、情绪分→正/负/中性辅助决策、novelty→新颖性 | mws50 与 nws18 同族，字段角色划分可直接参照 |
| 《情绪差模板出货一般》SJ65808（15 赞） | Sentiment Comparison（正负情绪配对差）在 AMR 几万模拟仅 ~10 个 S>1 | **负证据**：纯「情绪差配对净额」骨架出货率低，别当主骨架 |
| 《【Alpha灵感】情绪类因子》SY50351 | 当日新闻总情绪无单字段可表；情绪内含极大不确定性；股价涨→吸引资金（反身性） | 支持「聚合窗（aes/vea 91d）优于瞬时情绪」 |
| 《拷打AI：机构情绪分歧因子》ZL35633（17 赞） | 买/卖机构数对比判趋势持续性（IND） | 呼应论文 2 分歧口径：多空计数分歧→持续性条件 |

**取证结论 → 模板池方向先验（预告）**：①情绪水平正向+负侧非对称 ②分歧/量-波弹性负向（vea 机制箱）③聚合窗（91d 比率/量）优于瞬时 ④relevance 门控剔噪 ⑤「情绪差配对净额」只作对照不作主骨架。模板池设计须 ≥10 互异并逐条标来源。

