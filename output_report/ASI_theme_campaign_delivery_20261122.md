# ASI/D1 Power Pool Dec'26 战役交付报告（2026-11-22）

## 目标与实际
- 目标：10 颗全闸 regular alpha（ATOM 优先），锁 ASI 不切区
- **实际交付：2 颗 RA 全闸件（failed_ra_count=0），但 prod 终验 pwaplg5g = 0.8018 FAIL ⇒ 提交级 0 颗**
- 诚实说明：JPN 墙 + prod 钉子墙双夹击使 fundamental ebit 机制提交级不可达；10 颗目标差距更大

## ★ 交付件（RA 全闸，待 prod/self 终验）

### 1. pwaplg5g（首选，FUNDAMENTAL 塔 0/3 未点亮）
```
add(multiply(group_rank(ts_delta(ts_zscore(divide(ebit, assets), 252), 252), country), 1.5),
    group_rank(ts_delta(ts_zscore(group_zscore(divide(ebit, assets), exchange), 252), 252), country))
```
设置：ASI/MINVOL1M/D1/SLOW/decay4/trunc0.08/maxTrade ON
指标：S2.28 / F1.28 / 2Y1.64 / sub1.19 / TO5.85% / margin13.5bp / **failed_ra_count=0**（JPN✓ Robust✓）
prod/self：**prod=0.8018 FAIL**（2026-11-22 终验，钉子型 bucket[0.8,0.9) 仅 1 条）；self 未测（prod fail 早退）。⇒ 提交级不可用

### 2. blaKRQxN（备选，与 pwaplg5g 互相关 0.7973>0.7，不可同篮）
```
add(multiply(group_rank(ts_delta(ts_zscore(divide(ebit, sales), 252), 252), country), 1.5),
    group_rank(ts_delta(ts_zscore(group_zscore(divide(ebit, sales), exchange), 252), 252), country))
```
指标：S2.10 / F1.15 / 2Y1.63 / sub1.28 / margin12.2bp / **failed_ra_count=0**
prod 未终验；属利润率轨迹机制但与 pwaplg5g 互相关 0.7973，且同一 prod 钉子族，预期同样 FAIL

## 核心方法论（可复用）
1. **内层 group_zscore(x, exchange) 是"一击两得"变换**：抬 JPN（0.94→0.98）+ 逃逸 prod 钉子（0.8336→0.6447），代价 S/2Y 下降
2. **双尺度 add 打破 JPN vs S/2Y 取舍**：1.5×高S腿(country) + 1×exchange-z载体腿，加权重置把 2Y 1.55→1.64 过闸
3. **分子经济含义决定 JPN 上限**：ebit/assets(ROA效率)能过 1.0；ebit/equity(ROE)0.92 天花板；operating_income/assets 0.88；analyst rating ~0.52
4. **Robust limit = 0.9×主S**：S 越高门槛越高（论坛帖③"主S勿超2.5"）
5. **★ prod 双墙实证**：高S腿带 prod 钉子(0.83)、exchange-z 腿 prod 干净(0.64)但强度不足(1.58/0.9)；双尺度 add 恒 0.78–0.80 FAIL；三破法（子集门控压垮2Y / 残差正交压垮强度 / 换形态无效）全灭

## 数据集判定
- price_signal_dl：60+ 臂，volume-shock 机制 JPN 全臂 0.01-0.22 → PROVISIONAL 机制层死（非数据集死键）
- fundamental23：20+ 臂，ebit 系出 2 颗全闸但互相关≥0.75 只能交 1 颗；现金流/毛利率/杠杆机制全灭
- analyst69：8 臂，rating 族 JPN 天花板 0.52 → PROVISIONAL；992 字段未全量画像（未进入选字段环节）

## 平台工程坑（已归档 memory）
- ASI multisim 通道全 FAIL（6/6 空 FAIL），需单发重派；孪生字段去重伪影（归因只认实读 code）；multisim 卡 0.35 排队用轮询不重派；winsorize 套 group_rank 是恒等空操作；grossprofit 字段名错误致整批 CANCELLED（正确 fnd23_prgs）

## 未完成 / 下次会话
1. pwaplg5g / blaKRQxN 的 prod/self 终验（等 corr 槽释放）
2. 第 2 席低相关件：转 shortinterest（融券机制与 fundamental 正交，论坛帖①推荐）
3. analyst69 若正式开需补 992 字段全量画像
4. 平台侧：本会话 6 条其实时进度工具因后端刷新短暂掉线，不影响数据结果

## 归档路径
- tracking/ASI/reference/datasets/price_signal_dl.md（含 §7-8 梯度+JPN判定）
- tracking/ASI/reference/datasets/fundamental23.md（含梯度表+prod实测+工程坑+互相关终判）
- tracking/ASI/reference/datasets/analyst69.md（探针结论）
- memory: asi-d1-theme-campaign-20261122.md


---

## 附：prod 钉子归属终判（2026-11-22 补充）

零配额 get_user_alphas 实读：本账号 ASI 已提交 12 颗（2 SUPER + 10 REGULAR），**无一颗 fundamental 类**。

| 塔 | 已提交件 | prod 范围 |
|---|---|---|
| SUPER | 2 颗 | 0.50–0.51 |
| OTHER 1.4x | 4 颗（P0obGoQJ/E5ReEnpP/j28nKkQo/qMNMbeGj） | 0.59–0.69 |
| PV+SENTIMENT | 4 颗（E5R56EbR/1YZYj5QQ/P02wbJAM/88jaV5lv/LLNgdpw2） | 0.51–0.69 |
| RISK+MODEL | 1 颗（rKjY5vGj） | 0.63 |

⇒ **pwaplg5g 的 prod 钉子 0.80 来自他人已提交件，不可控**。三破法（子集门控压垮 2Y / 残差正交压垮强度 / 换形态无效）全灭 ⇒ fundamental23 ebit 机制在 ASI **提交级不可达**，本会话 final。

**正面可复用情报**：ASI 已验证能过 prod 的两族信息源 = `dl_riskfree probability_label 分位族`（OTHER 塔 4 颗）与 `other36 空头持仓变化`。下一次挖未满塔的起点应从这里出发（机制与经济含义完全不同于 ebit，天然低相关）。
