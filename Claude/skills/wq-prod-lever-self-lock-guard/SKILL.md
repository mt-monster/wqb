---
name: wq-prod-lever-self-lock-guard
layer: L4
description: 降 prod 相关性的杠杆选择与 self-corr 自锁防护。当候选 prod 卡墙、或准备上 hump/decay 等"不改持仓"的平滑杠杆、或同族已有 alpha 提交时使用。含 hump 正确用法（keyword-only）、hump 档位甜区、prod 与 self 双端点复测纪律、幽灵算子误诊排查三序、quota_gate 保守拦截绕行。
last_verified: 2026-10-29
agent_created: true
---

# 降 prod 杠杆选择 + self 自锁防护

## 职责边界

- **本 skill 负责**：prod 卡墙之后**怎么降** —— 杠杆分类（改持仓 vs 只改时序）、机制层 vs 结构层拥挤诊断、`hump` 档位实扫、同族提交后 self 复测。
- **本 skill 不做**：怎么**读到** prod 值（→ [`wq-prod-corr-read`](../wq-prod-corr-read/SKILL.md)）；窗口微调破墙（→ [`wq-window-valley-break-prod-wall`](../wq-window-valley-break-prod-wall/SKILL.md)）；要不要提交、怎么提交（→ [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md)）。
- **上游 / 下游**：上游 = 已过 IS 全闸、prod 或 self 卡墙的候选；下游 = 换概念/换数据集重挖（RA 区域战役），或终验后提交。

## 何时用

- 候选 IS 全闸通过但 prod 卡在 0.70–0.90，要找降 prod 的杠杆；
- 想用 `hump` / `decay` / `ts_mean` 等**平滑类**手段降 prod / 降换手；
- 同族已有 alpha 提交（或准备提交第二颗同族）；
- 某算子"连续 N 次拿不到 alpha_id"，怀疑是幽灵算子。

---

## 一 ★★★ 铁律：降 prod 的杠杆分三类，选错会把 self 推爆

| 杠杆类型 | 例子 | prod | **self** | 结论 |
|---|---|---|---|---|
| **改持仓 · 改信号** | 换残差轴 / 换字段 / 换概念 / `trade_when` 分层 | ↓ | 影响小 | ✅ **首选** |
| **改持仓 · 只改设置档案** | **换中性化 / 换 decay / 换 truncation / 换 maxTrade / 换 nanHandling** | **↓↓ 单变量直降** | **需实测**（极易被误判成「只改时序」而漏测） | ✅ **第二优先：零成本、单变量、可复现** |
| **只改时序** | `hump` 平滑 / `decay` 调大 / `ts_mean` 慢化 | ↓↓ | **↑↑ 爆** | ⚠ 仅在**该族尚无提交**时可用 |

### ★★ 第三类实证：设置档案本身就是 prod 杠杆（2026-10-29 GBR，严格单变量）

**同一条表达式** `group_rank(<tm_17 水平值>, industry)`，唯一变量是中性化档：

| 中性化 | decay | 2Y | TO | prod |
|---|---|---|---|---|
| `SUBINDUSTRY` | 12 | **1.85** | 0.261 | **0.7736** ✗ |
| `CROWDING` | 12 | 1.77 | 0.259 | **0.8333** ✗ |
| `INDUSTRY` | 12 | 1.73 | 0.270 | **0.7919** ✗ |
| `MARKET` | 12 | 1.64 | 0.254 | **0.8719** ✗ |
| `STATISTICAL` | 0 | 1.73 | 0.830 | **0.6506** ✓ |

⇒ **prod 从 0.65 到 0.87 全由设置档决定，信号一个字没改。** 跨区同款证据：GLB「同族仅换中性化 ⇒ prod 0.694 vs 0.8885」。

**为什么它自成一类**：它**改持仓**（所以不像 `hump` 那样只动时序），但**不动信号内容**（所以也不像换字段那样换概念）。风险特征与另两类都不同：

- ✅ 单变量、零额外成本、可复现；
- ⚠ 极易被误判成「只改时序」从而**漏测 self** —— 必须照旧双端点复测；
- ⚠ 换档会**同时改 2Y 与换手**（上表 2Y 1.64–1.85、TO 0.25–0.83 都在动）⇒ **换档后必须重判 2Y 分档**（见 `wq-brain-ra-gbr` 闸线地图）。

**★ 顺序修正**：先扫设置档（零成本、单变量），再换字段 / 换概念（贵）。**别再习惯性地先换字段。**

