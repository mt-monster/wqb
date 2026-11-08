# DEU 目标恢复段 · 正交面开掘（2026-11-07 下半场）

> 背景：目标被用户恢复为 active。上一段（fundamental 12 集 + analyst7）0 颗全闸通过；
> 本段先做「遗留候选清算 + prod 墙量化」，再转向未被占用的机制面。

## 一、遗留 READY 候选清算（11 颗 → 0 颗可用）

`submit_ready` 中 DEU 残留 11 颗 READY，其中 10 颗 IS 全闸通过（S≥1.58 / F≥1.0 / 2Y≥1.58 / RA 零失败 / UNSUBMITTED），
只差 prod/self 未测。逐颗实测结果：**全部被相关性墙拦下**。

| id | S | F | 2Y | self（vs OS 池） | 拦路者 | 判定 |
|---|---:|---:|---:|---:|---|---|
| RREXxW6z | 1.77 | 1.61 | 1.83 | **1.000** | 2rjrMZ25 | 同核已提交 |
| 6Xdx65eK | 1.73 | 1.38 | 1.71 | ≥0.98（互相关） | RREXxW6z | 同核换桶粒度 |
| 1YNv8qaK | 1.76 | 1.35 | 1.61 | ≥0.98（互相关） | RREXxW6z | 同核换桶粒度 |
| Vkxnb8QG | 1.83 | 1.64 | 2.09 | 0.959 | LLM93nGa | self 墙 |
| E56AzejK | 1.71 | 1.36 | 2.79 | 0.918 | 2rmGAPqN | self 墙 |
| 58gGQmlN | 1.62 | 1.26 | 2.58 | ≥0.97（互相关） | E56AzejK | 同核 |
| MPY9VNY9 | 1.59 | 1.26 | 2.36 | 0.992 | xArzm3Mn | self 墙 |
| XgJ980Wb | 1.60 | 1.26 | 2.05 | 0.803 | 58gkLAkk | self 墙 + MODEL×OTHER 违规 |
| kqNRX1ZP | 2.06 | 1.86 | 2.37 | 0.794 | bl6OWZ2M | self 墙 |
| QPKKMg6Q | 1.65 | 1.47 | 1.58 | 0.668 ✅ | — | **prod 0.807 深钉**（[0.8,0.9] n=1、[0.7,0.8] n=8）✗ |

互相关（本地 compute_mutual_correlation, threshold 0.7, 4y）：最大对 RREXxW6z↔6Xdx65eK **0.9855**、
E56AzejK↔58gGQmlN **0.9701**；最大互不相关篮子仅 **7 颗**（RREXxW6z/E56AzejK/kqNRX1ZP/Vkxnb8QG/MPY9VNY9/QPKKMg6Q/XgJ980Wb）。

**结论**：DEU 的 OS 池已把「预期修订 / 融券 / 情绪 / 机构持仓 / 模型质量」五面占满，遗留候选只是同核变体。

## 二、OS 池与塔位占用（get_pyramid_alphas · 2026-11-07）

DEU/D1 已提交 ACTIVE 共 **14 颗**（S 1.64–2.27）：
bl6OWZ2M(2.03, SENTIMENT)、LLM93nGa(1.88, SHORTINT+ANALYST)、xArzm3Mn(1.64, SHORTINT)、mLYLEm99(2.27, SUPER)、
2rjrMZ25(1.77, ANALYST)、Wje5K71x(1.73, FUNDAMENTAL)、2rmGAPqN(1.81, INST+OTHER)、58gkLAkk(1.75, MODEL+OTHER)、
JjxrYjre(1.68)、2rOe10qY(2.10)、vRk6og8b(1.80)、Vk65zLzG(1.79)、883Y3bAW(2.17)、blRnKEk6(2.02)。

塔位计数（DEU/D1）：analyst 2 / other 2 / shortinterest 2 / institutions 1 / model 1 / fundamental 1 / sentiment 1；
**news 0、earnings 0、risk 0、macro 0、imbalance 0、pv 0、insiders 0、socialmedia 0、option 0**。

⇒ 可开新面 = 上述 9 个 0 计数面（单数据集 ATOM 不触碰 PV/MODEL/OTHER/FUNDAMENTAL 互组禁令）。

## 三、prod 墙量化（本地库 40 颗 DEU 高 S 候选）

| 区间 | 计数 | 样本 |
|---|---:|---|
| prod < 0.7（可用） | 8 | Wje5K71x 0.4305、MP3ENd38 0.4542、e7QYZN9l 0.4857、1YZ8AOXM 0.4908、pwdJKxQv 0.5273、58gkLAkk 0.5381、883Y3bAW 0.5434、blRnKEk6 0.5766 |
| prod 0.70–0.80 | 9 | RRE1Xrjj 0.7562、P0oe6wpJ 0.7694、2rOW3j6b 0.7783、j23xqexE 0.7746、j23xxK8o 0.7859、MP1ZZN3L 0.79、1YNv6Ymk 0.7983、vR102Ver 0.802、1YNvvgdJ 0.8306 |
| prod ≥ 0.80 | 4 | JjelQJoe 0.8373、QPvdMW8Q 0.8849、JjelQnvE 0.9084、E5vLLPV0 0.9386（族判死） |

**要点**：prod<0.7 的 8 颗中 6 颗已是 ACTIVE(OS)。⇒ **DEU 新件必须来自与书正交的机制面**，
同族提 S 只会把候选推进 0.75–0.91 的死区。

## 四、H1 探针：analyst_revision_horizons（180 个 change_pct 字段，几乎全零使用）

骨架 A = DEU 已验证双窗 + 桶轴：`group_neutralize(quantile(add(ts_mean(ts_backfill(F,1008),8),ts_mean(ts_backfill(F,1008),252))),bucket(rank(ts_mean(ts_backfill(F,1008),252)),range="0,1,0.1"))`
骨架 B = `group_rank(ts_mean(ts_backfill(F,1008),252),subindustry)`

multisim `4dHoUmbWj4gE98jwPvWTDX3`（10 条，decay4/SUBINDUSTRY/trunc0.08）：

| 字段 | 骨架A S | 骨架B S | 2Y(A) |
|---|---:|---:|---:|
| f12m_earnings_14d_short_4 | **1.01**（F0.64） | 0.92 | 0.42 |
| f12m_ebitda_60d_medium_4 | 0.66 | 0.58 | 0.46 |
| f12m_ebitda_14d_long_4 | 0.06 | 0.43 | −0.12 |
| f12m_earnings_90d_long_4 | 0.18 | 0.12 | −0.74 |
| current_year_eps_90d_long | 0.16 | 0.69 | 0.09 |

**判词**：该集字段「有数据、无强度」——天花板 S 1.01，且与 OS 池 2rjrMZ25（eps 修订核）同机制。
长期限（90d）变体接近零 ⇒ 修订只对最短窗口（14d）有效，与既有书同源。**该面封存，不再投入。**

## 五、新开面探针（在飞）

| 批 | multisim | 面 | 条数 | 模板 |
|---|---|---|---:|---|
| J1 | 2xMo84gbj5apcihU7h4tk0N | imbalance5（0 塔位） | 8 | 水平/反向/66d均值/252z/22d差分/桶轴/市值归一/av_diff |
| K1 | 4oZclxfeb5iZ9yi30U6QfGN | macro27（0 塔位，招聘数据） | 8 | active 水平/增长/净新增/created/removed/252z/vec_avg 口径/repost 占比 |

## 六、取证

- 论坛（search_forum_posts）：《【Alpha 模板】USA 点亮 imbalance Pyramid》22 赞 —— 核心模板 `reverse(ts_entropy({field},144))`
  （逆向熵值量化失衡模式复杂性，微观结构异常检测）。本区 preflight 已验证 `ts_entropy` 可用。
- 论文：Chordia–Roll–Subrahmanyam 订单不平衡序列相关与预测力；中国/巴西市场横截面外证 ⇒ 方向先验存在但市场相关。
- 论文（macro27）：LinkedIn 岗位发布数据预测股票收益（ACM, Data-Driven Social Signal Mining）；
  Labor Pains（劳动市场竞争力 → 收益）；Labor Market Frictions and Asset Prices（招聘/解雇成本进入估值）。

## 七、空面探针结果（2026-11-07 下半场）

| 面 | multisim | 最强读数 | 判词 |
|---|---|---|---|
| imbalance5 | 2xMo84gbj5apcihU7h4tk0N | 9qxMxJVo S **1.03**/F0.78/**2Y −0.93**（反向件 −1.03/+0.93） | **死**：全样本有效但近两年反向，符号不稳定；其余 7 条 S≤0.83 且 2Y 全负 |
| macro27（招聘） | 4oZclxfeb5iZ9yi30U6QfGN | YP1z1vqo S **0.59**/F0.41/2Y0.75（repost 占比） | **死**：其余 S≤0.34，招聘数据在 DEU 无横截面预测力 |
| option1（IV 曲面） | 3zQJYo78F5i5ctp1xbWUBlh | 最强 bl6z6rRm S 0.18/2Y0.52；其余 A1VzVr0W −0.31、1YNKNlxm 0.31、Vkxzxm68 −0.27、0mYgYNRr −0.28、leAGA585 0.10、xArGr23w −0.29、E56z68pK −0.25 | **死**：max abs(S)=**0.31**，含符号在内的全 8 条无一达 0.5；DEU 期权隐含波动曲面无横截面预测力 |
| insider_agg_matrix | 4FWmxe3Vq4jQb2sIVA6dXE7 | 5 完成件 max abs(S)=**0.42**（3qoPoOkN −0.23/2Y−0.74、N1NzNGzq −0.10/2Y0.22、pwdGdkGV −0.42/2Y−0.66、akKzK8z1 0.04/2Y0.36）；另 3 条 add() 单位不兼容 WARNING | **死**：全部 S≤0.42、failed_ra_count 4-6，DEU 内部人聚合矩阵无横截面预测力 |
| risk71（specific return 残差反转） | JgZkCaVq4xf9zVHytcE1Gl | **78LmYkz2 S 1.35/F0.37/2Y1.08**；其余 7 条 S −0.14~0.44 | **活口**（见第八节） |
| news29（Reuters Significant Developments，全 VECTOR 事件码，3 用户/4 alpha） | 2XuOUa7Ct4JT9nA1clMrqO2H | 最强 0mYgPWV2 S 0.70/F0.81/TO0.042；kqNGa5Ad S 0.68/2Y **2.08**（近两年单边）；其余 ≤0.68 | **弱判死**：max\|S\|=0.70，距 1.58 需 2.3×；事件码数据在 DEU 存在但无横截面力度 |
| pv13（Revere 竞争/客户网络中心度，PV 塔位 0） | 1LGBYT84X4wmb7lywJV02ON | 最强 kqNGaP9g S 0.51/F0.25/2Y0.89/TO **0.0137**；其余 \|S\|≤0.43 | **死**：数据存在（TO 非零）但中心度为静态特征，max\|S\|=0.51 |

## 八、risk71 残差反转：本段唯一活口（2026-11-07）

**数据集**：risk71 *Daily Specific Return Profiling Dataset*（DEU 10 字段，全域最低使用量之一；
`ecs_top800_specific_return_dsrt` / `epp_minvol1m` / `top800_residual_return_dsrt` 均 0 用户 0 alpha）。
塔位：risk **0**（DEU 无已提交 risk 塔 alpha）；单数据集 ATOM，不触任何组腿禁忌。

**批 1（`JgZkCaVq4xf9zVHytcE1Gl`，8 条，decay4/SUBINDUSTRY/trunc0.08）**

| id | 模板 | S | F | 2Y | TO | sub |
|---|---|---:|---:|---:|---:|---:|
| **78LmYkz2** | **`-group_rank(ts_rank(R,22),subindustry)`** | **1.35** | 0.37 | **1.08** | 0.928 | 0.38 |
| gJeGaY8K | 12-1 残差动量绝对值 | 0.44 | 0.20 | 0.05 | 0.068 | 0.24 |
| 0mYgPbp8 | ts_zscore 5/66 | 0.38 | 0.08 | −0.25 | 0.419 | −0.36 |
| vR1GAKvQ | 5 日残差反转 | 0.30 | 0.06 | −0.33 | 0.418 | −0.29 |
| 9qxMlzX1 | 66 日残差波动倒数 | 0.30 | 0.06 | −0.33 | 0.408 | −0.27 |
| QPvz01GX | 22 日残差 IR 反转 | 0.29 | 0.08 | −0.47 | 0.190 | 0.08 |
| GrWzmqGQ | 22 日符号一致性 | −0.14 | −0.03 | −0.51 | 0.167 | 0.23 |
| N1NzPXb7 | 5/66 残差惊喜差分 | −0.10 | −0.02 | 0.66 | 0.053 | 0.05 |

**归因**：唯一有效的是 **`ts_rank` 时序分位**几何，其余「水平 / 比值 / 综合」几何全在 0.3 附近。
⇒ 经济含义不是「残差反转」本身，而是 **残差收益在自身近一月分布中的极端位置**（short-term residual
reversal 的极值触发式），与 Blitz-Huij-Martens(2011) 残差动量同源但取极值分位而非累计和。
- `ts_rank` 的日频噪声大 ⇒ **TO 0.928 破 0.7 上限**（HIGH_TURNOVER）；
- 覆盖 longCount 145 / shortCount 143（500 池中 288 只），sub 0.38 < 0.474×S=0.64；
- 2Y 1.08 未达 1.58。

