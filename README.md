Reprenez votre brief "Les pays en chiffre" pour recréer une base de données Mongo et déporter la logique (procédure et fonction) dans une API construite en flask.

Vous devez :

[x] créer une fonction qui retourne le pays qui correspond au critère passé en paramètre. Ce paramètre est le nom du pays
[x] créer une fonction qui insert un nouveau pays avec des données random (on précise uniquement le pays)
curl -X POST http://localhost:5000/api/v1/resources/countries/insert?name=patate
[x] réaliser une fonction pour retourner les pays qui sont regroupés par 4 tranches (à definir) de densité de population
[x] mettre la date de l'insertion lors d'une création ou mettre à jour une date de modification lors d'un changement de valeur
curl -X PUT "http://localhost:5000/api/v1/countries/update/population?name=patate&value=99999"