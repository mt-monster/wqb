# EUR D1 news50：画像约束后的新闻分歧

## 字段
字段均来自本轮 EUR / TOPCS1600 / D1 的平台字段扫描，具体绑定列于各 Concept 的 Fields 行；字段白名单及类型记录在 s1_news50_d1。

## 特征
按可证伪经济机制设计；主信号、分母和事件门控的角色由各 Mechanism 描述限定。只保留 GEM 实现的概念原式，自动添加的同字段模板变体不纳入本轮回测。

## 建议
以下 Implementation Example 是概念实现契约。先经过 GEM 生成、语法/类型/画像预检，再进行有限首批验证；未达到资格线不得开展参数优化。


**Dataset**: news50
**Region**: EUR
**Delay**: 1

全部 VECTOR 必须 vec_avg。范围 EUR TOPCS1600 D1 REGULAR。体检包明确：weekly>=52、monthly>=120、quarterly>=252；统一 252 标准窗口，避免跨字段窗口错配。所有 ID/tag/time/category 禁作数值信号。禁止加权混合、PV、MODEL。下述每项具体字段精确绑定，不做后缀替换。冷门字段全部 users<=9。继承胜绩的 surprise-residual 机制，不继承饱和字段。

**Concept**: Recommendation revision against broad tone
**Mechanism**: Analyst recommendation news relative to composite tone reveals disagreement about fundamentals; long the relatively strong recommendation signal.
**Fields**: mws50_ghc_lna, mws50_ssc.
**Implementation Example**: `subtract(rank(ts_backfill(vec_avg({mws50_ghc_lna}),252)),rank(ts_backfill(vec_avg({mws50_ssc}),252)))`

**Concept**: Impact versus granular tone surprise
**Mechanism**: News projected to matter economically but not scored optimistically contains unincorporated impact information; test the historical residual mechanism on independent news fields.
**Fields**: mws50_nip, mws50_ess.
**Implementation Example**: `subtract(rank(ts_backfill(vec_avg({mws50_nip}),252)),rank(ts_backfill(vec_avg({mws50_ess}),252)))`

**Concept**: Earnings evaluation versus released facts
**Mechanism**: The evaluation classifier versus the release classifier separates interpretation from facts, a falsifiable news disagreement signal.
**Fields**: mws50_bee, mws50_ber.
**Implementation Example**: `subtract(rank(ts_backfill(vec_avg({mws50_bee}),252)),rank(ts_backfill(vec_avg({mws50_ber}),252)))`

**Concept**: Specialist versus aggregate language
**Mechanism**: The specialist equity classifier relative to the generic composite tone captures company-specific information.
**Fields**: mws50_qcm, mws50_ssc.
**Implementation Example**: `subtract(rank(ts_backfill(vec_avg({mws50_qcm}),252)),rank(ts_backfill(vec_avg({mws50_ssc}),252)))`

**Concept**: Persistently positive event share
**Mechanism**: Higher positive-event share over the package's trailing 91-day event window may indicate persistent good news; use its slow cross-sectional state as a simple baseline.
**Fields**: mws50_aes.
**Implementation Example**: `group_rank(ts_backfill(vec_avg({mws50_aes}),252),subindustry)`

**Concept**: Corporate action interpretation
**Mechanism**: A quarterly revision in the corporate-action sentiment classifier measures changing expectations around corporate policy, not broad market sentiment.
**Fields**: mws50_acb.
**Implementation Example**: `rank(ts_delta(ts_backfill(vec_avg({mws50_acb}),252),252))`

**Concept**: Mergers interpretation
**Mechanism**: M&A classifier intensity compares firms within their industry; this is a distinct economic source from generic earnings news.
**Fields**: mws50_bam.
**Implementation Example**: `group_rank(ts_backfill(vec_avg({mws50_bam}),252),subindustry)`

**Concept**: Rising event attention activates directional tone
**Mechanism**: Only refresh the composite-tone position when non-neutral event volume grows; event volume is a gate, never an additive alpha leg.
**Fields**: mws50_vea, mws50_ssc.
**Implementation Example**: `trade_when(greater(ts_delta(ts_backfill(vec_avg({mws50_vea}),252),252),0),rank(ts_backfill(vec_avg({mws50_ssc}),252)),-1)`
