# EUR 信号挖掘工作流：字段画像 → 配模板 → 扫描 → 定向开发

> 版本 2026-10-21 ｜ 覆盖工具链、判据、四杠杆链、已知陷阱  
> 目标：把「找一个 alpha」从手工试错变成一条可复用的流水线

---

## 〇、一页总览

```
选集(EV) → 画维度地图(画像) → 配模板(属性×标定) → 派发(维度/模板族/边界三闸)
        → 收割归因 → 定向开发(四杠杆链) → 全闸验证(prod/self/robust) → 标绿/存档
```



---

## 一、工具链

| 工具                                                             | 作用                                                          |
| -------------------------------------------------------------- | ----------------------------------------------------------- |
| `tools/load_field_profiles_to_db.py`                           | 建库：`dataset_profile`（178 行）+ `field_profile_full`（38,609 行） |
| `tools/query_profile.py`                                       | 查询：datasets / fields / dims / search / stats / top          |
| `tools/full_coverage_gate.py`                                  | 派发前闸：维度覆盖 + 模板族 + 边界算子（默认维度级）                               |
| `tools/full_template_campaign.py`                              | 全数据集流水线（8 模板族 × 维度级，断点续跑）                                   |
| `tools/fields/field_semantic_type.py`                          | 字段语义分类（count/ratio/level/score/…）                           |
| `cache/_run_gate.py` / `_harvest_safe.py` / `_alpha_detail.py` | 派发 / 收割 / 详情                                                |

---

## 二、Step 1：选集（先算期望值，不看名字）

```bash
$PY tools/query_profile.py datasets --min-cov 0.7 --sort value_score
$PY tools/query_profile.py stats
```

**判据**：`EV = valueScore × 平均覆盖 × 未测占比 ÷ (1 + alphaCount/1000)`，EV 降序。

**硬排除**：

- 覆盖 < 0.5 → 不做主腿（可作条件/分组）
- 平台 `field_count=0`（画像有字段 ≠ 平台能用）
- 该语义维度同族字段全 DEAD（探针证据）且 max_S < 1.0

**注意**：EV 只反映「拥挤度 × 覆盖 × 未测占比」，**不反映字段信号强度**——EV 高只是「值得先探」，不是「能出活」。

---

## 三、Step 2：画维度地图 + 读字段属性

```bash
$PY tools/query_profile.py fields --dataset <ds>
$PY tools/query_profile.py dims --min-dim-cov 1.0
```

看三件事：

1. **语义维度**（`semantic_family`）——每个维度都要覆盖
2. **字段语义类型**（`sem_type`）——决定模板约束（见 Step 3）
3. **历史判定**（`verdict`）——ALIVE 是金矿，UNUSABLE/DEAD 是雷区

**关键字段属性 → 模板约束**（本战役实证）：

| 属性                                    | 判据    | 约束                                           |
| ------------------------------------- | ----- | -------------------------------------------- |
| `freq` = quarterly/semi-annual        | 慢频    | backfill ≥252、平滑 ≥63、**禁 3–22 短窗**           |
| `near_zero_ratio` > 0.3               | 稀疏    | 必须 backfill + 事件式 decay                      |
| `shape` = ceiling                     | 截断    | 先 `rank`，禁裸 zscore                           |
| `integer` = 1                         | 计数    | 用 spread/ratio，禁 level                       |
| `pos_ratio` ≈ 1                       | 全正    | 禁裸 zscore，先 `rank`                           |
| 有符号（0.1–0.9）                          | 双向    | 可直接用，**符号即方向**                               |
| `sem_type` = ratio                    | 比率    | 直接上模板（实测 avg_S 0.51 最高）                      |
| `sem_type` = revision_change          | 已是变化量 | **禁再套 ts_delta**                             |
| `sem_type` = score                    | 有界噪声  | 先 `rank`/`quantile`，或只作门控                    |
| `sem_type` = level_amount             | 规模水平  | **先 `vector_neut(F, size)` 体检**（归零即 size 代理） |
| `sem_type` = identifier/cluster_label | —     | 不可作信号                                        |
| VECTOR 事件型                            | —     | **必须先 `vec_*(F)`**，禁事件层算术与 ts_backfill       |

