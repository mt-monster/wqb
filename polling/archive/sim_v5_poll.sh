#!/usr/bin/env bash
CSV="C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/outputs/simulation_status_usa_d1_sentiment_v5.csv"
LOG="D:/coding/traeCN_project/wqb/sim_v5_poll.log"
TARGET=6
PY="D:/coding/traeCN_project/wqb/world-quant-brain-mcp/.venv/Scripts/python.exe"
while true; do
  if [ ! -f "$CSV" ]; then echo "$(date) waiting csv"; sleep 30; continue; fi
  DONE=$("$PY" -c "
import csv,sys
try:
    rows=list(csv.DictReader(open(r'$CSV')))
except: print(0); sys.exit()
print(sum(1 for r in rows if str(r.get('status','')).upper() in ('COMPLETED','COMPLETE')))
")
  NOW=$(date)
  echo "$NOW complete=$DONE/$TARGET"
  if [ "$DONE" -ge "$TARGET" ]; then
    echo "$NOW ALL DONE - exit"
    break
  fi
  sleep 60
done
