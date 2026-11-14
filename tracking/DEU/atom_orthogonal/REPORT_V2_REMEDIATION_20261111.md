# 补课波战报：探针协议 v2 启动 + tail 并列块机制（2026-11-11 上午）

## 一、本轮四波（v2 L1 正交网格 + 论坛文献臂）

| 波 | 内容 | 结果 |
|---|---|---|
| BE48 | institutions1 conviction 线 6 臂（ts_mean 版） | **全灭**（S -0.28~0.35，fail 4-5） |
| BE49 | insider_agg_matrix 论坛模板移植 10 臂 | 最佳 S 0.76（买卖占比，fail 2），<1.0 校准线 |
| BE51 | 新闻×I7 + tail 阶梯 5 臂 | 三次语法迭代后在飞 |
| BE50 | institutions1 正确配方（ts_sum+winsorize2+tail）6 臂 | 三次语法迭代后在飞 |

## 二、★关键机制发现：事件型低覆盖数据集的「并列块污染」

来源：论坛帖 43178926004887（DEU INSTITUTIONS 破咒帖，88 次回测，已提交 xAjEkeOq S1.68 全闸）。
完整拆解见 TAIL_TIEBLOCK_MECHANISM_20261111.md。要点：

1. nanHandling=ON 把无申报股票填 0 → ts_sum 后仍 0 → group_rank 把横截面 72-80% 压成同一值
   （rank 中段 ≈0.4）⇒ 四分之三横截面无信号、subU 被稀释最狠；
2. 正确配方：vec_sum → divide(+ε) → winsorize(std=2) → **ts_sum(66)**（不是 ts_mean！）→ group_rank → tail；
3. tail 阶梯 0.20-0.30 是宽平台（S 1.60-1.67），winsorize 与 tail 必须成对；
4. 作者猜想：**所有 coverage<0.5 事件型数据集都有这块假中段** ⇒ 需回溯重测所有事件型判决。

## 三、BE48 为什么全灭（归因）

- 我用了 **ts_mean**（帖子实证：事件频率被除掉，1.44→0.73）；
- winsorize 用了 std=4（甜点是 std=2，std=4 → S 0.32）；
- 缺 tail；分组轴用 industry 但缺 SLOW_AND_FAST 中性化档。
⇒ **BE48 是配方错误，不是信号死亡**——正是 v2「文献前置」制度要防的错。

## 四、平台语法三次迭代（tail）

1. `tail(x, 0.25)` → toolkit 静态闸整批拒（第2参必须命名 lower=）；
2. `tail(x, lower=0.25)` → 平台报 Required attribute "upper"（5/5 ERROR）；
3. `tail(x, lower=0.25, upper=1.0)` → 平台报 Required attribute "newval"（6/6 ERROR）；
4. **正确**：`tail(x, lower=q, upper=1.0, newval=0)`（在飞：BE51=3kSYKx65b565crCANQzTaBs、BE50=1nTExDeXA4XD8YU1yi4cWcL）。

附带：镜像负腿写 `subtract(0, group_rank(...))` 规避「加权混腿」毒模式。

## 五、待授权篮子的污染盘点（用平台原始表达式核实，非记忆）

- qM7KxkQV / d5a2vxzY / Jj8VQwoe / 9qlz29Oe：**4 颗的事件型腿全部可能被并列块污染**；
- RREPm361（纯 analyst MATRIX）不受影响；78Yk8VR1 已 ACTIVE，tail 版会撞 self，不做；
- BE52 预设计（8 臂替换升级路径）已落档：waveBE52_design_tail_enhanced_basket_20261111.md。

## 六、下一步

1. 收割 BE51/BE50 → 若 tail 有效：回溯重测 insiders1 / insider_agg / news20 / shortinterest3 事件型判决；
2. 派 BE52（tail 增强版待授权篮子，替换升级）；
3. 按 v2 协议继续补 option1 / pattern_scores / risk72 / continuation_score / intraday_pv_feats 的 L1 网格；
4. 积压消费：pv30 165 / news81 188 / other128 48 / other546 48 条 0 回测表达式。