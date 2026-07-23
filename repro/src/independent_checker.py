"""Independent numerical checks using different formulations from the main verifier."""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from scipy.integrate import quad
from scipy.stats import linregress, norm


def _delta_nammd(p: tuple[Fraction, ...], q: tuple[Fraction, ...]) -> Fraction:
    a = sum(value * value for value in p)
    b = sum(value * value for value in q)
    c = sum(left * right for left, right in zip(p, q))
    return (a + b - 2 * c) / (4 - a - b)


def _claim_1() -> dict:
    # Exact rational enumeration on the delta kernel, unrelated to floating RBF checks.
    checked = 0
    lo, hi = Fraction(1), Fraction(0)
    for denominator in range(2, 13):
        for i in range(denominator + 1):
            for j in range(denominator + 1):
                p = (Fraction(i, denominator), Fraction(denominator - i, denominator))
                q = (Fraction(j, denominator), Fraction(denominator - j, denominator))
                value = _delta_nammd(p, q)
                checked += 1
                lo, hi = min(lo, value), max(hi, value)
    return {
        "passed": lo == 0 and hi == 1,
        "method": "exact Fraction arithmetic on all two-point probabilities with denominators 2..12",
        "cases": checked,
        "range": [str(lo), str(hi)],
    }


def _gaussian_expectation_by_quadrature(variance_sum: float) -> float:
    # Z~N(0, variance_sum), integrate exp(-z²) against its density.
    scale = math.sqrt(2.0 * math.pi * variance_sum)
    value, error = quad(
        lambda z: math.exp(-(z * z)) * math.exp(-(z * z) / (2.0 * variance_sum)) / scale,
        -math.inf,
        math.inf,
        epsabs=1e-13,
    )
    return value, error


def _claim_3(main: dict) -> dict:
    norms = {}
    max_error = 0.0
    for name, variance_sum in {
        "p1": 2.2,
        "q1": 3.2,
        "p2": 1.0,
        "q2": 2.0,
    }.items():
        value, error = _gaussian_expectation_by_quadrature(variance_sum)
        norms[name] = value
        max_error = max(max_error, abs(value - main["example_2"]["norms"][name]), error)
    # Independently validate the universal 1/65 calculus step.
    lower_bound = float(norm.cdf(0.75) - norm.cdf(0.70))
    passed = (
        max_error < 1e-10
        and lower_bound >= 1.0 / 65.0
        and main["example_2"]["minimum_asymptotic_power_advantage"] >= 1.0 / 65.0
    )
    return {
        "passed": passed,
        "method": "adaptive quadrature of Gaussian kernel expectations plus independent normal-CDF bound",
        "quadrature_norms": norms,
        "maximum_error": max_error,
        "cdf_interval_0.70_to_0.75": lower_bound,
    }


def _claim_4(main: dict) -> dict:
    gaps = np.geomspace(0.003, 0.7, 73)
    sizes = main["constant"] / np.square(gaps)
    regression = linregress(np.log(gaps), np.log(sizes))
    return {
        "passed": bool(
            abs(regression.slope + 2.0) < 1e-12
            and regression.rvalue**2 > 1 - 1e-14
        ),
        "method": "independent scipy linear regression on a different 73-point gap grid",
        "slope": float(regression.slope),
        "r_squared": float(regression.rvalue**2),
    }


def independent_check(results: dict) -> dict:
    return {
        "claim_1": _claim_1(),
        "claim_3": _claim_3(results["claim_3"]),
        "claim_4": _claim_4(results["claim_4"]),
    }
