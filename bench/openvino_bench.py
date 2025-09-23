"""Simple OpenVINO benchmark harness.

Provides a safe no-op fallback when OpenVINO isn't installed so developers
can run the benchmark script locally without requiring OpenVINO.

Usage:
    python -m bench.openvino_bench --runs 50 --size 224
"""
from __future__ import annotations

import time
import statistics
from typing import List
import importlib.util


def _has_openvino() -> bool:
    try:
        return importlib.util.find_spec("openvino.runtime") is not None
    except Exception:
        return False


def synthetic_workload(size: int = 224) -> List[float]:
    """Run a synthetic workload that resembles an inference loop.

    If OpenVINO is available the function will attempt to load a tiny
    compiled model (not provided here) and run inference; otherwise it will
    simulate compute by running a tight CPU-bound loop to provide timings.
    """
    timings: List[float] = []

    if _has_openvino():
        try:
            import numpy as np  # type: ignore

            # This is a placeholder: users should replace with a real model path
            # and preprocessing matching their model. For tests we simulate a
            # small numeric workload.
            for _ in range(10):
                inp = np.random.rand(1, 3, size, size).astype("float32")
                start = time.perf_counter()
                # No real model available — simulate a small delay
                _ = inp.sum()
                end = time.perf_counter()
                timings.append(end - start)
            return timings
        except Exception:
            # Fallback to synthetic timings
            pass

    # Synthetic CPU-bound workload as fallback
    for _ in range(20):
        start = time.perf_counter()
        s = 0.0
        for i in range(size * size):
            s += (i % 7) * 0.000001
        end = time.perf_counter()
        timings.append(end - start)

    return timings


def summarize(times: List[float]) -> dict:
    if not times:
        return {}
    return {
        "count": len(times),
        "mean_s": statistics.mean(times),
        "median_s": statistics.median(times),
        "p90_s": statistics.quantiles(times, n=10)[-1],
        "min_s": min(times),
        "max_s": max(times),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OpenVINO benchmark harness")
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--size", type=int, default=224)
    args = parser.parse_args()

    all_times = []
    for _ in range(max(1, args.runs // 5)):
        t = synthetic_workload(size=args.size)
        all_times.extend(t)

    stats = summarize(all_times)
    print("OpenVINO bench (or synthetic fallback) results:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
