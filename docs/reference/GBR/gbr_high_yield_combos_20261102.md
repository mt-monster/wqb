## 4. 历史库存收割结果（2026-11-02 资格验证，logs/_f72_hist_gate_check.json）

按四层漏斗（fRA=0 / 覆盖无缺口 / self<0.7 / prod<0.7 + 互相关）逐条验证 5 条优先候选：

| alpha | 骨架族 | S/F/2Y/SUB | fRA | self | prod | 判定 |
|---|---|---|---|---|---|---|
| **leA0X7lA** | 模型预测字段+trade_when | 3.41/2.29/2.72/1.94 | 0 | **0.511** | **0.602** | **全绿入篮** |
| qMLAdj7V | 融资/资产 504 延窗 | 1.63/1.12/2.02/1.08 | 0 | 0.691 | **0.935** | prod 撞死 |
| 6Xdw1OqG | 融资/资产 vector_neut | 1.68/1.07/2.42/1.15 | 0 | 0.671 | **0.756** | prod 撞死 |
| 78LwQKYx | 融资/资产 252 源 | 1.70/1.18/1.89/0.98 | 0 | **0.722** | 未测 | self 撞死 |
| 1YNJVzvJ | add 混信号+tvr_decay | 1.62/1.22/2.21/1.39 | 1 | 0.513 | 未测 | CW 挂 |

**结论**：
- **融资现金流/资产反向比值族在 GBR 生产池极度拥挤**（prod 0.93/0.76/0.72 三连撞，直方图 0.7+ 尾巴厚）——
  历史 IS 达标 ≠ 可提交；这一族与 EV 族同命（IS 强、OS 墙死）。
- **leA0X7lA 全闸全绿**（含互相关 vs 篮内 9 条 max 0.067）：主信号 single_bucket_20day_return_estimate_ohlcv_img_2
  （模型预测字段）+ signed_power(subtract(group_rank(·, country), 0.5), 0.5) 非线性截面几何 + trade_when 门控。
  塔位：模型预测×FUNDAMENTAL 门控（trio×非trio 组合，配额用 1）。
- 同主信号的 3qoALER6（换 dividend 门控）S 1.93 但 2Y 1.23 不过 ⇒ 门控选择影响 2Y 结构，值得做变体。
