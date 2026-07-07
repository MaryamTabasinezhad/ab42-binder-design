# Computational Demand & Scaling — AI Protein Binder Design

**Subject:** GPU compute required to design therapeutic protein binders against amyloid-beta (the Alzheimer's target), and how that requirement scales with the number of candidates produced.
**Audience:** compute-grant / cloud-credit reviewers (e.g. NVIDIA Inception and similar programs).
**Prepared:** 2026-07-06. Baseline GPU-hours and candidate counts are taken from job-scheduler accounting (`sacct`) and delivered output files on NVIDIA A100 hardware; derived figures (unit cost, scaling projections) are labelled as such.

---

## 1. Executive summary

We design protein drug candidates entirely on GPUs. Each candidate is a novel 3-D protein structure generated and scored by deep-learning models — there is no non-GPU version of this work.

- **Measured baseline:** producing **62 accepted binder structures** (computationally accepted; not yet wet-lab tested) against amyloid-beta consumed **~324 NVIDIA A100 GPU-hours**.
- **Derived unit cost:** **≈ 5.2 A100 GPU-hours per accepted binder structure.**
- **Scaling is approximately linear in the number of candidates** — the generator is stochastic and its attempts are independent, so producing more candidates takes proportionally more GPU time (with target-dependent caveats, Section 6).

| Target output (accepted binder structures) | GPU-hours (A100) | Wall-clock on 8× A100 | Wall-clock on 32× A100 |
|---:|---:|---:|---:|
| 50  | ~260   | ~1.4 days  | ~8 hours |
| 100 | ~520   | ~2.7 days  | ~16 hours |
| 500 | ~2,600 | ~14 days   | ~3.4 days |
| 1,000 | ~5,200 | ~27 days | ~6.8 days |

The compute requirement is well within the range of a cloud-credit grant, and the workload runs as many independent jobs, so adding GPUs shortens the wall-clock proportionally.

---

## 2. What we compute, and why it is GPU-bound

A "binder" is a small protein designed to stick to a chosen disease target. Designing one from scratch is a sequence of deep-learning steps, each of which is a forward/backward pass on a GPU:

1. **Generative design** — a gradient-based model proposes a candidate protein and refines it so its predicted 3-D shape docks onto the target. This is the dominant cost and the basis of every number in this report.
2. **Structure prediction** — an AlphaFold2-class model predicts the 3-D structure of each candidate to check it folds and binds as intended.
3. **Scoring & filtering** — each candidate is scored on predicted binding confidence and biophysical quality; most are rejected.

Only steps 1–2 use the GPU heavily. Step 3 and all bookkeeping run on CPU in minutes and are a negligible fraction of the compute budget (well under 1%). **The bottleneck is GPU time; more GPU directly converts into more candidate structures.**

---

## 3. Measured baseline (the anchor)

The generative-design stage for the amyloid-beta target was run as two long-running GPU jobs and its resource use recorded by the scheduler. Both jobs produced accepted designs and then terminated at the tail of their run (one hit a memory limit, one was stopped manually) — this is normal for a long-running generator that writes candidates incrementally; it does not affect the candidates already written.

| Quantity | Value | Source |
|---|---|---|
| GPU hardware | NVIDIA A100 (40 GB) | scheduler |
| GPU-hours consumed (generation) | **~324 A100-hours** (265.5 + 58.6 across two runs) | `sacct` measured |
| Accepted structures produced | **62** (50 from the first run, 12 from the second) | delivered output files |
| **Cost per accepted structure** | **≈ 5.2 A100 GPU-hours** | derived (324 ÷ 62) |

The generative model is stochastic: it explores many design attempts and keeps the ones that meet its internal quality bar. Because attempts are independent, total GPU cost is proportional to how many accepted structures you want — which is what makes the scaling in Section 4 approximately linear.

*Note on design attempts:* the generator explored on the order of ~1,300 design trajectories (from its run logs) to yield these 62, i.e. a single-digit-percent acceptance rate. Acceptance for this class of method is strongly **target-dependent** — a second target in this program (Section 5) accepted a much higher fraction — so the "design attempts" figures in Section 4 are indicative, not guaranteed.

---

## 4. Scaling model

**Assumption:** linear scaling at the measured rate of ~5.2 A100 GPU-hours per accepted structure (Section 3), i.e. the same target pushed for more candidates. See Section 6 for where this assumption weakens.

### 4.1 GPU-hours vs. number of structures

| Accepted structures | Design attempts (indicative) | **A100 GPU-hours** |
|---:|---:|---:|
| 50    | ~1,100  | **~260**   |
| 100   | ~2,200  | **~520**   |
| 500   | ~10,900 | **~2,600** |
| 1,000 | ~21,700 | **~5,200** |

*(The "design attempts" column back-outs a ~4.6% acceptance rate from the baseline; actual attempts required scale up if the acceptance rate for a given target is lower, and down if higher.)*

### 4.2 Wall-clock (the same GPU-hours, spread across more GPUs)

The workload runs as many independent design jobs — separate GPUs, no coordination between them — so wall-clock time ≈ GPU-hours ÷ number of GPUs.

| Accepted structures | 1× A100 | 8× A100 | 24× A100 | 64× A100 |
|---:|---:|---:|---:|---:|
| 100   | ~22 days  | ~2.7 days | ~22 hours | ~8 hours |
| 500   | ~108 days | ~14 days  | ~4.5 days | ~1.7 days |
| 1,000 | ~217 days | ~27 days  | ~9 days   | ~3.4 days |

The practical takeaway: **a single GPU is the limiting factor today; a modest cloud allocation (tens of GPUs) turns many months of serial work into days.**

### 4.3 Confirmation-step overhead

Beyond generation, each candidate is typically re-checked with a structure-prediction pass (a few minutes of GPU each). For a batch of candidates this adds roughly a low-double-digit-percent overhead on top of generation. It is a rough estimate (it depends on how many off-target checks are run and on prediction settings), so it is noted for completeness only and is not built into the Section 4.1 totals; it does not change their order of magnitude.

---

## 5. Compute consumed to date

The program has already run at meaningful scale on NVIDIA hardware:

- **Amyloid-beta binder generation:** ~324 A100 GPU-hours → 62 accepted structures (Section 3).
- **A second target:** the same method was also run against a different disease target on **NVIDIA H100** GPUs, producing 380 accepted structures. That run used a different target and quality regime and its recorded hours cover the full workflow rather than generation alone, so we do **not** use it as an A100-vs-H100 hardware benchmark — it is reported only as additional NVIDIA-GPU workload delivered.
- Plus structure-prediction, filtering, and multi-part assembly runs on both A100 and H100.

Every one of these is an NVIDIA GPU workload. The software stack is GPU-native end to end: CUDA, JAX (XLA on GPU), PyTorch, and GPU containers.

*Reconciliation with the pitch deck:* the ~324 A100-hours here is the amyloid-beta **generation subset**. The larger "~1,891 A100-hours on this cluster" figure quoted in the company pitch deck is the **total** consumption on a shared cluster allocation across all of this program's work (generation for both targets, structure-prediction/counter-screen, filtering, and unrelated internal campaigns on the same account). The two are consistent: 324 is a clean, isolated slice; 1,891 is the shared-account total.

---

## 6. What additional compute unlocks

Because cost-per-candidate is measured, a compute grant converts fairly predictably into output:

| Grant size (A100-hours) | Additional accepted structures (approx.) | What it enables |
|---:|---:|---|
| 500   | ~95    | Deepen one target: a broader candidate set |
| 2,500 | ~480   | A full second target end-to-end, or ~5× the current amyloid-beta set |
| 10,000 | ~1,900 | Multiple new disease targets in parallel |
| 25,000–50,000 | ~4,800–9,600 | Platform-scale: many targets, broad candidate exploration |

**Caveat on scaling one target hard:** the linear model describes *expected raw count* of accepted structures. It does **not** promise that every additional candidate is as useful — as a single target is pushed, structural diversity saturates (in this program's second target, one structural family already dominated the top candidates, and a per-family cap had to be applied), and acceptance rate can drift. In practice the compute is best spent across *more targets* rather than exhaustively over-sampling one. Within the ranges above, and especially when spread across targets, the GPU requirement remains the governing constraint.

---

## 7. Methodology & assumptions (for reproducibility)

- **Directly measured:** total generation GPU-hours (from `sacct`: job elapsed time × GPUs allocated, summed over the two amyloid-beta generation jobs) and the accepted-structure count (62 delivered output files). Accounting window: jobs from 2026-05-01 onward; all 62 accepted designs are dated within this window.
- **Derived (not directly measured):** the ~5.2 GPU-hours/structure unit cost (324 ÷ 62), the "design attempts" columns (back-out from an approximate acceptance rate), and the confirmation-step overhead. These are labelled as derived wherever they appear.
- **Linear-scaling assumption** holds for expected raw count because design attempts are statistically independent; it is standard for this class of generative-design workload. Useful-diversity and acceptance-rate caveats are in Section 6.
- **"Runs as many independent jobs"** means each design job occupies one GPU and does not communicate with the others, so N GPUs give ~N× throughput until other limits (storage, scheduling) intervene.
- **CPU cost** (filtering, ranking, assembly, sequence preparation) is minutes-to-an-hour on a few cores per step — omitted from the totals as negligible (<1% of the compute budget).
- All GPU-hours are **actually consumed**, including the tail of runs that ended at a memory limit or were stopped manually — i.e. real allocation used, not an idealized minimum.
