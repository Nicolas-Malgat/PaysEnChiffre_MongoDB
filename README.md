<p  align="center">
<h1  align="center">Pays en Chiffre - MongoDB</h3>
</p>

## Table of Contents

*  [Getting Started](#getting-started)

	*  [Installation](#installation)

	*  [Usage](#usage)

## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
```git
git clone https://github.com/Nicolas-Malgat/PaysEnChiffre_MongoDB.git
```
## Usage

#### To execute the program
```
python main.py
```
- [x] créer une fonction qui retourne le pays qui correspond au critère passé en paramètre. Ce paramètre est le nom du pays.
Adresse: [/api/countries?country=France](http://127.0.0.1:5000/api/countries?country=France)
	

- [x] créer une fonction qui insert un nouveau pays avec des données random (on précise uniquement le pays)
	```
	curl -X POST http://localhost:5000/api/countries/insert?name=patate
	```

- [x] réaliser une fonction pour retourner les pays qui sont regroupés par 4 tranches (à definir) de densité de population
Adresse: [/api/countries/density](http://127.0.0.1:5000/api/countries/density)

- [x] mettre la date de l'insertion lors d'une création ou mettre à jour une date de modification lors d'un changement de valeur
	- On peut choisir l'attribut à modifier après "update/" 
	- Indiquer la valeur de l'attribut dans "?value=" 
	```
	curl -X PUT "http://localhost:5000/api/countries/update/population?name=patate&value=99999"```
