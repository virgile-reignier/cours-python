import requests
import json

### Exercice 1 :

url = "https://dicotopo.cths.fr/api/1.0/search?query=dep-id:34 AND text-date:<=1300"
response = requests.get(url)
if response.status_code == 200:
    data = json.loads(response.text)
    with open('resultats/herault_old_labels.json', 'w') as f:
        json.dump(data, f)
else:
    print(f"Error fetching data: {response.status_code}")

### Exercice 2 :

url = "https://dicotopo.cths.fr/api/1.0/search?query=label:abbeville AND dep-id:80"
response = requests.get(url)
if response.status_code == 200:
    data = json.loads(response.text)
    print(len(data["data"]))
    communes = []
    for toponyme in data["data"]:
        if toponyme["attributes"]["localization-insee-code"] not in communes:
            communes.append(toponyme["attributes"]["localization-insee-code"])
    print(len(communes))
else:
    print(f"Error fetching data: {response.status_code}")

### Exercice 3 :

from bs4 import BeautifulSoup
import csv

# Commencer par créer votre propre compte utilisateur sur geonames
username_geonames = "demo"

results = []
# On part de la variable communes définie dans l'exercice 2
for commune in communes:
    content_line = {}
    url_dicotopo = "https://dicotopo.cths.fr/api/1.0/communes/" + commune + "?without-relationships"
    data_dictotopo = json.loads(requests.get(url_dicotopo).text)["data"]
    content_line["nom"] = data_dictotopo["attributes"]["NCCENR"]
    content_line["code INSEE"] = commune
    content_line["id DicoTopo"] = data_dictotopo["attributes"]["place-id"]
    id_geonames = data_dictotopo["attributes"]["geoname-id"]
    url_geonames = "http://api.geonames.org/get?geonameId=" + id_geonames + "&username=" + username_geonames
    response_geonames = requests.get(url_geonames)
    if response_geonames.status_code == 200:
        data_geonames = BeautifulSoup(response_geonames.text, features="xml")
        content_line["description"] = data_geonames.find("fcodeName").get_text()
        content_line["habitants"] = data_geonames.find("population").get_text()
    else:
        print(f"Error fetching data: {response.status_code}")
    results.append(content_line)
    
with open('resultats/geonames.csv', 'w', newline='') as csvfile:
    fieldnames = ['nom', 'code INSEE', 'id DicoTopo', 'description', 'habitants']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for line in results:
        writer.writerow(line)