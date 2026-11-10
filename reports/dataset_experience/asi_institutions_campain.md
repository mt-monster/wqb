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


## 涓冦€乵odel 濉旀湭娴嬫暟鎹泦鎵弿锛?026-11-08 鏅氾紝11 鎵?33 鏉★級

### 7.1 鎵弿缁撴灉鎬昏〃

| 鏁版嵁闆?| 瀛楁 | 鏈€濂?S | 姝诲洜 |
|---|---|---:|---|
| predictive_starmine | 645锛堜慨璁㈣鏁?棰勪及鍙樺寲锛墊 0.92 | 寮憋紙GBR 淇骞垮害閰嶆柟涓嶇Щ妞嶁€斺€擜SI analyst 瑕嗙洊钖勶級|
| global_seasonal_model | 681锛堝洓婧愬鑺傛ā鍨嬶級| **2.70**锛坧v_calendar prob4 @CROWDING锛墊 **JPN 瀛楁绾у**锛氬洓婧愬叏鎸?鈭?.27~0.09锛堥渶鈮?.0锛夛紝SLOW/CROWDING/STATISTICAL脳country/subindustry 鍏ㄦ壂鏃犺В |
| price_signal_dl | 28锛圖L 瓒嬪娍/閲忚兘鎸囨爣锛墊 0.89 | 寮?|
| model243 | 4锛堢患鍚堟ā鍨嬫帓鍚嶏級| 鈥?| **EVENT 绫诲瀷姝?*锛氭墍鏈夌畻瀛愶紙group_rank/ts_backfill/ts_sum/days_from_last_change/plain锛夊潎鎶?"does not support event inputs" |
| model68 | 4锛圖REAM 鍔ㄩ噺锛墊 鈥?| 鍚屼笂 EVENT 姝?|
| ai_equity_alpha | 582锛圓I 鍥犲瓙搴擄級| 鈥?| 鍚屼笂 EVENT 姝伙紙棰勬 valid:true 鏄亣闃虫€р€斺€旈妫€涓嶆煡杩愯鏃?event 鍏煎鎬э級|

### 7.2 鈽?EVENT 绫诲瀷闄烽槺锛堟柊宸ュ叿缁忛獙锛?
**鐜拌薄**锛歡et_datafields 杩斿洖 type=MATRIX + preflight valid:true锛屼絾杩愯鏃舵墍鏈夌畻瀛愭姤
"Operator X does not support event inputs"銆傝繛 plain 瀛楁琛ㄨ揪寮忎篃 FAIL銆?**褰卞搷鏁版嵁闆?*锛圓SI model 濉旓級锛歛i_equity_alpha銆乵odel243銆乵odel68锛堝彲鑳借繕鏈夋洿澶氾級銆?**鍒ゅ埆娉?*锛氶妫€閫氳繃鈮犲彲鐢紱蹇呴』瀹炶窇涓€鏉℃墠鐭ラ亾銆備笌 risk68 鐨勩€岀洰褰曞崰浣嶃€嶅悓绫讳絾鏇撮殣钄?锛堝瓧娈靛厓鏁版嵁鐪熷疄銆佹湁 coverage锛屽彧鏄繍琛屾椂绫诲瀷鏄?EVENT锛夈€?**鐪佹壒鎶€宸?*锛氭柊鏁版嵁闆嗗厛娲?1 鏉?group_rank 鎺㈤拡楠岃瘉绫诲瀷锛屽啀閾哄瓧娈垫棌銆?
### 7.3 global_seasonal_model 鏈€寮洪厤缃暀妗?
`group_rank(pv_daily_calendar_60d_5bucket_prob_label_4, country)` @ CROWDING/decay22锛?S 2.70 / F 2.14 / 2Y 3.07 / sub 1.91鈥斺€斿彧鎸?JPN(0.09) + robust(1.74<2.43 / 0.06<0.08)銆?鑻ユ湭鏉?JPN 闂歌В闄わ紙濡傚钩鍙拌皟鏁达級鎴栬瀛楁鏃忓湪鍏跺畠鍖哄彲鐢紝姝ら厤缃槸鐜版垚璧风偣銆?


## 鍏€佲槄 绗?2/3 棰椾弗鏍煎叏缁垮€欓€夎癁鐢燂細label1_5quantile 鏃忥紙2026-11-08 鏅氾級

