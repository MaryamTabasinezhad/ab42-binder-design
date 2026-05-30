# Multi-Agent Claude Code Coordination on HPC Clusters

> A complete, honest guide to running multiple Claude Code agents across SLURM-managed HPC clusters, coordinated via a shared git repo. Written from the Aβ42 × TfR1 bispecific binder design project (2026-05-26 to 2026-05-29), which ran 3 agents across Frontenac, Nibi, and Narval clusters.

---

## 1. The core idea

Each HPC cluster gets its own Claude Code session. The sessions cannot talk to each other directly — there is no shared memory, no API, no socket. Instead, they communicate through a **shared git repository** on GitHub. The repo is the single source of truth. Every instruction, status update, and result flows through git commits.

One agent is the **coordinator** (makes decisions, assigns work). The others are **workers** (execute assigned tasks, report results). The coordinator role is defined in the repo's CLAUDE.md, not in Claude Code itself.

**What works well:**
- Asynchronous coordination across clusters with different schedules, queues, and hardware
- Full audit trail — every decision, message, and result is a git commit
- No special infrastructure — just git, GitHub, and the SLURM clusters you already have
- Agents on different clusters genuinely work in parallel on different GPUs

**What doesn't work well:**
- Real-time communication is impossible. An agent only sees new messages after `git pull`, which happens at session start. There is no push notification.
- Merge conflicts happen when two agents push at the same time. They are always resolvable (each agent edits different sections), but they require manual `git pull --no-rebase` and conflict resolution.
- An agent cannot "wake up" another agent. You (the user) must start each session manually on each cluster.
- The inbox system is glorified file-dropping — there is no delivery confirmation, no read receipts, no threading.

---

## 2. Repository structure

```
your-project/
├── CLAUDE.md                          # Root instructions — cluster detection, protocols
├── clusters/
│   ├── README.md                      # How to add a new cluster
│   ├── frontenac.env                  # Shell-sourceable env vars (paths, SLURM, Globus)
│   ├── narval.env
│   ├── nibi.env
│   ├── frontenac/CLAUDE.md            # Coordinator-specific instructions
│   ├── narval/CLAUDE.md               # Worker-specific instructions
│   └── nibi/CLAUDE.md                 # Worker-specific instructions
├── coordination/
│   ├── COORDINATION.md                # Campaign parameters, agent registry, rules
│   ├── DASHBOARD.md                   # Live status — updated by every agent every session
│   ├── inbox/
│   │   ├── README.md                  # Inbox protocol docs
│   │   ├── frontenac/.gitkeep         # Coordinator's inbox
│   │   ├── narval/.gitkeep            # Worker inbox
│   │   └── nibi/.gitkeep             # Worker inbox
│   ├── manifests/
│   │   ├── README.md                  # Manifest format docs
│   │   └── manifest_<stage>_<cluster>.tsv
│   ├── globus/
│   │   ├── endpoints.md               # Globus endpoint IDs per cluster
│   │   └── transfer_recipes.sh        # Reusable Globus transfer commands
│   └── scripts/
│       └── inbox_watcher.sh           # Background poller (optional)
└── <your-project-dirs>/               # Actual science/code
```

---

## 3. Setting it up from scratch

### 3.1. Create the GitHub repo

```bash
# On your coordinator cluster
mkdir my-project && cd my-project
git init
git remote add origin git@github.com:<your-org>/<your-repo>.git
```

### 3.2. Write the root CLAUDE.md

This is the most important file. Every Claude Code session reads it automatically. It must:
1. Tell the agent which cluster it's on (hostname detection)
2. Tell it what to read at session start
3. Tell it how to communicate

Here is the exact template (adapt the hostname patterns and cluster names):

