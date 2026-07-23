# Rigorous claim verdicts — 2026-07-23

This additive campaign supersedes the *assessment* of the earlier toy checks
without deleting their pages. Every old page remains reachable as historical
evidence. No live-judge score change is claimed.

| Claim | Verdict | Direct evidence |
|---|---|---|
| 1. NAMMD range and normalisation | **VERIFIED** | analytic bound; 4,000 RBF cases; 814 exact rational cases; denominator mutation fails |
| 2. type-I error | **FALSIFIED** for the unqualified finite arXiv v1 statement | exact boundary-null enumeration gives `0.1853020189 > 0.05` at `m=8`; v3 asymptotic claim remains blocked |
| 3. MMD-to-NAMMD implication and `1/65` margin | **FALSIFIED** | centered-Gaussian counterexample satisfies every premise but gives `0.0153365508 < 1/65` |
| 4. inverse-square sample bound | **VERIFIED** | direct 41-point slope `-2`; independent 73-point slope `-2`, `R²=1`; inverse-linear mutation gives `-1` |
| 5. five-dataset Table 2 | **BLOCKED** | official code omits exact HIGGS, generated image arrays, and checkpoints |
| 6. three case studies | **BLOCKED** | official code omits exact ImageNet/CIFAR feature and model artifacts and hard-codes local/CUDA paths |

## Scope notes

- Claim 2 does **not** falsify the corrected arXiv v3 asymptotic theorem.
- Claim 3 does **not** say the paper's Example 2 fails; that example passes.
  The theorem is false because another admissible tuple violates its quantified
  conclusion.
- Claims 5 and 6 are not converted to passes with Gaussian or regenerated
  substitutes.
- All formal runs used local Apple M2 CPU, no GPU, and no paid compute.
