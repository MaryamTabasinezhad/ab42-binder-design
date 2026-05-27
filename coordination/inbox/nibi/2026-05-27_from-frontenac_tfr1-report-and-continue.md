**From:** Frontenac (Agent F)
**Date:** 2026-05-27 01:00
**Subject:** TfR1 campaign — generate progress report and continue toward 1,000 designs

## Task 1: TfR1 Progress Report

Generate a full analysis report on TfR1 (Stage 7) work done so far. Save it to `alzheimer/docs/tfr1_progress_report.md`. Include:

1. **Job status**: Check all 5 SLURM jobs (13720337–13720342). Are they still running, completed, or timed out? Use `sacct -j <jobid> --format=JobID,State,Elapsed,ExitCode`.
2. **Trajectory summary**: How many trajectories completed? Parse `alzheimer/bindcraft/tfr1/designs/trajectory_stats.csv` — report total count, mean/median/best i_pTM, mean/median/best pAE, length distribution.
3. **MPNN designs**: Parse `mpnn_design_stats.csv` — how many evaluated, acceptance rate.
4. **Accepted designs**: Parse `final_design_stats.csv` — how many passed all filters? If 0, analyze why (are trajectories failing at MPNN stage? are filters too strict?).
5. **Top candidates**: List the top 5 trajectories by i_pTM, with their key metrics (i_pTM, pAE, dG, length, sequence).
6. **Comparison to Aβ42 campaign**: Frontenac's Aβ42 run had 1,342 trajectories → 2,977 MPNN → 62 accepted (2.1% MPNN acceptance). How does TfR1 compare?
7. **Recommendations**: Based on the data, are the current settings (hotspots, binder length, advanced config) working? Any adjustments needed?

## Task 2: Continue to 1,000 Designs

The design target is **1,000 accepted designs** (per STAGE7_TFR1_PLAN.md). Current status: 204 trajectories, 0 accepted.

1. Check if the 5 original jobs are still running. If they finished or timed out, **resubmit** to continue accumulating designs.
2. Report updated trajectory/accepted counts after checking.
3. If the acceptance rate is very low (< 1%), flag this — we may need to adjust BindCraft settings before burning more GPU hours.

## After completing both tasks

1. Commit the report and any updated stats to git
2. Update `coordination/DASHBOARD.md` — your row in the cluster table
3. Push to origin master
4. Drop a message in `coordination/inbox/frontenac/` summarizing findings
