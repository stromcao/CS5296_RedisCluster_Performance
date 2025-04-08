#!/usr/bin/env python3
from datetime import datetime
import sys

def parse_monitor_log(filename):
    timestamps = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            if len(parts) < 2:
                continue
            try:
                timestamp_str = parts[0] + " " + parts[1]
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                timestamps.append(timestamp)
            except ValueError:
                continue
    return timestamps

def calculate_latency(log_file):
    timestamps = parse_monitor_log(log_file)
    if len(timestamps) < 2:
        return 0
    latencies = [
        (timestamps[i] - timestamps[i - 1]).total_seconds() * 1000
        for i in range(1, len(timestamps))
    ]
    avg_latency = sum(latencies) / len(latencies)
    return avg_latency

def calculate_qps(log_file):
    timestamps = parse_monitor_log(log_file)
    if len(timestamps) < 2:
        return 0
    start_time = timestamps[0]
    end_time = timestamps[-1]
    total_requests = len(timestamps)
    total_time = (end_time - start_time).total_seconds()
    qps = total_requests / total_time if total_time > 0 else 0
    return qps

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_redis_log.py <log_file>")
        sys.exit(1)
    log_file = sys.argv[1]
    avg_latency = calculate_latency(log_file)
    qps = calculate_qps(log_file)
    print(f"Log File: {log_file}")
    print(f"Average latency: {avg_latency:.3f} ms")
    print(f"Throughput (QPS): {qps:.2f} req/sec")
