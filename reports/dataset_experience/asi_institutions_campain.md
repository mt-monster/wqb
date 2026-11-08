# ASI Institutions 数据集全字段画像（2026-11-08）

区域：ASI / MINVOL1M / D1（campaign 配置：SLOW / country 轴 / trunc 0.08）
范围：Institutions category 全部 2 个数据集、41 个字段（禁止抽样，全列）
归档路径：`reports/dataset_experience/asi_institutions_campain.md`（项目规范：`<region小写>_<dataset>_campain.md`）

## 一、institutions6（11 字段，全 MATRIX，cov 0.995–1.000，aC 137–330）

机构持仓 13F 类季度数据（报告期聚合到日频前向填充）。

| 字段 | cov | aC | 类型 | 更新频率 | 分布特征 | 可用性 | 潜在 alpha 适用性 |
|---|---:|---:|---|---|---|---|---|
| aggregate_equity_value_all_owners | 1.000 | 330 | M | 季度 | 右偏（市值尺度） | 高 | 分母/规模轴；不宜直接做信号 |
| aggregate_equity_value_institutions | 0.995 | 185 | M | 季度 | 右偏 | 高 | 机构持仓占比的分子 |
| aggregate_share_count_all_owners | 1.000 | 183 | M | 季度 | 右偏 | 高 | 同上（股数口径） |
| aggregate_share_count_institutions | 0.995 | 220 | M | 季度 | 右偏 | 高 | 聪明钱流向（股数口径）★ |
| count_institutional_buyers_security | 1.000 | 215 | M | 季度 | 离散计数 | 高 | 买方家数——共识动量分子 ★ |
| count_institutional_holders_security | 1.000 | 172 | M | 季度 | 离散计数 | 高 | 分母（活跃度）；直接用 S 弱 |
| count_institutional_sellers_security | 1.000 | 267 | M | 季度 | 离散计数 | 高 | 卖方家数——共识动量分母 ★ |
| market_value_institutional_shares_acquired | 1.000 | 137 | M | 季度 | 右偏 | 高 | 买入金额（聪明钱流向分子）★ |
| market_value_institutional_shares_disposed | 1.000 | 194 | M | 季度 | 右偏 | 高 | 卖出金额 ★ |
| quantity_institutional_shares_acquired | 1.000 | 147 | M | 季度 | 右偏 | 高 | 买入股数 |
| quantity_institutional_shares_disposed | 1.000 | 219 | M | 季度 | 右偏 | 高 | 卖出股数 |

**机制映射**（经济含义）：
- M1 净家数比 = (buyers − sellers)/holders：机构共识方向——**拥挤反转**（家数口径，历史 S 1.17 天花板，旧配方）
- M2 股数/金额净流 = 机构资金流向——**聪明钱动量**（与 M1 符号相反，不可混用）
- M3 持仓量 ts_delta：机构增减仓动量

## 二、fund_holdings_panel（30 字段 = 15 对 base/active，cov 0.787–0.911）

fund 账户级持仓/交易面板。**13 个 VECTOR 字段必须先 vec_avg/vec_sum 聚合**（平台规则）。
"active" 后缀 = 只计活跃账户（覆盖率低 0.08），base = 全账户。

| 字段族 | 字段（base/active） | 类型 | 机制含义 |
|---|---|---|---|
| 持仓集中度 | herfindahl_index_holdings (0.911/85) + _active | MATRIX | HHI 拥挤度——高集中 → 反转 ★ |
| 持仓分布分 | holding_value_distribution_score (0.911/73) + _active | MATRIX | 自定义拥挤度——同 HHI 方向 |
| 信念持仓 | top_weighted_account_number (0.911/18) + _active | MATRIX | conviction 账户数（top 30% 权重）★ |
| 账户数 | holder_account_total (0.911/37) + _active | MATRIX | 持有账户数——广度 |
| 平均权重 | mean_security_weight (0.911/24) + _active | MATRIX | 账户组合内平均权重 |
| 持仓金额 | security_holding_usd_value (0.911/33) + _active | MATRIX | USD 持仓规模 |
| 边界交易 | boundary_transaction_total (0.887/31) + _active | VECTOR | 新建仓/清仓事件 ★ |
| 边界金额 | boundary_transaction_usd_value (0.887/15) + _active | VECTOR | 边界交易金额 |
| 稳定边界 | stable_boundary_trade_count_21d (0.887/10) + _active | VECTOR | 冷启动账户的边界交易 ★ |
| 大单计数 | large_trade_count_50bps (0.887/3) + _active | VECTOR | >0.5% AUM 的大单数 |
| 交易金额 | security_transaction_usd_value (0.887/18) + _active | VECTOR | 交易金额 |
| 交易集中度 | herfindahl_index_transactions (0.887/8) + _active | VECTOR | 交易方集中度 |
| 交易分布分 | transaction_value_distribution_score (0.887/9) + _active | VECTOR | 交易分布拥挤度 |
| 交易账户 | transaction_account_total (0.887/9) + _active | VECTOR | 交易账户数 |
| 信念交易 | top_weighted_transaction_number (0.887/3) + _active | VECTOR | conviction 交易数 |

