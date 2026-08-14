# Source manifest

This manifest fixes the paper versions, code, data, and environment used by
the NAMMD audit.

## Paper versions

- Title: *Are Two Datasets Close Enough With Statistical Significance? A
  Kernel Distributional Closeness Testing Approach*
- Authors: Zhijian Zhou, Liuhua Peng, Xunye Tian, Mingming Gong, and Feng Liu
- Current arXiv record: [2507.12843](https://arxiv.org/abs/2507.12843), v3
- Review identifier: [dWuxvV7ekd](https://openreview.net/forum?id=dWuxvV7ekd)
- v1 source hash used for the finite theorem audit:
  ddee0e2059e694d1813c418400a4a5d0c5abc17df4246873a232df1c89377829
- v3 source hash used for the current theorem and experiment audit:
  3141cd2d2785515c50892a54ae19015b4dcb811e320893947b0a1f40183395f5
- Metadata checked: 2026-08-14

Version distinction is essential. C2 falsifies the unqualified finite v1
display, while the corrected v3 asymptotic statement remains blocked. C3
targets the theorem's 1/65 margin in both version numberings.

## Official code

The official code was audited at commit
8aca5dc1ec3804ff3754b3cbc82076f8afde9219. The exact asset inventory at that
source did not include all data products, trained checkpoints, or generated
feature arrays needed for Table 2 and the three case studies.

## Claim source map

- C1: Definition 1 and the NAMMD formula.
- C2: v1 Theorem 4 and v3 Theorem 6.
- C3: v1 Theorem 7 / Appendix D.4 and v3 Theorem 9 / Appendix C.6.
- C4: v1 Theorem 5 and v3 Theorem 7.
- C5: v3 Section 6.1 and Table 2.
- C6: v3 Section 5.2 and Figures 3–5.

## Code and evidence

- Core metric: repro/src/nammd.py
- End-to-end producer: repro/src/verify_nammd.py
- Independent checker: repro/src/independent_checker.py
- C3 search/checker: repro/src/claim3_counterexample.py
- Authoritative claim evidence: .openresearch/artifacts/
- Published text-only evidence: release/hf-space-delta/
- Human report: reports/nammd-claim-reproduction-2026-07-23/report.md

## Environment

- Command: uv run --frozen python repro/src/verify_nammd.py
- Python: 3.9.25
- uv: 0.11.29
- Lockfile: uv.lock
- Compute: local Apple M2 CPU, eight cores, no GPU
- Seeds: 12843 and 250712843
- Cost: 0 USD

The exact missing assets are recorded in the claim-5 and claim-6 raw
artifacts. Regenerated images, substitute feature tensors, or nearby Gaussian
proxies cannot establish the paper's named empirical claims.
