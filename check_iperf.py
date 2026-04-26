import json
import sys
from pathlib import Path

udp_file = Path("results/iperf/udp.json")
tcp_file = Path("results/iperf/tcp.json")

failed = False

if udp_file.exists():
    udp = json.loads(udp_file.read_text())
    end = udp.get("end", {})
    s = end.get("sum", {})
    udp_bps = s.get("bits_per_second", 0)
    jitter = s.get("jitter_ms", 999999)
    loss = s.get("lost_percent", 100)

    print("UDP results:")
    print(f"  throughput: {udp_bps:.2f} bps")
    print(f"  jitter:     {jitter} ms")
    print(f"  loss:       {loss}%")

    if udp_bps < 90_000_000:
        print("FAIL: UDP throughput below 90 Mbps")
        failed = True
    if loss > 0.5:
        print("FAIL: UDP loss above 0.5%")
        failed = True
    if jitter > 5:
        print("FAIL: UDP jitter above 5 ms")
        failed = True

if tcp_file.exists():
    tcp = json.loads(tcp_file.read_text())
    end = tcp.get("end", {})
    s = end.get("sum_received", {})
    tcp_bps = s.get("bits_per_second", 0)

    print("TCP results:")
    print(f"  throughput: {tcp_bps:.2f} bps")

    if tcp_bps <= 0:
        print("FAIL: TCP throughput missing or zero")
        failed = True

if failed:
    sys.exit(1)

print("PASS: iPerf checks passed")
