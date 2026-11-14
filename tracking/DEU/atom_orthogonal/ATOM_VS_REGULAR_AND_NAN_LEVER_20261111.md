# ★ATOM 与 regular 口径分离（2026-11-11 22:16 核验）

## 一、9 颗交付件的真实塔构成（get_alpha_details 实测）

| alpha | 数据集（塔） | ATOM? | 设置 |
|---|---|:--:|---|
| GrW9OxmG | ANALYST | **✅ ATOM** | decay=4 / SUBINDUSTRY / nan=OFF |
| zq3eb7No | ANALYST | **✅ ATOM** | decay=0 / FAST / nan=OFF |
| 78Yk8VR1 | SHORTINTEREST | **✅ ATOM** | decay=4 / FAST / nan=ON |
| RREPm361 | ANALYST | **✅ ATOM** | decay=0 / FAST / nan=OFF |
| bl6AvMkN | MODEL + ANALYST | ❌ regular（2塔） | decay=4 / SUBINDUSTRY / nan=OFF |
| rKRx2Alj | MODEL + ANALYST | ❌ regular（2塔） | decay=2 / SUBINDUSTRY / nan=OFF |
| qM7KxkQV | SHORTINTEREST + INSIDERS | ❌ regular（2塔） | decay=4 / SUBINDUSTRY / nan=ON |
| Jj8VQwoe | SHORTINTEREST + OTHER | ❌ regular（2塔） | decay=4 / SUBINDUSTRY / nan=ON |
| vR1oxZA3 | 无塔标记 | ❌ 不适用 | decay=1 / FAST / nan=ON |

**⇒ 严格 ATOM 口径 = 4 颗；regular 口径 = 5 颗。**

## 二、口径对目标达成度的影响

| 口径 | 数量 | 对 10 的达成度 |
|---|---:|---|
| 严格 ATOM（单数据集） | **4** | 40% |
| ATOM + regular 合计 | **9** | 90% |

⇒ 报数时必须分开写，不能笼统说「10 个 ATOM 已达成」。

## 三、★新发现的未验证杠杆：nanHandling

观察：**4 颗 ATOM 件里 3 颗是 `nanHandling=OFF`**（GrW9OxmG / zq3eb7No / RREPm361），
而此前所有批量仿真一律用 `nan=ON`。

**假设**：nan=OFF 让缺失值股票不进组合 → 持仓更集中、信号更纯；nan=ON 把缺失值按中性处理 → 稀释信号。
若成立，那些「S 1.30-1.52 差一点」的臂换 nan=OFF 有可能跨过 1.58。

**BE20 对照（sim 2E3jn95GZ5f5aMmI3Lwy2tN，4 臂，nan_handling=OFF）**：

| 臂 | 内容 | 对照对象（nan=ON 时的实测） |
|---|---|---|
| 1 | nws20 Δ66 × I7 @ group_zscore | P05JM61x：S1.46 / F0.79 |
| 2 | nws20 Δ66 × I7 @ group_rank 外层 | QP010j5W：S1.52 / F0.83 |
| 3 | nws20 Δ66 平滑8 × I7 | wpo83GXx：S1.40 / F1.00 |
| 4 | shrt3 Δ220 × I7（对照组） | qM7KxkQV：S1.72 / F1.34 |

**判定**：臂 4 若明显高于 1.72，或臂 2 越过 1.58 ⇒ nan 是有效杠杆，需回溯重刷历史臂；
臂 4 若与 1.72 基本一致 ⇒ nan 无影响，第 10 颗维持不可行结论。

## 四、另一个待核实项：设置层是未系统搜索的维度

4 颗 ATOM 件的 decay 与 neutralization 各不相同（decay 0/4、FAST/SUBINDUSTRY），
说明提交前曾逐件调过设置。此前精力全在表达式层（窗口/腿/标准化/分组），
**设置层（decay × neutralization × nanHandling）从未做过网格**。
若 BE20 证明 nan 有效，下一步应做「设置层网格」而不是继续改表达式。