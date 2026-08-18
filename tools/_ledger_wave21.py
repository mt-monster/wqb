import json, sys
sys.path.insert(0, r"C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts")
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _lib.ledger import LedgerStore

store = LedgerStore(r"D:\coding\traeCN_project\wqb\tracking\GBR\gbr_d1_campaign_state.json")

def mut(d):
    ws = d.setdefault("waves", {})
    if "21" not in ws:
        ws["21"] = {
            "dataset": "shortinterest3",
            "note": ("24/24 backtested; securities-lending activity weak in GBR D1 "
                     "(best sh0.53 all LOW_SHARPE); one wave and rotate, dead-ish"),
            "at": "2026-08-18T02:00:00",
        }
    verdict = json.load(open(
        r"D:\coding\traeCN_project\wqb\tracking\GBR\reviews\wave21_verdict.json",
        encoding="utf-8"))
    verdict.setdefault("recorded_at", "2026-08-18")
    d["wave21_verdict"] = verdict

store.update(mut)
print("ledger OK; waves keys:", sorted(store.load().get("waves", {}).keys()))
