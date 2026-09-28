# submit_ready 梳理与提交优先级计划（2026-09-21）

> 数据源：本地 `submit_ready` 表（62 行）+ 平台实时复验（`check_correlation(refresh=true)` / `check_self_correlation`）
> 复验时间：2026-09-21 16:30 GMT+8｜配额口径：ET 日（12:00 GMT+8 重置），昨日 09-20 已用满 5 颗（REGULAR 4 + SUPER 1）

## 0. 结论先行

| 项 | 数 |
|---|---|
| `submit_ready` 总行数 | 62 |
| 其中 `SUBMITTED`（历史留痕，不可重复提交）| 52 |
| 其中 `IS_ONLY`（仅过 IS 层，且已标 `retired:SUBMITTED`/`superseded-by`）| 13 |
| **本轮复验后真正可提交（READY）** | **9** |
| 本轮实测被拦（标 BLOCKED）| 1 |

**今日建议提交 4 颗（REGULAR 配额）**：`d5bnE8jJ` → `j2AXkdKO` → `P02wbJAM` → `88jaV5lv`，覆盖 3 个区域、4 个不同骨架。

## 1. 复验结果（10 条 READY 全量）

| alpha_id | 区域 | 设置 | IS S/F | 库内 prod | **实测 prod** | 实测 self | 判定 |
|---|---|---|---|---|---|---|---|
| `d5bnE8jJ` | GLB | MINVOL1M d10 SUBIND | 3.62 / 1.49 | 0.6307 | **0.6307** | 0.136 | ✅ 可提交 |
| `j2AXkdKO` | IND | TOP500 d4 STAT | 3.61 / 2.38 | 0.5716 | **0.5790** | 0.572 | ✅ 可提交 |
| `3qX3Mp6O` | IND | STAT | 3.18 / 2.02 | 0.6437 | *未复验（网络）* | 0.644 | ⚠ 需重验 |
| `xA392Xpb` | IND | STAT | 3.18 / 2.00 | 0.6911 | *未复验（网络）* | **0.691** | ⚠ 需重验（self 贴线）|
| `3qX6wLJQ` | IND | TOP500 d4 | 3.07 / 2.34 | ~~0.5171~~ | **0.9895** | 0.518 | ❌ **BLOCKED** |
| `3qX6wLkP` | IND | TOP500 d4 | 2.84 / 1.74 | 0.5836 | *未复验（网络）* | 0.476 | ⚠ 需重验 |
| `88jaV5lv` | ASI | MINVOL1M d12 SECTOR | 2.35 / 1.11 | 0.5093 | **0.5093** | 0.000 | ✅ 可提交 |
| `P02wbJAM` | ASI | MINVOL1M d12 SECTOR | 2.30 / 1.43 | 0.6715 | **0.6715** | 0.000 | ✅ 可提交 |
| `LLNgdpw2` | ASI | MINVOL1M d12 SECTOR | 1.98 / 1.02 | 0.5116 | **0.5116** | 0.000 | ✅ 可提交 |
| `mLmxKN12` | GLB | MINVOL1M d6 SUBIND | 2.99 / 1.69 | 0.6940 | **0.6940** | 0.195 | ⚠ 可提交但余量仅 0.006 |

★ **`3qX6wLJQ` 是本轮最重要的发现**：库内 `prod=0.5171`，**实时复验 = 0.9895**（远超 0.7）→
若直接按库内值提交，会浪费一次提交尝试。已回写真实值并标 `BLOCKED`（备份 `data/wqb.db.bak_readyverify_20260921_163337`）。
→ **纪律复述：提交前一律以 `check_correlation(refresh=true)` 为准，库内 prod 会过期。** 这也意味着同批次的
`3qX3Mp6O` / `xA392Xpb` / `3qX6wLkP`（同为 `add-many clobber` 事故批次）**可信度存疑，必须重验**。

## 2. 推荐批次（按序执行，403 零成本）

| 序 | alpha_id | 区域 | 依据 | 期望 OS（≈0.32×IS）|
|---|---|---|---|---|
| 1 | **`d5bnE8jJ`** | GLB | prod 0.631（余量 0.07）/ self 0.136（最低之一）/ IS 3.62；note 记载 AMER 1.92·EMEA 1.76·APAC 2.76·ladder 4.1 | **≈1.16** |
| 2 | **`j2AXkdKO`** | IND | prod 0.579 / self 0.572 / IS 3.61 | **≈1.16** |
| 3 | **`P02wbJAM`** | ASI | prod 0.672 / self 0.000 / **与另两颗 ASI 互相关仅 0.13** / IS 2.30 | ≈0.74 |
| 4 | **`88jaV5lv`** | ASI | prod 0.509（余量 0.19）/ self 0.000 / IS 2.35 | ≈0.75 |

**批次内相关性核查**：`d5bnE8jJ × P02wbJAM = 0.49`（note 实测）；`P02wbJAM × 88jaV5lv = 0.13`（note 实测）→ 均在闸内。

**备选队列（前序 403 时顺位顶上）**：
5. `mLmxKN12`（GLB，IS 2.99 → 期望 OS 0.96，但 prod 0.694 余量仅 0.006，很可能 403；09-20 曾尝试一次，`final_status=UNSUBMITTED`）
6. `LLNgdpw2`（ASI，IS 1.98 → 0.63；**不可与 `88jaV5lv` 同批**，二者互相关 0.65 贴线）
7. `3qX3Mp6O` / `3qX6wLkP`（IND，**先补 prod 重验**再入队）

## 3. 排除清单（附理由）

| alpha_id | 理由 |
|---|---|
| `3qX6wLJQ` | ❌ 实测 prod **0.9895** ≥ 0.7（库内 0.5171 为陈旧值）→ 已标 BLOCKED |
| `xA392Xpb` | self **0.6913** 距 0.7 仅 0.009，且 prod 未复验（网络抖动）→ 重验后再议 |
| `88jaV5lv` + `LLNgdpw2` 同批 | 互相关 0.65，贴 0.7 线 → 二选一 |
| 52 条 `SUBMITTED` / 13 条 `IS_ONLY` | 历史留痕或已提交，**不可当作待提交候选**（IS_ONLY 还标了 `retired:SUBMITTED`、`superseded-by:`）|

## 4. 执行方式

```bash
# 1) 提交判定（零成本，权威）
python tools/submit_verdict.py --alpha-id <ID>          # 或逐条批量
# 2) 用户确认后提交（当日配额 REGULAR 4 / SUPER 1）
python tools/submit_batch.py --spec <spec>
```
★ `POST /alphas/{id}/submit` 失败即同步 403 = **零成本**（不扣配额）且回带全部提交层 checks
→ 因此**队列可排 6 条打 4 个配额**，失败者顺位顶上，无副作用。
★ 每候选只发 1 次 submit；201 后只轮询。

## 5. 待办

- [ ] `3qX3Mp6O` / `xA392Xpb` / `3qX6wLkP` 补 prod 重验（网络恢复后）→ 重验通过方可入队
- [ ] 本轮未记录 `towers`（全部为空）→ 若要点塔优选，需补 `pyramid-alphas` 数据
- [ ] `mLmxKN12` 若 403 → 其 prod 余量仅 0.006，建议缓到下一 ET 日再试（或放弃）
