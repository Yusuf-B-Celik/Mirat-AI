#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT LLM İstemcisi, Önbellek ve Bütçe Yöneticisi Birim Testleri
Gerçek API çağrısı yapmadan yerel sahte sunucu ve mock nesneleri ile test edilir.
"""

import http.server
import json
import os
import shutil
import tempfile
import threading
import unittest
from unittest.mock import patch

from mirat.llm.cache import LLMCache
from mirat.llm.budget import BudgetManager, BudgetExceededError
from mirat.llm.router import ModelRouter
from mirat.llm.client import OpenCodeClient, extract_json

class TestLLMInfrastructure(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cache_db = os.path.join(self.test_dir, "test_cache.db")
        self.usage_db = os.path.join(self.test_dir, "test_usage.db")
        self.cache = LLMCache(self.cache_db)
        self.budget = BudgetManager(self.usage_db)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cache_put_and_get(self):
        messages = [{'role': 'user', 'content': 'Test soru'}]
        req_hash = self.cache.compute_hash('deepseek-v4.1-flash', messages)
        self.assertIsNone(self.cache.get(req_hash))

        resp_data = {'content': 'Test cevap', 'usage': {'total_tokens': 15}}
        self.cache.set(req_hash, 'deepseek-v4.1-flash', messages, resp_data)

        cached = self.cache.get(req_hash)
        self.assertIsNotNone(cached)
        self.assertEqual(cached['content'], 'Test cevap')

    def test_budget_cost_and_windows(self):
        # DeepSeek V4.1 Flash: aylık $60, 5 saat = %20 = $12, güvenli tavan %50 = $6
        st = self.budget.window_status('deepseek-v4.1-flash')
        self.assertAlmostEqual(st['5h']['cap_usd'], 12.0)
        self.assertAlmostEqual(st['5h']['safe_cap_usd'], 6.0)

        cost = self.budget.record_usage('deepseek-v4.1-flash',
                                        usage={'prompt_tokens': 1_000_000, 'completion_tokens': 0})
        self.assertIn(round(cost, 2), (0.15, 0.30))  # off-peak / peak
        usage = self.budget.get_current_usage('deepseek-v4.1-flash')
        self.assertEqual(usage['request_count'], 1)

    def test_budget_exceeded_exception(self):
        # Güvenli tavanı aşacak kadar harcama kaydet ($6'dan fazla)
        self.budget.record_usage('deepseek-v4.1-flash',
                                 usage={'prompt_tokens': 0, 'completion_tokens': 20_000_000})
        with self.assertRaises(BudgetExceededError):
            self.budget.check_and_reserve('deepseek-v4.1-flash')

    def test_unknown_model_blocked(self):
        with self.assertRaises(BudgetExceededError):
            self.budget.check_and_reserve('bilinmeyen-model')

    def test_model_router(self):
        self.assertEqual(ModelRouter.get_models_for_task('antonym_census'),
                         ['deepseek-v4.1-flash', 'qwen3.7-plus'])
        self.assertEqual(ModelRouter.get_primary_model('prompt_dev'), 'space-bunny-free')

    def test_client_cache_hit_offline(self):
        client = OpenCodeClient(api_key="fake-key", cache=self.cache, budget=self.budget)
        messages = [{'role': 'user', 'content': 'Ayet 1:1 nedir?'}]
        req_hash = self.cache.compute_hash('deepseek-v4.1-flash', messages, 0.0, None)
        self.cache.set(req_hash, 'deepseek-v4.1-flash', messages, {'content': 'Besmele', 'usage': {'total_tokens': 10}})
        res = client.chat_completion('deepseek-v4.1-flash', messages)
        self.assertEqual(res['source'], 'cache')
        self.assertEqual(res['content'], 'Besmele')

    def test_extract_json_fenced(self):
        self.assertEqual(extract_json('```json\n{"a": 1}\n```'), {'a': 1})
        self.assertEqual(extract_json('Sonuç: [1, 2] bitti'), [1, 2])


class _FakeHandler(http.server.BaseHTTPRequestHandler):
    calls = []

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        _FakeHandler.calls.append({'headers': dict(self.headers), 'body': body})
        # İlk çağrıda boş içerik (reasoning bütçesi bitti), sonra gerçek içerik
        content = "" if len(_FakeHandler.calls) == 1 else '{"ok": true}'
        out = json.dumps({'choices': [{'message': {'content': content}, 'finish_reason': 'length'}],
                          'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *args):
        pass


class TestClientAgainstFakeServer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        _FakeHandler.calls = []
        self.server = http.server.HTTPServer(('127.0.0.1', 0), _FakeHandler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.client = OpenCodeClient(
            api_key="test-key-1234567890", base_url=f"http://127.0.0.1:{self.server.server_port}",
            cache=LLMCache(os.path.join(self.tmp, 'c.db')), budget=BudgetManager(os.path.join(self.tmp, 'u.db')),
            session_id="mirat-test-session", min_interval=0)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_headers_and_empty_retry(self):
        with patch.dict(os.environ, {'MIRAT_OFFLINE': '0'}):
            data, res = self.client.chat_json('deepseek-v4.1-flash', [{'role': 'user', 'content': 'x'}], max_tokens=100)
        self.assertEqual(data, {'ok': True})
        self.assertEqual(len(_FakeHandler.calls), 2)
        h = {k.lower(): v for k, v in _FakeHandler.calls[0]['headers'].items()}
        self.assertEqual(h['user-agent'], 'mirat-research-agent/6.0')
        self.assertEqual(h['x-opencode-session'], 'mirat-test-session')
        # Boş yanıttan sonra max_tokens büyütülmeli
        self.assertGreater(_FakeHandler.calls[1]['body']['max_tokens'], 100)


if __name__ == '__main__':
    unittest.main()
