#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT v6 — Keşif Çıktısı Tutarlılık Testleri (Kategori 17 regresyonu).

Bu testler iki hatanın regresyonunu korur:
  1) c17 global bulguları bh_adjust'ten geçmediği için q_value=None kalıyordu;
     bu durum mirat_cli.py --findings komutunu TypeError ile çökertiyordu.
  2) export_site_data.py, q_value=None olan bulguları "dürüst negatif"
     sayımına katmadığı için site 73 gösterirken katalog 75 diyordu.
"""

import json
import os
import subprocess
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class TestC17QValueAssigned(unittest.TestCase):
    """Kategori 17'deki HER test bulgusu q_value almış olmalı."""

    @classmethod
    def setUpClass(cls):
        from mirat.features import get_corpus
        from mirat.discovery import c17_ring_detection
        cls.findings, _ = c17_ring_detection.run(corpus=get_corpus())

    def test_c17_global_findings_have_q_value(self):
        """Global düzey bulguları bh_adjust'ten geçmeli; q_value None OLMAMALI."""
        f_map = {f.id: f for f in self.findings}
        for fid in ("c17_global_ayah", "c17_global_block"):
            self.assertIn(fid, f_map)
            self.assertIsNotNone(
                f_map[fid].q_value,
                f"{fid} q_value=None aldı; bh_adjust bu bulgulara uygulanmamış. "
                "Bu, mirat_cli.py --findings komutunu çökertir."
            )

    def test_c17_all_tested_findings_have_q_value(self):
        """null_p'si olan hiçbir c17 bulgusu q_value'suz kalmamalı."""
        missing = [f.id for f in self.findings
                   if f.null_p is not None and f.q_value is None]
        self.assertEqual(
            [], missing,
            f"q_value=None kalan c17 bulguları: {missing}"
        )


class TestAllEnginesQValueConsistency(unittest.TestCase):
    """9 keşif motorunun hiçbirinde q_value=None kalmamalı."""

    def test_no_engine_leaves_q_value_none(self):
        from mirat.features import get_corpus
        from mirat.discovery import runner
        import importlib

        corpus = get_corpus()
        problems = []
        for cat in sorted(runner.ENGINES):
            mod = importlib.import_module(runner.ENGINES[cat])
            findings, _ = mod.run(corpus=corpus)
            missing = [f.id for f in findings
                       if f.null_p is not None and f.q_value is None]
            if missing:
                problems.append((cat, missing))
        self.assertEqual(
            [], problems,
            f"q_value=None kalan bulgular (kategori, id'ler): {problems}"
        )


class TestC19DeterministicOrdering(unittest.TestCase):
    """Kategori 19 çift id'si çalıştırmalar arasında değişmemeli.

    `figs` listesi `defaultdict(set)` üzerinden kurulduğu için sıra hash
    seed'ine bağlıydı; aynı komut üç farklı çalıştırmada üç farklı sıra
    üretti (örn. 'c19_co_عِيسَى_مَرْيَم' / 'c19_co_مَرْيَم_عِيسَى').
    """

    def test_c19_co_ids_stable_across_runs(self):
        from mirat.features import get_corpus
        from mirat.discovery import c19_narrative
        corpus = get_corpus()
        runs = []
        for _ in range(3):
            findings, _ = c19_narrative.run(corpus=corpus)
            runs.append(tuple(sorted(f.id for f in findings)))
        self.assertEqual(
            runs[0], runs[1],
            "Kategori 19 bulgu id'leri çalıştırmalar arasında değişiyor "
            "(deterministik değil)."
        )
        self.assertEqual(
            runs[1], runs[2],
            "Kategori 19 bulgu id'leri çalıştırmalar arasında değişiyor "
            "(deterministik değil)."
        )

    def test_c19_figure_pair_order_is_sorted(self):
        """Eşanılma çift id'leri figür adlarına göre sabit sıralı olmalı."""
        from mirat.features import get_corpus
        from mirat.discovery import c19_narrative
        findings, _ = c19_narrative.run(corpus=get_corpus())
        for f in findings:
            if not f.id.startswith("c19_co_") or f.id == "c19_co_network":
                continue
            parts = f.id[len("c19_co_"):].split("_")
            self.assertEqual(2, len(parts),
                             f"Beklenmeyen id biçimi: {f.id}")
            self.assertLessEqual(parts[0], parts[1],
                                 f"{f.id} çifti sıralı değil")


class TestCliFindingsDoesNotCrash(unittest.TestCase):
    """mirat_cli.py --findings q_value=None bulgular yüzünden çökmemeli."""

    def test_cli_findings_exit_code_zero(self):
        proc = subprocess.run(
            [sys.executable, "mirat_cli.py", "--findings"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(
            0, proc.returncode,
            f"CLI çöktü (exit={proc.returncode}):\n{proc.stderr[-2000:]}"
        )
        self.assertNotIn("TypeError", proc.stderr)
        self.assertIn("Kategori 17", proc.stdout)

    def test_cli_findings_category_17_exit_code_zero(self):
        """Kategori 17'yi tek başına seçmek de çökmemeli (q_value=None kaynaklıydı)."""
        proc = subprocess.run(
            [sys.executable, "mirat_cli.py", "--findings", "--category", "17"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(
            0, proc.returncode,
            f"Kategori 17 CLI çöktü (exit={proc.returncode}):\n{proc.stderr[-2000:]}"
        )
        self.assertIn("c17_global_ayah", proc.stdout)


class TestSiteExportCountConsistency(unittest.TestCase):
    """Site sayaçları ile katalog tablosu aynı sayıları vermeli."""

    def test_exported_counts_match_catalog_totals(self):
        from mirat.discovery.runner import load_findings
        data = load_findings()
        self.assertIsNotNone(data, "mirat_kesifler.json bulunamadı")
        all_f = [f for c in data["categories"].values() for f in c["findings"]]
        tested = [f for f in all_f if f["null_p"] is not None]
        sig = [f for f in tested if f["q_value"] is not None and f["q_value"] < 0.05]
        # q_value None olan test varsa sayım tutarsızdır
        self.assertEqual(
            [], [f["id"] for f in tested if f["q_value"] is None],
            "Test bulgusu q_value=None; katalog 'anlamsız' sütunu sayımı bozulur."
        )
        catalog_sig = sum(
            1 for c in data["categories"].values() for f in c["findings"]
            if f["null_p"] is not None and f["q_value"] is not None and f["q_value"] < 0.05
        )
        catalog_null = sum(
            1 for c in data["categories"].values() for f in c["findings"]
            if f["null_p"] is not None and f["q_value"] is not None and f["q_value"] >= 0.05
        )
        # Site verisi ile katalog sayıları eşleşmeli
        site_path = os.path.join(PROJECT_ROOT, "site", "src", "data", "findings.json")
        if os.path.exists(site_path):
            with open(site_path, encoding="utf-8") as f:
                site = json.load(f)
            self.assertEqual(catalog_sig, site["significant_count"],
                             "Site 'anlamlı' sayısı katalogla uyuşmuyor")
            self.assertEqual(catalog_null, site["honest_null_count"],
                             "Site 'dürüst negatif' sayısı katalogla uyuşmuyor")
            self.assertEqual(len(all_f), site["total_count"],
                             "Site toplam bulgu sayısı katalogla uyuşmuyor")


if __name__ == '__main__':
    unittest.main()
