#!/bin/bash
# /home/elliot/code/bart-clock/run_with_protection.sh
MAX_RESTARTS=3
RESTART_WINDOW=300  # 5 minutes
LOCKFILE="/tmp/display_service.lock"
RESTART_COUNT_FILE="/tmp/display_restart_count"
LOG_FILE="/var/log/display_service.log"

# Rotate logs if they get too big (1MB)
if [ -f "$LOG_FILE" ] && [ $(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE") -gt 1048576 ]; then
    mv "$LOG_FILE" "$LOG_FILE.old"
fi

# Initialize or read restart count
if [ ! -f "$RESTART_COUNT_FILE" ]; then
    echo "0 $(date +%s)" > "$RESTART_COUNT_FILE"
fi

read count timestamp < "$RESTART_COUNT_FILE"
now=$(date +%s)

# Reset counter if outside window
if [ $((now - timestamp)) -gt $RESTART_WINDOW ]; then
    count=0
fi

# Check if we've exceeded restart limit
if [ $count -ge $MAX_RESTARTS ]; then
    echo "Too many restarts in time window. Waiting for manual intervention." >> "$LOG_FILE"
    exit 1
fi

# Update restart count
count=$((count + 1))
echo "$count $now" > "$RESTART_COUNT_FILE"

# Run the actual script
python3 /home/elliot/code/bart-clock/main.py 2>&1 | tee -a "$LOG_FILE"
