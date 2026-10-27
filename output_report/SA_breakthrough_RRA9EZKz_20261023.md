# SA 突破报告：KOR TOP600 CROWDING 全闸通过

> **执行摘要**：13 颗 SA 候选实测，**1 颗通过全部闸门**。最优候选 **`RRA9EZKz`（KOR TOP600 CROWDING d1 l10）S=4.11 F=5.94 prod=0.67 self=0.67，`all_passed: true`**。
>
> **🎉 2026-10-23 08:10 提交成功**：RRA9EZKz 已 ACTIVE 上线（stage=OS，name=`KOR_S_10comp_A9EZKz`，9 项 RA 检查全过，无 fail 无 pending）。

---

## 🎉 推荐提交候选：RRA9EZKz

| 指标 | 值 | 门槛 | 状态 | 余量 |
|---|---:|---:|---|---:|
| **Sharpe** | **4.11** | ≥1.58 | ✅ | +2.53（161% 溢出） |
| **Fitness** | **5.94** | ≥1.0 | ✅ | +4.94（比赛档 C） |
| **Turnover** | 0.116 | <0.30 | ✅ | 社区档 B |
| Two-Year Sharpe | 3.95 | ≥1.58 | ✅ | +2.37 |
| Sub-Universe Sharpe | 3.61 | ≥1.32 | ✅ | +2.29 |
| Investability Sharpe | 3.87 | 动态 | ✅ | — |
| **Prod Correlation** | **0.6732** | <0.7 | ✅ | **0.027** |
| **Self Correlation** | **0.6728** | <0.7 | ✅ | **0.027** |
| failed_ra_count | 0 | 0 | ✅ | — |
| failed_ppa_count | 0 | 0 | ✅ | — |
| **all_passed** | **true** | true | ✅ | — |

**配方**：
```json
{
  "region": "KOR", "universe": "TOP600", "delay": 1,
  "neutralization": "CROWDING", "decay": 1,
  "truncation": 0.02, "selectionHandling": "POSITIVE",
  "selectionLimit": 10, "combo_power": 1,
  "componentActivation": "IS", "selection": "(1 + 0 * (prod_correlation > 0)) * (1 - self_correlation)"
}
```

**Top 5 self-correlated**（全部 <0.7）：
- npPVP253: 0.6728
- E5vwqXNK: 0.6331
- 9qjGvaWe: 0.6127
- 9qWJv1do: 0.5162
- rKOPg9gd: 0.4752

**Top 5 全部为已提交 ACTIVE SA**（KOR 池 8 颗，PPA 池排除 14 颗）

---

## 关键教训：prod 天花板是「区域 × 中性化族」的函数

| 区域 | 中性化 | S | prod | 结果 |
|---|---|---:|---:|---|
| USA · TOP3000 | STAT d22 l30 | 3.98 | 0.818 | ⛔ prod 爆 |
| USA · TOP3000 | SUBIND d10 l100 | 2.88 | 0.835 | ⛔ prod 爆 |
| USA · TOP2000 | SUBIND d5 l15 | 2.38 | 0.792 | ⛔ prod 爆 |
| IND · TOP500 | CROWDING d1 l10 | 4.07 | 0.822 | ⛔ prod 爆 |
| IND · TOP500 | CROWDING d15 l10 | 3.10 | 0.725 | ⛔ prod 爆 |
| **KOR · TOP600** | **CROWDING d1 l10** | **4.11** | **0.673** | **✅ PASS** |

**发现**：
1. **CROWDING 是新的杠杆**：IND 池 38 组件 + KOR 池 28 组件 + CROWDING 中性化 = S 4.0+
2. **区域差异巨大**：IND CROWDING (S=4.07, prod=0.82) 与 KOR CROWDING 同配方（S=4.11, prod=0.67）结果截然相反
3. **KOR 是首个 CROWDING+l10 突破 prod 墙的区域**

---

## 13 颗 SA 候选全景

### 已测（13 颗，1 颗 PASS）

