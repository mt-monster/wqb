import sys
sys.path.insert(0, r'C:\Users\MENGTAO\.workbuddy\skills\wq-brain-campaign-toolkit\scripts')
from _lib.ledger import LedgerStore

store = LedgerStore(r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json')

def mutate(d):
    d['wave36_turn_summary'] = {
        'wins': [
            'SUBINDUSTRY杠杆首启即出全门槛过88pZW2Vo(sh2.59/2y2.27/ra=0)',
            'XgoxdaxX SLOW_AND_FAST全门槛过(2y压线1.60)',
            '僵尸进程根因破解+限流真因定位(data-fields端点桶限流)',
            'KOR universe仅TOP600平台事实实证',
        ],
        'losses': [
            '两候选PROD全撞墙(0.8213/0.8783)',
            'STATISTICAL轨2y崩(1.39/0.98 RA失败)',
            '白名单扫描被端点限流拦截',
        ],
        'blocked': [
            'other455白名单(data-fields端点限流, WebDataScope本地无此集)',
            'ai_equity_alpha二轮/insider_feats复攻待窗口',
        ],
        'progress': '1/3不变; dl_riskfree终判信号级结构墙封存; 下一战线=other455(需限流恢复)',
        'recorded_at': '2026-08-16',
    }
    return d

store.update(mutate)
print('keys=', len(store.load()))
