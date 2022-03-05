from flask import Flask
from pymongo import MongoClient
from flask_mongoengine import MongoEngine

app = Flask(__name__)

client = MongoClient("mongodb+srv://practicedb:practicedb@cluster0.73alj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = MongoEngine()
db.init_app(app)

from application import routes