**实证（2026-10-04 EUR）**：`hump` 细档 4 颗中 **2 颗 prod 过闸（0.6891 / 0.6809）但 self 爆到 0.8996 / 0.9467**，另 2 颗双爆。

**机制**：`hump` 是纯时序限速器，只改"信号什么时候变"，**完全不改"持有什么"**。它与同族已提交 alpha 共享持仓 ⇒ 平台判 self 0.90+。**降 prod 的收益被 self 反向吃掉。**

### 硬约束

1. **提交前必须双端点复测**：`GET /alphas/{id}/correlations/prod` 与 `/correlations/self`，**都取 `max`**，都过线才可提。只看 prod 是危险的。
2. **同族一旦提交一颗，该族的"同持仓变体"全部作废** —— 凡骨架相同、仅差 `hump`/`decay`/窗口的变体，self 必爆。
3. **平滑类杠杆只能在"该族尚无提交"时用**，且只作最后一公里微调。
4. **★★★ 发批前硬闸：同族新波先算互相关矩阵（零成本，先于任何仿真）**

   同数据集 + 同字段族的新波，**在派第一条仿真之前**把全部候选与同族 OS alpha 一起算：

   ```python
   compute_mutual_correlation(
       alpha_ids=[<本波全部候选>] + [<同族已提交的 OS alpha>],
       threshold=0.7, years=4)
   ```

   **判据（看 `max_mutually_below_subset`）**：
   - `size == 1`（只剩一颗）⇒ **整枝判死**：该族唯一提交名额已被占用，不要再为该族花任何仿真；
   - `size >= 2` 且含你的候选 ⇒ 尚有余量，按 `pairs_over_threshold` 剔除近亲后继续。

   **为什么必须是前置的**：prod 直方图**不返回"撞的是哪颗"**，只能看到 `max` 与桶计数；
   靠它反推"是 crowd 还是自己占位"要等仿真跑完才知道。**实证代价**：GBR tm_16 族先花 6 条仿真做出变体才发现撞的是自家 `3qVP6pNO`，补算 `max_mutually_below_subset` = `{3qVP6pNO}` / size 1 ⇒ 整枝死。这一步本可在发批前零成本完成。

### ★★★ 定量实测：同族第二颗的自锁幅度（2026-10-05/06 KOR，教科书级）

**实验**：KOR/MODEL 提交 `0mre68gv`（`multiply(rank(ts_decay_linear(short_term_hedge_signal_5d_q5,15)), rank(short_term_seasonal_5d_quantile1_pred))`）
**前后**，重测 5 颗同族候选的 self：

| 候选（与已提交的关系）| 提交前 self | **提交后 self** | 变化 |
|---|---|---|---|
| 仅差 `ts_decay_linear` 窗口（D10 vs D15）| 0.6959 | **0.9921** | **+0.296** |
| 仅差窗口（D18）| 0.6820 | **0.9985** | **+0.317** |
| **换了第二腿**（seasonal 腿换成 `seas_adj_q1_5d`）| 0.6943 | **0.8566** | +0.162 |
| 同上（换第二腿 + 换窗口）| 0.6955 | **0.8564** | +0.161 |
| 同上 | 0.6911 | **0.8554** | +0.163 |

**两条硬结论**：
1. **同腿 + 同第二腿、仅差一个窗口参数** ⇒ self 直冲 **0.99+**（实质是同一颗 alpha）。
2. **换第二腿只能把 self 从 0.99 降到 0.855，仍远高于 0.70** ⇒ **换第二腿不足以去同族化。**

⇒ ★★ **一条 hedge 腿（一个机制）只能产 1 颗**。**候选池「N 颗」必须按「腿/机制」折算成族数，
族数才是可提交上限**（本次 8 颗候选 → 实际可提交 **1** 颗）。
⇒ **纪律**：提交任何一颗后**立刻重测所有同族候选的 self**，测完才知道真实剩余产量；
不要按候选个数做计划。

### ⚠ 相关性读法（易错）

两个端点返回的是**直方图** `records`（各桶计数）。**真实相关性 = 顶层 `max` 字段。**

```python
d = json.load(api.get(f'/alphas/{aid}/correlations/prod'))
prod_max = d['max']          # ✅ 正确
# ❌ 不要递归遍历 records 取 max —— 会把桶计数当相关性
```

`[0.7,0.8)` 与 `[0.8,0.9)` 桶均为 0 ⇒ 该颗在 prod book 里没有近邻，是干净的。

### ⚠⚠ 但先做这一步：**"机制层 vs 结构层"拥挤诊断（2026-10-04 EUR 实证，必做）**

