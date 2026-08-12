# TerangaNet Ops Toolkit 🛠️

**TerangaNet Ops Toolkit** est un outil en ligne de commande (CLI) développé en Python pour automatiser l'audit d'équipements réseau localisés sur différents sites au Sénégal. Il combine des données d'inventaire local, des seuils de configuration et les conditions météorologiques en temps réel pour émettre des alertes.

---

## 📌 Fonctionnalités

* **Gestion d'inventaire :** Lecture et structuration des données multi-sites et équipements depuis un fichier YAML (`data/equipements.yaml`).
* **Intégration Météo en Direct :** Récupération de la température et de la vitesse du vent via l'API Open-Meteo pour chaque site.
* **Moteur d'Audit :** Analyse du statut d'activité des équipements et contrôle des métriques (utilisation CPU, météo) par rapport aux seuils configurés (`config.yaml`).
* **Rapports JSON :** Export structuré et horodaté des résultats d'audit dans `rapports/audit_rapport.json`.

---

## 🚀 Installation & Prérequis

### Prérequis
* Python 3.8 ou supérieur
* Git

### Installation
1. Cloner le dépôt :
   ```bash
   git clone [https://github.com/Marogaekoka/teranga-toolkit.git](https://github.com/Marogaekoka/teranga-toolkit.git)
   cd teranga-toolkit
 ## 👥 Auteurs & Répartition du travail
* **Membre A :** Gestion de l'inventaire YAML (`data/equipements.yaml`), intégration de l'API Open-Meteo (`teranganet/meteo.py`) et tests unitaires (`tests/test_inventaire.py`).
* **Membre B :** Logique du moteur d'audit (`teranganet/rapport.py`), interface CLI (`toolkit.py`), documentation (`README.md`) et gestion des dépendances (`requirements.txt`).
* > *Projet réalisé dans le cadre de la soutenance finale d'administration réseau.*
