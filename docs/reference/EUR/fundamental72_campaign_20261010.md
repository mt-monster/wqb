# EUR × Fundamental 战役：`fundamental72` 挖掘战报

> 时间：2026-10-10 18:40–19:30 ｜ 8 波 64 条仿真 ｜ 零提交
> 设置全程锁定 settings.json 正式档：`EUR / TOPCS1600 / SUBINDUSTRY / decay 4 / maxTrade ON / nanHandling ON`

---

## 一、结论摘要

| 项 | 结果 |
|---|---|
| **S 突破** | **0.16 → 1.40**（★ 门控机制，本轮核心发现） |
| 最佳候选 | **`9qWmLdmq`** S 1.40 / F 0.99 / 2Y 1.01 / margin 43.2bp / **TO 0.0287** |
| **硬约束** | ★ **TO 0.0287 < 0.05**，**正式档下机制内无解**（8 种 TO 杠杆全部试过） |
| 可提交候选 | **0 颗** |
| CT / robust | **全部合格**（CT 0.83–1.18 正、robust 0.79–0.86） |
| skill 沉淀 | ✅ 已完成（含 `vector_neut` 失效修正，见 §5） |

---

## 二、选型：为什么是 `fundamental72`

### 2.1 塔状态（平台实查）
EUR/D1 金字塔：`model=1 / fundamental=1 / risk=1`，其余 0 ⇒ **fundamental 塔未满，有潜力**。

### 2.2 三条选型依据

| 依据 | 证据 |
|---|---|
| **几乎未被挖掘** | 本地库仅 8 条记录（最高 S −0.01）；对比 `fundamental1` 有 368 条 |
| **白空间明确** | `fnd72_pit_or_*`（VECTOR）userCount **0–4**；而 `fnd72_s_*`（MATRIX）已被挖 **1115 次** |
| **不在判死记录内** | skill 判死的是 f23/f93/other401/f17 参数扩展 |

### 2.3 ★ 已挖 8 条历史失败的根因
全部是**裸绝对金额的水平/zscore**（应收账款、应付账款、累计折旧、资本公积）——
**未做尺度归一化** ⇒ 绝对金额跨公司不可比 ⇒ 必然无效。

---

## 三、突破路径：S 0.16 → 1.40

### 3.1 ★★ 关键发现一：VECTOR 与 MATRIX 版本的 TO 差 5–10 倍

| 版本 | 字段例 | 类型 | TO |
|---|---|---|---|
| `fnd72_pit_or_cf_q_cf_cash_from_oper` | 无 `s_` 前缀 | **VECTOR**（需 `vec_avg`） | **0.10 附近 ✅** |
| `fnd72_s_pit_or_cf_q_cf_cash_from_oper` | 有 `s_` 前缀 | **MATRIX**（直接可用） | **0.011–0.023 ✗** |

⇒ **反直觉结论**：MATRIX 通常更好用（无归约负担），此处却因 TO 不合格而不可用。
**机理**：`vec_avg` 归约引入横截面变化；MATRIX 的单一季度值变化极慢。

### 3.2 ★★★ 关键发现二：`trade_when` 门控是唯一 S 来源

```
trade_when(
  greater(divide(vec_avg(cfo_q), vec_avg(net_inc_q)), 0.3),   ← 门控：CFO/净利 > 0.3
  group_rank(divide(vec_avg(cfo_q), vec_avg(tot_asset_q)), market),  ← 信号：CFO/TA 组内秩
  -1)
```

**门控的经济含义**：剔除「利润无现金流支撑」的公司（高应计/财务操纵嫌疑）⇒
剩余样本上信号更纯净 ⇒ **是「样本清洗」而非「减仓」**。

