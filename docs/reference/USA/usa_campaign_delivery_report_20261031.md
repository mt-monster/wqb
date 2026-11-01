# USA 战役阶段交付报告（2026-10-30 ~ 2026-10-31）

> 目标：未点亮塔挖掘 20 颗 REGULAR alpha（优先 ATOM），prod < 0.70 / self < 0.70 / 全平台硬闸通过。
> 本报告口径：**已完成 / 已派发 / 未完成**分列；每条候选给出 prod / self / 模拟层三闸的实测值与出处。

---

## 1. 核心结论（先给答案）

### 1.1 本轮挖到的最硬成果

| 类别 | alpha | 塔位 | S / F | 2Y / SUB | TO | prod | self | inv_S | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| **四绿（唯一）** | `E56YodoJ` | OTHER | 1.63 / 1.06 | 2.20 / 0.81 | **7.47%** | **0.6435 ✅** | **0.305 ✅** | **0.80 ✅** | fRA 0、checks.fail 空 |
| 三绿（指标最强） | `kqNb7XY6` | OTHER | 2.47 / 2.18 | 3.49 / 1.33 | 17.51% | 0.6569 ✅ | 0.018 ✅ | −0.37 | fRA 0、checks.fail 空 |
| 三绿 | `58E3oA3X` | OTHER | 2.35 / 2.03 | 3.30 / 1.32 | 17.69% | 0.6715 ✅ | 0.004 ✅ | −0.22 | fRA 0、checks.fail 空 |
| 三绿（prod 余量最大） | `vROPEJ8w` | OTHER | 2.08 / 1.74 | 3.49 / 1.31 | 10.52% | **0.5517 ✅** | −0.073 ✅ | 0.17 | fRA 0、checks.fail 空 |
| 三绿 | `O0Jgd7Y7` | OTHER | 2.27 / 2.03 | 3.09 / 1.22 | 13.0% | 0.5655 ✅ | 0.0 ✅ | 0.17 | fRA 0、checks.fail 空 |
| 三绿 | `LL53QVvn` | OTHER | 1.61 / 1.39 | 2.75 / 1.00 | 11.2% | 0.6163 ✅ | −0.036 ✅ | 0.13 | fRA 0、checks.fail 空 |
| 三绿 | `1Yj08nb6` | OTHER | 1.58 / 1.20 | 2.29 / 0.94 | 10.01% | 0.5796 ✅ | — | −0.03 | fRA 0 |
| 三绿 | `XgRM3Yra` | OTHER | 1.66 / 1.19 | 2.27 / 0.97 | 8.69% | 0.5803 ✅ | — | −0.06 | fRA 0 |
| 双塔候选 | `O0AqkrA7` | **RISK + OTHER** | 2.34 / 1.96 | 3.23 / 1.08 | 9.93% | **0.7832 ❌** | — | −0.06 | fRA 0、IS_LADDER PASS |
| RISK 差一项 | `A1VYRo2w` | RISK | 2.24 / 1.42 | 2.19 / 0.35 | 5.05% | **0.495 ✅** | — | — | fRA 1（只差 SUB） |
| RISK 差一项 | `zq3QvlL1` | RISK | 2.07 / 1.30 | 1.63 / 0.42 | 4.99% | — | — | — | fRA 1（只差 SUB） |
| INSTITUTIONS+RISK | `9qxP0JbV` | INSTITUTIONS + RISK | 2.45 / 1.74 | 2.76 / 1.87 | 8.8% | 0.5263 ✅ | 0.103 ✅ | — | fRA 0 |
| RISK | `9qxLOPxr` | RISK | 2.69 / 1.67 | 2.24 / 1.44 | — | 0.6835 ⚠️ | 0.287 ✅ | — | 贴线，提交前须 refresh |
| INSIDERS | `pwdQlr2V` | **PV + INSIDERS** | 1.64 / 1.12 | 2.29 / 0.89 | 1.3% | 0.6997 ⚠️ | — | 1.02 | fRA 0、checks.fail 空；**含 rank(cap) ⇒ 触 PV 边界** |

### 1.1b 跨数据集残差化带来的双塔 / 三塔候选（wave278–279）