**机制映射**：
- M4 持仓集中度反转：herfindahl/holding_value_distribution 高 → 基金拥挤 → 做空
- M5 信念跟随：top_weighted_account_number（conviction 账户数增加）→ 做多
- M6 边界事件：boundary/stable_boundary（新仓位建立）→ 动量方向

## 三、历史判据（本战役早轮，旧配方）

- institutions6 家数口径取反：S 1.17 天花板（10 模板）——**当时未用 country 轴/短窗/decay 突破配方，需重测**
- fund_holdings_panel：10 模板最好 S 1.11——同上需重测

## 四、探针计划（新配方：ts_rank 短窗 + country + SLOW + decay 扫描）

- IQ 批：M1 净家数比 / M2 持仓量动量 / 金额差比（decay22）
- 后续：M4 HHI 反转 / M5 conviction / M6 边界事件（vec_avg 先聚合 VECTOR）


## 浜斻€佹壂鎻忕粨鏋滐紙2026-11-08锛? 鎵?24 鏉¤〃杈惧紡锛孧INVOL1M/TOP500 脳 SLOW/country锛?
### 5.1 institutions6锛?2 鏉¤〃杈惧紡 脳 5 鍑犱綍锛?
| 鎵?| 琛ㄨ揪寮忚鐐?| 璁剧疆 | S | 鍒?|
|---|---|---|---:|---|
| IQ1 | 鍑€瀹舵暟姣?ts_rank8 | M1/SLOW/d22 | 0.50 | 寮?|
| IQ2 | 鎸佷粨閲?ts_delta22 | M1/d22 | 鈭?.63锛堟 +0.63锛墊 寮?|
| IQ3 | 閲戦宸?鎸佷粨姣?ts_rank8 | M1/d22 | 0.56 | 寮?|
| IR1 | 鍑€瀹舵暟姣?姘村钩 鍙栧弽 | M1/d22 | 0.39 | 寮憋紙鍘嗗彶 1.17 鏈鐜帮級|
| IR2 | 鍑€瀹舵暟姣?ts_rank63 | M1/d22 | 0.62 | **鏈泦鏈€濂?* |
| IR3 | 鎸佷粨閲?ts_delta63 | M1/d22 | 鈭?.61锛堟 +0.61锛墊 寮?|
| IU1 | 鎹㈡墜姣?acquired/(a+d) | M1/d44 | 0.04 | 姝?|
| IU2 | holder 鏁?ts_delta63 鍙栧弽 | M1/d44 | 0.32 | 寮?|
| IU3 | 鏈烘瀯鎸佷粨鍗犳瘮鍙樺寲 | M1/d44 | 0.22 | 姝?|
| IV1 | 绾拱瀹舵暟 鍙栧弽 | M1/d22 | 鈭?.23锛堟 +0.23锛墊 姝?|
| IV2 | 绾崠瀹舵暟 鍙栧弽 | M1/d22 | 鈭?.50锛堟 +0.50锛墊 姝?|
| IV3 | 绾寔鏈夋暟 鍙栧弽 | M1/d22 | 鈭?.25锛堟 +0.25锛墊 姝?|
| IX2a | 鍑€瀹舵暟姣?鍙栧弽 @TOP500 | TOP500/d22 | 0.58 | 寮憋紙浣?robust 鍏ㄨ繃锛墊
| IX2b | 鑲℃暟鍔ㄩ噺 @TOP500 | TOP500/d22 | 鈭?.33 | 姝?|

