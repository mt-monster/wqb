# EUR × news_sentiment_dl 字段画像（2026-11-09）

> 50/未完（complete=false）；Deep Learning News Sentiment Signals（新闻文本 DL 特征）
> 塔位：OTHER(×1.5)；拥挤度：aC 2 / uC 1（几乎无人用）

## 一、字段结构
三来源（bbguns_enhanced/inferess/trna）× 文本特征：avg_syllables_per_word、avg_words_per_sentence、pos/neg 词的 {max/min/mean} sentiment、词数统计……全部 VECTOR，cov 0.7443-0.7723。纯文本可读性/词频特征，无情绪极性模型分。

## 二、判定
1. **文本可读性特征**（音节/句长）学术先验：可读性差 → 复杂披露 → 负信号（Loughran-McDonald 语境），但效应弱且慢
2. cov 0.74-0.77 < 0.85 → 覆盖判死线不达标
3. aC 2/uC 1 极冷 + 普查表「news_sentiment_dl 未明确」——**判定：覆盖判死 + 低先验，排除**