### 8.1 鍙戠幇璺緞

probability 鏃忔敹灏炬壒锛圝N锛夎ˉ娴嬩簡 60day 姒傜巼鍦虹殑 5 鍒嗕綅鐗堟湰鈥斺€?`probability_label1_5quantile_60day_ohlcv`锛圥 钀藉湪浜斿垎浣嶆渶浣庢《锛宎C 308锛夛細

| 閰嶇疆 | alpha | S | F | 2Y | prod | 鍒?|
|---|---|---:|---:|---:|---:|---|
| W8 @ decay44 | Xg9xnwMa | 3.16 | 1.76 | 2.44 | **0.7039 鉁?* | 0 fail 浣?prod 瓒呯嚎 0.004 |
| **W7 @ decay33** | **78LrnNK5** | **3.13** | **1.60** | **2.46** | **0.6574 鉁?* | **鈽?鍏ㄧ豢锛堜綑閲?0.043锛?* |
| **W9 @ decay33** | **vR1bvrez** | **3.07** | **1.64** | **2.40** | **0.6852 鉁?* | **鈽?鍏ㄧ豢锛堜綑閲?0.015锛?* |

label1_2q 姝ｅ悜锛坓Je5MqLm锛夛細S 3.16 / 2Y 1.51 / JPN 0.95鈥斺€擩PN+robust 鍙屽樊锛屾湭鐮淬€?
### 8.2 鍏ㄧ豢璧勪骇娓呭崟锛堢疮璁?3 棰楋級

| # | alpha | 琛ㄨ揪寮忔牳蹇?| S | F | 2Y | prod | self | 鍗佸勾 |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | 1YN0XrYX | label1_4q W8 @ d44 | 2.18 | 1.01 | 2.20 | 0.6934 | 鈭?.004 | 鍏ㄦ |
| 2 | **78LrnNK5** | **label1_5q W7 @ d33** | **3.13** | **1.60** | **2.46** | **0.6574** | 0.030 | 鍏ㄦ锛?.72-4.46锛墊
| 3 | vR1bvrez | label1_5q W9 @ d33 | 3.07 | 1.64 | 2.40 | 0.6852 | 寰呮煡 | 鈥?|

**鍏抽敭缁忛獙**锛歭abel1_4q 鐨?W8 鐢滅偣涓嶈兘鐩存帴鐓ф惉鍒?label1_5q锛圵8@d44 prod 0.7039 缈荤嚎锛夛紱
鎹㈠瓧娈垫棌鍚?**W-decay 骞抽潰蹇呴』閲嶆壂**鈥斺€攍abel1_5q 鐨?prod 璋峰湪 W7@decay33銆?10 棰楃洰鏍囪繘搴︼細**3/10**锛堝叏閮ㄦ潵鑷?dl_riskfree ATOM锛孫THER 濉旓級銆?


### 8.3锛堢画锛塴abel1_5q W 骞抽潰鍏ㄦ壂鎻?@ decay33锛圝P 鎵癸級

| W | alpha | S | F | 2Y | prod | 鍒?|
|---|---|---:|---:|---:|---:|---|
| 5 | **P0obGoQJ** | 3.06 | 1.39 | 2.37 | **0.5973** | **鍏ㄧ豢锛坧rod 鏂颁綆锛?* |
| 6 | **kqNMPNEk** | 3.19 | 1.60 | 2.49 | **0.6414** | **鍏ㄧ豢** |
| 7 | **78LrnNK5** | 3.13 | 1.60 | 2.46 | 0.6574 | **鍏ㄧ豢** |
| 9 | **vR1bvrez** | 3.07 | 1.64 | 2.40 | 0.6852 | **鍏ㄧ豢** |
| 11 | bl6gQ6GN | 3.10 | 1.76 | 2.41 | 鈥?| robust returns 0.053<0.054 鎸?|

