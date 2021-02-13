from flask import Flask, request
from flask_pymongo import PyMongo
import datetime

from pymongo.message import query

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_user:1q2w3e4r@158.108.182.0:2277/exceed_backend'
mongo = PyMongo(app)
myCollection = mongo.db.g9

@app.route('/in_car', methods=['PATCH'])
def update_one():

    id = request.args.get('id')
    if(id == ""):
        return {'result' : 'No parameter'}

    filter = {'type': "park", "park_num" : int(id)}

    utc_datetime = datetime.datetime.utcnow()

    

    updated_content = {"$set": {'status' : 1}}
    myCollection.update_one(filter, updated_content)

    updated_content = {"$set": {'in_time': utc_datetime.strftime("%H:%M:%S")}}
    myCollection.update_one(filter, updated_content)

    return find()

@app.route('/create', methods=['POST'])
def insert_one():
    data = request.json

    myCollection.insert_one(data)
    return {'result': 'Created successfully'}

@app.route('/find_all', methods=['GET'])
def find():
    query = myCollection.find({"type": "park"})
    # query = myCollection.find({'type': "park", "park_num" : 2})
    output = []
    for ele in query:
        output.append({
            "park_num" : ele["park_num"],
            "all_car": ele["time_list"],
            "status": ele["status"]
            })

    return { "result": output }

@app.route('/inpark', methods=['PATCH'])
def inpark():
    flit = {'type' : 'all'}
    tmp = myCollection.find(flit)
    update_car = tmp[0]["all_car"]
    update_car += 1
    update = {"$set" : {"all_car": update_car}}
    myCollection.update_one(flit, update)
    return {"result" : "success"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='50002', debug=True)