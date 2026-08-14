# Branch audit

## Final branch vocabulary

The intended final remote contains eight purpose-based branches:

| Final branch | Historical source ref | Responsibility |
| --- | --- | --- |
| main | master | Canonical README, status, reports, release metadata, and public snapshot |
| baseline/judged-5-12 | orx/frozen-judged-baseline-5-12 | Frozen judged baseline and locked environment |
| research/core-contracts | orx/core-theorem-contracts-and-analytic-checks | Initial theorem contracts and analytic checks |
| audit/finite-type-i | orx/finite-type-i-exact-stress-audit | Exact finite type-I counterexample |
| research/theorem-suite | orx/cumulative-rigorous-theorem-suite | Cumulative theorem suite and regression |
| audit/claim3-counterexample | orx/claim-3-admissible-gaussian-counterexample-searc | Admissible Gaussian C3 counterexample and checker |
| release/additive-candidate | orx/additive-release-candidate-and-visual-report | Release candidate, report, notebook, and evidence |
| release/sealed-provenance | orx/seal-release-provenance-after-passing-regression | Sealed final provenance and publication manifests |

Historical names are retained only for provenance and are not intended to
remain as public remote refs.

## Identity policy

All approved commits use:

```text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
```

No co-author or tool-signature lines are added. History normalization covers
every commit reachable from the eight final branches.

## Required remote invariants

- Owner: MachineLearning-Nerd
- Repository: icml26-nammd-dataset-closeness
- Default branch: main
- Public branch count: 8
- Legacy refs absent: master and all orx/* refs
- README, STATUS.md, SOURCE_MANIFEST.md, AUDIT_REPORT.md,
  publication_gate.json, and BRANCH_AUDIT.md are present on main
- Every final branch is pushed and readable

Remote verification is recorded here after the rename and final push.

## Remote verification

Verified on 2026-08-14 against the GitHub remote:

- HEAD points to main
- git ls-remote --heads origin returns exactly eight branches
- master and every orx/* ref are absent
- All reachable commit authors and committers are
  MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
- GitHub metadata reports owner MachineLearning-Nerd, default branch main,
  the target repository name, and the canonical arXiv homepage
