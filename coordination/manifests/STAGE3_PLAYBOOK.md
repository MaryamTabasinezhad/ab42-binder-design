# Stage 3: Negative-Design Counter-Screen Playbook

## Goal

Test all 62 accepted BindCraft designs against 8 targets using ColabFold complex prediction. A design passes Stage 3 only if:
- **Positive:** pae_interaction < 10 on 9CO4 (re-confirmation)
- **Negative:** pae_interaction > 15 on ALL 7 counter-targets

## Targets

| Target | PDB | Type | Purpose |
|--------|-----|------|---------|
| 9CO4 | `alzheimer/structures/9CO4.pdb` | Positive | Receptor-bound Conf 1 (design target) |
| 9CKI | `alzheimer/structures/negative_targets/9CKI.pdb` | Negative | Receptor-bound Conf 2 (plaque-equivalent) |
| 9CK6 | `alzheimer/structures/negative_targets/9CK6.pdb` | Negative | Sarkosyl-insoluble plaque fibril |
| 7Q4B | `alzheimer/structures/negative_targets/7Q4B.pdb` | Negative | Brain plaque type I |
| 7Q4M | `alzheimer/structures/negative_targets/7Q4M.pdb` | Negative | Brain plaque type II |
| 6SHS | `alzheimer/structures/negative_targets/6SHS.pdb` | Negative | Abeta-40 fibril (ARIA risk) |
| 1IYT | `alzheimer/structures/negative_targets/1IYT.pdb` | Negative | Abeta-42 monomer (assembly selectivity) |
| Ab40_monomer | `alzheimer/structures/negative_targets/Ab40_monomer_af2.pdb` | Negative | Abeta-40 monomer (isoform selectivity) |

## Input

Binder sequences are in `alzheimer/bindcraft/designs/final_design_stats.csv`, column `Sequence`.

For each (design, target) pair, the ColabFold input is the binder sequence joined with the target chain sequence(s) by colon (`:`). For multi-chain targets (9CO4 has chains C/E/G), join all target chains.

## ColabFold Setup

```bash
source clusters/narval.env  # or your cluster's env file
eval "$(conda shell.bash hook)"
conda activate ${CONDA_ENV_COLABFOLD}
```

If ColabFold is not installed, create the env:
```bash
conda create -n colabfold python=3.11
conda activate colabfold
pip install colabfold[alphafold]
```

## Running the Counter-Screen

### Step 1: Extract binder sequences and target sequences

Write a Python script that:
1. Reads `final_design_stats.csv` to get design_id → binder sequence mapping
2. Reads each target PDB to extract target chain sequences (use BioPython)
3. For each (design, target) pair in the manifest, creates a ColabFold input CSV line:
   `id,sequence` where sequence = `binder_seq:target_chain1_seq:target_chain2_seq:...`

### Step 2: Run ColabFold in batch

ColabFold can process a CSV of complexes:
```bash
colabfold_batch input.csv output_dir/ --num-models 1 --num-recycle 3
```

Use `--num-models 1` (model_1_ptm only) to save compute. One model is sufficient for pae_interaction screening.

### Step 3: Extract pae_interaction from results

For each prediction, extract:
- `pae_interaction`: mean PAE between binder and target chains (lower = more confident interaction)
- `iptm`: interface pTM score
- `plddt`: per-residue confidence

ColabFold outputs JSON score files with these metrics.

### Step 4: Apply filters

```python
POSITIVE_THRESHOLD = 10   # pae_interaction < 10 on 9CO4
NEGATIVE_THRESHOLD = 15   # pae_interaction > 15 on all 7 negatives

# A design passes if:
# 1. pae_interaction on 9CO4 < POSITIVE_THRESHOLD
# 2. pae_interaction on ALL 7 negatives > NEGATIVE_THRESHOLD
```

### Step 5: Save results

Write to `alzheimer/bindcraft/filtering/stage3_results.csv`:
```
design_id,target,pae_interaction,iptm,plddt_binder,pass
```

And a summary to `alzheimer/bindcraft/filtering/stage3_summary.csv`:
```
design_id,pae_9CO4,pae_9CKI,pae_9CK6,pae_7Q4B,pae_7Q4M,pae_6SHS,pae_1IYT,pae_Ab40,pass_positive,pass_all_negative,pass_stage3
```

## SLURM Strategy

### Option A: Single batch job (simpler)
Submit one job per target (8 jobs), each processing all 62 designs against that target:
```bash
#SBATCH --account=def-ghaedi
#SBATCH --gres=gpu:a100:1
#SBATCH --time=05:59:00
#SBATCH --mem=48G
```
~62 predictions × 5 min = ~5 hours per target. Fits in 6-hour walltime.

### Option B: Array job (faster)
Submit 496 individual tasks as a SLURM array:
```bash
#SBATCH --array=1-496%20
```
Each task runs one ColabFold prediction (~5 min). Faster but more scheduling overhead.

**Recommendation:** Option A (8 jobs) is simpler and sufficient.

## Decision Gate 1 Criteria

After Stage 3 completes:

| Outcome | Criterion | Action |
|---------|-----------|--------|
| **Pass** | >= 20 designs pass both filters | Proceed to Stage 4 |
| **Marginal** | 5-19 designs pass | Expand campaign, relax parameters |
| **Fail** | < 5 designs pass | Switch to RFdiffusion pipeline |

## Manifest

Work assignments are in `coordination/manifests/manifest_stage3_narval.tsv`. Update the `status` column as tasks complete.
