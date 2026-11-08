# Wave R10 收割 + 归因（COMPLETE 8/8 · **强骨架只对 anlystsn 有效，载荷族无第二强轴**）

- multisim: `31xUXm7Al4ii8PaaxOItLA3`
- 设置：KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay 1 · trunc 0.04 · nanHandling ON（= omERn83n 档）
- 骨架与 omERn83n **完全一致**，只换 PRIMARY_LOADING 字段（隔离字段变量）

## 读数
| id | 主载荷字段 | aC | S | F | TO | 2Y | subS | raFail |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `pwdMvreg` | **btop** | 794 | **0.80** | 0.56 | 0.0943 | **1.44** | 0.89 | 3 |
| `QPvNYkAW` | earnyild | 1795 | 0.73 | 0.48 | 0.0931 | 1.32 | 0.48 | 3 |
| `j2YPeRkj` | divyild | 274 | 0.71 | 0.38 | 0.0768 | 0.39 | 0.51 | 3 |
| `MPYe0Rv8` | earnqlty | 255 | 0.68 | 0.37 | 0.0760 | 1.00 | 0.94 | 3 |
| `omEJo50l` | growth | 551 | 0.47 | 0.20 | 0.0706 | 0.27 | 0.36 | 3 |
| `VkxmdjQV` | profit | 467 | 0.44 | 0.20 | 0.0788 | 1.40 | **0.19** | 4 |
| `xAr2187p` | newssent | 93 | 0.43 | 0.17 | **0.1629** | 0.46 | 0.57 | 3 |
| `LLMm5aY2` | invsqlty | 530 | 0.35 | 0.14 | 0.0699 | 1.01 | 0.41 | 3 |

## ⭐ 核心归因（本条是本战役最重要的负面结论）
**同一骨架、同一设置、同一数据集，只换载荷字段：**

| 主载荷 | S | 相对最强 |
|---|---:|---|
| **anlystsn**（先行战役 omERn83n） | **1.62** | 基准 |
| btop | 0.80 | **0.49x** |
| earnyild | 0.73 | 0.45x |
| divyild | 0.71 | 0.44x |
| earnqlty | 0.68 | 0.42x |
| growth / profit / newssent / invsqlty | 0.35–0.47 | 0.22–0.29x |

⇒ **「载荷 正交于 动量」不是可泛化的机制族**。强信号是 **`asetrd_anlystsn` 这一个字段的单点**，
   不是「risk70 载荷族」的整族性质。9 个载荷字段全测，第二名只有 0.80（S 掉 51%）。

### 与先行战役 10 颗池交叉印证
先行战役池里 risk70 的非-anlystsn 件（S 0.42–1.06）与本轮 R10 读数**同一量级**（0.35–0.80）。
两条独立战役、三套设置档（STATISTICAL·decay4·trunc0.08 / RAM·decay1·trunc0.04 / 先行战役档）
给出**一致结论**：risk70 除 anlystsn 外无 S≥1.1 的字段。

## 次结论：2Y 与 S 在本族仍分离
- 2Y 榜：btop 1.44 > profit 1.40 > earnyild 1.32 > invsqlty 1.01 / earnqlty 1.00。
- S 榜：btop 0.80 > earnyild 0.73 > divyild 0.71。
- **无一颗同时 S≥1.58 且 2Y≥1.58**，最好组合 btop（0.80 / 1.44）仍双欠。
- `profit` sub_universe_sharpe 0.19 ⇒ 尽管 2Y 1.40，子宇宙闸直接挂，不可用。

## 已知失效复核（先行战役预判，本轮实证）
- `btop` prod 0.7322 / `earnyild` prod 0.8383 先行战役已判 prod FAIL ⇒ `pwdMvreg` / `QPvNYkAW`
  即便 S 够线也过不了 prod 闸。**本轮证明它们连 S 都不够，双重出局。**

## 准入 / 禁入
- ⛔ risk70 载荷族（除 anlystsn）**封盘**：再不派发任何「换主载荷字段」的波次。
- ⛔ 不再用「同骨架换字段」做扩产假设 —— 本波已系统性证伪。
- ✅ 唯一还开着的门：**风险量族（srisku/srisk/resvol）× RAM 档**（R12-06/07/08），及 R11 anlystsn 换正交腿。