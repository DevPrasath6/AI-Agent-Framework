OpenVINO benchmark harness
===========================

This folder contains a small benchmark harness that can be used to measure
inference-like timings either with OpenVINO (if installed) or using a CPU
synthetic fallback for development and CI.

Files:
- `openvino_bench.py` — small script that runs a synthetic workload and
  reports timing statistics. If `openvino.runtime` is available it will use
  a placeholder path (user should replace with a real model) otherwise it
  runs a synthetic CPU-bound loop.

Usage:

```powershell
python -m bench.openvino_bench --runs 50 --size 224
python bench\openvino_bench.py --model-path path/to/model.xml --runs 40 --out bench_output\result.json --plot
```

CLI options:
- `--model-path` — Optional path to an OpenVINO model (IR XML or other supported format). When provided the harness will attempt to load and run the model using `openvino.runtime`.
- `--runs` — Number of inference runs to perform (default: 20).
- `--size` — Fallback synthetic input size (default: 224). Only used when no model is provided.
- `--out` — Path to write JSON results (will contain `stats` and raw `times`).
- `--plot` — If set and `matplotlib` is available, the harness will also write a PNG timing plot next to the JSON output.

CI integration:

We include a GitHub Actions workflow at `.github/workflows/bench_openvino.yml` that demonstrates running the harness on a matrix (with/without installing `openvino`). The workflow:

- Checks out the repo and installs Python dependencies.
- Optionally installs `openvino` via `pip` when running the `openvino=true` matrix job (best-effort).
- Runs the harness and writes results to `bench_output/result.json`.
- Uploads `bench_output` as an artifact for later inspection.

Notes on runners and OpenVINO:
- Installing `openvino` via `pip` on standard GitHub runners is best-effort and may not provide the exact hardware-optimized runtime you want. For consistent results use a self-hosted runner or a container image with OpenVINO preinstalled.
- To track results over time you can download the artifacts from each run and process them into a dashboard (e.g., commit a CSV to a branch, or push metrics to an external monitoring service). The current workflow uploads JSON+PNG artifacts so you can manually download and visualize them or add a follow-up workflow to aggregate artifacts across runs.

If you'd like, I can extend the workflow to automatically aggregate results into a CSV and commit them to a `benchmarks/` branch, or push visualizations to GitHub Pages. Tell me which option you prefer and I will implement it.
