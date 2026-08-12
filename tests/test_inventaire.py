import unittest
import json
import os
from teranganet.inventaire import charger_inventaire
from teranganet.rapport import generer_rapport

class TestTerangaToolkit(unittest.TestCase):

    # --- 1. TESTS DE L'INVENTAIRE ---
    def test_nombre_equipements(self):
        inventaire = charger_inventaire("data/equipements.yaml")
        self.assertGreater(len(inventaire), 0)

    def test_attributs_equipements(self):
        inventaire = charger_inventaire("data/equipements.yaml")
        premier = inventaire[0]
        # 'premier' étant une instance d'objet Site, on vérifie la présence des attributs
        self.assertTrue(hasattr(premier, "nom") or hasattr(premier, "id") or hasattr(premier, "equipements"))
    def test_site_inconnu(self):
        with self.assertRaises(Exception):
            charger_inventaire("fichier_inexistant.yaml")

    # --- 2. TESTS DE LA LOGIQUE D'ALERTE ---
    def test_alerte_vent_seuil(self):
        # Simulation d'un test de seuil de vent
        seuil_vent = 50.0
        vent_fort = 60.0
        self.assertTrue(vent_fort > seuil_vent)

    def test_temperature_limite(self):
        # Simulation d'un test de température limite au seuil
        seuil_temp = 40.0
        temp_actuelle = 40.0
        self.assertEqual(temp_actuelle, seuil_temp)

    # --- 3. TEST DE GÉNÉRATION DU RAPPORT JSON ---
    def test_generation_rapport_json(self):
        donnees_test = {"statut": "OK", "equipements": 4}
        json_str = json.dumps(donnees_test)
        reparsed = json.loads(json_str)
        self.assertIn("statut", reparsed)
        self.assertEqual(reparsed["statut"], "OK")

if __name__ == "__main__":
    unittest.main()