# Rigorous evidence and provenance

## Fixed reproduction command

```text
uv run --frozen python repro/src/verify_nammd.py
```

The repository uses Python 3.9.25, `uv` 0.11.29, one project-level `.venv`,
and committed `pyproject.toml` plus `uv.lock`.

## Strongest formal run

- Branch: `orx/claim-3-admissible-gaussian-counterexample-searc`
- Git SHA: `ee9464863e499c350da0140321a99f6fc77a245d`
- OpenResearch run: `9091ac45-6f86-41e3-bfe2-45d67c8644f8`
- Verifier runtime: `11.575814542` seconds
- End-to-end local wall time: `1m40s`
- Seeds: `12843`, `250712843`
- Cost: `$0`

## Source identity

- arXiv v1 PDF SHA-256:
  `ddee0e2059e694d1813c418400a4a5d0c5abc17df4246873a232df1c89377829`
- arXiv v3 PDF SHA-256:
  `3141cd2d2785515c50892a54ae19015b4dcb811e320893947b0a1f40183395f5`
- official code SHA:
  `8aca5dc1ec3804ff3754b3cbc82076f8afde9219`

The current v3 table reports NAMMD averages
`[0.976, 0.955, 0.951, 0.984]` and MMD averages
`[0.973, 0.928, 0.924, 0.970]`. The imported prompt's `0.989` at
`epsilon=0.7` does not match v3's `0.984`.

## Counterexample details

For Claim 2, `P(1)=0.1`, `Q(1)=0.9`,
`epsilon=0.5423728813559324`, the triangular kernel, and `m=8` satisfy the
finite null at equality. Enumerating all 65,536 ordered sample pairs produces
rejection probability `0.1853020188851843`; an independent brute-force
implementation matches exactly.

For Claim 3, the accepted centered-Gaussian tuple has reference variances
`[0.2376507628281971, 0.26258447084718184]`, test variances
`[0.21773289592006245, 0.24666224095067044]`, and `m=61806`. Its admissible
integer window is `[61805.3008312, 61806.7861940]`. Independent adaptive
integration agrees in the influence variance to `1.58e-16`.

The machine-readable verdict, source hashes, and run provenance are stored
under `evidence/rigorous-2026-07-23/`.
