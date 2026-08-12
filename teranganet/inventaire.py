# Module de chargement et de structuration de l'inventaire des equipements
import yaml


class Equipement:
    """Représente un équipement réseau (routeur, switch, serveur, etc.)."""

    def __init__(self, nom, ip, type_equipement="autre", est_actif=True, cpu_usage=0):
        self.nom = nom
        self.ip = ip
        self.type = type_equipement
        self.est_actif = est_actif
        self.cpu_usage = cpu_usage

    def __repr__(self):
        return f"<Equipement {self.nom} ({self.ip}) - Actif: {self.est_actif}>"


class Site:
    """Représente un site géographique hébergeant un ou plusieurs équipements."""

    def __init__(self, site_id, nom, latitude, longitude, equipements=None):
        self.id = site_id
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude
        self.equipements = equipements if equipements is not None else []
        self.meteo_data = None

    def ajouter_equipement(self, equipement):
        """Ajoute un objet Equipement au site."""
        self.equipements.append(equipement)

    def __repr__(self):
        return f"<Site {self.nom} ({len(self.equipements)} équipements)>"


def charger_inventaire(chemin_fichier):
    """
    Lit le fichier YAML d'inventaire et instancie les objets Site et Equipement.
    Returns:
        list[Site]: Liste des sites chargés avec leurs équipements respectifs.
    """
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    sites = []
    for site_data in data.get("sites", []):
        liste_equipements = []
        for eq_data in site_data.get("equipements", []):
            eq = Equipement(
                nom=eq_data.get("nom", "Inconnu"),
                ip=eq_data.get("ip", "0.0.0.0"),
                type_equipement=eq_data.get("type", "autre"),
                est_actif=eq_data.get("est_actif", True),
                cpu_usage=eq_data.get("cpu_usage", 0)
            )
            liste_equipements.append(eq)

        site = Site(
            site_id=site_data.get("id", "site-inconnu"),
            nom=site_data.get("nom", "Site Sans Nom"),
            latitude=site_data.get("latitude", 0.0),
            longitude=site_data.get("longitude", 0.0),
            equipements=liste_equipements
        )
        sites.append(site)

    return sites