# Wave BE1 — regular alpha 组合波（强腿 x 正交弱腿）2026-11-10 20:0x

> 触发：用户指令「如果实在实现不了ATOM，就考虑regular alpha」。
> ATOM 路线已由三层证据证否（数据集面最高 1.15、OTHER×NEWS 0.86、FUNDAMENTAL×NEWS 0.94）。

## 设计逻辑：不只是提 S，更是换 PnL 结构

现有 19 颗 OS 池把 analyst 族锁死（24 颗纯 analyst 候选 self 全 >0.7，仅 1YNMAA8M 0.6946 过关）。
**但 self 相关性取决于最终 PnL**——把强腿与正交弱腿混合后，PnL 结构改变，self 可能显著下降。
这才是 regular alpha 真正的解锁点。

## 五条臂（全部 == 等级权重，无系数加权，避开毒模式）

| # | 组合 | 塔关系 | 算子 | 设计意图 |
|---|---|---|---:|---|
| E1 | RREPm361(S2.02) + news18 N4(0.57/2Y1.44) | ANALYST x NEWS | 11 | 强 analyst 腿 + 情绪波动腿 |
| E2 | E569ZE7L 简化骨架(S1.68) + N4 | SHORTINTEREST x NEWS | 10 | 借券需求 + 情绪波动 |
| E3 | RREPm361 + other47 W1(0.80/sub1.04) | ANALYST x OTHER（集合外x集合内，≤5 配额） | 11 | 预期修正 + 反关注 |
| E4 | E569ZE7L 简化 + W1 | SHORTINTEREST x OTHER | 10 | 借券 + 反关注 |
| E5 | RREPm361 + E569ZE7L 简化 | ANALYST x SHORTINTEREST（均集合外） | 11 | 两条全清强腿合体 |

（第 6 臂 1YNMAA8M+N4 因 15 算子超限，已剔除）

## 禁混合规核对

禁混集合 = {PV, MODEL, OTHER, FUNDAMENTAL}：
- E1/E2：ANALYST/SHORTINTEREST x NEWS —— **均集合外 x 集合外**，不限量 ✓
- E3/E4：x OTHER —— **集合外 x 集合内**，此类总量 ≤5（本波占 2 个）✓
- E5：ANALYST x SHORTINTEREST —— **均集合外** ✓
- 无 PV/MODEL/FUNDAMENTAL 参与，无集合内两两组合 ✓

## 出口

1. 任一臂 **S≥1.58** ⇒ 立即查 self/prod（这是关键：若 self<0.7 即成为第 6 颗候选）。
2. S 在 1.2-1.58 但 **self 明显低于纯 analyst 族**（<0.6）⇒ 进破闸队列，杠杆=窗口/轴/decay。
3. 全部 S<1.2 ⇒ regular alpha 组合路径也关闭。
---

## BE1 收割前的 self 风险预判（2026-11-10 20:0x）

### 五臂的 self 风险分层

| 臂 | 组合 | 两腿已在池中的 self | 预期 self 走向 | 判断 |
|---|---|---|---|---|
| E1 | RREPm361 + N4 | RREPm361 **0.3275**（健康）；N4 未提交（无 self 记录） | **可能低**（N4 是全新信息面） | ★最优先看 |
| E2 | E569ZE7L骨架 + N4 | E569ZE7L 0.5444；N4 新 | **可能中低** | ★次优先 |
| E3 | RREPm361 + W1 | RREPm361 0.3275；other47 族未在 OS 池 | **可能低** | ★同等优先 |
| E4 | E569ZE7L骨架 + W1 | 0.5444 + 新腿 | 可能中 | 看读数 |
| E5 | RREPm361 + E569ZE7L | 0.3275 + 0.5444（两腿都在池） | **可能最高**（两腿自身与池有交集） | 风险最大 |

### 关键观察：为什么 N4 / W1 是好的「稀释腿」

1. **N4（news18 负情绪波动）从未提交**，OS 池里没有同族件 ⇒ 引入全新 PnL 成分。
2. **other47 族（反关注）从未提交**，同样是全新信息面。
3. **相反，E5 的两条腿都已在池**（RREPm361 虽未提交但属 analyst7 族，与已 ACTIVE 的 zq3eb7No 同族）⇒ self 下降空间最小。

### 乘法结构的先验（来自 1YNMAA8M 的成功）

**1YNMAA8M 的真实表达式是三腿乘法**：
```
multiply(
  multiply(
    group_rank(ts_mean(mean_estimate_change_pct_f12m_earnings_7d_4, 10), sector),
    group_rank(ts_mean(netprofit_y1_estimate_change_3mo, 50), sector)
  ),
  group_rank(ts_sum(anl15_dps_gr_12_m_3m_chg, 22), sector)
)
```
- 它是 **24 颗 analyst 候选中唯一 self 过关（0.6946）的**，而它是**乘法**结构。
- ⇒ **乘法（rank 乘积）比加法更能改变 PnL 结构**，从而降低 self。
- **BE2 应补乘法臂**：`rank(强腿) x rank(弱腿)`，尤其是 × N4 / × W1。