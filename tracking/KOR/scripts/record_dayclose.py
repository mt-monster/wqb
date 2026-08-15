import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['lesson_multisim_cancelled'] = {
    'pattern': '连续三批(P9/P9-v2/P9-v3)8/8全CANCELLED，P9批内含重复式、后两批8式全互异仍取消→批内重复假设被推翻',
    'root_cause': '大概率平台每日模拟配额耗尽(本夜已跑30+批×8式≈240+模拟)。平台对超限模拟直接CANCELLED且无错误信息',
    'rule': [
        '整夜战役需预估配额: 每批8式, 控制总批数≤15-20, 优先攻坚已近门槛的骨架而非开新数据集',
        '遇连续CANCELLED立即停手不再重提, 等配额重置(ET零点)后优先跑已备好的CW攻击批',
        'create_multi_simulation批内8式必须互不相同(重复浪费槽位)',
    ],
}

d['wave22P9v3_verdict'] = {
    'multisim': '4g4QZC8UR5dTbCKfLKBVEjD',
    'result': 'CANCELLED(配额耗尽)',
    'ready_to_rerun': {
        'design': 'CW手册指导8式全互异',
        'expressions': [
            'ts_decay_linear60全腿平滑',
            'group_rank(sector)摊权',
            'signed_power0.7压尾',
            '6腿扩散(spreadbp+slippage44+tcm44)',
            'ts_mean10平滑EM腿',
            '基础式对照(=KPGZmLMl sh2.03)',
            '跨Category PV腿0.15 ts_rank(close,90)★手册类型三终极解★',
            'ts_weighted_delay2防跳变',
        ],
        'settings': 'SECTOR decay6 t0.08 KOR TOP600 D1 max_trade=ON',
    },
}

d['campaign_status_20260815_day'] = {
    'submit_ready_count': 0,
    'nearest_candidate': 'KPGZmLMl model170四腿: sh2.03/fit1.52/2y2.09/mg11.3bp/tvr26.1%/rn1.70/PROD0.601(三腿版已过) 仅剩CW',
    'blocked_by': 'CW结构墙(待P9-v3批验证手册解法) + 平台日模拟配额耗尽',
    'next_session_plan': [
        '1.配额重置后重提P9-v3八式(重点看跨Category PV腿)',
        '2.若CW仍败: 按手册第一步查model170在KOR覆盖率,<40%则放弃model170转新数据集',
        '3.查KOR覆盖率≥40%+alphaCount≤50的蓝海数据集重开战线(P2骨架多样化)',
        '4.KPGvRMg1已在48h配额内占用1提交位(剩余3), 提交前需用户确认',
    ],
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
