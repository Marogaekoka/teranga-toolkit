import requests


def obtenir_meteo_site(latitude, longitude):
    """
    Interroge l'API Open-Meteo pour obtenir les métriques météo actuelles
    en fonction des coordonnées GPS du site.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather", {})
        return {
            "temperature": current.get("temperature"),
            "vent_vitesse": current.get("windspeed"),
            "code_meteo": current.get("weathercode")
        }
    except Exception as e:
        print(f"[AVERTISSEMENT] Échec de la collecte météo ({latitude}, {longitude}): {e}")
        return {
            "temperature": None,
            "erreur": str(e)
        }