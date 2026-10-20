#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT v6 Keşif Koşucusu

Tüm keşif motorlarını (kategori 11-19) çalıştırır, bulguları tek bir şemada toplar ve
  - veriler/mirat_kesifler.json
  - raporlar/MIRAT_KESIF_KATALOGU.md
dosyalarına yazar. Anlamsız (q >= 0.05) testler ve negatif sonuçlar da katalogda yer alır.

Kullanım:
  python3 -m mirat.discovery.runner            # tümü
  python3 -m mirat.discovery.runner 12 14      # seçili kategoriler
"""

import importlib
import json
import os
import sys
import time
from datetime import datetime

from mirat.features import get_corpus

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_PATH = os.path.join(PROJECT_ROOT, "veriler", "mirat_kesifler.json")
MD_PATH = os.path.join(PROJECT_ROOT, "raporlar", "MIRAT_KESIF_KATALOGU.md")

ENGINES = {
    11: "mirat.discovery.c11_chronology",
    12: "mirat.discovery.c12_rhetoric",
    13: "mirat.discovery.c13_number_morphology",
    14: "mirat.discovery.c14_repetition",
    15: "mirat.discovery.c15_semantic_network",
    16: "mirat.discovery.c16_antonyms",
    17: "mirat.discovery.c17_ring_detection",
    18: "mirat.discovery.c18_information",
    19: "mirat.discovery.c19_narrative",
}


def run_all(categories=None, verbose=True):
    corpus = get_corpus()
    categories = categories or sorted(ENGINES)
    out = {"generated_at": datetime.now().isoformat(timespec="seconds"), "categories": {}}
    for cat in categories:
        mod = importlib.import_module(ENGINES[cat])
        t0 = time.time()
        findings, _extras = mod.run(corpus=corpus)
        dt = time.time() - t0
        out["categories"][str(cat)] = {
            "name": mod.CATEGORY, "runtime_sec": round(dt, 2),
            "findings": [f.to_dict() for f in findings],
        }
        if verbose:
            n_sig = sum(1 for f in findings if f.q_value is not None and f.q_value < 0.05)
            n_test = sum(1 for f in findings if f.null_p is not None)
            print(f"  [{cat}] {mod.CATEGORY}: {len(findings)} bulgu, {n_test} test, {n_sig} anlamlı (q<0.05) — {dt:.1f} s",
                  flush=True)
    # Var olan dosyayla birleştir (yalnızca bazı kategoriler çalıştırıldıysa)
    if os.path.exists(JSON_PATH) and categories != sorted(ENGINES):
        with open(JSON_PATH, encoding="utf-8") as f:
            old = json.load(f)
        old["categories"].update(out["categories"])
        old["generated_at"] = out["generated_at"]
        out = old
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    write_markdown(out)
    return out


def load_findings():
    if not os.path.exists(JSON_PATH):
        return None
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def _fmt(v, nd=3):
    if v is None:
        return "—"
    if isinstance(v, float):
        if abs(v) < 1e-4 and v != 0:
            return f"{v:.1e}"
        return f"{v:.{nd}f}"
    return str(v)


def write_markdown(data):
    os.makedirs(os.path.dirname(MD_PATH), exist_ok=True)
    cats = data["categories"]
    all_f = [f for c in cats.values() for f in c["findings"]]
    tests = [f for f in all_f if f["null_p"] is not None]
    sig = [f for f in tests if f["q_value"] is not None and f["q_value"] < 0.05]
    L = []
    L.append("# MİRAT v6 — Keşif Kataloğu\n")
    L.append(f"_Üretim: {data['generated_at']} · Tüm sayılar deterministik koddan; LLM yalnızca etiket (anlam, zıt kök, "
             f"anlam alanı) üretir ve bu bulgular 🤖 ile işaretlidir._\n")
    L.append("| Kategori | Bulgu | Test | Anlamlı (q<0.05) | Anlamsız / negatif |")
    L.append("|---|---:|---:|---:|---:|")
    for k in sorted(cats, key=int):
        c = cats[k]
        t = [f for f in c["findings"] if f["null_p"] is not None]
        s = [f for f in t if f["q_value"] is not None and f["q_value"] < 0.05]
        L.append(f"| {c['name']} | {len(c['findings'])} | {len(t)} | {len(s)} | {len(t) - len(s)} |")
    L.append(f"| **Toplam** | **{len(all_f)}** | **{len(tests)}** | **{len(sig)}** | **{len(tests) - len(sig)}** |\n")
    L.append("> [!NOTE]\n> q-değerleri kategori içi Benjamini-Hochberg düzeltmesidir. Kök/çift taramalarında yalnızca en güçlü "
             "bulgular listelenir; tarama özetleri toplam test sayısını verir. \"Anlamsız\" sütunu, raporlanan ama "
             "hipotezi desteklemeyen testleri sayar — bunlar bilinçli olarak katalogda tutulur.\n")
    for k in sorted(cats, key=int):
        c = cats[k]
        L.append(f"\n## {c['name']}\n")
        L.append(f"_Çalışma süresi: {c['runtime_sec']} s_\n")
        for f in c["findings"]:
            badge = ""
            if f["null_p"] is not None:
                badge = "✅" if (f["q_value"] is not None and f["q_value"] < 0.05) else "⚪"
            else:
                badge = "📋"
            if f.get("llm_assisted"):
                badge += "🤖"
            L.append(f"### {badge} {f['title']}")
            row = [f"**Yöntem:** {f['method']}", f"**Ölçüt:** {f['metric']} = {_fmt(f['value'])}"]
            if f["null_p"] is not None:
                row.append(f"**p:** {_fmt(f['null_p'], 4)} · **q:** {_fmt(f['q_value'], 4)}")
            if f.get("effect_size") is not None:
                row.append(f"**Etki:** {_fmt(f['effect_size'])}")
            L.append(" · ".join(row) + "\n")
            if f.get("detail"):
                L.append(f"{f['detail']}\n")
            if f.get("evidence"):
                ev = f["evidence"][:15]
                L.append("<details><summary>Kanıt (" + str(len(f["evidence"])) + ")</summary>\n\n" +
                         "\n".join(f"- {e}" for e in ev) + "\n\n</details>\n")
    L.append("\n---\n**Simgeler:** ✅ FDR sonrası anlamlı · ⚪ anlamsız / negatif sonuç · 📋 betimsel envanter · 🤖 LLM etiketi kullanır\n")
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return MD_PATH


if __name__ == "__main__":
    cats = [int(x) for x in sys.argv[1:]] or None
    run_all(cats)
    print("Yazıldı:", JSON_PATH, "|", MD_PATH)
