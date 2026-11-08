# GBR 提交执行包 · 10 席篮（seat10 · 2026-11-03）

> 用途：10 条 REGULAR alpha 的一次性提交执行清单（含精确表达式 / 指标 / 提交序 / 终验 SOP）。
> 提交是不可逆动作，逐条执行前必须重测 self/prod（池会漂）。
> 1YNzwl6k 是 2026-11-03 R6 几何换面新锁件（第 10 席）；其余 9 席 2026-11-03 03:47-03:55 快照全过。

## 0. 目标与口径

- 目标：archon goal「锁定 GBR 的 NEWS 点塔，挖 10 个 regular（最好是 ATOM）」。
- NEWS 塔权威账当前 2/3（A1VPlR3l + 58E7jkaN，均 nws17 系 ACTIVE）；**kqNZKN5K 或 rKRPAWv9 任一提交即点亮第 3 塔**（单数据集 news 路线，用户已确认不用门控）。
- 闸线（GBR REGULAR）：S≥1.58 / F≥1.0 / 2Y 分档制（真值≥limit+0.005）/ prod<0.7 严格 / self<0.7 严格；ATOM 只豁免 IS_LADDER_SHARPE。
- 提交前逐条四审：①五闸 ②failed_ra_count=0（WARNING 级也算）③prod 当轮重测 ④self 重测。

## 1. 提交序（干净件先行 → 贴线三件当轮 refresh 立提）

1. rKRPAWv9（prod 0.3998 最净）→ 立刻点亮 NEWS 3/3
2. 1YNzwl6k（prod 0.5188，self 0.12）
3. bl6qldJ6（prod 0.5421；GLB 件，见 §4 协调条款）
4. O0AKLMKq（prod 0.5989）
5. kqNZKN5K（prod 0.6227；NEWS 点塔双保险）
6. vR1aEpa3（prod 0.6632）
7. WjOkLGWx（prod 0.6577，主题厚尾 886）
8. P0gvv5gE（贴线 0.6905）—— 当轮 refresh 立提
9. 9qWwZ3go（贴线 0.6890，中尾 208）—— 当轮 refresh 立提
10. 0mYoANkv（贴线 0.6932，厚尾 662）—— 当轮 refresh 立提

## 2. 10 席明细（指标 2026-11-03 拉取，状态全 UNSUBMITTED / fRA=0）

| # | ID | S | F | 2Y | TO | returns | sub-univ | prod(11-03) | self | 信号 |
|---|----|---|---|----|----|---------|----------|-------------|------|------|
| 1 | rKRPAWv9 | 1.76 | 1.07 | 1.89 | 8.1% | 5.53% | 1.56 | 0.3998 | 0.28 | nws17 事件情绪-相关性对比差（负向 contrarian，TVR 壳） |
| 2 | 1YNzwl6k | 1.73 | 1.06 | 2.30 | 15.4% | 5.78% | 1.36 | 0.5188 | 0.12 | NI/EV 504 日趋势 ts_zscore 几何（R6 新锁） |
| 3 | bl6qldJ6 | 2.59 | 1.02 | 2.02 | 35.3% | 5.77% | 0.97 | 0.5421 | 0.277 | snt21 双否定置信门控 × 预测三分位（GLB 件，OTHER+SENTIMENT 双塔） |
| 4 | O0AKLMKq | 2.28 | 2.00 | 2.21 | 8.8% | 6.12% | 2.42 | 0.5989 | 0.423 | 收益波动门控 × NI/EV 504 趋势 quantile-gaussian |
| 5 | kqNZKN5K | 1.91 | 1.18 | 1.99 | 9.9% | 5.38% | 1.23 | 0.6227 | 0.62 | nws17 事件情绪-相关性对比差（裸版，news17 双子星） |
| 6 | vR1aEpa3 | 2.32 | 2.11 | 2.29 | 12.3% | 6.36% | 2.50 | 0.6632 | 0.524 | 成交量突变门控 × NI/EV 504 趋势 quantile-gaussian |
| 7 | WjOkLGWx | 1.72 | 1.26 | 2.09 | 9.3% | 5.74% | 1.25 | 0.6577 | 0.496 | fnd6 现金/市值 84 日趋势（subindustry 中性） |
| 8 | P0gvv5gE | 1.72 | 1.03 | 1.84 | 12.2% | 5.31% | 1.28 | 0.6905 ⚠ | 0.636 | ep_yield 20 日 delta（TVR 壳，industry 中性） |
| 9 | 9qWwZ3go | 1.67 | 1.09 | 2.21 | 13.4% | 6.23% | 1.64 | 0.6890 ⚠ | 0.595 | mdl28 结构性信用漂移 8 日 delta（TVR 壳，industry 中性） |
| 10 | 0mYoANkv | 1.89 | 1.54 | 2.08 | 11.7% | 5.85% | 1.84 | 0.6932 ⚠ | 0.521 | cap/fnd6_newa2_re 84 日趋势（反向，quantile-gaussian） |

## 3. 精确表达式（复制即用）

回测设置除注明外均为：**GBR / TOP700 / delay 1 / decay 15 / FAST / neutralization 0.05 / truncation 0.08 / unitHandling CLEAN / nanHandling ON / pasteurization ON / maxTrade 0.01 / testPeriod 2016-12-01~2025-12-01**。

### 1) rKRPAWv9
```
ts_target_tvr_decay(group_neutralize(-ts_rank(ts_mean(vec_sum(nws17_multiple_comp_event_sentiment_score), 60), 252), densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)
```

### 2) 1YNzwl6k（R6 几何换面新锁）
```
rank(ts_zscore(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 504), 22))
```