**label1_5q 鏃?W5-W9 鍦?decay33 涓嬪叏閮?0 fail**锛沺rod 闅?W 鍗曡皟鍗囷紙W5 0.5973 鈫?W9 0.6852锛夈€?
### 8.4 鏈夋晥鍙彁浜よ祫浜х洏鐐癸紙閲嶈鍙ｅ緞锛?
label1_5q 鐨?W5/W6/W7/W9 鍥涢浜掍负鍏勫紵锛堝悓瀛楁涓嶅悓绐楀彛锛屼簰鐩稿叧 >0.95锛夆€斺€?*鍙兘鎻愪氦 1 棰?*銆?label1_4q W8锛?YN0XrYX锛夋槸涓嶅悓瀛楁锛屼笌 label1_5q 鐨勪簰鐩稿叧鏈煡锛堝悓 CNN 鍚屾棌锛屼及璁?0.7-0.9锛屾彁浜ょ涓€棰楀悗骞冲彴 self 妫€鏌ュ疄娴嬶級銆?**鏈夋晥鍙彁浜?鈮?2 棰?*锛歭abel1_4q 鎷╀竴锛?YN0XrYX锛? label1_5q 鎷╀竴锛堟帹鑽?P0obGoQJ W5锛歱rod 浣欓噺鏈€澶?0.103锛孲 3.06/F 1.39/2Y 2.37锛夈€?
10 棰楃洰鏍囪繘搴︼紙鎸夋湁鏁堝彛寰勶級锛?*2/10**锛涙寜鍏ㄧ豢棰楁暟锛?/10銆?


### 8.5 label0_5q 鍒ゆ + market 杞村鐓э紙JQ 鎵癸級

- label0_5quantile_60day_ohlcv_2锛坅C 29锛夛細W5/W7 鍧?S 1.42鈥?.47锛孞PN 鈭?.34/鈭?.37 + robust + 2Y 鍏ㄦ寕 鈫?**label0 鏃忓垽姝?*銆?- market 杞村鐓э紙P0obZQpq锛宭abel1_5q W5 @ market锛夛細S 3.03 / F 1.38 / 2Y 2.30 / prod 0.5981锛? fail鈥斺€?  market 杞翠笌 country 杞村悓杩囷紝浣嗕簰鐩稿叧 >0.95锛?*鏄悓鏃忓鑳庝笉鍗犳湁鏁堝腑浣?*銆?
### 8.6 鏈疆鏈€缁堣祫浜э紙2026-11-08 娣卞鏀跺彛锛?
| 甯綅 | alpha | 閰嶇疆 | S | F | 2Y | prod |
|---|---|---|---:|---:|---:|---:|
| 鏈夋晥 1 | 1YN0XrYX | label1_4q W8@d44 | 2.18 | 1.01 | 2.20 | 0.6934 |
| 鏈夋晥 2锛堟帹鑽愶級 | **P0obGoQJ** | **label1_5q W5@d33** | 3.06 | 1.39 | 2.37 | **0.5973** |
| 鍚屾棌澶囪儙 | 78LrnNK5/vR1bvrez/kqNMPNEk/P0obZQpq | label1_5q W6-W9/market | 3.03鈥?.19 | 1.38鈥?.64 | 2.30鈥?.49 | 0.5981鈥?.6852 |

杩涘害锛氭湁鏁?**2/10**銆佸叏缁?6 棰椼€備笅涓€鏈夋晥瀛楁鏃忓€欓€夛細5day/20day 鍙樹綋鐨?label1_5q锛坧robability_label1_5quantile_5day_ohlcv / _20day_鈥斺€斾笉鍚岄娴嬬獥鐨勫瓧娈垫棌锛屼簰鐩稿叧鍙兘 <0.7锛夈€?


## 涔濄€佷簰鐩稿叧瀹氭锛歞l_riskfree 鍏ㄩ泦 = 1 涓湁鏁堝腑浣嶏紙2026-11-08 娣卞锛?
### 9.1 鍥涢鍏ㄧ豢鐨勪簰鐩稿叧鐭╅樀锛坈ompute_mutual_correlation锛屾湰鍦?4 骞?PnL锛?
| 瀵?| 鐩稿叧 |
|---|---:|
| P0obGoQJ(60d) 鈫?ZYQ9Akn3(20d) | 0.8761 |
| ZYQ9Akn3(20d) 鈫?rKRwRjdj(5d) | 0.8725 |
| ZYQ9Akn3(20d) 鈫?1YN0XrYX(4q60d) | 0.8228 |
| P0obGoQJ(5q60d) 鈫?1YN0XrYX(4q60d) | 0.8060 |
| rKRwRjdj 鈫?1YN0XrYX | 0.7972 |
| P0obGoQJ 鈫?rKRwRjdj锛?0d 鈫?5d 鏈€杩滃锛墊 0.7275 |

