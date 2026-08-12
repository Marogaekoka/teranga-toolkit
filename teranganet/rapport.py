import json
import os
from datetime import datetime


def auditer_equipement(equipement, meteo_site, config):
    """
    Effectue l'audit d'un équipement en comparant ses métriques
    aux seuils définis dans le fichier de configuration.
    """
    alertes = []
    seuils = config.get("seuils", {})

    # 1. Vérification de la disponibilité (Statut)
    if not getattr(equipement, "est_actif", True):
        alertes.append({
            "niveau": "CRITIQUE",
            "message": "Équipement hors ligne / injoignable"
        })

    # 2. Vérification de la température extérieure du site
    temp_max = seuils.get("temperature_max_celsius", 40)
    if meteo_site and "temperature" in meteo_site:
        if meteo_site["temperature"] > temp_max:
            alertes.append({
                "niveau": "ATTENTION",
                "message": f"Température du site élevée ({meteo_site['temperature']}°C > {temp_max}°C)"
            })

    # 3. Vérification de la charge CPU (si disponible)
    cpu_max = seuils.get("cpu_max_pct", 85)
    cpu_usage = getattr(equipement, "cpu_usage", None)
    if cpu_usage is not None and cpu_usage > cpu_max:
        alertes.append({
            "niveau": "AVERTISSEMENT",
            "message": f"Charge CPU critique ({cpu_usage}% > {cpu_max}%)"
        })

    statut_audit = "CONFORME" if not alertes else "NON_CONFORME"

    return {
        "nom": getattr(equipement, "nom", "Inconnu"),
        "ip": getattr(equipement, "ip", "0.0.0.0"),
        "type": getattr(equipement, "type", "autre"),
        "statut_audit": statut_audit,
        "alertes": alertes
    }


def generer_rapport(sites, config, fichier_sortie=None):
    """
    Parcourt l'ensemble des sites et génère un rapport global sérialisé en JSON.
    """
    résultats_sites = []
    total_alertes = 0

    for site in sites:
        meteo_data = getattr(site, "meteo_data", None)
        audit_equipements = []

        equipements = getattr(site, "equipements", [])
        for eq in equipements:
            res_audit = auditer_equipement(eq, meteo_data, config)
            audit_equipements.append(res_audit)
            total_alertes += len(res_audit["alertes"])

        résultats_sites.append({
            "site_id": getattr(site, "id", "Inconnu"),
            "site_nom": getattr(site, "nom", "Sans nom"),
            "meteo_actuelle": meteo_data,
            "equipements": audit_equipements
        })

    rapport = {
        "timestamp": datetime.now().isoformat(),
        "projet": "TerangaNet Ops Toolkit",
        "metriques_globales": {
            "total_sites": len(sites),
            "total_alertes": total_alertes
        },
        "sites": résultats_sites
    }

    if fichier_sortie:
        dossier = os.path.dirname(fichier_sortie)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        with open(fichier_sortie, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=4, ensure_ascii=False)

    return rapport