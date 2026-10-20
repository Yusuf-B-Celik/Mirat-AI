#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT v6 Kök Sözlüğü (LLM destekli, düşük hacimli, toplu).

Tek bir istekle her kök için üç ETİKET alınır:
  - gloss   : Türkçe temel anlam (raporların okunabilirliği için)
  - antonym : Kur'an'da geçen ve açık sözlüksel zıt anlamlı kök (yoksa null)
  - field   : Sabit 20 maddelik listeden anlam alanı

Kurallar:
  - LLM hiçbir SAYI üretmez; sayımlar keşif motorlarında deterministik yapılır.
  - İki bağımsız model aynı istemle etiketler; uyum (Cohen kappa) raporlanır, yalnızca
    iki modelin UZLAŞTIĞI zıt-anlam çiftleri istatistiksel testlere girer.
  - Ham yanıtlar veriler/lexicon/<model>.json içinde saklanır (tekrar üretilebilirlik);
    istekler llm_cache.db'de önbelleklenir, tekrar çalıştırma ücretsizdir.

Kullanım:
  python3 -m mirat.discovery.lexicon --model deepseek-v4.1-flash
  python3 -m mirat.discovery.lexicon --model qwen3.7-plus
  python3 -m mirat.discovery.lexicon --merge
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict

from mirat.features import get_corpus

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEX_DIR = os.path.join(PROJECT_ROOT, "veriler", "lexicon")
MERGED_PATH = os.path.join(LEX_DIR, "root_lexicon.json")
BATCH = 40
MODELS = ["deepseek-v4.1-flash", "qwen3.7-plus"]

FIELDS = [
    "İnanç/Tanrı", "Ahiret", "Peygamberlik/Vahiy", "İbadet", "Erdem/İyilik", "Günah/Kötülük",
    "Hukuk/Toplum", "Aile/Akrabalık", "Savaş/Çatışma", "Ekonomi/Mal", "Doğa/Kozmos", "Bitki/Hayvan",
    "Beden/Sağlık", "Bilgi/Akıl", "Konuşma/İletişim", "Hareket/Mekân", "Zaman", "Duygu",
    "Yaratılış/Hayat-Ölüm", "Diğer/Dilbilgisel",
]

PROMPT = """Sen Kur'an Arapçası sözlükbilimcisisin. Aşağıda Kur'an'da geçen kökler ve her birinin en sık lemması var.
Her kök için:
  "gloss": Kur'an bağlamında temel Türkçe anlam (1-3 kelime)
  "antonym": Bu kökün AÇIK ve YAYGIN kabul gören sözlüksel zıt anlamlısı olan başka bir Arapça kök (ör. حيي→موت, نور→ظلم, جنن(cennet) değil). Zıt kök MUTLAKA aşağıdaki "izinli kökler" kümesinden biri olmalı. Kesin bir zıtlık yoksa null yaz. Eş anlam, ilişki ya da sebep-sonuç zıtlık DEĞİLDİR.
  "field": şu listeden TAM OLARAK bir anlam alanı: {fields}
Yalnızca JSON döndür: {{"items": [{{"root": "...", "gloss": "...", "antonym": "..." | null, "field": "..."}}, ...]}}
Kökler (kök: lemma): {items}
İzinli kökler: Kur'an'daki tüm kökler (1651 kök) — zıt kök Kur'an'da geçmeli."""


def root_inventory(corpus=None):
    corpus = corpus or get_corpus()
    lemma_by_root = defaultdict(Counter)
    for sg in corpus.segments:
        if sg.root:
            lemma_by_root[sg.root][sg.lemma] += 1
    freq = {r: sum(c.values()) for r, c in lemma_by_root.items()}
    roots = sorted(freq, key=lambda r: (-freq[r], r))
    return roots, {r: lemma_by_root[r].most_common(1)[0][0] for r in roots}, freq


def model_path(model):
    return os.path.join(LEX_DIR, f"{model}.json")