```markdown
# CLAUDE.md

## What this repo is
<One paragraph describing your project. Be specific about what kind of work
the agents will do — SLURM jobs, analysis scripts, data processing, etc.>

## Multi-Cluster Coordination Protocol

### Your identity
Detect your cluster from hostname and read the matching CLAUDE.md:
- `*frontenac*` or `frnt*` → **Frontenac (Coordinator)** — read `clusters/frontenac/CLAUDE.md`
- `*nibi*` → **Nibi (Worker)** — read `clusters/nibi/CLAUDE.md`
- `*narval*` → **Narval (Worker)** — read `clusters/narval/CLAUDE.md`

Source cluster-specific paths and SLURM settings from `clusters/<cluster>.env`.

### Session start protocol (ALL CLUSTERS)
1. `git pull origin master` — get latest coordination state
2. Read this file (`CLAUDE.md`)
3. Read `clusters/<your-cluster>/CLAUDE.md` for cluster-specific details
4. Read `coordination/DASHBOARD.md` for campaign status across all clusters
5. Read `coordination/COORDINATION.md` for campaign parameters and rules

### Session end protocol
1. Update `coordination/DASHBOARD.md` with your progress
2. Commit with `[<cluster>] <message>` prefix
3. `git push origin master`

### Communication rules
- This repo IS the communication channel
- Work assignments are in `coordination/manifests/`
- Messages between agents go in `coordination/inbox/<recipient>/`
- Large data transfers use Globus (not git) — see `coordination/globus/`
```

### 3.3. Create cluster env files

One file per cluster. These are `source`-able shell files with all cluster-specific paths and SLURM settings. This is what makes scripts portable across clusters.

**Template — `clusters/<cluster>.env`:**

```bash
# <Cluster Name> (<Institution>) — <Role: coordinator|worker>
CLUSTER_NAME="<cluster>"
CLUSTER_ROLE="<coordinator|worker>"

# Paths
PROJECT_ROOT="<absolute path to repo on this cluster>"
SCRATCH_ROOT="<scratch path if applicable>"

# SLURM
SLURM_ACCOUNT="<allocation account>"
GPU_TYPE="<a100|h100|v100|etc>"
GPU_GRES="gpu:<type>:1"
MAX_WALLTIME="<max walltime>"
MAIN_MEM="64G"

# Conda environments (names may differ per cluster)
CONDA_ENV_MAIN="<env name>"

# Containers (if using Apptainer/Singularity)
CONTAINER_DIR="${PROJECT_ROOT}/container"
# COLABFOLD_SIF="${CONTAINER_DIR}/colabfold.sif"

# Globus (for large file transfers)
GLOBUS_ENDPOINT="<endpoint UUID>"
GLOBUS_BASE_PATH="${PROJECT_ROOT}"
```

**Real example — `clusters/narval.env`:**

```bash
CLUSTER_NAME="narval"
CLUSTER_ROLE="worker"
PROJECT_ROOT="/home/ghaedi/projects/def-ghaedi/ghaedi/protein"
SCRATCH_ROOT="/scratch/ghaedi/protein"
SLURM_ACCOUNT="def-ghaedi"
GPU_TYPE="a100"
GPU_GRES="gpu:a100:1"
MAX_WALLTIME="6-23:00:00"
MAIN_MEM="64G"
CONTAINER_DIR="${PROJECT_ROOT}/container"
COLABFOLD_SIF="${CONTAINER_DIR}/colabfold_1.6.1-cuda12.sif"
COLABFOLD_CACHE="${CONTAINER_DIR}/colabfold_cache"
APPTAINER_MODULE="apptainer"
GLOBUS_ENDPOINT="a1713da6-098f-40e6-b3aa-034efe8b6e5b"
GLOBUS_BASE_PATH="${PROJECT_ROOT}"
```

Scripts auto-detect the cluster and source the right file:

```bash
case "$(hostname -f)" in
  *frontenac*|frnt*) CLUSTER="frontenac" ;;
  *nibi*)            CLUSTER="nibi" ;;
  *narval*)          CLUSTER="narval" ;;
  *) echo "ERROR: Unknown cluster" >&2; exit 1 ;;
esac
source "${REPO_ROOT}/clusters/${CLUSTER}.env"
```

