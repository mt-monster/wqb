# 第五轮战报（BE74/75/甄别批 + 设置档分族手册，2026-11-12）

## 一、BE74 设置档扫描两档（核心检验）

| 设置 | P05JM61x 原式 | news+I7 无回填版 | liq_i7 组合 | I7 单腿 | 流动性单腿 |
|---|---:|---:|---:|---:|---:|
| nan OFF / decay4 / SUBINDUSTRY | 0.18 | -0.11 | -0.27 | -0.01 | -0.91 |
| nan OFF / decay0 / FAST | 0.54（TO 0.68 爆） | -0.01 | -0.29 | -0.11 | -1.29 |
| nan ON / decay4 / SUBINDUSTRY（原档） | 1.46 | — | — | 1.00(单) | — |

**结论**：① nan OFF 对 nws20 高覆盖情绪腿是伤害（填 0 让无新闻股变现金腿是合理的）——nan OFF 的普适性被否定；
② RREPm361 的 2.02 是「纯 MATRIX 预估族 + FAST + decay0」的族专属适配，不能推广到事件型 VECTOR 族；
③ 流动性腿在 nan OFF 下 -0.91/-1.29 ⇒ 成交额字段必须 nan ON（cov=0 字段的缺失股被填 0 后恰好构成「零流动性」端点，是该因子的语义组成部分）。

## 二、★设置档分族终版手册（已落 SETTINGS_PLAYBOOK_FINAL_20261112.md）

nan ON/OFF 取决于「无数据股票在该信号里的角色」：高覆盖事件型 = ON（现金腿合理）；
预估类 MATRIX = OFF+FAST+decay0；中性化因族而异（信念比值=聚类簇 / analyst=FAST / 语调=SUBINDUSTRY）；
decay 因族而异（analyst=0 / starmine=8 / 事件双腿=4 / EAT=6）。

## 三、BE75 8/8 ERROR → 2 臂甄别在飞

- 正确符号版（成交额+内部人 8 变体）整批 ERROR（通用错误，非算子问题）；
- 按 BE13b 先例派 2 臂甄别批（top2 构造：insiders mean66 / s27 mean66），sim 4htkURdTM4qG8Z99xAhjLMC，在飞；
- 若甄别批也 ERROR ⇒ 平台瞬断或字段在 nan ON 下的除零/数值问题，需加 ε 重试。

## 四、pv20 流动性线现状

- BE70 组合 1.23（平台 code 核实：正号成交额腿 ts_zscore504 + 内部人 ts_mean66 不回填）；
- BE71 负号版 -0.93（符号确认：高流动性 ⇒ 正收益）；
- BE72/73（回填版内部人腿）全弱 ⇒ 回填毁信号第三次复现；
- 甄别批在飞：若通过，按 v2 L2 升级满波冲 1.58。