import matplotlib.pyplot as plt
import requests
import random
import time
import signal
import sys
from tabulate import tabulate

# Define fog node endpoints
FOG_ENDPOINTS = [
    "http://localhost:5001/filter",
    "http://localhost:5002/filter",
    "http://localhost:5003/filter",
    "http://localhost:5004/filter"
]

# Metrics
fog_request_count = [0, 0, 0, 0]
fog_total_latency = [0.0, 0.0, 0.0, 0.0]
request_latencies = []
fallbacks_used = 0

# Graceful shutdown flag
running = True

# Signal handler
def signal_handler(sig, frame):
    print("\nShutting down... generating graphs and metrics...")
    generate_graphs()
    show_summary_table()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Generate graphs
def generate_graphs():
    fog_labels = [f"Fog {i+1}" for i in range(4)]

    # Request distribution
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.bar(fog_labels, fog_request_count, color="skyblue")
    plt.title("Requests per Fog Node")
    plt.ylabel("Number of Requests")

    # Average latencies
    avg_latencies = [
        fog_total_latency[i]/fog_request_count[i] if fog_request_count[i] > 0 else 0
        for i in range(4)
    ]
    plt.subplot(1, 2, 2)
    plt.bar(fog_labels, avg_latencies, color="salmon")
    plt.title("Average Request Latency per Fog")
    plt.ylabel("Latency (s)")

    plt.tight_layout()
    plt.show()

    # Request latency trend
    plt.figure()
    plt.plot(request_latencies, marker='o', linestyle='--')
    plt.title("Latency per Request")
    plt.xlabel("Request #")
    plt.ylabel("Latency (s)")
    plt.grid()
    plt.show()

# Show final summary as table
def show_summary_table():
    avg_latencies = [
        fog_total_latency[i]/fog_request_count[i] if fog_request_count[i] > 0 else 0
        for i in range(4)
    ]
    table = []
    for i in range(4):
        table.append([
            f"Fog {i+1}",
            fog_request_count[i],
            f"{avg_latencies[i]:.4f} s"
        ])

    print("\nFinal Summary:")
    print(tabulate(table, headers=["Fog Node", "Total Requests", "Avg Latency"], tablefmt="grid"))
    print(f"\n Total fallback attempts used: {fallbacks_used}")
    print(f" Total requests sent: {sum(fog_request_count)}")

# Send data
def send_data_from_edge(i):
    global fallbacks_used

    fog_index = i // 20  # 20 devices per fog
    primary_fog = FOG_ENDPOINTS[fog_index]

    data = {
        "device_id": f"edge_{i}",
        "timestamp": time.time(),
        "vitals": {
            "heart_rate": random.randint(60, 150),
            "bp": f"{random.randint(110, 150)}/{random.randint(70, 100)}",
            "spo2": random.randint(90, 100)
        }
    }

    try:
        start = time.time()
        response = requests.post(primary_fog, json=data, timeout=1.0)
        latency = time.time() - start
        fog_request_count[fog_index] += 1
        fog_total_latency[fog_index] += latency
        request_latencies.append(latency)

    except requests.exceptions.RequestException:
        # Try fallback fogs
        for alt_index, alt_fog in enumerate(FOG_ENDPOINTS):
            if alt_index == fog_index:
                continue
            try:
                start = time.time()
                response = requests.post(alt_fog, json=data, timeout=1.0)
                latency = time.time() - start
                fog_request_count[alt_index] += 1
                fog_total_latency[alt_index] += latency
                request_latencies.append(latency)
                fallbacks_used += 1
                print(f"Edge {i} fallback from Fog {fog_index+1} to Fog {alt_index+1}")
                break
            except requests.exceptions.RequestException:
                continue

# Main loop
print("Starting continuous edge simulation... Press Ctrl+C to stop.")
edge_device_count = 80  # 20 edge devices per fog

while True:
    for i in range(edge_device_count):
        send_data_from_edge(i)
        time.sleep(0.05)
