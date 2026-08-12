import requests


def obtenir_meteo_site(latitude, longitude):
    """
    Interroge l'API Open-Meteo pour obtenir les métriques météo actuelles.
    Gère les erreurs réseau et de délai d'attente (timeout).
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
            "code_meteo": current.get("weathercode"),
            "statut": "OK"
        }

    except requests.exceptions.Timeout:
        print(f"[AVERTISSEMENT] Timeout lors de la connexion API pour ({latitude}, {longitude})")
        return {"temperature": None, "vent_vitesse": None, "statut": "TIMEOUT"}

    except requests.exceptions.RequestException as e:
        print(f"[AVERTISSEMENT] Erreur réseau/API météo ({latitude}, {longitude}): {e}")
        return {"temperature": None, "vent_vitesse": None, "statut": "ERREUR"}