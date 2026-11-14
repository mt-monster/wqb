# pv30 积压清单（s2_pv30_d1，33 条从未回测）

生成：2026-11-11 只读查询 expressions 表；可直接整批派发（字段已预检存在）。

- [69455/gem] `days_from_last_change(sign(eighth_pca_component_top1200_group513))`
- [69456/gated] `days_from_last_change(sign(eleventh_pca_component_top1200_group513))`
- [69457/gem] `days_from_last_change(sign(fifteenth_pca_component_top1200_group513))`
- [69458/gem] `days_from_last_change(sign(fifth_pca_component_top1200_group513))`
- [69459/gem] `days_from_last_change(sign(fourteenth_pca_component_top1200_group513))`
- [69460/gem] `days_from_last_change(sign(ninth_pca_component_top1200_group513))`
- [69461/gem] `days_from_last_change(sign(seventh_pca_component_top1200_group513))`
- [69462/gem] `days_from_last_change(sign(tenth_pca_component_top1200_group513))`
- [69464/gated] `divide(subtract(ts_delta(eleventh_pca_component_top1200_group513, 5), ts_delta(eighth_pca_component_top1200_group513, 5)), add(abs(eleventh_pca_component_top1200_group513), abs(eighth_pca_component_top1200_group513)))`
- [69465/gem] `divide(subtract(ts_delta(fifteenth_pca_component_top1200_group513, 5), ts_delta(eighth_pca_component_top1200_group513, 5)), add(abs(fifteenth_pca_component_top1200_group513), abs(eighth_pca_component_top1200_group513)))`
- [69466/gem] `divide(subtract(ts_delta(eighth_pca_component_top1200_group513, 5), ts_delta(eleventh_pca_component_top1200_group513, 5)), add(abs(eighth_pca_component_top1200_group513), abs(eleventh_pca_component_top1200_group513)))`
- [69467/gem] `divide(subtract(ts_delta(fifteenth_pca_component_top1200_group513, 5), ts_delta(eleventh_pca_component_top1200_group513, 5)), add(abs(fifteenth_pca_component_top1200_group513), abs(eleventh_pca_component_top1200_group513)))`
- [69468/gem] `divide(subtract(ts_delta(fifth_pca_component_top1200_group513, 5), ts_delta(fifteenth_pca_component_top1200_group513, 5)), add(abs(fifth_pca_component_top1200_group513), abs(fifteenth_pca_component_top1200_group513)))`
- [69469/gem] `divide(subtract(ts_delta(fourteenth_pca_component_top1200_group513, 5), ts_delta(fifteenth_pca_component_top1200_group513, 5)), add(abs(fourteenth_pca_component_top1200_group513), abs(fifteenth_pca_component_top1200_group513)))`
- [69470/gem] `divide(subtract(ts_delta(fifteenth_pca_component_top1200_group513, 5), ts_delta(fifth_pca_component_top1200_group513, 5)), add(abs(fifteenth_pca_component_top1200_group513), abs(fifth_pca_component_top1200_group513)))`
- [69471/gem] `divide(subtract(ts_delta(fourteenth_pca_component_top1200_group513, 5), ts_delta(fifth_pca_component_top1200_group513, 5)), add(abs(fourteenth_pca_component_top1200_group513), abs(fifth_pca_component_top1200_group513)))`
- [69472/gem] `divide(subtract(ts_delta(fifteenth_pca_component_top1200_group513, 5), ts_delta(fourteenth_pca_component_top1200_group513, 5)), add(abs(fifteenth_pca_component_top1200_group513), abs(fourteenth_pca_component_top1200_group513)))`
- [69473/gem] `divide(subtract(ts_delta(fifth_pca_component_top1200_group513, 5), ts_delta(fourteenth_pca_component_top1200_group513, 5)), add(abs(fifth_pca_component_top1200_group513), abs(fourteenth_pca_component_top1200_group513)))`
- [69474/gem] `divide(subtract(ts_delta(eighth_pca_component_top1200_group513, 5), ts_delta(ninth_pca_component_top1200_group513, 5)), add(abs(eighth_pca_component_top1200_group513), abs(ninth_pca_component_top1200_group513)))`
- [69475/gem] `divide(subtract(ts_delta(eleventh_pca_component_top1200_group513, 5), ts_delta(ninth_pca_component_top1200_group513, 5)), add(abs(eleventh_pca_component_top1200_group513), abs(ninth_pca_component_top1200_group513)))`
- [69516/gem] `multiply(days_from_last_change(sign(eighth_pca_component_top1200_group513)), sign(second_pca_component_top400))`
- [69517/gem] `multiply(days_from_last_change(sign(eighth_pca_component_top1200_group513)), sign(sixth_pca_component_top400))`
- [69518/gem] `multiply(days_from_last_change(sign(eighth_pca_component_top1200_group513)), sign(thirteenth_pca_component_top400))`
- [69519/gem] `multiply(days_from_last_change(sign(eleventh_pca_component_top1200_group513)), sign(second_pca_component_top400))`
- [69520/gem] `multiply(days_from_last_change(sign(eleventh_pca_component_top1200_group513)), sign(sixth_pca_component_top400))`
- [69521/gem] `multiply(days_from_last_change(sign(eleventh_pca_component_top1200_group513)), sign(thirteenth_pca_component_top400))`
- [69522/gem] `multiply(days_from_last_change(sign(fifteenth_pca_component_top1200_group513)), sign(second_pca_component_top400))`
- [69523/gem] `multiply(days_from_last_change(sign(fifteenth_pca_component_top1200_group513)), sign(sixth_pca_component_top400))`
- [69524/gem] `multiply(days_from_last_change(sign(fifteenth_pca_component_top1200_group513)), sign(thirteenth_pca_component_top400))`
- [69525/gem] `multiply(days_from_last_change(sign(fifth_pca_component_top1200_group513)), sign(second_pca_component_top400))`
- [69526/gem] `multiply(days_from_last_change(sign(fifth_pca_component_top1200_group513)), sign(sixth_pca_component_top400))`
- [69527/gem] `multiply(days_from_last_change(sign(fifth_pca_component_top1200_group513)), sign(thirteenth_pca_component_top400))`
- [69619/gem] `ts_rank(tenth_pca_component_top1200_group513, 252)`