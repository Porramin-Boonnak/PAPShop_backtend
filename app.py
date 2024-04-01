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

dbpro = client["product"]
collectionpro = dbpro["pro_info"]

collectionbill = db["bill"]
collectionaddress = db["address"]

@app.route("/")
def Greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/customer/login/<string:_id>", methods=["GET"])
def login_customer(_id):
    username_found = collection.find_one({"_id": _id})
    if username_found:
        return jsonify(username_found)
    else:
        return jsonify({"error": "username not found"}), 404
    
@app.route("/product", methods=["GET"])
def get_product():
    product = collectionpro.find()
    if product:
        return jsonify(list(product))
    else:
        return jsonify({"error": "product not found"}), 404

@app.route("/product/insert", methods=["POST"])
def insert_product():
    data = request.get_json()
    collectionpro.insert_one(data)

@app.route("/product/array", methods=["POST"])
def get_product_array():
    data = request.get_json()
    product = []
    for x in data['data']:
     product.append(collectionpro.find_one({"_id":x['res']}))
    
    return jsonify(list(product))
    
@app.route("/product/<string:_id>", methods=["PUT"])
def PUT_product(_id):
    product = collectionpro.find_one({"_id":_id})
    if product:
        data = request.get_json()
        collectionpro.update_one({"_id": _id}, {"$set": data})
        product = collectionpro.find_one({"_id":_id})
        return jsonify(product)
    else:
        return jsonify({"error": "product not found"}), 404

@app.route("/product/<string:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = collectionpro.find_one({"_id": product_id})
    if product:
        collectionpro.delete_one({"_id": product_id})
        return jsonify({"message": "product deleted successfully"}), 200
    else:
        return jsonify({"error": "product not found"}), 404
    
@app.route("/product/<string:_id>", methods=["GET"])
def GET_one_product(_id):
    product = collectionpro.find_one({"_id": _id})
    if product:
        return jsonify(product)
    else:
        return jsonify({"found": False}), 404

@app.route("/customer/signup", methods=["POST"])
def signup_customer():
    data = request.get_json()
    found = collection.find_one({"_id": data['_id']})
    if found :
        return jsonify({"login": False})
    else:
        collection.insert_one(data)
        return jsonify({"login": True})

@app.route("/bill", methods=["POST"])
def insert_bill():
    data = request.get_json()
    collectionbill.insert_one(data)

@app.route("/bill/<string:_id>", methods=["GET"])
def GET_bill(_id):
    bill = collectionbill.find_one({"_id": _id})
    if bill:
        return jsonify(bill)
    else:
        return jsonify({"found": False}), 404

@app.route("/bill/<string:_id>", methods=["PUT"])
def PUT_bill(_id):
    bill = collectionbill.find_one({"_id": _id})
    if bill:
        data = request.get_json()
        collectionbill.update_one({"_id": _id}, {"$set": data})
        bill = collectionbill.find_one({"_id": _id})
        return jsonify(list(bill))
    else:
        return jsonify({"error": "bill not found"}), 404

@app.route("/address", methods=["POST"])
def address_customer():
    data = request.get_json()
    found = collectionaddress.find_one({"_id": data['_id']})
    if found :
        collectionaddress.update_one({"_id": data['_id']}, {"$set": data})
        return jsonify({"succsess": False})
    else:
        collectionaddress.insert_one(data)
        return jsonify({"succsess": True})

@app.route("/address/<string:_id>", methods=["GET"])
def GET_one_address(_id):
    address = collectionaddress.find_one({"_id": _id})
    return jsonify(address)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)