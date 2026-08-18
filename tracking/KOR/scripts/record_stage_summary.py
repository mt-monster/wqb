import sys
sys.path.insert(0, r'C:\Users\MENGTAO\.workbuddy\skills\wq-brain-campaign-toolkit\scripts')
from _lib.ledger import LedgerStore

store = LedgerStore(r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json')

def mutate(d):
    d['stage_summary_20260816'] = {
        'report': 'tracking/KOR/KOR_D1_STAGE_SUMMARY_20260816.md',
        'progress': '1/3 (WjAxxZVk ACTIVE)',
        'dl_riskfree': '20+冠军候选池封存 PROD墙0.82-0.92结构性 三维穷尽',
        'best': 'O0Gj6PqJ sh2.83/fit3.39 PROD0.8211族史最低',
        'next': ['other455侦察', 'insider_feats复攻', 'ai_equity_alpha二轮'],
        'lessons': ['字段后缀不对称需实测核对', 'CANCELLED先疑连坐用lookINTO下钻',
                    'PROD墙薄(>0.7<=20/7.9万)判结构性早撤', '工具层400/429/401降级是基建'],
        'recorded_at': '2026-08-16'
    }
    return d

store.update(mutate)
print('keys=', len(store.load()))
