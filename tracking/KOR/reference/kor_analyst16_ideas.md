# KOR delay1 analyst16 GEM Ideas（TOP600 / SECTOR / decay4）

**Dataset**: analyst16
**Region**: KOR
**Delay**: 1


数据集：analyst16（109 VECTOR 字段）。信号白名单见 ledger `s1_analyst16_d1`。
死路规避：评级修正×SH 族（KOR-MLPROJ-RATING-SH-SATURATED）不复刻；评级分布族仅对照。
VECTOR 字段一律 `vec_avg` 聚合后横截面运算。

**Concept**: 盈利意外漂移（post-earnings drift）
- **Mechanism**: 财报实际值超预期的公司在公告后存在持续漂移，意外幅度越大漂移越强
- **Fields**: `anl16_actsurprise`
- **Implementation Example**: `rank(vec_avg({anl16_actsurprise}))`
- **Direction**: 正
- **expected_exposure**: post-earnings drift

**Concept**: SUE 标准化意外情绪
- **Mechanism**: 按历史波动标准化的意外幅度（SUE），剔除公司尺度差异后的纯情绪分
- **Fields**: `anl16_actsuescore`
- **Implementation Example**: `rank(vec_avg({anl16_actsuescore}))`
- **Direction**: 正
- **expected_exposure**: earnings surprise momentum

**Concept**: 一致预期修正动量（estimate revision momentum）
- **Mechanism**: 事件后一致预期均值相对事件前的上修幅度，捕捉分析师集体转向强度
- **Fields**: `anl16_aftercons_difference`
- **Implementation Example**: `rank(vec_avg({anl16_aftercons_difference}))`
- **Direction**: 正
- **expected_exposure**: estimate revision momentum

**Concept**: 归一修正幅度（防大盘股主导）
- **Mechanism**: 修正绝对值除以事件前一致预期均值，得到相对修正率，小盘股不被尺度淹没
- **Fields**: `anl16_aftercons_difference`, `anl16_beforecons_mean`
- **Implementation Example**: `rank(divide(vec_avg({anl16_aftercons_difference}), add(abs(vec_avg({anl16_beforecons_mean})), 0.001)))`
- **Direction**: 正
- **expected_exposure**: revision magnitude

**Concept**: 单分析师盈利预测修正（低拥挤腿）
- **Mechanism**: 个体分析师盈利预测事件后相对变化百分比，users≤6 低拥挤
- **Fields**: `anl16_afterest_percentage`
- **Implementation Example**: `rank(vec_avg({anl16_afterest_percentage}))`
- **Direction**: 正
- **expected_exposure**: analyst revision breadth

**Concept**: 分歧收窄（uncertainty resolution）
- **Mechanism**: 事件前一致预期标准差相对当前分散度的下降=分歧收敛，不确定性消除后的重估
- **Fields**: `anl16_beforecons_stddev`, `anl16_eststddev_normal`
- **Implementation Example**: `rank(subtract(vec_avg({anl16_beforecons_stddev}), vec_avg({anl16_eststddev_normal})))`
- **Direction**: 正
- **expected_exposure**: low-vol / uncertainty resolution

**Concept**: 行业内相对意外（group 骨架）
- **Mechanism**: 盈利意外在行业内相对排序，剥离行业共性后捕捉个股特质信息
- **Fields**: `anl16_actsurprise`
- **Implementation Example**: `group_rank(vec_avg({anl16_actsurprise}), industry)`
- **Direction**: 正
- **expected_exposure**: intra-industry relative surprise

**Concept**: 共识凝聚（预期宽度收窄）
- **Mechanism**: 一致预期最高-最低差相对均值的收窄=分析师共识凝聚，取负方向做多凝聚股
- **Fields**: `anl16_aftercons_high`, `anl16_aftercons_low`, `anl16_aftercons_mean`
- **Implementation Example**: `multiply(-1, rank(divide(subtract(vec_avg({anl16_aftercons_high}), vec_avg({anl16_aftercons_low})), add(abs(vec_avg({anl16_aftercons_mean})), 0.001))))`
- **Direction**: 负（宽度收窄做多）
- **expected_exposure**: consensus convergence