### 3) bl6qldJ6 ⚠ GLB 件，设置 = GLB / TOP3000 / delay 1 / decay 15 / FAST / neutralization 0.05 / truncation 0.01
```
trade_when(rank(ts_mean(snt21_2neg_conf_low_394, 22)) > 0.7, signed_power(subtract(group_rank(predicted_third_quantile_one_day_return_4, exchange), 0.5), 0.5), rank(ts_mean(snt21_2neg_conf_low_394, 22)) < 0.6)
```

### 4) O0AKLMKq
```
trade_when(greater(rank(ts_std_dev(returns, 5)), 0.8), rank(ts_quantile(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 252), 22, driver=gaussian)), -1)
```

### 5) kqNZKN5K
```
ts_rank(ts_mean(subtract(vec_sum(nws17_multiple_comp_event_sentiment_score), vec_sum(nws17_multiple_comp_relevance)), 60), 252)
```

### 6) vR1aEpa3
```
trade_when(greater(rank(ts_zscore(ts_backfill(volume, 22), 66)), 0.8), rank(ts_quantile(ts_av_diff(divide(quarterly_net_income_3, current_enterprise_value), 252), 22, driver=gaussian)), -1)
```

### 7) WjOkLGWx
```
group_rank(ts_quantile(ts_av_diff(divide(fnd6_newq_cheq, cap), 252), 84, driver=gaussian), subindustry)
```

### 8) P0gvv5gE
```
group_rank(ts_target_tvr_decay(rank(ts_delta(ts_backfill(ep_yield_pct_smest_fy1_3, 500), 20)), lambda_min=0, lambda_max=1, target_tvr=0.13), industry)
```

### 9) 9qWwZ3go
```
group_zscore(ts_target_tvr_decay(-rank(ts_delta(ts_backfill(mdl28_sm_structural_credit_structural_asset_drift_pct, 250), 8)), lambda_min=0, lambda_max=1, target_tvr=0.15), industry)
```

### 10) 0mYoANkv
```
reverse(rank(ts_quantile(ts_av_diff(divide(cap, fnd6_newa2_re), 252), 84, driver=gaussian)))
```

## 4. 提交 SOP（逐条执行）

1. 当轮重测 self（corr_check --types self）与 prod（corr_check --refresh 即时取；轮询 unknown 就 prod_wait.py --peek 收值）。
2. 重拉指标 batch_get_alpha_metrics：S/F/2Y 仍过线、failed_ra_count=0、status 仍 UNSUBMITTED。
3. 计算与已提交前序的互相关（compute_mutual_correlation，阈值 0.7）——提交后 OS 池变化，前序变已提交件。
4. 全过才提交（worldquant-submit-alpha skill / POST /alphas/{id}/submit）；任一项破线就跳过该条、不阻塞后续。
5. 提交后回读 get_alpha_details：pyramids.effective 应出现 news category（kqNZKN5K/rKRPAWv9 提交后 category_summary 核验 NEWS=3）。

## 5. 风险与协调条款

- **bl6qldJ6 双计划重叠**：同时在 GBR 10 席篮与 GLB Day-1 提交路线图（reports/glb_mutual_corr_ceiling_and_submit_roadmap_20261103.md）——**只提交一次、两边计数**，执行时与 GLB 计划协调。
- **贴线三件（P0gvv5gE 0.6905 / 9qWwZ3go 0.6890 / 0mYoANkv 0.6932）**：prod 5 天可漂 0.55→1.00（rKRkL9QE 前科），必须当轮 refresh 后立提；如 refresh 撞 0.7+，按浅钉流程（直方图判 n → 几何换面）救援，勿盲提。
- **P0gvv5gE self 0.636 / kqNZKN5K self 0.62**：提交前 self 重测是硬步骤（OS 池加入新件会翻转历史读数，MPYq0819 前科）。
- 提交不可逆：本包只做执行准备，等用户一句明确授权后才动 submit。

## 6. 附：破墙波归因（第 10 席由来）

- pwdQb78v（R6 基线）：S 1.99/F 1.24/2Y 2.34 全过，唯 prod 0.7205 卡墙，直方图 [0.7,0.8) n=1 浅钉。
- R1-R12 十二臂消融：唯一活口 R6 换矩几何 ts_quantile(gaussian)→ts_zscore（prod→0.5188 直方图 n=0，S 仅损 0.26）；R3/R9/R10 换信号矩灭信号（S 0.17-1.09）；R4/R7/R8/R11 壳与分组轴反噬（S 0.29-1.26）；R12 窗口谷对照 S 1.47 且不破钉（与 window-valley skill「n=1 窗口无救 16/16」互证）。
- 定稿方法论已沉淀记忆：**浅钉 n=1 破墙首选=同信号几何换面（quantile↔zscore↔rank），窗口位移无效**。

## 7. 当轮三审快照（2026-11-03 04:1x）

- **self 重测**（平台真值，from_cache=false）：10/10 过——最大 P0gvv5gE 0.6364 / kqNZKN5K 0.6227 / 9qWwZ3go 0.5952，其余 ≤0.53；红线 0.7 全有余量。
- **指标重拉**：10/10 success，failed_ra_count=0，全 UNSUBMITTED；S 1.67–2.59 / F 1.02–2.11 / 2Y 1.84–2.30 全过闸。
- **互相关精确解**（threshold 0.7，years 4）：max_mutually_below_subset_size=10 且 max_subset_exact=true；max_pair 仍 O0AKLMKq↔vR1aEpa3 0.6566；pairs_over_threshold 为空。
- 产物：results/_seat10_final_self.json、_seat10_final_metrics.json、_seat10_final_mutual.json。
- **结论：篮子此刻完全可提交**；但提交是不可逆动作，仍等用户一句明确授权（Goal 模式超时自动选项不构成授权，未执行任何提交）。
