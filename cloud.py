from flask import Flask, request, jsonify
from pymongo import MongoClient
import time

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["healthcare_db"]
collection = db["cloud_records"]

@app.route("/final_store", methods=["POST"])
def final_store():
    data = request.json
    data["cloud_received_time"] = time.time()
    result = collection.insert_one(data)
    return jsonify({
        "status": "stored",
        "inserted_id": str(result.inserted_id),
        "total_records": collection.count_documents({})
    })

@app.route("/records", methods=["GET"])
def get_all_records():
    records = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB internal _id
    return jsonify(records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