### 5.2 fund_holdings_panel锛?2 鏉¤〃杈惧紡 脳 6 鏈哄埗鏃忥級

| 鎵?| 鏈哄埗 | S | 鍒?|
|---|---|---:|---|
| IS1 | HHI 鎷ユ尋鍙嶈浆 | 鈭?.80锛堟 +0.80锛墊 寮?|
| IS2 | conviction 璐︽埛鏁?| 0.17 | 姝?|
| IS3 | boundary 浜嬩欢 | 0.36 | 姝?|
| IT1 | 鎸佷粨鍒嗗竷鍒?鍙栧弽 | 鈭?.97锛?*姝?+0.97 鍏ㄩ泦鏈€濂?*锛墊 寮?|
| IT2 | 澶у崟璁℃暟 vec_avg | 0.19 | 姝?|
| IT3 | 绋冲畾杈圭晫 vec_avg | 0.24 | 姝?|
| IW1 | mean_security_weight | 0.82 | 寮?|
| IW2 | holder_account_total 鍙栧弽 | 0.27 | 姝?|
| IW3 | 鎸佷粨閲戦 ts_rank63 | 鈭?.48 | 姝?|
| IX2c | 鎷ユ尋搴?@TOP500 | 0.50 | 寮?|

### 5.3 鍗佸勾瑕嗙洊锛堥€愬勾 longCount / pnl锛?
- institutions6锛坓Je0NK20锛夛細2014鈥?023 lc 1637鈥?372锛宲nl 7 姝?3 璐?鈫?**瑕嗙洊 鉁?*
- fund_holdings_panel锛坖2YJ2rak锛夛細**2014 lc=0/pnl=0锛堣捣濮嬪勾绌虹獥锛?*锛?015鈥?023 瀹屾暣 鈫?鎸夌敤鎴峰彛寰勶紙杩炵画澶氬勾绌虹獥鎵嶅垽姝伙級鍕夊己鍙帴鍙楋紝浣嗛骞寸己鏁版嵁

### 5.4 鍊欓€夋竻鍗曚笌閫夊畾鐞嗙敱锛堢洰鏍囩涓€闃舵浜や粯鐗╋級

**缁撹锛欼nstitutions category 鍒ゆ锛堟棤璁″彲鏂斤級锛岀悊鐢卞涓嬶細**

1. **寮哄害澶╄姳鏉?~0.97**锛?4 鏉¤〃杈惧紡銆? 澶ф満鍒舵棌銆? 涓?universe銆? 绉嶅嚑浣曘€乨ecay 22/44 鍏ㄦ壂锛夛紝
   璺?1.58 绾跨己 39%鈥斺€斾笉鏄€岃繎闂搞€嶆槸銆岃繙闂搞€嶏紝鏃犲畾鍚戞寲鎺樹环鍊笺€?2. **JPN 闂哥粨鏋勬€ф寕**锛?9/24 鏉℃寕 LOW_ASI_JPN_SHARPE锛堟満鏋勬暟鎹湪 JPN 瀛愰泦鏃犱俊鍙凤級銆?3. **鏃х粨璁?S 1.17/1.11 鏈兘澶嶇幇**锛圱OP500 + 姘村钩/瀛ｅ害鍑犱綍鍧囪瘯杩囷級鈥斺€旀棫鍊煎彲鑳芥槸 SUBINDUSTRY/鍏跺畠璁剧疆鐨勪骇鐗╋紝涓斿嵆渚垮鐜颁篃杩囦笉浜?JPN銆?4. fund_holdings_panel 2014 骞寸┖绐?+ 鍏ㄥ瓧娈?aC 鈮?85锛堜綆浣跨敤鐜囦晶闈㈠嵃璇佸急锛夈€?5. **TOP500 鐨勬闈㈠彂鐜?*锛歳obust 鍙岄椄鍦?TOP500 鍏ㄨ繃锛堟祦鍔ㄦ€у畤瀹欏ぉ鐒堕珮淇濈暀鐜囷級鈥斺€旇嫢鏈潵鍦?TOP500 涓婃壘鍒?S>1.5 鐨勪俊鍙凤紝robust 涓嶆槸闂銆傛鎯呮姤宸茶鍏ョ粡楠屻€?
