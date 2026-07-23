"""Admissible Gaussian counterexample search for Theorem 7/9's 1/65 bound."""
from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm


Z_95 = float(norm.ppf(0.95))
TARGET = 1.0 / 65.0
SEARCH_SEED = 250712843


def same_moment(variance):
    return 1.0 / np.sqrt(1.0 + 4.0 * variance)


def cross_moment(left_variance, right_variance):
    return 1.0 / np.sqrt(1.0 + 2.0 * (left_variance + right_variance))


def product_moment(base_variance, left_variance, right_variance):
    left_scale = 1.0 + 2.0 * left_variance
    right_scale = 1.0 + 2.0 * right_variance
    exponent_scale = 1.0 / left_scale + 1.0 / right_scale
    return 1.0 / (
        np.sqrt(left_scale * right_scale)
        * np.sqrt(1.0 + 2.0 * base_variance * exponent_scale)
    )


def sigma_m_squared(test_p_variance, test_q_variance):
    """Closed-form 4*Var(E[H12|Z1]) for k(x,y)=exp(-(x-y)^2)."""
    a = same_moment(test_p_variance)
    b = same_moment(test_q_variance)
    c = cross_moment(test_p_variance, test_q_variance)
    a2_p = (
        product_moment(test_p_variance, test_p_variance, test_p_variance)
        + product_moment(test_p_variance, test_q_variance, test_q_variance)
        - 2.0 * product_moment(test_p_variance, test_p_variance, test_q_variance)
    )
    a2_q = (
        product_moment(test_q_variance, test_p_variance, test_p_variance)
        + product_moment(test_q_variance, test_q_variance, test_q_variance)
        - 2.0 * product_moment(test_q_variance, test_p_variance, test_q_variance)
    )
    mean_p = a - c
    mean_q = c - b
    mmd2 = a + b - 2.0 * c
    second = a2_p + a2_q - 2.0 * mean_p * mean_q
    return 4.0 * np.maximum(second - mmd2**2, 0.0)


def _candidate_arrays(count: int):
    rng = np.random.default_rng(SEARCH_SEED)
    test_p = np.exp(rng.uniform(np.log(0.02), np.log(2.0), count))
    test_ratio = np.exp(rng.uniform(np.log(1.05), np.log(8.0), count))
    test_q = test_p * test_ratio
    scale = np.exp(rng.uniform(np.log(1.05), np.log(20.0), count))
    reference_p = test_p * scale
    reference_ratio = np.exp(
        rng.uniform(np.log(1.001), np.log(1.0 + 0.85 * (test_ratio - 1.0)), count)
    )
    reference_q = reference_p * reference_ratio
    return reference_p, reference_q, test_p, test_q


def search(count: int = 750_000) -> dict:
    rp, rq, tp, tq = _candidate_arrays(count)
    ar, br = same_moment(rp), same_moment(rq)
    at, bt = same_moment(tp), same_moment(tq)
    cr, ct = cross_moment(rp, rq), cross_moment(tp, tq)
    mmd_r, mmd_t = ar + br - 2.0 * cr, at + bt - 2.0 * ct
    norm_r, norm_t = 4.0 - ar - br, 4.0 - at - bt
    nammd_r, nammd_t = mmd_r / norm_r, mmd_t / norm_t
    sigma_sq = sigma_m_squared(tp, tq)
    sigma = np.sqrt(sigma_sq)
    difference = mmd_t - mmd_r
    with np.errstate(divide="ignore", invalid="ignore"):
        c2 = ((Z_95 + 0.7) * sigma / difference) ** 2
        m_a_minus = (Z_95 * sigma / difference) ** 2
        m_b = (20.0 * (1.0 - norm_t / norm_r) * mmd_r / sigma) ** -2
        m = np.floor(c2)
        a_term = (np.sqrt(m) * difference - sigma * Z_95) / sigma
        b_term = np.sqrt(m) * (1.0 - norm_t / norm_r) * mmd_r / sigma
        advantage = norm.cdf(a_term + b_term) - norm.cdf(a_term)
        delta = (
            np.sqrt(m)
            * nammd_r
            * ((at + bt) - (ar + br))
            / (np.sqrt(m) * mmd_r + sigma * Z_95)
        )
    valid = (
        np.isfinite(advantage)
        & (m >= 4)
        & (m <= 10_000_000)
        & (m >= np.maximum(m_a_minus, m_b))
        & (m <= c2)
        & (mmd_r > 0.0)
        & (mmd_t > mmd_r)
        & (nammd_t > nammd_r)
        & ((ar + br) < (at + bt))
        & (sigma_sq > 0.0)
        & (a_term >= 0.0)
        & (a_term <= 0.7 + 1e-12)
        & (b_term >= 0.05 - 1e-12)
        & (delta > 0.0)
        & (delta < 0.5)
    )
    if not np.any(valid):
        return {"found": False, "searched": count}
    indices = np.flatnonzero(valid)
    index = int(indices[np.argmin(advantage[indices])])
    result = {
        "found": bool(advantage[index] < TARGET),
        "searched": count,
        "reference_variances": [float(rp[index]), float(rq[index])],
        "test_variances": [float(tp[index]), float(tq[index])],
        "m": int(m[index]),
        "mmd2_reference": float(mmd_r[index]),
        "mmd2_test": float(mmd_t[index]),
        "nammd_reference": float(nammd_r[index]),
        "nammd_test": float(nammd_t[index]),
        "embedding_norm_sum_reference": float(ar[index] + br[index]),
        "embedding_norm_sum_test": float(at[index] + bt[index]),
        "norm_denominator_reference": float(norm_r[index]),
        "norm_denominator_test": float(norm_t[index]),
        "sigma_m_squared": float(sigma_sq[index]),
        "c1": float(max(m_a_minus[index], m_b[index])),
        "c2": float(c2[index]),
        "a_term": float(a_term[index]),
        "b_term": float(b_term[index]),
        "delta": float(delta[index]),
        "power_advantage": float(advantage[index]),
        "target_1_over_65": TARGET,
        "violation_margin": float(TARGET - advantage[index]),
    }
    result["assumptions"] = {
        "both_alternatives": bool(
            result["mmd2_test"] > result["mmd2_reference"]
            and result["nammd_test"] > result["nammd_reference"]
        ),
        "strict_norm_order": bool(
            result["embedding_norm_sum_reference"]
            < result["embedding_norm_sum_test"]
        ),
        "integer_in_c1_c2": bool(result["c1"] <= result["m"] <= result["c2"]),
        "delta_in_0_half": bool(0.0 < result["delta"] < 0.5),
        "same_kernel": True,
    }
    return result


