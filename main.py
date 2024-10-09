from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
import enum
import pandas as pd

# Définir le modèle de base
Base = declarative_base()


# Définir l'énumération pour Acces
class Acces(enum.Enum):
    Exterieur = "Exterieur"
    Interieur = "Interieur"


# Définir la classe DaeEntity
class DaeEntity(Base):
    __tablename__ = 'dae'  # Nom de la table en minuscules

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    latitude = Column(Numeric(precision=12, scale=8))
    longitude = Column(Numeric(precision=12, scale=8))
    adresse_num = Column(String)
    adresse_voie = Column(String)
    adresse_cp = Column(String)
    adresse_commune = Column(String)
    acces = Column(Enum(Acces))  # Utilisation de l'énumération pour acces
    acces_libre = Column(Boolean)
    photo = Column(String)
    dispo_jour = Column(String)
    dispo_heure = Column(String)
    etat_fonctionnement = Column(String)


# Créer une connexion à la base de données PostgreSQL
engine = create_engine('postgresql://postgres:postgres@localhost:5432/lifeline')  # Port 5432

Base.metadata.create_all(engine)  # Crée les tables

# Créer une session
Session = sessionmaker(bind=engine)
session = Session()


# Fonction pour enregistrer un DaeEntity
def save_dae(dae_entity):
    session.add(dae_entity)
    session.commit()
    print(f"DaeEntity inserted with id: {dae_entity.id}")


# Exemple d'utilisation

df = pd.read_csv("geodae.csv", delimiter=';')

for index, row in df.iterrows():
    lat = row["c_lat_coor1"]
    long = row["c_long_coor1"]

    if -90 <= lat <= 90 and -180 <= long <= 180:
        new_dae = DaeEntity(
            id=row["gid"],
            name=row["c_nom"],
            latitude=lat,
            longitude=long,
            adresse_num=row["c_adr_num"],
            adresse_voie=row["c_adr_voie"],
            adresse_cp=row["c_com_cp"],
            adresse_commune=row["c_com_nom"],
            acces=Acces.Exterieur,
            acces_libre=False,
            photo=row["cc_photo1"],
            dispo_jour=row["c_disp_j"],
            dispo_heure=row["c_disp_h"],
            etat_fonctionnement=row["c_etat_fonct"]
        )
        if (row["c_acc"] == "Intérieur"):
            new_dae.acces = Acces.Interieur
        if (row["c_acc_lib"] == 't'):
            new_dae.accesLibre = True
        save_dae(new_dae)
    else:
        print(f"Invalid coordinates: Latitude {lat}, Longitude {long}")

session.close()
