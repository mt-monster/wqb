# KOR 挖掘经验总结（2026-11-07~09 战役 · campaign_20261107_pv_atom）

> 范围：KOR / TOP600 / D1 / REGULAR（主设置 RAM/d4/trunc0.08/nanON/pasteurON）。
> 本文只记录**本轮实测事实**与可复用规则；推测单独标注。滚动日志：tracking/KOR/campaign_20261107_pv_atom/DELIVERY_KOR_ATOM.md §1-37；快照：DELIVERY_SNAPSHOT_v2_20261109.md。

---

## 0. 一句话结论

**KOR 的瓶颈是「S≥1.58+2Y≥1.58 双闸强度天花板」+「prod 配对墙」**：ATOM 面 192 排名集全部有归宿（可提取 6 颗，已验 5+1 ACTIVE）；非 ATOM 组合面 21 批 118 臂双过线仅 3 例，其中 2 例死于 prod 配对墙、1 例存活（QPvx8M1W 0.6687）。20 颗目标现口径不可达（五轮实证）。

---

## 1. 字段面实证（核心资产）

| 数据集 | 强面 | 弱面/死面 | 备注 |
|---|---|---|---|
| analyst10（640 字段=12 指标×9 角色） | sal_fy2/net_fy1/**pre_fy1** pred_surps_v1（cov 0.83-0.95）；pre 面 2023 仍强（1.45） | smart_ests_v1 裸水平 S≈1.0；revision/innovation 族 TO1.3-1.4 判死 | **sal 面 2023 衰减 0.69（qML REJECT 根因）**；面级差异>指标级 |
| insiders5 | insd5_vol_chg 分歧（vec_stddev+ts_mean55）ATOM 强面（RRE9NkVj ACTIVE） | — | **与之配对普遍撞 prod 墙**（§3） |
| risk68 | weight_volatility_short−weight_dadv 双 ts_delta22 价差（d5Wvpmbx S1.82/2Y4.10/ΔS+0.47，2023=4.69 增强）；dadv 也是干净配对腿 | 组轴变体不构成第二席（互相关 0.69-0.96） | KOR 现役最强 ATOM 面 |
| risk70 | mfm2_asetrd_anlystsn 对 momentum vector_neut 正交 + signed_power2.5 + ts_target_tvr_decay0.22（omERn83n） | — | 9 算子偏多 |
| intraday_pv_feats | corr_bid_price_with_bid_size 反转（ZYQ116ln，3 算子） | — | SLOW/d2 破 prod 墙先例 0.7827→0.6981 |
| other466（字段前缀 oth466_） | ROA=net_inc/assets_tot ts_rank420 窗口谷（LLZ6wZO2 S1.99） | — | **IS 强 ≠ 组合增量**：ΔS=0.0000+diversity 阻断 |
| 判死清单 | — | model31/fundamental94/other545/acquisition_model(百分位近静态)/sentiment21(cov0.475 实测弱)/imbalance5(2Y 历史衰减救不活)/risk62 系(状态量) | 翻案纪律：判死理由必须实测（sentiment21/other466 均曾凭描述误判） |

## 2. 形状/杠杆配方（已验证）

- **GN-industry 外壳 = 近线件真破壁杠杆**：mLoGN(300/Δ66) S1.53/2Y2.04 → QPvx S1.67/2Y2.02/fRA0/prod0.6687。基座依赖（126 基座只抬 S 不救 2Y）。
- **KOR 最强组合骨架**：`hump(subtract(group_rank(慢腿,sector),group_rank(快腿,sector)),hump=0.003)`（同源价差合规）+ 可选 GN(industry)。
- multiply 共振稳定 S1.3-1.4 近线带（多例），单独难过线。
- **S/2Y 前沿负相关**：短窗(126/Δ22)高S低2Y ↔ 长窗(300/Δ66)反之；前沿双达标点稀少（250/Δ66、300+GN）。
- **死杠杆**（本族实测）：STATISTICAL（S 腰斩 0.73-0.94）、CROWDING（1.20 全崩）、trunc0.05（逐位空操作）、adv20 门控（fRA2）、signed_power0.5（2Y+0.20 方向对幅度不足）。
- 水平×交叉动量（论坛 DEU 几何）：机制对（动量腿供 2Y）但 KOR smart_ests 水平基线太弱，不过线。
- **杠杆不跨几何外推（W17 实证）**：pre_fy1 面在 subtract 分歧几何全闸（9qxn S1.58/2Y2.11），同字段在 multiply 共振几何仅 S1.45/2Y1.23——字段面/窗口/中性化增益一律绑定（数据集×几何×配对），换语境必须重测。

## 3. ★prod 墙粒度=配对面（本轮最大方法论增量）

| 件 | anl10 腿 | 配对腿 | prod |
|---|---|---|---|
| E56jA0AP | sal_fy2(250) | insd5_vol_chg | 0.7264 ✗ |
| 9qxnYPjd | pre_fy1(250) | insd5_vol_chg | 0.7025 ✗（换字段只挪 0.024） |
| QPvx8M1W | sal_fy2(300) | rsk68_dadv+GN | **0.6687 ✓** |

- 规则：①族判死 subject=**配对几何**非单数据集；②归因用换腿/换面单杠杆消融；③seal 写到配对级；④贴线 FAIL（差<0.005）不追掷硬币变体（GN 壳与母件 ~0.94 相关 ⇒ prod 同带；贴线 PASS 对日漂脆弱）。
- self≠prod（E56 self 0.6074 过 / prod 挂）；**ΔSharpe 边际服务独立于 prod 槽**（堵死时预检照常）。

## 4. 工具/工程坑（本轮实付学费）

- harvest/lookINTO 必须传完整 URL `https://api.worldquantbrain.com/simulations/<id>`（裸 id 404）。
- margin bp = API 值 ×10⁴（×10³ 会把 24.5bp 写成 2.45bp 误报软标记）。
- `--peek` 空体 ≠ 平台无值（缓存路径与端点不同步）；权威读数=check_correlation(refresh=False)，busy 时按 retry_after 守约不抢槽。
- ts_skewness 幽灵算子连坐整批；偏度用 reduce_skewness(VECTOR) 或手工 Fisher。
- morphology_gate 三坑：bounded_spread 形态臂须含 smoothing（hump/ts_mean）；KOR M5 批次须覆盖 trade_when+adv20；**GN 壳会把臂归入 peer_gap 族**（M4 ≥2 族需配非 GN 几何臂）。
- 平台拥堵 progress 0.35 卡点属常态（10-25min），不是失败。

## 5. 提交链现状（2026-11-09 23:00）

- 确认清单 4 颗：d5Wvpmbx(ΔS+0.47)/QPvx8M1W(+0.28)/ZYQ116ln(+0.24)/omERn83n(+0.10)；参数草案 SUBMIT_DRAFT_20261109.md。
- qMLOooX1 REJECT（2023 衰减）三选一待裁定，W17_QMLREPAIR 修复证据波在飞（2×2 析因：pre/sal × 250/300）。
- robustness 台账 7 条（wqb-db robustness_*）+ reports/robustness_20261109.md。