def _feature_mean(x: float, distribution_variance: float) -> float:
    return math.exp(-(x * x) / (1.0 + 2.0 * distribution_variance)) / math.sqrt(
        1.0 + 2.0 * distribution_variance
    )


def independent_sigma_by_quadrature(test_p_variance: float, test_q_variance: float) -> float:
    """Numerically integrate the influence variance without closed-form products."""
    def density(x: float, variance: float) -> float:
        return math.exp(-(x * x) / (2.0 * variance)) / math.sqrt(
            2.0 * math.pi * variance
        )

    def influence(x: float) -> float:
        return _feature_mean(x, test_p_variance) - _feature_mean(x, test_q_variance)

    mean_p = quad(
        lambda x: influence(x) * density(x, test_p_variance),
        -math.inf,
        math.inf,
        epsabs=1e-12,
    )[0]
    mean_q = quad(
        lambda x: influence(x) * density(x, test_q_variance),
        -math.inf,
        math.inf,
        epsabs=1e-12,
    )[0]
    second_p = quad(
        lambda x: influence(x) ** 2 * density(x, test_p_variance),
        -math.inf,
        math.inf,
        epsabs=1e-12,
    )[0]
    second_q = quad(
        lambda x: influence(x) ** 2 * density(x, test_q_variance),
        -math.inf,
        math.inf,
        epsabs=1e-12,
    )[0]
    mmd2 = mean_p - mean_q
    second = second_p + second_q - 2.0 * mean_p * mean_q
    return 4.0 * (second - mmd2**2)


def independent_check(candidate: dict) -> dict:
    if not candidate.get("found"):
        return {"passed": False, "reason": "search found no violating candidate"}
    tp, tq = candidate["test_variances"]
    sigma_sq = independent_sigma_by_quadrature(tp, tq)
    sigma = math.sqrt(sigma_sq)
    gap = candidate["mmd2_test"] - candidate["mmd2_reference"]
    m = candidate["m"]
    a_term = (math.sqrt(m) * gap - sigma * Z_95) / sigma
    b_term = (
        math.sqrt(m)
        * (
            1.0
            - candidate["norm_denominator_test"]
            / candidate["norm_denominator_reference"]
        )
        * candidate["mmd2_reference"]
        / sigma
    )
    advantage = 0.5 * (
        math.erf((a_term + b_term) / math.sqrt(2.0))
        - math.erf(a_term / math.sqrt(2.0))
    )
    assumptions_hold = all(candidate["assumptions"].values())
    return {
        "passed": bool(
            assumptions_hold
            and abs(sigma_sq - candidate["sigma_m_squared"]) < 1e-9
            and advantage < TARGET
        ),
        "method": "adaptive numerical integration of influence moments plus math.erf CDF",
        "sigma_m_squared": sigma_sq,
        "sigma_absolute_error": abs(sigma_sq - candidate["sigma_m_squared"]),
        "a_term": a_term,
        "b_term": b_term,
        "power_advantage": advantage,
        "target_1_over_65": TARGET,
        "assumptions_hold": assumptions_hold,
    }