> 手法：`vector_neut(主腿, 其他数据集腿)` —— 主腿必须是**信息量更大**的那个数据集；
> **跨数据集绝不能用 multiply**（实测 S −1.36 / DD 46.9% 与 S −3.27 / DD **171.9%**）。

| alpha | 组合 | 塔位 | S / F | 2Y / SUB | TO | inv_S | fRA | prod |
|---|---|---|---|---|---|---|---|---|
| **`58E3agW1`** | insider base → risk59 → governance | **RISK + INSIDERS + OTHER** | 2.34 / 1.96 | 2.83 / 1.21 | 9.69% | −0.18 | **0** | 未测 |
| **`pwdoV5OX`** | top insider → risk59(shares) | RISK + OTHER | 2.49 / 2.32 | 3.58 / 1.20 | 11.29% | 0.01 | **0** | 未测 |
| **`e75gdQoM`** | base 63×z504 → risk59 | RISK + OTHER | 2.03 / 1.74 | 2.19 / 1.07 | 11.31% | −0.19 | **0** | 未测 |
| **`1YN1aZQX`** | base 252 窗 → risk59 | RISK + OTHER | 1.74 / 1.27 | 2.02 / 1.07 | 10.37% | −0.04 | **0** | 未测（**指标最低 ⇒ prod 预期最低 ⇒ 最该优先测**） |
| **`qMLvP0qv`** | insider 差值腿 → governance | **INSIDERS + OTHER** | 1.68 / 1.10 | 2.17 / 0.83 | 7.36% | **0.86** | **0** | 未测 |
| **`kqNb1g5d`** | insider 22 窗 → governance | INSIDERS + OTHER | **3.32 / 3.29** | 3.65 / 1.76 | 17.34% | −0.50 | **0** | 未测（指标最高 ⇒ prod 预期最高） |
| `WjOndPLx` | insider 差值腿 → risk59 | RISK + OTHER | 1.58 / **0.99** | 2.24 / 0.72 | 7.59% | **0.78** | 1（F 差 1%） | 未测 |
| `O0AqkrA7` | insider secondary → risk59 | RISK + OTHER | 2.34 / 1.96 | 3.23 / 1.08 | 9.93% | −0.06 | 0 | **0.7832 ❌** |

### 1.1c INSIDERS 塔（wave280–281）—— 塔位纯净 + prod 饱和的关键结论

| alpha | 表达式要点 | 塔位 | S / F | 2Y / SUB | TO | inv_S | fRA | prod |
|---|---|---|---|---|---|---|---|---|
| **ZYQkoman** | 任期 × 网络 × **董事会规模**(bucket) | **INSIDERS 单塔（纯净）** | 1.72 / 1.09 | 1.98 / 0.74 | 1.57% | 1.77 | **0** | **0.8046 ❌** |
| qMLvlqJ1 | **CEO 任期** × 网络 × 董事会规模 | INSIDERS 单塔 | 1.73 / 1.09 | 2.18 / 0.77 | 1.55% | 1.75 | **0** | 未测 |
| KPJq9aMN | **最长任期** × 网络 × 董事会规模 | INSIDERS 单塔 | 1.72 / 1.12 | 1.97 / 0.80 | 1.55% | 1.76 | **0** | 未测 |
| zq3Qmp71 | 任期 × 网络 × 规模（**504 窗**） | INSIDERS 单塔 | 1.72 / 1.09 | 1.99 / 0.74 | 1.58% | 1.77 | **0** | 未测 |
| **qMLvP0qv** | insider 差值腿 主导 + 治理腿残差 | **INSIDERS + OTHER** | 1.68 / 1.10 | 2.17 / 0.83 | 7.36% | **0.86** | **0** | 未测 |
| **kqNb1g5d** | insider 短窗腿 主导 + 治理腿残差 | **INSIDERS + OTHER** | **3.32 / 3.29** | 3.65 / 1.76 | 17.34% | −0.50 | **0** | 未测 |