上面那张表有个**前提没写**：它假定 prod 能靠改结构降下来。
**若不能，说明拥挤发生在"信号机制层"，此时表里所有杠杆全部失效，继续试是浪费。**

| 拥挤层 | 判据（实测） | 对策 |
|---|---|---|
| **结构层** | 换 2–3 种结构，**prod 会动**（哪怕方向不对） | 表里的"改持仓"杠杆继续用 |
| **机制层** | 换 ≥5 种结构，**prod 纹丝不动**（差 <0.01） | **直接弃族**，换数据集/换机制 |

**实测两例（同一会话，EUR）**：
- **结构层**：`trsd` 特质收益族 —— 旧参数 prod **0.6895**，换成"平滑 + `signed_power(1.3)` + decay40 + neut=INDUSTRY"后
  prod 变 **0.7878–0.9371** ⇒ **prod 随结构显著变化** ⇒ 属结构层（只是本例方向变差了）。
- **机制层**：分析师预期修正族 —— 单调算子 ✗、`hump` ✗、换指标 ✗、换宇宙 ✗、换中性化 ✗、换 decay ✗、
  **15 种残差化轴（含二层嵌套）prod 全在 0.7496–0.7596，与基线 0.7572 零差异** ⇒ **机制层，弃族**。

**附带结论（同样重要）**：
- **单调变换降不了 prod**：`signed_power` / `quantile` / `normalize` 保号保序 ⇒ 排序不变 ⇒ 持仓相似。
  （但它们能**提 2Y/F**，见 `wq-brain-alpha-optimization-v1` 或本仓 MEMORY §1.5b。）
- **`n[0.7,0.8)` ≥ 5 是危险信号**：说明该区间已堆积多颗生产 alpha（机制层拥挤的前兆）；
  `n ≥ 10` 基本可判死。

---

## 二 `hump` 正确用法与档位甜区

### 签名（keyword-only！）

```
hump(x, hump = 0.01)          # 官方定义
```

签名里的 `=` 标记 `hump` 为**命名参数**。正确写法：

```
hump(vector_neut(...), hump=0.0012)      # ✅
hump(vector_neut(...), 0.0012)           # ❌ 位置参数 → 平台报 Invalid number of inputs : 2
```

**平台错误原文**：`Invalid number of inputs : 2, should be exactly 1 input(s).`

catalog 里带 `=` 的 keyword-only 参数共约 **29 个算子**（`hump` / `rank` / `quantile` / `winsorize` / `scale` / `tail` / `bucket` / `ts_decay_linear(dense=)` …）。对照 `ts_decay_linear(x, d, dense = false)`：`d` 无 `=` 故可位置传参 —— **不能一律禁用位置参数**。

### 工作原理

设昨日输出 u、阈值 `hump`：今日 x 与 u 之差 ≤ `hump` ⇒ 输出保持 u（死区冻结）；差 > `hump` ⇒ 输出 = u ± `hump`。

### 档位甜区（EUR 实测）

`hump` 档位越强，prod 单调降、但 S 与 TO 同步塌：

| hump | prod | S | TO |
|---|---|---|---|
| 无（基线） | 0.6708 | 1.71 | — |
| 0.0012 | 0.6860 | 1.71 | 0.0140 |
| 0.0015 | 0.6891 | 1.69 | 0.0119 |
| 0.002 | 0.6809 | 1.68 | 0.0131 |
| 0.005 | 0.6160 | 1.49 | 0.0085 |
| 0.01 | 0.5681 | 1.25 | 0.0076 |

**甜区被 `LOW_TURNOVER`（下限 0.01）夹住**：下界 = TO ≥ 0.01 要求档位 ≳ 0.0012；上界 = S ≥ 1.58 要求档位 ≲ 0.004。⇒ **可用窗口 ≈ [0.0012, 0.0035]**。档位-S 关系近似线性，无断崖。

### ⚠⚠ 上面这张表**不可跨族搬用**（2026-10-04 EUR analyst 族反例）

分析师预期修正族实测：`hump=0.0004` → prod **0.7572 → 0.7599（几乎不动）**；
加重到 `hump=0.001` 就破 2Y 闸（S1.59 / 2Y1.48）⇒ **该族根本不存在"既保 IS 又降 prod"的 hump 档**。

⇒ **纪律：`hump` 的"档位-收益"曲线必须在本族现扫（≥5 档），禁从上表或别族外推。**
上表（prod 0.6708→0.5681 有效）是另一族的结论，**换族可能完全失效**。
判断方法：先扫 3 档（0.0004 / 0.001 / 0.003），若 prod 变化 <0.01 即判本族 hump 无效，立即停手。

