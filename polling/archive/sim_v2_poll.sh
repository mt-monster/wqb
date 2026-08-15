#!/bin/bash
CSV="C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/outputs/simulation_status_usa_d1_sentiment_v2.csv"
SIM_PID=1160
TOTAL=10
LOG="D:/coding/traeCN_project/wqb/sim_v2_poll.log"
echo "v2 poll start $(date) target=$TOTAL pid=$SIM_PID" > "$LOG"
for i in $(seq 1 120); do
  if [ -f "$CSV" ]; then
    done=$(tail -n +2 "$CSV" 2>/dev/null | grep -c "COMPLETE")
  else
    done=0
  fi
  alive=$(powershell.exe -NoProfile -Command "(Get-Process -Id $SIM_PID -ErrorAction SilentlyContinue).HasExited" 2>/dev/null)
  echo "$(date +%H:%M:%S) complete=$done/$TOTAL sim_exited=$alive" >> "$LOG"
  if [ "$done" -ge "$TOTAL" ]; then echo "ALL_DONE" >> "$LOG"; break; fi
  if [ "$alive" = "True" ]; then echo "SIM_EXITED_PARTIAL done=$done" >> "$LOG"; break; fi
  sleep 60
done
echo "=== FINAL V2 CSV ===" >> "$LOG"
cat "$CSV" >> "$LOG" 2>/dev/null
echo "v2 poll end $(date)" >> "$LOG"