**两条决定性结论**：
1. **换 bucket 的分母字段 = 切换塔归属**：波 196 的 `pwdQlr2V` bucket 用 `rank(cap)`（PV 塔字段）⇒ 塔位 **[PV, INSIDERS]**；wave280 的 `ZYQkoman` 用 `rank(board_member_count_2)`（INSIDERS 自身字段）⇒ 塔位 **[INSIDERS] 单塔**。同一家族结构，只换 bucket 分母即可拿到纯净单塔。
2. **★ 治理族在 USA 的 prod 已饱和**：波 196 的 0.6997–0.7244（已预警）→ wave280 `ZYQkoman` 实测 **0.8046** → `KPJeor68` 实测 0.7146 ⇒ **纯治理骨架 prod 普遍 > 0.7 ⇒ INSIDERS 塔不能用纯治理点亮**，必须用机制正交的组合（insider 腿主导 + 治理腿残差）。
3. **治理族候选彼此互相关 0.93–0.9999**（ZYQkoman ↔ zq3Qmp71 = 0.9999）⇒ 纯治理族**同篮最多 1 颗**。INSIDERS 塔的最优 4 颗篮子（两两 0.06–0.69）：`ZYQkoman` + `qMLvP0qv` + `kqNb1g5d` + `pwdQlr2V`。

### 1.2 塔位现状（平台 `get_pyramid_alphas` 权威，2026-10-31）

USA/D1：`model 4` / `analyst 6` / `other 1` / `earnings 1`，**其余 12 塔全 0**（pv / fundamental / socialmedia / news / option / macro / insiders / risk / shortinterest / sentiment / institutions / imbalance）。
USA/D0：全 0。

| 塔 | 计数 | 本轮进展 | 缺什么 |
|---|---|---|---|
| **OTHER** | 1 | **6 颗全闸候选已产出**（kqNb7XY6 / 58E3oA3X / vROPEJ8w / O0Jgd7Y7 / LL53QVvn / 1Yj08nb6 / XgRM3Yra / E56YodoJ），互相关最大对 0.97 | 只差**真人确认提交** |
| **RISK** | 0 | 9qxP0JbV 已备（INSTITUTIONS+RISK 双塔）；A1VYRo2w / zq3QvlL1 只差 SUB | SUB 在 risk59 内部无解（见 §3） |
| **INSTITUTIONS** | 0 | 9qxP0JbV（双塔） | 单塔候选 |
| **INSIDERS** | 0 | pwdQlr2V（fRA 0，但含 rank(cap) ⇒ 塔位是 [PV, INSIDERS]） | 需裁定 PV 边界 |
| **FUNDAMENTAL** | 0 | fundamental17 / fundamental93 两波**全灭**（成长外推反转方向反 + 应计质量因子已被套利） | 需换数据集/机制 |
| OPTION / NEWS / SENTIMENT / SHORTINTEREST | 0 | 本轮未动（前序已判死或封盘） | — |
| PV / MODEL / ANALYST / EARNINGS | 0/4/6/1 | MODEL/ANALYST/EARNINGS 已点亮 | PV 禁混 ⇒ 不做 |

---

## 2. 本轮 14 波的完整归因

### 2.0 ★ 全库终态扫描：22 颗「全闸 + prod<0.7 已实测」候选（prod 升序）

