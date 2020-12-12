# V1

## 目的

展示IDE集成docker-compose
展示環境變數的使用

## 流程

創建Pycharm專案

設定Pipfile
```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]
"flask" = "1.11.0"
"line-bot-sdk"="*"
"pymongo"="3.9.0"
"boto3"="*"

[requires]
python_version = "3.8"
```

設定.gitignore
```
.idea
```

設定dockerfile
```
FROM python:3.8.5
WORKDIR /app
# COPY Pipfile Pipfile.lock /app/
COPY . /app
RUN pip install pipenv
RUN pipenv update;pipenv install --system --deploy
EXPOSE 5000
CMD ["python", "app.py"]
```

設定docker-compose.yml
```
version: '3'

services:
  flask-chatbot.pri:
    build:
      context: .
      dockerfile: dockerfile
    ports:
        - "5000:5000"
    environment:
      line_channel_access_token: 'Your line chatbot access token'
      line_channel_secret: 'Your line channel secret'
      line_db_host: 'mongo.pri'
    volumes:
        - .:/app
```
設定Python interprter 為 remote docker compose

設定Run configuration 為 docker compose

編寫app.py
```
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

```

運行服務，訪問以下路徑
```
localhost:5000
localhost:5000/os-envir
```


# V2 - 集成第二個Container 

在docker-compose.yml檔的底下，追加ngrok服務
```
  ngrok-temp:
    image: wernight/ngrok
    ports:
      - "4040:4040"
    command: ngrok http flask-chatbot.pri:5000 -region ap
    depends_on:
      - flask-chatbot.pri
```

重新deploy服務，訪問localhost:4040

# V3 - 集成資料庫服務

在docker-compose.yml的底下，追加mongo與mongo-express
```
  mongo.pri:
    image: mongo:3.6.12
    container_name: mongo.pri
    restart: always

  mongo-express.pri:
    image: mongo-express:0.54.0
    restart: always
    ports:
      - 8081:8081
    environment:
      ME_CONFIG_MONGODB_SERVER: mongo.pri

```

運行服務，訪問以下路徑
```
localhost:5000
localhost:5000/os-envir
localhost:5000/db-demo-insert

localhost:8081
```