---

## 四、Step 3：配模板（用标定表，不凭感觉）

**决定模板的是「频段」，不是「机制」**（256 次标定矩阵实证）：

| 字段频段      | 最佳模板             | 次佳   | 最差    |
| --------- | ---------------- | ---- | ----- |
| 慢频文本/事件   | **一阶/二阶差分**      | 事件衰减 | 双窗秩乘积 |
| 慢频分析师预期   | **双窗秩乘积**        | 横截面秩 | 二阶差分  |
| 高频价量      | **双窗秩乘积 + 横截面秩** | 时序秩  | 差分族   |
| 慢频基本面（比率） | **横截面秩 / 冠军栈**   | 双窗   | 二阶差分  |

**8 个模板族（判死必须全试）**：

| # | 模板    | 形式                                                                    |
| - | ----- | --------------------------------------------------------------------- |
| 1 | 冠军栈   | `signed_power(ts_zscore(ts_backfill(F,BF), ZW), 1.5)`                 |
| 2 | 横截面秩  | `rank(ts_backfill(F, BF))`                                            |
| 3 | 一阶差分  | `ts_delta(ts_backfill(F,BF), W1)`                                     |
| 4 | 二阶差分  | `ts_delta(ts_delta(ts_backfill(F,BF),W1),W1)`                         |
| 5 | 双窗秩乘积 | `multiply(rank(ts_mean(bf(F,BF),WS)), rank(ts_mean(bf(F,BF),WL)))`    |
| 6 | 时序秩   | `ts_rank(ts_backfill(F,BF), ZW)`                                      |
| 7 | 事件衰减  | `ts_decay_linear(ts_backfill(F,252), 63)`                             |
| 8 | 波动调整  | `divide(ts_delta(bf(F,BF),W1), add(ts_std_dev(bf(F,BF),ZW), 0.0001))` |

窗口按频率匹配（日频 bf22/短5/长126；季频 bf252/短63/长252/504）。

---

## 五、Step 4：派发（三闸先过）

```bash
$PY tools/full_coverage_gate.py --region EUR --dataset <ds> \
    --exprs-file cache/_cand.txt --campaign-dir tracking/EUR --gate-mode enforce
```

三道闸（默认维度级）：

1. **维度覆盖闸**：每个语义维度至少被 1 条候选触及（字段数 <3 的族并入「其他」；字段数 ≤10 的小集退回字段级全覆盖）
2. **模板族闸**：历史已试 ≥3 个模板族（判死需 8 族全试）
3. **边界算子闸**：算子参数在 `boundary_ops_eur.json` 合法档内

---

## 六、Step 5：收割 + 归因

收割后用「近闸归因」决定下一步：

| 情况                       | 判据         | 动作                        |
| ------------------------ | ---------- | ------------------------- |
| 全部 max_S < 1.0           | 信号弱        | 换集                        |
| S 1.2–1.6 且 sub/robust 过 | 近闸         | 进入定向开发                    |
| S 过但 2Y 不过               | 查逐年        | 死年 → FAST 中性化（见杠杆②）       |
| S 过但 prod 不过             | 查 prod 直方图 | 密墙 → 换持仓域（流动性分片）；单钉 → 换字段 |

**prod 直方图定性**（决定处方）：

- **单颗钉子**（0.7–0.8 只有 1–2 颗）→ 换字段/换分组轴可破
- **密墙**（0.7–0.8 几十颗）→ 必须换持仓集合（流动性分片），换字段无效

---

## 七、Step 6：定向开发（四杠杆链）

每个杠杆负责一道闸，按序叠加：

