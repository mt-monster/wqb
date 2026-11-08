# other47 SEMrush 网站流量 模板池 —— DEU/TOP500/D1 —— 2026-11-03

**机制与取证**：见 `dataset_inventory_2026-11-02.md` other47 节（字段画像 + 2 论文锚 + 论坛对口帖）。
**方向先验**：水平型=负向（Firm Websites & Risk：流量高→信息不对称低→预期收益低）；变化型=正向（Berkeley Digital Footprints：流量加速→营收/股价涨）。
**量纲纪律**：全字段 VECTOR ⇒ 数值位一律 `vec_avg` 包裹；除法分母一律 `add(x, multiply(0.01, x))` 除零保护；水平型分组轴用 `industry` 去规模混淆（禁逐股 ts 归一化）。

## 波 2 收批（Run A 实际载荷版，5 条全 COMPLETE，2026-11-03 03:16）

| 杠杆 | 形态 | alpha_id | S | 2Y | 覆盖 | 判定 |
|---|---|---|---:|---:|---|---|
| L1 窗口对齐 (252,126) | 乘积 | 2rANLXXZ | **1.04** | 1.58 贴线 | 2014-2018 五年连续空窗（T3 族 leading-gap） | ★ 幅度上限仍未到 1.58 |
| L5 T9 反号 | 0−group_rank(ts_delta(rank,66)) | QPv99kZQ | 0.91 | **2.09** | **十年 pnl 全非零，无空窗** | 覆盖最干净；S 弱但 2Y 强=后段集中 |
| L3 几何 neutralize (240,176) | group_neutralize | Xg98n3Rx | 0.83 | 1.52 | — | 换几何反而降 |
| L2 拉长 (504,252) | 乘积 | xArdk22b | 0.75 | 1.02 | — | 长趋势钝化 |
| L4 短窗 (66,22) | 乘积 | omEglbEl | 0.56 | 1.52 | — | 短窗弱 |

**分流判定**：最高 1.04 ∈ [1.0,1.58) ⇒ 再一轮单杠杆（波 3 窗口谷）。窗口轴趋势：240/176=0.99 → 252/126=1.04，甜点在对齐白名单窗口；继续探 (252,66)/(252,22)/(504,66)/价差。
**归因补充**：QPv99kZQ 2Y 2.09 >> S 0.91 = 收益集中在后段（2017 起），但覆盖判据十年无空窗——若波 3 谷底仍 <1.58，它是 other47 里唯一「覆盖干净+2Y 强」的收口保留件。

## 波 3 窗口谷（在飞，task_id=other47_wave3_valley，pid 52340，batch 2/cc 1）

W1 (252,66) / W2 (252,22) / W3 (504,66) / W4 同字段双周期价差 rank(252d)−rank(22d)。预检：verify 4/4 + preflight 零未知零改写。
收批判据（预锁）：任一 S≥1.58 → 破闸（2Y/prod/self/fRA+逐年）；最好 ∈[1.2,1.58) → 谷内再微调一轮；全 <1.2 → other47 收口「机制真、幅度不足」，QPv99kZQ 留档，主力转 news50。

## news50 正式波（在飞，task_id=news50_wave1，pid 53160，12 条 = 10 主 + 2 对照）

载荷 tracking/DEU/news50_wave1_templates.json（合法 settings 白名单格式）。预检：verify 12/12 + preflight 8 字段全存在零改写。收批判据见 s1_news50_template_pool.md（≥1.58 破闸 / [0.8,1.58) 赢单杠杆+反号 / <0.8 判情绪机制弱；逐年覆盖必查）。

## 事故记录（2026-11-03 03:21）：重复派发 + settings 键写坏

compaction 后误判波 2 未派发，用同 task-id 重发 → Run B resume 认不出 CSV 行重交 5 条 → settings 含多余键（pruning/combMethod/decayField）+ 缺 instrumentType → 400 整批拒收（CSV 尾部 5 行 SUBMISSION_FAILED 是污染行，忽略）。Run A 结果未受损。教训已存 Agent 记忆。
