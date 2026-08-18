import os
"""Full picture: details + self-corr of the 4 OS alphas, plus re-confirm vRvg7NzA/MPQVZRnk."""
import sys, json
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session, get_simulation_result_json, get_self_corr

s = start_session()
BASE = "https://api.worldquantbrain.com"

OS = ["KPGvRMg1", "6XpMb0aG", "gJ8eVmNM", "QPGvgO2G"]
CHECK = ["vRvg7NzA", "MPQVZRnk"] + OS

info = {}
for aid in CHECK:
    j = get_simulation_result_json(s, aid)
    if not j:
        print(f"{aid}: NOT FOUND / not owned"); continue
    st = j.get("settings", {})
    _r = j.get("regular") or j.get("combo") or ""
    expr = (str(_r).replace("\n"," "))[:90]
    info[aid] = {
        "stage": j.get("stage"),
        "region": st.get("region"), "uni": st.get("universe"),
        "sharpe": (j.get("is") or {}).get("sharpe"),
        "fitness": (j.get("is") or {}).get("fitness"),
        "expr": expr,
    }
    print(f"\n{aid}: stage={j.get('stage')} {st.get('region')}/{st.get('universe')} sharpe={info[aid]['sharpe']} fit={info[aid]['fitness']}")
    print(f"   expr: {expr}")

# self-correlation (collision with submitted alphas) for each OS alpha
print("\n=== SELF_CORRELATION among OS alphas ===")
for aid in OS:
    try:
        df = get_self_corr(s, aid)
        if df is not None and len(df):
            # show rows where correlation is notable
            print(f"\n{aid} self-corr:")
            print(df.to_string()[:1500])
    except Exception as e:
        print(f"{aid} self_corr err: {e}")