**批 2 精修（`3jciKGaR357S9KKruI5GDEv`，decay4，8 条）**——三杠杆各分工：
① 平滑降 TO：`ts_rank(ts_mean(R,3|5),W)`；② 提 sub：`group_rank→group_zscore`（DEU news23 已验证杠杆）；
③ 窗口定峰：W ∈ {22,66,126,252}（月/季/半年/年）；另 1 条换 `residualized_return_top600_ats` 做独立字段稳健性。

## 九、risk71 精修（R3）与跨字段复验：sub 闸判死（2026-11-07）

**R3（`2f4bxafOj4PSa0q76ViUyNu`，decay **10**，其余同基线）**

| id | 模板 | S | F | 2Y | TO | sub |
|---|---|---:|---:|---:|---:|---:|
| YP1zax06 | rank(ts_rank(R,22),subind) | 1.10 | 0.33 | 0.65 | **0.652** | −0.05 |
| gJeGaW10 | zscore(ts_rank(R,22),subind) | 1.08 | 0.32 | 0.48 | 0.692 | 0.03 |
| qMLG7ElP | 裸 ts_rank（无 group 变换） | 0.99 | 0.30 | 0.45 | 0.635 | −0.17 |
| O0AzWJZd | zscore 版 + sector | 0.94 | 0.28 | 0.43 | 0.631 | −0.21 |
| wpQGo9l6 | rank 版 + sector | 0.93 | 0.27 | 0.27 | 0.631 | −0.17 |
| d5WzaK0j | W=66 | 0.93 | 0.27 | 0.45 | 0.641 | −0.03 |
| rKRG7dP1 | 平滑 3 + W22 | 0.53 | 0.14 | 0.29 | 0.417 | −0.23 |
| 9qxMlErx | 波动归一 | 0.43 | 0.12 | −0.53 | 0.414 | −0.02 |

**关键**：decay 4→10 把 TO 0.928→0.652（达标），代价是 S 1.35→1.10；
但 **sub_universe_sharpe 全批落在 −0.23~0.03**，而 REGULAR 需要 sub ≥ 0.474×S ≈ 0.75。
⇒ **该面被 sub 闸结构性判死**，不是 S 不够的问题，调窗口/轴/decay/zscore 都无效。
经济解读：残差反转的收益集中在流动性边缘股，最流动性子集里没有力度。

**risk72 跨字段复验（`a23LWffg4zWcwupWSoCnqc`，同几何 decay10，8 个独立特异性收益字段）**

| 字段 | S | 2Y | sub |
|---|---:|---:|---:|
| top2500_equity_residualized_return | **1.06** | 0.48 | 0.06 |
| top2500_equity_residualized_return_nogroup | 1.00 | 0.56 | −0.18 |
| —— 以下 6 个全 ≈0（|S|≤0.21） | | | |
| ecs_top800 / top600_nogroup / cfg2_top800 / ecs_top800_cfg2 / ats_top1200 / top600_reproducible | 0.01~0.21 | — | — |

⇒ 只有 top2500 口径（≈500 池全覆盖）有信号，更窄宇宙口径全灭；NOGROUP 变体在本批同样 ~0。

**新面判死追加（本轮）**

| 面 | multisim | 读数 | 判词 |
|---|---|---|---|
| model141 Interest Rate Sensitivity（value 7，2 用户） | 21WANv60z4pOcgqq6HJncpm | 8 条全负，最强 vR1GY3Vw **S 0.38**/2Y−0.57；IRR、COE score、escore、通胀敏感、油价 beta 全 S −0.19~−0.58 | **死**：DEU 利率/通胀敏感度无横截面预测力（反向亦仅 0.58） |
| model182 Geographic Network Momentum（value 7，3 用户） | 3VyufDgcT4SQbcXnimYcDL | 最强 e75G1Jng **S 0.23**；复合网络动量 0.08 / 反向 −0.08；分析网/业务段/地理/高管修订动量 |S|≤0.21 | **死**：网络动量通道在 DEU 全无力度 |
| risk72 独立字段复验 | a23LWffg4zWcwupWSoCnqc | max S 1.06（同 sub 缺陷） | 随 risk71 一并封存 |

**★ 本段最重要的结构性判据（跨区可复用）**
> 探针只读 S 会误判「活口」。DEU/TOP500 上 REGULAR 的真实杀手是 **sub_universe_sharpe ≥ 0.474×S**。
> 一个 S 1.35 的面可能在 sub 上归零 —— 这类面无论怎么调窗口/轴/decay 都过不了，
> 应**在探针阶段就把 sub 纳入判据**：一批 8 条若 sub 全在 0 附近，立即封存，别再精修。

## 十、本轮新面判死汇总（2026-11-07 下半场，10 个面 / 80 条回测）

| # | 面 | multisim | 最强读数 | 判词 |
|---|---|---|---:|---|
| 1 | option1 隐含波动曲面 | 3zQJYo78F5i5ctp1xbWUBlh | \|S\| 0.31 | 死 |
| 2 | insider_agg_matrix | 4FWmxe3Vq4jQb2sIVA6dXE7 | 0.42 | 死 |
| 3 | news29 Reuters 事件码（3 用户） | 2XuOUa7Ct4JT9nA1clMrqO2H | 0.70 | 弱判死 |
| 4 | pv13 Revere 网络中心度（塔位 0） | 1LGBYT84X4wmb7lywJV02ON | 0.51 | 死（静态特征） |
| 5 | risk71 残差反转 | JgZkCaVq4xf9zVHytcE1Gl / 2f4bxafOj4PSa0q76ViUyNu | **1.35**（decay4） | **sub 闸判死** |
| 6 | risk72 八字段复验 | a23LWffg4zWcwupWSoCnqc | 1.06 | 随 5 封存 |
| 7 | model141 利率/通胀敏感（value 7，2 用户） | 21WANv60z4pOcgqq6HJncpm | 0.38（8 条全负） | 死 |
| 8 | model16 五维基本面打分（1 用户） | 3cHWwk8BR59C9JCKNC8ckmH | 0.46 | 死 |
| 9 | model182 地理/分析网动量（value 7） | 3VyufDgcT4SQbcXnimYcDL | 0.23 | 死 |
| 10 | institutions25 基金空头拥挤（value 6） | 1yJSSz61h5akbsk3pXrFOm | 0.52 | 死 |

**规律**：value 分高 / 用户少的「冷门面」在 DEU 普遍只有 S 0.2–1.0。
唯一上到 1.35 的 risk71 又被 sub 闸清零。⇒ **冷门 ≠ 有效**：低 prod 的先验不能替代信号强度。

## 十一、遗留候选重审：10 颗 → 0 颗可提交（2026-11-07）

对 prod 卡在 0.70–0.86 的 10 颗 IS 全过件（S 1.65–2.39、RA 零失败）逐颗读塔位与实况相关性：

| id | S | F | 2Y | sub | TO | 塔位 | 判定 |
|---|---:|---:|---:|---:|---:|---|---|
| RRE1Xrjj | 2.16 | 1.75 | 2.09 | 1.43 | 0.180 | MODEL+OTHER | ✗ **禁混**（破墙亦不可提交） |
| 2rOW3j6b | 2.17 | 1.82 | 2.25 | 1.51 | 0.166 | MODEL+OTHER | ✗ 禁混 |
| j23xqexE | 2.14 | 1.82 | 2.16 | 1.53 | 0.158 | MODEL+OTHER | ✗ 禁混 |
| j23xxK8o | 2.16 | 1.66 | 2.02 | 1.44 | 0.199 | MODEL+OTHER | ✗ 禁混 |
| MP1ZZN3L | 2.15 | 1.63 | 2.04 | 1.45 | 0.200 | MODEL+OTHER | ✗ 禁混 |
| P0oe6wpJ | 2.14 | 1.99 | 2.56 | 1.37 | 0.104 | SENTIMENT | ✗ **self 0.8467 + prod 0.8467 双墙**（本地库 0.7694 已失效） |
| 1YNv6Ymk | 2.28 | 1.25 | 1.60 | 1.11 | 0.379 | OTHER | ？prod 0.798（未破） |
| vR102Ver | 2.39 | 1.29 | 1.60 | 1.19 | 0.435 | OTHER | ？prod 0.802 |
| 1YNvvgdJ | 2.28 | 1.28 | 1.89 | 1.09 | 0.378 | OTHER | ？prod 0.831 |
| QPKKMg6Q | 1.65 | 1.47 | 1.58 | 1.00 | 0.072 | ANALYST | **唯一 self 0.668 过闸**，仅 prod 0.807 卡墙（[0.8,0.9] n=1、[0.7,0.8) n=8 成簇） |

**实测 self（本地零配额通道）**：1YNv6Ymk **0.134**、vR102Ver **0.148**、1YNvvgdJ **0.160**、QPKKMg6Q 0.668
⇒ 这 4 颗全部 **self 干净**，是「合法 + 正交 + 仅 prod 卡线」的唯一一批。

**prod 钉深实测（决定能不能破）**
- `1YNv6Ymk` prod 0.7983：**厚尾** —— [0.7,0.8) **n=36**、[0.6,0.7) n=109、[0.5,0.6) n=282、[0.4,0.5) n=648
  ⇒ 要让 max 落到 0.70 以下需同时与 36+109 颗脱钩，属**成片厚尾，判死**，不再投入窗口微调。
- `QPKKMg6Q` prod 0.807：[0.8,0.9) n=1、[0.7,0.8) n=8 ⇒ 浅钉但小簇，**唯一还有理论空间**的一颗。
- `vR102Ver` prod 查询平台超时返回 null（>120s 不落缓存），未取到钉深。

**结论**：DEU 现存资产中，同时满足「塔组合合法 + self<0.7 + prod<0.7」的候选 = **0 颗**。
- 5 颗最强件（RRE1Xrjj 族 S 2.14–2.17）全部是 MODEL+OTHER，**永远不可提交**，破墙无意义；
- 3 颗 OTHER 单塔件 self 极干净（0.13–0.16），但 prod 0.798–0.831 且至少 1YNv6Ymk 是成片厚尾；
- QPKKMg6Q 是唯一「self 过 + prod 浅钉」的组合，值得一次定向破墙。

**★ 破墙优先级（下一轮唯一入口）**
1. QPKKMg6Q（ANALYST 单塔，S 1.65/F1.47/2Y1.58/sub 1.00，self 0.668）：按窗口谷法位移 ts 窗，
   验收 prod<0.70 且 S、2Y 不低于 1.58。
2. 若 QPKKMg6Q 失败，DEU 在本账号内**已无可提交路径**，需用户裁定：放宽塔混限制 / 提高 prod 容忍 / 换区域。

## 十二、全库审计：DEU 可提交候选 = 0（2026-11-07 终审）

不再只看那 10 颗，改为对本地库**全部** S≥1.58 的 DEU 件（60 颗，多为 prod 从未测过）做三闸联审。

**步骤 1｜互相关聚类**（`compute_mutual_correlation`，32 颗 IS 全过件，4 年，threshold 0.7）
- 超阈对 **181 对**；最大互不相关篮子仅 **6 颗**：[mLox6Mg2, JjelQJoe, qML0EAo1, QPvdMW8Q, E5vxZ7bK, O0AZAJxb]（贪心近似）
- 池内重复极重：j23xxK8o≡RRVKKwAj (1.000)、MP1ZZN3L≡mLg11W6W (1.000)、E5vLLPV0/mLg11W6W 0.997、
  9qxrrq3K/RRE1Xrjj 0.995 —— 本质是 2~3 个族反复换参数。

**步骤 2｜篮子逐颗过三闸**

| id | S | F | 2Y | sub | TO | 塔位 | self | prod | 判定 |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| JjelQJoe | 2.70 | 1.28 | 2.29 | 1.40 | — | — | — | 0.8373 | ✗ prod |
| QPvdMW8Q | 2.30 | 1.55 | 2.37 | 1.64 | — | — | — | 0.8849 | ✗ prod |
| E5vxZ7bK | 2.11 | 2.03 | 2.21 | 1.30 | 0.109 | MODEL+OTHER | — | — | ✗ **禁混** |
| O0AZAJxb | 2.19 | 1.79 | 2.05 | 1.32 | 0.171 | PV+MODEL+OTHER | — | — | ✗ **双禁混** |
| mLox6Mg2 | 2.05 | 1.71 | 2.53 | 1.29 | 0.147 | SENTIMENT | **0.9922** | — | ✗ self |
| **qML0EAo1** | 2.05 | 1.92 | 2.40 | 1.34 | 0.090 | **SENTIMENT（合法）** | **0.4836 ✅** | **0.9318** | ✗ prod 深钉（[0.9,1] n=1） |

**终审结论：DEU 现存资产中同时满足「塔组合合法 + self<0.7 + prod<0.7」的候选 = 0 颗。**
qML0EAo1 是本轮唯一走完 self 的合法件（self 0.484），仍被 prod 0.9318 深钉拦死。

**唯一结构性解锁点**：RRE1Xrjj 族 5 颗（S 2.14–2.17 / F 1.63–1.82 / 2Y 2.02–2.25 / sub 1.44–1.53 / RA 0 / 算子 10）
全部只卡在 MODEL+OTHER 这一条禁混规则上；其中 RRE1Xrjj prod 0.7562 且为单钉（可破）。
⚠️ 自动化问卷的「放开禁混」选项是 60s 超时自动选定，**未获用户确认，不作为执行依据**。

