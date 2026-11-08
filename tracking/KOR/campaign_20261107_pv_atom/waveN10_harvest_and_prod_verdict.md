# Wave N10 换轴批 + dl_riskfree 激增族 prod 攻坚终判（2026-11-07）

## A. 本轮新增 prod 实测（全部 MCP check_correlation，串行）

| alpha | 变体 | S | F | 2Y | self | prod | 形态 |
|---|---|---:|---:|---:|---:|---:|---|
| rKRG91g9 | d10×lv60 MARKET | 1.72 | 1.39 | 2.16 | 0.598 | **0.7783** | [0.7,0.8)21钉 + [0.5,0.7)3734 |
| gJeGXMdm | ts_rank126×lv60 MARKET | 1.66 | 1.14 | 2.15 | — | **0.7593** | [0.7,0.8)20钉 + [0.5,0.7)4139 |
| kqNGWN16 | d5×lv60 **industry轴** | 1.79 | 1.19 | 1.83 | 0.545 | **0.7567** | [0.7,0.8)14钉 + [0.5,0.7)2883 |

## B. N10 换轴批 IS 指标（分组粒度单调律再验证）

| id | 轴 | S | F | 2Y | sub | TO | raFail |
|---|---|---:|---:|---:|---:|---:|---:|
| kqNGWN16 | industry | 1.79 | 1.19 | 1.83 | 1.61 | 0.263 | 0 |
| j2YGPYn5 | subindustry | 1.53 | 0.90 | 1.70 | 1.28 | 0.259 | 2 |

分组轴：sector 1.88 > industry 1.79 > subindustry 1.53 —— **细轴降 S**（与 other532 反转族一致的粒度律）。

## C. 14 变体 prod 全景（升序）

| prod | 变体 |
|---:|---|
| 0.7567 | kqNGWN16 d5×lv60 industry轴 |
| 0.7593 | gJeGXMdm ts_rank126×lv60 MARKET |
| 0.7688 | xArGra8W d5×lv60 MARKET（旧最优） |
| 0.7757 | Xg9zabl0 ts_rank×lv60 MARKET |
| 0.7779 | WjOzLZlj d5×lv60 SECTOR |
| 0.7783 | rKRG91g9 d10×lv60 MARKET |
| 0.7804 | omEGEe5b d5×lv22 MARKET |
| 0.7813 | 78Lmo5Y1 d5×lv22 SECTOR |
| 0.7946 | 6Xd0lGxE d5×lv60 RM |
| 0.7986 | 6Xd0A1ZE ts_rank66×lv22 RM |
| 0.8182 | 0mYgpJzK 基准 d5×lv22 RM |
| 0.8255 | 2rA6OVWY winsorize 后置 |
| 0.8271 | ZYQz7XZx d10×lv22 RM |
| 0.8468 | JjezNgLA decay8（反效果） |

## D. ★ 判死结论（符合 prod 判死口径）

实测 14 个结构各异变体（窗口/合取腿/中性化/分组轴/ts_rank包装/decay/winsorize 全覆盖），
prod 全部落在 **0.7567–0.8468** 窄带；最好件距 0.70 仍差 **0.0567**。
每个都是**厚尾**：[0.7,0.8) 14–21 钉 + [0.5,0.7) 成片 2883–4139 颗（非 n=1 单钉）。
累计表达式杠杆仅能 −0.06，无法推出 −0.118 所需位移。

⇒ **「激增信号 × level 门控」机制在 KOR prod 池被结构性占据**，与 insiders5 tnc 水平族同结论。
  根因是机制面撞墙，不是参数没调到位。按纪律：深钉厚尾 ⇒ 判死，不再靠同族变体充数。

## E. 设置层杠杆穷尽确认

get_platform_setting_options：**KOR/D1 仅支持 universe=TOP600**（无 TOP400/TOP200）⇒ universe 换基物理上不存在。
neutralization 已试 RM/SECTOR/MARKET/STATISTICAL；decay 4–16；trunc 0.04–0.12 ⇒ 全部穷尽。

## F. 唯一未封方向：换机制面（非换参数）

同一数据集 dl_riskfree 的**未试结构互异机制**（持仓完全不同 ⇒ 可能绕开 prod 墙）：
1. label0/label1 **模型分歧度**（p1−p0 / ratio，横截面分歧而非激增）
2. **概率期限结构斜率**（5d vs 20d vs 60d 的 term spread）
3. **概率变化加速度**（二阶差分 ts_delta(ts_delta)）
4. **概率历史分位**（ts_zscore/ts_rank 相对自身历史，非激增幅度）
5. **截面离散度 / 分布偏度**（二阶矩）

按用户 SOP「思路阻塞查论坛+论文」补检索后再决定是否派探针波。
