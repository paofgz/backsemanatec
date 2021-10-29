from flask import Flask
from flask import request
from flask import jsonify
from flask_pymongo import pymongo
from bson import json_util
import ssl
import json
import uuid
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

CONNECTION_STRING = "mongodb+srv://paofgz:Bob,esponja0@cluster0.erpn5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING, ssl_cert_reqs=ssl.CERT_NONE)
db = client.get_database('flask_mongodb_atlas')
covidlogs_collection = pymongo.collection.Collection(
    db, 'covidlogs_collection')


@app.route("/covidlogs/list", methods=['GET'])
def list_logs():
    logs = covidlogs_collection.find()
    response = [log for log in logs]
    return json.dumps(response, default=json_util.default)


@app.route("/covidlogs/list/searches", methods=['GET'])
def count_searches():
    response = covidlogs_collection.aggregate(
        [{
            "$group":
            {"_id": "$country",
             "total": {"$sum": 1}
             }}
         ])
    res = [log for log in response]
    return json.dumps(res, default=json_util.default)


@app.route("/covidlogs/add_log", methods=['POST'])
def post_log():
    data = request.json
    date = str(datetime.now())
    covidlogs_collection.insert_one(
        {"_id": str(uuid.uuid4()), "country": data["country"], "confirmed": data["pos"], "deaths": data["death"], "search_date": date})
    return "Log created "
