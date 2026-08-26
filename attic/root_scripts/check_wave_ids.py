import sqlite3

conn = sqlite3.connect('data/wqb.db')
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT wave, wave_id FROM expressions WHERE region='USA' ORDER BY wave")
results = cursor.fetchall()

print("现有 wave 和 wave_id 对应关系:")
for row in results:
    print(f"  wave={row[0]}, wave_id={row[1]}")

conn.close()
