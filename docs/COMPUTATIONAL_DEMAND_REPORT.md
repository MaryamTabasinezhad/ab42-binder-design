# Computational Demand & Scaling — AI Protein Binder Design

**Subject:** GPU compute required to design therapeutic protein binders against amyloid-beta (the Alzheimer's target), and how that requirement scales with the number of candidates produced.
**Audience:** compute-grant / cloud-credit reviewers (e.g. NVIDIA Inception and similar programs).
**Prepared:** 2026-07-06. All baseline figures are measured from job-scheduler accounting (`sacct`) on NVIDIA A100 hardware, not estimated.

---

## 1. Executive summary

We design protein drug candidates entirely on GPUs. Each candidate is a novel 3-D protein structure generated and scored by deep-learning models — there is no non-GPU version of this work.

- **Measured baseline:** producing **62 validated binder structures** against amyloid-beta consumed **~325 NVIDIA A100 GPU-hours**.
- **Unit cost:** **≈ 5.2 A100 GPU-hours per accepted binder structure.**
- **Scaling is essentially linear** — the generator is stochastic, so producing 2× the candidates takes ≈ 2× the GPU time.

| Target output (accepted binder structures) | GPU-hours (A100) | Wall-clock on 8× A100 | Wall-clock on 32× A100 |
|---:|---:|---:|---:|
| 50  | ~260   | ~1.4 days  | ~8 hours |
| 100 | ~520   | ~2.7 days  | ~16 hours |
| 500 | ~2,600 | ~14 days   | ~3.4 days |
| 1,000 | ~5,200 | ~27 days | ~6.8 days |

The compute requirement is well within the range of a cloud-credit grant, and the workload is embarrassingly parallel: adding GPUs shortens the wall-clock proportionally.

---

## 2. What we compute, and why it is GPU-bound

A "binder" is a small protein designed to stick to a chosen disease target. Designing one from scratch is a sequence of deep-learning steps, each of which is a forward/backward pass on a GPU:

1. **Generative design** — a diffusion/gradient model proposes a candidate protein and refines it so its predicted 3-D shape docks onto the target. This is the dominant cost.
2. **Structure prediction** — an AlphaFold2-class model predicts the 3-D structure of each candidate to confirm it folds and binds as intended.
3. **Scoring & filtering** — each candidate is scored on predicted binding confidence and biophysical quality; most are rejected.

Only steps 1–2 use the GPU heavily. Step 3 and all bookkeeping run on CPU in minutes and are a negligible fraction of the compute budget (well under 1%). **The bottleneck is GPU time; more GPU directly converts into more validated candidates.**

---

## 3. Measured baseline (the anchor)

The generative-design stage for the amyloid-beta target was run to completion and its resource use recorded by the scheduler:

| Quantity | Measured value |
|---|---|
| GPU hardware | NVIDIA A100 (40 GB) |
| GPU-hours consumed (generation) | **325 A100-hours** |
| Design attempts explored ("trajectories") | 1,342 |
| Candidates that passed the model's internal acceptance | **62 accepted structures** |
| Effective acceptance rate | ~4.6% of attempts |
| **Cost per accepted structure** | **≈ 5.2 A100 GPU-hours** |

The generative model is stochastic: it explores many attempts and keeps the ones that meet its quality bar. Because attempts are independent, the total GPU cost is proportional to how many accepted structures you want — which is what makes the scaling below linear and predictable.

*Cross-check on newer hardware:* the same method run against a second target on **NVIDIA H100** GPUs produced 380 accepted structures for ~1,100 H100-hours (≈ 2.9 H100-hours each) — roughly **1.8× faster per structure than A100**, consistent with H100's throughput advantage. Access to H100-class hardware therefore reduces the numbers below.

---

## 4. Scaling model

**Assumption:** linear scaling at the measured rate of 5.2 A100 GPU-hours per accepted structure (Section 3). This is conservative — it does not credit the ~1.8× speed-up available on H100.

### 4.1 GPU-hours vs. number of structures

| Accepted structures | Design attempts (~) | **A100 GPU-hours** | Equivalent H100 GPU-hours (~) |
|---:|---:|---:|---:|
| 50    | ~1,100  | **~260**   | ~145 |
| 100   | ~2,200  | **~520**   | ~290 |
| 500   | ~10,900 | **~2,600** | ~1,450 |
| 1,000 | ~21,700 | **~5,200** | ~2,900 |

### 4.2 Wall-clock (the same GPU-hours, spread across more GPUs)

The workload is embarrassingly parallel — independent design jobs run on separate GPUs with no coordination. Wall-clock time = GPU-hours ÷ number of GPUs.

| Accepted structures | 1× A100 | 8× A100 | 24× A100 | 64× A100 |
|---:|---:|---:|---:|---:|
| 100   | ~22 days  | ~2.7 days | ~22 hours | ~8 hours |
| 500   | ~108 days | ~14 days  | ~4.5 days | ~1.7 days |
| 1,000 | ~217 days | ~27 days  | ~9 days   | ~3.4 days |

The practical takeaway: **a single GPU is the limiting factor today; a modest cloud allocation (tens of GPUs) turns a year of serial work into days.**

### 4.3 Full-pipeline overhead

Adding the confirmation step (structure prediction of each accepted candidate against the target and a panel of related off-targets) costs roughly **0.6–0.7 additional GPU-hours per candidate** at ~4 minutes per structure prediction. This raises the fully-validated cost to **≈ 6 A100 GPU-hours per candidate** — about a 12% overhead on top of generation. It is included here for completeness; it does not change the order of magnitude.

---

## 5. Compute consumed to date

The program has already run at meaningful scale on NVIDIA hardware:

- **Amyloid-beta binder generation:** ~325 A100 GPU-hours → 62 accepted structures (Section 3).
- **Second-target binder generation:** ~1,100 H100 GPU-hours → 380 accepted structures.
- Plus structure-prediction, filtering, and multi-part assembly runs on both A100 and H100.

Every one of these is an NVIDIA GPU workload (A100 and H100). The program is GPU-native from end to end: the software stack is CUDA, JAX (XLA on GPU), PyTorch, and GPU containers.

---

## 6. What additional compute unlocks

Because cost-per-candidate is fixed and measured, a compute grant converts directly and predictably into output:

| Grant size (A100-hours) | Additional accepted structures (~) | What it enables |
|---:|---:|---|
| 500   | ~95    | Deepen one target: a broader, higher-quality candidate set |
| 2,500 | ~480   | A full second target end-to-end, or 5× the current amyloid-beta set |
| 10,000 | ~1,900 | Multiple new disease targets in parallel |
| 25,000–50,000 | ~4,800–9,600 | Platform-scale: many targets, exhaustive candidate exploration |

There is no diminishing return within this range: the generator keeps finding new valid structures as long as GPUs are available.

---

## 7. Methodology & assumptions (for reproducibility)

- **Source of baseline numbers:** the compute cluster's own job accounting (`sacct`): GPU-hours = job elapsed time × number of GPUs allocated, summed over the generation jobs for the amyloid-beta target. Hardware and allocations are recorded per job.
- **Unit cost** = measured generation GPU-hours (325) ÷ accepted structures (62) = 5.2 A100 GPU-hours each.
- **"Design attempts" columns** back out the number of raw attempts from the measured ~4.6% acceptance rate; actual acceptance varies with target difficulty and quality thresholds, so treat these as indicative.
- **Linear-scaling assumption** holds because design attempts are statistically independent; it is standard for this class of generative-design workload.
- **CPU cost** (filtering, ranking, assembly, sequence preparation) is minutes-to-an-hour on a few cores per step — omitted from the totals as negligible (<1% of the compute budget).
- **H100 comparison** is a measured second data point on a different target; treat the 1.8× speed-up as approximate, not a controlled benchmark.
- All figures are **GPU-hours actually consumed**, including runs that were later superseded — i.e. real allocation burned, not idealized minimums.