def load_model_labels(model):
    p = model_path(model)
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def label_roots(model, client=None, limit=None, verbose=True, session_id=None):
    from mirat.llm.client import OpenCodeClient
    os.makedirs(LEX_DIR, exist_ok=True)
    roots, top_lemma, _ = root_inventory()
    valid = set(roots)
    labels = load_model_labels(model)
    client = client or OpenCodeClient(session_id=session_id or f"mirat-lexicon-{model}")
    todo = [r for r in roots if r not in labels]
    if limit:
        todo = todo[:limit]
    spent = 0.0
    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        items = ", ".join(f"{r}: {top_lemma[r]}" for r in chunk)
        prompt = PROMPT.format(fields=" | ".join(FIELDS), items=items)
        try:
            data, res = client.chat_json(model, [{"role": "user", "content": prompt}], max_tokens=8000)
        except Exception as e:
            print(f"  [{model}] parti {i // BATCH} HATA: {str(e)[:200]}", file=sys.stderr)
            continue
        spent += res.get("cost_usd", 0.0) or 0.0
        got = 0
        for it in (data.get("items") if isinstance(data, dict) else data) or []:
            r = (it or {}).get("root")
            if r not in chunk:
                continue
            ant = it.get("antonym")
            ant = ant if isinstance(ant, str) and ant in valid and ant != r else None
            field = it.get("field") if it.get("field") in FIELDS else "Diğer/Dilbilgisel"
            labels[r] = {"gloss": str(it.get("gloss") or "").strip()[:60], "antonym": ant, "field": field}
            got += 1
        with open(model_path(model), "w", encoding="utf-8") as f:
            json.dump(labels, f, ensure_ascii=False, indent=0, sort_keys=True)
        if verbose:
            print(f"  [{model}] {min(i + BATCH, len(todo))}/{len(todo)} kök | bu parti {got}/{len(chunk)} | "
                  f"kaynak={res.get('source')} | toplam ${spent:.4f}", flush=True)
    return labels


def cohen_kappa(a, b):
    """İki etiket listesinin Cohen kappa uyumu."""
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def merge(models=MODELS):
    """İki modelin etiketlerini birleştirir; uyum istatistikleri ve uzlaşılmış zıt çiftleri yazar."""
    labs = [load_model_labels(m) for m in models]
    common = sorted(set(labs[0]) & set(labs[1]))
    has_a = [labs[0][r]["antonym"] is not None for r in common]
    has_b = [labs[1][r]["antonym"] is not None for r in common]
    fa = [labs[0][r]["field"] for r in common]
    fb = [labs[1][r]["field"] for r in common]

    def pair(a, b):
        return tuple(sorted((a, b)))
    pairs_a = {pair(r, labs[0][r]["antonym"]) for r in labs[0] if labs[0][r]["antonym"]}
    pairs_b = {pair(r, labs[1][r]["antonym"]) for r in labs[1] if labs[1][r]["antonym"]}
    agreed = sorted(pairs_a & pairs_b)
    merged = {}
    for r in set(labs[0]) | set(labs[1]):
        la, lb = labs[0].get(r), labs[1].get(r)
        base = la or lb
        merged[r] = {
            "gloss": base["gloss"],
            "field": la["field"] if (la and lb and la["field"] == lb["field"]) else base["field"],
            "field_agreed": bool(la and lb and la["field"] == lb["field"]),
        }
    out = {
        "models": models,
        "n_labeled": {m: len(l) for m, l in zip(models, labs)},
        "n_common": len(common),
        "kappa_has_antonym": cohen_kappa(has_a, has_b),
        "kappa_field": cohen_kappa(fa, fb),
        "pairs_model_a": len(pairs_a), "pairs_model_b": len(pairs_b),
        "agreed_pairs": [list(p) for p in agreed],
        "roots": merged,
    }
    os.makedirs(LEX_DIR, exist_ok=True)
    with open(MERGED_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=True)
    # Glossary dosyasını da doldur (okunabilirlik)
    from mirat.discovery import glossary
    g = glossary._load()
    for r, v in merged.items():
        if v["gloss"] and r not in g:
            g[r] = v["gloss"]
    glossary._save()
    return out


def load_merged():
    if not os.path.exists(MERGED_PATH):
        return None
    with open(MERGED_PATH, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--merge", action="store_true")
    a = ap.parse_args()
    if a.model:
        label_roots(a.model, limit=a.limit)
    if a.merge:
        o = merge()
        print(json.dumps({k: v for k, v in o.items() if k not in ("roots", "agreed_pairs")}, ensure_ascii=False, indent=1))
        print("Uzlaşılmış zıt çift:", len(o["agreed_pairs"]), o["agreed_pairs"][:20])
