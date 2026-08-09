# -*- coding: utf-8 -*-
"""stage1 续跑启动器: 复用 stage1_first_order.pkl(150 候选),
直接喂给 multi_simulate_with_summary, 由函数内部按 blocked_fields +
已模拟 expression 幂等跳过, 只跑剩余候选。
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pickle
import glb_pipeline as gp

CACHE = gp.CACHE
fo = pickle.load(open(os.path.join(CACHE, "stage1_first_order.pkl"), "rb"))
print(f"[resume] loaded {len(fo)} first-order candidates from pkl", flush=True)
print(f"[resume] REGION={gp.REGION} UNIVERSE={gp.UNIVERSE} NEUT={gp.NEUT}", flush=True)
gp.multi_simulate_with_summary(fo, "glb_first", summary_every=10)
print("\n=== stage1 resume finished ===", flush=True)
