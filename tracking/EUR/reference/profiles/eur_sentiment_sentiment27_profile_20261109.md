# EUR × sentiment27 字段画像（2026-11-09）

> 30/30 全量（complete=true）；Website Popularity Rankings（Tranco 网站流量排名，与 sentiment26 同源双版本）
> 塔位：SENTIMENT(×1.4，2/3)；拥挤度：aC 1160 / uC 404；os_is 0.2154

## 一、字段结构
双前缀（snl27 cov 0.75-0.91 / snt27 cov 0.90-1.0）：avgranking、rank（Tranco 日排名）、relpopularity1/08（1/rank 复合注意力分）、kurtosis/skewness（排名分布形状）、top{50,75}pctranking(avg)、totaldomains、dltcc（国家域）。全部 VECTOR。

## 二、判定
1. **sentiment27 天花板已 5 次确认**（S 1.33，returns 5.68%，结构/轴/幂次/平滑/L2 级联/vec 聚合/16 包装算子全试）——存量结论覆盖本集全部读数
2. snt27_relpopularity1（uC 104/aC 136 最热）= E56Jea7P 的小腿读数已占用
3. **判定：天花板 1.33 关闭（存量结论沿用），不投槽**
