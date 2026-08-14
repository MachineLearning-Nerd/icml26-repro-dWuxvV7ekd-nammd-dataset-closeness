# Output provenance

The authoritative current result is
.openresearch/artifacts/final-run/verdicts.json, together with each claim's
raw result, contract, independent checker, negative control, and limitations.

The root outputs/verdict.json and outputs/verify_run.log are earlier
publication-lineage artifacts from the initial toy run. They are preserved to
keep provenance intact, but their old 6/6 aligned label is not the current
claim verdict.

- Canonical command: uv run --frozen python repro/src/verify_nammd.py
- Final evidence run: cc08ef43-6a98-4bf7-8884-37e6166b45ce
- Historical source branch: orx/additive-release-candidate-and-visual-report
- Historical source commit: 6c13dd24f0c73f26f44bd961e94d6f75c542ba5a
- Compute: local Apple M2 CPU, no GPU, cost 0 USD

The published Hugging Face evidence is separately hashed under
release/hf-upload-sha256.tsv and documented in release/PUBLICATION.md.
