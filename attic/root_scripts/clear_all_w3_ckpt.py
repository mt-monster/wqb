import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

# 删除所有 wave 3 相关的 checkpoint
keys_to_delete = [
    'ckpt_w3',
    'gate_w3_option_chart_model',
    'gate_w3_ai_news_scores'
]

for key in keys_to_delete:
    cursor.execute("DELETE FROM ledger_kv WHERE region='USA' AND key=?", (key,))
    print(f'删除 {key}: {cursor.rowcount} 行')

conn.commit()
conn.close()
