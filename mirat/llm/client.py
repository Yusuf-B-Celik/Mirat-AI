#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT OpenCode Go İstemcisi (v6)

- Uç nokta: https://opencode.ai/zen/go/v1 (OpenAI uyumlu /chat/completions)
- Zorunlu başlıklar: özel User-Agent ve sabit `x-opencode-session`
- Dolar bazlı bütçe denetimi (bkz. budget.py), SHA-256 önbellek, hız sınırı
- Akıl yürütme (reasoning) modellerinde boş yanıt için tek seferlik yeniden deneme
- Yalnızca standart kütüphane (urllib) kullanır
"""

import json
import os
import re
import sys
import time
import uuid
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mirat.llm.cache import LLMCache
from mirat.llm.budget import BudgetManager, BudgetExceededError  # noqa: F401 (re-export)

DEFAULT_BASE_URL = "https://opencode.ai/zen/go/v1"
USER_AGENT = "mirat-research-agent/6.0"
MIN_INTERVAL_SEC = 1.0  # saniyede en fazla 1 istek


def load_env_file():
    """Proje kökündeki .env dosyasını (varsa) ortam değişkenlerine yükler."""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(root_dir, ".env")
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


load_env_file()


def extract_json(text):
    """Model çıktısından JSON nesnesini/listesini ayıklar (```json çitlerini temizler)."""
    if text is None:
        raise ValueError("Boş yanıt")
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        # İlk { veya [ ile son } veya ] arasını dene
        starts = [i for i in (t.find("{"), t.find("[")) if i != -1]
        if not starts:
            raise
        s = min(starts)
        e = max(t.rfind("}"), t.rfind("]"))
        return json.loads(t[s:e + 1])


class OpenCodeClient:
    def __init__(self, api_key=None, base_url=None, cache=None, budget=None,
                 max_retries=3, session_id=None, min_interval=MIN_INTERVAL_SEC):
        self.api_key = api_key if api_key is not None else os.environ.get("OPENCODE_API_KEY", "")
        self.base_url = (base_url or os.environ.get("OPENCODE_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        self.cache = cache if cache is not None else LLMCache()
        self.budget = budget if budget is not None else BudgetManager()
        self.max_retries = max_retries
        self.session_id = session_id or f"mirat-{uuid.uuid4().hex[:12]}"
        self.min_interval = min_interval
        self._last_call = 0.0

    def is_configured(self):
        if os.environ.get("MIRAT_OFFLINE") == "1":
            return False
        return bool(self.api_key and len(self.api_key) > 10)

    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": USER_AGENT,
            "x-opencode-session": self.session_id,
        }

    def _throttle(self):
        wait = self.min_interval - (time.time() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.time()

    def _post(self, payload):
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=self._headers(), method="POST")
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def chat_completion(self, model, messages, temperature=0.0, response_format=None, max_tokens=4000):
        """
        Önbellek -> bütçe -> canlı çağrı. Dönen sözlük:
        {'source': 'cache'|'live_api', 'model', 'content', 'usage', 'cost_usd'}
        """
        req_hash = self.cache.compute_hash(model, messages, temperature, response_format)
        cached = self.cache.get(req_hash)
        if cached is not None:
            return {'source': 'cache', 'model': model, 'content': cached['content'],
                    'usage': cached.get('usage', {}), 'cost_usd': 0.0}

        if not self.is_configured():
            raise ValueError("OPENCODE_API_KEY tanımlı değil (.env veya ortam değişkeni).")

        self.budget.check_and_reserve(model)

        payload = {'model': model, 'messages': messages, 'temperature': temperature, 'max_tokens': max_tokens}
        if response_format:
            payload['response_format'] = response_format

        last_error = None
        empty_retry_done = False
        attempt = 0
        while attempt < self.max_retries:
            attempt += 1
            self._throttle()
            try:
                resp = self._post(payload)
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="ignore")[:500]
                last_error = f"HTTP {e.code}: {body}"
                if e.code in (429, 500, 502, 503, 504) and attempt < self.max_retries:
                    time.sleep(2 ** attempt + 1)
                    continue
                self.budget.record_usage(model, status=f"error_{e.code}")
                raise RuntimeError(f"OpenCode API hatası: {last_error}") from e
            except (urllib.error.URLError, TimeoutError) as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    time.sleep(3)
                    continue
                raise RuntimeError(f"Bağlantı hatası: {last_error}") from e

            choice = (resp.get('choices') or [{}])[0]
            content = (choice.get('message') or {}).get('content') or ""
            usage = resp.get('usage', {}) or {}
            cost = self.budget.record_usage(model, usage=usage, status='success')

            if not content.strip():
                # Reasoning modeli tüm bütçeyi düşünmeye harcamış olabilir: bir kez, daha geniş sınırla dene
                if not empty_retry_done:
                    empty_retry_done = True
                    payload['max_tokens'] = max(payload['max_tokens'] * 2, 8000)
                    attempt -= 1
                    continue
                raise RuntimeError(f"[{model}] boş yanıt döndü (finish_reason={choice.get('finish_reason')}).")

            self.cache.set(req_hash, model, messages,
                           {'content': content, 'usage': usage, 'finish_reason': choice.get('finish_reason')})
            return {'source': 'live_api', 'model': model, 'content': content, 'usage': usage, 'cost_usd': cost}

        raise RuntimeError(f"İstek başarısız: {last_error}")

    def chat_json(self, model, messages, temperature=0.0, max_tokens=4000):
        """JSON çıktısı isteyip ayrıştırılmış nesneyi döner."""
        res = self.chat_completion(model, messages, temperature=temperature,
                                   response_format={'type': 'json_object'}, max_tokens=max_tokens)
        return extract_json(res['content']), res
