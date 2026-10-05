# 六法背景资料（datafield 评测）

> 主流程见 [`SKILL.md`](SKILL.md)。本文只留**出处、向量写法与验证例**；2026-09-29 由英文转载稿精简，删去「Advanced Applications」「Related Resources」等泛论。

## 出处与时效

- 来源：BRAIN 论坛帖 *[BRAIN TIPS] 6 ways to quickly evaluate a new dataset*（作者 KA64574，约两年前，265 位关注者）。
- 帖子是**公开平台的通用做法**，不是本仓库实测出来的；本仓库据此做了四处改动（依据都在 SKILL 里）：去掉 `? 1 : 0` 三元（本仓库文法不支持，MCP 静态门禁会整批拒绝；比较式本身就返回 0 / 1）；法 5 的 `ts_median` 换成 `ts_mean`（`ts_median` 是本账号的幽灵算子）；法 6 的 `scale_down` 换成 `zscore` 刻度（`scale_down` 不在本账号 103 个已验证算子里）；VECTOR 一律先 `vec_*`（闸 3）。
- 「六法」是**定性**工具：读 IS Summary 的 Long Count / Short Count，不看 Sharpe。

## 六法与向量写法

`vector_operator` 指 `get_operators` 目录里的 `vec_*`（`vec_avg` / `vec_sum` / `vec_max` / `vec_min` / `vec_count` / `vec_stddev` / `vec_range`）；MATRIX 字段不要包它。

| 法 | MATRIX 字段 | VECTOR 字段 | 读什么 |
|---|---|---|---|
| 1 覆盖 | `datafield` | `vec_avg(datafield)` | (Long + Short) / Universe Size ≈ 覆盖率 |
| 2 非零 | `datafield != 0` | `vec_avg(datafield) != 0` | Long Count ≈ 每日非零个数 |
| 3 频率 | `ts_std_dev(datafield, N) != 0` | `ts_std_dev(vec_avg(datafield), N) != 0` | 随 N = 5 / 22 / 66 的计数形状 |
| 4 范围 | `abs(datafield) > X` | `abs(vec_avg(datafield)) > X` | 逐档 X 的计数 |
| 5 中心 | `ts_mean(datafield, 252) > X` | `ts_mean(vec_avg(datafield), 252) > X` | 逐档 X 的计数 |
| 6 分布 | `zscore(datafield) > k` | `zscore(vec_avg(datafield)) > k` | k = -1 / 0 / 1 / 2 的占比 vs 正态 |

## 验证例（原帖）

仿真 `close <= 0`：Long / Short Count 都是 0，说明收盘价恒为正——**先用一个你确知答案的字段跑一遍**，确认设置（Neutralization `None`、Decay `0`、Test Period `P0Y0M0D`）和你对计数的读法没错，再去测未知字段。

## 什么时候用哪一法

| 法 | 最适合 | 何时用 |
|---|---|---|
| 1 覆盖 | 初判 | 任何新字段第一步 |
| 2 非零 | 数据质量 | 法 1 之后，区分缺失与真零 |
| 3 频率 | 新鲜度 | 要定窗口 / decay 之前 |
| 4 范围 | 量纲 | 要把它与别的字段组合之前 |
| 5 中心 | 典型值 | 要判断「正常水平」之前 |
| 6 分布 | 形态 | 要选 `winsorize` / `rank` / 门控之前 |

## 设置的理由（都是为了看到**原始**行为）

- **Neutralization `None`**：中性化会抹掉截面上的整体水平差异，掩盖覆盖 / 值域模式。
- **Decay `0`**：衰减会平滑掉更新频率与跳变。
- **universe**：选与目标战役相同的池——大池与小池的覆盖、分布可能不同。
