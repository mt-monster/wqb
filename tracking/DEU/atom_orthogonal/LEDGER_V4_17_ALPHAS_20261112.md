# ★★★交付台账 v4：17 / 20（85%）

日期：2026-11-12

## 一、17 颗最终篮子（互相关全对 <0.7，最大独立集 17 = 数学上限）

| # | alpha | 状态 | S | F | 2Y | sub | ops | 塔 | eff | 说明 |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---|
| 1 | vR1oxZA3 | ACTIVE | 3.27 | 3.09 | 4.39 | 1.99 |  | （无标记） | — | 存量 |
| 2 | WjlMlWJd | 待授权 | 2.21 | 1.84 | 2.40 | 1.43 | 26 | PV+INSIDERS+ANALYST | 0 | insiders×cap×AN2（压缩版） |
| 3 | RREPm361 | 待授权 | 2.02 | 1.25 | 1.82 | 1.24 |  | ANALYST | — | 存量 |
| 4 | zq3eb7No | ACTIVE | 2.01 | 1.28 | 1.64 | 1.00 |  | ANALYST | — | 存量 |
| 5 | rKRx2Alj | ACTIVE | 1.95 | 1.80 | 2.23 | 1.17 |  | MODEL+ANALYST | — | 存量 |
| 6 | 9qlz29Oe | 待授权 | 1.86 | 1.34 | 2.02 | 0.89 |  | SHORT+NEWS | — | 存量 |
| 7 | MP6OgoPr | 待授权 | 1.81 | 1.21 | 1.56 | 1.44 | 11 | INSIDERS+MODEL | 2 | **B单腿+AS3（逐年无负年）** |
| 8 | 0mPqGEgq | 待授权 | 1.74 | 1.18 | 2.28 | 1.18 | 14 | INSIDERS+MODEL | 2 | **C+F+AS3（新核心）** |
| 9 | npa9PKWw | 待授权 | 1.74 | 1.52 | 2.66 | 0.94 | 37 | INSIDERS+OTHER | 2 | insiders×other455长窗132 |
| 10 | qM7KxkQV | 待授权 | 1.72 | 1.34 | 2.43 | 0.92 |  | SHORT+INSIDERS | — | 存量 |
| 11 | 1YWeGdGz | 待授权 | 1.70 | 1.36 | 2.38 | 1.01 | 9 | INSIDERS+MODEL | 2 | **C+AS4（新核心·最简9算子）** |
| 12 | 78Yk8VR1 | ACTIVE | 1.68 | 1.21 | 2.27 | 0.86 |  | SHORTINTEREST | — | 存量 |
| 13 | Jj8VQwoe | 待授权 | 1.65 | 1.24 | 2.42 | 1.22 |  | SHORT+OTHER | — | 存量 |
| 14 | mLapKbd2 | 待授权 | 1.64 | 1.30 | 3.18 | 0.84 | 9 | INSIDERS+OTHER | 2 | **C+O4（2Y 3.18 最高）** |
| 15 | GrW9OxmG | ACTIVE | 1.62 | 1.56 | 1.93 | 1.19 |  | ANALYST | — | 存量 |
| 16 | bl6AvMkN | ACTIVE | 1.61 | 1.36 | 2.15 | 0.94 |  | MODEL+ANALYST | — | 存量 |
| 17 | d5a2vxzY | 待授权 | 1.60 | 1.08 | 2.05 | 0.76 |  | SHORTINTEREST | — | 存量 |

**验证**：`compute_mutual_correlation(17 颗, threshold=0.7)` ⇒ `all_below_threshold = True`，`max_mutually_below_subset_size = 17`
**加入更多候选后独立集仍为 17** ⇒ 已达上限。

## 二、本轮新增 5 颗（全部合规、全部 eff=2）

| alpha | 构造 | S | F | 2Y | sub | ops | 塔 |
|---|---|---:|---:|---:|---:|---:|---|
| **npa962ex** | B+C+AS3 | **1.98** | 1.39 | 2.56 | 1.33 | 12 | INSIDERS+MODEL |
| **e7am10NE** | A+C+AS3 | 1.89 | 1.29 | 2.25 | 1.24 | 13 | INSIDERS+MODEL |
| **0mPqGEgq** | C+F+AS3 | 1.74 | 1.18 | 2.28 | 1.18 | 14 | INSIDERS+MODEL |
| **1YWeGdGz** | C+AS4 | 1.70 | 1.36 | 2.38 | 1.01 | 9 | INSIDERS+MODEL |
| **mLapKbd2** | C+O4 | 1.64 | 1.30 | **3.18** | 0.84 | 9 | INSIDERS+OTHER |

其中 `npa962ex` 与 `e7am10NE` 因与 `0mPqGEgq` 相关 0.86-0.88 未能入选，作为备选。

## 三、突破的方法论（这是本轮最大收获）

**要出低相关件，必须换核心结构，不是换搭档。**

| 做法 | 结果 |
|---|---|
| 固定 S7 四腿核心 × 换 8 个搭档族 | 全部 0.78-0.83 高相关，5 次独立验证 |
| **换核心为单腿（C / B / F）× 单搭档** | **成功出 3 颗 <0.7 新件** |
| 换核心为双腿（C+F / A+C / B+C）× 搭档 | 出 2 颗，但其中 1 颗与已有件 0.86 冲突 |

**机理**：S7 的四腿（A×C + B×FR + C + B）把 holdings 存量信息榨干，成为主导共同因子。
只保留其中一腿（尤其 C 集中度）时，PnL 驱动因子彻底改变，才能拉开距离。

## 四、塔点亮推演（更新）

| 塔 | 平台当前 | 提交 17 颗后 | 状态 |
|---|---:|---:|---|
| **INSIDERS** | **0** | **8** | ✅ **从 0 直接点亮** |
| ANALYST | 6 | 6 | 已亮 |
| SHORTINTEREST | 3 | 5 | 已亮 |
| MODEL | 3 | 3 | 已亮 |
| **OTHER** | **2** | **4** | ✅ **也将点亮** |
| PV | 0 | 1 | 差 2 |
| NEWS | 0 | 1 | 差 2 |

⇒ **提交 17 颗将同时点亮 INSIDERS 塔与 OTHER 塔两座。**

## 五、缺口 3 颗

需要 3 颗满足：① `checks.fail=[]` ② trio≤1 ③ 与 17 颗互相关 <0.7。

已知可用但已被挤出篮子的高 S 备选（因高相关）：
- `d5apW38x` S 2.36（撞 npa962ex 0.803 / MP6OgoPr 0.7999）
- `d5ap9Akx` S 1.74（撞 e7am10NE 0.7535 / 0mPqGEgq 0.7509）
- `npa962ex` S 1.98（撞 0mPqGEgq 0.8797 / MP6OgoPr 0.8377）

⇒ 下一批应继续「更细的单腿 × 新搭档」或「两腿新颖组合」，并优先尝试**尚未用过的搭档族**（institutions / sentiment / earnings）以拉开距离。