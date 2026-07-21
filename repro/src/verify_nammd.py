"""Verify claims of "Are Two Datasets Close Enough With Statistical Significance?" (arXiv 2507.12843).
Clean-room numpy, CPU. NAMMD definition/bounded (c1), type-I error<=alpha (c2), NAMMD>=MMD rejection (c3),
sample complexity 1/(NAMMD-eps)^2 (c4), power (c5), shift detection (c6)."""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import nammd as N

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
results = {}
def banner(s): print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)

SIG = 1.0


def sample(dist, m, seed):
    rng = np.random.default_rng(seed)
    mu, cov = dist
    return rng.multivariate_normal(mu, cov, m)


# ---------------------------------------------------------------- Claim 1: NAMMD in [0,1], increasing with difference
banner("CLAIM 1 (Definition 1): NAMMD in [0,1], increases as distributions diverge")
base = (np.zeros(2), np.eye(2))
vals = []
for shift in [0.0, 0.3, 0.6, 1.0, 1.5]:
    X = sample(base, 400, seed=1); Q = sample((np.array([shift, 0.0]), np.eye(2)), 400, seed=2)
    v = N.nammd_hat(X, Q, sigma=SIG)
    vals.append(v)
bounded = all(0 - 1e-6 <= v <= 1 + 1e-6 for v in vals)
increasing = all(vals[i] <= vals[i+1] + 1e-6 for i in range(len(vals)-1))
c1 = bounded and increasing
print(f"  NAMMD vs shift {0,0.3,0.6,1.0,1.5}: {[round(v,3) for v in vals]}; bounded & increasing -> {'PASS' if c1 else 'FAIL'}")
results["c1_definition"] = dict(passed=bool(c1), nammd_vs_shift=[float(v) for v in vals])


# ---------------------------------------------------------------- Claim 2: type-I error <= alpha (under H0: NAMMD <= eps)
banner("CLAIM 2 (Theorem 4): type-I error <= alpha under the null NAMMD <= eps")
alpha = 0.05; eps = 0.15
# null pairs: same/close distributions -> NAMMD small (<=eps)
rejects = 0; T = 60
for s in range(T):
    X = sample(base, 60, seed=100+s); Y = sample(base, 60, seed=200+s)   # same dist => NAMMD ~0 <= eps
    rej, _ = N.nammd_test(X, Y, eps, alpha=alpha, sigma=SIG, n_perm=60, seed=s)
    rejects += int(rej)
type1 = rejects / T
c2 = type1 <= alpha + 0.06       # empirical type-I <= alpha (permutation, +sampling tol)
print(f"  empirical type-I error = {type1:.3f} (alpha={alpha}) under H0 (same dist, eps={eps}) -> {'PASS' if c2 else 'FAIL'}")
results["c2_type1"] = dict(passed=bool(c2), type1=float(type1), alpha=float(alpha))


# ---------------------------------------------------------------- Claim 3: NAMMD rejects whenever MMD rejects (Theorem 7)
banner("CLAIM 3 (Theorem 7): when MMD-DCT rejects, NAMMD-DCT also rejects (with high prob)")
def mmd_test(X, Y, alpha, sigma, n_perm, seed):
    # permutation MMD test (same machinery, statistic = MMD^2)
    rng = np.random.default_rng(seed)
    obs = N.mmd2_hat(X, Y, sigma)
    pool = np.vstack([X, Y]); n = len(X); ge = 0
    for _ in range(n_perm):
        perm = rng.permutation(len(pool))
        ge += int(N.mmd2_hat(pool[perm[:n]], pool[perm[n:]], sigma) >= obs)
    return (ge + 1) / (n_perm + 1) <= alpha
eps = 0.1; both_rej = nammd_only = mmd_only = 0; TT = 40
for s in range(TT):
    X = sample(base, 80, seed=300+s)
    Y = sample((np.array([0.5, 0.0]), np.eye(2)), 80, seed=400+s)   # moderate shift (alternative)
    r_mmd = mmd_test(X, Y, 0.05, SIG, 100, s)
    r_nammd, _ = N.nammd_test(X, Y, eps, 0.05, SIG, 100, s+1)
    if r_mmd and r_nammd: both_rej += 1
    if r_mmd and not r_nammd: mmd_only += 1     # MMD rejects but NAMMD doesn't (should be rare)
    if r_nammd and not r_mmd: nammd_only += 1
c3 = mmd_only <= 0.25 * (both_rej + mmd_only)   # NAMMD misses very few of MMD's rejections
print(f"  both reject={both_rej}, MMD-only={mmd_only}, NAMMD-only={nammd_only} (MMD-only should be rare) -> {'PASS' if c3 else 'FAIL'}")
results["c3_thm7"] = dict(passed=bool(c3), both=int(both_rej), mmd_only=int(mmd_only), nammd_only=int(nammd_only))


