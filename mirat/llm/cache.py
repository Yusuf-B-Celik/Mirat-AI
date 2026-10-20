#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT LLM Yanıt Önbelleği (SHA-256 Keyed Response Cache)
Tekrarlanan veya deneme çağrılarında API kotasını tüketmemek için
tüm LLM yanıtlarını yerel SQLite veritabanında saklar.
"""

import hashlib
import json
import os
import sqlite3
import time

CACHE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "veriler", "llm_cache.db")

class LLMCache:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path is not None else CACHE_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.executescript("""
            CREATE TABLE IF NOT EXISTS response_cache (
                request_hash TEXT PRIMARY KEY,
                model TEXT,
                prompt_snippet TEXT,
                response_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_cache_model ON response_cache(model);
            """)
            conn.commit()

    @staticmethod
    def compute_hash(model, messages, temperature=0.0, json_schema=None):
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'json_schema': json_schema
        }
        serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def get(self, request_hash):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT response_json FROM response_cache WHERE request_hash = ?", (request_hash,))
            row = c.fetchone()
            if row:
                return json.loads(row[0])
        return None

    def set(self, request_hash, model, messages, response_data):
        prompt_snippet = ""
        if messages and isinstance(messages, list):
            prompt_snippet = str(messages[-1].get('content', ''))[:100]

        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
            INSERT OR REPLACE INTO response_cache (request_hash, model, prompt_snippet, response_json)
            VALUES (?, ?, ?, ?)
            """, (request_hash, model, prompt_snippet, json.dumps(response_data, ensure_ascii=False)))
            conn.commit()

    def get_stats(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT count(*), count(DISTINCT model) FROM response_cache")
            total, models = c.fetchone()
            return {'total_cached_responses': total, 'models_cached': models}
