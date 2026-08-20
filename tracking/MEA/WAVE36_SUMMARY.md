# MEA Wave 36 战役进展

## 阶段
- S-PRE/S0/S1/S2-D/S2' 已在 wave35 完成，复用设置
- S3: 批量回测（本波）

## 关键修正（相对 wave35）
- wave35 的 6 个 analyst7 表达式字段虚构（analyst_eps_*/analyst_consensus_*/analyst_flash_* 不存在），全部 ERROR 连坐 → 已重写为真实 price_target 字段
- wave35 的 16 个子模拟全部 404 过期 → 重新提交

## 数据集方向决策
- 用户确认：未点亮金字塔优先（fundamental72 1.5x + analyst7 1.4x）
- 接受低 coverage（0.545/0.478），tier1 model25/model31 已点亮不主攻

## 提交批次（2批×8，五槽填槽）
- Batch 1 (fundamental72 ×8): multisim `14B2rg7TK4uwbbf105KWmxf7`
  - EPS动量/增长、盈利能力、现金流质量、FCF收益率、ROE、低负债、低应计
- Batch 2 (analyst7 ×6 + fnd72 ×2): multisim `3MIjAO59b4SPc6NbWhrIQPA`
  - PT溢价、PT动量、PT修订净额、PT离散度(反向)、PT覆盖度、PT中位/均值比、EPS+现金流复合、现金/资产

## 设置
MEA/TOP400/D1/SECTOR/decay=4/truncation=0.08/maxTrade=ON/pasteurization=ON/unitHandling=VERIFY/nanHandling=OFF

## 闸预检
- gate.py 5闸：fnd72 10/10 pass，analyst7 6/6 pass

## 筛选条件
sharpe>1.58, fitness>1, 2ysharpe>1.6, margin>5bp, turnover 5%-30%
risk_neut: sharpe>1, fitness>0.7, margin>5bp, ra_failed_count=0

## 配额
48h/4，已用2，剩2，最早释放 2026-08-21T02:49 (约18h后)

## 目标
10个可提交alpha，相关性<0.5，策略风格完全不同，点亮fundamental+analyst金字塔

## 下一步
1. 轮询2批回测结果
2. 筛选达标alpha → robust test（换universe/neutralization）
3. 过拟合测试（2y sharpe）
4. 相关性矩阵 → 选10个<0.5
5. 过IS检查后设属性提交
