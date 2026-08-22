# -*- coding: utf-8 -*-
"""分析 model219 字段族分布 + 选候选字段"""
import json, re, collections

# 从 scan_fields 输出提取 JSON 部分
raw = open(r"C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4dc\e74b0ec1.txt", encoding="utf-8", errors="replace").read()
# 找到第一个 { 到最后 }
start = raw.find("{")
end = raw.rfind("}")
d = json.loads(raw[start:end + 1])
fields = d["fields"]
print("total fields:", len(fields))

names = [f["id"] for f in fields]
print("\n=== 命名前缀分布 ===")
prefixes = collections.Counter()
for n in names:
    if "_q_dlr_" in n:
        prefixes[n.split("_q_dlr_")[0] + " (q_dlr)"] += 1
    elif n.startswith("mdl219_"):
        parts = n.split("_")
        prefixes["mdl219_" + parts[1]] += 1
    else:
        prefixes["OTHER"] += 1
for p, c in prefixes.most_common(15):
    print(f"  {p}: {c}")

# 列出 0 竞争且 cov>=0.85 的字段, 按后缀语义分组
print("\n=== 零竞争高覆盖字段 (userCount==0, cov>=0.90) 抽样 ===")
zero = [f for f in fields if f["userCount"] == 0 and f["coverage"] >= 0.90]
print("count:", len(zero))
# 提取常见后缀
suffixes = collections.Counter()
for f in zero:
    m = re.search(r"_(\w+)$", f["id"])
    if m:
        suffixes[m.group(1)] += 1
for s, c in suffixes.most_common(30):
    print(f"  suffix _{s}: {c}")

# 输出全部零竞争字段名到文件
with open(r"d:\coding\traeCN_project\wqb\tracking\KOR\cache\model219_zero_comp_fields.json", "w", encoding="utf-8") as fo:
    json.dump([{"id": f["id"], "cov": f["coverage"]} for f in zero], fo, ensure_ascii=False, indent=0)
print("\nzero-comp fields -> cache/model219_zero_comp_fields.json")
