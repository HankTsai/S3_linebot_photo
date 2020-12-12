from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

import os
@app.route('/os-envir')
def get_os_env():
    line_channel_access_token=os.environ['line_channel_access_token']
    line_channel_secret= os.environ['line_channel_secret']
    return line_channel_access_token + "  " + line_channel_secret

from pymongo import MongoClient
import datetime
@app.route('/db-demo-insert')
def insert_data_to_db():
    client = MongoClient( os.environ['line_db_host'], 27017)
    db = client.test_database
    collection = db.test_collection
    post = {"author": "Mike","date": datetime.datetime.utcnow()}
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    return ""

app.run(host='0.0.0.0',port=5000)