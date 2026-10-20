# Interview slide: AI-designed Aβ42 × TfR1 bispecific binders

One 16:9 slide for a postdoctoral interview, prepared 2026-10-20 from repository data at commit beff539. Status: complete; next scientific step is experimental expression, binding/selectivity and transport evaluation. No new protein predictions were run.

## Deliverables

- `08_03_alzheimer_bispecific_interview_slide.pptx`: one PowerPoint slide containing an embedded high-resolution image; text is not individually editable. The Python source is provided for revision.
- Matching `.pdf` and `.png`: presentation/export versions.
- `08_01_fusion_arm_confidence.png`: N-terminal versus C-terminal arm mean pLDDT, all 250 fusions.
- `08_02_fusion_ptm_interdomain_pae.png`: fusion pTM versus inter-domain PAE, all 250 fusions.
- `08_04_fusion_plot_data.csv` and `08_04_slide_summary.json`: plot data and counts.
- `build_interview_slide.py`: regenerate with `python3 alzheimer/bindcraft/fusion/pic_graphs/build_interview_slide.py` from the repository root. Uses Python standard library and the existing Pillow installation; no software was installed.

## Evidence and interpretation

- `../stage8_results_merged.csv`: 250 unique designs, 183 pass (73.2%), 67 fail. Scores agree exactly with the populated metric rows pooled from `stage8_results_splitA.csv` (125 predictions) and `stage8_results_splitB.csv` (125 predictions). All 250 pass flags were recalculated and agree with the script's strict thresholds: both arm pLDDT >80 and inter-domain PAE >15 Å. Source: `../scripts/analyze_fusions.py`.
- `../inputs/fusion_manifest.csv` and `../../../docs/STAGE8_FUSION_PLAN.md`: five Aβ42 binders × five TfR1 binders × five linkers × two domain orders = 250. Arm 1/2 identify sequence positions, not fixed target identities, because both domain orders were tested.
- `../../../docs/bindcraft_62design_analysis.md`: 62 accepted Aβ42 designs, 1,342 reported trajectories and 2,977 evaluated MPNN designs. The 62 accepted rows are present in `../../designs/final_design_stats.csv`.
- Repository-root `coordination/DASHBOARD.md` (2026-06-25): 380 accepted TfR1 designs and 224 survivors; `../../tfr1/filtering/stage7_5_full_ranking.csv` contains the 224 survivor rows. The committed TfR1 accepted-design CSV has 310 rows and is an earlier snapshot. Thus **442 = 62 + 380 is the campaign-reported accepted arm library**, not a count of all raw structures committed to Git, all generated sequences, or fusion designs.
- `../../filtering/stage5/stage5_ranked.csv`: 23 ranked Aβ42 designs; the 224-row TfR1 full ranking supports the other survivor count.
- `../../../HANDOFF.md` identifies BindCraft as the primary engine and RFdiffusion as a separate/fallback route. ProteinMPNN redesign and AlphaFold2/ColabFold prediction are recorded. The slide does not incorrectly imply that this fusion cohort originated in RFdiffusion or that all listed tools formed one serial pipeline.

High inter-domain PAE means uncertain relative domain placement; it is a pipeline heuristic for independent domains, not proof of independence or retained binding. Global pTM is not a hard gate. Fusion ipTM and binder–target interface PAE are not present in Stage 8 monomer scores; inter-domain PAE must not be relabeled as binding-interface PAE. The slide reports computational fold screening, not experimentally validated dual binding, selectivity, production or BBB transport. Earlier computational counter-screens were bypassed after unsuccessful positive controls (see `../../../HANDOFF.md`); their selectivity gates are not part of the Stage 8 pass count.

## Suggested 45–60 second narration

“My current project aims to combine an amyloid-beta binder with a transferrin receptor 1 binder as a potential brain-delivery strategy for Alzheimer’s disease. I built the computational workflow from target and epitope preparation through de novo design, sequence redesign, structural scoring and developability ranking. The documented campaigns yielded 62 accepted amyloid-beta designs and 380 TfR1 designs. I selected five diverse binders per target and tested five linkers in both domain orders, generating 250 fusion designs. AlphaFold2-based screening identified 183 that passed the predefined domain-folding and inter-domain PAE gates. The plots show each domain’s folding confidence and why whole-chain pTM alone is not an appropriate gate for a flexible tandem construct. These are computational candidates; the next step is to establish expression, dual-target binding, selectivity and BBB transport experimentally.”

## Verification

Recomputed all Stage 8 gate flags and reconciled split metrics against the merged table. Inspected the rendered slide for legibility and clipping. Checked the PowerPoint ZIP and parsed all XML parts; PNG/PDF exports were generated successfully. PowerPoint/LibreOffice is unavailable on this host, so no application-level PowerPoint rendering was performed.
