# NAMMD claim-by-claim reproduction candidate

This repository contains a CPU-only reproduction of
[Are Two Datasets Close Enough With Statistical Significance?](https://arxiv.org/abs/2507.12843).
The strongest result is not a benchmark score: exact and analytic checks
resolve the paper’s first four mathematical claims, including counterexamples
to the unqualified finite type-I statement in arXiv v1 and to Theorem 7/9’s
`1/65` power-margin conclusion.

| Claim | Paper result | Observed result | Assessment |
|---|---:|---:|---|
| NAMMD bound | `0 <= NAMMD <= 1` | analytic proof; exact range `[0,1]` | VERIFIED |
| v1 finite type-I | error `<= 0.05` | exact error `0.1853020189` at `m=8` | FALSIFIED |
| Theorem 7/9 margin | advantage `>= 1/65 = 0.0153846154` | `0.0153365508` with every premise satisfied | FALSIFIED |
| sample scaling | exponent `-2` | slopes `-2.0000000000` and `-2.0000000000` | VERIFIED |
| five-dataset Table 2 | NAMMD average power higher | exact assets absent | BLOCKED |
| three case studies | all three applications | exact ImageNet/CIFAR assets absent | BLOCKED |

The theorem checks are full-contract checks, not downscaled proxies. The two
empirical claims remain blocked rather than being replaced by synthetic data.
All runs used the local Apple M2 CPU, one locked repository `.venv`, and cost
`$0`; Hugging Face CPU was not needed.

[Read the illustrated report](reports/nammd-claim-reproduction-2026-07-23/report.md) ·
[Open the tutorial notebook](notebooks/nammd_claims.py) ·
[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-dWuxvV7ekd-nammd-dataset-closeness/blob/master/notebooks/nammd_claims.py)

## Experiment log

The run command below is copied verbatim from every `orx exp status`.

| Branch / experiment | Purpose | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`orx/frozen-judged-baseline-5-12`](https://github.com/MachineLearning-Nerd/icml26-repro-dWuxvV7ekd-nammd-dataset-closeness/tree/orx/frozen-judged-baseline-5-12) | Freeze and reproduce the judged toy baseline | `uv run --frozen python repro/src/verify_nammd.py` | Reproduced judged toy metrics; no new full credit | local Apple M2 CPU |
| [`orx/finite-type-i-exact-stress-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-dWuxvV7ekd-nammd-dataset-closeness/tree/orx/finite-type-i-exact-stress-audit) | Exact finite Claim 2 audit | `uv run --frozen python repro/src/verify_nammd.py` | v1 finite statement FALSIFIED | local Apple M2 CPU |
| [`orx/cumulative-rigorous-theorem-suite`](https://github.com/MachineLearning-Nerd/icml26-repro-dWuxvV7ekd-nammd-dataset-closeness/tree/orx/cumulative-rigorous-theorem-suite) | Merge and regress Claims 1–4 | `uv run --frozen python repro/src/verify_nammd.py` | Claims 1/4 verified; Claim 3 proof gap isolated | local Apple M2 CPU |
| [`orx/claim-3-admissible-gaussian-counterexample-searc`](https://github.com/MachineLearning-Nerd/icml26-repro-dWuxvV7ekd-nammd-dataset-closeness/tree/orx/claim-3-admissible-gaussian-counterexample-searc) | Construct and independently check Claim 3 counterexample | `uv run --frozen python repro/src/verify_nammd.py` | Claim 3 FALSIFIED; cumulative suite passes | local Apple M2 CPU |
| [`orx/additive-release-candidate-and-visual-report`](https://github.com/MachineLearning-Nerd/icml26-repro-dWuxvV7ekd-nammd-dataset-closeness/tree/orx/additive-release-candidate-and-visual-report) | Add durable evidence, report, notebook, and additive Space candidate | `uv run --frozen python repro/src/verify_nammd.py` | Release regression passes at `6c13dd2` | local Apple M2 CPU |
| [`orx/seal-release-provenance-after-passing-regression`](https://github.com/MachineLearning-Nerd/icml26-repro-dWuxvV7ekd-nammd-dataset-closeness/tree/orx/seal-release-provenance-after-passing-regression) | Seal completed release-run provenance and manifests | `uv run --frozen python repro/src/verify_nammd.py` | Cumulative release gate passes | local Apple M2 CPU |
| `master` | Publication surface | Not run as an experiment (publication surface) | Awaiting explicit release approval | — |

## Reproduce

```bash
uv sync --frozen
uv run --frozen python repro/src/verify_nammd.py
```

The formal evidence command must normally be launched through OpenResearch on
the relevant experiment node. To explore the tutorial locally:

```bash
uv run marimo edit notebooks/nammd_claims.py
uv run marimo run notebooks/nammd_claims.py
```

The prior upstream README consisted only of the project title; the section
above is the project-specific public landing page.
