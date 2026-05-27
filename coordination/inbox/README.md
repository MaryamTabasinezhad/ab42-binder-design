# Agent Inbox System

Inter-agent messaging via git. Each agent has an inbox directory.

## How it works

1. To send a message to Frontenac: write a `.md` file in `inbox/frontenac/`
2. Commit and push with `[<your-cluster>] msg: <subject>`
3. The recipient does `git pull` and checks their inbox
4. After reading, the recipient deletes the message file and commits

## Message format

Filename: `YYYY-MM-DD_from-<sender>_<subject>.md`

Content:
```markdown
**From:** <sender cluster>
**Date:** YYYY-MM-DD HH:MM
**Subject:** <one-line summary>

<message body>
```

## Examples

Narval reporting a blocker:
```
inbox/frontenac/2026-05-27_from-narval_colabfold-oom.md
```

Frontenac assigning new work:
```
inbox/narval/2026-05-27_from-frontenac_run-extra-designs.md
```

## Automated Watcher

Run the inbox watcher in the background to get notified of new messages:
```bash
# Start (from repo root):
nohup bash coordination/scripts/inbox_watcher.sh &

# Check status:
cat /tmp/inbox_watcher_$(hostname -f | grep -oP 'frontenac|nibi|narval').pid

# Stop:
kill $(cat /tmp/inbox_watcher_<cluster>.pid)

# Adjust poll interval (default 120s):
INBOX_POLL_INTERVAL=60 nohup bash coordination/scripts/inbox_watcher.sh &
```

The watcher does `git pull` every cycle, detects new `.md` files in your inbox,
and logs the first 20 lines to `coordination/inbox/<cluster>/.watcher.log`.

## Manual Polling

During active sessions, agents can also manually check:
```bash
git pull --quiet origin master
ls coordination/inbox/<your-cluster>/
```

Claude Code agents can use `/loop` to automate this check every few minutes.
