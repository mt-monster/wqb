# GBR D1 fundamental45 挖掘经验（电话会议语言同源姊妹集 · 探针判死）

范围：2026-10-30。GBR/TOP700/D1 的 `fundamental45`。本文件只记录 **2 条结构互异探针**
的全灭结果；这是**探针级**判死（不是 6 模板级），证据强度低于 `analyst83` / `other384`，
但方向一致、且作为同源集交叉印证有独立价值。

数据集画像（DB `datasets` 表实读，id=180）：category `FUNDAMENTAL`、`field_count 12`、
`coverage 0.2719`、`alpha_count 0`（平台侧尚无已提交 alpha）、`value_score 5`、
`pyramid_multiplier 2`、`delay 1`、`tier EXCLUDED`。

★ **`pyramid_multiplier 2` 是本区最高档之一，`alpha_count 0` 说明无人开采** —— 这两个
信号都是「诱因」，本文件的作用正是记录它们**没有**兑现成信号。

## 判死结论（registry：`GBR-FUNDAMENTAL45-CALLTRANSCRIPT-DEAD`，2026-10-30）

| 骨架 | 机制 | Sharpe |
|---|---|---:|
| 双模型分歧（两个分类器 tone 之差） | 模型间不确定度 | **−0.57** |
| 双重差分（`ts_av_diff` 套 `ts_av_diff`） | 语调加速度 | **−0.17** |

两条都是**负信号**：不是「弱」，是方向相反。回测设置 `STATISTICAL` + `decay 4` + `trunc 0.08`。

## 判死口径与限制（务必照抄）

- 只有 **2 条**探针，**不足以**支撑「fundamental45 全数据集无效」。`field_count 12`
  本身字段就少，2 条已覆盖「模型间分歧」与「二阶变化」两个主要方向，但没有覆盖
  「水平」「覆盖度」「跨期稳定性」。
- 真正让判死站得住的是**同源交叉**：`analyst83`（6 模板）+ `fundamental45`（2 探针）
  + `other384`（6 模板 + 1 变体）= **16 条 0 达标**，且都是「电话会议语言数据」这一族。
  ⇒ 判死的是**机制族**，不是单个数据集。
- `tier EXCLUDED` 是平台/本地 S0 早先给的标签——它与本次实测**同向**，但不要用
  `tier` 当判死依据（那是先验，不是证据）。

## 后续边界

- **不再单独立项挖 `fundamental45`**。若同族（transcript tone）出现新证据，应把它
  作为**同源验证集**而不是主战场（只有 12 个字段，独立自由度太低）。
- 若要重启，最低要求：①先拿到与 `analyst83`/`other384` 不同的经济假设
  ②模板池 ≥10 个结构互异模板（当前只跑了 2 个）③必须做 `level vs change` 对照。
- 本集回测**未入 `backtest_results` 表**（`region='GBR' AND dataset='fundamental45'`
  实读 0 行），证据仅存于本文件与 registry payload。

## 证据落点

- 判死条目：`registry_empirical` → `GBR-FUNDAMENTAL45-CALLTRANSCRIPT-DEAD`
- 同源姊妹集：`gbr_analyst83_campain.md`、`gbr_other384_campain.md`
- 论坛模板：`43907846056599`（earnings-call tone 权威实证，3 赞）