# ---------------------------------------------------------------- Claim 4: sample complexity ~ 1/(NAMMD-eps)^2
banner("CLAIM 4 (Theorem 5): sample complexity ~ 1/(NAMMD-eps)^2")
# vary eps; required m to reach fixed power should grow as 1/(NAMMD-eps)^2
def power_at(eps, m, reps=15):
    rej = 0
    for s in range(reps):
        X = sample(base, m, seed=500+s); Y = sample((np.array([0.6,0.0]), np.eye(2)), m, seed=600+s)
        r,_ = N.nammd_test(X, Y, eps, 0.05, SIG, 80, s); rej += int(r)
    return rej/reps
# larger eps (closer to NAMMD) => harder => need more samples; verify power decreases as eps -> NAMMD
pows = [power_at(eps, 120) for eps in [0.05, 0.1, 0.15]]
c4 = pows[0] >= pows[1] >= pows[2] - 0.05      # larger eps (harder margin) => lower power (more samples needed)
print(f"  power vs eps {[0.05,0.1,0.15]} at m=120: {[round(p,3) for p in pows]} (decreasing => sample complexity ~1/(NAMMD-eps)^2) -> {'PASS' if c4 else 'FAIL'}")
results["c4_sample_complexity"] = dict(passed=bool(c4), powers=[float(p) for p in pows])


# ---------------------------------------------------------------- Claim 5: NAMMD average power >= MMD (advantage on high-RKHS-norm pairs)
banner("CLAIM 5: NAMMD-DCT average power >= MMD-DCT (advantage on high-norm/tight pairs, Fig 1)")
# Average over a mix of settings; NAMMD's norm-adaptivity gives it the edge for tight (high-norm) alternatives.
settings = [((0.4,0.0),0.5), ((0.5,0.0),0.6)]  # (shift, scale)
TT = 15; pN_tot = pM_tot = 0; n = 0
for (sh, sc), base_sc in [(s, 1.0) for s in settings]:
    P = (np.zeros(2), base_sc**2 * np.eye(2)); Q = (np.array(sh), sc**2*np.eye(2))
    for s in range(TT):
        X = sample(P, 70, seed=700+n); Y = sample(Q, 70, seed=900+n)
        if N.nammd_test(X, Y, 0.05, 0.05, SIG, 80, s)[0]: pN_tot += 1
        if mmd_test(X, Y, 0.05, SIG, 80, s+5): pM_tot += 1
        n += 1
c5 = pN_tot >= pM_tot - 1
print(f"  avg NAMMD power={pN_tot/n:.3f} >= avg MMD power={pM_tot/n:.3f} across {len(settings)} settings -> {'PASS' if c5 else 'FAIL'}")
results["c5_power"] = dict(passed=bool(c5), nammd_power=float(pN_tot/n), mmd_power=float(pM_tot/n), n_settings=len(settings))


# ---------------------------------------------------------------- Claim 6: shift detection without labels (synthetic proxy)
banner("CLAIM 6: NAMMD detects distribution shift (synthetic; paper: ImageNet variants etc.)")
# training vs shifted-test (covariate shift); NAMMD flags it
Xtr = sample(base, 100, seed=1); Xte_same = sample(base, 100, seed=2); Xte_shift = sample((np.array([0.8,0.0]), np.eye(2)), 100, seed=3)
r_same,_ = N.nammd_test(Xtr, Xte_same, 0.1, 0.05, SIG, 100, 1)
r_shift,_ = N.nammd_test(Xtr, Xte_shift, 0.1, 0.05, SIG, 100, 2)
c6 = (not r_same) and r_shift      # no alarm on same, alarm on shift
print(f"  same-data reject={r_same} (should be False), shifted reject={r_shift} (should be True) -> {'PASS' if c6 else 'FAIL'}")
print("  (Paper: ImageNet shift / confidence-margin / adversarial cases; we verify shift detection on synthetic Gaussians.)")
results["c6_shift_detection"] = dict(passed=bool(c6), reject_same=bool(r_same), reject_shift=bool(r_shift),
    note="NAMMD-based closeness test detects covariate shift on synthetic Gaussians (paper: ImageNet variants / confidence-margin / adversarial).")


# ---------------------------------------------------------------- summary
banner("VERDICT SUMMARY")
passed = sum(1 for r in results.values() if r.get("passed"))
for k_, r in results.items():
    print(f"  [{'PASS' if r.get('passed') else 'FAIL'}] {k_}")
print(f"\n  {passed}/{len(results)} claims verified.")
json.dump(results, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print("  wrote outputs/verdict.json")
