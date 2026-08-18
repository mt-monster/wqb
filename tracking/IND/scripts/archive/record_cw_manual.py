import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['forum_cw_manual'] = {
    'source': '论坛帖40972941718807 LC97552《CONCENTRATED WEIGHT 系统性排查与修复手册-1》63票29评',
    'core': 'CW是数据品质问题不是参数问题。truncation/decay/neutralization修不了CW',
    'diagnosis_flow': [
        '第一步查数据集覆盖率: <40%直接换数据集(ROI最高)',
        '第二步查数据类型: VECTOR->vec_avg转标量+ts_backfill; 事件型(earnings/consensus)->跨Category rank加法; 时序型->查窗口长度(拉长2-5天)',
        '第三步仍FAIL->ts_backfill最小窗口从1-5天起试',
    ],
    'key_techniques': [
        '跨Category rank加法(事件型CW终极解): add(rank(event_field),rank(ts_rank(close,90))) FAIL->PASS且恢复IS_LADDER; 2y从0.09到3.11案例',
        '蓝海字段userCount=0是CW免费通行证',
        'ts_backfill(x,d) d=2~40(基本面60); 但VECTOR禁包ts_backfill(本战役事故记录,需先vec_avg)',
        'group_count(is_nan(a),market)>N ? a : nan 检测缺失骤降时期',
        'ts_decay_exp_window/exp_window/ts_weighted_delay(days_from_last_change/keep)平滑降噪',
        'trade_when(x,y,z)条件更新降换手',
        '新兴市场噪声填充法: group_extra+0.0001*group_rank(-returns,industry) filter=true',
        'ts_backfill(ts_rank(field,5),3)小市值市场组合(SY90356评论)',
    ],
    'mapping_to_model170': 'model170字段是VECTOR+季度更新事件型->符合类型三结构性CW模式。P8稀释腿提权无效已证伪参数方向; P9-v2已按手册加入跨Category PV腿(0.15权重 ts_rank(close,90))验证',
    'retrieved_at': '2026-08-15',
}

d['wave22P9_status'] = {
    'p9_first': {'multisim': '4D2MBXbRP4wCbo4To4MZbJx', 'result': '8/8 CANCELLED(平台侧取消,语法本地验证全过)', 'lesson': 'CANCELLED非表达式问题,直接重提'},
    'p9_v2': {'multisim': '32urMtfx053099CUVfhRQzs', 'design': 'CW手册指导8变体: ts_decay_linear60/group_rank(sector)/signed_power0.7/6腿扩散/ts_mean10平滑/基础式对照/跨Category PV腿0.15/基础式对照2', 'status': '在飞待轮询'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
