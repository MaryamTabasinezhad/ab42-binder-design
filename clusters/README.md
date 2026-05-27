# Cluster Configurations

Each HPC cluster has:
- `<cluster>.env` — shell-sourceable env vars (paths, SLURM account, GPU type, conda envs, Globus endpoint)
- `<cluster>/CLAUDE.md` — Claude Code instructions specific to that cluster

## Supported clusters

| Cluster | Role | GPU | Account | Env file |
|---------|------|-----|---------|----------|
| Frontenac | Coordinator | A100 40GB | `def-hpcg6049_gpu` | `frontenac.env` |
| Nibi | Worker | H100 80GB | `def-ghaedi` | `nibi.env` |
| Narval | Worker | A100 40GB | `def-ghaedi` | `narval.env` |

## How scripts use cluster configs

Scripts auto-detect the cluster and source the correct env file:

```bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "$(hostname -f)" in
  *frontenac*|frnt*) CLUSTER="frontenac" ;;
  *nibi*)            CLUSTER="nibi" ;;
  *narval*)          CLUSTER="narval" ;;
  *cedar*)           CLUSTER="cedar" ;;
  *graham*)          CLUSTER="graham" ;;
  *) echo "ERROR: Unknown cluster $(hostname -f)" >&2; exit 1 ;;
esac
source "${REPO_ROOT}/clusters/${CLUSTER}.env"
```

## Adding a new cluster

1. Create `<cluster>.env` with all required variables (copy an existing one as template)
2. Create `<cluster>/CLAUDE.md` with cluster-specific instructions
3. Add the hostname pattern to the detection `case` block
4. Update `coordination/COORDINATION.md` agent registry
5. Update `coordination/DASHBOARD.md`
