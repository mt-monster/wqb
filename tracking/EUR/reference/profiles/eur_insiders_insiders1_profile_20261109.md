# EUR × insiders1 字段画像（2026-11-09）

> 9/9 全量（complete=true）；Global Insider Trading Data（全球内部人交易）
> 塔位：INSIDERS(×1.1，2/3)；拥挤度：aC 394 / uC 191；os_is 0.3509

## 一、字段清单（9 字段，全 VECTOR，cov 0.5512）
insd1_shares（交易股数，uC 72 最热）、insd1_price（交易价）、insd1_value/valueeur（交易金额）、insd1_holdings（交易后持股）、insd1_tradesignificance（交易重要性 1-5 分）、max_trade_price、insd1_gvkey（标识）、transaction_currency_code

## 二、判定
1. **cov 0.5512 < 0.85 → 覆盖判死**（sub 闸结构性不可达）
2. 事件型 VECTOR → TO 爆炸风险（同族 insider_feats/insider_trx_matrix 均已 TO 判死）
3. **判定：覆盖判死 + 同族 TO 前科，排除**