**閫夊畾鐞嗙敱锛堝幓鐣欙級**锛氭棤閫夊畾鏁版嵁闆嗏€斺€斾袱闆嗗叏寮便€傛寜鐩爣銆屼粎鍦ㄧ‘瀹炴棤璁″彲鏂芥椂鏇存崲骞惰鏄庡師鍥犮€嶏紝
Institutions 鐨勬棤璁″彲鏂借瘉鎹摼濡備笂锛?4 鏉?/ 8 鎵?/ 鍏ㄦ満鍒舵棌锛夛紝鐜板湪杞悜鎴樺焦鍐呭凡鐭ョ殑鍞竴鍙彁浜ゆ簮
dl_riskfree_returns锛圤THER 濉旓級鐨勮繎闂稿€欓€夌户缁畾鍚戞寲鎺橈紙KPJ2leYp robust 宸?0.0001銆?LLM2aWme JPN 宸?0.01銆乴abel2_3q/label3 robust 澧欙級锛岃繖浜涙槸鐪熸鐨勩€岃繎闂稿€欓€夈€嶃€?


## 鍏€乨l_riskfree 杩戦椄琛ユ祴涓?TOP500 瀹囧畽瀹為獙锛?026-11-08 鏅氾級

### 6.1 quantile 杩戦椄 ts_av_diff / ts_zscore锛圛Y 鎵?@ d10锛?
| alpha | 琛ㄨ揪寮忚鐐?| S | F | 2Y | fail |
|---|---|---:|---:|---:|---|
| VkxLVzW5 | ts_av_diff(W4) | 4.14 | 1.70 | 2.38 | robust 3.66<3.73 / 0.0666<0.0679 |
| wpQAqG06 | ts_av_diff(W5) | 4.16 | 1.82 | 2.43 | robust 3.66<3.74 / 0.0666<0.0683 |
| akK86z5W | ts_zscore(W5) | 4.18 | 1.87 | 2.57 | robust 3.45<3.76 / 0.0657<0.0714 |

robust 甯告暟 0.88 閲嶇幇鈥斺€攓uantile 鏃?30 閰嶇疆锛坱s_rank 脳 decay 脳 signed_power 脳 av_diff 脳 zscore 脳 group_backfill锛夊叏閮ㄨ瘉浼€?
### 6.2 鈽?TOP500 瀹囧畽瀹為獙锛圛Z 鎵?@ d44锛?
| alpha | 瀛楁 | S | 鍒?|
|---|---|---:|---|
| WjORq2pj | label1 W8 | 鈭?.42 | **淇″彿缈昏浆姝讳骸** |
| wpQAmkR1 | label1 W10 | 鈭?.31 | 姝?|
| mLoN3W85 | quantile W4 | 1.51 | 宸?0.07 鍒扮嚎 |

**涓や釜鍏抽敭淇涓庝竴鏉℃儏鎶?*锛?1. **淇鏃х粨璁?*锛歞l_riskfree 瀛楁鍦?TOP500 涓婂瓨鍦紙鏃ф垬褰瑰彧娴嬩簡 TOP3000/1200/600锛夈€?2. **dl_riskfree 淇″彿渚濊禆灏忕エ鍩?*锛歍OP500锛堝ぇ绁級涓?label1 淇″彿绗﹀彿缈昏浆涓旀浜♀€斺€擟NN 妯″瀷鐨勯娴嬪彧鍦?MINVOL1M 鍩熸湁鏁堛€?3. **TOP500 涓?robust 鍙岄椄澶╃劧鍏ㄨ繃**锛坕nstitutions 鎵弿鍚屾壒纭锛夆€斺€旇嫢鏈潵鎵惧埌 TOP500 涓婄殑寮轰俊鍙凤紝robust 涓嶆槸闂搞€?
### 6.3 ASI 鎴樺焦鎬荤煩闃碉紙鏂扮洰鏍囧惎鍔ㄥ悗 +8 鎵?35 鏉★級

Institutions 鍒ゆ锛堣绗簲鑺傦級鈫?dl_riskfree 杩戦椄鍏ㄧ畻瀛愯ˉ娴嬭瘉浼?鈫?TOP500 淇″彿鍩熶簰鏂ャ€?**ASI 鍞竴鍙彁浜や俊鍙蜂粛鏄?1YN0XrYX锛坙abel1_4q_60day W8 @ decay44锛孧INVOL1M锛?*銆?
