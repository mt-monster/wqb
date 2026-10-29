# EUR 挖掘会话复盘（2026-10-27 ~ 10-29）

> 覆盖 ~250 条仿真、40+ 批次。产出 2 颗全闸可交付 alpha（`E56Jea7P` 已提交、`leAXvaLn` 待交），
> 判死 20 个数据集/方向，点亮 2 个未点亮塔（SENTIMENT / INSTITUTIONS）。

---

## 一 历程：五次转折，每次都由一次"归因纠错"触发

| 阶段 | 起点假设 | 打翻它的事实 | 结果 |
|---|---|---|---|
| ① 破 prod 墙（10-27） | prod 是"字段问题" → 78 字段宽扫 | `1YNerr2X` 与 `e75pkq7E` prod **完全相同 0.6896**（换了主腿） | **prod 由结构决定，与字段无关** ⇒ N 颗 = N 个结构 |
| ② 未点亮塔（10-28 前半） | 7 个未点亮类别里单数据集硬挖 | 97 条实证，最好 S 0.56（= 闸线 1/3）；4 类被 cov 封死 | **"未点亮塔 = 数据可得性问题"**，不是方法问题 |
| ③ 转向 analyst7（10-28 后半） | 修正幅度是唯一读数 | 换科目 ebt→dps 只改 self，不改 2Y 天花板 | 发现 **5 类读数**，"广度"是全新信号族 |
| ④ 倾斜腿点塔（10-28 夜） | 换倾斜腿 = 换机制，可批量点塔 | `compute_mutual_correlation`：4 颗"不同倾斜腿"彼此 **0.948–0.970** | **倾斜腿不增席位**，只决定点亮哪个塔 |
| ⑤ 读数决定 prod（10-29） | 换科目能降 prod | 扩散指数 ebt 0.7801 vs ebi 0.7549（差 0.025）；广度 `/num_4wks_ago` 0.653–0.675 | **prod 由读数决定，2Y 由科目决定** ⇒ 拆成两个独立旋钮 |

**方法论上最大的收获**：五次的破局点全部来自**"同一变量的对照实验"**，没有一次来自新数据集。
新数据集只贡献"判死"，不贡献"产出"。

---

## 二 需要完善的地方（按伤到的成本排序）

### P0-1 候选批量派 prod 前，必须先做本地互测（本会话白烧 8 轮抢槽）

`check_correlation(type=self)` **只跟已提交池比**。4 颗同基底换倾斜腿的候选 self 各报 0.506–0.536（全"通过"），
实测彼此 **0.948–0.970** ⇒ 只有 1 颗能交。

- 根因：把 self 当成"独立性判据"，它其实是"与历史池的重合度"。
- 代价：若无 peer 抢占，会连测 4 次 prod（每次 300s inflight + 平台算力）。
- 改法：`compute_mutual_correlation`（**纯本地、零队列、零仿真**）作为 prod 前的强制前置，只看 `max_mutually_below_subset`。
- 落点：`wq-brain-ra-pipeline` 反模式 + `brain-calculate-alpha-selfcorr-quick` 盲区章节 + `wq-brain-ra-eur` ⑥ 终验。

### P0-2 ★★★★★ 判死「读数」而不是「数据集」——同一错误犯了三次，白跑 95 条

本会话最贵的错误。每次都是"用错读数形态 → 全灭 → 判死整个数据集"，而该数据集上其实早有有效读数的记录：

| 数据集 | 我判死的读数 | 实际有效的读数 | 成本 | 二次核实结果 |
|---|---|---|---|---|
| `news46` / news 类 | 情绪极性分（`news73`/`news17`/`sentiment21`） | **新闻条数 = 关注度** `mws46_ravenpack_sum_story_count` | **77 条** | `Xgojww1X` ACTIVE 早就是这个形态（S1.80/prod 0.5906）|
| `techindi_model` | `tm_N` 模型族 + `group_scale`（prod 0.745–0.816） | **双窗秩乘积** `multiply(rank(ts_mean(F,2)),rank(ts_mean(F,252)))` | **12 条** | `e76kv2xE` prod **0.6916** 早已过线，但已优化为 `LL5VwgO1` 并提交 ⇒ `e76kv2xE` self **0.9980** 锁死 |
| `predictive_starmine` | ARM **rank 水平**读数（S 0.10–0.49） | **二阶差分/极值差** `ts_max_diff` / `ts_delta(ts_delta(...))` | **6 条** | `RRAvGrn0` ACTIVE（S1.99/prod 0.5437），同字段同数据集 |

**判死前置二事（缺一不可）**：
1. 读 `references/<类别>.md` 里该数据集的**全部历史结论**——里面常有已过线的 prod 实测值。
   我上一轮只读了 `_dataset-inventory.md` 的 2.1/2.2 摘要，没读 `other.md`，所以不知道 techindi 有 prod 0.6916 的结构。
