import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # When are two datasets close enough?

    This tutorial opens with the reproduction evidence; it does not rerun the
    expensive or exhaustive checks. The paper proposes **NAMMD**, a normalised
    squared MMD intended for distribution-closeness tests.

    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">
      <div style="padding:18px;border-radius:14px;background:#123b35;color:white"><b>2 VERIFIED</b><br/>Claims 1 and 4</div>
      <div style="padding:18px;border-radius:14px;background:#4a2528;color:white"><b>2 FALSIFIED</b><br/>Claims 2 and 3</div>
      <div style="padding:18px;border-radius:14px;background:#3c3217;color:white"><b>2 BLOCKED</b><br/>Claims 5 and 6</div>
    </div>

    The verdicts are scoped: Claim 2 falsifies the unqualified finite v1 wording,
    not the corrected v3 asymptotic theorem.
    """)
    return


@app.cell
def _():
    evidence = {
        "claim_1": {"verdict": "VERIFIED", "paper": "[0,1]", "observed": "[0,1] exactly"},
        "claim_2": {"verdict": "FALSIFIED", "paper": "<= 0.05", "observed": 0.1853020188851843},
        "claim_3": {"verdict": "FALSIFIED", "paper": 1 / 65, "observed": 0.015336550797451998},
        "claim_4": {"verdict": "VERIFIED", "paper": -2.0, "observed": -1.9999999999999996},
        "claim_5": {"verdict": "BLOCKED", "paper": "five datasets", "observed": "exact assets absent"},
        "claim_6": {"verdict": "BLOCKED", "paper": "three case studies", "observed": "exact assets absent"},
    }
    return (evidence,)


@app.cell
def _(evidence, mo):
    rows = "\n".join(
        f"| {name.replace('_', ' ').title()} | {item['paper']} | {item['observed']} | **{item['verdict']}** |"
        for name, item in evidence.items()
    )
    mo.md(
        f"""
        ## Evidence table

        | Claim | Paper | Observed | Assessment |
        |---|---:|---:|---|
        {rows}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why the finite type-I result is exact

    The counterexample uses Bernoulli samples with `P(1)=0.1`, `Q(1)=0.9`, `m=8`,
    and a triangular kernel. Setting epsilon to the population NAMMD puts the
    distribution exactly on the null boundary. There are only `2^(2m)=65,536`
    ordered sample pairs, so the rejection probability can be summed without
    Monte Carlo uncertainty:

    - nominal alpha: **0.05**
    - exact paper-test rejection probability: **0.1853020188851843**
    - independent enumeration absolute difference: **0**
    - threshold-mutation rejection probability: **0.5147278302366373**
    """)
    return


@app.cell
def _(mo):
    margin_svg = """
    <svg width="760" height="245" viewBox="0 0 760 245" xmlns="http://www.w3.org/2000/svg">
      <rect width="760" height="245" fill="#f8fafc" rx="14"/>
      <text x="30" y="38" font-family="Arial" font-size="22" font-weight="700" fill="#0f172a">Claim 3 power advantage</text>
      <line x1="160" y1="195" x2="720" y2="195" stroke="#64748b"/>
      <line x1="175" y1="65" x2="175" y2="195" stroke="#7c3aed" stroke-width="3" stroke-dasharray="7 6"/>
      <text x="185" y="75" font-family="Arial" font-size="15" fill="#6d28d9">1/65 target</text>
      <text x="30" y="125" font-family="Arial" font-size="17" fill="#0f172a">counterexample</text>
      <rect x="160" y="98" width="12" height="38" fill="#e11d48"/>
      <text x="185" y="123" font-family="Arial" font-size="16" fill="#9f1239">0.0153365508</text>
      <text x="30" y="178" font-family="Arial" font-size="17" fill="#0f172a">paper example</text>
      <rect x="160" y="151" width="520" height="38" fill="#10b981"/>
      <text x="565" y="176" font-family="Arial" font-size="16" fill="#064e3b">0.0199441143</text>
    </svg>
    """
    mo.Html(margin_svg)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Interpreting the theorem counterexample

    The paper's own Gaussian example satisfies the `1/65` margin. The theorem is
    quantified more broadly. A deterministic search found a second
    centered-Gaussian tuple whose integer sample size lies inside the stated
    `[C1,C2]` window and satisfies every other premise, but whose asymptotic power
    advantage is below `1/65`. Adaptive numerical integration independently
    confirms the influence variance.

    ## What remains

    The benchmark and application claims are not converted to passes. Their exact
    HIGGS, generated MNIST/CIFAR, ImageNet feature, and model artifacts are absent
    from the official repository. Replacing those inputs would answer a different
    question.

    See the repository report for source hashes, experiment branches, limitations,
    and the release gate.
    """)
    return


if __name__ == "__main__":
    app.run()
