# Wave3 news20 派发记录

- 触发：Wave2 other553 max|S|=0.71 < 1.0（决策树换集）
- 数据集：news20（Web Sources News Sentiment；news 塔 0/3；ATOM 单集）
- 换集原因链：严格 SM 不可用 → forum 全灭 → other553 无 S≥1.0 活苗
- 设置：KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08 · nan OFF
- preflight：valid=true · unknown_fields=[] · 8 字段全在
- 条数：8（N01–N08）
- tags：N01_ssc / N02_ssc_rel / N03_nip / N04_evt_snt / N05_novelty / N06_evt_cnt / N07_ssc_dlt / N08_qmb
- multisim: `1fpAhv3iZ4LBcy01eXSMAA4P`
- location: https://api.worldquantbrain.com/simulations/1fpAhv3iZ4LBcy01eXSMAA4P
- 仿真≠提交；并发占用 1/2（Wave2 已释放）
- reserve 未派：N09_qep / N10_ssc_std
