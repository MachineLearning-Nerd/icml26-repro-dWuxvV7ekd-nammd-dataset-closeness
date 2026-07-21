# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_defa0341b40c", "created_at": "2026-07-21T13:51:24+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. NAMMD is defined by normalizing squared MMD by the RKHS norms of the two compared distributions, producing a bounded value in [0,1] that increases as the underlying distributions become more concentrated (Section defining NAMMD).
2. Theorem 4 proves that the NAMMD-based distribution closeness test maintains type-I error bounded by the nominal level alpha (Theorem 4).
3. Theorem 7 proves that whenever an MMD-based distributional closeness test correctly rejects the null hypothesis, the NAMMD-based test also rejects with high probability, and gives examples where NAMMD rejects while MMD-based DCT fails (Theorem 7).
4. Theorem 5 shows the sample complexity of the NAMMD-based test scales as 1/(NAMMD(P,Q;kappa) - epsilon)^2 (Theorem 5).
5. Across five benchmark datasets (blob, higgs, hdgm, mnist, cifar10), NAMMD attains higher average test power than MMD-based DCT, e.g., 0.976 vs. 0.973 at epsilon=0.1 and 0.989 vs. 0.970 at epsilon=0.7 (Experimental results section).
6. The method is applied without ground-truth labels to three case studies: ImageNet distribution-shift variant classification, confidence-margin detection, and adversarial perturbation quantification on CIFAR-10 (Case studies section).
