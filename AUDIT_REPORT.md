# Reproduction audit report

## Executive assessment

The final evidence package is MIXED_RESULTS:

- C1 is VERIFIED_SCOPED under the bounded nonnegative shift-invariant
  positive-definite kernel assumptions.
- C2 is FALSIFIED for the unqualified finite v1 theorem display. The corrected
  v3 asymptotic theorem remains BLOCKED.
- C3 is FALSIFIED by an independently checked, assumption-satisfying
  centered-Gaussian counterexample.
- C4 is VERIFIED_SCOPED as the inverse-square scaling of a sufficient bound.
- C5 and C6 are BLOCKED because the exact named datasets, features,
  checkpoints, and generated artifacts are unavailable.
- The evidence-release gate is PASSED; the strict universal paper-claim gate
  is NOT_READY.

The historical root output once reported 6/6 aligned on toy inputs. The
authoritative final run supersedes that label with two verified claims, two
falsified theorem targets, and two blocked empirical targets.

## Claim-to-evidence map

| Claim | Evidence producer | Independent or blocking check | Result |
| ---: | --- | --- | --- |
| C1 | verify_nammd.py::claim_1 | independent_checker.py::_claim_1 exact rational enumeration and denominator mutation | VERIFIED_SCOPED |
| C2 | verify_nammd.py exact finite audit | ordered-state enumeration, brute-force enumeration, and median-threshold negative control | FALSIFIED_LITERAL_V1; v3 asymptotic BLOCKED |
| C3 | claim3_counterexample.py and verify_nammd.py::claim_3 | adaptive Gaussian quadrature, premise checks, and failed 1/65 margin | FALSIFIED |
| C4 | verify_nammd.py::claim_4 | independent 73-point regression and inverse-linear mutation | VERIFIED_SCOPED |
| C5 | verify_nammd.py::blocked_claims | exact five-dataset asset inventory | BLOCKED |
| C6 | verify_nammd.py::blocked_claims | exact case-study data/checkpoint inventory | BLOCKED |

## Resolved mathematical claims

### C1 — NAMMD range

The audit proves the numerator is at most 2K and the denominator is at least
2K under the paper's bounded nonnegative kernel assumptions. Exact rational
delta-kernel enumeration reaches both 0 and 1, while 4,000 finite-support RBF
cases remain in range. A denominator mutation produces the intended failure.

### C2 — finite type-I statement

For Bernoulli P(1)=0.1 and Q(1)=0.9, the triangular kernel, m=8, and the
boundary epsilon=0.5423728814, all 65,536 ordered sample pairs are enumerated.
The exact rejection probability is 0.1853020188851843, versus alpha=0.05.
Independent brute force agrees to zero absolute error. Replacing the 95th
percentile with the median raises rejection to 0.5147278302.

This falsifies only the unqualified finite statement displayed in v1. The
corrected v3 theorem is asymptotic and is not silently treated as falsified by
the finite counterexample.

### C3 — 1/65 power margin

The search found a centered-Gaussian tuple satisfying both alternatives, the
same-kernel requirement, strict norm ordering, delta in (0, 1/2), and integer
m in the theorem window. The power advantage is 0.015336550797452, below
1/65 by 0.00004806458716. Independent quadrature reproduces the influence
variance and violation at the reported numerical precision.

### C4 — sample scaling

For 41 positive gaps, m times gap squared is constant to 1.42e-14 and the
log-log slope is -1.9999999999999996. An independent 73-point regression
returns -2.0000000000000004 with R-squared 1. The inverse-linear mutation
returns slope -1.0000000000000004. This verifies the stated sufficient-bound
scaling, not necessity or tightness.

## Blocked empirical claims

### C5 — Table 2

The exact comparison requires blob, HIGGS, HDGM, MNIST, and CIFAR-10 rows at
all reported epsilon values. Missing assets include HIGGS_TST.pckl, generated
fake-MNIST arrays, generated/adversarial CIFAR arrays, and trained deep-kernel
checkpoints. A blob-only or regenerated-image experiment would not be the
paper's Table 2.

### C6 — case studies

The exact conjunction requires ImageNet distribution-shift trees, ResNet-50
feature tensors, confidence-margin split features, a CIFAR-10 ResNet-18
checkpoint, and the paper's adversarial arrays. The official code also
contains hard-coded local ImageNet paths and CUDA-only attack operations.
The historical same-versus-shifted Gaussian page remains toy evidence only.

## Publication and provenance

The approved text-only Hugging Face revision is
21969c11f261d021b8097df8838ad313e08d090a, with publication status awaiting
judge and no score increase claimed. Six allowlisted text files were
verified against their published hashes; the final audit source run is
cc08ef43-6a98-4bf7-8884-37e6166b45ce on the local Apple M2.

No GPU or paid compute was used. The full evidence chain is committed under
.openresearch/artifacts and release/hf-space-delta.