| 门控阈值 | 分组轴 | alpha | S | F | 2Y | margin | TO |
|---:|---|---|---:|---:|---:|---:|---:|
| 无门控 | sector | — | 0.16 | 0.04 | 0.41 | 1.3bp | **0.111** |
| 1.5 | sector | `O08VPbJY` | 0.73 | 0.35 | 0.06 | 21.0bp | 0.0271 |
| 1.2 | sector | `blOnZoOr` | 0.87 | 0.46 | 0.16 | 23.6bp | 0.0293 |
| 1.0 | sector | `wpbPm0bd` | 0.92 | 0.50 | 0.44 | 23.9bp | 0.0305 |
| 0.8 | sector | `e7QvwdQO` | 1.08 | 0.63 | 0.63 | 26.9bp | 0.0313 |
| 0.6 | sector | `9qWm13lV` | 1.24 | 0.77 | 0.74 | 29.5bp | 0.0323 |
| 0.3 | sector | `pw5ZAMMj` | 1.31 | 0.82 | 0.90 | 29.4bp | 0.0335 |
| **0.8** | **market** | `MP3ZRng9` | **1.32** | **0.91** | 0.92 | **44.7bp** | 0.0267 |
| 0.3 | **market** | ★**`9qWmLdmq`** | ★**1.40** | ★**0.99** | ★**1.01** | 43.2bp | 0.0287 |

**两条单调规律**：
1. **门控阈值越低 ⇒ S 越高**，峰值在 **0.3–0.6**（0.2 已回落）
2. **分组轴：`market` ≫ `sector` > `industry` > `subindustry`**（1.40 / 1.31 / 0.82 / 0.56）

### 3.3 失败的路线（已穷尽，勿重试）

| 路线 | 结果 |
|---|---|
| skill 的残差骨架（2/3 腿 `subtract(rank,rank)`） | S 0.01 / −0.09 ⇒ **在 f72 上无效** |
| 无门控 + 幂次外置（1.3/1.5） | S −0.06 ~ −0.07 ⇒ **幂次在此无效** |
| `ts_corr` / `ts_zscore` / `ts_av_diff` / `ts_quantile` / `zscore+winsorize` | 全弱（−0.41 ~ 0.01） |
| 非标准科目（异常项 / 或有负债 / 养老金 / 股票薪酬 / 商誉减值 / 有效税率） | 全负（−0.47 ~ −0.07） |

---

## 四、硬约束：TO 在正式档下不可突破

### 4.1 S–TO 前沿（完整测出）

```
无门控        S 0.16   TO 0.111  ✅ TO 合格但 S 弱
阈值 0.6      S 1.24   TO 0.032
阈值 0.3      S 1.40   TO 0.029  ← S 峰
短窗时序信号   S 0.46   TO 0.042  ← TO 峰（带门控）
review 线     S 1.58   TO 0.050
```

⇒ ★★★ **在 `maxTrade=ON` + `decay=4` 下，TO ≥0.05 与 S ≥1.25 不可兼得。**

### 4.2 提 TO 的 10 种尝试（全部失败）

| 尝试 | TO | 判定 |
|---|---:|---|
| `ts_target_tvr_decay(target_tvr=0.05/0.08/0.1)` | 0.0282 / 0.0286 / 0.0287 | ❌ **完全未变** ⇒ 该算子**只降不升** |
| `ts_target_tvr_hump(target_tvr=0.05)` | 0.0282 | ❌ 同上 |
| 门控 + `ts_rank(...,66)` | 0.0419 | ⚠ TO↑但 S 掉到 0.46 |
| 门控 + `ts_scale(...,66)` | 0.0378 | ⚠ S 0.41 |
| 门控 + `ts_zscore(...,66)` | 0.0400 | ⚠ S 0.44 |
| 门控 + `ts_delta(...,252)` | 0.0279 | ❌ S −0.01 |
| 幂次外置（<1 压中间） | 0.0304 | ❌ 无效 |
| 更宽松门控（0.2/0.5） | 0.029–0.033 | ❌ 同步降 S |
| ★**横截面排名门控**（`group_rank(CFO/NI) > θ`） | 0.0282 | ❌ 未改善（原假设「排名波动⇒门控频繁开关」不成立） |
| ★**时序排名门控**（`ts_rank(CFO/NI, 252) > θ`） | 0.0262 | ❌ 更差 |

