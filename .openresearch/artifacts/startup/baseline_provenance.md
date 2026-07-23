# Frozen baseline provenance

- Expected starting SHA: `d05e9bf7cac90cce30eab0f53e9393311330c869`
- Baseline branch before setup: `master`
- Judge/HF revision: `9494ace83ec1c99632a33b773f64c82e12891405`
- Live score at retrieval: `5/12`
- Fixed command: `uv run --frozen python repro/src/verify_nammd.py`
- Compute: local Apple M2 CPU, 8 logical CPUs, 16 GiB RAM
- Environment: one repository-local `.venv`, Python 3.9.25, `uv` 0.11.29
- Existing verifier behavior was not changed before the baseline run.

The authoritative upstream environment uses Python 3.9.0 and a CUDA-oriented
PyTorch 2.0.1/torchvision 0.15.2 stack. That pair hangs while loading
torchvision's native image extension on macOS 26/Apple Silicon. This CPU
reproduction keeps the documented Python 3.9 minor series and numerical
versions, but resolves PyTorch 2.8.0/torchvision 0.23.0. Linux uses the
CPU-only wheel index. The full CUDA dependency set is intentionally excluded
because GPU execution is prohibited.

The protected judged Space, exact live verdict row, and retrieved paper sources
are stored outside the Git worktree in the OpenResearch Files directory under
`project/startup-audit/`. The judged Space manifest covers 17 immutable files.