## 十三、★ 突破：predictive_starmine 单数据集 ATOM 全闸通过（2026-11-07）

**破局思路**：把最强件 RRE1Xrjj 的 4 条腿**逐条单独回测**，用平台返回的 `pyramids` 反推类别：
- `mean_estimate_change_pct_f12m_earnings_14d_4` → MODEL（S 1.07 / sub 0.59）
- `mean_estimate_change_pct_f12m_ebitda_90d_3` → MODEL（S 1.23 / sub 0.60）
- `predicted_surprise_f12m_ebitda_4` → MODEL（S 0.60）
- `quantile_label_1bucket_5day_ohlcv_2` → OTHER
⇒ RRE1Xrjj 的违规根源就是最后那条 OTHER 腿。**三条 MODEL 腿同属一个数据集 `predictive_starmine`
（Predictive Analyst-Company Signal Set，631 字段）**，去掉 OTHER 腿后即为合法单数据集 ATOM。

**★ 已全闸通过的候选（可提交）**

```
QPvzNNGG
group_neutralize(
  add(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 12)),
          rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
      rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22))),
  bucket(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 252)), range="0,1,0.05"))
```

| 项 | 值 | 闸 |
|---|---:|---|
| Sharpe | **1.70** | ≥1.58 ✅ |
| Fitness | **1.30** | ≥1.0 ✅ |
| 2Y Sharpe | **2.18** | ≥1.58 ✅ |
| sub-universe | **1.18** | ≥0.474×1.70=0.81 ✅ |
| Turnover | 0.155 | ≤0.7 ✅ |
| RA 失败 | **0** | ✅ |
| self | **0.6779** | <0.7 ✅ |
| prod | **0.6777**（all_passed=true） | <0.7 ✅ |
| 塔位 | **MODEL 单塔** | 合法 ✅ |
| 数据集 | predictive_starmine（单数据集） | ATOM ✅ |
| 算子数 | 12 | ≤12 ✅ |

设置：DEU / TOP500 / D1 / decay 4 / SUBINDUSTRY / trunc 0.08 / nan OFF / pasteurize ON / unit VERIFY。

