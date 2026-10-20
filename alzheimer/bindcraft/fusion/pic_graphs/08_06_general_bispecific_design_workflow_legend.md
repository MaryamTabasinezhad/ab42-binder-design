# Figure legend — Structure-guided design of bispecific proteins

**Figure X | Proposed general workflow for structure-guided discovery and validation of bispecific proteins.** **a,** Target-specific arm discovery is repeated for each target or epitope. Target definition considers structure, biological state, epitope accessibility and relevant counter-targets. Alternative generation routes include RFdiffusion followed by ProteinMPNN, BindCraft for miniprotein binders, and RFantibody for framework-based antibody or VHH design. Candidate complexes are reassessed using an independent prediction setup where practical, then shortlisted using structural confidence, epitope recovery, developability, controls and sequence/scaffold diversity. Individual-arm binding and specificity should be established experimentally before committing to extensive format optimization when feasible. **b,** Selected arms are combined by sampling arm pairings, linkers, domain order and valency, with format-specific chain-pairing engineering for IgG-like architectures. Whole-construct modeling assesses domain folds, steric compatibility and target accessibility. Expression and purification are followed by biophysical quality control and measurements of individual-target affinity, simultaneous dual binding, specificity and application-dependent function. Experimental results guide further arm or construct redesign. Blue denotes computational design/selection, and green denotes experimental assessment; green text in the arm-selection node identifies the early experimental check. Numbered arrows specify the order, with the lower row read from right to left. This is a proposed methodological schematic, not evidence that all stages have been completed or that any design is experimentally validated.

## Figure notes

**1. Independent complex reassessment.** RFantibody contains antibody-finetuned RFdiffusion, ProteinMPNN and antibody-finetuned RoseTTAFold2 (RF2) prediction/filtering. This RF2 filtering belongs to the generation pipeline and is not an independent validation stage. BindCraft also uses AlphaFold2-based design and filtering internally. A separate complex prediction configuration, model family or withheld validation setup can add evidence, but models can share training data and structural biases: computational agreement is not independent experimental confirmation. Select prediction methods and target context for each modality; no method is guaranteed to work for every target.

**2. Arm-selection checkpoint.** Assess specificity using relevant homologs, alternative target states and negative/nonbinding controls, with suitable positive controls for assay and prediction performance. Where possible, measure the binding of each isolated arm before larger-scale bispecific assembly. Predicted off-target scores alone do not establish specificity, and an unsuccessful positive control makes a computational counter-screen inconclusive. Parallel exploratory fusion modeling can proceed if early arm experiments are unavailable, but the corresponding confidence gap must remain explicit.

**Format-specific steps.** Tandem miniprotein, VHH and scFv constructs typically require linker/domain-order optimization. IgG-like bispecifics additionally require the appropriate heavy-chain heterodimerization and, when applicable, light-chain pairing solution. Fc engineering is not required for every format. Antibody candidates also need framework/CDR compatibility, sequence-liability and human-compatibility assessment. Native glycosylation, oligomeric context and membrane geometry should be considered where relevant.

**Metrics and assays.** Use per-domain structural confidence and interface metrics where applicable, together with clashes, contact geometry, epitope recovery and developability. Define thresholds from the target, modality, controls and validation evidence; no universal pTM, ipTM or PAE cutoff is proposed. High inter-domain PAE indicates uncertain relative placement, not proven flexibility or physical separation. Computational scores do not measure affinity. SPR/BLI experiments for simultaneous binding require an assay configuration that explicitly tests both targets; measuring each target separately is insufficient. SEC–MALS assesses size/assembly and heterogeneity, and DSF assesses thermal unfolding behavior under the chosen conditions. Neither alone establishes developability. Functional assays depend on the intended biology, such as signaling, receptor internalization, transport or cell engagement.

## Abbreviations

- **BLI:** biolayer interferometry.
- **CDR:** complementarity-determining region.
- **DSF:** differential scanning fluorimetry.
- **Fc:** fragment crystallizable region of an immunoglobulin.
- **IgG:** immunoglobulin G.
- **ipTM:** predicted interface TM-score.
- **PAE:** predicted aligned error.
- **pLDDT:** predicted local distance difference test score.
- **ProteinMPNN:** protein message-passing neural network.
- **pTM:** predicted TM-score.
- **QC:** quality control.
- **RF2:** RoseTTAFold2.
- **scFv:** single-chain variable fragment.
- **SEC–MALS:** size-exclusion chromatography coupled to multi-angle light scattering.
- **SPR:** surface plasmon resonance.
- **VHH:** single variable domain of a heavy-chain-only antibody.

## Primary references

1. *De novo design of protein structure and function with RFdiffusion.* Nature (2023). [doi:10.1038/s41586-023-06415-8](https://doi.org/10.1038/s41586-023-06415-8).
2. *Robust deep learning–based protein sequence design using ProteinMPNN.* Science (2022). [doi:10.1126/science.add2187](https://doi.org/10.1126/science.add2187).
3. *One-shot design of functional protein binders with BindCraft.* Nature (2025). [doi:10.1038/s41586-025-09429-6](https://doi.org/10.1038/s41586-025-09429-6).
4. *Atomically accurate de novo design of antibodies with RFdiffusion.* Nature. [doi:10.1038/s41586-025-09721-5](https://doi.org/10.1038/s41586-025-09721-5). [RFantibody pipeline documentation](https://github.com/RosettaCommons/RFantibody).
5. *Accurate structure prediction of biomolecular interactions with AlphaFold 3.* Nature (2024). [doi:10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w).
6. *ColabFold: making protein folding accessible to all.* Nature Methods (2022). [doi:10.1038/s41592-022-01488-1](https://doi.org/10.1038/s41592-022-01488-1).

Model descriptions and reference links checked 2026-10-20. This general workflow is an original synthesis adapted from the organizational intent of the two supplied project charts, not a reproduction of a model paper's figure. Each primary citation supports its method; the complete proposed bispecific pipeline is not presented as a published, experimentally validated protocol.

## Export and verification

- **Editable PPTX:** `08_06_general_bispecific_design_workflow_editable.pptx`; one 16:9 slide, native editable text, vector boxes and connectors; no flattened slide image.
- **PNG:** `08_06_general_bispecific_design_workflow.png`; 2400 × 1350 pixels, metadata set to 180 mm print width (approximately 339 dpi).
- **Vector PDF:** `08_06_general_bispecific_design_workflow.pdf`; 180 × 101.25 mm, embedded/subset fonts, no raster images. Labels are at least 7.02 pt at this size. This full-width layout should not be reduced to a narrow single column without re-layout.
- **Builder:** `build_visual_workflow_slide.py`; uses existing Pillow, pycairo and Liberation Sans, without installing software.
- Verified XML/package structure and native editable content; rendered and visually inspected PNG and PDF. Checked the PDF with `pdfinfo`, `pdffonts` and `pdfimages -list` for dimensions, embedded fonts and absence of raster images. Native PowerPoint rendering is not available on this host.
- Final adaptation to a named journal's font, dimensions, color, raster-resolution and accessibility requirements remains a submission-stage step. The figure legend should be adapted to the manuscript and the stages actually executed.

Temporary PDF inspection preview: `/tmp/bispecific_publication_pdf_preview.png`, produced with `pdftoppm -scale-to 1600 -singlefile -png alzheimer/bindcraft/fusion/pic_graphs/08_06_general_bispecific_design_workflow.pdf /tmp/bispecific_publication_pdf_preview`. Durable figure files, this legend and the builder reside in the tracked project directory. No protein inference jobs were run.