⇒ ★★★ **结论：TO 在正式档（`maxTrade=ON` + `decay=4`）下无法通过任何机制杠杆提升。**
根本原因：门控（无论用绝对值/横截面排名/时序排名）都会把持仓集中到「现金流覆盖利润」的子集，
该子集的公司集合本身**季度间变化很小** ⇒ 持仓稳定 ⇒ TO 天然低。

### 4.3 唯一剩余路径：改档（需用户批准）

| 档位变更 | 预期效果 | 依据 |
|---|---|---|
| `maxTrade: ON → OFF` | TO **+34%**（0.0287 → 0.0385） | 本日 analyst7 单变量实测（3 条对照） |
| `decay: 4 → 1` | TO 预计再 +30–50% | skill「decay 匹配信号速度，快信号上 decay 越大越差」 |
| **两者合并** | **0.0385 × 1.4 ≈ 0.054 ✅ 可达 0.05 线** | 待实测 |

⚠ 但按 skill 锁定条款：「**设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比**」
⇒ **改档需用户明确批准**，且改后 S/F/2Y/CT 需全部重测。

---

## 五、skill 沉淀（用户要求：总结经验沉淀到 skills）

### 5.1 ★★★ 修正 `vector_neut` 失效（三处）

| 位置 | 原内容 | 修正后 |
|---|---|---|
| `tracking/EUR/config/cells.json` `note` | 「EUR 破 prod 墙的**唯一**有效杠杆：vector_neut 残差化」 | 「vector_neut 已于 2026-10-10 实测被平台移除 ⇒ 改用 ts_regression / group_neutralize / subtract(rank,rank)」 |
| 同上 `generation.notes` | — | 追加失效说明 + 替代路径 |
| 同上 skeleton `evidence` | 「2 层嵌套 prod 0.6997 过线」 | 保留历史证据 + 标注「不可再执行」 |
| `src/wqb/profiles/locked.py:44` **GLOBAL_FORBIDDEN** | 残差化举例 `regression_neut / vector_neut` | 改 `ts_regression / group_neutralize`（**两个旧算子都不在平台清单**） |

### 5.2 流程（已执行）
```bash
PYTHONPATH=src python -m wqb.profiles check --region EUR      # 校验
PYTHONPATH=src python -m wqb.profiles render --region EUR --apply   # 重渲 11 文件
PYTHONPATH=src python tools/sync_skills.py --apply             # 同步 66 文件/6 安装位
```
备份：`tracking/EUR/config/cells.json.bak_before_vectorn_neut_fix_20261010`

### 5.3 本轮新增的可复用经验

1. ★★ **同一数据集可能有 VECTOR / MATRIX 两套字段**（`fnd72_*` vs `fnd72_s_*`）——
   **两者 TO 可差 5–10 倍**，选字段前必须两套都试。
2. ★★ **`trade_when` 在基本面数据上可能是「样本清洗」而非「减仓」** ——
   `trade_when(CFO/NI > θ, signal, -1)` 让 S +0.98、margin +24bp
   ⇒ **与算子清单 HINTS 的「多数场景压 S」相反**。
3. ★ **`ts_target_tvr_decay` / `ts_target_tvr_hump` 只降 TO 不升 TO** ——
   当前 TO 低于 target 时不生效（本轮 4 条实测 TO 完全未变）。
4. ★ **门控阈值越低 S 越高（峰值 0.3–0.6）**，但 TO 同步下降 ⇒ 需按目标档位选阈值。

---

## 六、下一步（需用户决策）

### 决策点：是否批准改档

**选项 A（推荐）**：批准 `maxTrade=OFF` + `decay=1` 试跑
- 预期：TO 0.0287 → ~0.054 ✅，S/F/2Y 需重测
- 风险：与正式档结果不可比；若 S 大幅下滑则前功尽弃

**选项 B**：保持正式档，换机制方向
- 已证明 f72 的 S–TO 前沿无解 ⇒ 需换数据集（但用户要求"不频繁切换数据集"）

**选项 C**：接受当前结果，将 `9qWmLdmq`（S1.40/F0.99）等作为「非正式档参考」存档
- 待平台规则或 settings 变化后再用

---

铁律：本轮**零提交、零入队**，`ALLOW_ALPHA_SUBMIT` 未触碰；全部仅仿真。