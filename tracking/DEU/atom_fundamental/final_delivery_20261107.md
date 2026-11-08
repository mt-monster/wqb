# DEU ATOM 战役 · 最终交付与存档索引（2026-11-07 收口版）

> 战役窗口 04:33–06:13 · 176 条回测（Fundamental 110 + Analyst 66）· 全程 MCP 工具 · create-multi-simulation 并发 ≤2 · prod 用 MCP check_correlation 实测
> 交付口径：REGULAR 硬闸 S≥1.58 ∧ 2Y≥1.58（用户 2026-11-06 确认线）；本段 **0 颗全闸通过**，三级近闸篮如下。

## 一、三级近闸篮（全部标注「未达 REGULAR 线」）

### Tier-1（S 差 0.01 + prod 浅钉，双重缺口）
| id | 家族 | S | F | 2Y | sub | self | prod | 覆盖 | ops |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| omEGe0Vn | analyst7 广度占比 k=0.375 sector @decay1 | 1.57 | 1.27✅ | 1.66✅ | 1.16✅ | 0.347✅ | **0.7552✗(n=3 浅钉)** | 10/10✅ | 4 |

### Tier-2（单闸结构性缺口）
| id | 家族 | S | 2Y | 缺口 |
|---|---|---:|---:|---|
| omEG5nk6 | fnd45 电话会正交三轴复合（sector） | 0.99 | 1.89✅ | S 差 37%（中性化四点曲线+全几何已穷尽） |
| KPJzjRx8 | fnd90 现金流覆盖 market rank | 1.02 | 0.42 | 2Y 差 1.16（2023 机制死亡内禀） |

### Tier-3（已判死封存）
fnd6 oiadpq 族（Wje5K71x 已提交占位，S 1.73）；afs 分歧度族（|S|≤0.51 方向反转）；fnd22 ESG（0.48）；analyst7 侧臂 8 族；shortinterest3 塔（MPY9VNY9 独占，11-04 收口）；cov0 五集。

## 二、类目终审（结构性上限）
- Fundamental：5 机制面全部到顶（fnd45 S 0.99 / fnd90 1.02·2Y0.42 / fnd6 槽位占 / fnd22 0.48 / 其余灭）——10 颗不可达。
- Analyst：A2 广度家族 S 平台硬顶 1.57（30+ 变体不敏感）——唯一近闸族。
- shortinterest3：11-04 已收口（MPY9VNY9 独占）。
- **本段唯一 >1.58 全闸件 = Wje5K71x（上一战役交付，已 ACTIVE OS）**。

## 三、存档索引
| 产物 | 路径 |
|---|---|
| Fundamental 终审 | tracking/DEU/atom_fundamental/campaign_verdict_20261107.md |
| Fundamental 全程台账（F1-F8） | tracking/DEU/atom_fundamental/wave_F3_dispatch_20261107.json |
| 12 集字段目录 | tracking/DEU/atom_fundamental/fields/*.json |
| Fundamental 画像汇总 | tracking/DEU/atom_fundamental/field_profiles_20261107.md |
| Wave 设计稿 | tracking/DEU/atom_fundamental/wave_F1_design_20261107.md、wave_F6_design_20261107.md |
| Analyst 终审（A2 家族） | tracking/DEU/atom_analyst/A2_family_verdict_20261107.md |
| Analyst 全程台账（AW1-AW8） | tracking/DEU/atom_analyst_wave1_dispatch_20261107.json |
| Analyst 字段目录 | tracking/DEU/atom_analyst/fields/*.json（11-06 建） |
| Wave1 设计稿 | tracking/DEU/atom_analyst/wave1_design_20261106.md |

## 四、方法论沉淀（长期记忆已写入）
参数平台硬顶签名（≥3 批 ±0.05 内 ⇒ 停参数扫）；阻尼参数 S/2Y frontier 测绘法；正交异质轴合成有效 vs 同质合成无效；winsorize 双侧被 rank 吸收；中性化四点曲线（STATISTICAL 不可跨信号迁移）；FAST 档扩书伪影；收割管线（batch_status → harvest_multisim_alphas，子代注册滞后 ~55 分钟）。

## 五、待决项
omEGe0Vn 双破路线（豁免 S 0.01 + prod 浅钉破墙）留作用户明示后执行——注意 A2 核为纯横截面比值（无 ts 窗口），窗口谷法适用性存疑。
