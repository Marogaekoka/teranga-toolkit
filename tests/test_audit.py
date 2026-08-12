import json
import os
import unittest

from teranganet.rapport import auditer_equipement, generer_rapport


class MockEquipement:
    def __init__(self, nom, ip, eq_type, est_actif=True, cpu_usage=50):
        self.nom = nom
        self.ip = ip
        self.type = eq_type
        self.est_actif = est_actif
        self.cpu_usage = cpu_usage


class MockSite:
    def __init__(self, site_id, nom, equipements, lat=14.69, lon=-17.44):
        self.id = site_id
        self.nom = nom
        self.equipements = equipements
        self.latitude = lat
        self.longitude = lon
        self.meteo_data = {"temperature": 28.5, "conditions": "Ensoleillé"}


class TestAuditRapport(unittest.TestCase):

    def setUp(self):
        self.config = {
            "seuils": {
                "temperature_max_celsius": 40,
                "cpu_max_pct": 80
            }
        }
        self.eq_ok = MockEquipement("Router-Dakar", "192.168.1.1", "routeur", True, 40)
        self.eq_hs = MockEquipement("Switch-Thies", "192.168.2.1", "switch", False, 0)
        self.eq_cpu = MockEquipement("Server-Core", "192.168.1.10", "serveur", True, 92)

    def test_equipement_conforme(self):
        res = auditer_equipement(self.eq_ok, {"temperature": 30}, self.config)
        self.assertEqual(res["statut_audit"], "CONFORME")
        self.assertEqual(len(res["alertes"]), 0)

    def test_equipement_hors_ligne(self):
        res = auditer_equipement(self.eq_hs, {"temperature": 30}, self.config)
        self.assertEqual(res["statut_audit"], "NON_CONFORME")
        self.assertTrue(any(a["niveau"] == "CRITIQUE" for a in res["alertes"]))

    def test_charge_cpu_elevee(self):
        res = auditer_equipement(self.eq_cpu, {"temperature": 30}, self.config)
        self.assertEqual(res["statut_audit"], "NON_CONFORME")
        self.assertTrue(any(a["niveau"] == "AVERTISSEMENT" for a in res["alertes"]))

    def test_generation_fichier_json(self):
        site = MockSite("site-01", "Dakar Principal", [self.eq_ok, self.eq_hs])
        fichier_test = "tests/test_output.json"

        rapport = generer_rapport([site], self.config, fichier_sortie=fichier_test)

        self.assertTrue(os.path.exists(fichier_test))
        self.assertEqual(rapport["metriques_globales"]["total_sites"], 1)

        # Nettoyage après le test
        if os.path.exists(fichier_test):
            os.remove(fichier_test)


if __name__ == "__main__":
    unittest.main()