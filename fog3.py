from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)
CLOUDLET_URL = "http://localhost:5006/store"  # Assign each fog to a cloudlet

@app.route("/filter", methods=["POST"])
def filter_and_forward():
    data = request.json
    start = time.time()
    
    # Simulate filtering (could add rules here)
    if data.get("vitals", {}).get("heart_rate", 0) > 100:
        data["flag"] = "High Heart Rate"
    
    resp = requests.post(CLOUDLET_URL, json=data)
    latency = time.time() - start
    return jsonify({"fog_to_cloudlet_latency": latency, "cloudlet_response": resp.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)  # Change to 5002, 5003, etc. for other fogs
