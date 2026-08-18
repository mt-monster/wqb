# -*- coding: utf-8 -*-
"""波10 T1/T2 回收结论 + institutions6 判死写入 WAVE_LEDGER.md 与 ledger.json。"""
import json, os, io

ROOT = r'd:\coding\traeCN_project\wqb\tracking\USA'
LEDGER_MD = os.path.join(ROOT, 'WAVE_LEDGER.md')
LEDGER_JSON = os.path.join(ROOT, 'ledger.json')

section = '''
### 精调批回收（TUNE/T1/T2，24 条，累计 96 条 PASS=0）
- **TUNE = 1CcZ1TgWQ4CvbxeuU6tPqmJ**（8 条，signed_power 指数矩阵 0.3/0.5/0.7/1.5/2.0）：**5 档指数指标完全相同（1.03/0.55/9.9%/7.2bp/2y 2.01）——signed_power 是单调变换，被外层 quantile 完全抵消**；真正解锁变量是 decay2，指数维度实测无效
- **T1 = aInFTd2m54Zc2eEvZbZar0**（8 条，TOP3000/decay1：share 复合 × SUBIND/INDUSTRY、num reverse、value 复合、share−count、双水平复合、count 差 reverse）：sharpe 0.70-1.04，**margin 全崩回 0.0-0.1bp**（d2 时 7.2bp）→ decay1 是负贡献，decay2 为 margin 唯一解锁点
- **T2 = 1RYSQiaC4ZkaVhWBp8euRD**（8 条，TOP1000/decay2 核心骨架 8 条）：sharpe 0.03-0.55、margin 0.0-0.1bp 全灭 → **TOP1000 universe 对 institutions6 负贡献**（机构信号在 TOP1000 上无边际）

### ★institutions6 判死定案（96 条 PASS=0，维度全穷尽）
1. 已穷尽配置矩阵：**4 中性化（SUBIND/INDUSTRY/STATISTICAL）× 7 decay 档（1/2/4-16）× 2 universe（TOP3000/TOP1000）× 21 字段全口径（share/value/quantity/count/num/market_value）× 全骨架（水平/占比/差值/净买家/双水平复合）× signed_power 指数（实测无效）**
2. 天花板：sharpe 1.03（ZYEVZQw0）/ fitness 0.59（mL5nOo22）/ subU 0.53，距闸门 1.58 差 1.53 倍；虽未达 3 倍结构性线，但**配置空间已数学穷尽 + 论坛求证无新招（仅数据集知识帖/工具帖）** → 按"模板多样性已穷尽且无计可施"条款判死
3. 核心教训：① decay2 是 margin/tv 双解锁点，但 sharpe 天花板由 13F 低频信息含量决定；② 单调变换（signed_power 等）在 quantile 外层完全失效；③ TOP1000 无增量
4. **禁发**：institutions6 任何表达式（share/value/quantity/count/num/market_value 全口径）

### 下一波决策（波11）：切换 order_book_imbalance
1. **数据集**：order_book_imbalance（imbalance 金字塔唯一数据集，24 用户/198 字段/42 alpha/pyr 1.4，极蓝海）——订单流失衡微结构风格，与全部已判死风格（情绪/期权/借贷/分析师/机构持股）独立；198 字段全 VECTOR 型
2. **前置**：198 字段登记 fields_gate.json（VECTOR 型需 vec_* 聚合包裹，注意 GROUP 位门禁）；imbalance 类骨架（净失衡/多档失衡）首发探针批
3. 禁发延续：analyst44/option/sentiment/si3/institutions6 全系
4. 提交前置不变：数值七闸门 → PROD<0.7 → robust/过拟合

---

## 每 10 波全量多样性评估（独立成章）'''

with open(LEDGER_MD, encoding='utf-8') as f:
    md = f.read()

anchor = '---\n\n## 每 10 波全量多样性评估（独立成章）'
assert anchor in md, 'anchor not found in WAVE_LEDGER.md'
md = md.replace(anchor, section, 1)
with open(LEDGER_MD, 'w', encoding='utf-8') as f:
    f.write(md)
print('WAVE_LEDGER.md updated')

with open(LEDGER_JSON, encoding='utf-8') as f:
    led = json.load(f)

led['wave_in_progress'] = '波11: order_book_imbalance 首攻（imbalance 金字塔唯一数据集，198 VECTOR 字段登记中）'
led['backtests_total'] = '波1-9: 352 条 + 波10 已回收 96 条（WW~T2 含重复 8 条）= 448 条'
led['datasets']['institutions6'] = {
    'status': 'dead',
    'evidence': '96 条 PASS=0；sharpe 天花板 1.03（ZYEVZQw0 d2），4 中性化 × 7 decay × 2 universe × 21 字段 × 全骨架穷尽；decay1/TOP1000/STATISTICAL 均负贡献；signed_power 单调变换被 quantile 抵消实测无效',
    'ban': 'share/value/quantity/count/num/market_value 全口径任何表达式禁发'
}
led['wave10_primary'] = 'institutions6 判死（96 条 PASS=0，维度全穷尽，天花板 1.03 差 1.53 倍）；decay2 解锁 margin 但 sharpe 天花板由 13F 低频信息含量决定'
led['dead_summary']['institutions'] = ['institutions6']
led['dead_summary']['submission_candidates'] = 0
led['best_candidates'].append({
    'id': 'ZYEVZQw0',
    'sharpe': 1.03, 'fitness': 0.55, 'tv': 0.099, 'margin_bp': 7.2,
    'two_year_sharpe': 2.01, 'subU': 0.37,
    'notes': 'inst6 冠军（share−quantity复合 d2 SUBIND），已随 institutions6 判死封存'
})
led['structural_findings'].append(
    '单调变换定律：signed_power(x,p) 等单调变换被外层 quantile 完全抵消，指数参数无效（TUNE 批 5 档指数同指标实证）'
)
led['structural_findings'].append(
    'decay 阶梯实证：d1 margin 0.1bp → d2 7.2bp（70 倍）→ d8-16 1.0-3.8bp；decay2 是 institutions6 margin 唯一解锁点'
)
led['structural_findings'].append(
    'universe 敏感度：TOP1000 下 institutions6 信号全灭（sharpe≤0.55），机构信号无小盘边际'
)
led['pending']['in_flight'] = []
led['pending']['next_dataset'] = 'order_book_imbalance（imbalance 金字塔唯一数据集，24 用户/198 字段/42 alpha/pyr 1.4，全 VECTOR）'

with open(LEDGER_JSON, 'w', encoding='utf-8') as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print('ledger.json updated')