| 杠杆                     | 表达式                                                | 解决的闸     | 实测幅度            |
| ---------------------- | -------------------------------------------------- | -------- | --------------- |
| ① 双窗秩乘积                | `multiply(rank(ts_mean(F,短)), rank(ts_mean(F,长)))` | **sub**  | 0.62 → 1.00     |
| ② **FAST 中性化**         | settings `neutralization=FAST`                     | **2Y**   | 1.46 → **2.09** |
| ③ signed_power 0.7–0.8 | 外层压缩                                               | S        | +0.06           |
| ④ 换字段（同族变体）            | 换 `_pct_`/`fy1`/`fy2` 变体                           | **prod** | 0.77 → 0.685    |

**sub↔prod 权衡的铁律**：同一信号族里，任何「改后处理」都是用一个闸换另一个闸；**只有换字段能同时保住两个**（因为同族字段的 prod 钉子互不相关）。

---

## 八、Step 7：全闸验证

最终候选必须同时过（以平台 `get_alpha_details` 为准）：

| 闸            | 限                   |
| ------------ | ------------------- |
| Sharpe       | ≥ 1.58              |
| Fitness      | ≥ 1.0               |
| 2Y           | ≥ 1.58              |
| sub-universe | ≥ 0.53 × S          |
| robust       | ≥ 0.70              |
| turnover     | 0.01–0.7            |
| **prod**     | < 0.70              |
| **self**     | < 0.70              |
| CW           | —                   |
| CLUSTER      | ≥ 1.58（WARNING 非阻塞） |

验证命令：

```
submit_verdict          # failed_ra 应为 0
check_correlation       # prod<0.7 且 self<0.7
get_alpha_yearly_stats  # 归因死年
```

---

## 九、标绿 / 存档

- **全闸过** → `set_alpha_properties(color=GREEN, name, tags, descriptions)`，等用户决定提交
- **近闸**（8/9 过）→ 标 `YELLOW` + `near-gate` 标签 + 写明唯一失败闸与归因
- **判死** → 写 `docs/reference/EUR/datasets/<ds>.md` 的死因，更新 `field_profile_perf`

---

## 十、已知陷阱（都是踩过的坑）

| 陷阱                   | 现象                                          | 解法                        |
| -------------------- | ------------------------------------------- | ------------------------- |
| VECTOR 事件层算术         | `multiply does not support event inputs`    | 先 `vec_*`                 |
| VECTOR + ts_backfill | `ts_backfill does not support event inputs` | 先 `vec_*`                 |
| 全正字段裸 zscore         | 极端值主导                                       | 先 `rank`                  |
| revision_change 再差分  | 信号被毁                                        | 用 level 或累积               |
| level 类字段不做 size 体检  | 正交后归零                                       | `vector_neut(F, size)` 先行 |
| 收割顺序 ≠ 提交顺序          | 模板映射错                                       | **模板优先派发**（每批只含一个模板）      |
| 判死只测 3 个模板           | 误判                                          | **判死需 8 族全试**（铁律）         |
| EV 高 = 能出活           | 错                                           | EV 只反映拥挤度/覆盖，不反映信号强度      |

---

## 十一、命令速查

```bash
# 选集
$PY tools/query_profile.py datasets --min-cov 0.7 --sort value_score
$PY tools/query_profile.py dims --min-dim-cov 1.0

# 看某集
$PY tools/query_profile.py fields --dataset <ds>

# 派发前过闸
$PY tools/full_coverage_gate.py --region EUR --dataset <ds> \
    --exprs-file cand.txt --campaign-dir tracking/EUR --gate-mode enforce

# 全数据集流水线（后台）
WQB_CAMPAIGN_FRESH= python tools/full_template_campaign.py --limit 30

# 收割 / 详情
python cache/_harvest_safe.py <sim_id> <dataset> <label>
python cache/_alpha_detail.py <alpha_id>
```

---

## 附录 A：8 模板族的匹配性评估与扩充（2026-10-21，sentiment26 实证）

### 结论：8 族**不够**，缺了一整层

