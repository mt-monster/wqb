# GBR 10-alpha 战役 · 阶段结题报告（2026-10-10）

> 指令：不换 region（锁 GBR）、已点亮塔不选（MODEL 排除）、不频繁换数据集、查论坛+论文补灵感、算子全量考虑。
> 本报告覆盖两天：方法论整改（骨架多样性）→ 处女池扫描 → 中性化全档扫描 → 首颗可提交候选。

---

## 一、★ 最终战果：1 颗可提交 REGULAR alpha（硬闸全过）

```
alpha_id  e7QVlE6z（首选）｜ 1YZOrXQz（同腿备选）
表达式    group_rank(ts_target_tvr_decay(winsorize(rank(group_neutralize(
            add(ts_mean(ts_backfill(tm_16_r1_r5_r10_rh_glb_d1_r10_q2_p1,500),1),
                ts_mean(ts_backfill(tm_16_r1_r5_r10_rh_glb_d1_r10_q2_p1,500),120)), sector)),
            std=0.2), lambda_min=0, lambda_max=1, target_tvr=0.45), sector)
settings  GBR / TOP700 / D1 · decay 2 · CROWDING · trunc 0.08 · nanHandling ON · maxTrade ON

S=1.72 ✅ ｜ F=1.01 ✅ ｜ 2Y=1.86 ✅ ｜ TO=0.193 ✅ ｜ sub_OK ✅
prod=0.6898 ✅（≤0.70）｜ self=0.044 ｜ Failed RA=0 ｜ 模拟层 17 checks FAIL 0
```

**数据源**：`techindi_model`（OTHER 类，技术指标分位桶）—— 前天 coverage 判据修正解锁的池子。
**分类归属**：OTHER 塔（GBR D1 此前 0 颗）⇒ 提交即点亮新塔。

## 二、达成路径（四段式）

| 阶段 | 关键动作 | 产出 |
|---|---|---|
| ① 方法整改 | 「画像驱动骨架」+ 两级多样性闸门 + 语义×骨架实测矩阵 | 12 族骨架面板 + SEM_PREFERRED v2（实测校准） |
| ② 处女池扫描 | 7 个低拥挤池逐探（全部读 description 定性） | 全弱（≤1.11），判据留档 |
| ③ 中性化全档扫描 | GBR 合法 11 档 × 三大冠军表达式 | **CROWDING×techindi 唯一活路** |
| ④ tvr 梯子 | CROWDING 下 tvr 0.30→0.45 | prod 0.7103→0.7043→**0.6982**→**0.6898** ✅ |

## 三、处女池终局判读（GBR，全部实测）

| dataset | aCnt | 内容（description 读出） | 条数 | 最强 S | 判 |
|---|---:|---|---:|---:|---|
| fundamental90 | ~0 | 会计质量经典库（F-score/Ohlson/CHS/NOA/iCFROE） | 24 | 0.28 | ✗ 死 |
| other567 | 2 | 员工评价（Glassdoor 式，Edmans 机制） | 16 | 0.76 | ✗ 弱 |
| other696 | 0 | 事件情绪计数（正负对偶差） | 8 | 0.57 | ✗ 弱 |
| earningscall_sentiment | 18 | 电话会 Q&A 情绪 | 8 | 0.53 | ✗ 弱（assetutilization 2Y2.13 属 D 形态留档） |
| analyst69 | ~300 | 一致预期修订 + 前瞻 E/P | 24 | 1.11 | ✗ 差 0.47 |
| event_ml_signals | 4 | 激进投资者/破产/审计事件 | 8 | 0.66 | ✗ 弱 |
| other455 | 88 | N2V 竞争网络 PCA 因子（**平台真名 `_value`，本地目录名是错的 `_va`**） | 8 | 0.87 | ✗ 弱 |
| news54 | 9 | 事件时间戳（temporal_meta） | 0 | — | ✗ 描述即判死（未烧波） |
| news23 / fundamental1 | 11/22 | VC 交易数据 / 董事薪酬 | 0 | — | ✗ 同上（稀疏/元数据） |

## 四、★ 中性化扫描的核心规律（本战役最大方法层沉淀）

1. **prod 拥挤对 analyst7/pv47 是「机制级」的** —— 换任何中性化档 prod 都在 0.76–0.87 不脱钩；
   **CROWDING 只救「池里稀缺」的信号**（techindi 分位桶）。
2. **CROWDING 会杀死「本身就是拥挤因子」的信号**（analyst47 情绪 S1.96→0.3；analyst69 E/P S1.11→0.25）。
3. **FAST / REVERSION_AND_MOMENTUM 能把 analyst7 IS 推到 S1.97–2.13**（储备档，pool 若变可启用）。
4. **新纪律（已写入）**：凡 prod 卡墙，宣布死锁前必须先扫「中性化全档 × tvr 梯子」。

## 五、记分牌与诚实评估

```
目标 10 颗 ｜ 已锁定 1 颗（e7QVlE6z，OTHER 塔）｜ 缺口 9
techindi 家族内部 self-corr 实测 0.88–0.94 ⇒ 同池只能出 1 颗（一腿一颗纪律）
```

**诚实结论**：GBR 的可提交空间在本轮证据下≈1 颗。继续挖剩余池（fundamental72 余部 519、
dl_riskfree_returns 余部、continuation_score 等）期望产出递减；**建议先把 e7QVlE6z 落袋**，
剩余配额投入「候选池组合优化」或等新字段上线。

## 六、过程纪律自检

- 骨架两级闸门本日拦下我 **3 次**违规波（2 次模板单一、1 次字段级不足）+ op-lint 拦下 1 个非法算子 `ts_max`；
- 我自己仍有 **2 次边缘违规派发**（62% 单模板，oth455 两波）—— 已记录，后续 dispatch 将把闸门做成硬阻断；
- 回测脚本全部带断点续跑；所有收割行落库（backtest_results 今日 +~200 行）。
