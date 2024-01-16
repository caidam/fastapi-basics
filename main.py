# Importe la classe FastAPI depuis le module fastapi
from fastapi import FastAPI
import pandas as pd

# Création d'un dataframe qui va contenir les données interrogées par l'API
df = pd.read_csv('communes_france.csv', index_col=0)

# Crée une instance de l'application FastAPI
app = FastAPI()

# Définis une route pour l'URL "/"
# Lorsqu'un client accède à cette URL avec une méthode GET, la fonction "root" sera appelée
@app.get("/")
def root():
    """
    Renvoie un message de bievenue.
    
    """
    # Le contenu de cette fonction sera renvoyé comme réponse à la requête
    return {"message": "Bonjour"}
    

# Nombre de villes par région
@app.get("/regions/city-count")
def get_cities_by_region():
    """
    Récupère le nombre de villes par région.
    """
    
    cities_by_region = df.groupby('nom_region')['nom_commune_complet'].count()

    return cities_by_region.to_dict()
    
# Nombre de villes par département d'une région donnée
@app.get("/{region}/departments/city-count")
def get_cities_by_department(region):
    """
    Récupère le nombre de villes par département en fonction d'une région.
    """ 
    if region in df['nom_region'].tolist():

        cities_by_department = df[df['nom_region'] == region]\
            .groupby('nom_departement')['nom_commune_complet'].count()
        
        return cities_by_department.to_dict()
    
    else:
        return "Nom de région invalide"

# Communes et codes commune INSEE d'un département
@app.get("/{department}/cities")
def get_cities_in_department(department):
    """
    Récupère la liste des communes et codes commune INSEE respectifs d'un département.
    """

    cities_in_department = df[df['nom_departement'] == department]\
        [['nom_commune_complet', 'code_commune_INSEE']].set_index('nom_commune_complet')
    
    return cities_in_department.to_dict()

# Informations d'un code commune INSEE
@app.get("/cities/{insee_code}")
def get_city_information(insee_code):
    """
    Récupère les informations liées à un code commune INSEE
    """

    city_information = df[df['code_commune_INSEE'] == insee_code].iloc[0]
    
    return city_information.to_dict()
