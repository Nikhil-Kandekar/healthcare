from flask import Flask, request, jsonify
import time

app = Flask(__name__)
db = []  # Simulated database

@app.route("/final_store", methods=["POST"])
def final_store():
    data = request.json
    data["cloud_received_time"] = time.time()
    db.append(data)
    return jsonify({"status": "stored", "total_records": len(db)})

@app.route("/records", methods=["GET"])
def get_all_records():
    return jsonify(db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
