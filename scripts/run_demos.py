"""Driver script to run demos and collect logs/artifacts.
This runs the stock agent, real-time demo, and system demo and stores outputs under bench_output/demos/<timestamp>/
"""
import asyncio
import os
from datetime import datetime
import json

ROOT = os.path.dirname(os.path.dirname(__file__))
OUT_DIR = os.path.join(ROOT, 'bench_output', 'demos')
os.makedirs(OUT_DIR, exist_ok=True)

async def run_and_capture(coro, name, out_dir):
    try:
        result = await coro()
        # If coroutine returns None that's OK; we capture None
        with open(os.path.join(out_dir, f"{name}.json"), 'w', encoding='utf-8') as f:
            json.dump({"name": name, "result": str(result)}, f, indent=2)
        return True
    except Exception as e:
        with open(os.path.join(out_dir, f"{name}_error.txt"), 'w', encoding='utf-8') as f:
            f.write(str(e))
        return False

async def run_all():
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_dir = os.path.join(OUT_DIR, ts)
    os.makedirs(out_dir, exist_ok=True)

    # Import demo functions lazily so tests can monkeypatch imports first
    from test_stock_agent import test_with_real_stock_data, test_multi_stock_monitoring
    from demo_real_time_problems import main as demo_real_time_main
    from test_system_agent import main as system_demo_main

    # Run stock tests as a grouped coroutine
    async def run_stock():
        await test_with_real_stock_data()
        await test_multi_stock_monitoring()
        return "stock_done"

    # Wrap demo mains which may be synchronous
    async def run_real_time():
        # demo_real_time_main may be synchronous; call in executor if so
        try:
            # If it's async callable, await it
            if asyncio.iscoroutinefunction(demo_real_time_main):
                await demo_real_time_main()
            else:
                demo_real_time_main()
            return "real_time_done"
        except Exception as e:
            raise

    async def run_system():
        try:
            if asyncio.iscoroutinefunction(system_demo_main):
                await system_demo_main()
            else:
                system_demo_main()
            return "system_done"
        except Exception as e:
            raise

    results = {}

    results['stock'] = await run_and_capture(run_stock, 'stock_demo', out_dir)
    results['real_time'] = await run_and_capture(run_real_time, 'real_time_demo', out_dir)
    results['system'] = await run_and_capture(run_system, 'system_demo', out_dir)

    # Summary
    with open(os.path.join(out_dir, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"Demos finished. Artifacts stored in: {out_dir}")

if __name__ == '__main__':
    asyncio.run(run_all())