| alpha | prod | self | S | F | 2Y | SUB | TO | 数据集 | 塔位 |
|---|---:|---|---:|---:|---:|---:|---:|---|---|
| `QPvrZW7X` | **0.5289** | — | 2.45 | 1.77 | 2.77 | 1.85 | 10.6% | _unknown | ? |
| `vROPEJ8w` | 0.5517 | 0 | 2.08 | 1.74 | 3.49 | 1.31 | 10.5% | insider_trx_matrix | OTHER |
| `O0Jgd7Y7` | 0.5655 | 0 | 2.27 | 2.03 | 3.09 | 1.22 | 13.0% | insider_trx_matrix | OTHER |
| `Xg9wmjgX` | 0.5716 | 0.072 | 2.33 | 1.50 | 2.25 | **1.90** | 8.8% | _unknown | ? |
| `1Yj08nb6` | 0.5796 | — | 1.58 | 1.20 | 2.29 | 0.94 | 10.0% | insider_trx_matrix | OTHER |
| `XgRM3Yra` | 0.5803 | — | 1.66 | 1.19 | 2.27 | 0.97 | 8.7% | insider_trx_matrix | OTHER |
| `LL53QVvn` | 0.6163 | −0.036 | 1.61 | 1.39 | 2.75 | 1.00 | 11.2% | insider_trx_matrix | OTHER |
| **`E56YodoJ`** | **0.6435** | **0.305** | 1.63 | 1.06 | 2.20 | 0.81 | **7.5%** | insider_trx_matrix | OTHER | ★ 四绿 |
| `78LAAm92` / `78LAAZx1` / `P0MRkP0M` / `LL5rpRY2` | 0.6530 | — | 1.74–1.79 | 1.25–1.32 | 1.86–1.93 | 1.22–1.23 | 15.8–16.5% | _unknown | ? |
| `kqNb7XY6` | 0.6569 | 0.018 | 2.47 | 2.18 | 3.49 | 1.33 | 17.5% | insider_trx_matrix | OTHER |
| `58E3oA3X` | 0.6715 | 0.004 | 2.35 | 2.03 | 3.30 | 1.32 | 17.7% | insider_trx_matrix | OTHER |
| `88vXxaqv` | 0.6811 | — | 1.99 | 1.66 | 2.04 | 0.89 | 9.5% | insider_trx_matrix | OTHER |
| `78Lb3aoQ` | 0.6839 | — | 1.82 | 1.21 | 2.31 | 1.06 | 3.4% | _unknown | ? |
| `zqrgna91` | 0.6877 | 0.287 | 2.67 | 1.66 | 1.68 | 1.47 | 15.8% | _unknown | ? |
| `N1eLE1de` | 0.6916 | 0.275 | 2.63 | 1.54 | 2.07 | 1.66 | 14.1% | _unknown | ? |
| `YPMvZZvv` | 0.6958 | 0.411 | 1.79 | 1.06 | 1.68 | 0.83 | 6.2% | analyst_consensus | ANALYST（已亮） |
| `88v2XRm7` | 0.6993 | 0.086 | 2.73 | 2.60 | 3.55 | 1.27 | 12.9% | insider_trx_matrix | OTHER |
| `rKRY3NZ1` | 0.6995 | — | 1.79 | 1.17 | 2.28 | 0.93 | 4.6% | _unknown | ? |
| `pwdQlr2V` | 0.6997 | — | 1.64 | 1.12 | 2.29 | 0.89 | 1.3% | board_gov_stats | **[PV, INSIDERS]** |

**另有 `9qxP0JbV` prod 0.5263 / self 0.103（INSTITUTIONS + RISK 双塔）** —— 塔位表里未出现在上一查询是因为它的 `sub_universe_sharpe` 记录缺失被 SQL 过滤，但 `batch_get_alpha_metrics` 实测 SUB 1.87 ⇒ 实际全闸。

### 2.1 波次索引

| 波 | 数据集 | 主题 | 结果 |
|---|---|---|---|
| 266 | risk59 | sq 252 → 504 纠错 | PARTIAL（发现 504 更优） |
| 267 | risk59 | 10 互异模板（sq504 × s3u252） | PARTIAL（`bl62JAXM` S1.71/F0.76/SUB0.74 过闸） |
| 267s | risk59 | 设置层扫描（decay × 中性化，7 条） | **FAIL**（设置层已穷尽） |
| 268 | risk59 | 10 互异模板（内生规模正交腿等） | FAIL，但**意外发现联动性机制** |
| 269 | risk59 | 联动性反转（ts_corr） | **PARTIAL**（`MPYlnRaM` S1.81/F1.00/prod0.4616） |
| 270 | fundamental17 | 成长外推反转（论坛帖） | **FAIL**（★ 方向反转，7/10 S 为负） |
| 271 | risk59 | 联动性抬 S/F（换对象 × 长窗） | **PARTIAL**（3 条 S>2.0/F>1.2；`9qxPe8X2` prod 0.5331） |
| 272 | fundamental93 | 应计质量因子（Sloan 1996） | **FAIL**（\|S\| ≤ 0.34，已被套利） |
| 272b | risk59 | 长窗 × 强对象交叉 | PARTIAL（2 条 fRA=1 只差 SUB） |
| 273 | insider_trx_matrix | 卖出侧 / 净方向 / 美元金额 | PARTIAL（**买卖比是新机制**） |
| 274 | insider_trx_matrix | 窗口扰动 + 买卖比精炼 + 残差化 | **PASS**（`kqNb7XY6` 全闸+prod+self 三绿） |
| 275 | insider_trx_matrix | 新鲜度轴极限 + 标准化窗 + 乘性 | PASS（2 条 fRA=0） |
| 276 | insider_trx_matrix | 聚合配方 × 几何 × 宇宙 | PASS（4 条 fRA=0；**发现 prod 0.8958 撞墙**） |
| 277 | insider_trx_matrix | 压 prod 偏离波 | PASS（5 条 fRA=0；**`E56YodoJ` 四绿**） |
| 278 | risk59 + insider_trx_matrix | 跨数据集残差化（双塔） | PASS（**首颗双塔全闸** `O0AqkrA7`，但 prod 0.7832 ❌） |
| 279 | 三数据集 | 低 prod 腿 + 新塔组合 | 已派发 |