2. `get_alpha_details` 读该数据集已 ACTIVE alpha 的 `regular.code`，看它用的是哪种**读数形态**
   （水平 / 变化 / 极值差 / 双窗积 / 关注度 vs 极性 / 广度 vs 幅度）。

**判死结论的写法**：写「`<数据集>` 的 `<读数/结构>` 死」，不写「`<数据集>` 死」。
二者在 EUR 差了 3 次整族误杀。

### P0-3 "未点亮塔数学上封闭"这条判据是错的，且它误导了整个 ② 阶段

ra-eur SKILL.md ④ 写着「未点亮塔路径数学上封闭：`Fitness 上限 ≈ Sharpe × sqrt(returns/0.125)`，EUR returns 普遍 < 0.03」。

- 事实：本会话用「**已点亮强腿 × 1.2 权重未点亮小腿**」点亮了 **SENTIMENT(1.4)** 与 **INSTITUTIONS(1.1)** 两个塔，两颗都 0 项 fail。
- 该闭式只对**单腿**成立。加倾斜腿时 F 由合成腿的 S/returns 决定，不受未点亮腿的单腿 returns 约束。
- 副作用：这条判据让我在 ② 阶段只考虑"单数据集挖未点亮类"，从未考虑"强腿 + 小腿"这个唯一可行形态——
  而仓库里 `Xgojww1X` 早就是这个形态。

### P1-4 同字段的"读数"是一个独立旋钮，整个 skills 体系里没有条目

analyst7 的 `est_12m_<科目>_*` 有 5 类读数，语义与 prod 特性完全不同：

| 读数 | 公式 | S | prod | 备注 |
|---|---|---|---|---|
| 幅度 | `(mean−mean_4wks_ago)/std` | 1.97 | 0.50–0.62 | ebt/dps/gps/pre 已被占位 |
| **广度** | `(r−l)/num_4wks_ago` | 1.63 | **0.653–0.675** | ★ 最低 prod，但 S 偏低卡 F |
| 扩散指数 | `(r−l)/(r+l)` | 2.13 | 0.755–0.780 | sub 最优 1.36，prod 最高 |
| up-share | `r/(r+l)` | ≡ 扩散 | — | 与扩散单调等价 |
| 13 周 | `(mean−mean_3mth_ago)/std` | 0.66–1.18 | — | 死 |

前 3 轮只用了"幅度"，等于只挖了 1/4 的信号面。且**只有把广度（低 prod）+ 扩散（高 S）混成一腿，才同时过 F 与 prod**（`leAXvaLn`）。

### P1-5 universe 是"抬 S 也抬 prod"的双刃剑，ra-eur 却写"别混用 TOP2500"

- ra-eur ① 写「历史台账还有 TOP2500/COUNTRY/decay 6 的记录，**别混用**」。
- 实测：techindi 同公式 TOPCS1600→TOP2500，S 1.99→**2.57**、sub 1.37→**1.80**、2Y 2.06→2.34，把两条 rob FAIL 修成 0 fail。
- 但 prod 也从 0.7454 抬到 0.7794（**+0.034**）。
- 正确表述应是：**universe 是 prod–S 前沿上的平移旋钮，不是"禁区"**。选 universe = 决定把余量花在哪个闸上。

### P1-6 `group_scale(·, industry)` 是本会话最强单点 prod 杠杆，skills 里没有

实测排序（EUR，逐项单加）：

| 杠杆 | Δprod |
|---|---|
| `group_scale(·, industry)` | **−0.057** |
| 换读数 `/num` → `/num_4wks_ago` | −0.051 |
| 幂次 +0.4 | −0.027 |
| cap 20 桶中性化 | −0.025 |
| 加 1.2 权重倾斜腿 | **+0.013（反效果）** |

`group_scale` 还是唯一**四项同得**的杠杆（prod↓ / S↑ / 2Y↑ / sub↑），且在两个族（analyst7 广度、techindi 双腿）通用。
但**读数依赖**：输入必须是"截面可比分数"，对单股时序标准化幅度是破坏性的（analyst7 ebi 幅度 S 1.97→1.14；fundamental23 sub 崩到 0.63）。

### P1-7 F 闸的真实门槛没被量化

ra-eur 只给了闭式 `F = S^1.5 × sqrt(vol/0.125)`。实操门槛是：
**EUR 低波动族需 S ≥ 1.75 才过 F ≥ 1.0**（S 1.62 ⇒ F 0.87；S 1.71 ⇒ F 0.97）。
这直接解释了为什么"广度读数"（prod 最低）总卡 F——**prod 最低的读数恰好 S 最低，二者不可兼得**，
只能靠双读数混合打破。

