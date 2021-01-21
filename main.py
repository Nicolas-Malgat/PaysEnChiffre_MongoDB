import socket
import os
from dotenv import load_dotenv

from modules.loader import Loader

def load_csv():
    load = Loader(
        "https://simplonline-v3-prod.s3.eu-west-3.amazonaws.com/media/file/csv/25d9c746-3622-4c48-835e-d7ccafa311f5.csv"
        , "../datas/RAW/"
    )
    load.ensure_data_loaded()

def send_csv_to_mongo(csv_path):
    pass

if __name__ == "__main__":
    load_dotenv('.env')
    SECRET_KEY = os.environ.get("MONGO_USER")
    DATABASE_PASSWORD = os.environ.get("MONGO_PASSWORD")

    print(
        "mon IP:\t", socket.gethostbyname(socket.gethostname()),
        "\nmon user:\t", SECRET_KEY,
        "\nmon mdp:\t", DATABASE_PASSWORD
    )

    load_csv()
    send_csv_to_mongo(
        "../datas/RAW/" + "25d9c746-3622-4c48-835e-d7ccafa311f5.csv"
    )