### 2.2 五条可迁移的机制结论

1. **「水平残差」vs「走势联动性」是两种机制**（risk59）
   `vector_neut(-ts_rank(A), ts_rank(B))` 用两个**水平**做残差；`-ts_corr(A, B, W)` 用两者的**同步性**。后者捕捉「结构性错离」，天然过 CW + TO 双闸（相关系数有界 ⇒ 幅度不极端）。**卡 F/CW 闸时优先试 `-ts_corr`。**
2. **窗口长度由机制的时间衰减速度决定，不是通用偏好**
   risk59 联动性：504–1008 窗最优（S2.24）；内部人买入：**22 窗最优**（S2.47）；买卖比：63 窗最优。**短窗 = 新鲜度敏感（知情交易衰减快）；长窗 = 结构性慢变量。**
3. **指标强度与 prod 相关性负相关**（insider_trx_matrix）
   指标最强 `3qo3Wv5O`（S3.42/F3.06）prod **0.8958 ❌**；指标中等 `vROPEJ8w`（S2.08）prod **0.5517 ✅**。**提交候选排序以 prod 升序为第一原则。**
4. **压 prod 的五条偏离轴**：更长组合窗 / 更粗口径 / 更少几何加工 / 换宇宙与中性化 / 用**差值**而非比值。
5. **跨数据集只能用 vector_neut 残差化，绝不能用 multiply**
   跨数据集相乘：S −1.36 / DD 46.9%、S −3.27 / DD **171.9%**。残差化时「主腿选信息量更大的那个数据集」。

---

## 3. 差距说明（为什么还没提交 / 还有什么没解决）

### 3.1 提交缺口：**只差真人确认**
- 今日 REGULAR 配额 **4 颗，本会话已用 0 颗**。
- `ask_user` 问卷已 **连续 12 次自动超时**（`responseSource=automatic_timeout` / `explicitUserConfirmation=false`）⇒ 按纪律**未执行任何不可逆提交**。
- 已备好 8 颗三绿以上候选（§1.1），其中 `E56YodoJ` 是唯一四绿。
- **需要用户裁定三件事**：
  1. 提交哪几颗（今日 4 颗额度）；
  2. 是否豁免「investability ≥ 0.70」这条**项目自设**线（非平台闸）—— `E56YodoJ` inv_S 0.80 已达标，但 `kqNb7XY6` inv_S −0.37 / `58E3oA3X` −0.22；
  3. `pwdQlr2V` 含 `rank(cap)` ⇒ 塔位是 **[PV, INSIDERS]**，是否接受这个双塔（PV 与 INSIDERS 非 trio 内部，按规则允许，但 PV 塔本季计数为 0）。

