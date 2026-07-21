"""Clean-room NAMMD (norm-adaptive MMD) distribution-closeness test from
"Are Two Datasets Close Enough With Statistical Significance?" (arXiv 2507.12843). numpy, CPU.

Definition 1: NAMMD(P,Q;kappa) = MMD^2(P,Q) / (4K - ||mu_P||^2 - ||mu_Q||^2),  in [0,1],
  MMD^2 = ||mu_P - mu_Q||^2_Hk,  ||mu_P||^2 = E_{x,x'~P} kappa(x,x'),  K = kappa(0) (=1 for Gaussian).
U-statistic estimator: MMD^2_hat = (1/m(m-1)) sum_{i!=j} H_ij,
  H_ij = kappa(x_i,x_j)+kappa(y_i,y_j)-kappa(x_i,y_j)-kappa(y_i,x_j).
DCT: H0: NAMMD <= eps  vs  H1: NAMMD > eps; reject via permutation threshold at level alpha.
"""
from __future__ import annotations
import numpy as np


def gauss_kernel(X, Y, sigma=1.0):
    """Gaussian kernel kappa(x,y)=exp(-|x-y|^2/(2 sigma^2)), K=kappa(0)=1."""
    d2 = (X[:, None, :] - Y[None, :, :]) ** 2
    return np.exp(-d2.sum(2) / (2 * sigma ** 2))


def embedding_norm_sq(X, sigma=1.0):
    """||mu_P||^2 = E_{x,x'~P} kappa(x,x'), U-statistic (i!=j)."""
    K = gauss_kernel(X, X, sigma)
    m = len(X)
    return (K.sum() - np.trace(K)) / (m * (m - 1))


def mmd2_hat(X, Y, sigma=1.0):
    Kxx = gauss_kernel(X, X, sigma); Kyy = gauss_kernel(Y, Y, sigma); Kxy = gauss_kernel(X, Y, sigma)
    m = len(X)
    hxx = (Kxx.sum() - np.trace(Kxx)) / (m * (m - 1))
    hyy = (Kyy.sum() - np.trace(Kyy)) / (m * (m - 1))
    hxy = Kxy.mean()
    return hxx + hyy - 2 * hxy


def nammd_hat(X, Y, sigma=1.0, K=1.0):
    m2 = mmd2_hat(X, Y, sigma)
    np_ = embedding_norm_sq(X, sigma); nq = embedding_norm_sq(Y, sigma)
    denom = 4 * K - np_ - nq
    return max(m2 / denom, 0.0) if denom > 1e-12 else 0.0


def nammd_test(X, Y, eps, alpha=0.05, sigma=1.0, n_perm=200, seed=0):
    """Permutation NAMMD-DCT: reject H0 (NAMMD<=eps) if the permutation p-value of the
    'exceedance' (NAMMD_hat - eps) is <= alpha. Returns (reject, stat)."""
    rng = np.random.default_rng(seed)
    obs = nammd_hat(X, Y, sigma) - eps
    pool = np.vstack([X, Y]); n = len(X)
    ge = 0
    for _ in range(n_perm):
        perm = rng.permutation(len(pool)); P = pool[perm[:n]]; Q = pool[perm[n:]]
        ge += int(nammd_hat(P, Q, sigma) - eps >= obs)
    pval = (ge + 1) / (n_perm + 1)
    return bool(pval <= alpha), float(obs)