### 3.4. Create per-cluster CLAUDE.md files

Each cluster gets its own instructions file at `clusters/<cluster>/CLAUDE.md`. This tells Claude Code what its role is and what HPC-specific details matter.

**Coordinator template — `clusters/frontenac/CLAUDE.md`:**

```markdown
# Frontenac — Coordinator (Agent F)

You are running on **Frontenac**. You are the **central coordinator**.

## Coordinator responsibilities
1. Assign work to worker clusters via `coordination/manifests/`
2. Update `coordination/DASHBOARD.md` after each session
3. Merge results from workers
4. Make campaign decisions (proceed/hold/reassign)

## HPC details
Source `clusters/frontenac.env` for all paths and SLURM settings.
- **GPU account:** `def-hpcg6049_gpu` (MUST specify)
- **Never specify `--partition`** — scheduler auto-routes
- **Primary GPU:** A100-PCIE-40GB
```

**Worker template — `clusters/narval/CLAUDE.md`:**

```markdown
# Narval — Worker (Agent Narval)

You are running on **Narval**. You are a **worker agent** coordinated from Frontenac.

## Worker responsibilities
1. Pull latest from `origin master` at session start
2. Execute assigned work
3. Commit summary results to git and push
4. Transfer large data to coordinator via Globus
5. Do NOT modify campaign parameters or settings

## HPC details
Source `clusters/narval.env` for all paths and SLURM settings.
- **Account:** `def-ghaedi`
- **GPU:** A100 40GB
- **Scratch purge:** 60 days — touch files monthly
```

### 3.5. Create the inbox system

```bash
mkdir -p coordination/inbox/{frontenac,narval,nibi}
touch coordination/inbox/{frontenac,narval,nibi}/.gitkeep
```

**`coordination/inbox/README.md`:**

```markdown
# Agent Inbox System

Inter-agent messaging via git. Each agent has an inbox directory.

## Protocol
1. To send a message: write a `.md` file in `inbox/<recipient>/`
2. Commit with `[<sender>] msg: <subject>` prefix and push
3. Recipient picks it up on next `git pull`
4. Recipient deletes the file after reading and commits

## Filename format
`YYYY-MM-DD_from-<sender>_<subject-slug>.md`

## Message template
```
# Message from <Sender>

**Date:** YYYY-MM-DD
**From:** <sender cluster>
**To:** <recipient cluster>
**Subject:** <one-line summary>

---

<message body — be specific about what action is needed>
```
```

### 3.6. Create the dashboard

**`coordination/DASHBOARD.md`:**

```markdown
# Campaign Dashboard

**Last updated:** <date> by <cluster> — <one-line summary>

## Cluster Status

| Cluster | Agent | Current Work | SLURM Jobs | Last Update |
|---------|-------|--------------|------------|-------------|
| Frontenac | F | <current task> | <job IDs> | <date> |
| Nibi | Nibi | <current task> | <job IDs> | <date> |
| Narval | Narval | <current task> | <job IDs> | <date> |

## Recent Actions

| Date | Agent | Action |
|------|-------|--------|
```

### 3.7. Create the coordination rules

**`coordination/COORDINATION.md`:**

```markdown
# Multi-Cluster Coordination Protocol

**Coordinator:** Frontenac (Agent F)

## Agent Registry
| Agent | Cluster | Working Dir | GPU | Status |
|-------|---------|-------------|-----|--------|

## Communication Protocol
1. Coordinator pushes instructions and status updates to `master`
2. Workers pull `master` at session start
3. Workers commit results and push to `master`
4. Large data transfers via Globus (not git)

## Commit message convention
Prefix all commits with the cluster name in brackets:
```
[frontenac] Update dashboard: Stage 2 complete
[narval] Complete counter-screen batch 1
```

## Conflict avoidance
Each cluster modifies only its own section in DASHBOARD.md and its own
manifest files. The coordinator modifies the overall status.

## Rules for All Agents
1. Pull before starting work; push after completing work
2. Use ONLY the provided settings and configs — no modifications without coordinator approval
3. All scripts use `set -eo pipefail` and absolute paths
4. Log all SLURM job IDs in DASHBOARD.md
```