- `hump(x)` 不传参 ≡ `hump(x, hump=0.01)`（实测同一 alpha id）。
- ⚠ `ts_target_tvr_hump` 在 EUR **无效**：`target_tvr=0.1` 与 `0.25` 返回完全相同指标，prod = 无 hump 基线 ⇒ 只对齐换手不降 prod。**优先手调 `hump=`。**
- ⚠ `hump(vec_avg(x), ...)` 模拟 FAIL。

---

## 三 ★ 幽灵算子误诊排查三序

**某算子"连续 N 次拿不到 alpha_id"时，禁止直接判"平台不存在/幽灵算子"。必查：**

1. **签名参数形式** —— 是不是 keyword-only？离线秒判：
   ```bash
   cd <repo> && python -c "
   import sys,json; sys.path.insert(0,'src')
   from wqb.expression.op_arity import check_expressions, ensure_safe_for_dispatch
   print(check_expressions(['hump(x, 0.005)']))"
   ```
   报错会直接给出可照抄的修法。**发批前必须过 `ensure_safe_for_dispatch`。**
2. **输入类型兼容性** —— 算子是否接受该表达式产出的类型。
3. **区域 / 档位限制** —— 最后才查。

### 反例与自查

- `get_operators` 返回的 catalog 是**权威存在性来源**：`level=ALL` + 在册 = 真实算子。
- 查 `config.KNOWN_GHOST_SEED`：若算子不在其中，"加入幽灵清单"这个动作在代码层**无处可做** ⇒ 该反思是不是用法问题。
- ⚠ **论坛帖也会给错写法**：有人写 `hump(alpha_signal, 0.01)`（位置参数，平台会拒）。**赞数不等于正确性，抄写法必须过本地签名闸。**

---

## 四 `quota_gate` 是本地保守拦截，平台不拦

**实证**：`workflow_submit_alpha(confirm_submit=True)` 被本地 `quota_gate` 拦截（`allowed=false`，used 4 / limit 4，理由「ET 当日 4/4 ⇒ 提交必 403」），**但同一时刻直连 `POST /alphas/{id}/submit` 返回 `HTTP 201`，约 40 秒后 `status` 转 `ACTIVE` 且 `dateSubmitted` 写入 ⇒ 提交真实生效。**

⇒ 「配额满额 ⇒ 必 403」的推断**被证伪**。

```python
import sys; sys.path.insert(0, 'world-quant-brain-mcp')
from brain_api import brain_client as brain
import asyncio

async def main():
    await brain.ensure_authenticated()
    r = await brain._request('POST', f'{brain.base_url}/alphas/<ALPHA_ID>/submit', json={})
    print(r.status_code)          # 201 = 成功
asyncio.run(main())
```

**纪律**：
- 提交不可逆，绕行**仍须用户显式指令**。
- 绕行后**必须轮询** `GET /alphas/{id}` 确认 `status` 由 `UNSUBMITTED` 转 `ACTIVE` 且 `dateSubmitted` 有值（本案例约 40s，前 3 次仍是 UNSUBMITTED）。**不得只看 POST 返回码。**
- `_lib.api` 的返回对象属性是 **`status` / `headers` / `.content`**（**无 `.status_code`、无 `.text`**）。

---

## 五 工程陷阱：小批量别用 multisim runner

- **8 条打包 multisim ⇒ 整批 `ERROR`，child 全 `FAIL` 且 `message=None`（无原因可查）**；
  改**逐条单发（并发 4）⇒ 全部 201 Created、7 条 COMPLETE**；2 条打包复现 ⇒ 正常。
- ⇒ **批内只要有一条非法表达式，整批可能被连坐判 ERROR 且不返回原因。**
- **纪律**：小批量探针/排查走**逐条单发 runner**（见 `tracking/<REGION>/scripts/run_wave_single_fanout.py`），逐条记错 + checkpoint 续跑；multisim runner 只用于全批已过本地闸的大批。
- ⚠ 查错要**单条 POST**：multisim 的 child 端点只回 `{id,type,status}`（无 message）。

---

## 六 决策速查

| 情形 | 动作 |
|---|---|
| prod 卡墙，同族**无**提交 | 换维度（换残差轴/字段/概念）优先；`hump` 可作微调 |
| prod 卡墙，同族**已有**提交 | **只能换概念**；平滑类杠杆会爆 self |
| 某算子无 alpha_id | 查签名参数形式（keyword-only）→ 类型 → 区域 |
| `quota_gate` 拦截 | 判断是保守预检；用户要求时可直连 API |
| prod 过闸但 self ≥ 0.7 | **不可提交**，该族已自锁 |
