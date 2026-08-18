# -*- coding: utf-8 -*-
"""波11 探针台账更新：AA~AF 六批 48 条结论 + ★双数据集混合策略（用户授权）+ AG 批在途。"""
import json

LEDGER_MD = r'd:\coding\traeCN_project\wqb\tracking\USA\WAVE_LEDGER.md'
LEDGER_JSON = r'd:\coding\traeCN_project\wqb\tracking\USA\ledger.json'

WAVE11_SECTION = """
---

## 波11（2026-08-16）— order_book_imbalance 探针（AA~AF 六批 48 条回收，AG 混合批在途）

### 批次与结论
| 批 | multisim | 内容 | 结论 |
|---|---|---|---|
| AA | 4pwNeBd3o50N8NE5zZF7Bmt | imbalance 占比/auction/spread 族探针 | 全灭：占比族 |sharpe|≤0.7 且 tv 35-62% 超高；spread 负向 -0.61（流动性溢价方向）；executed 占比 RN 1.03 但 IS 0.15 |
| AB | tN7zj3pP5bNamIxi0o0123 | 慢变字段族（twa 深度/fill_prob/rest_time/dark-lit/impact/spread ts_mean5） | **dark/lit 暗池占比发现 0mpZQ0A6：0.51/RN 1.44/RN fit 0.68/tv 11.7%/2y -0.59**；fill_prob 族 RN 1.17-1.18 但 2y -1.21 负；market impact 单独 0.24 |
| AC | 4uiSlDcoH4my9aYaiTKsD2J | market impact 精调（原始/ts_decay4/16/reverse/减 spread/加权/乘 spread） | **impact−mean_relative_spread 净效应 VkGQl72G：0.60/tv 5.8%/RN 0.64 为波11 单信号最强**；children 核对修正认知（0mpZQ0A6 实为 dark/lit，非 impact） |
| AD | 2dT7dn3u04V2bt4ymZHQwqv | dark/lit 精调（ts_decay4/16/reverse/count/notional 口径/nonaddressable）+ impact/spread 变体 | 全灭：**dark/lit 族天花板 0.51 确认**（decay4/16 降至 0.43-0.48，count 口径 -0.66 反向、notional -0.40 弱，仅 volume 口径有效）；impact−time_weighted_spread 0.18 弱；impact/spread 比值 0.57 未超差值 |
| AE | 4GB7Nddfu4vxa7m81oG5V3D | 双亮点复合（add/multiply）+ 未测字段族（auction dislocation/intraday vol/VWAP spread/修改强度） | **复合正反馈首次出现：dark/lit × (impact−spread) 乘法 0.66/RN 1.29/tv 8.6%（波11 新高）**，加法 0.63；其余字段族全灭（auction dislocation -0.57、vol -0.01、VWAP spread 0.10） |
| AF | 2lXu7g47G4VGaYFdGcYKfyU | 三重复合（×fill_prob/×executed）+ 权重变体（2×impact−spread）+ 差异信号 + spread 动量 | 已提交待回收（本次会话提交后轮询被中断，需补回收） |

### ★双数据集混合策略（用户 2026-08-16 授权，流程已融合）
1. **动机**：analyst44 判死时"earnings yield 需价格字段破坏单数据集纪律"被放弃（波9 天花板 0.45 差 3.5 倍）；波11 微结构亮点（dark/lit 0.51、impact−spread 0.60）与基本面风格正交 → 用户授权允许混入两个数据集字段构造经济学意义 alpha
2. **规则**：① 上限 2 个数据集（expr_lint.py 已加双数据集门控：字段→数据集归属追踪，>2 拦截，恰好 2 个标 [MIX]）；② 经济学意义优先（知情交易确认/估值×流动性/信息×微结构）；③ 混合批命名规范 `usa_<ds1>_<ds2>_batch_<tag>.txt`；④ 单数据集纪律仍为默认，混合为显式授权扩展；⑤ 已判死数据集可作混合成分（judged dead 指单数据集信号不足，非字段无信息）
3. **AG 批首发**（3aXpmIbcV54q9DtrmdLazRO，decay8/SUBIND，在途）：EPS 63d/126d 共识修正 × dark/lit 暗池占比、earnings yield（EPS/close）× dark/lit / × (impact−spread)、EBITDA/nxt_yr 修正 × dark/lit、EPS 修正 + dark/lit 加法复合

### 波11 阶段结论与下一步
- 微结构信号共性：sharpe 天花板由日内订单流信息含量决定（单信号 0.24-0.60），复合可放大至 0.66 但仍距闸门 1.58 差 2.4 倍；tv 结构尚可（复合后 8.6% 在 5-30% 区间）
- 下一步：① 回收 AF + AG 批（混合路径首验）；② 若混合有效（>0.8 方向）→ 混合矩阵扩展（decay 阶梯/中性化/更多信息×微结构组合）；③ 若无效 → 波11 判死评估（模板多样性已 6 批 56 条 + 双数据集混合首验），执行 Round20 多样性评估 + canvas 落地报告
- 提交前置不变：数值七闸门 → PROD<0.7 → robust/过拟合
"""

def update_md():
    with open(LEDGER_MD, encoding='utf-8') as f:
        md = f.read()
    if '## 波11（2026-08-16）— order_book_imbalance 探针' in md:
        # 已存在则替换旧波11 节（保留其后评估章节）
        start = md.index('## 波11（2026-08-16）— order_book_imbalance 探针')
        end = md.index('## 每 10 波全量多样性评估', start)
        md = md[:start] + WAVE11_SECTION.strip() + '\n\n' + md[end:]
    else:
        # 追加到多样性评估章节之前
        marker = '## 每 10 波全量多样性评估'
        idx = md.index(marker)
        md = md[:idx] + WAVE11_SECTION.strip() + '\n\n' + md[idx:]
    with open(LEDGER_MD, 'w', encoding='utf-8') as f:
        f.write(md)
    print('[MD] 波11 章节已更新')

def update_json():
    with open(LEDGER_JSON, encoding='utf-8') as f:
        d = json.load(f)
    d['wave_in_progress'] = '波11: order_book_imbalance 探针（AA~AF 六批 48 条回收，AG 双数据集混合批在途）'
    d['backtests_total'] = '波1-9: 352 条 + 波10 已回收 96 条（WW~T2 含重复 8 条）+ 波11 已回收 48 条（AA~AF）+ AG 在途 8 条 = 504 条'
    d['mix_strategy'] = {
        'authorized': '2026-08-16 用户授权',
        'max_datasets': 2,
        'gate': 'expr_lint.py 双数据集门控（字段→数据集归属，>2 拦截，==2 标 [MIX]）',
        'naming': 'usa_<ds1>_<ds2>_batch_<tag>.txt',
        'rationale': '经济学意义优先：知情交易确认 / 估值×流动性 / 信息×微结构；已判死数据集可作混合成分',
        'first_batch': 'AG: order_book_imbalance × analyst44（3aXpmIbcV54q9DtrmdLazRO，decay8/SUBIND，在途）'
    }
    d['pending']['in_flight'] = ['AG 双数据集混合批 3aXpmIbcV54q9DtrmdLazRO（obim×anl44，8 条，decay8/SUBIND）']
    d['updated'] = '2026-08-16'
    with open(LEDGER_JSON, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print('[JSON] ledger.json 已更新')

if __name__ == '__main__':
    update_md()
    update_json()
    print('DONE')
