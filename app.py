import json
import os
from logging import debug
from random import randint
from types import new_class

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo
from flask_pymongo.wrappers import Collection

from modules.loader import Loader
from modules.pays_en_chiffre import PaysEnChiffre as pec

load_dotenv('.env')
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "PaysEnChiffre"
app.config["MONGO_URI"] = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@paysenchiffre.rcjx8.mongodb.net/PaysEnChiffre?retryWrites=true&w=majority"

mongo = PyMongo(app)
db_pays: Collection = mongo.db.pays

@app.route("/")
def home_page():
    pays = db_pays.find()
    # print(articles.rewind()) # Reset du curseur sur la base de données
    return render_template(
        "index.html",
        liste = pays
    )

@app.route('/api/countries/all', methods=['GET'])
def api_all():
    response = [c for c in db_pays.find()]
    return json.dumps(response, default=str)

@app.route('/api/countries', methods=['GET'])
def api_country():
    if 'country' in request.args:
        country = request.args['country']
    else:
        return "Error: No country field provided. Please specify a country."

    response = [c for c in db_pays.find({"Country": country})]
    return json.dumps(response, default=str)

@app.route('/api/countries/density', methods=['GET'])
def api_density():
    if 'd1' in request.args:
        d1 = request.args['d1']
    else: d1 = 100
    if 'd2' in request.args:
        d2 = request.args['d2']
    else: d2 = 500
    if 'd3' in request.args:
        d3 = request.args['d3']
    else: d3 = 1000
    
    countries = [c for c in db_pays.find()]

    below_d1 = [ c for c in countries if c['Density'] in range(d1) ]
    between_d1_d2 = [ c for c in countries if c['Density'] in range(d1, d2) ]
    between_d2_d3 = [ c for c in countries if c['Density'] in range(d2, d3) ]
    over_d3 = [ c for c in countries if c['Density'] in range(d3, 999999) ]

    return json.dumps(
        [
            {f"below_{d1}":below_d1}, 
            {f"between_{d1}_{d2}":between_d1_d2}, 
            {f"between_{d2}_{d3}":between_d2_d3}, 
            {f"over_{d3}":over_d3}
        ],
        default=str
    )

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

    pays: dict = json.load(open("../datas/CURATED/pays_en_chiffre.json"))

    if mongo.db.pays:
        mongo.db.pays.drop()
    db_pays = mongo.db["pays"]
    db_pays.insert_many(pays)

    return jsonify(
        etat="success"
    )

@app.route("/api/countries/insert", methods=['POST'])
def api_insert():
    try:
        name = request.args['name']
        population = randint(1000000, 100000000)
        land_area = randint(100000, 10000000)
        yearly_change = randint(1,10)
        new_country = {
            "Country": name,
            "Population": population,
            "Yearly_Change": yearly_change,
            "Net_Change": population * yearly_change,
            "Density": population / land_area,
            "Land_Area": land_area,
            "Migrants": randint(100000,1000000),
            "Fert_Rate": randint(1,10),
            "Med_Age": randint(30,90),
            "Urban_Pop_%": randint(10,100),
            "World_Share": randint(1,10)
        }

        db_pays.insert(
            new_country
        )

        return jsonify(
            etat="success"
        )
    except:
        return jsonify(
            etat="Failed"
        )

@app.route("/api/countries/update/<key>", methods=['PUT'])
def api_update(key):
    from datetime import datetime
    try:

        name = request.args.get('name', None)
        value = request.args.get('value', None)

        updated_result = db_pays.update_one(
            {"Country":name}, 
            {'$set': {
                key: value,
                "Updated_time":datetime.now().strftime("%H:%M:%S")
            }}
        )
        return jsonify(etat="success")
    except Exception as e:

        print(e)
        return jsonify(
            etat="failed"
        )
