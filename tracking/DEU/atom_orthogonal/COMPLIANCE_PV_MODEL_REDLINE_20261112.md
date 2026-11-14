# ★★合规红线：analyst 腿被平台判为 MODEL ⇒ PV+MODEL 禁混被触发

日期：2026-11-12
依据：Goal 约束第 7 条——「禁止PV,MODEL,OTHER下数据字段两两组腿，不能PV.MODEL,OTHER之间两两组腿，比如出现PV+MODEL,PV+PV，但是可以它们同其它category组腿，比如PV+NEWS，但是这种也仅限于5个数量」

## 一、违规事实

BE138 产出 7 颗 fail=0，最高 S 2.63（`2r5MO67Z`）。但它们的塔归属是：

```
2r5MO67Z  pyramids = [DEU/D1/PV ×1.6, DEU/D1/INSIDERS ×1.6, DEU/D1/MODEL ×1.8]
d5apOzxj  pyramids = [DEU/D1/PV ×1.6, DEU/D1/INSIDERS ×1.6, DEU/D1/MODEL ×1.8]
```

- `cap` 字段 → **PV** 类
- `predicted_surprise_*` / `mean_estimate_change_*` → 被平台归入 **MODEL** 塔（交叉验证：已提交件 `Vk65zLzG` 用同批字段，塔归属同样是 MODEL ×1.8）
- insd1_holdings / significant_value_* → **INSIDERS**

⇒ 三分类并存且含 **PV+MODEL** ⇒ **违反约束 7**。
⇒ **BE138 的 7 颗 fail=0 全部不合规，不能呈交。**

## 二、合规判定表

| 组合 | 分类 | 合规 | 证据 |
|---|---|---|---|
| insiders + cap(PV) | PV+INSIDERS | ✅ | 两类别，非 trio 内部两两 |
| insiders + analyst(MODEL) | MODEL+INSIDERS | ✅ | 两类别，非 trio 内部两两 |
| insiders + cap(PV) + analyst(MODEL) | PV+INSIDERS+MODEL | ❌ | **含 PV+MODEL** |
| insiders + cap(PV) + news(NEWS) | PV+INSIDERS+NEWS | ✅ | PV+NEWS 是 goal 明确举例允许 |
| insiders + analyst + news | MODEL+INSIDERS+NEWS | ✅ | 无 trio 内部两两 |

**关键操作规则：`cap` 桶（PV）与 analyst/model 腿（MODEL）永远不能同时出现。**

## 三、处置

1. **BE138 结果作废**（不作呈交，仅作机制参考：证明 analyst 腿能把 S 从 1.54 推到 2.63）。
2. **BE140**（`2Y4NER90j52Ab2sRS4eGb8E`，10 臂）重派**合规版**：去掉 `bucket(rank(cap))`，外层降为单层 `group_zscore(·,sector)` ⇒ 只留 MODEL+INSIDERS 两类别。
   - 代价：失去 PV 塔归属、失去市值分桶中性化（T9 实测纯 insiders 去 cap 桶 S 1.50→1.25、sub 0.90→0.63）
3. **BE139**（`3942397fx4ZoaeSHZPMMTkb`，insiders × news104 + cap 桶）**合规**，继续跑。

## 四、合规前提下「点塔」的唯一路径

| 想要 | 构造 | 塔倍率 |
|---|---|---|
| PV + INSIDERS 双塔（effective 2）| insiders + cap 桶，**不加任何 trio 类腿** | ×1.6 ×1.6 |
| MODEL + INSIDERS 双塔 | insiders + analyst，**不加 cap 桶** | ×1.8 ×1.6 |
| PV + INSIDERS + NEWS | insiders + cap + news | 待实测 effective |

⇒ 若要「insiders 塔 3 颗点亮」，**最优路径是 insiders+cap（PV+INS, effective 2）**，因为它是唯一实测 effective=2 的合规形态；
或 insiders+analyst 去 cap（MODEL+INS）若能过闸，则同时给 MODEL+INSIDERS 两塔各加 1。