### 3.8. Clone on each worker cluster

On each worker cluster:

```bash
cd /path/to/projects/
git clone git@github.com:<org>/<repo>.git
cd <repo>
# Verify hostname detection works
hostname -f
```

The agent will read CLAUDE.md on first session and self-identify.

---

## 4. How communication actually works (honest version)

### 4.1. The inbox flow

```
Coordinator (Frontenac)                    Worker (Narval)
─────────────────────                      ──────────────
                                           
1. Write file to                           
   inbox/narval/2026-05-29_from-           
   frontenac_do-task-X.md                  
                                           
2. git add, commit with                   
   "[frontenac] msg: do task X"            
                                           
3. git push origin master                  
                                           
   ~~~ TIME PASSES ~~~                     
                                           
                                           4. User starts Claude Code
                                              session on Narval
                                           
                                           5. Agent does git pull
                                              (session start protocol)
                                           
                                           6. Reads CLAUDE.md, detects
                                              it's on Narval
                                           
                                           7. Checks inbox/narval/ —
                                              sees the message
                                           
                                           8. Reads message, does task X
                                           
                                           9. Deletes message file
                                           
                                          10. Writes results to git,
                                              optionally sends reply to
                                              inbox/frontenac/
                                           
                                          11. Commits and pushes
```

**Key limitation:** Step 4 requires you (the human) to start the session. There is no way for the coordinator to trigger a session on another cluster. You must SSH into each cluster and start Claude Code manually.

**What about the inbox watcher?** We built one (`coordination/scripts/inbox_watcher.sh`) that polls `git pull` every 2 minutes and logs new messages. It is marginally useful — it tells you there's a message waiting, but it can't start a Claude Code session to act on it. In practice, we rarely used it.

### 4.2. What messages look like

**A real coordinator → worker message (instructions):**

```markdown
# Message from Frontenac (Coordinator)

**Date:** 2026-05-29
**From:** Frontenac (Agent F)
**To:** Nibi
**Subject:** Stop production after current jobs, start Stage 7.5 ranking now

---

## Decisions

### 1. No resubmission — 2,051 trajectories is sufficient
Let jobs 14990515–19 finish naturally but do NOT submit new jobs.

### 2. Start Stage 7.5 ranking NOW on the 224 survivors
Rank using the composite score from the development plan.

### Stage 7.5 ranking spec
| Metric | Weight | Direction |
|--------|--------|-----------|
| i_pTM | 0.25 | Higher is better |
| dG | 0.20 | More negative is better |
...

**Output:** Write to `alzheimer/bindcraft/tfr1/filtering/stage7_5_ranked.csv`
```

**A real worker → coordinator message (results):**

```markdown
# Message from Narval

**Date:** 2026-05-30
**From:** Narval
**To:** Frontenac (Coordinator)
**Subject:** Phase B monomer pLDDT COMPLETE — 26/26 pass

---

## Result
**All 26 Phase A survivors pass monomer pLDDT > 85.**

| Metric | Value |
|--------|-------|
| Designs tested | 26 |
| Pass | 26 |
| Mean pLDDT | 92.80 |
| Min pLDDT | 88.00 |

### Files
- `filtering/stage4/phase_b_results.csv`

### Status
All 26 designs ready for Phase C on Frontenac.
```

### 4.3. Merge conflicts

They happen. Two agents push at the same time, especially when both update DASHBOARD.md. The resolution pattern:

```bash
git push origin master
# ERROR: rejected (fetch first)

git pull --no-rebase origin master
# CONFLICT in coordination/DASHBOARD.md

# Resolve: keep both agents' updates, take the most recent "Last updated" line
# Edit the file to remove conflict markers

git add coordination/DASHBOARD.md
git commit -m "[frontenac] Merge Nibi+Narval updates"
git push origin master
```

**Prevention strategy:** Each agent only edits its own row in the dashboard table and its own inbox. The coordinator edits the summary lines. This reduces conflicts to the `Last updated` line, which is trivially resolvable.

### 4.4. Manifests (work assignments)

For batch work (e.g., "run ColabFold on 62 designs × 8 targets"), the coordinator creates TSV manifests that assign specific tasks to specific clusters.

**Format — `coordination/manifests/manifest_stage3_narval.tsv`:**

```tsv
design_id	target_pdb	cluster	status
ab42_l60_s103118_mpnn17	9CO4	narval	pending
ab42_l60_s103118_mpnn17	9CKI	narval	pending
ab42_l60_s103118_mpnn17	9CK6	narval	pending
```

Workers update `status` from `pending` → `complete` or `failed` as they process tasks.

**When we actually used manifests vs. inbox messages:**
- Manifests: Stage 3 counter-screen (496 specific tasks to distribute)
- Inbox messages: everything else (instructions, decisions, status reports, questions)

Manifests are overkill for most coordination. Use them only when you have a concrete list of items to parallelize.

---

## 5. The dashboard — what actually gets updated

The dashboard is the most-read file in the repo. Every agent reads it at session start and updates it at session end. It has three sections that matter:

1. **Last updated line** — one-line summary of who did what last
2. **Cluster status table** — one row per cluster: current work, running SLURM jobs, key numbers
3. **Recent actions table** — chronological log of all significant actions

The dashboard is NOT a planning document. It is a snapshot of what IS, not what SHOULD BE. Agents use it to understand the current state before deciding what to do next.

---

## 6. What the coordinator actually does

In practice, the coordinator agent:

1. **Starts every session** by pulling git, reading the dashboard, and checking its inbox
2. **Reviews results** from workers (committed CSVs, inbox messages)
3. **Makes decisions** (with the PI/user): proceed? recalibrate? skip?
4. **Sends instructions** to workers via inbox messages — these are specific and actionable, not vague
5. **Updates all status files** (DASHBOARD.md, HANDOFF.md, PROJECT_STATUS.md)
6. **Commits and pushes** with `[frontenac]` prefix

The coordinator does NOT:
- Start sessions on other clusters (you do this manually)
- Monitor SLURM queues on other clusters
- Transfer large files (Globus is a separate manual step)

---

## 7. What workers actually do

Worker agents:

1. **Pull and read** the dashboard + their inbox
2. **Execute the specific task** from the inbox message or manifest
3. **Report results** — commit CSVs/status to git, send reply to coordinator inbox
4. **Delete read inbox messages** to keep the inbox clean
5. **Push** with `[<cluster>]` prefix

Workers do NOT:
- Make campaign decisions
- Modify shared parameters or settings
- Edit other clusters' sections of the dashboard

---

## 8. Globus (large file transfers)

Git is for small files (CSVs, markdown, scripts). PDB files, container images, and datasets go through Globus.

**`coordination/globus/endpoints.md`:**

```markdown
| Cluster | Endpoint UUID | Type | Base path |
|---------|---------------|------|-----------|
| Frontenac | 79136050-... | personal | /global/project/hpcg6049/protein |
| Narval | a1713da6-... | institutional | /home/ghaedi/projects/.../protein |
| Nibi | <endpoint-id> | institutional | /home/ghaedi/projects/.../protein |
```

Transfers are initiated manually via `globus transfer` CLI or the web UI. We stored reusable commands in `coordination/globus/transfer_recipes.sh`.

---

## 9. Honest assessment — what we'd change

