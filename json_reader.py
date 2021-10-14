import json

with open('parcours/lugan/lugan_donnees.json') as json_data:
    data_dict = json.load(json_data)
    nbPoints = data_dict["nbPoints"]
    posPix = data_dict["posPix"]
    distPoints = data_dict["distPoints"]
    nbPtsPente = data_dict["nbPtsPente"]
    pentes = data_dict["pentes"]
    distPentes = data_dict["distPentes"]

    print(nbPoints)
    print(posPix)
    print(distPoints)
    print(nbPtsPente)
    print(pentes)
    print(distPentes)
