from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)
CLOUD_URL = "http://localhost:5007/final_store"

@app.route("/store", methods=["POST"])
def cloudlet_store():
    data = request.json
    data["cloudlet_timestamp"] = time.time()
    
    # Simulate processing delay
    time.sleep(0.05)
    
    resp = requests.post(CLOUD_URL, json=data)
    return jsonify({"cloudlet_to_cloud": resp.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)  
