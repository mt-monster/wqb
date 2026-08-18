import json, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

lines = open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\conversation-history\task-a60\task-a60.jsonl', encoding='utf-8').read().splitlines()

for i, ln in enumerate(lines, 1):
    try:
        obj = json.loads(ln)
    except Exception:
        continue
    content = obj.get('message', {}).get('content', '')
    if isinstance(content, list):
        text = ' '.join(c.get('text', '') for c in content if isinstance(c, dict))
    else:
        text = str(content)
    if 'probe-score' in text or 'mark-dead' in text or 'probe_score' in text:
        hits = re.findall(r'.{120}(probe-score|mark-dead).{200}', text)
        for h in hits[:10]:
            print(f'--- line {i} [{obj.get("role")}] ---')
            print(h.replace('\\n', ' | ')[:400])
            print()
