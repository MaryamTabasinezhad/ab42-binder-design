# Interview slide: AI-designed Aβ42 × TfR1 bispecific binders

One 16:9 slide for a postdoctoral interview, prepared 2026-10-20 from repository data at commit beff539. Status: complete; next scientific step is experimental expression, binding/selectivity and transport evaluation. No new protein predictions were run.

## Presentation revision (2026-10-20)

The revised slide preserves the one-slide structure and uses Liberation Sans (an Arial-compatible presentation font), a white header and light footer instead of the dark blue bands, and a blue/orange scientific plotting palette (#0072B2 / #D55E00). Only the first footer line remains; the validation caveats and separate RFdiffusion-route explanation remain documented here.

The left plot now uses **TfR1 arm mean pLDDT on the x-axis and Aβ42 arm mean pLDDT on the y-axis**. Coordinates are remapped using each fusion's `domain_order`, checked against `../inputs/fusion_manifest.csv`: for `ab-tfr1`, TfR1 is arm 2; for `tfr1-ab`, TfR1 is arm 1. The exported plot-data CSV includes these target-specific scores and domain order. This deliberately changes point placement relative to the original positional-arm plot while preserving each design's scores and pass flag.

The slide additionally reports **1,342 Aβ42 trajectories and 2,051 TfR1 trajectories before filtering**, as documented in `../../../docs/bindcraft_62design_analysis.md` and repository-root `coordination/DASHBOARD.md`. These are campaign-reported design-exploration counts, not accepted-design counts or counts of all ProteinMPNN sequences. The reported accepted arm library remains 62 + 380 = 442, and the fusion result remains 183/250. Raw trajectory/stat CSVs in Git are partial snapshots; no unrecorded total of evaluated TfR1 sequences is inferred.

## Editable PowerPoint version

`08_05_alzheimer_bispecific_interview_slide_editable.pptx` is the editable version of the revised slide. It contains **35 native text boxes, editable panel shapes, and two native scatter charts**, with two embedded Excel workbooks. It contains no flattened slide image. Select text or shapes to edit them; select a chart and use **Chart Design → Edit Data** to change its data, or **Format Axis** to change axes. Blue/orange point series and dashed threshold series can be formatted independently. The domain mappings and 183/250 pass count are unchanged. Text uses Arial; PowerPoint may substitute a local font if Arial is unavailable.

Rebuild with `python3 alzheimer/bindcraft/fusion/pic_graphs/build_editable_slide.py`. The existing image-based PowerPoint, PDF and PNG are preserved separately. Native chart rendering can differ slightly from the PNG preview. The new file's package, XML, both embedded workbooks, 35 text boxes and two chart references were checked; PowerPoint/LibreOffice is not available on this host, so application-level rendering has not been verified.

## Deliverables

- `08_03_alzheimer_bispecific_interview_slide.pptx`: one PowerPoint slide containing an embedded high-resolution image; text is not individually editable. The Python source is provided for revision.
- Matching `.pdf` and `.png`: presentation/export versions.
- `08_01_fusion_arm_confidence.png`: TfR1 versus Aβ42 arm mean pLDDT, all 250 fusions.
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

## Understanding inter-domain and intra-domain PAE

**PAE (Predicted Aligned Error)** is AlphaFold's estimate of positional error for one residue when the predicted and true structures are aligned using another residue's local frame. It is measured in ångströms (Å); 10 Å = 1 nanometre. Low PAE indicates confident relative placement; high PAE indicates uncertain relative placement. PAE is prediction uncertainty, not a measured structural error or the physical distance between residues or domains.

**Inter-domain PAE** summarizes uncertainty between residues belonging to different domains. In these tandem fusions, it describes uncertainty about the position and orientation of one binder arm relative to the other. The Stage 8 script averages the two cross-domain blocks of the PAE matrix, in both directions, excluding the linker. High inter-domain PAE can be compatible with two individually well-folded arms whose relative arrangement is uncertain. It does not establish that the arms are far apart, sufficiently separated, flexible, independently functional, or able to bind both targets simultaneously.

**Intra-domain PAE** describes uncertainty between residues within the same domain. For example, a binder containing three helices should ideally have low PAE between those helices, supporting confidence in their relative packing. Higher PAE within an arm can indicate uncertain packing, a flexible loop or subregion, or an unreliable structural prediction; it does not by itself distinguish those explanations. Inspecting the within-domain PAE pattern is more informative than relying only on a whole-domain average.

| Comparison | Desired or acceptable pattern | Interpretation |
|---|---|---|
| Within each binder arm | Low intra-domain PAE | Confident relative placement of parts of that arm |
| Between the two binder arms | Higher inter-domain PAE can be acceptable for this tandem design | Uncertain relative domain arrangement despite potentially confident individual folds |

The current CSV files report **inter-domain PAE**, not intra-domain PAE. To calculate intra-domain PAE, use each arm's within-domain block of the original PAE matrix with the correct sequence boundaries and linker exclusion. Per-arm pLDDT is a separate local confidence measure and cannot be converted into intra-domain PAE.

### Reading the right-hand plot

Each dot represents one of the 250 fusions. The horizontal axis is whole-chain pTM (higher means more confident overall topology); the vertical axis is mean inter-domain PAE (higher means less certain relative placement of the arms). For example, a point at pTM 0.53 and PAE 23 Å means moderate whole-chain confidence and substantial uncertainty between arms; 23 Å is not their separation distance. A well-predicted fold in each arm can coexist with moderate global pTM if their relative arrangement is uncertain.

The dashed line at 15 Å is the project's **inter-domain PAE >15 Å** screening heuristic. It is not a universal AlphaFold quality threshold, and passing it does not prove domain independence. Blue points pass this threshold and both per-arm pLDDT >80 gates. Orange points fail at least one gate; an orange point above the line therefore fails at least one arm's pLDDT gate. Lower-PAE, higher-pTM orange designs have a more confidently predicted overall arrangement and are not necessarily biologically worse.

In the 250-design CSV, inter-domain PAE ranges from **10.29 to 27.69 Å**; the median among the 183 passing fusions is **23.16 Å**. These observed values are distinct from the model's output range. PAE output limits depend on the prediction implementation; values near the upper reporting limit should be interpreted as high uncertainty rather than a precise error estimate.

## Understanding pTM for one domain and a two-domain fusion

**pTM (predicted TM-score)** estimates the overall structural similarity expected between a prediction and the true structure. It ranges from **0 to 1**, with higher values indicating greater confidence in the overall fold and arrangement. It is dimensionless, not a distance, and a value of 0.6 does not mean a 60% probability that the structure is correct.

| Structure supplied for prediction | What the reported pTM evaluates |
|---|---|
| One isolated binder domain | The overall fold of that domain |
| A complete two-domain fusion | The whole fusion, including the relative arrangement of its domains |

The Stage 8 CSV's `ptm` column is **whole-fusion pTM**. It does not contain separate pTM scores for the two arms. Per-arm pLDDT is a different confidence measure and must not be called per-arm pTM.

### Thresholds and interpretation

A pTM above approximately **0.5** is commonly used as a rough indication that the overall fold may be correct. This is not a universal acceptance threshold or experimental validation. Scores can be influenced by domain size, uncertain relative domain placement, and poorly predicted regions. A larger, confidently predicted domain can dominate the score even when another part is less reliable. See [EMBL-EBI's AlphaFold confidence-score guidance](https://www.ebi.ac.uk/training/online/courses/alphafold/inputs-and-outputs/evaluating-alphafolds-predicted-structures-using-confidence-scores/confidence-scores-in-alphafold-multimer/).

In a tandem fusion, each arm can have a confident individual fold while their relative orientation remains uncertain. This can reduce whole-fusion pTM; it does not by itself establish that either arm is incorrectly folded. The converse also matters: a high whole-fusion pTM does not prove dual-target binding or successful BBB transport.

For this project's Stage 8 analysis:

- `pass_ptm_soft` records whether **pTM >0.6**. This is an informational flag, not a required gate. The numerical pTM score also acts as a ranking tiebreaker after mean and minimum per-arm pLDDT.
- `pass_all` requires **both arms' mean pLDDT >80 and inter-domain PAE >15 Å**. It does not require `pass_ptm_soft=True`.
- The median whole-fusion pTM among the **183 passing designs is 0.53**. Those designs pass the stated Stage 8 gates despite many falling below the soft pTM threshold.

A useful distinction for presenting the slide is: **per-arm confidence asks whether each piece is well formed; whole-fusion pTM also reflects confidence in how the pieces fit together.** Evaluate pTM alongside per-arm pLDDT and the PAE matrix rather than using it alone to judge a tandem fusion.

## Suggested 45–60 second narration

“My current project aims to combine an amyloid-beta binder with a transferrin receptor 1 binder as a potential brain-delivery strategy for Alzheimer’s disease. I built the computational workflow from target and epitope preparation through de novo design, sequence redesign, structural scoring and developability ranking. The documented campaigns yielded 62 accepted amyloid-beta designs and 380 TfR1 designs. I selected five diverse binders per target and tested five linkers in both domain orders, generating 250 fusion designs. AlphaFold2-based screening identified 183 that passed the predefined domain-folding and inter-domain PAE gates. The plots show each domain’s folding confidence and why whole-chain pTM alone is not an appropriate gate for a flexible tandem construct. These are computational candidates; the next step is to establish expression, dual-target binding, selectivity and BBB transport experimentally.”

## Verification

Recomputed all Stage 8 gate flags and reconciled split metrics against the merged table. Inspected the rendered slide for legibility and clipping. Checked the PowerPoint ZIP and parsed all XML parts; PNG/PDF exports were generated successfully. PowerPoint/LibreOffice is unavailable on this host, so no application-level PowerPoint rendering was performed.

README clarification, 2026-10-20: added PAE definitions, within-arm versus between-arm interpretation, and a reading guide for the right-hand plot. Checked against the existing Stage 8 script and recorded CSV summaries; no predictions or slide regeneration were performed.

README clarification, 2026-10-20: added single-domain versus whole-fusion pTM, its 0–1 range, general interpretation, and the project-specific >0.6 soft flag and ranking role. Checked against `../scripts/analyze_fusions.py` and the recorded summary; no predictions or slide regeneration were performed.

Presentation revision verification, 2026-10-20: regenerated PPTX/PDF/PNG and both plots; verified target-to-arm mappings for all 250 designs against the manifest, all Stage 8 flags and split metrics, and the PPTX ZIP/XML contents. Visually inspected the final slide. No new protein predictions were run.

Editable-slide milestone, 2026-10-20: added native editable PowerPoint and its reproducible builder; retained existing slide exports and scientific results.

## General bispecific binder / antibody workflow

The current general figure is a proposed methodological schematic adapted from `Chart1_DeNovo_Binder_Design.png` and `Chart2_Screening_and_Fusion.png`, with original charts preserved. It does not report completed experimental stages or new predictions.

- [PNG figure](08_06_general_bispecific_design_workflow.png): 2400 × 1350; 180 mm print width, approximately 339 dpi.
- [Editable PowerPoint](08_06_general_bispecific_design_workflow_editable.pptx): native text, boxes and vector connectors, with no flattened slide image.
- [Vector PDF](08_06_general_bispecific_design_workflow.pdf): 180 × 101.25 mm, embedded fonts, no raster images, minimum label size 7.02 pt.
- [Figure legend, scientific notes, abbreviations and primary references](08_06_general_bispecific_design_workflow_legend.md).

Panel A covers target-specific discovery for each arm: target definition, modality-specific generation, independent complex reassessment where practical, and arm selection. Panel B covers format engineering and experimental testing; its numbered path runs from right to left, avoiding the previous long return connector. Blue denotes computational design/selection and green denotes experimental assessment, including the early isolated-arm check. RFantibody's internal RF2 filtering is distinguished from independent reassessment; IgG-like chain pairing is explicitly format-dependent. No universal computational score threshold is specified.

Rebuild all three exports with `python3 alzheimer/bindcraft/fusion/pic_graphs/build_visual_workflow_slide.py`; `build_general_workflow.py` forwards to the same builder. Uses existing Pillow, pycairo and Liberation Sans. Text uses Arial in PowerPoint and its compatible Liberation Sans equivalent in PNG/PDF.

Publication-preparation milestone, 2026-10-20: revised scientific gates and layout; added a proposed-workflow designation, full legend and references, 180-mm vector PDF and explicit export specifications. Verified 45 native text labels and 82 native shapes in the PPTX; inspected PNG and rendered PDF; checked PDF dimensions, embedded fonts and absence of raster images. Journal-specific adaptation and manuscript review remain necessary before submission. Native PowerPoint rendering is unavailable on this host. Temporary inspection paths and commands are recorded in the legend; durable artifacts and builder are present here. No software installation or protein inference was performed.
