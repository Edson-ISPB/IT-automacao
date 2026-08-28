import unittest
import config
from evaluator import (
    evaluate_cpu,
    evaluate_ram,
    evaluate_disk,
    evaluate_uptime,
    evaluate_connectivity,
    evaluate_temp_size,
    evaluate_services,
    get_all_recommendations,
)


class TestEvaluator(unittest.TestCase):

    def test_evaluate_cpu(self):
        self.assertEqual(evaluate_cpu(50), "OK")
        self.assertEqual(evaluate_cpu(config.CPU_WARNING), "AVISO")
        self.assertEqual(evaluate_cpu(config.CPU_CRITICAL + 1), "CRÍTICO")

    def test_evaluate_ram(self):
        self.assertEqual(evaluate_ram(70), "OK")
        self.assertEqual(evaluate_ram(config.RAM_WARNING), "AVISO")
        self.assertEqual(evaluate_ram(config.RAM_CRITICAL + 5), "CRÍTICO")

    def test_evaluate_disk(self):
        self.assertEqual(evaluate_disk(60), "OK")
        self.assertEqual(evaluate_disk(config.DISK_WARNING), "AVISO")
        self.assertEqual(evaluate_disk(config.DISK_CRITICAL + 1), "CRÍTICO")

    def test_evaluate_uptime(self):
        self.assertEqual(evaluate_uptime(5), "OK")
        self.assertEqual(evaluate_uptime(14), "AVISO")
        self.assertEqual(evaluate_uptime(30), "AVISO")

    def test_evaluate_connectivity(self):
        self.assertEqual(evaluate_connectivity(True), "OK")
        self.assertEqual(evaluate_connectivity(False), "CRÍTICO")

    def test_evaluate_temp_size(self):
        self.assertEqual(evaluate_temp_size(1.0), "OK")
        self.assertEqual(evaluate_temp_size(config.TEMP_SIZE_WARNING_GB), "AVISO")
        self.assertEqual(evaluate_temp_size(config.TEMP_SIZE_CRITICAL_GB + 2.0), "CRÍTICO")

    def test_evaluate_services(self):
        services_ok = [{"name": "Spooler", "status": "EM EXECUÇÃO"}]
        services_bad = [{"name": "Spooler", "status": "PARADO"}]

        self.assertEqual(evaluate_services(services_ok), "OK")
        self.assertEqual(evaluate_services(services_bad), "AVISO")

    def test_recommendations_generation(self):
        mock_data = {
            "uptime": 20,
            "uptime_status": "AVISO",
            "cpu": 95,
            "cpu_status": "CRÍTICO",
            "top_processes": {"top_cpu": [{"name": "bad_process.exe", "cpu_percent": 85.0}]},
            "disks": [],
            "network_status": "OK",
            "temp_status": "OK",
            "services": [],
        }

        recs = get_all_recommendations(mock_data)
        self.assertTrue(len(recs) >= 2)
        categories = [r["categoria"] for r in recs]
        self.assertIn("Sistema / Uptime", categories)
        self.assertIn("Processador (CPU)", categories)


if __name__ == "__main__":
    unittest.main()