### What worked
- **Git as communication channel** was reliable and auditable. We never lost a message.
- **Cluster env files** made scripts truly portable. Same SLURM script ran on all 3 clusters by sourcing the right `.env`.
- **The dashboard** was invaluable for onboarding — any agent could get up to speed in 30 seconds.
- **Commit prefixes** (`[frontenac]`, `[narval]`) made `git log` instantly readable.
- **Inbox messages with specific instructions** (not vague tasks) got executed correctly on the first try.

### What was friction
- **Manual session starts.** You have to SSH to each cluster and start Claude Code. There is no "run this on Narval" button.
- **Stale dashboard.** If a worker pushes results but the coordinator doesn't start a session for a day, the dashboard is out of date from the coordinator's perspective. Each agent only updates its own view.
- **Merge conflicts on DASHBOARD.md.** Happened 2-3 times. Always trivially resolvable but annoying.
- **No delivery confirmation.** You write to an inbox, push, and hope the recipient reads it. No read receipt, no retry.
- **Worker agents needed very specific instructions.** Vague messages like "run the counter-screen" produced questions. Messages with exact commands, thresholds, and output paths worked first time.
- **Inbox cleanup was inconsistent.** Some agents deleted read messages, some didn't. Old messages piled up in Nibi's inbox.

### What we'd add next time
- A `coordination/STATUS.yaml` that each agent machine-updates (easier to parse than DASHBOARD.md)
- A `coordination/inbox/<cluster>/QUEUE.md` that agents append to instead of creating individual files (reduces git churn)
- Stricter inbox cleanup protocol (delete on read, always)
- A standardized result format for worker reports (JSON schema, not freeform markdown)

---

## 10. Minimal replication checklist

To replicate this setup for a new project on the same HPC clusters:

1. [ ] Create GitHub repo, clone on all clusters
2. [ ] Write root `CLAUDE.md` with hostname detection and session protocols
3. [ ] Create `clusters/<cluster>.env` for each cluster (copy and adapt from above)
4. [ ] Create `clusters/<cluster>/CLAUDE.md` for each cluster (coordinator vs worker)
5. [ ] Create `coordination/` directory with DASHBOARD.md, COORDINATION.md, inbox dirs
6. [ ] Create `coordination/inbox/<cluster>/.gitkeep` for each cluster
7. [ ] Add `coordination/inbox/README.md` with the protocol
8. [ ] Initial commit and push
9. [ ] Clone on each worker cluster, verify hostname detection
10. [ ] Start a Claude Code session on the coordinator — it should self-identify and read the right files
11. [ ] Start a Claude Code session on a worker — it should self-identify and wait for instructions

**Total setup time:** ~30 minutes for the coordinator, ~5 minutes per worker (clone + verify).

---

## 11. File-by-file reference

| File | Purpose | Who edits | When |
|------|---------|-----------|------|
| `CLAUDE.md` | Root instructions, hostname detection, protocols | Coordinator (rarely) | Setup, protocol changes |
| `clusters/<cluster>.env` | Paths, SLURM account, GPU type, Globus | Coordinator (rarely) | Setup, new software |
| `clusters/<cluster>/CLAUDE.md` | Per-cluster agent instructions | Coordinator | Setup, role changes |
| `coordination/DASHBOARD.md` | Live status across all clusters | All agents | Every session |
| `coordination/COORDINATION.md` | Campaign parameters, agent registry, rules | Coordinator | Setup, major changes |
| `coordination/inbox/<cluster>/*.md` | Messages between agents | Any sender | As needed |
| `coordination/manifests/*.tsv` | Batch work assignments | Coordinator creates, workers update status | When distributing batch work |
| `coordination/globus/endpoints.md` | Globus endpoint IDs | Coordinator | Setup |

---

*Written by Claude Code (Frontenac coordinator), 2026-05-30. Based on 4 days of live multi-agent coordination across 3 HPC clusters.*
