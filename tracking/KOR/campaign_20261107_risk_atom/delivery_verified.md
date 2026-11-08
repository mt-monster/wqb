# 已验收交付件（逐颗终验）

## 交付 #1 · omERn83n —— 全闸通过

MCP get_alpha_details 直查结果（2026-11-07）：

| 项 | 值 | 闸 |
|---|---|---|
| Sharpe | **1.62** | >=1.58 PASS |
| Fitness | **1.23** | >=1.0 PASS |
| 2Y Sharpe | **2.27** | >=1.58 PASS |
| Turnover | 0.1319 | 在档 PASS |
| sub_universe_sharpe | 1.31 | PASS |
| investability_sharpe / fitness | 1.25 / 0.87 | PASS |
| **ra.failed_ra_count** | **0** | **全过 PASS** |
| checks.fail | 空 | PASS |
| checks.warning | 仅 MATCHES_COMPETITION / MATCHES_THEMES | 非阻断 PASS |
| self（先行战役实测） | 0.4211 | <0.70 PASS |
| prod（先行战役实测） | 0.6898 | <0.70 PASS（余量 0.0102） |
| 金字塔 | KOR/D1/RISK x1.3，effective=1 | ATOM 确认 PASS |
| 区间 | 2014-01-01 ~ 2023-12-31 | 10 年 PASS |

**设置**：KOR / TOP600 / D1 / EQUITY · REVERSION_AND_MOMENTUM · decay 1 · truncation 0.04 · unitHandling VERIFY · nanHandling ON · pasteurization ON · maxTrade OFF

**表达式**（9 个算子，<=12）：

    ts_target_tvr_decay(
      signed_power(
        group_rank(
          winsorize(
            vector_neut(
              rank(ts_backfill(rsk70_mfm2_asetrd_anlystsn, 40)),
              rank(ts_backfill(rsk70_mfm2_asetrd_momentum, 22))),
            std=0.38),
          sector),
        2.5),
      target_tvr=0.22)

- 数据集：risk70 MFM2（单数据集 ⇒ ATOM）
- 核心字段：rsk70_mfm2_asetrd_anlystsn（分析师情绪载荷，aC 2922）+ rsk70_mfm2_asetrd_momentum（同集正交控制腿）
- 算子：ts_target_tvr_decay / signed_power / group_rank / winsorize / vector_neut / rank / ts_backfill / rank / ts_backfill = 9
- 机制：把分析师情绪载荷对动量正交化，取剩余特质情绪暴露。属纯 risk-model 载荷，不是 dsrt 反转族，不受 KOR 反转判死影响。

> 该件由先行战役 campaign_20261106_risk_atom 产出，本战役经 MCP 独立复核确认全闸通过。
