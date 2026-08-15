#!/bin/bash
CSV="C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/outputs/simulation_status_usa_d1_sentiment_v3.csv"
SIM_PID=34472
TOTAL=11
LOG="D:/coding/traeCN_project/wqb/sim_v3_poll.log"
echo "v3 poll start $(date) target=$TOTAL pid=$SIM_PID" > "$LOG"
for i in $(seq 1 140); do
  if [ -f "$CSV" ]; then done=$(tail -n +2 "$CSV" 2>/dev/null | grep -c "COMPLETE"); else done=0; fi
  alive=$(powershell.exe -NoProfile -Command "(Get-Process -Id $SIM_PID -ErrorAction SilentlyContinue).HasExited" 2>/dev/null)
  echo "$(date +%H:%M:%S) complete=$done/$TOTAL sim_exited=$alive" >> "$LOG"
  if [ "$done" -ge "$TOTAL" ]; then echo "ALL_DONE" >> "$LOG"; break; fi
  if [ "$alive" = "True" ]; then echo "SIM_EXITED_PARTIAL done=$done" >> "$LOG"; break; fi
  sleep 60
done
echo "=== FINAL V3 CSV ===" >> "$LOG"
cat "$CSV" >> "$LOG" 2>/dev/null
echo "v3 poll end $(date)" >> "$LOG"
