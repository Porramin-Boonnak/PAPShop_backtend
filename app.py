from flask import request, Flask, jsonify
from pymongo.mongo_client import MongoClient
from flask_cors import CORS
uri = "mongodb+srv://shopmongo:1212312121@cluster0.kjvosuu.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

app = Flask(__name__)
CORS(app)

db = client["customer"]
collection = db["cus_info"]

@app.route("/")
def Greet():
    return "<p>Welcome to Student Management API</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)