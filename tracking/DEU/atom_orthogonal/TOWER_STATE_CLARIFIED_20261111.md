# 塔状态澄清：DEU D1 的 INSIDERS / PV 均为 0 颗（重要纠错）

## 一、先前的错误假设

我在 OS 池看到两颗 `pyramid: INSIDERS` 的 alpha（`9qxdnV72` S1.84、`RRE9NkVj` S1.76，均 2026-11-06 提交），一度以为 DEU INSIDERS 已有 2 颗。

## 二、实际归属（逐条核对 pyramids 字段）

| alpha | pyramids 实际归属 | 区域 |
|---|---|---|
| 9qxdnV72 | **EUR/D1/INSIDERS** ×1.1 | **EUR**（非 DEU）|
| RRE9NkVj | **KOR/D1/INSIDERS** ×1.2 | **KOR**（非 DEU）|

⇒ **DEU/D1/INSIDERS 仍为 0 颗**，`get_pyramid_alphas` 的计数正确。

## 三、DEU D1 全塔状态（当前）

| 塔 | 已有 | 需点亮 | 还差 | 备注 |
|---|---:|---:|---:|---|
| INSIDERS | **0** | 3 | **3** | 我们最强形态 rK7Y2vEJ（PV+INSIDERS）可贡献第 1 颗 |
| PV | **0** | 3 | **3** | 同上（同一颗双计）|
| NEWS | 0 | 3 | 3 | 四类战役已判死 |
| RISK | 0 | 3 | 3 | 四类战役已判死 |
| EARNINGS | 0 | 3 | 3 | 四面证书关闭 |
| institutions | 1 | 3 | 2 | |
| fundamental | 1 | 3 | 2 | |
| sentiment | 1 | 3 | 2 | |
| **已点亮** | ANALYST 6 / MODEL 3 / SHORTINTEREST 3 / OTHER 2 | | | 用户 11-11 指令冻结 |

## 四、战略含义

1. **我们的高 S 形态（1.46-1.55）即使提交，也只能各贡献 1 颗**——离点亮 3 颗还远
2. **塔倍率（get_pyramid_multipliers）**：DEU D1 的 insiders 与 pv 都是 **×1.6**（高倍率区），值得投入
3. **但要真正点亮 INSIDERS 塔，需要 3 颗同类 alpha** —— 我们的三正交结构可以产出多个「不同几何」的版本（加法版/交互版/新鲜度版），只要它们互相关 <0.7 就有机会各占一席

## 五、修正后的路径

**从「做 1 颗最强」改为「做 3 颗互相关低但都过闸」**：
- 已有三个形态族：加法三正交（1.54）/ A×C 交互（1.46/2Y1.53）/ 新鲜度门控（1.55）
- 若三者的 self-corr 都 <0.7，且都能过 S 闸 ⇒ **一次点亮 INSIDERS 塔**
- 但它们目前 S 都在 1.46-1.55，**差 0.03-0.12**，还需破闸