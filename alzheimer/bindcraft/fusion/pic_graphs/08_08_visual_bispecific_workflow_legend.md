# 08_08 — Visual workflow for de novo bispecific protein design

**Figure | Proposed structure-guided discovery and validation of bispecific
proteins.** **A**, Repeat target-specific arm discovery for each target or
epitope: define accessible epitopes in their native context; generate
miniprotein binders or antibody/VHH candidates using modality-appropriate
methods; reassess predicted complexes; select diverse, developable candidates
and measure isolated-arm binding and specificity where feasible. RFdiffusion
followed by ProteinMPNN, or BindCraft, are shown as alternative miniprotein
routes; RFantibody is the antibody route. **B**, combine selected arms in tandem
or IgG-like formats; assess the whole construct; produce and characterize it;
and test simultaneous binding, specificity and relevant biological function.
The numbered path runs left to right in panel A and right to left in panel B.
Assay results guide redesign.

Blue and purple denote arm/target specificities A and B; gray is structural
context, linkers or antibody constant regions. Green identifies experimental
assessment. Lobed target surfaces, helices, Fab/VHH and IgG-like glyphs are
schematic. The confidence-matrix motif is illustrative and has no numerical
scale. Both assay curves are illustrative, without measured values or axes
units; neither implies successful binding, monodispersity or functional
activity. The tandem and IgG-like symbols are alternative architectures,
not mandatory sequential intermediates. The VHH glyph has one variable domain;
the Fab glyph has paired variable/constant domains, and the IgG-like symbol
has two differently colored binding arms and a neutral Fc.

## Scientific scope retained from 08_06

This figure condenses the existing workflow, not a new inference campaign or
validated universal protocol. Sources, primary references and detailed
qualifications remain in
[08_06_general_bispecific_design_workflow_legend.md](08_06_general_bispecific_design_workflow_legend.md).

- RFantibody includes antibody-finetuned RFdiffusion, ProteinMPNN and RF2;
  its internal RF2 filtering is not independent validation. BindCraft also
  uses AF2-based design/filtering internally. Reassessment should use a
  separate setup or model family where practical, recognizing shared biases.
- Structural confidence, interface geometry, epitope recovery, controls,
  diversity and developability inform selection. No universal score cutoff
  is proposed. Predictions do not establish binding affinity or specificity.
- Arm-level experimental checks should precede extensive format optimization
  where feasible; exploratory fusion modeling may proceed with an explicit
  confidence gap if those experiments are unavailable.
- Target context includes oligomeric state, glycosylation and membrane
  accessibility where relevant. Counter-targets and positive/negative controls
  remain important even though their long explanations move to this legend.
- IgG-like formats require suitable heavy-chain and, where applicable,
  light-chain pairing. Linker/domain-order engineering is format dependent.
- Whole-construct assessment includes domain folds, interfaces, clashes,
  epitope recovery and dual-target accessibility. A favorable monomer fold
  does not establish simultaneous binding. High inter-domain PAE describes
  uncertain placement, not proven flexibility or separation.
- Production/QC encompasses expression, purification, assembly/heterogeneity
  (e.g. SEC–MALS) and stability measurements (e.g. thermal unfolding). No
  single assay establishes overall developability.
- SPR/BLI must use a configuration explicitly testing simultaneous target
  binding; separate single-target measurements are insufficient. Functional
  assays must match the intended biology.

## Files, reproduction and checks

Prepared 2026-10-21 from `08_06_general_bispecific_design_workflow.png` and its
existing builder/legend. The original is preserved. Direct vector drawing
reuses the project's established `build_visual_workflow_slide.py` and
`08_07_build_visual_overview.py` rendering/OOXML patterns rather than generating
uncontrolled molecular imagery.

- `08_08_visual_bispecific_workflow.png`: 2400 × 1350, 16:9; approximately
  339 dpi at 180 mm width.
- `08_08_visual_bispecific_workflow.pdf`: vector, 180 × 101.25 mm;
  embedded fonts, no raster objects; minimum label size 7.02 pt.
- `08_08_visual_bispecific_workflow_editable.pptx`: editable native text,
  molecular glyphs, paths and illustrative curves; no flattened slide image.
- `08_08_build_visual_bispecific_workflow.py`: self-contained builder using
  existing Pillow, pycairo, Poppler and Liberation Sans; PowerPoint uses Arial.

```bash
python3 alzheimer/bindcraft/fusion/pic_graphs/08_08_build_visual_bispecific_workflow.py
```

Checked PNG decoding, PDF dimensions, embedded fonts/no raster objects,
PowerPoint ZIP/XML and relationships, native editable objects, label size and
visual clarity. Inspected the numbered path, specificity colors, target-facing
epitope patches, alternative formats and experimental qualifiers. Native
PowerPoint application rendering is unavailable. No installation, protein
prediction or assay was performed. Final journal-specific sizing, caption
and artwork rules must be applied for a named submission.
