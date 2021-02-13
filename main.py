from flask import Flask, request
from flask_pymongo import PyMongo
import datetime
import math

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_user:1q2w3e4r@158.108.182.0:2277/exceed_backend'
mongo = PyMongo(app)
myCollection = mongo.db.g9


@app.route('/in_car', methods=['PATCH'])
def update_one():
    park_num = request.args.get('id')
    if park_num == "":
        return {'result': 'No parameter'}

    filt = {'type': "park", "park_num": int(park_num)}

    que = myCollection.find_one(filt)
    status = que['status']

    if status == 1:
        return {"result": "Already have a car in park {}".format(id)}

    in_time = datetime.datetime.now().timestamp()

    updated_content = {"$set": {'status': 1}}
    myCollection.update_one(filt, updated_content)

    updated_content = {"$set": {'in_time': in_time}}
    myCollection.update_one(filt, updated_content)

    return {"result": "Updated successful"}


@app.route('/get_data', methods=['GET'])
def get_data():
    P1 = myCollection.find_one({'type': "park", "park_num": 1})
    P2 = myCollection.find_one({'type': "park", "park_num": 2})
    P3 = myCollection.find_one({'type': "park", "park_num": 3})
    P4 = myCollection.find_one({'type': "park", "park_num": 4})
    ALL = myCollection.find_one({'type': "all"})
    min_price = 20
    out = {
        "P1": {
            "all_time": P1['all_time'],
            "this_park_time": 0,
            "status": P1['status'],
            "charge": P1['all_time']*min_price,
            "uncharge": 0
        },
        "P2": {
            "all_time": P2['all_time'],
            "this_park_time": 0,
            "status": P2['status'],
            "charge": P2['all_time']*min_price,
            "uncharge": 0
        },
        "P3": {
            "all_time": P3['all_time'],
            "this_park_time": 0,
            "status": P3['status'],
            "charge": P3['all_time']*min_price,
            "uncharge": 0
        },
        "P4": {
            "all_time": P4['all_time'],
            "this_park_time": 0,
            "status": P4['status'],
            "charge": P4['all_time']*min_price,
            "uncharge": 0
        },
        "ALL": {
            "all_time": ALL['all_time'],
            "all_car": ALL['all_car'],
            "all_money": ALL['all_money'],
        }
    }
    if P1['status'] == 1:
        out['P1']['this_park_time'] = datetime.datetime.now().timestamp() - \
            P1['in_time']
        out['P1']['uncharge'] = min_price * \
            math.ceil(
                (datetime.datetime.now().timestamp() - P1['in_time']) / 60)
    if P2['status'] == 1:
        out['P2']['this_park_time'] = datetime.datetime.now().timestamp() - \
            P2['in_time']
        out['P2']['uncharge'] = min_price * \
            math.ceil(
                (datetime.datetime.now().timestamp() - P2['in_time']) / 60)
    if P3['status'] == 1:
        out['P3']['this_park_time'] = datetime.datetime.now().timestamp() - \
            P3['in_time']
        out['P3']['uncharge'] = min_price * \
            math.ceil(
                (datetime.datetime.now().timestamp() - P3['in_time']) / 60)
    if P4['status'] == 1:
        out['P4']['this_park_time'] = datetime.datetime.now().timestamp() - \
            P4['in_time']
        out['P4']['uncharge'] = min_price * \
            math.ceil(
                (datetime.datetime.now().timestamp() - P4['in_time']) / 60)

    return out


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
            "park_num": ele["park_num"],
            "all_car": ele["time_list"],
            "status": ele["status"]
        })

    return {"result": output}


@app.route('/in_park', methods=['PATCH'])
def in_park():
    filt = {'type': 'all'}
    tmp = myCollection.find(filt)
    update_car = tmp[0]["all_car"]
    update_car += 1
    update = {"$set": {"all_car": update_car}}
    myCollection.update_one(filt, update)
    return {"result": "success"}


@app.route('/', methods=['GET'])
def hello():
    return {"name": "G9"}


@app.route('/out_car', methods=['PATCH'])
def out_car():
    park_num = request.args.get('id')
    if park_num == "":
        return {'result': 'No parameter'}

    filt = {'type': "park", "park_num": int(park_num)}

    que = myCollection.find_one(filt)

    status = que['status']
    in_time = que['in_time']
    time_list = que['time_list']
    money_list = que['money_list']
    all_time = que['all_time']
    all_money = que['all_money']
    out_time = datetime.datetime.now().timestamp()

    if status == 0:
        return {"result": "Not have car in park {}".format(id)}

    time_interval = math.ceil(out_time/60 - in_time/60)
    res_money = 20*time_interval

    time_list.append(time_interval)
    all_time += time_interval
    money_list.append(res_money)
    all_money += res_money

    tmp = myCollection.find({'type': 'all'})
    money = tmp[0]['all_money']
    money += res_money
    updated_all_money = {'$set': {'all_money': money}}
    myCollection.update_one({'type': 'all'}, updated_all_money)

    timesec = time_interval
    t = tmp[0]['all_time']
    t += timesec
    updated_all_time = {'$set': {'all_time': t}}
    myCollection.update_one({'type': 'all'}, updated_all_time)

    updated_status = {"$set": {'status': 0}}
    myCollection.update_one(filt, updated_status)

    updated_in_time = {"$set": {'in_time': 0}}
    myCollection.update_one(filt, updated_in_time)

    updated_time = {"$set": {'all_time': all_time}}
    myCollection.update_one(filt, updated_time)

    updated_money = {"$set": {'all_money': all_money}}
    myCollection.update_one(filt, updated_money)

    updated_money_list = {"$set": {'money_list': money_list}}
    myCollection.update_one(filt, updated_money_list)

    updated_time_list = {"$set": {'time_list': time_list}}
    myCollection.update_one(filt, updated_time_list)

    return {"result": "Out Successfully"}


@app.route("/reset", methods=["PATCH"])
def reset():
    filt = {'type': "park"}
    all_data = myCollection.find(filt)
    for i in all_data:
        filt = {'park_num': i["park_num"]}
        updated_content = {"$set": {
            "type": "park",
            "park_num": i["park_num"],
            "status": 0,
            "all_time": 0,
            "all_money": 0,
            "time_list": [],
            "money_list": [],
            "in_time": 0
        }}
        myCollection.update_one(filt, updated_content)

    filt = {"type": "all"}
    updated_content = {'$set': {
                       'all_car': 0,
                       'all_time': 0,
                       'all_money': 0
                       }}
    myCollection.update_one(filt, updated_content)
    return {"result": "Reset Successfully"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)
