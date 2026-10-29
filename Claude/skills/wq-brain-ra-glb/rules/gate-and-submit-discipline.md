# GLB 闸门与提交纪律

> **as_of**：2026-10-28 ｜ **来源**：GLB 战役 w92–w151
> **定位**：本区**闸门判定口径**与**提交链纪律**的单一叙述；通用提交链在
> [`worldquant-submit-alpha`](../../worldquant-submit-alpha/SKILL.md)，本文件只写 **GLB 特有**的部分与本区实证。
> 实证明细 → [`../references/_glb-zero-tower-gate-20261028.md`](../references/_glb-zero-tower-gate-20261028.md)。

---

## 1. 平台阈值：**读 `checks[].limit`，不抄字面量**

判定一律读平台 `get_alpha_details` 的 `checks[].limit` / `value`。
本区已实测出**两个跨区通用值不成立**的地方（GLB 与其它区不同 ⇒ **禁止套用其它区的数字**）：

| 检查 | 跨区通用值 | **GLB 实测** | 后果 |
|---|---|---|---|
| `IS_LADDER_SHARPE` / `LOW_2Y_SHARPE` | 跨区下限（见 `config.PLATFORM_CHECK_LINES["low_2y_sharpe_min"]`） | **平台 limit 更高** | 本区 8 颗 PV 候选 2Y 落在下限之下**仍 FAIL** ⇒ 用下限判会**误放行** |
| `HIGH_TURNOVER` | 见 `config.PLATFORM_CHECK_LINES["turnover_range"]` 上界 | 与通用值一致 | 用更严的内部值（`thresholds.json` 的 `review.turnover_max`）判会**误杀** |

⇒ **`thresholds.json` 的 `review.*` 是内部宽松筛，不是平台线**；内部过关的平台仍可能 FAIL。

## 2. RA 失败名单：**取 `ra.ra_failed_checks`，不取 `checks.fail`**

平台把 RA 类失败记在 **`ra.ra_failed_checks`**（并在 `checks.warning` 里以 `WARNING` 呈现），
而 **`checks.fail` 恒为空**（GLB 实测：`88R9ARkm` / `rKObq6mm` / `WjOQX8rj` 的 `checks.fail` 都是 `[]`，
但 `ra_failed_checks` 有 `CONCENTRATED_WEIGHT`）。
⇒ 只读 `checks.fail` ⇒ 把「只差一闸」的候选当成 fRA=0 ⇒ **直接误导提交筛选**（2026-10-28 实测误判 40+ 颗）。
⇒ 本地回测库必须存 `ra_failed_checks` / `two_year_sharpe` / `pyramid_short` 三个字段。

## 3. CW 是 RA 层失败项（不是「恒 WARN」）

旧区域面板写「`cw_gate=WARN` —— 代码尚未读取（闸 7 恒 WARN，CW 在步 7 人工判）」⇒ **已过时**。
2026-10-28 实测：CW 以 `ra_failed_checks=["CONCENTRATED_WEIGHT"]` 出现，**计入 `failed_ra_count`** ⇒
**CW 未过 = 不可提交**，不是「人工判一下」。
⇒ 步 7 遇到 CW：按 [`wq-operator-playbook-by-gate`](../../wq-operator-playbook-by-gate/SKILL.md) §1 的 CW 处方走，
**修不了就换信号腿类型**（本区实证：VECTOR → MATRIX 是唯一有效解）。

## 4. 区域闸（`LOW_GLB_AMER/EMEA/APAC_SHARPE`）

- GLB 独有三个区域闸，只看 `LOW_SHARPE` 会漏。
- **解法优先级第一：换 `FAST` 中性化**（本区第三次独立验证：8 颗 PV 候选 INDUSTRY→FAST 后 fRA 1→0）。
- 其次才是换轴 / 换信号腿。

## 5. prod 纪律（本区特有）

1. **prod 是「持仓形态」的属性，不是「信号」的属性** —— 同一表达式族仅换中性化 ⇒ prod 0.694 vs 0.8885。
   ⇒ **破闸顺序固定：① 修 RA 闸 → ② 重测 prod → ③ 再算互相关 → ④ 才能进篮子。**
2. **同 category 内 prod 差异极大**（PV 域 0.694 ~ 0.9898）⇒ **逐颗实测，不按族推断**。
3. **RISK 域 category 级饱和**（risk60/risk68/risk70 三个数据集 prod 全在 0.80–0.94）⇒ RISK 只能当**门控腿**。
4. **平台 prod 是账号级单并发队列** ⇒ 串行低频、一次 1–3 颗；**别并发**（并发会触发 API 429 并打死其它读路径）。
5. **提交当刻必须 `refresh=True` 重测**（缓存会漂移；本区有候选缓存 0.694 只差 0.006）。

## 6. 点塔算术（提交篮怎么选）

- **「覆盖的不同塔数」≠「点亮的塔数」**：按本批逐塔 +1 算「提交后 ≥3 且提交前 <3」才算点亮。
  本区实证：候选 A 覆盖 5 座塔只点亮 1 座；候选 B 覆盖 4 座点亮 2 座 ⇒ **按覆盖塔数排序会稳定地选错**。
- **打分序**：点亮塔数 → 覆盖塔数 → 两两互相关最大值 → prod 离上限的距离。**穷举**所有合法组合，不贪心。
- **禁混闸优先于一切排序**：PV/MODEL/OTHER 两两混或三塔同现 ⇒ 一律不进篮子（见
  [`worldquant-submit-alpha` 的点塔优选](../../worldquant-submit-alpha/references/quota-and-tower.md)）。
  本区代价实测：2618 行回测里 **47 颗指标很好的候选因混塔不可提交** ⇒ **选波阶段就要避开**。

## 7. 稳健性闸（提交前）

- **声明必须读台账**（`robustness_<alpha_id>`），**禁止硬编码 `True`** —— 2026-10-28 实测台账里当时**篮子 4 颗一颗记录都没有**，
  硬编码会静默放行未审计候选。
- **「近十年都有数据」用 `get_alpha_yearly_stats` 逐年验**（平台 `coverage` 可能是 meta 造假）。
- 台账写入按主键 **merge**、**失败结果不写入**（一次 429 曾把 3 条有效记录冲成错误记录且失败被静默）。

## 8. 配额

- 每 **ET 日历日**：REGULAR 4 + SUPER 1 + PPA 1，**互不占用**，00:00 ET 重置。
- 现值以 `python tools/quota_status.py` 为准（不要在文档里写死「12:00」—— 夏令时/冬令时不同）。
- **批量提交前 30 秒内复检一次**（并行会话共用同一账号配额）。
