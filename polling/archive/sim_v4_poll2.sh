#!/usr/bin/env bash
CSV="C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/outputs/simulation_status_usa_d1_sentiment_v4.csv"
LOG="D:/coding/traeCN_project/wqb/sim_v4_poll2.log"
PY="D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe"
echo "v4 poll2 start $(date) target=8 csv=$CSV" > "$LOG"
for i in $(seq 1 40); do
  if [ -f "$CSV" ]; then
    done=$( "$PY" -c "
import csv,sys
try:
    rows=list(csv.DictReader(open('$CSV')))
except Exception:
    print(0); sys.exit()
c=sum(1 for r in rows if str(r.get('status','')).upper() in ('COMPLETED','COMPLETE'))
print(c)
" 2>/dev/null )
  else
    done=0
  fi
  echo "$(date) complete=$done/8 iter=$i" >> "$LOG"
  if [ "${done:-0}" -ge 8 ]; then
    echo "DONE complete=$done" >> "$LOG"
    break
  fi
  sleep 45
done
echo "poll2 end $(date)" >> "$LOG"
