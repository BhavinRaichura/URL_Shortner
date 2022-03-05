from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient("mongodb+srv://<user>:<password>@cluster0.73alj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client
db.init_app(app)

from application import routes