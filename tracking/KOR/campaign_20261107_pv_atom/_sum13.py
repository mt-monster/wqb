import json,re,collections
raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_intraday.json", encoding="utf-8-sig").read()
intr = json.loads(raw[raw.find("{"):])["results"]
ids = [x["id"] for x in intr]
for t in ("corr_bid_price_with_volume","corr_ask_price_with_slippage","corr_bid_price_with_slippage","corr_last_trade_price_with_volume","corr_vwap"):
    sel = [i for i in ids if t in i]
    print(t, "->", sel[:5])
print()
raw2 = open("tracking/KOR/campaign_20261107_pv_atom/_df_mfrp.json", encoding="utf-8-sig").read()
mf = json.loads(raw2[raw2.find("{"):])["results"]
mids = [x["id"] for x in mf]
suf = collections.defaultdict(set)
for i in mids:
    m = re.match(r"^(long|short)(_.*)$", i)
    if m: suf[m.group(2)].add(m.group(1))
both = [k for k,v in suf.items() if len(v)==2]
print("PAIRED long/short suffixes:", len(both))
for k in sorted(both)[:40]: print("   long"+k, "| short"+k)