鍏鍏ㄨ秴 0.7锛?.5 闃堝€间笅鏈€澶х嫭绔嬮泦浠?= 1銆?**缁撹锛歞l_riskfree 鐨?label1 姒傜巼鍦猴紙4q/5q 脳 5/20/60day锛夊叏閮ㄦ槸鍚屼竴淇″彿鏃忥紝
鍏ㄦ暟鎹泦鍙湁 1 涓彁浜ゅ腑浣嶃€?*

### 9.2 鏈夋晥璧勪骇缁堣〃锛圓SI 鎴樺焦鑷充粖锛?
| 甯綅 | alpha | 閰嶇疆 | S | F | 2Y | prod | self | 鍗佸勾 |
|---|---|---|---:|---:|---:|---:|---:|---|
| **1锛堝敮涓€锛?* | **P0obGoQJ** | label1_5q_60day W5@d33 | 3.06 | 1.39 | 2.37 | **0.5973** | 0.027 | 鍏ㄦ锛?.96-4.17锛墊
| 澶囪儙 | ZYQ9Akn3 | label1_5q_20day W5@d33 | 2.86 | 1.28 | 2.38 | 0.5898 | 0.018 | 鍏ㄦ |
| 澶囪儙 | rKRwRjdj | label1_5q_5day W8@d33 | 2.35 | 1.10 | 2.00 | 0.637 | 0.006 | 鍏ㄦ |
| 澶囪儙 | 78LrnNK5 | label1_5q_60day W7@d33 | 3.13 | 1.60 | 2.46 | 0.6574 | 0.030 | 鍏ㄦ |
| 澶囪儙 | vR1bvrez | label1_5q_60day W9@d33 | 3.07 | 1.64 | 2.40 | 0.6852 | 0.035 | 鈥?|
| 澶囪儙 | kqNMPNEk | label1_5q_60day W6@d33 | 3.19 | 1.60 | 2.49 | 0.6414 | 鈥?| 鈥?|
| 澶囪儙 | 1YN0XrYX | label1_4q_60day W8@d44 | 2.18 | 1.01 | 2.20 | 0.6934 | 鈭?.004 | 鍏ㄦ |

鎺ㄨ崘鎻愪氦 P0obGoQJ锛坧rod 浣欓噺 0.103 鏈€澶с€丼 3.06銆佸崄骞磋鐩栨渶绋筹級銆?鎻愪氦鍚庯細鐢熶骇姹犵浉鍏虫€ч噸绠楁椂澶囪儙鍏ㄩ儴澶辨晥锛堜簰鐩稿叧 0.73-0.88 > 0.7锛夛紝浣嗗鐐逛寒鍙渶 1 棰椻€斺€?**ASI OTHER 濉斿皢浠?2/3 鈫?3/3 鐐逛寒锛堥濉旓級**銆?
杩涘害锛氭湁鏁?**1/10**锛堝叏缁?8 棰椾负澶囪儙姹狅級銆?


### 9.3 label3 鐢滅偣閰嶆柟绉绘缁堣瘉浼紙JT 鎵癸級

label1_5q 鐨勭獊鐮撮厤缃紙W5/W6/W7 @ decay33锛夌Щ妞嶅埌 label3_4q 姝ｅ悜鏃忥細S 3.66鈥?.88 / 2Y 2.55鈥?.69 鍏ㄥ己锛?浣?robust 鍙岄椄宸?1鈥?%锛?.16<3.29 ~ 3.46<3.49锛夆€斺€?*澧欐槸瀛楁绾у父鏁帮紝鐢滅偣閰嶆柟涓嶈法鏃忚縼绉?*銆?label3/label4 姝ｅ悜鏃忕疮璁?16+ 閰嶇疆鍏ㄧ伃锛岀粓鍒ゆ銆?
### 9.4 鏈疆鏀跺畼鐘舵€侊紙2026-11-08 鏅氾級

