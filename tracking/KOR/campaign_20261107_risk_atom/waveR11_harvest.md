# Wave R11 收割 + 归因（COMPLETE 8/8 · **换正交腿能救 2 颗到 S 1.2+，但都差 S 线**）

- multisim: `Be8ib7qH5hmbBw14ULGjugm` · 设置 KOR/TOP600/D1 · RAM · decay1 · trunc0.04 · nan ON
- 骨架与 omERn83n 完全一致，primary 固定 anlystsn，只换「被正交掉的腿」

| id | 正交腿 | S | F | TO | 2Y | subS | raFail | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `e75V6zQl` | **srisk** | **1.29** | **1.03** | 0.1285 | **2.13** | 1.00 | **1** | 仅 LOW_SHARPE |
| `xAr21j3m` | resvol | 1.23 | 0.91 | 0.1238 | 1.71 | 1.03 | 2 | LOW_SHARPE / LOW_FITNESS |
| `akKQV7b6` | beta | 0.58 | 0.26 | 0.1234 | 0.57 | 0.47 | 4 | 多闸 |
| `2rAXjlmZ` | indmom | 0.47 | 0.17 | 0.1466 | 1.77 | 0.26 | 4 | 多闸 |
| `O0AMJ78J` | ltrevrsl | 0.13 | 0.03 | 0.1169 | 0.42 | 0.02 | 5 | 多闸 |
| `N1NJe7Q8` | size | -0.02 | 0.00 | 0.1169 | -0.50 | -0.30 | 5 | 多闸 |
| `Vkxmd7a5` | earnyild | -0.07 | -0.01 | 0.1157 | -0.98 | -0.15 | 5 | 多闸 |
| `RRElA7bb` | btop | -0.28 | -0.09 | 0.1161 | -0.77 | -0.28 | 5 | 多闸 |

## 结论 1：正交腿是有序的强杠杆，且最优腿已找到
按「剥离什么」排序：**srisk 1.29 > resvol 1.23 > beta 0.58 > indmom 0.47 > ltrevrsl 0.13 > size -0.02 > earnyild -0.07 > btop -0.28**
- 经济解读：把 anlystsn 对**同族风险量（srisk）/残差波动（resvol）**正交后留下的特质情绪暴露最纯；
  对**风格估值（btop/earnyild）**或**规模（size）**正交会把信号抹掉 —— 说明 alystsn 载荷里最有用的成分本就与估值/规模共线。
- 与先行战役一致：对 momentum 正交给 omERn83n（momentum 未在本轮，故 1.62 仍是最强腿组合）。

## 结论 2：⚠ `ts_target_tvr_decay(target_tvr=0.22)` 在本族是 **no-op**
按 wq-alpha-gate-push-op-min 杠杆阶梯 L3：**只有 TO > target_tvr 时才激活**。
本族 TO = 0.1157–0.1466，**全部 < 0.22** ⇒ 最外层那个算子在全部 8 条里都不起作用。
⇒ ① 可以直接删掉它省 1 个算子（指标不变，须实测确认）；
   ② 若想真激活平滑，target_tvr 必须设到 **0.10 以下**（如 0.08），此时才会 TO↓/fit↑/S 微升（阶梯实测 +0.03）。
⇒ 这条同时解释了「为什么 omERn83n 的 S 增益不能归因于 ts_target_tvr_decay」。

## 结论 3：S 线的真实缺口
- `e75V6zQl` S1.29，距 1.58 差 **0.29**。阶梯里能用的活杠杆只剩：
  L3 真激活 target_tvr(0.08) ≈ +0.03、L6 两腿相乘 ≈ +0.11、L4 winsorize std↑ ≈ +0.02 ⇒ 合计上限 ≈ +0.16 < 0.29。
- ⇒ **e75V6zQl 结构性达不到 1.58**，xAr21j3m（差 0.35）更不能。

## 交付状态
**1/10**（仅 omERn83n）。本波未新增达标件。
近线件（可作池内低 S 补充，但不能提交）：e75V6zQl(S1.29)、xAr21j3m(S1.23)。