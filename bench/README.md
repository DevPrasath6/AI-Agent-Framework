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
```

Notes:
- This harness is intentionally minimal—it's a starting point. For real
  benchmarking replace the synthetic_workload with a loader for your
  OpenVINO model and provide representative inputs.
- When running on CI you can install `openvino` packages and update the
  script to point at the compiled model file.