### 3.2 RISK 塔缺口：SUB 在 risk59 内部**无解**
- 联动性骨架全部 5 闸（LOW_SHARPE / LOW_FITNESS / LOW_2Y / CW / TO）可同时过，但 **SUB 恒在 0.23–0.53**（闸 0.78–0.97）。
- 机理已定性：联动性收益集中在大盘高流动性股（inv_S 1.83–2.08），子宇宙反而更均匀。
- 已试无效手段：`winsorize`（连续两波有害）、`group_zscore` / `group_neutralize`（连续三波有害）、`ts_rank` 二次包装（归零）、秩差替代（TO 升到 12.5% ⇒ CW 挂）。
- ⇒ **RISK 塔第 3 颗必须靠跨数据集小票腿**，wave278/279 正在做（`O0AqkrA7` 已双塔全闸，只差 prod 0.7832）。

### 3.3 FUNDAMENTAL 塔缺口：两个机制族都被证否
- **成长外推反转**（wave270）：论坛帖 43153154839831 明确写「USA 方向一致」，实测 **7/10 模板 S 为负** ⇒ 帖子的方向声明不可信，必须实测。
- **应计质量因子**（wave272）：Sloan (1996) 的 accruals anomaly 在 USA 已被完全套利（\|S\| ≤ 0.34）。
- 两条独立机制族同向为负 ⇒ **USA 基本面存在系统性「坏消息偏误」**，后续 fundamental 模板的方向假设应先按「取负」起手。
- 剩余未侦察：`fundamental91`（407 字段，命名体系未知）、`fundamental69` / `fundamental93`（tax 数据）。

### 3.4 未完成的在线操作
- **prod 队列被跨会话占用**：本轮多次 `check_correlation` 超时（平台单并发槽，另一会话在跑 GBR）。已实测 prod 的：E56YodoJ 0.6435 / kqNb7XY6 0.6569 / 58E3oA3X 0.6715 / vROPEJ8w 0.5517 / O0Jgd7Y7 0.5655 / LL53QVvn 0.6163 / 1Yj08nb6 0.5796 / XgRM3Yra 0.5803 / 9qxP0JbV 0.5263 / 9qxLOPxr 0.6835 / O0AqkrA7 0.7832 / A1VYRo2w 0.495 / KPJeor68 0.7146。
- **待测 prod**：`kqNbeA2k` / `VkxqKWoJ` / `RREq0gLg` / `JjeYR9ln` / `88v2XRm7`（142h stale 需 refresh）/ `xAr9029b` / `A1VYMrbe` / `zq3QvlL1` / `N1NMdZ7X` 等 INSIDERS 族 12 条。
- **wave279 在飞**（3 数据集组合，含 INSIDERS 新组合）。

---

## 4. 字段画像台账（本次新增 4 份）

| 文档 | 内容要点 |
|---|---|
| `docs/reference/USA/usa_insider_trx_matrix_field_profile_20261030.md` | **OTHER 塔富矿**：29 字段全 MATRIX / cov 0.7642 / **alphaCount 仅 1（低相关红利未折旧）**；7 大机制族 + 判死清单 + 完整窗口曲线 + 「指标 vs prod」对照表 + 四绿候选 |
| `docs/reference/USA/usa_fundamental17_field_profile_20261030.md` | 402 字段 / 4 大机制族（成长 / 质量 / 估值 / 盈利意外）/ **fundamental67 与 fundamental22 的排除依据** / 派发前 5 查 |
| `docs/reference/USA/usa_fundamental93_field_profile_20261030.md` | 应计质量因子：46 字段 uCnt≤12 冷门集 / 应计族 6 种聚合统计结构 / 覆盖分档 |
| `docs/reference/USA/board_gov_stats_field_profile.md` | **既有文档，本轮补充实测**：治理族 7 族分类 / 流动率族判死 / 任期族与网络族有效 / `*_tenure_days` 不能用时序算子 |

---

## 5. 波次结论台账（DB）

`wave_results` 已写入 13 条波次结论（267 / 267s / 268 / 269 / 270 / 271 / 272 / 272b / 273 / 274 / 275 / 276 / 277 / 278），每条含 `key_findings`（结构化归因）与 `batches`（逐模板 alpha 对照）。
`backtest_results` 累计新增 100+ 行（wave267–279），全部带 `code` / 指标 / `ra_failed_checks`。
`ledger_kv["usa_submit_ready_candidates"]` 已固化的完整候选清单（13 颗，含 prod/self/塔位/缺口说明）。
