# GBR 10-alpha 战役 · 中场战报（2026-10-10 凌晨）

> 指令：不换 region（锁 GBR）、已点亮塔不选（MODEL 排除）、锁定 category 深挖、查论坛+论文补灵感、算子全量考虑。
> 本战报覆盖：选类 → 处女池逐探 → 中性化全档扫描 → 首颗可提交候选诞生。

---

## 一、★ 战果：首颗可提交 REGULAR 候选（硬闸全过）

```
alpha_id  e7QVlE6z（同腿对照 1YZOrXQz 亦过线，按「一腿一颗」取 e7QVlE6z 为优）
表达式    group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(
            add(ts_mean(ts_backfill(tm_16_r1_r5_r10_rh_glb_d1_r10_q2_p1,500),1),
                ts_mean(ts_backfill(tm_16_r1_r5_r10_rh_glb_d1_r10_q2_p1,500),120)), sector)),
            std=0.2), lambda_min=0, lambda_max=1, target_tvr=0.45), sector)
settings  GBR / TOP700 / D1 · decay 2 · CROWDING · trunc 0.08 · nanHandling ON · maxTrade ON

S = 1.72 ✅ ｜ F = 1.01 ✅ ｜ 2Y = 1.86 ✅ ｜ TO = 0.193 ✅ ｜ sub_OK ✅
prod = 0.6898 ✅（≤0.70）｜ self = 0.0441 ｜ Failed RA = 0 ｜ 模拟层 17 checks FAIL 0
```
**数据源**：`techindi_model`（OTHER 类，技术指标分位桶模型）—— 正是昨天 coverage 判据修正解锁的池子。
**关键钥匙**：**CROWDING 中性化**（prod 0.7644 → 0.6982，−0.066）+ **tvr 0.40+**（tvr↑ ⇒ prod↓）。

## 二、选类逻辑回执（三维：潜力 × 拥挤 × 文献）

GBR D1 塔：model 5（点亮→排除）｜ analyst 2/3（未点亮但 prod 墙实测）｜ 其余 13 类全 0。
处女池扫描（aCnt≈0–35）→ 按 description 读语义 → 逐池探针：

| dataset | aCnt | 内容 | 探针 | 最强 | 判 |
|---|---:|---|---|---:|---|
| fundamental90 | ~0 | 会计质量库（F-score/C-score/Ohlson/CHS/Mohanram/NOA/iCFROE） | 24 条 | ≤0.28 | ✗ 判死 |
| other567 | 2 | 员工评价（Glassdoor 式） | 16 条 | 0.76 | ✗ 弱 |
| other696 | 0 | 事件情绪计数（正负对偶） | 8 条 | 0.57 | ✗ 弱 |
| earningscall_sentiment | 18 | 电话会 Q&A 情绪 | 8 条 | 0.53（2Y2.13 的 D 形态） | ✗ 弱 |
| analyst69 | ~300 | 一致预期修订 + 前瞻 E/P | 16 条 | 1.11 | ✗ 差 0.47 |
| event_ml_signals | 4 | 激进投资者/破产/审计事件 | 8 条 | 0.66 | ✗ 弱 |

**论坛贡献**（按你的指令）：锁定《基本面稳定性因子》（长窗波动率+线性衰减）、华泰《财务质量因子》
（信号放大/市值分组中性化/量能门控 trade_when）—— 全部实测后判负。

## 三、★ 中性化全档扫描（GBR/D1 合法 11 档全试过）—— 本战役最重要的设置级结论

| 档 | pv47 冠军 | analyst7 冠军 | techindi 冠军 | 判 |
|---|---|---|---|---|
| STATISTICAL（原档） | 全闸 ✅ | 全闸 ✅ | 全闸 ✅ | prod 全 ❌（0.76–0.86） |
| SECTOR / INDUSTRY / MARKET | 2Y 塌 | 2Y 塌 | — | ✗ |
| SUBINDUSTRY | S 差 0.12 / 2Y1.64 | 塌 | S1.14 塌 | ✗ |
| SLOW / RnM | 塌 | **S2.13/F1.71**（RnM）但 prod 未脱钩 | — | ✗ |
| FAST | S0.67 塌 | **S1.97-1.98/F1.41-1.59/2Y1.86-2.10 大超闸** | — | **prod 0.81-0.87 仍卡** ✗ |
| **CROWDING** | 2Y 塌 | 2Y 塌 | **全闸 + prod ≤0.70 ✅** | ★ **唯一活路** |

**★ 核心规律（新沉淀）**：
1. **prod 拥挤对 analyst7/pv47 是「机制级」的** —— 换任何中性化档都不脱钩（池子里全是同类修正/反转信号）；
2. **CROWDING 只对「池里本来就稀缺」的信号有效**（techindi 技术指标分位桶）；
3. **FAST / REVERSION_AND_MOMENTUM 能把 analyst7 的 IS 推到 S1.97–2.13**（储备档，若池子未来变化可启用）。

## 四、当前记分牌

```
目标：10 颗可提交 REGULAR ｜ 已锁定腿：1（techindi × CROWDING）
同腿候选（选一）：e7QVlE6z（prod 0.6898，S1.72）/ 1YZOrXQz（prod 0.6982，S1.65）
```

## 五、剩余路径与诚实评估

**已穷尽**：① 六类封死形态（prod 墙/2Y 塌/F 卡/D 形态/同语义反向/未测池无信号）② 中性化 11 档全扫
③ 处女池 6 集全弱 ④ techindi 单一腿（q1 2Y 差 0.05、r5_q1 F 差 0.06、tm_15 模型弱）。

**未探尽（期望递减）**：news23 / fundamental1 / alpha_factor_lib / other455（N2V 竞争网络 PCA 因子）/
news54 / continuation_score / pv20 余部 / dl_riskfree_returns 余部 / fundamental72（519 UNKN_COV）。

**诚实评估**：GBR 内再出 9 条「全闸 + prod≤0.70」的腿，按当前证据**概率低**。
建议：先把这 1 颗落袋（提交权在你），同时我按剩余清单继续低强度扫描；若你接受，也可考虑
「同池多腿但 self-corr 允许」的边界情形（techindi 不同模型/桶的 self-corr 实测值还没测过两两矩阵）。
