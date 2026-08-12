#!/usr/bin/env python3
import argparse
import sys
import yaml

from teranganet.inventaire import charger_inventaire
from teranganet.meteo import obtenir_meteo_site
from teranganet.rapport import generer_rapport


def charger_config(chemin_config):
    """Charge le fichier de configuration YAML pour les seuils d'alerte."""
    try:
        with open(chemin_config, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[ERREUR] Impossible de lire le fichier de configuration '{chemin_config}': {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="TerangaNet Ops Toolkit - Outil d'audit réseau & météo"
    )
    parser.add_argument(
        "-c", "--config",
        default="config.yaml",
        help="Chemin du fichier de configuration (défaut: config.yaml)"
    )
    parser.add_argument(
        "-i", "--inventaire",
        default="data/equipements.yaml",
        help="Chemin du fichier d'inventaire (défaut: data/equipements.yaml)"
    )
    parser.add_argument(
        "-o", "--output",
        default="rapports/audit_rapport.json",
        help="Chemin de sortie du rapport JSON (défaut: rapports/audit_rapport.json)"
    )
    parser.add_argument(
        "--no-meteo",
        action="store_true",
        help="Désactiver l'interrogation de l'API météo Open-Meteo"
    )

    args = parser.parse_args()

    print("=== TerangaNet Ops Toolkit ===")
    print(f"[+] Chargement de la configuration : {args.config}")
    config = charger_config(args.config)

    print(f"[+] Chargement de l'inventaire : {args.inventaire}")
    try:
        sites = charger_inventaire(args.inventaire)
    except Exception as e:
        print(f"[ERREUR] Échec du chargement de l'inventaire: {e}")
        sys.exit(1)

    if not args.no_meteo:
        print("[+] Collecte des données météorologiques...")
        for site in sites:
            lat = getattr(site, "latitude", None)
            lon = getattr(site, "longitude", None)
            if lat is not None and lon is not None:
                site.meteo_data = obtenir_meteo_site(lat, lon)

    print("[+] Lancement de l'audit et génération du rapport...")
    rapport = generer_rapport(sites, config, fichier_sortie=args.output)

    print(f"\n[OK] Audit terminé avec succès.")
    print(f" -> Rapport sauvegardé dans : {args.output}")
    print(f" -> Total sites audités     : {rapport['metriques_globales']['total_sites']}")
    print(f" -> Total alertes détectées : {rapport['metriques_globales']['total_alertes']}")


if __name__ == "__main__":
    main()