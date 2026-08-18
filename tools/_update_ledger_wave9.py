# -*- coding: utf-8 -*-
"""更新 ledger.json：波9 判死 + option 类定案 + 波次推进。"""
import json

path = r'd:\coding\traeCN_project\wqb\tracking\USA\ledger.json'
with open(path, encoding='utf-8') as f:
    d = json.load(f)

d['updated'] = '2026-08-16'
d['waves_completed'] = 9
d['wave_in_progress'] = 10
d['backtests_total'] = '波1-9 约 328 条（波9 analyst44 24条已回收全灭；波10 inst6 WW/XX 在飞）'
d['whitelist'] = 'D1 scope 628 字段 / 10 数据集（analyst44 37字段 + institutions6 21字段 新登记）'

ds = d['datasets']

# analyst44 判死
ds['analyst44'] = {
    'status': 'dead',
    'evidence': 'consensus 修正类信号天花板 ~0.45（24条 PASS=0，最高 WjArQLLd 0.45）；RN 全负；3中性化x3decay 全灭；21d 修正稀疏多数为0',
    'ban': 'consensus 修正/水平/增长任何表达式禁发'
}

# option40 判死（option 类金字塔整体判死定案）
ds['option40']['status'] = 'dead_option_pyramid'
ds['option40']['note'] = '★option 类金字塔整体判死（option8+option40 88+条）：IV衍生族 PROD 0.83-0.91 结构性墙 + subU 结构性低 + 三武器无法解封；标准曲面 Greeks 弱信号；翻案批例外已失效'
ds['option40']['ban'] = 'IV 族/标准曲面任何表达式禁发'
ds['option40']['dead_alpha_prods'] = {
    'O0Gd05Ng': 0.8306,
    '3qpmqn9N': 0.8369,
    'VkGQ1LK5': 0.8787,
    'VkGQvdOw': 0.9018
}

# option8 / shortinterest3 翻案批已回收：维持判死，例外失效
ds['option8']['status'] = 'dead'
ds['option8']['retrial'] = '翻案批已回收（ts_target_tvr_decay/残差差分/vec_max 三武器实测）：tvr_decay 压换手但 sharpe 差 0.05 且 subU 0.24 仍 fail；残差差分全无效 → 例外失效，永久封存'
ds['shortinterest3']['status'] = 'dead'
ds['shortinterest3']['retrial'] = '翻案批已回收：vec_max/vec_avg tvr_decay 1.13-1.18 不足 + subU 0.2-0.28 fail → 例外失效，永久封存'

# 波10 主攻
d['wave10_primary'] = 'institutions6（机构持股/资金流风格，21字段登记，WW/XX 在飞）'

# 判死汇总
d['dead_summary'] = {
    'sentiment_pyramid': ['sentiment21', 'news_transformer_scores', 'sentiment22'],
    'option_pyramid': ['option8', 'option40'],
    'shortinterest': ['shortinterest3'],
    'analyst': ['analyst44'],
    'submission_candidates': 0
}

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('ledger.json updated')
print('dead_summary:', d['dead_summary'])
