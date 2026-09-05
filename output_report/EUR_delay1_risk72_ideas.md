**Dataset**: risk72
**Region**: EUR
**Delay**: 1

Note: risk72 = 风险模型残差收益（specific return, % 单位），已做风险因子中性化，与主流 MODEL 金字塔信号天然低相关（prod_corr 墙风险低）。cov≈0.60；36/40 字段 users 0-9 冷门（理论 prod≈0）。残差收益已中性化，勿再叠 group_mean 双重中性化；nocountry/nogroup 变体提交前实测 prod。EUR win recipe：慢 MODEL 残差腿（invert）+ 快 PV pattern 腿，SUBINDUSTRY + decay4。

**Concept**: 残差动量慢腿（Blitz 2011 残差动量）
- **Mechanism**: 风险模型中性化后的残差收益存在数月尺度的动量漂移：个股特质性信息被市场渐进吸收，慢窗均值捕获尚未定价的残余漂移。
- **Fields**: `top2500_equity_residualized_return_nocountry`
- **Implementation Example**: `rank(ts_mean({top2500_equity_residualized_return_nocountry}, 66))`
- **Direction**: 残差动量正延续 → long 高残差漂移股（方向需实测，EUR 反转格局下可能反号）
- **Expected Exposure**: momentum
- **Expected Turnover Band**: low
- **Expected Coverage Band**: wide
- **Why not crowded**: risk72 数据集 EUR 从未挖过（0 alpha），字段 users 0-9；nocountry 残差排除国家因子后与带 country 的主流 MODEL alpha 正交。

---

**Concept**: 残差反转快腿（短期过度反应修复）
- **Mechanism**: 日内/短窗残差收益反映流动性补偿与对特质性消息的过度反应，随后快速修复；1-5 日窗反转是残差收益的经典快信号。
- **Fields**: `top2500_equity_residualized_return`
- **Implementation Example**: `reverse(rank(ts_delta({top2500_equity_residualized_return}, 5)))`
- **Direction**: 短窗残差涨幅高 → short（反转）；方向需实测
- **Expected Exposure**: reversal
- **Expected Turnover Band**: high
- **Expected Coverage Band**: wide
- **Why not crowded**: 快腿反转通常用 raw return 构造，本概念用风险中性化后的残差收益，排除市场/行业/风格共同运动后只剩特质性反转。

---

**Concept**: 风险模型配置分歧（model disagreement）
- **Mechanism**: 同一股票的残差收益在不同风险模型配置（cfg2 top1200 vs top800 宇宙）下估计不同，配置分歧度量模型不确定性；分歧大的股票随后被错误定价修正。
- **Fields**: `cfg2_top1200_residual_return`, `cfg2_top800_residual_return`
- **Implementation Example**: `subtract(rank(ts_mean({cfg2_top1200_residual_return}, 22)), rank(ts_mean({cfg2_top800_residual_return}, 22)))`
- **Direction**: 高分歧 → 待修正方向实测
- **Expected Exposure**: behavioral
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: medium
- **Why not crowded**: 非单字段套壳，而是跨模型配置的差分结构（非对称 shape op1(A)-op2(B)），冷门字段 users 0-9，从未被 EUR 挖掘。

---

**Concept**: alt universe 冷门残差动量（ecs_top1600 覆盖边缘带）
- **Mechanism**: ecs 引擎在 top1600 扩展宇宙的残差收益提供超出 top2500 主流的边际信息；字段 ac=0、users 0-9，几乎无竞争。覆盖边缘用 ts_backfill 稳定序列。
- **Fields**: `ecs_top1600_residual_return_cfg2`
- **Implementation Example**: `rank(ts_mean(ts_backfill({ecs_top1600_residual_return_cfg2}, 66), 66))`
- **Direction**: 残差动量正延续（方向实测）
- **Expected Exposure**: momentum
- **Expected Turnover Band**: low
- **Expected Coverage Band**: medium
- **Why not crowded**: 扩展宇宙残差字段 ac=0，理论上 prod_corr≈0；ts_backfill 处理后覆盖达标即可过体检硬门。

---

**Concept**: minvol 宇宙残差 + crats（低波动残差拥挤修正）
- **Mechanism**: EUR 最小波动率宇宙的残差收益叠加 crats（拥挤调整）变体：低波动股票组合的特质性收益经拥挤修正后仍有稳健漂移（低波动异象的残差形态）。
- **Fields**: `eur_equity_minvol1m_residual_return_crats`
- **Implementation Example**: `rank(ts_mean({eur_equity_minvol1m_residual_return_crats}, 66))`
- **Direction**: 残差动量正延续（方向实测）
- **Expected Exposure**: lowvol
- **Expected Turnover Band**: low
- **Expected Coverage Band**: wide
- **Why not crowded**: crats 变体本身即拥挤度调整字段，users 0-9；minvol 残差与市值/价值主信号正交。

---

**Concept**: win-shape 慢快残差腿混和（EUR region prior 换腿）
- **Mechanism**: EUR 实证 win recipe = 0.4×慢 MODEL 残差腿 + 0.6×快 pattern 腿。本波在 risk72 内做同形状换腿：0.4 慢残差动量 + 0.6 快残差反转，把已验证的权重结构迁移到未点亮残差数据集。
- **Fields**: `top2500_equity_residualized_return_nocountry`, `top2500_equity_residualized_return`
- **Implementation Example**: `add(multiply(rank(ts_mean({top2500_equity_residualized_return_nocountry}, 66)), 0.4), multiply(reverse(rank(ts_delta({top2500_equity_residualized_return}, 5))), 0.6))`
- **Direction**: 慢动量 + 快反转复合（EUR 反转格局下整体通常取负向，方向实测）
- **Expected Exposure**: momentum
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: wide
- **Why not crowded**: 权重形状是 EUR region_kb 实证结晶（win_recipes），换到零竞争数据集做机制迁移；跨数据集策略相关 <0.4 需实测。