**直接证据**：sentiment26 的 S 突破不是来自 8 族中任何一个，而是来自族外的
`if_else(greater(rank(S),0.85), S, 0)` 稀疏化——S 1.01 → **1.52**（+0.50）。
8 族全部是「信号提取」变换（水平/差分/衰减/双窗），**没有「截面处理」这一层**。

### 问题 1：8 族混淆了正交层

alpha 构造实为 4 个正交层，8 族把其中两层焊死了：

| 层 | 作用 | 算子池 | 8 族现状 |
|---|---|---|---|
| L1 信号提取 | 拿什么信息 | level / ts_delta / ts_delta² / decay / vec_stddev / ts_ir | ✅ 有覆盖 |
| L2 归一化 | 怎么可比 | rank / zscore / quantile / ts_rank / ts_scale | ⚠️ 焊死（cs 用 zscore、rk 用 rank，没交叉） |
| L3 时间结构 | 多久尺度 | 单窗 / 双窗秩乘积 / regime 门 | ⚠️ 只有 dw |
| L4 截面处理 | 持仓怎么切 | plain / group_rank / **稀疏化 if_else** / 减组均值 | ❌ **几乎没有** |

### 问题 2：缺失的族（按实证价值排序）

| 新族 | 代表构造 | 实证 |
|---|---|---|
| **gate（稀疏化/门控）** | `if_else(greater(rank(S),q), S, 0)`，q∈{0.7,0.8,0.85,0.9} | sentiment26 S +0.50，阈值倒 U（0.85 甜点） |
| **regime 门（数据集内）** | `trade_when(ts_zscore(辅助字段)>0, S, -1)` | 待验 |
| **dispersion（VECTOR 内离散）** | `vec_stddev(F)` / `vec_range(F)` | 新信息维度（域名间注意力集中度） |
| **ts-位置** | `ts_scale / ts_arg_max / days_from_last_change` | 事件新鲜度 |
| **quantile 归一** | `ts_quantile(F,d)` 替换 rank | 尾部处理不同 |

### 修正后的流水线结构（两阶段）

```
阶段 1（选信号）：8 族 × 代表字段  —— 找「哪个字段有信息」
阶段 2（榨干）：对最佳构造自动跑「后处理电池」——
   稀疏化 q ∈ {0.7, 0.8, 0.85, 0.9}
   group_rank ∈ {market, sector}
   signed_power ∈ {0.5, 0.7, 1.5}
   regime 门（用同集辅助字段）
```

**判据更新**：「数据集判死」现在要求阶段 1 + 阶段 2 都跑完
（旧的 8 族-only 判死会漏掉 sentiment26 这类「信号弱但稀疏化后可救」的集）。

### 稀疏化的机制解释（为什么它有效）

注意力类信号的信息集中在**极端尾部**（真正被关注飙升的股票），中间 80% 是噪声持仓、
稀释收益还贡献换手。`if_else(rank>0.85, S, 0)` 把组合浓缩到真信号段——
这与论坛评论「事件密度天然把权重堆在少数极端股票上，要在表达式层处理集中度」同向，
但用法相反：不是分散权重，而是**砍掉噪声段**。

### 修复落地（2026-10-21 20:40）：分层模板已生效

`full_template_campaign.py` 旧 8 族 → **L1×L2 交叉 12 族**：

```
L1 提取：lvl(水平) / d1(一阶差分) / d2(二阶差分) / ed(事件衰减) / ir(信噪比) / dsp(组内离散,仅VECTOR)
L2 归一：rk(rank) / zs(zscore) / qt(quantile) / tr(ts_rank) / sc(ts_scale)
组合：lvl×{rk,zs,qt,tr,sc} | d1×{rk,va} | d2×rk | ed×rk | ir | dsp×rk | + dw(L3双窗)
L4 截面：阶段 2 电池（稀疏化 0.8/0.85/0.9 + group_rank(market) + signed_power 0.7）
```

判死新口径：**12 族 + 阶段 2 电池全跑完**（取代「8 族全试」）。