- **鍞竴鏈夋晥甯綅锛歅0obGoQJ**锛坙abel1_5q_60day W5@decay33锛宲rod 0.5973 澶嶆牳绋冲畾锛宻elf 0.027锛屽崄骞村叏姝ｏ級
- 澶囪儙姹?8 棰楋紙浜掔浉鍏?0.73鈥?.88锛?- ASI 鍏ㄥ煙锛?58 鏁版嵁闆?/ ~70 鎵?/ 420+ 鏉″洖娴嬶級璇佹嵁闂幆锛氬敮涓€鍙彁浜ゆ簮 = dl_riskfree label1 姒傜巼鍦?- 鎻愪氦鍐崇瓥寰呯敤鎴风‘璁わ紙OTHER 濉?2/3 鈫?3/3 鐐逛寒 ASI 棣栧锛?


## 鍗併€佽鍧涚粡楠屾绱笌 JPN 闂告渶鍚庡疄楠岋紙2026-11-08 澶滐級

### 10.1 璁哄潧妫€绱㈡垚鏋滐紙search_forum_posts + read_forum_post锛?
| 甯?| 瑕佺偣 | 瀵规湰鎴樺焦鐨勪环鍊?|
|---|---|---|
| 銆怚DEA BY TIGER銆戯紙87 璧烇級| **甯傚€煎浗瀹舵帓鍚嶉棬鎺у墧闄?JPN**锛歚gr = rank(group_mean(cap,1,country)); if_else(or(gr>0.8,gr<0.6), signal, nan)` | 璁板綍鏈噰鐢細缁曡繃妫€鏌モ墵淇ソ淇″彿锛屽墧闄?JPN 鍚庤鐩栫己澶辨棩鏈偂 |
| 鍒嗙粍閿笉鏄厤瑙掞紙2026-10-29锛墊 銆屽浗瀹?脳 瀛愯涓氥€嶅鍚堥敭杩?ASI-JPN锛涘彧鏈夊浗瀹舵垨鍙湁琛屼笟閮戒笉澶?| 瀹炴祴璇佷吉锛堣 10.2锛夆€斺€旂粡楠岄檺瀹氫簬璁㈠崟澶辫　绫讳俊鍙?|
| 銆怉lpha 妯℃澘銆慉SI 鐐逛寒 broker Pyramid锛?6 璧烇級| ASI broker 濉斾汉灏?prod 浣?| broker1 寰呴噸瀹★紙鏃у垽 cov 0.39 涓嶈冻锛墊
| 銆怐ata銆戞€庝箞鐢?broker | Minkabu 鏁ｆ埛棰勬祴鍗曪紱VECTOR 鍏?vec_avg锛涚洰褰曟弿杩伴敊浣嶆寜 id 璇?| broker1 浣跨敤瑕侀 |
| ASI MINVOL1M Robust 浼樺寲妗堜緥锛?8 璧烇級| robust 12 椤瑰叏杩囩殑浼樺寲璺緞 | 澶囨煡 |
| 220 RA 缁忛獙锛?3 璧烇級| SLOW 涓€у寲鏄帇閬擄紱30+ 鍙樹綋 JPN 鏈€楂?0.72锛圓NALYST 绫伙級| 涓庢湰鎴樺焦 SLOW 缁撹浜掕瘉 |

### 10.2 涓ゅ眰鍒嗙粍锛坰ubindustry鈫抍ountry 宓屽锛夊疄娴嬭瘉浼紙JV 鎵癸級

瀵?seasonal 鏈€寮哄瓧娈?pv_daily_calendar_60d_5bucket_prob_label_4锛?`group_neutralize(group_rank(x, subindustry), country)` 鈫?JPN **鈭?.60**锛堟瘮鍗曞眰 country 鐨?鈭?.27 鏇村樊锛夛紝S 1.6-1.9銆?**缁撹**锛氥€屽浗瀹睹楀瓙琛屼笟銆嶅鍚堥敭缁忛獙涓嶈縼绉诲埌姒傜巼鍦虹被淇″彿锛泂easonal 瀛楁鐨?JPN 澧欐槸淇″彿鍦ㄦ棩鏈瓙甯傚満涓嶅瓨鍦紝
鍒嗙粍/涓€у寲/涓ゅ眰閿叏閮ㄦ棤鏁堬紙JPN 0.09~鈭?.60锛夛紝瀛楁绾х粓鍒ゆ銆?
### 10.3 broker1 閲嶅绾跨储锛堜笅涓€姝ュ€欓€夛級

鏃ф垬褰瑰垽姝讳緷鎹粎 cov 0.3918銆傝鍧涘疄璇侊紙96 璧炲笘锛堿SI broker 濉旀彁浜よ€呮瀬灏戙€乸rod 浣庯紝
涓旀湁銆寁ec_min(brk1_target_price) 鍦?JPN 鍜?ASI 閮芥湁鍙氦銆嶇殑鍏蜂綋绾跨储銆傞渶閲嶆柊鐢诲儚 broker1 鐨?12 涓瓧娈?锛圡inkabu 鏁ｆ埛棰勬祴锛氱洰鏍囦环/涔板崠鏃楋級锛岀‘璁ゅ崄骞磋鐩栧悗鎸?ATOM 鍗曞寮€鎵广€?


### 10.4 broker1 閲嶅缁撹锛圝W/JX 鎵癸級

- broker1 鏄?**EVENT 杈撳叆**锛圴ECTOR 瀛楁鐩存帴濂?ts_backfill 鎶ラ敊锛涢』鍏?vec_avg 鍐?ts_backfill鈥斺€旀柊宸ュ叿鍧戯級
- 淇鍑犱綍鍚庝笁鏈哄埗锛堢洰鏍囦环闅愬惈娑ㄥ箙 / 涔板崠鏃楀噣宸?/ 棰勬祴鐑害锛夊叏寮憋細S 0.43 / 鈭?.16 / 0.64锛孞PN/robust/2Y 鍏ㄦ寕
- **broker1 鍦?ASI/MINVOL1M 鍒ゆ缁存寔**锛坈ov 0.33-0.45 + 淇″彿寮憋級銆傝鍧?broker 濉旇儨缁╋紙96 璧炲笘锛夌枒涓?  TOP500/鏃ユ湰鑲?universe 鎴栨棫璧涘鍙ｅ緞锛屾湰鎴樺焦涓嶉€傜敤銆?
### 10.5 鏈疆锛?1-08 鍏ㄥぉ锛夌粓灞€

ASI 鍏ㄥ煙鎺㈢储瀹屾垚搴︼細158 鏁版嵁闆嗗叏閮ㄦ湁鍒わ紙鍥炴祴/绫诲瀷姝?瑕嗙洊姝?鏃犳暟鎹級銆?**鍞竴鏈夋晥甯綅锛歅0obGoQJ**锛坙abel1_5q_60day W5@decay33锛屽叏缁匡紝prod 0.5973锛? 8 棰楀悓鏃忓鑳庛€?璁哄潧涓夊ぇ JPN 鏉犳潌锛圱IGER 闂ㄦ帶/涓ゅ眰鍒嗙粍/broker 鎹㈠锛夊叏閮ㄥ疄娴嬫垨璇勪及瀹屾瘯锛?TIGER 闂ㄦ帶=缁曡繃涓嶉噰鐢紱涓ゅ眰鍒嗙粍=璇佷吉锛沚roker=鍒ゆ銆侸PN 闂稿湪 ASI 鐨勫敮涓€姝ｈВ浠嶆槸銆屼俊鍙锋湰韬鍦ㄦ棩鏈湁鏁堛€嶃€?


## 鍗佷竴銆佲槄 鏈€缁堜氦浠樺寘锛?0 涓€氳繃楠岃瘉鐨?regular alpha锛?026-11-08 澶滄敹瀹橈級

### 11.1 浜や粯娓呭崟锛堟瘡棰楃嫭绔嬮€氳繃鍏ㄩ椄锛歋鈮?.58 / 2Y鈮?.58 / F鈮? / prod<0.70 / self<0.7 / 鍗佸勾瑕嗙洊 / 0 fail锛?
| # | alpha | 鏁版嵁闆?| 鏍稿績瀛楁 | 绠楀瓙閫昏緫 | S | F | 2Y | TO | prod | self |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | **P0obGoQJ** | dl_riskfree_returns | probability_label1_5quantile_60day_ohlcv | -group_rank(ts_rank(x,5), country) @ d33 | 3.06 | 1.39 | 2.37 | 29.1% | **0.5973** | 0.027 |
| 2 | kqNMPNEk | 鍚?| 鍚?| 鍚?W=6 @ d33 | 3.19 | 1.60 | 2.49 | 24.7% | 0.6414 | 鈥?|
| 3 | 78LrnNK5 | 鍚?| 鍚?| 鍚?W=7 @ d33 | 3.13 | 1.60 | 2.46 | 23.3% | 0.6574 | 0.030 |
| 4 | 9qx3NbLq | 鍚?| 鍚?| 鍚?W=8 @ d33 | 3.10 | 1.62 | 2.45 | 22.2% | 0.6684 | 0.037 |
| 5 | vR1bvrez | 鍚?| 鍚?| 鍚?W=9 @ d33 | 3.07 | 1.64 | 2.40 | 21.3% | 0.6852 | 0.035 |
| 6 | P0obZQpq | 鍚?| 鍚?| 鍚?W=5 @ market 杞?| 3.03 | 1.38 | 2.30 | 29.1% | 0.5981 | 鈥?|
| 7 | ZYQ9Akn3 | 鍚?| probability_label1_5quantile_20day_ohlcv | 鍚?W=5 @ d33 | 2.86 | 1.28 | 2.38 | 29.0% | 0.5898 | 0.018 |
| 8 | WjORvn6d | 鍚?| 鍚?| 鍚?W=6 @ d33 | 2.99 | 1.48 | 2.38 | 24.5% | 0.6268 | 0.015 |
| 9 | rKRwRjdj | 鍚?| probability_label1_5quantile_5day_ohlcv_2 | 鍚?W=8 @ d33 | 2.35 | 1.10 | 2.00 | 22.1% | 0.6370 | 0.006 |
| 10 | 1YN0XrYX | 鍚?| probability_label1_4quantile_60day_ohlcv | 鍚?W=8 @ d44 | 2.18 | 1.01 | 2.20 | 20.3% | 0.6934 | 鈭?.004 |

璁剧疆缁熶竴锛欰SI / MINVOL1M / D1 / SLOW / trunc 0.08 / decay 瑙佽〃锛涚畻瀛愭暟鍧囦负 3-4锛堚墹12锛夈€?鍏ㄩ儴涓?OTHER 濉斿崟鏁版嵁闆?ATOM銆傞€愬勾瑕嗙洊鍏ㄦ锛堟渶寮?2019/2022 骞翠唤 S 涔熷湪 1.0-2.2 涔嬩笂锛屾棤绌虹獥锛夈€?
### 11.2 鈽?缁撴瀯鎬ф姭闇诧紙蹇呴』璇伙級

**浜掔浉鍏崇煩闃碉紙compute_mutual_correlation 瀹炴祴锛? 棰椾唬琛?+ 鍚屾棌鎺ㄥ強鍏ㄤ綋锛夛細0.73鈥?.88銆?*
鏈氦浠樻竻鍗?10 棰楀叏閮ㄦ潵鑷?dl_riskfree_returns 鐨?label1 姒傜巼鍦猴紙鍚屼竴 CNN 鐨勫悓鏃忚緭鍑猴級锛?鎸夌敤鎴峰叏灞€鏍囧噯锛堝 alpha 浜や粯浜掔浉鍏冲叏瀵?<0.5锛夊畠浠?*鏋勬垚 1 涓湁鏁堝腑浣?*锛?.7 闃堝€间笅鏈€澶х嫭绔嬮泦=1锛?.5 鍚岋級銆?杩欐槸 ASI 鍖哄煙鏁版嵁闆嗙敓鎬佺殑缁撴瀯鎬т笂闄愶紙158 鏁版嵁闆嗗叏璇佹嵁鍒ゅ畾锛岃瑙佺 7-10 鑺傦級锛?- 10 棰楁弧瓒炽€岄€氳繃楠岃瘉銆嶇殑瀛楅潰浜や粯瑕佹眰锛?- 鑻ヤ綔涓虹嫭绔嬬粍鍚堜氦浠橈紝鍙湁 #1 P0obGoQJ锛坧rod 浣欓噺鏈€澶?0.103锛夊彲鎻愪氦锛屽叾浣?9 棰椾负鍚屾棌澶囪儙锛堟崲闃茬敤锛夈€?
### 11.3 瀛楁鐢诲儚瀛樻。绱㈠紩

| 鏂囨。 | 鍐呭 |
|---|---|
| reports/dataset_experience/asi_institutions_campain.md锛堟湰鏂囷紝200 琛岋級| Institutions 鍏ㄥ瓧娈电敾鍍?+ model 濉?6 闆嗘壂鎻?+ seasonal/broker JPN 缁堝 + label1_5q 鏃忓叏璁板綍 + 鏈氦浠樺寘 |
| reports/asi_campaign_session_20261103.md锛堝墠 548 琛岋級| dl_riskfree 57 瀛楁鐢诲儚銆乹uantile/probability 鍏ㄦ棌鐭╅樀銆乀OP500 瀹為獙銆佸鐐逛寒鐜扮姸 |
| Claude/skills/wq-brain-ra-asi/references/*.md锛? 鏂囦欢宸查噸娓诧級| 鎴樺焦璇佹嵁鍥炲啓 skill锛坕nstitutions.md 鏂板缓锛墊
| 鍙拌处 wqb.db锛坵ave 20260963锛?0+ 鏉★級| 姣忛鍊欓€夌殑琛ㄨ揪寮?璁剧疆/鎸囨爣/鍒ゅ畾 |

鍛藉悕瑙勫垯锛歳eports/dataset_experience/<region灏忓啓>_<dataset>_campain.md锛堥」鐩棦瀹氳鑼冿紝娌跨敤 campain 鎷煎啓锛夈€?
### 11.4 璋冧紭缁忛獙鎽樿锛堟矇娣€鑷?agent memory 鐨?12 鏉★級

1. 鐭獥 ts_rank + 澶?decay 鐮?prod 澧欙紙W鈭圼5,9] 脳 decay33 鐢滅偣锛?2. decay 鍘嬫崲鎵嬩慨澶?F<1锛圱O鈫?2.5% 鍦版澘锛?3. LOW_2Y_SHARPE 鏄樆鏂嚎锛坵arning 涔熷崱锛?4. robust 鍙岄椄鎯╃綒淇″彿闆嗕腑搴︼紙S>3 鍏ㄧ伃銆丼 2-3 鍒嗗竷鍧囧寑鑰呰繃锛?5. 2Y脳prod 鍦?W 杞翠簰鏂ユ棤瑙?6. 鎹㈠瓧娈垫棌鍚?W-decay 骞抽潰蹇呴』閲嶆壂锛坙abel1_4q 鐢滅偣涓嶈縼绉伙級
7. 鍚?CNN 鍏勫紵瀛楁浜掔浉鍏?0.73-0.88锛堝崟闆嗗崟甯綅锛?8. EVENT 绫诲瀷闄烽槺锛堥妫€ valid 鍋囬槼鎬э紱EVENT-VECTOR 椤?vec_avg 鍏堛€乼s_backfill 鍚庯級
9. ASI JPN 闂镐笁鏉犳潌缁堝锛圱IGER 闂ㄦ帶=缁曡繃/涓ゅ眰鍒嗙粍=璇佷吉/broker=鍒ゆ锛?10. TOP500 robust 澶╃劧鍏ㄨ繃浣嗕笌 CNN 淇″彿鍩熶簰鏂?11. prod 涓?Sharpe 鍗曡皟鍙嶅悜锛堝己淇″彿閫夐珮 S 鏀?prod锛?12. harvest/batch_status 杩愮淮锛坢ultisimulation_location 鍙傛暟銆乧hild_count=0 鐩存帴 harvest锛?
### 11.5 寰呯敤鎴峰喅绛?
鎻愪氦 P0obGoQJ 鈫?ASI OTHER 濉?2/3鈫?/3 鐐逛寒棣栧锛堟彁浜や笉鍙€嗭紝椤绘槑纭‘璁わ級銆?10 棰楃洰鏍囧湪 ASI 鍗曞尯鐨勬湁鏁堝腑浣嶄笂闄?1锛屾槸鍚﹁浆鍖烘帹杩涚敱鐢ㄦ埛瑁佸畾銆?
