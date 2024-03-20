from flask import request, Flask, jsonify
from pymongo.mongo_client import MongoClient
from flask_cors import CORS
uri = "mongodb+srv://papshop:1212312121@cluster0.kjvosuu.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

app = Flask(__name__)
CORS(app)

db = client["customer"]
collection = db["cus_info"]

@app.route("/")
def Greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/customer/login/<string:username>", methods=["GET"])
def login_customer(username):
    username_found = collection.find_one({"username": username})
    if username_found:
        return jsonify(username_found)
    else:
        return jsonify({"error": "username not found"}), 404

@app.route("/customer/signup", methods=["POST"])
def signup_customer():
    data = request.get_json()
    found = collection.find_one({"_id": data['_id']})
    if found :
        return jsonify({"login": False})
    else:
        collection.insert_one(data)
        return jsonify({"login": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)