### P1-8 2Y 的"科目属性"判据能省掉大量无效实验

同结构跨科目：ebt **2.12–2.62**｜dps 2.41｜gps 2.02｜pre 1.62 ≫ **ebi/eps/sal 天花板 1.46–1.57**。

- 该族 2Y 不足时，第一步应是**换科目**，不是调结构（结构杠杆在同科目内只有 ±0.05）。
- 我在 ebi/eps/sal 上把幅度/广度/双读数/倾斜权重（0.3–2.0）/时序窗（20/35/60）/decay（10–80）全扫了一遍，2Y 硬顶 1.57 —— 全是可省的成本。

### P2-9 派批前缺"表达式去重"检查

- `ts_delta(x,n) ≡ subtract(x, ts_delay(x,n))`：实测逐位相同，白跑 2 个仿真。
- `pv37` 的量压 z 与上行占比是单调等价变换：逐位同为 −0.49，白跑 1 个。
- 同一数据集内 6 条变体互测 0.89–0.99 的情况反复出现（techindi / fnd23）⇒ 应**先算互测再决定是否需要这么多变体**。

### P2-10 多实例并行时 prod 单并发互相饿死

账号级 prod 是**单并发**。peer 实例自 21:00 起不间断循环，holder 在 5 个 alpha 间轮换，
`QPvXPJ0p`/`zq31lNOK`/`N1NvGm5q` 各抢 3–5 轮全部 pending，累计浪费 ~2 小时。

- 现有 skills 没有"多实例 prod 预约"协议。
- 需要：① 开工先读 `logs/_dblock/correlation.inflight.json` 的 holder 与到期时间；② peer 活跃时**不要轮询**（每次调用重占 300s inflight，越试越慢）；③ prod 验证集中在一次窗口内做完（排队 N 颗一次抢，而不是一颗一轮）。

### P2-11 交付口径要区分"库存"与"目标"

会话中期我把"凑 20 颗"当成"从零做 20 颗"，直到盘点才发现 EUR 已有 16 颗 ACTIVE。
`get_user_alphas(stage=OS, region=EUR, type=REGULAR)` 是唯一权威口径（23 条 = 17 ACTIVE + 6 DECOMMISSIONED），
`get_submit_ready` 返回的 READY 池**不等于库存**（它漏掉已提交的、也可能含 GLB 污染）。

---

## 三 skills 改动清单（已执行）

| 文件 | 改动 | 起因 |
|---|---|---|
| `wq-brain-ra-eur/SKILL.md` ④ 破闸杠杆 | 删除"未点亮塔数学上封闭"；新增「倾斜腿点塔」形态 + 四条量化判据（group_scale/读数/2Y科目/F门槛）；sub 比率 0.53→**0.52** | P0-3、P1-4/6/7/8 |
| `wq-brain-ra-eur/SKILL.md` 本区流程差异 | TOP2500 从"别混用"改为"analyst7/techindi 必需 + prod–S 前沿旋钮" | P1-5 |
| `wq-brain-ra-eur/SKILL.md` ⑥ 终验 | 新增：批量派 prod 前必跑 `compute_mutual_correlation` | P0-1 |
| `wq-brain-ra-eur/references/_dataset-inventory.md` | 补 14 个判死集 + 修 techindi/analyst_factor_signals 的旧判定 | 本会话 20 条判死 |
| `brain-calculate-alpha-selfcorr-quick/SKILL.md` | 盲区章节新增「候选之间」，明确 self ≠ 独立性 | P0-1 |
| `wq-prod-lever-self-lock-guard/SKILL.md` | 铁律表新增 `group_scale` 一类（改分布不改持仓）；补 1.2 权重倾斜腿实测 | P1-6 |
| `wq-brain-ra-pipeline/SKILL.md` 反模式 | 新增 3 条（互测前置 / 读成功样本 code / 表达式等价去重） | P0-1/2、P2-9 |

---

## 四 尚未解决 / 下一会话的起点

1. **`leAXvaLn`（prod 0.6757）待用户点名提交**——与已提交 `E56Jea7P` 互测 0.6897（<0.70，可同交）。
2. **差 2 颗到 20**：analyst7 高-2Y 科目（ebt/dps/gps/pre）的幅度读数全被占位；
   唯一未试组合是「高-2Y 科目 × 广度读数 × 双读数混合」——即 `leAXvaLn` 的 dps/gps/pre 版本。
3. **未点亮塔还剩 NEWS**（earnings/macro/imbalance/socialmedia 已被 cov 封死）：
   `news46` 的 `sum_story_count` 当倾斜腿可点，但需挂在一个高-2Y 基底上。
4. **多实例 prod 预约协议**未落成工具（目前只有纪律，没有闸）。
