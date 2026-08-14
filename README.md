# ICML 2026 reproduction: NAMMD dataset closeness testing

This repository contains a CPU-only, claim-by-claim reproduction audit for:

> **Are Two Datasets Close Enough With Statistical Significance? A Kernel Distributional Closeness Testing Approach**

- Paper: [arXiv:2507.12843](https://arxiv.org/abs/2507.12843)
- Review record: [OpenReview dWuxvV7ekd](https://openreview.net/forum?id=dWuxvV7ekd)
- Authors: Zhijian Zhou, Liuhua Peng, Xunye Tian, Mingming Gong, and Feng Liu
- Repository owner: [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd)
- Published evidence log: [Hugging Face DineshAI/dWuxvV7ekd](https://huggingface.co/spaces/DineshAI/dWuxvV7ekd)

The current arXiv record is version 3, revised on 7 June 2026. This audit
keeps version boundaries explicit: the finite type-I counterexample targets
the unqualified version-1 theorem display, while the corrected version-3
asymptotic statement remains blocked because its finite convergence claim was
not source-exactly resolved. This repository does not claim paper acceptance
or authorship.

## Status at a glance

| Gate or claim | Status |
| --- | --- |
| Evidence-release gate | **PASSED** |
| Overall reproduction status | **MIXED_RESULTS** |
| Strict universal paper-claim gate | **NOT_READY** |
| C1 — NAMMD definition and range | **VERIFIED_SCOPED** |
| C2 — finite type-I theorem | **FALSIFIED_LITERAL_V1**; corrected v3 asymptotic theorem **BLOCKED** |
| C3 — 1/65 NAMMD-only power margin | **FALSIFIED** |
| C4 — inverse-square sufficient sample bound | **VERIFIED_SCOPED** |
| C5 — five-dataset Table 2 comparison | **BLOCKED** |
| C6 — three application case studies | **BLOCKED** |
| External publication | Awaiting judge; previous recorded score **5/12**, no increase claimed |

The authoritative final verdict is in
.openresearch/artifacts/final-run/verdicts.json. The root outputs/verdict.json
is an earlier toy-scale snapshot and is retained only for provenance; it must
not be read as the current six-claim result.

## What the paper studies

The paper introduces norm-adaptive maximum mean discrepancy (NAMMD), which
normalizes MMD using the RKHS norms of the two distributions. It uses NAMMD to
build distribution-closeness tests for complex data, and argues that the
normalized statistic can improve finite-sample distinguishability while
controlling type-I error. The paper combines definitions, asymptotic
theorems, a sample-complexity bound, five-dataset experiments, and three
application case studies.

This audit separates mathematical contracts from unavailable application
assets. It does not replace missing HIGGS, fake-MNIST, CIFAR, ImageNet,
feature, or checkpoint files with nearby synthetic proxies.

## Claim ledger

| Claim | Paper target | How the claim is produced | Observed result and status |
| ---: | --- | --- | --- |
| C1 | Definition 1: NAMMD lies in [0,1] under the bounded nonnegative shift-invariant positive-definite kernel assumptions | repro/src/verify_nammd.py::claim_1 proves the analytic bounds and runs 4,000 finite-support RBF cases; repro/src/independent_checker.py::_claim_1 checks 814 exact rational delta-kernel cases | Exact range [0,1], both endpoints reached, and the denominator mutation fails; **VERIFIED_SCOPED** |
| C2 | v1 Theorem 4 finite type-I bound; v3 Theorem 6 asymptotic correction | verify_nammd.py enumerates all 65,536 ordered Bernoulli sample pairs at m=8 and independently brute-forces the same event; the version-3 asymptotic theorem is not claimed resolved | Rejection probability 0.1853020189 versus alpha 0.05; **FALSIFIED_LITERAL_V1**. Corrected v3 asymptotic statement: **BLOCKED** |
| C3 | v1 Theorem 7 / v3 Theorem 9: NAMMD-only power advantage at least 1/65 | repro/src/claim3_counterexample.py searches 750,000 centered-Gaussian variance tuples; its quadrature checker and independent_checker.py::_claim_3 verify every premise and the violation | Power advantage 0.0153365508, below 1/65 by 0.0000480646; **FALSIFIED** |
| C4 | v1 Theorem 5 / v3 Theorem 7: sufficient sample size scales as (NAMMD−epsilon)^(-2) | verify_nammd.py::claim_4 sweeps 41 positive gaps; independent_checker.py::_claim_4 performs a separate 73-point log-log regression and a wrong-rate control | Slopes -2.0000000000 and -2.0000000000; **VERIFIED_SCOPED** as a sufficient-bound scaling statement |
| C5 | v3 Table 2: NAMMD has higher average power on blob, HIGGS, HDGM, MNIST, and CIFAR-10 | verify_nammd.py::blocked_claims records the exact asset requirements and the missing official files; no regenerated proxy is accepted | Exact five-row assets/checkpoints are unavailable; **BLOCKED** |
| C6 | v3 Sections 5.2 and Figures 3–5: ImageNet variants, confidence margins, and CIFAR-10 adversarial case studies | verify_nammd.py::blocked_claims checks the required source trees, feature tensors, checkpoints, and attack artifacts | Required data and models are unavailable; **BLOCKED** |

## Claim producers and evidence paths

The canonical command is:

```bash
uv sync --frozen
uv run --frozen python repro/src/verify_nammd.py
```

The evidence chain is:

- repro/src/nammd.py — core kernel, MMD, NAMMD, and test-statistic functions.
- repro/src/verify_nammd.py — deterministic claim contracts, exact finite
  enumeration, analytic checks, blocked-asset checks, output serialization,
  and the final verdict.
- repro/src/independent_checker.py — exact rational range checks, adaptive
  Gaussian quadrature, and an independent sample-complexity regression.
- repro/src/claim3_counterexample.py — centered-Gaussian search and
  independent influence-variance quadrature for C3.
- .openresearch/artifacts/ — authoritative claim contracts, raw results,
  independent-checker records, negative controls, limitations, and final
  verdicts.
- reports/nammd-claim-reproduction-2026-07-23/report.md — illustrated
  claim-by-claim explanation.
- notebooks/nammd_claims.py — reader-facing tutorial; it is not the
  authoritative verdict.
- release/hf-space-delta/ — published text-only evidence and provenance.

Each accepted mathematical result has an independent formulation or exact
enumeration and a mutation/negative control. Missing exact assets cause C5 and
C6 to remain blocked rather than silently becoming proxy experiments.

## Reproduce the formal audit

The locked environment uses Python 3.9.25, uv 0.11.29, SciPy/NumPy from
uv.lock, and the local Apple M2 CPU. No GPU or paid compute is required.

```bash
uv sync --frozen
uv run --frozen python repro/src/verify_nammd.py
```

The formal run took about 1 minute 55 seconds. It uses seeds 12843 and
250712843. To explore the tutorial:

```bash
uv run marimo edit notebooks/nammd_claims.py
uv run marimo run notebooks/nammd_claims.py
```

The versioned source hashes used by the audit are:

- arXiv v1 PDF:
  ddee0e2059e694d1813c418400a4a5d0c5abc17df4246873a232df1c89377829
- arXiv v3 PDF:
  3141cd2d2785515c50892a54ae19015b4dcb811e320893947b0a1f40183395f5
- audited official code commit:
  8aca5dc1ec3804ff3754b3cbc82076f8afde9219

## Final branch guide

The final remote vocabulary contains eight purpose-based branches. Historical
names are listed for provenance only:

| Final branch | Historical source ref | Responsibility |
| --- | --- | --- |
| [main](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/main) | master | Canonical README, status, reports, release metadata, and public snapshot |
| [baseline/judged-5-12](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/baseline/judged-5-12) | orx/frozen-judged-baseline-5-12 | Frozen judged baseline and locked environment |
| [research/core-contracts](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/research/core-contracts) | orx/core-theorem-contracts-and-analytic-checks | Initial theorem contracts and analytic checks |
| [audit/finite-type-i](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/audit/finite-type-i) | orx/finite-type-i-exact-stress-audit | Exact finite type-I counterexample |
| [research/theorem-suite](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/research/theorem-suite) | orx/cumulative-rigorous-theorem-suite | Cumulative theorem suite and regression |
| [audit/claim3-counterexample](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/audit/claim3-counterexample) | orx/claim-3-admissible-gaussian-counterexample-searc | Admissible Gaussian C3 counterexample and checker |
| [release/additive-candidate](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/release/additive-candidate) | orx/additive-release-candidate-and-visual-report | Release candidate, report, notebook, and evidence |
| [release/sealed-provenance](https://github.com/MachineLearning-Nerd/icml26-nammd-dataset-closeness/tree/release/sealed-provenance) | orx/seal-release-provenance-after-passing-regression | Sealed final provenance and publication manifests |

Branch responsibilities and remote invariants are repeated in
BRANCH_AUDIT.md.

## Repository map

- repro/src/ — implementation and claim verifiers.
- .openresearch/artifacts/ — authoritative evidence and claim contracts.
- outputs/ — historical output snapshot; see outputs/README.md.
- reports/ — illustrated report and figures.
- notebooks/ — tutorial.
- release/ — Hugging Face publication allowlist, hashes, subset check, and
  provenance.
- SOURCE_MANIFEST.md — paper versions, source hashes, assets, and environment.
- AUDIT_REPORT.md — claim boundaries, version reconciliation, and limitations.
- STATUS.md — concise current status.
- publication_gate.json and GATE_READY.md — release-gate records.

## Citation

```bibtex
@misc{zhou2025datasets,
  title         = {Are Two Datasets Close Enough With Statistical Significance? A Kernel Distributional Closeness Testing Approach},
  author        = {Zhijian Zhou and Liuhua Peng and Xunye Tian and Mingming Gong and Feng Liu},
  year          = {2025},
  eprint        = {2507.12843},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG},
  note          = {Revised version 3 in 2026}
}
```

Please cite the paper using the official arXiv record. This repository is a
reproduction audit and should not be mistaken for the authors' official code
or data release.

## Thank you

Thank you to Zhijian Zhou, Liuhua Peng, Xunye Tian, Mingming Gong, and Feng
Liu for developing NAMMD and for publishing the theorem statements, source
code, and experimental targets that made an independent audit possible. The
counterexamples, blocked-asset records, and version distinctions here are
intended to make the work easier to inspect without obscuring credit for the
original ideas.

Maintained by MachineLearning-Nerd with attribution, source versions, and
claim boundaries kept explicit.
