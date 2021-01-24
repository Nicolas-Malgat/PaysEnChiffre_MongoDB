import csv
import json
from flask.json import jsonify
import pandas as pd
from pandas.core.base import DataError
from pandas.core.series import Series
import re

class PaysEnChiffre:
    """
    docstring
    """

    @staticmethod
    def clean_csv(csv_path, target):
        pays: pd.DataFrame = pd.read_csv(csv_path)

        def clean_columns(column):
            column = re.sub("\(.+\)", '', column)
            column = column.strip().replace(' ', '_').replace('.', '')
            return column
            
        pays = pays.rename(columns=clean_columns)
        
        def clean_row(col):
            col_values = []

            for value in col:
                if type(value) != str:
                    col_values.append(value)
                    continue

                value = value.replace('%', '').strip()

                if value.lower().islower(): # verifie que la value contient du texte
                    # if value == "N.A.":
                    #     col_values.append(0)
                    #     continue
                    pass
                else:
                    try:
                        value = int(value)          # verifie si la value contient un int
                    except ValueError as e:
                        value = float(value)        # la ligne contient un float

                col_values.append(value)
            return Series(col_values)

        pays = pays.apply(clean_row)
        pays.to_csv(target, index=False)


    @staticmethod
    def jsonify_csv(csv_path, target):
        """
        docstring
        """
        pays: pd.DataFrame = pd.read_csv(csv_path)
        pays.to_json(target, orient="records")

if __name__ == "__main__":
    PaysEnChiffre.clean_csv(
        '../datas/RAW/25d9c746-3622-4c48-835e-d7ccafa311f5.csv',
        "../datas/CURATED/pays_en_chiffre.csv"
    )

    PaysEnChiffre.jsonify_csv(
        "../datas/CURATED/pays_en_chiffre.csv", 
        "../datas/CURATED/pays_en_chiffre.json"
    )