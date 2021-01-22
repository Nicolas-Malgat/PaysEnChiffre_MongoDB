import json
import os
from logging import debug

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo

from modules.loader import Loader
from modules.pays_en_chiffre import PaysEnChiffre as pec

load_dotenv('.env')
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
# print("mon IP:\t", socket.gethostbyname(socket.gethostname()))

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "PaysEnChiffre"
app.config["MONGO_URI"] = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@paysenchiffre.rcjx8.mongodb.net/PaysEnChiffre?retryWrites=true&w=majority"

mongo = PyMongo(app)
db_pays = mongo.db.pays

@app.route("/")
def home_page():
    pays = db_pays.find()
    # print(articles.rewind()) # Reset du curseur sur la base de données
    return render_template(
        "index.html",
        liste = pays
    )

@app.route('/save-file', methods=['POST'])
def save_file():
    if 'new_file' in request.files:
        new_file = request.files['new_file']
        mongo.save_file(new_file.filename, new_file)
        data = {'Name' : request.values.get('name'), 'File Name' : new_file.filename}
        db_operations.insert(data)
        return redirect('/')

@app.route('/load_pays', methods=['GET'])
def load_pays():
    load = Loader(
        "https://simplonline-v3-prod.s3.eu-west-3.amazonaws.com/media/file/csv/25d9c746-3622-4c48-835e-d7ccafa311f5.csv"
        , "../datas/RAW/"
    )
    csv_path = load.ensure_data_loaded()
    pec.clean_csv(
        '../datas/RAW/' + csv_path,
        "../datas/CURATED/pays_en_chiffre.csv")
    pec.jsonify_csv(
        "../datas/CURATED/pays_en_chiffre.csv", 
        "../datas/CURATED/pays_en_chiffre.json"
    )


    pays = json.loads(open("../datas/CURATED/pays_en_chiffre.json").read())
    db_pays.insert_many(
        pays
    )

    return jsonify(
        etat="success"
    )
