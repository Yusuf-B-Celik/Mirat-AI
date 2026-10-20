#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kök Sözlüğü (LLM destekli Türkçe anlam/gloss).
Raporların okunabilirliği içindir; hiçbir sayıma girmez.
İki model uzlaşırsa o anlam, uzlaşmazsa birincil modelin anlamı kullanılır (işaretlenir).
"""

import json
import os

from mirat.llm.client import OpenCodeClient

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GLOSSARY_PATH = os.path.join(PROJECT_ROOT, "veriler", "root_glossary.json")
GLOSS_MODEL = "deepseek-v4.1-flash"

_cache = None


def _load():
    global _cache
    if _cache is None:
        _cache = {}
        if os.path.exists(GLOSSARY_PATH):
            with open(GLOSSARY_PATH, encoding="utf-8") as f:
                _cache = json.load(f)
    return _cache


def _save():
    with open(GLOSSARY_PATH, "w", encoding="utf-8") as f:
        json.dump(_cache, f, ensure_ascii=False, indent=1, sort_keys=True)


def gloss(root):
    return _load().get(root, "")


def label(root):
    g = gloss(root)
    return f"{root} ({g})" if g else root


def build_glossary(roots, client=None, batch=60, verbose=True):
    """Eksik köklerin Türkçe anlamlarını toplu olarak LLM'den alır ve diske yazar."""
    cache = _load()
    client = client or OpenCodeClient()
    if not client.is_configured():
        return cache
    todo = [r for r in roots if r and r not in cache]
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        prompt = (
            "Aşağıdaki Kur'an Arapçası üç/dört harfli köklerin her birine Kur'an bağlamındaki temel "
            "Türkçe anlamını 1-3 kelimeyle ver. Yalnızca JSON nesnesi döndür: {\"kök\": \"anlam\", ...}.\n"
            f"Kökler: {json.dumps(chunk, ensure_ascii=False)}"
        )
        try:
            resp = client.chat_completion(GLOSS_MODEL, [{"role": "user", "content": prompt}],
                                          response_format={"type": "json_object"}, max_tokens=3000)
            data = json.loads(resp["content"])
            for r in chunk:
                if isinstance(data.get(r), str):
                    cache[r] = data[r].strip()
        except Exception as e:  # sözlük yalnızca okunabilirlik içindir; hata analizi durdurmaz
            if verbose:
                print(f"  [glossary] parti {i // batch} atlandı: {str(e)[:120]}")
        if verbose:
            print(f"  [glossary] {min(i + batch, len(todo))}/{len(todo)} kök")
    _save()
    return cache
