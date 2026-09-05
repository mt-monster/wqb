# pattern_scores breakaway_gap + continuation GEM Ideas (wave123)

**Dataset**: pattern_scores
**Region**: EUR
**Delay**: 1


**Concept**: 向上突破缺口水平（慢腿）
- **Implementation Example**: `rank(ts_mean({breakaway_gap_up_mean_simscore_lookback60}, 66))`
- **Rationale**: 向上突破缺口反映价格强势突破，高缺口预示上涨动力

**Concept**: 向下突破缺口水平（慢腿）
- **Implementation Example**: `rank(ts_mean({breakaway_gap_down_mean_simscore_lookback60}, 66))`
- **Rationale**: 向下突破缺口反映价格弱势突破，高缺口预示下跌动力

**Concept**: 突破缺口差异（慢腿）
- **Implementation Example**: `rank(ts_mean(subtract({breakaway_gap_up_mean_simscore_lookback60}, {breakaway_gap_down_mean_simscore_lookback60}), 66))`
- **Rationale**: 向上-向下突破缺口差异捕捉价格方向，正差异预示上涨

**Concept**: 持续下降楔形（慢腿）
- **Implementation Example**: `rank(ts_mean({avg_similarity_continuation_falling_wedge}, 66))`
- **Rationale**: 持续下降楔形反映价格持续下跌趋势，高相似度预示趋势延续

**Concept**: 持续上升楔形（慢腿）
- **Implementation Example**: `rank(ts_mean({avg_similarity_continuation_rising_wedge_120}, 66))`
- **Rationale**: 持续上升楔形反映价格持续上升趋势，高相似度预示趋势延续

**Concept**: 突破缺口变化（快腿）
- **Implementation Example**: `rank(ts_delta({breakaway_gap_up_mean_simscore_lookback60}, 21))`
- **Rationale**: 突破缺口变化反映价格动力变化，正变化预示上涨加速

**Concept**: 持续形态变化（快腿）
- **Implementation Example**: `rank(ts_delta({avg_similarity_continuation_falling_wedge}, 21))`
- **Rationale**: 持续形态变化反映趋势变化，正变化预示趋势加强

**Concept**: 突破缺口 × 持续形态交互（组合）
- **Implementation Example**: `rank(multiply(ts_zscore({breakaway_gap_up_mean_simscore_lookback60}, 66), ts_zscore({avg_similarity_continuation_rising_wedge_120}, 66)))`
- **Rationale**: 突破缺口与持续形态的交互项，捕捉"突破+趋势延续"与"突破+趋势反转"的差异