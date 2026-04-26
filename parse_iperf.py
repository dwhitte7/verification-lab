import json
from pathlib import Path

for file in Path("results/iperf").glob("*.json"):
    data = json.loads(file.read_text())
    print(f"\n=== {file.name} ===")

    end = data.get("end", {})

    if "sum_received" in end:
        bps = end["sum_received"].get("bits_per_second")
        if bps is not None:
            print(f"Throughput: {bps:.2f} bps")

    if "sum" in end:
        bps = end["sum"].get("bits_per_second")
        jitter = end["sum"].get("jitter_ms")
        lost = end["sum"].get("lost_percent")

        if bps is not None:
            print(f"Throughput: {bps:.2f} bps")
        if jitter is not None:
            print(f"Jitter: {jitter} ms")
        if lost is not None:
            print(f"Loss: {lost}%")
