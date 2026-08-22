# -*- coding: utf-8 -*-
"""提取 continuation_score 完整字段清单 + 分类"""
import json, re, collections

raw = open(r"C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4dc\228da027.txt", encoding="utf-8", errors="replace").read()
# 输出文件含截断占位符, 直接从 reference 白名单/catalog 找
# 先尝试 kor_continuation_score_field_whitelist.json
import os
base = r"d:\coding\traeCN_project\wqb\tracking\KOR\reference"
wl = os.path.join(base, "kor_continuation_score_field_whitelist.json")
cat = os.path.join(base, "kor_continuation_score_field_catalog.json")
print("whitelist exists:", os.path.exists(wl), "| catalog exists:", os.path.exists(cat))
for p in [wl, cat]:
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        if "verified_fields" in d:
            fs = list(d["verified_fields"].keys())
            print(f"\n{p}: {len(fs)} verified fields")
            print(fs)
        elif "fields" in d:
            fs = d["fields"]
            print(f"\n{p}: {len(fs)} fields")
            print([f if isinstance(f, str) else f.get("id") for f in fs][:60])
