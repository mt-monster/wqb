# GBR 会话资产：prod 全表 v2 / multisim 注册表 / 算子经验（2026-11-08）

## 一、GBR prod 相关性权威表（v2，含 2026-11-08 新增；升序）

| alpha | prod | 备注 |
|---|---:|---|
| rKRPAWv9 | 0.3998 | 篮内·NEWS ATOM |
| quant_factor_lib | 0.4455 | |
| RRE5Mwkn | 0.4744 | 篮内·PV+SHORT |
| other315 | 0.4675 | |
| multi_source_model | 0.4916 | |
| bl6KwjwK | **0.4582** | ★新·篮内·SHORT+MODEL（starmine 修订广度） |
| QPvbxjXw | 0.5794 | 篮内·ANALYST ATOM |
| risk68 | 0.5937 | |
| ZYQXZj73 | 0.6524 | 篮内·OTHER+SHORT |
| 3qoGxkqZ | 0.6729 | **0.5 口径出篮**（vs 两颗 0.51/0.54） |
| leAgQPO5 | 0.6866 | 篮内·IMBALANCE+PV |
| **gJerMjKg** | **0.7168** | ✝ 11-08 判死（institutions4 族，浅钉） |
| **P0oALL17** | **0.8384** | ✝ 11-08 判死（insider 族深钉，修补线最优） |
| leAgVON2 | 0.9527 | ✝（mdl216 ARM，S2.67 也救不回） |

（历史区间 0.6994-0.9187 的旧条目见会话摘要/台账，此处只列篮内+本会话新增关键对。）

## 二、本会话 multisim 注册表（2026-11-08）

| id | 臂 | 结果 |
|---|---|---|
| 2tWRLoeP24pTcqI1e7zE3unF | 8 | ✝ 8/8 FAIL 无 message（大批风险实锤） |
| 3jMGj03bl572cBQUzS9ZOu5 | 8 | ✝ 同上 |
| mXBJH9SW5bBbr11eUWbKGd9 | 2 | ✓ 探针：gJerMjKg 复现 + 58E2dQZX 出货 |
| Zar5jgLt59ccuCo6XMHbPs | 2 | ✓ rKRnajx8/P0oAL7kJ 全闸 |
| DgQ0Na2n4mp9FQ14vOlb9sc | 2 | ✓ P0oALL17/58E2dQZX 全闸 |
| 22mJK0a405izaKbt2OJocHK | 2 | ✓ leANm5zN/vR1oQpJa 不过线 |
| rSHYtMo4rp9XL1fmf5hdKB | 2 | ✓ P0oAV7Vp 弱 / **bl6KwjwK 出货** |
| 1K5mlod324sEaECeFgiSnAL | 2 | ✓ LLMwPOQv/npvl1wEd 不过线 |
| 3AibCr9Ki4q09vM28VjG87z | 2 | ✓ j2YJ5zge/88RZm5Lq 不过线 |
| 3LHTiu4WP57qaGNbcIBtyUx | 2 | ✓ news50 xAroAM5m/gJe5JvLQ 弱 |
| 4irnlZ9fU5eGctbj0Jeo2R8 | 2 | ✓ news50 N1NGXZbw/zq3EvVNO 弱 |
| 12Vq9M8GA579ceFBIeVvGn7 | 2 | ✓ news50 翻正 leAYeQEO/88RZ8aGX 弱 |
| 6vqly9Mt…/4uHRuN7l… | 2×2 | ✝ a9 两批 ERROR（GBR 故障） |
| 3f85Ed4Hp4NVar9cNYv02JK | 2 | ✝ 重派仍 ERROR |
| 3VBsZNVF52r9kA3zrddovN | 2 | ✝ 纯 COLD 探针 ERROR ⇒ region 级 |
| 1eOJLY6jM4HHcKJ15BXhpH13 | 2 | ✓ **DEU 对照 COMPLETE**（region 专属铁证） |

## 三、算子/语法新增经验（2026-11-08）

- `ts_target_tvr_decay(core, target_tvr=0.10~0.14)` 压 TO 16.3%→11-12%，F +0.10~0.14 且 S 不降反升——FITNESS 差一档的标准修法。
- `hump(x, hump=0.01/0.02)` 语法可用（预检过）但因大批全灭未获仿真验证。
- 无新增禁用算子；`ts_max/ts_min` 禁令、VECTOR 先 vec_* 等既有禁令全部复验有效。

## 四、跨区闸值与约束速查

| 区 | LOW_SHARPE | 备注 |
|---|---:|---|
| GBR/TOP700 | 1.58 | 当前主战场（region 故障中） |
| CHN/TOP2000U | **2.07** | 2Y 同 2.07、RETURNS≥8%；已判死 |
| EUR/TOP2500 | 未测 | 通道健康；**无 shortinterest category、无 loaned_share_count_main** ⇒ COLD 配方不可平移 |
| DEU/TOP500 | 1.58? | 通道健康（诊断 COMPLETE）；冷腿标尺 0.84 判死 |
