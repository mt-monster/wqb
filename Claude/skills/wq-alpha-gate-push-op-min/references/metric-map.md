# 指标 ↔ 杠杆映射（每个闸由哪些旋钮驱动）

> 用途：**拿到缺口后，直接查到该动哪个旋钮**，而不是盲扫。
> 阈值：`LOW_SHARPE ≥ 1.58`｜`LOW_FITNESS ≥ 1.0`｜2Y 闸 `≥ 1.58`（真值需 ≥1.585，因平台四舍五入 2 位后严格比较）｜ <!-- from config.PLATFORM_CHECK_LINES -->
> `SELF_CORRELATION < 0.7`｜`PROD_CORRELATION < 0.7`。 <!-- from config.prod_corr_max -->

---

## 一、公式与恒等式（读懂才能选杠杆）

```
fitness  = sharpe × sqrt(return / max(tvr, 0.125))
```

**两个推论**：
1. **TO > 0.125 时**：降 TO 有二次收益（`fit ∝ 1/√tvr`）。**TO ≤ 0.125 时**：分母被 `max()` 钉住 ⇒ 再降 TO 不提 fit。
2. **S 与 fit 同向**：提 S 自动提 fit；所以**先修 S，fit 往往跟着好**（但 fit 还受 TO/return 影响）。

---

## 二、闸 → 旋钮对照表

| 闸（当前不足） | 首选旋钮 | 次选 | 禁用 |
|---|---|---|---|
| **`LOW_SHARPE` < 1.58** | ① **L1 轴→`sector`**（+0.26~0.29）② **L2 双窗级联**（+0.18） | ③ **L3 `ts_target_tvr_decay`**（+0.03，需 TO>target）④ **L4 `winsorize std=3~4`**（+0.02）⑤ L6 联合（逐 category）⑥ L5 decay 3 微调（+0.01） | neutralization 换档（全降 S）、`group_zscore`/`tail`、腿级归一化 |
| **`LOW_FITNESS` < 1.0** | ① **L5 decay ↑**（TO↓ ⇒ fit↑）② **L3 `ts_target_tvr_decay`**（TO↓） | ③ 提 S（S↑ ⇒ fit↑）④ 提 return（`subtract` 取反向段 / 换样本） | 时间平滑（零和） |
| **2Y 闸（ladder / `LOW_2Y_SHARPE`）< 1.58** | ① **L1 轴→内置轴**（把严检查换宽检查）② **L2 双窗级联**（2Y +0.6） | ③ **字段变体换 `_main`**（2Y 1.88→2.71）④ 拉长窗（252~264）⑤ 降低 TO | 换 neutralization |
| **`SELF_CORRELATION` ≥ 0.7** | ① **换信号样本**（`if_else` 掩码，去相关第 3 维度）② 换字段族 / 换轴 | ③ `group_rank` → `group_zscore`（非保序，须重测 prod） | 同骨架复制（互相关 >0.99） |
| **`PROD_CORRELATION` ≥ 0.7** | ① **换横截面排序**：换 `multiply` 第 2 腿 / 换字段族 / 换轴 | ② 换字段变体（低 aC 变体）③ **`ts_delta`（水平→变化）**  | ⚠ `neutralization` 换档**只降 prod 但同量级降 S**（不是自由杠杆） |
| **`CONCENTRATED_WEIGHT` FAIL** | ① 加 **`ts_sum` 累积**（稀疏事件型）② `ts_backfill`（NaN 型） | ③ 降单股权重（换轴） | 截面过窄型 CW 修不了 |
| **`LOW_SUB_UNIVERSE_SHARPE` FAIL** | 提 S（它是比值闸，limit ≈ 0.47×S） | — | — |
| **`LOW_TURNOVER` / `HIGH_TURNOVER`** | 拉长窗 / 加限速器 | — | — |

---

## 三、「S ↔ prod 前沿」——最重要的结构性认知

**同一信号族里，S 与 prod 严格同向**（2026-10 战役在 shortinterest3 上实测完整个前沿）：

| 构造 | S | prod |
|---|---|---|
| TC×BAR | 1.59 | 0.788 ❌ |
| TC×SKEW×DUR | 1.52 | 0.7272 ❌ |
| TC×DUR | 1.41 | 0.7004 ❌ |
| TC×MV×DUR | 1.29 | **0.6917 ✅** |
| TC×MV | 1.14 | **0.6765 ✅** |

⇒ **在该族里「S≥1.58 且 prod<0.7」不可达**（前端斜率严格为正）。 <!-- from config.PLATFORM_CHECK_LINES, config.prod_corr_max -->
**⇒ 破局的唯一方向不是调参，而是换「横截面排序」**（换字段族 / 换腿 / 换轴）——
这会把点移出原前沿，而不是沿原前沿滑动。

**判据**：若某族内 **S 最高的 3 个变体 prod 全部 > 0.71** ⇒ 该族 prob 墙结构性，停止调参。

---

## 四、指标读取与判定细节

| 事项 | 规则 |
|---|---|
| IS 指标读取 | 原始 API 在 **`is` 下直接展开**（`is.sharpe`/`is.fitness`/`is.checks`），**不是 `is.metrics.*`** |
| 2Y 闸名 | 按轴来源变：数据集 GROUP 轴 ⇒ `IS_LADDER_SHARPE`；平台内置轴 ⇒ `LOW_2Y_SHARPE` |
| 取整规则 | ladder / 2Y 类**四舍五入 2 位后严格比较** ⇒ 目标值取 `limit + 0.005`（即 1.585） |
| `checks` 列表 | 只含仿真时评估的项；`SELF_CORRELATION` / `PROD_CORRELATION` 常为 `PENDING` ⇒ **必须单独调 check 接口** |
| `fails=NONE` 的含义 | 只代表「已评估的项无 FAIL」，**不代表未评估的闸通过**（如当前 S < 1.58 时 `LOW_SHARPE` 可能不在列表里） |
| prod 读数时效 | **>48h 不可信** ⇒ 提交前 `check_correlation(refresh=True)` |
| 相关性池 | self 池可能极小 ⇒ self 低 ≠ 安全；prod 池是全平台 |

---

## 五、达标判定的最小充分集

一个候选「可提交」必须**同时**满足（缺一不可）：

```
① is.checks 全 PASS（含 2Y 闸；注意 ladder 的 +0.005 取整）
② SELF_CORRELATION < 0.7（check_self_correlation） <!-- from config.self_corr_max -->
③ PROD_CORRELATION < 0.7（check_correlation refresh=True） <!-- from config.prod_corr_max -->
④ 同骨架只保留 1 颗（其余 SUPERSEDED）
```

⇒ 达标后**仍需用户授权提交**（`ALLOW_ALPHA_SUBMIT=False` 全局闸锁）。
