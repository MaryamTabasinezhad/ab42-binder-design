# Work Assignment Manifests

Manifests assign specific tasks to specific clusters. Each manifest is a TSV file.

## Format

```tsv
design_id	target_pdb	cluster	status
ab42_l86_s453481_mpnn1	9CO4	frontenac	pending
ab42_l86_s453481_mpnn1	9CKI	frontenac	pending
...
```

## Columns

- `design_id` — BindCraft design name (matches `final_design_stats.csv` Design column)
- `target_pdb` — counter-screen target (9CO4, 9CKI, 9CK6, 7Q4B, 7Q4M, 6SHS, 1IYT, Ab40_monomer)
- `cluster` — assigned cluster (frontenac, nibi, narval)
- `status` — `pending`, `running`, `complete`, `failed`

## Rules

1. Each (design_id, target_pdb) pair appears in exactly ONE manifest
2. Workers process only rows assigned to their cluster
3. Workers update `status` to `complete` or `failed` as tasks finish
4. Workers commit updated manifests and push

## Naming

- `manifest_stage3_<cluster>.tsv` — Stage 3 counter-screen assignments
- `manifest_stage7_<cluster>.tsv` — Stage 7 TfR1 campaign assignments (future)