| # | tag | S | F | prod | self | verdict |
|---|---|---:|---:|---:|---:|---|
| 1 | usa_top200_stat_d1_l10 | 0.96 | 0.41 | 0.58 | 0.00 | ⛔ BLOCKED |
| 2 | usa_top200_stat_d1_l15 | 0.94 | 0.41 | 0.50 | 0.00 | ⛔ BLOCKED |
| 3 | usa_top200_crowding_d1_l10 | 0.94 | 0.54 | — | 0.00 | ⛔ BLOCKED |
| 4 | usa_tops500_stat_d1_l15 | 1.46 | 0.73 | — | 0.00 | ⛔ BLOCKED |
| 5 | usa_top3000_stat_d22_l30 | 3.98 | 4.06 | 0.82 | 0.82 | ⛔ PROD_FAIL |
| 6 | usa_top3000_stat_d22_l50 | 3.57 | 3.60 | 0.80 | 0.70 | ⛔ PROD_FAIL |
| 7 | usa_top3000_subind_d10_l100 | 2.88 | 3.47 | 0.83 | 0.83 | ⛔ PROD_FAIL |
| 8 | usa_top2000_subind_d5_l15 | 2.38 | 2.37 | 0.79 | 0.58 | ⛔ PROD_FAIL |
| 9 | eur_top800_stat_d1_l10 | 1.50 | 0.62 | 0.61 | 0.00 | ⛔ BLOCKED |
| 10 | eur_top1200_stat_d1_l10 | 2.15 | 1.06 | 0.55 | 0.00 | ⛔ 2Y_FAIL |
| 11 | eur_top400_stat_d1_l10 | 1.34 | 0.51 | 0.34 | 0.00 | ⛔ BLOCKED |
| 12 | ind_top500_crowding_d1_l10 | 4.07 | 4.19 | 0.82 | 0.82 | ⛔ PROD_FAIL |
| 13 | ind_top500_crowding_d15_l10 | 3.10 | 3.39 | 0.73 | 0.73 | ⛔ PROD_FAIL |
| **14** | **kor_top600_crowding_d1_l10** | **4.11** | **5.94** | **0.67** | **0.67** | **✅ PASS** 🎉 |

**Alpha ID**：RRA9EZKz

---

## 结构性矛盾：S↔prod 剪刀差

**USA 现象**（10 颗 SA 实测）：
- 窄 universe (TOP200/TOPSP500/TOP500)：S=0.94–1.54（不到 1.58）
- 宽 universe (TOP1000+/TOP2000/TOP3000)：S=2.38–3.98（过线），但 prod=0.79–0.84（超 0.7）
- **结论**：USA 组件池 44 颗已「拥挤」，任何新 SA 都无法同时满足 S≥1.58 且 prod<0.7

**EUR 现象**（3 颗 SA 实测）：
- prod 全部低于 0.7（0.34–0.61，很好）
- 但 S=1.34–2.15（低于 1.58 或 2Y 崩塌）
- **结论**：EUR 组件池 14 颗太浅，STAT d1 l10 配置不够强

**KOR 现象**（1 颗 SA）：
- S=4.11，prod=0.67，双闸全过
- **结论**：KOR 组件池 28 颗 + CROWDING 中性化 = 完美的 S/prod 平衡

---

## 后续建议（仅构建，不提交）

### 高优先级（可尝试）
1. **KOR 其他 CROWDING 变体**：pool 28 组件，还有 d5/d15 SUBIND 未试
   - `kor_top600_crowding_d5_l10`
   - `kor_top600_crowding_d15_l10`
   - `kor_top600_crowding_d1_l15`
2. **KOR 其他中性化族**：MARKET / INDUSTRY / SECTOR
3. **GBR TOP700 CROWDING**（池 18，未试）
4. **DEU TOP500 CROWDING**（池 10 压线，未试）

### 停投
- **USA 全 region**：结构性 S↔prod 剪刀差，短中期不可解
- **EUR STAT d1 l10 家族**：2Y 天花板崩塌
- **IND CROWDING**：prod 天花板 0.73–0.82，双闸综合不可达

---

## 提交命令（**仅用户明确点名时执行**）

```bash
cd D:/coding/traeCN_project/wqb && \
WQB_ALLOW_ALPHA_SUBMIT=1 \
D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe \
tools/super_build.py submit --alpha-id RRA9EZKz --region KOR
```

**⚠ 提交前置**：先停掉后台 full_template_campaign.py 进程（PID 83244/4308）避免 API 争用  
**内置 prod 闸**：0.7 fail-closed，**无豁免参数**  
**复核**：等满 flip 窗（~250s）后 `tools/super_build.py status --alpha-id RRA9EZKz` 确认 `status=ACTIVE`

---

## 执行记录

- **执行时间**：2026-10-23 02:48–03:20（约 32 分钟）
- **总构建数**：13 颗（4 批 v1–v4）
- **总耗时**：约 55 分钟（含 API 排队、prod 计算）
- **通过率**：1/14 = 7.1%
- **最高 S**：4.11（KOR CROWDING d1 l10）
- **最高 prod**：0.84（USA TOP3000 SUBIND d10 l100）