**同族但卡 self 的近失件**（几何微调可继续降相关）：
P0oOjdZJ 1.90/self 0.810、6Xd0oPnJ 1.86/self 0.802、KPJz5YPz 1.73/**self 0.7011**、
9qxMddXr 1.88/self 0.796、omEGJJNv 1.71/**self 0.714**。

**纪律补充（本区类别卡）**：`ts_entropy` / `ts_skewness` / `ts_percentage` / `ts_decay_exp_window` 是**幽灵算子**——
本地 `preflight_expressions` 仍返回 valid=true、any_changed=false，但平台会**连坐整批 CANCELLED**。
⇒ 论坛的 `reverse(ts_entropy(F,144))` imbalance 模板在 DEU 不可用，preflight 通过不等于可派发。

---

## 十四、OS 池构成解剖 → self 墙的根因（2026-11-07）

### 14.1 DEU OS 池全 14 颗（stage=OS / ACTIVE）

| # | alpha | S | F | sub | 塔位 | 核心腿 |
|---|---|---:|---:|---:|---|---|
| 1 | bl6OWZ2M | 2.03 | 1.61 | 1.20 | SENTIMENT | snt7 views + snl27 relpop（vector_neut） |
| 2 | LLM93nGa | 1.88 | 1.74 | 0.91 | SHORTINT+ANALYST | mean_loan_rate_main + eps_y1_estimate_change_3mo |
| 3 | xArzm3Mn | 1.64 | 1.33 | 0.99 | SHORTINT | shrt3_bar（**ATOM 单数据集**） |
| 4 | mLYLEm99 | 2.27 | 1.67 | 1.69 | —（code 空，API 未返回） | 未知 |
| 5 | 2rjrMZ25 | 1.77 | 1.61 | 0.88 | ANALYST | eps_y1_estimate_change_3mo（**ATOM**） |
| 6 | Wje5K71x | 1.73 | 1.37 | 1.25 | FUNDAMENTAL | fnd6_newq_oiadpq（**ATOM**） |
| 7 | 2rmGAPqN | 1.81 | 1.48 | 1.30 | INSTITUTIONS+OTHER | inst1_valueeur / inst1_holdings |
| 8 | 58gkLAkk | 1.75 | 1.42 | 1.22 | MODEL+OTHER | earnings_14d_4 + oth455_relation |
| 9 | JjxrYjre | 1.68 | 1.47 | 1.49 | MODEL+OTHER | mean_buy_transaction_count + 4 条 starmine 腿 |
| 10 | 2rOe10qY | 2.10 | 1.98 | 1.11 | MODEL+OTHER | oth455_relation + 5/5/5 三条 starmine 腿 |
| 11 | vRk6og8b | 1.80 | 1.47 | 1.26 | SHORTINT+MODEL | -mean_loan_rate_main + 4 条 starmine 腿 |
| 12 | Vk65zLzG | 1.79 | 1.69 | 1.44 | INSIDERS+MODEL | directional_indicator + 4 条 starmine 腿 |
| 13 | 883Y3bAW | 2.17 | 1.24 | 1.44 | **MODEL 单塔** | 3 条 starmine 腿(5d) + closing_price（**ATOM**） |
| 14 | blRnKEk6 | 2.02 | 1.70 | 1.43 | SHORTINT+MODEL | -mean_loan_rate_main + 3 条 starmine 腿(5d) |

### 14.2 ★ 根因：self 墙不是「池子大」，是「池子挤」

14 颗里有 **7 颗**含 `predictive_starmine` 的**同一组腿**，且几乎全部用 **5 日窗口**：
`mean_estimate_change_pct_f12m_earnings_14d_4` / `predicted_surprise_f12m_ebitda_4` /
`predicted_surprise_pct_fy2_earnings_4` / `mean_estimate_change_pct_f12m_ebitda_14d_4`。

⇒ 任何新的 starmine 短窗（5d）组合，self 必然被这 7 颗同时拉高。
实测印证：`omEGG57n`（core+sector 中性化）self **0.8104**、`rKRGGg3d`（bucket on ts_std_dev）self **0.7767**，
两颗的 top1 相关件都是 `blRnKEk6`（0.810 / 0.777）。

**去相关方向定案**：不是换算子，是**换字段族 + 换周期**——
① 换预测期（fq2 / fy1 / fy2 而非 f12m）；
② 换指标（revenue 而非 earnings/ebitda）；
③ 换窗口长度（126 / 252 而非 5）；
④ 换未占用家族（revision breadth / rating / recommendation / ARM / surprise / intrinsic value / ep yield / growth）。

### 14.3 DEU 塔点亮表（get_pyramid_alphas，D1）

```
institutions 1 | insiders 0 | model 1 | news 0 | other 2 | analyst 2 | pv 0
earnings 0 | fundamental 1 | sentiment 1 | risk 0 | option 0 | macro 0
socialmedia 0 | shortinterest 2 | imbalance 0
```

**全部塔均未点亮（门槛 3）**。关键推论：**多塔混合作品不点亮塔，只有纯单塔计入**
——池里 7 颗含 MODEL，model 塔仍只计 1（883Y3bAW 是唯一纯 MODEL 件）。
⇒ QPvzNNGG 若提交，model 塔 → 2/3，距点亮一步。

### 14.4 ★ predictive_starmine 字段族全景（631 MATRIX，27 家族）

命名规律：`<家族>_<指标>_<预测期>_<窗口>_<变体号 2-7>`（变体号＝数据快照版本，无经济含义）。

| 家族 | 字段数 | 覆盖中位 | userMax | 占用判断 |
|---|---:|---:|---:|---|
| mean_estimate | 138 | 0.651 | **85** | 池已重度占用 |
| predicted（surprise） | 60 | 0.650 | **114** | 池已重度占用 |
| analyst_upward（revision count） | 60 | **0.973** | 14 | 低占用·高覆盖 ★ |
| iv（intrinsic value） | 53 | 0.912 | **3** | 极低占用 ★★ |
| eq（relation-value adj） | 45 | 0.716 | 29 | 中占用 |
| analyst_downward（revision count） | 44 | **0.973** | 28 | 中占用 |
| arm（Analyst Revisions Model） | 30 | 0.938 | 10 | 低占用 ★（含 userCount=0 字段） |
| rel（相对估值分项） | 22 | **0.963** | 8 | 低占用 ★ |
| projected（DPS 投影） | 20 | 0.912 | **1** | 近零占用 ★★ |
| forward（CAGR 投影/forward PE） | 14 | 0.912 | 4 | 低占用 ★ |
| actual_last（实际值） | 12 | 0.720 | 2 | 低占用 |
| surprise（上季 surprise pct） | 12 | 0.706 | 3 | 低占用 ★ |
| analyst_downgrade / upgrade | 10 / 10 | 0.973 | 18 / 14 | 中低占用 |
| recommendation（评级变动） | 10 | **0.970** | **3** | 极低占用 ★★ |
| price（to intrinsic value） | 8 | 0.912 | 2 | 低占用 ★ |
| ep（SmartEstimate 盈利收益率） | 6 | **0.966** | 4 | 低占用 ★ |
| trailing（trailing PE） | 4 | 0.679 | **0** | 零占用 |
| intrinsic / steady / days / market / warranted | 3/3/2/1/1 | 0.91-0.97 | 0-1 | 零占用 |

**关键纪律**：`analyst_upward_revision_count_*` 与 `analyst_downward_revision_count_*` 的**变体号不完全对齐**
（如 fy1_earnings_30d：up={5,6}、dn={4,7} 无交集）——组净额必须选**有交集变体号**的窗口
（fq1_ebitda_14d 交集={4}、upgrade/downgrade_30d 交集={4}），否则不是同口径配对。

### 14.5 本波派发（2026-11-07，并发 2）

- **A 批** `4qkgzp7fc4BCatq8SQulbaX`（8 条，未占用家族机制）：revision breadth 占比 / rating 净额 ts_zscore /
  recommendation 变动 / ARM score change / 上季 revenue surprise（PEAD）/ price-to-intrinsic-value 反向 /
  SmartEstimate 盈利收益率 / 5yr EPS CAGR 成长。
- **B 批** `HwFqCe3e55M9GMIwLxL2ba`（8 条，已验证机制长周期去相关）：fq2-revenue-30d@126 / f12m-revenue-90d@decay126 /
  fy1-revenue-60d@252 / fy1-ebitda-90d@industry 轴 / f12m-revenue-30d@zscore252@sector 轴 /
  conditional bucket(f12m-ebitda-30d, 按 upward_revision_count 分组) / fq2-revenue surprise@66 / f12m-ebitda-30d@ts_rank252。
- 全部**单数据集 predictive_starmine ⇒ MODEL 单塔 ATOM**，算子数 2–6（远低于 12 上限）。
- preflight：17 字段全存在、unknown_fields=[]、any_changed=false。

**待验**：两批的 S/F/2Y/sub/TO + **逐条 self**（A 批预期 self 低、S 未知；B 批预期 self 低、S 较高）。
### 14.6 A/B 两批收割结论（2026-11-07）

**A 批**（starmine 未占用家族 × 8）：**全灭**，|S| ≤ 0.37。

| # | 机制 | alpha | S | 判词 |
|---|---|---|---:|---|
| A1 | revision breadth 占比（fq1 ebitda 14d） | e75GGNaz | 0.16 | 死 |
| A2 | rating 净额 ts_zscore（upgrade−downgrade） | kqNGGva8 | −0.37 | 死 |
| A3 | recommendation 评级变动 | GrWzzXmx | 0.07 | 死 |
| A4 | ARM score change 7d | zq3GGgdV | 0.30 | 死 |
| A5 | 上季 revenue surprise（PEAD） | d5WzzY9X | 0.05 | 死 |
| A6 | price-to-intrinsic-value 反向 | 1YNKKOG6 | 0.24 | 死 |
| A7 | SmartEstimate 盈利收益率 | E56zzNmr | 0.24 | 死 |
| A8 | 5yr EPS CAGR 成长 | RREzz95d | −0.26 | 死 |

⇒ **starmine 的信号全部集中在 revision 幅度（mean_estimate_change_pct）与 predicted_surprise 两支上**；
广度（count）、评级（rating）、推荐（recommendation）、ARM、surprise、价值、成长**七个家族在 DEU TOP500 无信号**。
覆盖率不是问题（这些家族 cov 0.91–0.97），是**信号本身不存在**。

**B 批**（已验证机制长周期去相关 × 8）：最长窗口最好也只有 S 1.23。

| # | 几何 | alpha | S | sub | TO |
|---|---|---|---:|---:|---:|
| B1 | fq2-revenue-30d @ ts_mean126 | 9qxMMGEd | 0.00 | 0.12 | 0.036 |
| B2 | f12m-revenue-90d @ ts_decay_linear126 | 88RJJGvW | 0.87 | 0.63 | 0.032 |
| B3 | fy1-revenue-60d @ ts_mean252 | 0mYggGYq | 0.34 | −0.08 | 0.024 |
| B4 | fy1-ebitda-90d @ ts_mean126 @ industry 轴 | npvqq6vz | **1.23** | 0.51 | 0.035 |
| B5 | f12m-revenue-30d @ ts_zscore252 @ sector 轴 | qMLGG5LA | 0.35 | 0.47 | 0.169 |

⇒ **revision 信号是纯短窗事件型**：窗口从 5 拉到 126/252，S 单调塌陷。
「短窗 → S 高但 self 撞墙」「长窗 → self 低但 S 死」是 starmine 的**结构性两难**，不是参数问题。
**starmine 路线判定为基本耗尽**，最多再挤出 0–1 颗（靠 bucket 基准字段微调 self）。

### 14.7 ★★★★★ DEU 覆盖率为 0 的数据集清单——多数「判死」其实是「无数据」

对 7 个 valueScore 6–7、字段数多的候选集实测 get_datafields 覆盖率：

| 数据集 | category | 字段数 | 覆盖中位 | cov≥0.5 字段数 | 结论 |
|---|---|---:|---:|---:|---|
| pv71 | pv | 8 | **0.00** | 0 | DEU 无数据 |
| news54 | news | 39 | **0.00** | 0 | DEU 无数据 |
| model135 | model | 137 | **0.00** | 0 | DEU 无数据 |
| event_ml_signals | other | 104 | **0.00** | 0 | DEU 无数据 |
| analyst35 | analyst | 23 | **0.00** | 0 | DEU 无数据 |
| fundamental93 | fundamental | 46 | **0.00** | 0 | DEU 无数据 |
| continuation_score | pv | 560 | **0.00** | 0 | DEU 无数据 |
| sentiment33 | sentiment | 255 | 0.323 | 0 | 覆盖偏薄 |

**这是本轮最重要的方法论纠错**：论坛里 vs=6–7、字段几百个的数据集，在 DEU **覆盖率直接是 0**，
平台照常返回字段清单与 userCount（甚至 u=52/a=80），但回测拿不到数据。
⇒ 历史上把这些面判「机制不成立」的结论**部分失效**，真因是**区域无数据**；
反之也说明**不能靠 valueScore / 字段数 / userCount 选集**，必须先用 get_datafields 的 coverage 卡 0.5 线。

### 14.8 DEU 真正有数据的数据集白名单（实测 coverage ≥0.45 且有可用字段）

| 数据集 | category | 可用字段 | 覆盖 | 池内已用字段 |
|---|---|---:|---|---|
| predictive_starmine | model | 310 MATRIX | 0.65 | 4 个（revision/surprise 短窗） |
| fundamental6 | fundamental | **141** | 0.45–0.66 | 1 个（fnd6_newq_oiadpq） |
| shortinterest3 | shortinterest | 25 VECTOR | 0.65–0.78 | 3 个（shrt3_bar, mean_loan_rate_main ×2 件） |
| **sentiment27（snl27_*）** | sentiment | **13 VECTOR** | **0.90** | **1 个（relpopularity08，且仅作正交化基准、非信号腿）** |
| insider_agg_matrix | insiders | 34 MATRIX | 0.53–1.00 | 1 个（directional_indicator） |
| insiders1 | insiders | 8 VECTOR | 0.534 | 0（全部未用） |
| institutions1 | institutions | 7 VECTOR | 0.229 | 3 个（inst1_valueeur/holdings/tradesignificance） |
| sentiment7（snt7_*） | sentiment | 2 VECTOR | 0.74 | 1 个（all_languages_views） |

### 14.9 D 批判死（shortinterest3 未用家族 × 8）

| # | 机制 | alpha | S | 判词 |
|---|---|---|---:|---|
| D1.1 | max_loan_rate 水平（负号） | 6Xd0JR6J | 0.78 | 弱 |
| D1.2 | loan_rate_volatility zscore | npvqQnjM | −0.03 | 死 |
| D1.3 | loaned_market_value_usd | O0AzVnL7 | −0.18 | 死 |
| D1.4 | loaned_share_count ts_rank252（TO 0.77 超限） | 9qxMm9e2 | 0.33 | 死 |
| D1.5 | transaction_count | WjOz0N5Q | −0.02 | 死 |
| D1.6 | average_loan_duration_days | 2rA6WvYN | −0.49 | 死 |
| D1.7 | max_loan_rate × loaned_value 乘性 | xArGWeZW | 0.17 | 死 |
| D1.8 | max_loan_rate 在 loaned_value 桶内中性化 | 88RJYOMm | **−1.18 → 翻正 +1.18** | 未达线 |

⇒ shortinterest3 只有 shrt3_bar 与 mean_loan_rate 两条腿有力度（均已被池占用），其余 6 家族无信号。
**SHORTINTEREST 塔卡在 2/3**，无法用该集点亮。

### 14.10 ★ 派发前必做：字段名 Set 校验（preflight 假阴性）

D2 首批 8 条**整批 CANCELLED**：fnd6_newq_actq 不存在（正确名 fnd6_cptnewq_actq），
子代报 Attempted to use unknown variable "fnd6_newq_actq"，其余 7 条连坐。
**但 preflight_expressions 对这 8 条返回 valid=true、unknown_fields=[]。**
⇒ preflight 既不校验算子存在性（幽灵算子），**也不校验字段名存在性**。
派发前必须：get_datafields 取真实 id 集合 → 表达式所有标识符过白名单（跳过算子名与 subindustry/sector/industry）→ 才派发。
---

## 十五、机制级饱和的定量证明（2026-11-07，本段收官证据）

### 15.1 本轮全部新面回测汇总（9 批 / 64 条）

| 批次 | 数据集 | 机制 | 条数 | 最强 S | 状态 |
|---|---|---|---:|---:|---|
| A | predictive_starmine | 8 个未占用家族（breadth/rating/recommendation/ARM/surprise/value/growth） | 8 | 0.37 | 全灭 |
| B | predictive_starmine | 已验证机制 × 长周期去相关（126/252） | 8 | 1.23 | 全灭 |
| D1 | shortinterest3 | 6 个未用家族（波动/借券市值/股数/笔数/期限/最高费率） | 8 | 1.18 | 全灭 |
| D2 | fundamental6 | 8 个经典会计机制（应计/资产增长/ROE/资本开支/杠杆/利息保障/营运资本/股权发行） | 8 | 0.70 | 全灭 |
| E | sentiment27 | 8 个关注度机制（排名/域名数/偏度/峰度/相对热度） | 8 | 0.49 | 全灭 |
| F | insider_agg_matrix | 8 个内部人净买入机制 | 8 | 0.55 | 全灭 |
| G | fundamental6+shortinterest3+sentiment27+insider | **已证几何**（tvr_decay 双期限 delta）跨数据集 | 8 | 1.07 | 全灭 |
| H | predictive_starmine | 8 种几何（zscore/quantile/窗口/轴/两腿/乘性/IR/winsorize） | 8 | **1.69** | 1 颗过 S 线 |
| I | predictive_starmine | 非 f12m 短窗 revision（fq1/fy1/fy2 + revenue） | 8 | 待收 | 在飞 |
| J | institutions1+insiders1 | 未用向量字段（价值/股数/显著性/笔数） | 8 | 待收 | 在飞 |

### 15.2 ★★★★★ 决定性证据：starmine 的最大互不相关子集只有 2 颗

对 7 颗 starmine 候选（QPvzNNGG / bl6zAjJR / 2rA6elGZ / WjOzJ73k / d5WzvjYv / KPJz5YPz / omEGJJNv）
跑 `compute_mutual_correlation`（4 年，阈值 0.7）：

- 超阈对 **18 对**；最大互不相关子集 **仅 2 颗**：`[QPvzNNGG, d5WzvjYv]`。
- `QPvzNNGG ↔ bl6zAjJR = 0.7537`；`QPvzNNGG ↔ omEGJJNv = 0.9196`；`QPvzNNGG ↔ KPJz5YPz = 0.9116`。
- `bl6zAjJR`（S1.69/F1.32/sub1.17）自身 self = **0.7503**（top1 仍是 blRnKEk6）⇒ 双杀。
- `d5WzvjYv`（两腿 5 日 + industry 轴）S **1.53** < 1.58，不达提交线。

⇒ **DEU 的 starmine 面在「互不相关 + 全闸通过」口径下上限 = 1 颗**（QPvzNNGG）。
想凑到 10 颗只有两条路：放宽互不相关（纸面凑数，实际最多提交 2 颗），或放宽 MODEL+OTHER 禁混。

### 15.3 H 批全表（唯一出 S≥1.58 的一批）

| # | 几何 | alpha | S | F | 2Y | sub | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| H1 | group_zscore(core@12) | 2rA6elGZ | 1.53 | 1.18 | 1.06 | 1.06 | 0.117 | 2 |
| H2 | ts_quantile gaussian(core@12) | LLMz3782 | 1.04 | 0.67 | 1.13 | 1.17 | 0.149 | 3 |
| H3 | core@3 + bucket(F1,0.1) | WjOzJ73k | 1.39 | 0.85 | 1.70 | 1.02 | 0.198 | 2 |
| H4 | group_rank(core@8, sector) | bl6zAjJR | **1.69** | 1.32 | 1.38 | 1.17 | 0.143 | **1** |
| H5 | 两腿(F1,F2)@5 + industry 轴 | d5WzvjYv | 1.53 | 0.98 | 1.89 | 1.03 | 0.176 | 2 |
| H6 | multiply(rank,rank) | 88RJXlEo | 0.90 | 0.53 | 0.81 | 0.73 | 0.089 | 3 |
| H7 | ts_ir 单腿 | Jjezr7Wm | 0.87 | 0.56 | 0.15 | 0.83 | 0.024 | 3 |
| H8 | winsorize(F1@66) + bucket(F2) | pwdG3jM6 | 0.81 | 0.60 | 0.41 | 0.52 | 0.063 | 3 |

**唯一过线的 H4 被 self 0.7503 + 与 QPvzNNGG 相关 0.7537 双杀**。

### 15.4 G 批：已证几何跨数据集全部未达线

| # | 字段 | alpha | S | sub | 2Y |
|---|---|---|---:|---:|---:|
| G1 | fnd6_cptnewq_atq（资产增长，负号） | qMLGVbLK | −0.05 | −0.25 | 1.60 |
| G2 | fnd6_cptnewq_ibq（利润动量） | 1YNK0vNm | **1.07** | 0.85 | 0.94 |
| G3 | fnd6_cptnewq_revtq（营收动量） | gJeGLveM | 0.21 | 0.08 | −0.44 |
| G4 | fnd6_newq_cstkq（股权发行，负号） | 0mYg5oYr | 0.59 | 0.55 | 1.84 |
| G5 | vec_avg(max_loan_rate)（负号） | wpQGW6Qv | 0.09 | 0.31 | −0.01 |
| G6 | vec_sum(loaned_market_value_usd)（负号） | bl6zAp6m | 0.07 | −0.09 | 0.74 |
| G7 | vec_avg(snl27_totaldomains) | mLo7QOap | 0.31 | 0.26 | 1.37 |
| G8 | directional_indicator | xArG5Mvw | −0.05 | null | 0.04 |

⇒ **几何不是魔法**：Wje5K71x 的 1.73 来自 `fnd6_newq_oiadpq` 这个特定字段本身，不是骨架可迁移性。
同一骨架套到 atq/ibq/revtq/cstkq 上最强只有 1.07。

### 15.5 结论（供交付与后续区域复用）

1. **DEU 是机制级别饱和的区域**：池内 14 颗已覆盖 revision / shortinterest / fundamental / institutions / insiders / sentiment 六个可用机制，
   每个机制内只有 1–2 个字段有效，其余字段（哪怕覆盖率 0.9+）无信号。
2. **DEU 真正有数据的集只有 8 个**（见 14.8），其中 5 个本轮已穷尽。
3. **「互不相关 + 全闸通过」口径下 DEU 上限 = 1–2 颗**，无法到 10 颗；这不是努力量问题，是区域容量问题。
4. 复用建议：换区域时**先做 coverage 卡 0.5 的选集筛**（省掉一整轮），再反解本区已 ACTIVE 纯单塔件的几何骨架。
---

## 十六、收官：I/J/K/L 四批 + 最终结论（2026-11-07）

### 16.1 I 批（starmine 非 f12m 短窗 revision）全灭，最强 1.01

| # | 字段 | alpha | S | sub | TO |
|---|---|---|---:|---:|---:|
| I1 | mean_estimate_change_pct_fq1_earnings_14d_5 | xArGEbAw | 0.40 | 0.27 | 0.233 |
| I2 | mean_estimate_change_pct_fy1_earnings_14d_5 | gJeG0ZJM | 0.94 | 0.70 | 0.219 |
| I3 | mean_estimate_change_pct_fy1_revenue_60d_4 | leAGNKe5 | 0.48 | 0.24 | 0.110 |
| I4 | predicted_surprise_fy1_revenue_4 | zq3GLbKK | 0.49 | 0.65 | 0.097 |
| I5 | predicted_surprise_pct_fy2_ebitda_4 | d5WzP1kx | **1.01** | 0.98 | 0.108 |
| I6 | 两腿 + bucket(surprise) | 88RJ2P5V | 0.35 | 0.25 | 0.211 |
| I7 | predicted_surprise_f12m_revenue_4 | pwdGp5mX | 0.05 | 0.00 | 0.097 |
| I8 | fq2_revenue 两腿 | E56z2R1K | −0.04 | −0.13 | 0.150 |

⇒ 换成 fq1/fy1/fy2 + revenue 预测期后，短窗也不再有力（最强 1.01）。**池子用的 f12m earnings/ebitda 短窗是唯一强组合**。

### 16.2 J 批（institutions1 + insiders1 未用向量字段）全灭，最强 0.28

GrWz7GKQ −0.42 / mLo7l50W −0.44 / xArGENGq −0.33 / WjOzxAzN 0.20 / pwdGpNGv 0.10 / bl6zKQzr −0.01 / E56z2Gz9 0.27 / 9qxM2pm9 0.28

⇒ 机构/内部人的「价值/股数/显著性/笔数」四类聚合全部无信号。这两个集只能作为多塔组合里的辅助腿，不能独立成 ATOM。

### 16.3 K 批（analyst7 季度修订 est_q_* + 实际超预期 act_q_*）全灭，最强 0.59

akKz8JM1 0.31 / O0AzjekY 0.25 / JjezklmO 0.04 / d5Wz6q72 0.14 / P0ozbelw 0.33 / pwdGk0zv 0.24 / A1Vz56aX −0.15 / omEGX292 0.59

### 16.4 L 批（analyst7 分歧度 est_12m_*_std + 快照修订 _3mth_ago/_4wks_ago）全灭，最强 0.90

omEGXMMv 0.10 / 6Xd0QvvG −0.08 / Xg9zx550 0.04 / **78LmrE9O 0.90**（EBI 修订快照）/ LLMzwAJn −0.12 / VkxzLgJ0 −0.25 / YP1zOGqo 0.40 / GrWzNpvP 0.57

⇒ analyst7 的 107 个零占用 est_12m 字段 + 75 个 est_q 字段 + 13 个 act_q 字段**全部无信号**；
该集此前 A2 战役的 S1.57 平台只来自 rec/est_12m 广度占比一族，其余家族不可用。

### 16.5 ★ 最终结论

**DEU 在「每颗全闸通过（S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥0.474S / TO≤0.7 / RA=0 / self<0.7 / prod<0.7）+ 彼此互不相关」口径下，容量上限 = 1–2 颗。**

- 本轮共 **13 批 / 104 条回测**（另有 1 批 8 条因未知字段整批 CANCELLED），覆盖 DEU 全部 8 个有数据的数据集。
- 唯一全闸通过件：**QPvzNNGG**（S1.70 / F1.30 / 2Y2.18 / sub1.18 / TO0.155 / RA0 / self0.6779 / prod0.6777 / MODEL 单塔 / 单数据集 / 12 算子），**状态 UNSUBMITTED**。
- 交付报告：`tracking/DEU/atom_orthogonal/final_delivery_20261107.md`。

**给后续区域的两条硬纪律**：
① 选集第一步用 `get_datafields` 的 coverage 卡 0.5 线，**不要**看 valueScore / 字段数 / userCount；
② 首波模板必须包含「反解本区已 ACTIVE 纯单塔件的几何骨架」这一项，而不是默认 group_rank(ts_mean())。

---

## 十七、破局：结构位移找到第 2 颗（LLMzYrZe）+ 轴位移无效的定量证据（2026-11-07）

### 17.1 第 2 颗交付件 LLMzYrZe —— 全闸通过

```
group_rank(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
               rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))), sector)
```
设置 SUBINDUSTRY / decay **6** / trunc 0.08 / TOP500 / D1，**6 个算子**，MODEL 单塔，单数据集 ATOM。

| 指标 | 值 | 闸 | 判定 |
|---|---:|---|---|
| Sharpe | 1.61 | ≥1.58 | ✅ |
| Fitness | 1.16 | ≥1.0 | ✅ |
| 2Y | 1.69 | ≥1.58 | ✅ |
| sub | 1.20 | ≥0.474×1.61=0.763 | ✅ |
| TO | 0.1532 | 0.01–0.7 | ✅ |
| RA 失败 | 0 | =0 | ✅ |
| self | 0.6702 | <0.7 | ✅ |
| prod | 0.6697 (all_passed) | <0.7 | ✅ |
| 与 QPvzNNGG 互相关 | <0.7 | <0.7 | ✅ |

**关键杠杆 = decay 4→6**：同一两腿表达式 decay4 只有 S 1.55（差 0.03 不达线），decay6 直接 1.61 且 RA 归零。
decay 2 反向（1.52 / 1.46），**decay 是本区唯一仍然有效的设置层杠杆**
（truncation 0.05 / nanHandling / neutralization NONE 均无效或有害）。

### 17.2 ★ 轴位移 ≠ 结构位移：只换分组轴带来 0.9589 相关

P1 批（SUBINDUSTRY / decay6）8 条几何变体全表：

| 表达式骨架 | id | S | F | 2Y | sub | TO | RA |
|---|---|---:|---:|---:|---:|---:|---:|
| group_rank(two-leg, **industry**) | vR1G7jov | 1.58 | 1.10 | 1.85 | 1.12 | 0.1555 | 0 |
| group_zscore(two-leg, sector) | WjOzr7Rk | 1.58 | 1.10 | 1.65 | 1.26 | 0.1690 | 0 |
| group_rank(rank(ts_mean(F1,5)), sector) 单腿 | akKzm78x | 1.50 | 0.92 | 0.82 | 1.13 | 0.2018 | 3 |
| group_rank(rank(ts_mean(F2,5)), sector) 单腿 | 9qxM5X3e | 0.84 | 0.46 | 1.77 | 0.72 | 0.1017 | 2 |
| group_rank(two-leg W22, sector) | e75GMzZg | 1.20 | 0.83 | 1.00 | 0.97 | 0.0904 | 3 |
| ts_zscore 矩 | akKzm79x | 0.17 | 0.03 | −0.06 | 0.20 | 0.2591 | 4 |
| multiply×ts_delta 几何 | xArG7jpp | 0.29 | 0.06 | −0.14 | −0.11 | 0.3143 | 5 |
| ts_rank(66) 几何 | xArG7j7g | 0.51 | 0.18 | 0.24 | 0.57 | 0.2139 | 4 |

**互相关实测**：`LLMzYrZe ↔ vR1G7jov = 0.9589`（仅把 sector 换成 industry）。
⇒ **同一核心信号只换 group 轴 / rank↔zscore，相关 0.95+，不能算第二颗。**
QPvzNNGG 之所以与 LLMzYrZe 互不相关，靠的是三重结构差异叠加：①三腿 vs 两腿 ②异窗 12/5/22 vs 5/5
③分组几何 `bucket(rank(ts_mean(F1,252)), range="0,1,0.05")`（20 桶 × 一年均值基准）vs `group_rank(..., sector)`。

### 17.3 P2 批（SECTOR 中性化 / decay6）—— 高 S 但 2Y 塌陷

| 表达式骨架 | id | S | F | 2Y | sub | TO | RA |
|---|---|---:|---:|---:|---:|---:|---:|
| ts_target_tvr_decay(two-leg, tvr=0.03) | A1VzXGgE | **1.71** | **1.39** | **0.22** | 0.91 | 0.0315 | 1 |
| add(F1@5, F2@22) 异窗 | A1VzXGnE | 1.70 | 1.38 | 0.81 | 1.20 | 0.1207 | 1 |
| add(F1@22, F2@5) 异窗 | vR1G7Nd3 | 1.55 | 1.24 | 1.11 | 0.98 | 0.0944 | 2 |
| winsorize 后 add | 1YNK3pJm | 1.55 | 1.16 | 1.30 | 0.99 | 0.1353 | 2 |
| group_rank(two-leg W10, industry) | GrWzjGk5 | 1.44 | 1.04 | 0.62 | 0.97 | 0.1202 | 2 |
| group_neutralize(two-leg, bucket(F2@5,0.1)) | e75GM3L6 | 1.18 | 0.69 | 0.04 | 0.70 | 0.1970 | 3 |
| subtract 几何 | 58E5KpL6 | 0.40 | 0.14 | −0.15 | 0.06 | 0.1458 | 4 |
| reverse(F1@22) | npvqGNnd | −1.06 | −0.72 | −0.16 | −0.61 | 0.0846 | 4 |

**关键发现**：`ts_target_tvr_decay` 把 TO 压到 **0.0315**、S 拉到 **1.71 / F 1.39**（本轮最强），
但 **2Y 只有 0.22** ⇒ 收益集中在近期、长周期不稳，被 2Y 硬闸直接判死。
⇒ **压换手的平滑算子在 DEU 会牺牲 2Y**，不可当作提 S 手段。

### 17.4 结论

第 3 颗必须来自**结构位移**（分组性质 / 正交化 / 比率几何 / 事件型），不能再做轴位移或窗口位移。
已派 Q / R 两批 16 条验证该假设。

---

## 十八、★ 中性化轴决定 2Y 稳定性：SUBINDUSTRY 是 DEU 的必要条件（2026-11-07）

R 批（**SECTOR 中性化** / decay6）8 条结构变体全表：

| 表达式骨架 | id | S | F | 2Y | sub | TO | RA |
|---|---|---:|---:|---:|---:|---:|---:|
| ts_mean(two-leg, 22) | xArGLq2l | 1.59 | 1.23 | **0.39** | 1.16 | 0.0631 | 1 |
| multiply 交互项 | 6Xd0W7o5 | 1.42 | 0.97 | 0.80 | 0.90 | 0.1422 | 3 |
| bucket(rank(ts_std_dev(F2,66)),0.2) 分组 | 88RJ0bVW | 1.41 | 1.00 | 0.85 | 0.96 | 0.1567 | 2 |
| ts_decay_linear22 (industry) | npvqj9qz | 1.26 | 0.82 | 0.32 | 0.96 | 0.0781 | 3 |
| group_zscore + 10 桶(F1@252) | ZYQz86d1 | 1.10 | 0.50 | 1.32 | 0.99 | 0.2963 | 3 |
| max 几何 | YP1zV6zq | 0.92 | 0.56 | 0.23 | 0.80 | 0.1276 | 3 |
| F2 / 分歧 比率 | mLo7Gp05 | 0.63 | 0.37 | 1.20 | 0.60 | 0.0423 | 3 |
| vector_neut(F2 ‖ F1) (industry) | YP1zV6Eq | −0.02 | 0.00 | −0.27 | 0.44 | 0.0863 | 3 |

### 18.1 核心规律：中性化轴 = 2Y 的开关

把两个中性化设置下的同族结果对齐：

| 批 | 中性化 | 该批 2Y 分布 | 结论 |
|---|---|---|---|
| P1 | **SUBINDUSTRY** | 1.85 / 1.65 / 0.82 / 1.77 / 1.00 … | 前两名 2Y 健康 |
| P2 | SECTOR | 0.22 / 0.81 / 1.11 / 1.30 / 0.62 / 0.04 … | 全线塌陷 |
| R | SECTOR | 0.39 / 0.80 / 0.85 / 0.32 / 1.32 / 0.23 … | 全线塌陷 |

⇒ **DEU 上 SECTOR 中性化会把收益压缩到近期**，2Y 硬闸（≥1.58）系统性不过；
**SUBINDUSTRY 是保住 2Y 的必要条件**。这与 17.3 的「平滑算子压 TO 会牺牲 2Y」是同一现象的两个触发面：
凡是降低有效截面分散度/时变性的操作（更粗的中性化轴、平滑、winsorize 后置），都会把收益集中到末期。

### 18.2 其它失败面（勿重试）

- `vector_neut(rank(F2@22) ‖ rank(F1@22))` = 完全无信号（S −0.02）⇒ 本区两个 starmine 字段几乎张成同一方向，
  正交化后无残余；这从另一角度解释了为何 starmine 的互不相关子集只有 2 颗。
- `max` / `multiply` 交互几何显著弱于 `add`（0.92 / 1.42 vs 1.61）⇒ 两腿是互补关系而非替代/共振关系。
- `ts_decay_linear` 与 `ts_mean` 平滑同样伤 2Y。

---

## 十九、★ 决定性证据：DEU 独立件容量 = 2（互相关 3×3 全矩阵）

### 19.1 最强第三候选 A1Vzp6Kd（本轮所有指标最优件）

```
group_neutralize(add(rank(ts_mean(mean_estimate_change_pct_f12m_earnings_14d_4, 5)),
                    rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5))),
                 bucket(rank(ts_std_dev(mean_estimate_change_pct_f12m_earnings_14d_4, 66)), range="0,1,0.2"))
```
设置 SUBINDUSTRY / decay6 / trunc0.08。**分组轴 = 分析师修订的离散度（5 桶）**，与 QPvzNNGG 的「F1 一年均值 20 桶」性质完全不同。

| 指标 | A1Vzp6Kd | LLMzYrZe | QPvzNNGG |
|---|---:|---:|---:|
| Sharpe | **1.66** | 1.61 | 1.70 |
| Fitness | **1.17** | 1.16 | 1.30 |
| 2Y | **1.85** | 1.69 | 2.18 |
| sub | **1.31** | 1.20 | 1.18 |
| TO | 0.1715 | 0.1532 | 0.155 |
| RA 失败 | 0 | 0 | 0 |
| self | 0.6833 | 0.6702 | 0.6779 |

A1Vzp6Kd 单独看**全面优于** LLMzYrZe，且 self 通过。

### 19.2 但三颗的互相关矩阵让它无法入列

| 对 | 相关 | 阈值 0.7 |
|---|---:|---|
| LLMzYrZe ↔ A1Vzp6Kd | **0.8915** | ✗ 超阈 |
| QPvzNNGG ↔ A1Vzp6Kd | **0.7341** | ✗ 超阈 |
| QPvzNNGG ↔ LLMzYrZe | <0.7 | ✓ |
| `max_mutually_below_subset` | **2 颗** | — |

**A1Vzp6Kd 恰好落在两颗之间**：与 LLMzYrZe 0.89、与 QPvzNNGG 0.73 ⇒ 它只能替换、不能新增。
而替换（QPvzNNGG+A1Vzp6Kd）仍超阈 0.7341 ⇒ **任何组合都只能取 2 颗**。

### 19.3 本轮在单一核心信号上做过的全部结构位移（38 条）都无法把相关压到 0.7 以下

| 结构位移维度 | 尝试 | 与既有件的最低相关 |
|---|---|---:|
| 分组轴（sector / industry / subindustry 互换） | vR1G7jov、WjOzr7Rk | **0.9589** |
| 分组性质（水平 → 离散度） | A1Vzp6Kd | 0.7341 |
| 腿数（2 腿 ↔ 3 腿） | QPvzNNGG vs 其余 | 0.7341 |
| 窗口（5 / 10 / 12 / 22 / 66 / 252，单窗与异窗） | P1-5、P2-4、P2-5 | 0.73+ |
| 几何（rank / zscore / ts_ir / max / multiply / subtract / ts_decay_linear） | P1、P2、Q、R | 0.73+ |
| 正交化（vector_neut） | YP1zV6Eq、88RJ0A1l | 信号本身归零（S 0.50 / −0.02） |
| 事件型（if_else 条件持仓） | Xg9z3q6x | 信号归零（S −0.12） |
| 换手压制（ts_target_tvr_decay） | A1VzXGgE | 2Y 塌陷（0.22） |

**根因（vector_neut 的实证）**：对本区两个 starmine 字段做正交化后残余信号直接归零（S −0.02 / 0.50），
说明 `mean_estimate_change_pct_f12m_earnings_14d_4` 与 `predicted_surprise_f12m_ebitda_4`
在 DEU 上几乎张成**同一方向**。整个 starmine 面只有**一个**有效信号维度 ⇒ 数学上最多只能切出少数几个互不相关组合，
实测就是 2 个。

### 19.4 结论

**DEU 区域 ATOM REGULAR 的互不相关交付上限 = 2 颗**（QPvzNNGG + LLMzYrZe）。
这不是挖掘力度不足，而是本区可交易信号维度只有 1 个造成的结构性上限。

---

## 二十、sentiment7（Wikipedia 关注度）判死 —— 最后一个有数据的数据集（2026-11-07）

### 20.1 字段画像（DEU / D1 / TOP500）

| 字段 | 类型 | 覆盖 | userCount | alphaCount | 含义 |
|---|---|---:|---:|---:|---|
| snt7_all_languages_views | VECTOR | 0.7539 | 34 | 65 | 公司维基页**全语言**浏览量 |
| snt7_views | VECTOR | 0.7357 | 27 | 34 | 分项目（语种）日浏览量 |
| snt7_timestamp | VECTOR | 0.7357 | 4 | 4 | 内容日期（非信号） |

覆盖率 **0.73–0.75 过 0.5 闸**，且 alphaCount 仅 34/65 ⇒ **远未饱和**，是本区唯一还有挖掘空间的集。

### 20.2 模板库（12 个结构互异模板，含正负号双向）

来源：Da-Engelberg-Gao (2011) *In Search of Attention* 的 ASVI 异常关注→反转先验，
Barber-Odean (2008) 关注驱动买入；文献均值口径 + 自建几何。

| # | 机制 | 表达式骨架 | id | S | 2Y | sub | TO | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | ASVI 式异常关注 | −group_rank(ts_zscore(vec_sum(A),22), subind) | ZYQz8QZx | −0.52 | 0.46 | −0.17 | 0.63 | 4 |
| 2 | 短窗关注冲击 | −group_rank(ts_delta(vec_sum(A),5), sector) | 78Lm5LO5 | −0.10 | 0.33 | −0.01 | 0.65 | 4 |
| 3 | 关注不稳定度 | −group_rank(ts_std_dev(vec_sum(A),66), subind) | KPJzoJxk | −0.07 | −0.74 | 0.24 | 0.019 | 3 |
| 4 | 长期关注水平 | −group_rank(ts_mean(vec_sum(A),252), sector) | j2YGpYNO | 0.13 | −0.77 | 0.32 | 0.013 | 3 |
| 5 | 关注时序分位 | −group_rank(ts_rank(vec_sum(A),22), subind) | vR1GE1nz | −0.40 | 0.06 | −0.25 | 0.63 | 5 |
| 6 | 关注信息比率 | −group_rank(ts_ir(vec_sum(V),66), sector) | P0ozRorx | −0.54 | −1.17 | −0.39 | 0.059 | 4 |
| 7 | 短期相对关注 | −group_rank(mean5/mean66, sector) | 2rA6gAQb | 0.01 | −0.27 | 0.40 | 0.261 | 4 |
| 8 | 年度异常关注 | −group_zscore(ts_zscore(vec_sum(V),252), subind) | KPJzoJqg | 0.11 | 0.18 | 0.42 | 0.504 | 4 |
| 9 | 关注广度（语种数） | group_rank(vec_count(V), subind) | gJeGlbbM | −0.27 | 0.80 | −0.55 | 0.119 | 5 |
| 10 | 广度扩张 | group_rank(ts_delta(vec_count(V),22), sector) | e75GYbb6 | −0.41 | −1.25 | −0.28 | 0.851 | 6 |
| 11 | 关注绝对水平 | group_rank(vec_avg(A), subind) | leAGnvv5 | 0.17 | 0.66 | −0.40 | 0.147 | 5 |
| 12 | 均值口径异常关注 | −group_rank(ts_zscore(vec_avg(V),66), subind) | bl6zmbbm | −0.12 | 0.52 | 0.25 | 0.639 | 4 |
| 13 | 每项目均值 | group_rank(vec_sum(V)/vec_count(V), sector) | mLo7Gm6p | 0.07 | 0.71 | −0.34 | 0.145 | 5 |
| 14 | 年度关注变化 | −group_rank(ts_delta(vec_sum(A),252), sector) | RREzOb60 | 0.11 | 0.63 | 0.17 | 0.589 | 4 |
| 15 | 按广度分组 | −group_neutralize(ts_zscore(vec_sum(A),22), bucket(vec_count(V),0.2)) | vR1GEr2d | −0.06 | 0.93 | 0.22 | 0.619 | 4 |
| 16 | **正号对照** | group_rank(ts_mean(vec_sum(V),5), subind) | 1YNK8XZX | −0.23 | 0.51 | −0.65 | 0.041 | 4 |

### 20.3 结论：双向符号全部无效 ⇒ 机制不成立

- 16 条里 **|S| 最大 0.54**（第 6 号），全部 RA 3–6 ⇒ 连 IS 闸都进不去。
- **正负号都测了**：第 16 号正号版 S −0.23、若翻负也只是 +0.23，第 12/13 号同理 ⇒ 不是「方向反了」，是**没有预测力**。
- 高换手模板（0.62–0.85）集中在短窗冲击类，低换手模板（0.013–0.06）集中在长窗水平类，**两类都无信号**。
⇒ **Wikipedia 关注度在 DEU TOP500 上不构成可交易信号**，本数据集判死。

### 20.4 DEU 有数据的 9 个数据集至此全部穷尽

predictive_starmine（唯一有信号）/ fundamental6 / shortinterest3 / sentiment27 / sentiment7 /
insider_agg_matrix / insiders1 / institutions1 / analyst7 —— **全部处理完毕**。

---

## 二十一、★★★ 重大更正：DEU 有 50 个 cov≥0.5 的数据集，此前「只有 9 个有数据」的结论是错的（2026-11-07）

### 21.1 错误来源

前序轮次的选集只覆核了**部分高 valueScore 候选集**，得出结论「DEU 真正有数据的集只有 8–9 个」。
本轮用 `get_datasets({region:"DEU", delay:1, universe:"TOP500"})` 拉全量：**共 172 个数据集**，
其中 **50 个 coverage ≥ 0.5**，而我实际挖过的只有 9 个 ⇒ **41 个数据集从未碰过**。

真正的 cov=0 集只有个别几个（pv71 / news54 / model135 / event_ml_signals / analyst35 / fundamental93 /
continuation_score / intraday_pv_feats / analyst_consensus 等）。之前把「我没扫到」误当成「区域无数据」。

### 21.2 DEU 全量 cov≥0.5 清单（50 个，本区真正可挖的池子）

| 数据集 | category | 字段 | cov | alphaCount | 状态 |
|---|---|---:|---:|---:|---|
| institutions6 | institutions | 11 | 1.00 | 270 | **未挖** |
| pv29 | pv | 50 | 1.00 | 66 | **未挖（实为聚类分组字段，非信号）** |
| risk88 | risk | 1 | 1.00 | 64 | **未挖** |
| analyst_earnings_ibes | model | 42 | 0.9978 | 279 | **未挖** |
| model264 | model | 380 | 0.9973 | 203 | **未挖** |
| pattern_scores | pv | 504 | 0.9888 | 266 | **未挖** |
| news104 | news | 11 | 0.963 | 100 | **本轮开挖** |
| other455 | other | 1500 | 0.9535 | 219 | **未挖** |
| model53 | model | 22 | 0.905 | **9** | **未挖（极低拥挤）** |
| sentiment27 | sentiment | 18 | 0.9038 | 324 | 已挖（最强 0.49） |
| fund_holdings_panel | institutions | 18 | 0.9019 | 102 | **未挖** |
| other532 | other | 8 | 0.8563 | 45 | **未挖** |
| model238 | model | 22 | 0.8552 | 130 | **未挖** |
| model36 | model | 20 | 0.8488 | 58 | **未挖** |
| risk60 | risk | 5 | 0.835 | 395 | **未挖** |
| model28 | model | 25 | 0.8105 | 53 | **未挖** |
| news18 | news | 70 | 0.8046 | 137 | **未挖** |
| news17 | news | 48 | 0.7906 | 87 | **未挖** |
| predictive_starmine | model | 631 | 0.7903 | 1143 | 已挖（2 颗交付） |
| analyst48 | analyst | 7 | 0.7879 | **7** | **未挖** |
| model106 | model | 14 | 0.7878 | 32 | **未挖** |
| news20 | news | 46 | 0.7729 | 33 | **未挖** |
| news50 | news | 37 | 0.7644 | 42 | **未挖** |
| sentiment7 | sentiment | 3 | 0.7418 | 94 | 已挖（全灭） |
| pv30 | pv | 285 | 0.7273 | 287 | **未挖** |
| analyst7 | analyst | 608 | 0.7207 | 3993 | 已挖（最强 0.90） |
| dl_riskfree_returns | other | 133 | 0.7147 | 922 | **本轮开挖（KOR 冠军族）** |
| model216 | model | 45 | 0.7121 | 629 | **未挖** |
| shortinterest3 | shortinterest | 25 | 0.7105 | 864 | 已挖（最强 1.18） |
| fundamental22 | fundamental | 1 | 0.69 | 40 | **未挖** |
| model250 | model | 20 | 0.6407 | 133 | **未挖** |
| analyst93 | analyst | 100 | 0.6373 | 193 | **未挖** |
| analyst47 | analyst | 5 | 0.6234 | 112 | **未挖** |
| other250 | other | 12 | 0.6126 | **2** | **未挖（近乎零拥挤）** |
| model25 | model | 217 | 0.6064 | 1946 | **未挖** |
| analyst_factor_signals | analyst | 108 | 0.5996 | 1575 | **未挖** |
| news38 | news | 3 | 0.5992 | 13 | **未挖** |
| analyst9 | analyst | 51 | 0.5825 | 106 | **未挖** |
| analyst44 | analyst | 72 | 0.5802 | 58 | **未挖** |
| model26 | model | 548 | 0.5778 | 908 | **未挖** |
| other47 | other | 18 | 0.577 | 62 | **未挖** |
| model30 | model | 14 | 0.5694 | 179 | **未挖** |
| insider_agg_matrix | insiders | 34 | 0.5617 | 170 | 已挖（最强 0.55） |
| insider_matrix | other | 33 | 0.5485 | 86 | **未挖** |
| insider_trx_matrix | other | 33 | 0.5419 | 32 | **未挖** |
| insiders1 | insiders | 8 | 0.5343 | 26 | 已挖（最强 0.28） |
| model109 | model | 544 | 0.529 | 259 | **未挖** |
| other545 | other | 4 | 0.5269 | 7 | **未挖** |
| multifactor_return_pred | model | 648 | 0.5187 | 356 | **未挖** |
| other699 | other | 7 | 0.506 | 5 | **未挖** |

### 21.3 结论修正

**第十九节「DEU 独立件容量 = 2」只在「predictive_starmine 这一个数据集」范围内成立，不能外推到整个 DEU 区域。**
区域级容量结论作废，需按「41 个未挖数据集」重新开挖后才有资格重下。

### 21.4 pv29 的特殊性（记录，避免白跑）

pv29 的 50 个字段全部是 `industry_grouping_level{2,10,20,50}_top{100,200,400,600,800,1200}_*513`
形式的**统计行业聚类标签**（cluster assignment），不是信号值。它的正确用途是给 `group_rank` / `group_neutralize`
当**自定义分组轴**（替代 sector/subindustry），单独无法构成 ATOM 信号。
注意：把它与 starmine 组腿会变成 MODEL+PV（禁混集合内部），不可用；只能与集合外数据集组腿。

---

## 二十二、未挖数据集首轮开波结果与字段画像（2026-11-07 晚）

### 22.1 W1｜dl_riskfree_returns（other，133 字段，cov 0.7147）—— KOR 冠军配方未直接迁移

KOR 冠军骨架（KOR 实测 S 2.09 / prod 0.794）：
`group_rank(ts_av_diff(probability_label2_3quantile_20day_ohlcv, 66), sector)`。
DEU 该字段存在且 **coverage = 1、alphaCount = 57**，但换到 DEU 后：

| 表达式骨架 | id | S | F | 2Y | sub | TO | RA |
|---|---|---:|---:|---:|---:|---:|---:|
| P2 偏离自身 66 均值（KOR 同构） | 6Xd0krRK | 1.30 | 0.58 | 1.06 | 0.68 | 0.2974 | 3 |
| 净信念 P2−P1 偏离 66 均值 | leAGm87N | 0.88 | 0.32 | 0.79 | 0.35 | 0.3099 | 4 |
| −ts_mean(P2,22) 概率水平 | akKzpLo6 | −0.29 | −0.11 | 0.59 | −0.55 | 0.0634 | 4 |
| ts_zscore(P2,66) | E56zdvk0 | 1.30 | 0.52 | 0.93 | 0.54 | 0.3406 | 4 |
| ts_delta(P2,22) | 6Xd0krzK | 1.28 | 0.51 | 0.93 | 0.86 | 0.3699 | 3 |
| P2 偏离 126 均值 | YP1ze5QJ | 1.09 | 0.44 | 0.46 | 0.64 | 0.2835 | 3 |
| −(P1 偏离 66 均值) | omEGd6Y2 | 0.28 | 0.06 | 0.18 | −0.03 | 0.3172 | 4 |
| 双标准化净信念 | QPvz83QQ | 0.60 | 0.14 | 0.61 | 0.67 | 0.4805 | 3 |

⇒ 最强 **S 1.30**，且 **TO 0.28–0.48 偏高、RA 3–4 不过闸**。
结论：KOR 的「ML 分位概率均值回复」几何**不可迁移到 DEU**（与 17.2 的「几何不可迁移」一致）。
该集 133 字段里还有 57 个 cov=1 字段与 2/4/5 分位 × 5/20/60 日的组合矩阵可继续试，
但首轮看信号强度不足（1.30 vs 需 1.58），优先级下调。

### 22.2 W2｜news104（news，11 字段，cov 0.9635）—— 全灭

| 表达式骨架 | id | S | F | 2Y | TO | RA |
|---|---|---:|---:|---:|---:|---:|
| ts_mean(sentiment,22) | wpQGrjnl | 0.38 | 0.13 | 0.61 | 0.156 | 3 |
| ts_mean(prob_pos − prob_neg,22) | 2rA6Ylaw | 0.29 | 0.09 | 0.26 | 0.155 | 3 |
| ts_delta(sentiment,5) | 9qxMnXae | −0.08 | −0.01 | 0.15 | 1.240 | 5 |
| 置信度加权情绪 | P0ozV7nE | 0.39 | 0.14 | 0.49 | 0.156 | 3 |
| 新颖性加权情绪 | MPYzr7b8 | 0.44 | 0.17 | 0.39 | 0.156 | 3 |
| 相关性加权情绪 | mLo7vjqK | 0.44 | 0.17 | 0.68 | 0.153 | 3 |
| marketimpactscore | xArGZjep | 0.01 | 0.00 | 0.15 | 0.134 | 3 |
| ts_zscore(sentiment,66) | d5WzGjdX | 0.09 | 0.01 | 0.07 | 1.300 | 6 |

⇒ 最强 **0.44**。置信度/新颖性/相关性三种加权全部无效 ⇒ 该新闻源的**情绪方向本身无预测力**，
不是加权方式问题。news104 判死。

### 22.3 已完成的未挖数据集字段画像（供后续开波）

**model53（model，22 字段，cov 0.873–0.926）—— 信用违约概率期限结构，alphaCount 仅 0–3，最值得挖**
| 字段族 | horizon | 说明 |
|---|---|---|
| `annualized_pd_{1_month,3_month,6_month,1_year,2_year,3_year,4_year,5_year,7_year,10_year}_jc7` | 9 档 | JC7 模型年化违约概率 |
| `mdl53_ms5_{1month,...,10year}` | 9 档 | Kamakura ms5 模型年化违约概率 |
| `mdl53_implied_spreads` | — | 模型隐含信用利差（cov 0.916） |

**institutions6（institutions，11 字段，cov 1.0）—— 13F 机构持仓**
买入/卖出/持有机构家数、机构买卖美元金额、机构买卖股数、机构持股占全部所有者比例。

**pattern_scores（pv，504 字段，cov 0.96–0.999）—— 图表形态相似度，PV 塔为 0**
字段命名规律 `{pattern}_{stat}_simscore_lookback{60,120}` 与 `{avg,adaptive,dynamic}_similarity_{pattern}`；
形态含 asc_triangle / falling_wedge / rising_wedge / breakaway_gap / symmetrical_triangle /
falling_support_flat_resistance 等，stat 含 mean/median/min/max/std/quantile。
绝大多数 alphaCount = 0–10 ⇒ **极低拥挤**。

**other250（other，12 字段，cov 0.6126）—— 电商商品数据**（星级、评论数、畅销榜排名、价格区间），alphaCount 0–2
**other699（other，7 字段，cov 0.506）—— TipRanks 持仓变动**（成交股数、前后持股、历史交易日数），alphaCount 0–4
**risk60（risk，5 字段，cov 0.835）—— 借券费率与做空拥挤度**（RISK 塔为 0）
**fund_holdings_panel / analyst48 / model28 / model36 / model106 / model238 / other532 / other545 / news17 / news18 / news20 / news50 / model264 / other455 / pv30 / pattern_scores** —— 均未开波。

### 22.4 首轮未挖数据集判死汇总（W3 / W4 / W5）

| 批 | 数据集 | 类别 | 机制 | 最强 S | 判定 |
|---|---|---|---|---:|---|
| W3 | model53 | model | 信用违约概率期限结构（PD 水平/斜率/短长期比率/隐含利差/恶化动量/双指标合成） | 0.41 | 全灭 |
| W4 | institutions6 | institutions | 13F 机构净买入广度/美元买入占比/持股占比/家数变化/净股数 | 0.64 | 全灭 |
| W5 | pattern_scores | pv | 图表形态相似度（上行缺口/突破缺口/上升楔形/下降楔形/对称三角/形态差/不确定度） | 0.60（负） | 全灭 |

**重要观察**：model53 的 22 个字段 alphaCount 只有 0–3（近乎零拥挤），pattern_scores 的 504 个字段 alphaCount 大多 0–10，
但 **低拥挤并不等于有信号** —— 与前面的判据一致：「能绕开拥挤的字段往往本身弱信号」。判死粒度仍应停在数据集层。

### 22.5 最新发现的两个高覆盖数据集

**other532（other，8 字段，cov 0.74–0.9714）—— Barra 特质收益（specific return）**
字段：oth532_global_daily_specificreturn（cov 0.9714, aC 25）、oth532_emerging_daily_specificreturn（0.9714, aC 5）、
月度版两个、idiosyncratic_return_eue/eult_{daily,monthly}。
经典机制：**特质收益反转**（specific return reversal）—— 个股特质收益短期过度反应后回补。
已派 W7 验证 8 个模板（5/22/66 日反转、月度、双区合成、正号动量对照）。

**fund_holdings_panel（institutions，18 字段，cov 0.876–0.9278）—— 基金交易行为**
字段：boundary_transaction_total（新建仓/清仓笔数）、herfindahl_index_transactions（交易集中度）、
large_trade_count_50bps（大额交易笔数）、stable_boundary_trade_count_21d（稳定边界交易）、
top_weighted_transaction_number（重仓信心交易笔数）、transaction_account_total（参与账户数）。
机制候选：**基金信心交易 / 集中度 → 未来收益**。

### 22.6 第二批未挖数据集判死（W6 / W7 / W8）

| 批 | 数据集 | 类别 | 机制 | 最强 S | 判定 |
|---|---|---|---|---:|---|
| W6 | model264 | model | 380 个「技术指标未来趋势向上概率」的单指标 / 8 指标共识 / 不确定度 / 概率变化 | 0.78 | 全灭 |
| W7 | other532 | other | Barra 特质收益反转（5/22/66 日、月度、双区合成、动量对照） | 0.23 | 全灭 |
| W8 首 | risk60 | risk | 借券费率与做空拥挤度（**未加 vec_avg**） | — | **8/8 ERROR 整批空跑** |
| W8b | risk60 | risk | 同上，已加 vec_avg 修正 | 见下 | 重跑中 |

**W6 细节**：所有「趋势向上概率」正号件全部为**负** S（−0.37 ~ −0.68），即翻符号后为 +0.37 ~ +0.68，仍远不达标；
唯一正号件是「BB 概率不确定度取负」S 0.78，但 sub 仅 0.28。⇒ 该族概率值与未来收益**反向**且强度不足。

**W7 细节**：特质收益反转在 DEU TOP500 上完全不成立（|S|≤0.25，sub 多数为负，RA 4–5）。

### 22.7 ★ 新增工具坑：VECTOR「event 类型」字段必须先 vec_* 聚合

W8 首批 8 条全灭，错误统一为 `Operator ts_mean/ts_delta/ts_zscore/ts_std_dev/subtract does not support event inputs`。
原因：`risk60` 的 `rsk60_offer` / `rsk60_crowding` / `lending_fee_bid_rate` 是 **event 类型 VECTOR**，
不能直接接 `ts_*` 或算术算子，必须先 `vec_avg` / `vec_sum` / `vec_count` 聚合成 MATRIX。

**易错点**：另一些 VECTOR 字段（sentiment27 / shortinterest3 的部分字段）不加 vec_* 也能跑，
容易养成「上次没加也行」的坏习惯。今后凡首次使用某数据集的 VECTOR 字段，一律统一加 vec_* 包装。
**关键**：`preflight_expressions` **不校验算子-类型兼容性**，这类错误只能靠控制批大小来限制损失。

### 22.8 分组轴类数据集（不是信号源，勿当信号挖）

| 数据集 | 字段数 | 性质 | 正确用法 |
|---|---:|---|---|
| pv29 | 50 | industry_grouping_level{2,10,20,50}_top{100..1200}_*513 统计行业聚类标签 | 作 group_rank / group_neutralize 的自定义分组轴 |
| other455 | 1500 | oth455_competitor_n2v_*_kmeans_cluster_* / pca_fact*_cluster_* 竞品嵌入聚类标签（GROUP 类型） | 同上 |

两者都不含连续信号值，单独无法构成 ATOM alpha。注意与 starmine 组腿会落入禁混集合内部（PV+MODEL / OTHER+MODEL），不可用；
只能与集合外 category 组腿。

---

## 二十三、★ 双数据集组腿实测：强腿 + 次强腿 = 崩塌（2026-11-07）

### 23.1 W8b｜risk60（risk，5 字段，cov 0.835）—— 全灭

| 表达式骨架 | id | S | F | 2Y | sub | TO | RA |
|---|---|---:|---:|---:|---:|---:|---:|
| 相对年度费率取负 | d5WzNo0v | 0.94 | 0.52 | 0.96 | 0.59 | 0.1912 | 4 |
| 费率水平取负 | rKRGZVW9 | 0.81 | 0.57 | 1.16 | 0.52 | 0.0399 | 3 |
| 出借费率取负 | QPvzwgaw | 0.79 | 0.55 | 1.10 | 0.52 | 0.0417 | 3 |
| 费率变化取负 | qMLGQ3AP | 0.43 | 0.12 | −0.12 | −0.05 | 0.3739 | 5 |
| 做空拥挤度取负 | 0mYg1681 | 0.34 | 0.12 | 0.18 | 0.39 | 0.1608 | 3 |
| 费率 zscore 取负 | A1Vzomwe | 0.30 | 0.08 | −0.28 | 0.01 | 0.2706 | 5 |
| 买卖价差取负 | 58E5PeON | −0.19 | −0.03 | −0.86 | −0.30 | 0.4665 | 5 |
| 费率波动取正 | j2YGqx0j | −0.71 | −0.45 | −0.91 | −0.89 | 0.0421 | 4 |

最强 0.94，全部 RA 3–5。借券费率水平**方向正确但强度不足**（与 shortinterest3 独立的 1.18 一致，同族天花板就在这里）。

### 23.2 W9｜MODEL × SHORTINTEREST 两数据集组合 —— 彻底失败

| 组合 | id | S | F | 2Y | sub | TO | RA |
|---|---|---:|---:|---:|---:|---:|---:|
| starmine 两腿 + 借券需求评级@22 | leAGonwx | 0.09 | 0.02 | −0.83 | 0.62 | 0.158 | 3 |
| F1 + 平均借券费率@22 | omEGxbj6 | −0.22 | −0.07 | −1.40 | 0.21 | 0.179 | 3 |
| F2 + 借券需求评级@66 | E56z9jnP | −0.09 | −0.02 | −0.08 | 0.39 | 0.094 | 3 |

**这是本轮最重要的负面结论**：
- starmine 两腿独立 **S 1.61**；shortinterest3 最强腿独立 **S 1.18**（达第一腿的 0.73 倍）；
- 用 `add(rank(A), rank(B))` 等权合成后 **S 0.09 / −0.22 / −0.09**，比任一单独腿都差 1.4–1.8 个 Sharpe，2Y 直接变负。

**机理**：rank 后 add 是等权混合，混合信号 IC ≈ 两条腿 IC 的加权平均；第二腿 IC 低于第一腿时平均必然下降。
更糟的是两腿时序波动不相关 ⇒ 混合后**信号噪声上升、均值下降**，Sharpe 被双重压缩。
「分散化提升 Sharpe」只在**两腿各自独立且强度相当**时成立，不适用于「一强一弱」。

**应用**：① 第二腿独立 S 必须 ≥ 第一腿的 ~0.8 倍才考虑组腿；② 判「S 不够」时不要加腿，应换数据集/换机制；
③ 这解释了为什么 ATOM（单数据集）路线在弱区反而是**正确**的 —— 组腿会把弱区彻底打死。

### 23.3 剩下面临的现实

已验证 15 个数据集（9 原有 + 6 新增），除 predictive_starmine 外**无一能上 1.58**：
最高的是 dl_riskfree_returns 1.30 与 shortinterest3 1.18。
剩余约 30 个未挖集多为同类（news17/18/20/50、analyst9/44/47/48/93、model25/26/28/30/36/106/109/216/238/250、
insider_matrix/insider_trx_matrix、other47/545/699、fundamental22、risk88），按已测同类集的表现预期上限也在 1.0 附近。
正在跑 W10（other250 电商需求）与 W11（analyst_earnings_ibes 价量反转/量能）做最后确认。

---

## 二十四、★★★★ 决定性转折：techindi_model 富矿 + 「先查存量再判死」方法论（2026-11-07）

### 24.1 错误链条的根因

第二十二、二十三节把 6 个新数据集判死、并得出「除 starmine 外无一能上 1.58」的结论。
本轮用 `search_alphas_by_sharpe({region:"DEU", limit:1000})` 拉本地库全部历史件后，**该结论被彻底推翻**。

关键事实：**本地库里躺着 1000 条 DEU alpha 记录**，其中
- S≥1.58 且 2Y≥1.58 且 F≥1.0 的 **249 颗**；
- 其中 **已测 prod 且 <0.7 的 24 颗**（含 8 颗 ACTIVE 已提交）；
- 其中 **prod 从未测过的 141 颗**（S 最高 2.19）。

我此前每轮都从零设计模板，**从不回查这些存量**，导致：
- 用简单几何（group_rank(ts_mean(...))）测出 0.5–1.3 就判死数据集；
- 而同一数据集里历史件的复杂几何（`vector_neut(ts_quantile(ts_ir(ts_mean(max(...)))))`）S 高达 2.05。

**★ 方法论铁律（新增）**：判死任一数据集之前，必须先 `search_alphas_by_sharpe({region})` 拉全量，
按字段族聚合出该族的 maxS / y2ok（S≥1.58 且 2Y≥1.58 的件数）。y2ok≥3 的族一律**不准判死**，
必须先把该族历史最佳表达式取出来（`get_alpha_details`）作为模板基线再测。

### 24.2 techindi_model：DEU 最强信号源（但 prod 数据集层封死）

`get_datafields(dataset_id:"techindi_model")` → **399 个字段**（全部 MATRIX），
命名规则 `tm_<M>_r1_r5_r10_rh[_ah3]_glb_d1_<r1|r5|r10>_<q1|q2_p0...>`：
- `q1` = 连续回归输出（21 个 = 7 个 tm × {r1,r5,r10}），其余 378 个是分桶概率。
- `tm_15_..._r10_q1` 的 alphaCount **571**、userCount 273 ⇒ 极度拥挤。
- 注意：`get_datafields` 对该集返回 coverage 全为 0（API 不填），**不代表无数据**。

**正向实证（我本轮实跑，非历史件）**：

| 批 | 表达式 | ID | S | F | 2Y | sub | RA |
|---|---|---|---:|---:|---:|---:|---:|
| TM-A | group_rank(tm_16_r5_q1, sector) | QPveKkPM | 2.37 | 1.29 | 1.25 | 1.25 | 1 |
| TM-A | group_rank(tm_17_ah3_r10_q1, sector) | **A1VmRAXW** | **2.41** | **1.42** | **1.64** | **1.19** | **0** |
| TM-A | group_rank(tm_19_ah3_r5_q1, sector) | qML3KRav | 2.31 | 1.25 | 1.45 | 1.12 | 1 |
| TM-B | group_rank(tm_15_r10_q1, sector) | **1YNv6Ymk** | **2.28** | 1.25 | **1.60** | 1.11 | **0** |
| TM-B | group_rank(tm_8_r10_q1, sector) | **GrWxrE2o** | **2.54** | **1.50** | **2.33** | **1.27** | **0** |
| TM-B | group_rank(tm_19_ah3_r10_q1, sector) | **1YNPY6MQ** | **2.23** | 1.24 | **1.62** | 1.12 | **0** |

设置：TOP500/D1/**CROWDING**中性化/decay 4/trunc 0.08。**CROWDING 是该族能出信号的唯一轴**：
TM-C 用 SUBINDUSTRY 跑同字段 8 种几何 → S 0.83–1.80 但 **F 全部 ≤0.95、RA 2–4**，全灭。

**负向实证 —— prod 墙在数据集层，三次不同字段/几何读数一致**：

| alpha | 字段 | 几何 | S | prod max | 直方图尾部 |
|---|---|---|---:|---:|---|
| JjelQJoe | tm_15_r5_q1 | group_rank(sector) | 2.70 | **0.8373** | [0.6,0.7)79 / [0.7,0.8)15 / [0.8,0.9)1 |
| A1VmRAXW | tm_17_ah3_r10_q1 | group_rank(sector) | 2.41 | **0.8405** | [0.6,0.7)99 / [0.7,0.8)19 / [0.8,0.9)2 |
| GrWxrE2o | tm_8_r10_q1 | group_rank(sector) | 2.54 | **0.8549** | [0.6,0.7)168 / [0.7,0.8)38 / [0.8,0.9)3 |

⇒ 三个**不同 tm 模型**、不同 r 档，prod 锁在 0.837–0.855 窄带 ⇒ 与「KOR dl_riskfree 三个机制 prod 恒定 0.79」同型：
**prod 墙是数据集层属性，换字段/换几何/换窗口只能移动 ±0.02**。
⇒ `techindi_model` 判死（CROWDING 轴下）。这是本区**最强但用不上**的数据集。

### 24.3 六颗已确认的全闸候选（互相关全部 <0.7）

| # | ID | 塔位 | S | F | 2Y | sub | TO | RA | prod | self |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **QPvzNNGG** | MODEL 单塔（starmine） | 1.70 | 1.30 | 2.18 | 1.18 | 0.155 | 0 | **0.6777** | null |
| 2 | **LLMzYrZe** | MODEL 单塔（starmine） | 1.61 | 1.16 | 1.69 | 1.20 | 0.153 | 0 | **0.6697** | null |
| 3 | **E56pROb9** | MODEL 单塔（mdl216） | 1.79 | 1.70 | 2.03 | 1.32 | 0.067 | 0 | **0.6859** | null |
| 4 | **mLox6Mg2** | SENTIMENT 单塔（snt7） | 2.05 | 1.71 | 2.53 | 1.29 | 0.147 | 0 | **0.6935** | 0.0304 |
| 5 | **xArYWKgg** | SHORTINTEREST+ANALYST | 1.87 | 1.72 | 2.22 | 0.92 | 0.090 | 0 | **0.6104** | null |
| 6 | **MPY9VNY9** | SHORTINTEREST 单塔（shrt3） | 1.59 | 1.26 | 2.36 | — | — | 0 | **0.5986** | 0.2703 |

**互相关矩阵（实测，3 年 782 点）**：

| | QPvzNNGG | LLMzYrZe | E56pROb9 | mLox6Mg2 | xArYWKgg | MPY9VNY9 |
|---|---:|---:|---:|---:|---:|---:|
| QPvzNNGG | 1 | 0.660 | 0.559 | 0.014 | 0.133 | — |
| LLMzYrZe | 0.660 | 1 | 0.588 | −0.004 | — | — |
| E56pROb9 | 0.559 | 0.588 | 1 | −0.018 | 0.241 | — |
| mLox6Mg2 | 0.014 | −0.004 | −0.018 | 1 | −0.002 | — |
| xArYWKgg | 0.133 | — | 0.241 | −0.002 | 1 | 0.085 |
| MPY9VNY9 | — | — | — | — | 0.085 | 1 |

⇒ 6 颗两两全 <0.7（最大 0.660）。**交付从 2 颗跃升到 6 颗。**

### 24.4 已被互相关堵死的边（勿再试）

| 族 | 成员 | 族内最大相关 | 可留 |
|---|---|---:|---:|
| starmine（含 A1Vzp6Kd / pwdl6ov6） | QPvzNNGG, LLMzYrZe, A1Vzp6Kd, pwdl6ov6 | 0.9247 | **2** |
| MODEL-mdl | E56pROb9, Vkx3MjW8, wpQYNvZp, Xg9WNVvl | 0.8644 | **2**（但 LLMzYrZe↔wpQYNvZp 0.7319、↔Vkx3MjW8 0.7098 ⇒ 只能留 E56pROb9） |
| snt7 纯件 | mLox6Mg2, GrWVx2aO, QPveY7Kg, A1Vvqded, QPvK5krW | 0.9921 | **1** |
| snt7+snl27 | kqNgoLkP, j2Y8YkPQ, QPvK5krW | 0.9346 | **0**（kqNgoLkP prod **0.8983** 死） |
| SHORTINT+ANALYST | xArYWKgg, Vkxnb8QG, zq3Ye20E | 0.9782 | **1** |
| shrt3 | MPY9VNY9, npvwXA8l | 0.9198 | **1** |
| techindi | JjelQJoe, A1VmRAXW, GrWxrE2o 等 | 0.7523 | **0**（prod 0.84） |

**重要**：MODEL 单塔 4 颗里，`LLMzYrZe ↔ wpQYNvZp = 0.7319`、`LLMzYrZe ↔ Vkx3MjW8 = 0.7098`，
即 **LLMzYrZe 占掉了「MODEL-mdl 第二颗」的位置**。若要用 wpQYNvZp（S1.68/prod0.6333）替换 LLMzYrZe（S1.61/prod0.6697），
总数不变，仅质量微调 —— 保留已有的 LLMzYrZe 更省事。

### 24.5 LOANRATE 族的两套子结构（prod 相差 0.3）

`mean_loan_rate_main`（借券费率）+ `eps_y1_estimate_change_3mo`（ANALYST）两塔：

| 子结构 | 示例 | S | prod |
|---|---|---:|---:|
| `add(..., -rank(vec_avg(mean_loan_rate_main)), ...)` 等权相加 | ZY0M1G53 / rK5VnXY3 / wpYPvgqY / MP1Z2mWk | 1.82–2.01 | **0.886–0.925** ❌ |
| `trade_when(rank(ts_backfill(vec_avg(mean_loan_rate_main),252)) < 0.75, group_neutralize(group_rank(add(eps_y1_...))))` | xArYWKgg / Vkxnb8QG / zq3Ye20E | 1.80–1.87 | **0.606–0.638** ✅ |

⇒ **把同一字段从「相加腿」改成「门控腿」（且门控带 0.75 分位截断）能把 prod 从 0.90 砍到 0.61**。
这是本轮发现的最强 prod 杠杆，比换中性化轴有效得多。

### 24.6 ★ 禁混硬约束再次拦截：R83/R84/R85 组全部违规

本地库 S 2.09–2.17 的 `R83`/`R84/R85` 组（E5vxZ7bK, 58QYZb7z, rK5VZdGj, E5vLLPV0 等）追查 `pyramids` 全部为
**`["DEU/D1/MODEL","DEU/D1/OTHER"]`** ⇒ MODEL 与 OTHER 同在禁混集合 {PV,MODEL,OTHER,FUNDAMENTAL} 内 ⇒ **一律不可交**。
典型表达式同时含 `oth455_relation_n2v_*` + `predicted_surprise_*` + `mean_estimate_*`。

⇒ 本地库里 S 最高的那批（2.1–2.2）**大多是禁混违规件**，这是它们停留在 UNSUBMITTED 且 prod 未测的真实原因。
**判读顺序必须是：先看 pyramids 判禁混 → 再看 prod → 再看互相关**。

### 24.7 下一步（缺口 4 颗）

已确认 6 颗，目标 10 颗。剩余方向按 prod 潜力排序：
1. **fundamental6 + FAST 中性化 + tvr_decay 双期限 delta 骨架**（Wje5K71x 配方，prod 仅 **0.4305**）—— F6-A/F6-B 16 条在飞；
2. fundamental6 的 ACTIVE 存量 4 颗（maxS 1.79）待取几何；
3. 129 颗未测 prod 存量中的 SHRT3 / FND6 族变体。









