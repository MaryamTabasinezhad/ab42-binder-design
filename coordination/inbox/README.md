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

## Polling

During active sessions, agents should periodically `git pull` and check their inbox:
```bash
git pull --quiet origin master
ls coordination/inbox/<your-cluster>/
```

Claude Code agents can use `/loop` to automate this check every few minutes.
