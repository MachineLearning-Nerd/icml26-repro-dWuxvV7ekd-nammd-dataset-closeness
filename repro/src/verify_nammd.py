"""Exact finite-sample stress audit of arXiv:2507.12843v1 Theorem 4.

The paper's v1 display states finite type-I control, while its proof and v3
replacement are explicitly asymptotic.  This program enumerates every ordered
sample for Bernoulli distributions and a triangular kernel, using the paper's
published plug-in variance formula and decision threshold.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import subprocess
import time
from itertools import product
from pathlib import Path

import numpy as np
from scipy.stats import norm


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"
COMMAND = "uv run --frozen python repro/src/verify_nammd.py"
ALPHA = 0.05
Z = float(norm.ppf(1.0 - ALPHA))
SOURCE_V1 = "ddee0e2059e694d1813c418400a4a5d0c5abc17df4246873a232df1c89377829"
SOURCE_V3 = "3141cd2d2785515c50892a54ae19015b4dcb811e320893947b0a1f40183395f5"


def git_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def paper_statistic_and_se(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """Port of official DCT_exp/power_epsn/utils.py at upstream SHA 8aca5dc.

    For support {0,1}, k(x,y)=max(1-|x-y|,0) equals the equality matrix.
    This triangular kernel is nonnegative, bounded, shift-invariant and PD.
    """
    m = len(x)
    kx = (x[:, None] == x[None, :]).astype(float)
    ky = (y[:, None] == y[None, :]).astype(float)
    kxy = (x[:, None] == y[None, :]).astype(float)
    eye = np.eye(m)
    ones = np.ones(m)
    kx0, ky0 = kx * (1.0 - eye), ky * (1.0 - eye)
    xx = kx0.sum() / (m * (m - 1))
    yy = ky0.sum() / (m * (m - 1))
    xy = (kxy.sum() - np.trace(kxy)) / (m * (m - 1))
    mmd2 = xx - 2.0 * xy + yy
    denominator = 4.0 - xx - yy
    nammd = mmd2 / denominator

    xxi1 = (
        (np.linalg.norm(kx0 @ ones) ** 2 - np.linalg.norm(kx0, "fro") ** 2)
        / (m * (m - 1) * (m - 2))
        - (
            (ones @ kx0 @ ones) ** 2
            - 4.0
            * (
                np.linalg.norm(kx0 @ ones) ** 2
                + 2.0 * np.linalg.norm(kx0, "fro") ** 2
            )
        )
        / (m * (m - 1) * (m - 2) * (m - 3))
    )
    yxi1 = (
        (np.linalg.norm(ky0 @ ones) ** 2 - np.linalg.norm(ky0, "fro") ** 2)
        / (m * (m - 1) * (m - 2))
        - (
            (ones @ ky0 @ ones) ** 2
            - 4.0
            * (
                np.linalg.norm(ky0 @ ones) ** 2
                + 2.0 * np.linalg.norm(ky0, "fro") ** 2
            )
        )
        / (m * (m - 1) * (m - 2) * (m - 3))
    )
    cross_correction = (
        (ones @ kxy @ ones) ** 2
        - np.linalg.norm(kxy.T @ ones) ** 2
        - np.linalg.norm(kxy @ ones) ** 2
        + np.linalg.norm(kxy, "fro") ** 2
    )
    varxi1 = (
        xxi1
        + yxi1
        + (np.linalg.norm(kxy @ ones) ** 2 - np.linalg.norm(kxy, "fro") ** 2)
        / (m**2 * (m - 1))
        - 2.0 * cross_correction / (m**2 * (m - 1) ** 2)
        + (np.linalg.norm(kxy.T @ ones) ** 2 - np.linalg.norm(kxy, "fro") ** 2)
        / (m**2 * (m - 1))
        - 2.0 * (ones @ kx0 @ kxy @ ones) / (m**2 * (m - 1))
        + 2.0
        * (
            (ones @ kx0 @ ones) * (ones @ kxy @ ones)
            - 2.0 * (ones @ kx0 @ kxy @ ones)
        )
        / (m**2 * (m - 1) * (m - 2))
        - 2.0 * (ones @ ky0 @ kxy.T @ ones) / (m**2 * (m - 1))
        + 2.0
        * (
            (ones @ ky0 @ ones) * (ones @ kxy.T @ ones)
            - 2.0 * (ones @ ky0 @ kxy.T @ ones)
        )
        / (m**2 * (m - 1) * (m - 2))
    )
    varxi2 = (
        xxi1
        + yxi1
        + 2.0 * np.linalg.norm(kxy, "fro") ** 2 / m**2
        - 2.0 * cross_correction / (m**2 * (m - 1) ** 2)
        - 4.0 * (ones @ kx0 @ kxy @ ones) / (m**2 * (m - 1))
        + 4.0
        * (
            (ones @ kx0 @ ones) * (ones @ kxy @ ones)
            - 2.0 * (ones @ kx0 @ kxy @ ones)
        )
        / (m**2 * (m - 1) * (m - 2))
        - 4.0 * (ones @ ky0 @ kxy.T @ ones) / (m**2 * (m - 1))
        + 4.0
        * (
            (ones @ ky0 @ ones) * (ones @ kxy.T @ ones)
            - 2.0 * (ones @ ky0 @ kxy.T @ ones)
        )
        / (m**2 * (m - 1) * (m - 2))
    )
    variance_mmd = (
        4.0 * (m - 2) * varxi1 / (m * (m - 1))
        + 2.0 * varxi2 / (m * (m - 1))
    )
    variance_nammd = variance_mmd / denominator**2
    standard_error = math.sqrt(variance_nammd) if variance_nammd > 0.0 else math.nan
    return nammd, standard_error, variance_nammd


def population_nammd(p: float, q: float) -> float:
    a = p * p + (1.0 - p) ** 2
    b = q * q + (1.0 - q) ** 2
    c = p * q + (1.0 - p) * (1.0 - q)
    return (a + b - 2.0 * c) / (4.0 - a - b)


def multiplicity(m: int, kx: int, ky: int, both_one: int) -> int:
    cells = (
        both_one,
        kx - both_one,
        ky - both_one,
        m - kx - ky + both_one,
    )
    value = math.factorial(m)
    for cell in cells:
        value //= math.factorial(cell)
    return value


def sufficient_states(m: int) -> list[dict]:
    states = []
    for kx in range(m + 1):
        for ky in range(m + 1):
            for both in range(max(0, kx + ky - m), min(kx, ky) + 1):
                x = np.array([1] * both + [1] * (kx - both) + [0] * (ky - both) + [0] * (m - kx - ky + both))
                y = np.array([1] * both + [0] * (kx - both) + [1] * (ky - both) + [0] * (m - kx - ky + both))
                statistic, se, variance = paper_statistic_and_se(x, y)
                states.append(
                    {
                        "kx": kx,
                        "ky": ky,
                        "both_one": both,
                        "multiplicity": multiplicity(m, kx, ky, both),
                        "statistic": statistic,
                        "standard_error": se,
                        "variance": variance,
                    }
                )
    assert sum(state["multiplicity"] for state in states) == 2 ** (2 * m)
    return states


def rejection_probability(states: list[dict], m: int, p: float, q: float, z: float) -> float:
    epsilon = population_nammd(p, q)
    total = 0.0
    for state in states:
        se = state["standard_error"]
        reject = math.isfinite(se) and state["statistic"] > epsilon + z * se
        if reject:
            kx, ky = state["kx"], state["ky"]
            weight = (
                p**kx
                * (1.0 - p) ** (m - kx)
                * q**ky
                * (1.0 - q) ** (m - ky)
            )
            total += state["multiplicity"] * weight
    return total


def brute_force_probability(m: int, p: float, q: float, z: float) -> float:
    epsilon = population_nammd(p, q)
    total = 0.0
    for x_tuple in product((0, 1), repeat=m):
        x = np.asarray(x_tuple)
        kx = int(x.sum())
        px = p**kx * (1.0 - p) ** (m - kx)
        for y_tuple in product((0, 1), repeat=m):
            y = np.asarray(y_tuple)
            ky = int(y.sum())
            statistic, se, _ = paper_statistic_and_se(x, y)
            if math.isfinite(se) and statistic > epsilon + z * se:
                total += px * q**ky * (1.0 - q) ** (m - ky)
    return total


def main() -> int:
    started = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    grid = [i / 20.0 for i in range(1, 20)]
    per_m = []
    global_best = {"probability": -1.0}
    cached_states = {}
    for m in range(4, 9):
        states = sufficient_states(m)
        cached_states[m] = states
        best = {"probability": -1.0}
        for p in grid:
            for q in grid:
                if p == q:
                    continue
                epsilon = population_nammd(p, q)
                if not 0.0 < epsilon < 1.0:
                    continue
                probability = rejection_probability(states, m, p, q, Z)
                candidate = {
                    "m": m,
                    "p": p,
                    "q": q,
                    "epsilon": epsilon,
                    "probability": probability,
                    "excess_over_alpha": probability - ALPHA,
                    "state_classes": len(states),
                    "ordered_samples": 2 ** (2 * m),
                }
                if probability > best["probability"]:
                    best = candidate
                if probability > global_best["probability"]:
                    global_best = candidate
        per_m.append(best)

    brute_probability = brute_force_probability(
        global_best["m"], global_best["p"], global_best["q"], Z
    )
    independent_error = abs(brute_probability - global_best["probability"])
    mutated_probability = rejection_probability(
        cached_states[global_best["m"]],
        global_best["m"],
        global_best["p"],
        global_best["q"],
        0.0,
    )
    counterexample = global_best["probability"] > ALPHA + 1e-12
    independent_passed = independent_error < 1e-12
    control_failed_as_intended = mutated_probability > global_best["probability"]

    claim = {
        "verdict": "FALSIFIED" if counterexample and independent_passed else "BLOCKED",
        "passed": bool(counterexample and independent_passed and control_failed_as_intended),
        "scope": "finite, unqualified v1 Theorem 4 statement",
        "counterexample": global_best,
        "independent_checker": {
            "method": "brute force over all ordered binary x/y sequences",
            "probability": brute_probability,
            "absolute_error": independent_error,
            "passed": independent_passed,
        },
        "negative_control": {
            "mutation": "replace z_(0.95) by z_(0.50)=0",
            "probability": mutated_probability,
            "failed_as_intended": control_failed_as_intended,
        },
        "asymptotic_v3": {
            "verdict": "BLOCKED",
            "reason": "A finite counterexample does not contradict the corrected asymptotic theorem.",
        },
        "kernel": {
            "formula": "k(x,y)=max(1-|x-y|,0)",
            "support": [0, 1],
            "properties": ["bounded by K=1", "nonnegative", "shift-invariant", "positive definite"],
        },
        "search": {
            "p_q_grid": grid,
            "sample_sizes": [4, 5, 6, 7, 8],
            "max_per_m": per_m,
            "exact_not_monte_carlo": True,
        },
    }
    evidence = {
        "paper": "arXiv:2507.12843",
        "source_sha256": {"v1": SOURCE_V1, "v3": SOURCE_V3},
        "official_code_sha": "8aca5dc1ec3804ff3754b3cbc82076f8afde9219",
        "command": COMMAND,
        "git_sha": git_sha(),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "machine": platform.machine(),
            "cpu_count": os.cpu_count(),
        },
        "runtime_seconds": time.perf_counter() - started,
        "claim_2": claim,
    }
    verdict_path = OUT / "verdict.json"
    verdict_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    manifest = {
        "outputs/verdict.json": {
            "sha256": sha256(verdict_path),
            "bytes": verdict_path.stat().st_size,
        }
    }
    print("CLAIM 2 EXACT FINITE-SAMPLE AUDIT")
    print(f"command={COMMAND}")
    print(f"git_sha={evidence['git_sha']}")
    print(f"verdict={claim['verdict']}")
    print(f"best={json.dumps(global_best, sort_keys=True)}")
    print(f"independent_probability={brute_probability:.17g}")
    print("ORX_EVIDENCE_JSON=" + json.dumps(evidence, sort_keys=True))
    print("ORX_OUTPUT_MANIFEST=" + json.dumps(manifest, sort_keys=True))
    return 0 if claim["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
