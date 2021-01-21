from flask import Flask
from flask import render_template
from flask import request
from flask_pymongo import PyMongo

from dotenv import load_dotenv
import os
import socket

load_dotenv('.env')
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
# print("mon IP:\t", socket.gethostbyname(socket.gethostname()))

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "PaysEnChiffre"
app.config["MONGO_URI"] = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@paysenchiffre.rcjx8.mongodb.net/PaysEnChiffre?retryWrites=true&w=majority"

print(app.config["MONGO_URI"])

mongo = PyMongo(app)

print(
    "\n"
    , mongo.db.articles
    , "\n"
)

db_articles = mongo.db.articles

@app.route("/")
def home_page():
    online_users = db_articles.find({"price": 200})
    print([user for user in online_users])
    return render_template(
        "index.html",
        online_users = online_users
    )

@app.route('/save-file', methods=['POST'])
def save_file():
    if 'new_file' in request.files:
        new_file = request.files['new_file']
        mongo.save_file(new_file.filename, new_file)
        data = {'Name' : request.values.get('name'), 'File Name' : new_file.filename}
        db_operations.insert(data)
        return redirect('/')