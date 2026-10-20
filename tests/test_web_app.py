#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Web Paneli ve API Endpoint'leri Birim Testleri
"""

import unittest
from fastapi.testclient import TestClient
from web.app import app

class TestWebApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_index_html(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("MİRAT v6.0", resp.text)
        self.assertIn("İddia Denetçisi", resp.text)
        self.assertIn("Keşif Kataloğu", resp.text)

    def test_api_findings(self):
        resp = self.client.get("/api/findings")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("categories", data)
        self.assertGreaterEqual(len(data["categories"]), 5)

    def test_api_audit(self):
        resp = self.client.get("/api/audit")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("claims", data)
        self.assertGreaterEqual(len(data["claims"]), 5)

    def test_api_budget(self):
        resp = self.client.get("/api/budget")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(len(data), 15)

    def test_api_null_models(self):
        resp = self.client.get("/api/null-models")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("base_rate", data)
        self.assertIn("waveform_permutation", data)

    def test_api_qa(self):
        resp = self.client.post("/api/qa", json={"query": "Kur'an'da deniz kelimesi kaç kez geçer?"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["type"], "deterministic_sql_count")

    def test_api_agent(self):
        resp = self.client.post("/api/agent/run", json={"domain": "etik", "n": 1})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("cycle_results", data)

if __name__ == '__main__':
    unittest.main()
