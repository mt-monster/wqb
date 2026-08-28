# EUR D1 Wave69 ideas — win mix salvage of Wave68 |S|≥1 slow legs

Wave68 RelVal EV/EBITDA `rank(ts_delta(..., 5))` **S1.09 F0.42 TVR16.5** 未过廉价闸，但慢腿自有 IS。
按 EUR win：**0.40 × 慢腿原样 + 0.60 × (v_rev + falling_wedge)**，**禁止** 0.30/0.40/0.30 三腿 resid 模板。
不混 |S|<1 腿。跳过 AFT（近闸已有，弱探针=0）。

## Slow legs
- `rank(ts_delta(rel_val_ev_ebitda_component_score_3, 5))` S1.09
- `rank(ts_delta(rel_val_ev_ebitda_component_score_3, 22))` S0.97
- `rank(predicted_surprise_pct_f12m_ebitda_5)` S0.89 TVR6.6
- CAGR zscore invert S0.90 TVR8.3

## Fast
`avg_similarity_v_reversal_bottom` + `avg_similarity_falling_wedge_pattern`（pattern_scores）
