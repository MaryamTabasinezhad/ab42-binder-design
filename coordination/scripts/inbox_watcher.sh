#!/bin/bash
# Inbox watcher — polls git for new messages in coordination/inbox/<cluster>/
# Run in background: nohup bash coordination/scripts/inbox_watcher.sh &
# Or in a tmux/screen session. Kill with: kill $(cat /tmp/inbox_watcher_${CLUSTER}.pid)

set -euo pipefail

INTERVAL="${INBOX_POLL_INTERVAL:-120}"  # seconds between checks, default 2 min

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

case "$(hostname -f)" in
  *frontenac*|frnt*) CLUSTER="frontenac" ;;
  *nibi*)            CLUSTER="nibi" ;;
  *narval*)          CLUSTER="narval" ;;
  *)
    echo "Unknown cluster: $(hostname -f)" >&2
    exit 1
    ;;
esac

INBOX_DIR="${REPO_ROOT}/coordination/inbox/${CLUSTER}"
LOG="${REPO_ROOT}/coordination/inbox/${CLUSTER}/.watcher.log"
PIDFILE="/tmp/inbox_watcher_${CLUSTER}.pid"

if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "Watcher already running (PID $(cat "$PIDFILE")). Kill it first or remove $PIDFILE."
  exit 1
fi

echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT

mkdir -p "$INBOX_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"
}

log "Inbox watcher started for ${CLUSTER} (PID $$, interval ${INTERVAL}s)"
log "Watching: ${INBOX_DIR}"

SEEN_FILES=""

while true; do
  # Pull latest (quiet, tolerate failures — network blips shouldn't kill the watcher)
  cd "$REPO_ROOT"
  if git pull --quiet origin master 2>/dev/null; then
    :
  else
    log "WARN: git pull failed (will retry next cycle)"
  fi

  # Check for .md files in inbox (exclude README.md and dotfiles)
  NEW_COUNT=0
  for f in "${INBOX_DIR}"/*.md; do
    [[ -f "$f" ]] || continue
    fname="$(basename "$f")"
    [[ "$fname" == "README.md" ]] && continue

    # Skip if already seen
    if echo "$SEEN_FILES" | grep -qF "$fname"; then
      continue
    fi

    NEW_COUNT=$((NEW_COUNT + 1))
    log "NEW MESSAGE: $fname"
    log "--- begin ---"
    head -20 "$f" | while IFS= read -r line; do log "  $line"; done
    log "--- end (first 20 lines) ---"
    SEEN_FILES="${SEEN_FILES}${fname}"$'\n'
  done

  if [[ $NEW_COUNT -gt 0 ]]; then
    log ">>> ${NEW_COUNT} new message(s) in inbox. Read and act on them next session."
  fi

  sleep "$INTERVAL"
done
