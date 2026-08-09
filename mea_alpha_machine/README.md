# MEA Alpha Machine — 一二三阶挖掘流水线(MEA / TOP400)

基于《WQ第五六节课代码/顾问参考代码》中 `machine_lib.py` + `Alpha Machine1.ipynb` 改造,面向 **MEA** 地区(EQUITY / TOP400 / delay=1 / SUBINDUSTRY)的字段回测。

## 文件

| 文件 | 说明 |
|---|---|
| `mea_machine_lib.py` | 改造版库(基于原 machine_lib.py) |
| `MEA Alpha Machine.ipynb` | 完整一二三阶流程,按序运行即可 |

## 对原代码的适配点

1. **登录**:`login()` 优先读环境变量 `BRAIN_EMAIL` / `BRAIN_PASSWORD`,回退到文件内默认凭据;不再使用占位符"邮箱/密码"。
2. **日期**:`get_alphas(..., year=2026)` 增加 `year` 参数,替代硬编码的 `2025-`;notebook 中自动取最近 7 天窗口。
3. **MEA 分组(二阶)**:`group_factory` 新增 `region="mea"` 分支 —— MEA 无 `fnd28` 数据集(原 `bps_group` 依赖 `fnd28_value_05480`,不可用),改用:
   - 通用分组:`market / sector / industry / subindustry`
   - bucket 分组:`cap` / `sector_cap` / `vol`
   - MEA 统计行业聚类(pv30):`sta2_top400_fact1~4_c2/c5/c10`
4. **一阶 region 化**:`get_first_order(pc_fields, ts_ops, region=...)` 新增 region 参数,内部 `group_factory` 不再硬编码 `"usa"`。
5. **prune 多前缀**:`mea_prune()` 按 MEA 数据集字段前缀(`mdl25/mdl31/fnd6/fnd72/analyst/est_/pv96/ern3`)逐组去重。
6. **数据集筛选**:MEA 数据集普遍较小,阈值由 `alphaCount>10000` 放宽为 `>1000`(原阈值下 MEA 只有 pv1 达标)。
7. **三阶事件**:`trade_when_factory` 用通用 open/exit 事件;`ern3_pre_reptime`(earnings3)在 MEA 存在,财报退出事件可用。

## 运行步骤

1. 打开 `MEA Alpha Machine.ipynb`,按序执行所有单元格。
2. 一阶模拟量大(10~20 万),如需试跑,设置 `FIRST_ORDER_LIMIT = 30000`(notebook 第 2 个单元格,默认 None 全量)。
3. 每阶跑完后自动拉取达标 alpha,进入下一阶;最后 `check_submission` 检查可提交性。

## 平台限制(MEA)

- 仅支持 **delay=1**
- Universe:`TOP400` / `TOP300`(本流程默认 TOP400)
- Neutralization:`NONE / MARKET / SECTOR / INDUSTRY / SUBINDUSTRY / COUNTRY`(无 REVERSION_AND_MOMENTUM 等)
- 金字塔:`MEA/D1/PV`(multiplier 1.1)等

## 已验证(2026-08-07)

- MEA/TOP400/SUBINDUSTRY 设置冒烟测试通过(alpha `ak1P6KMv`)
- 10 个 MEA 一阶表达式多模拟全部 COMPLETE(模拟 `30PxC9d1C4NbauCXVwhgR4e`),覆盖:
  - analyst7 VECTOR:`vec_avg(analyst_consensus_mean_estimate)` / `vec_avg(analyst_consensus_eps_low_estimate)`
  - fundamental72:`vec_avg(fnd72_pit_or_bs_a_bs_cash_near_cash_item)`
  - fundamental6:`fnd6_adesinda_curcd`
  - MEA 统计行业分组:`group_rank(..., densify(sta2_top400_fact3_c10))`
  - earnings3 事件字段:`ts_rank(ern3_pre_interval, 22)`
  - pv1 基础字段:`close/volume/returns/adv20` 及 `group_neutralize(..., densify(sector))`

> 注意:字段名必须严格以 API 返回为准(如 `analyst_consensus_mean_estimate` 而非手写的 `analyst_consensus_mean_eps`),notebook 中字段均从 `get_datafields` 自动拉取,不会出现笔误。
