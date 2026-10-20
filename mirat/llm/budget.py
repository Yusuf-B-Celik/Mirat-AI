#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT LLM Bütçe Yöneticisi (v6, dolar bazlı)

OpenCode Go limitleri aylık dolar tutarı olarak tanımlıdır:
  5 saat = aylık limitin %20'si, hafta = %50, ay = %100.
Her istekte yanıttaki `usage` x fiyat tablosu ile maliyet hesaplanır ve
kayan pencerelerde biriktirilir. Güvenlik payı olarak her pencerenin en fazla
`safety_fraction` kadarı (varsayılan %50) kullanılır.

Fiyatlar: https://opencode.ai/docs/go/ (1M token başına USD), 2026-10-04 itibarıyla.
"""

import os
import sqlite3
import time
from datetime import datetime, timezone

USAGE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                             "veriler", "llm_usage.db")

# model: (input, output, cached_read, monthly_limit_usd, peak_multiplier_applies)
PRICING = {
    'glm-5.3-flash': (0.15, 0.50, 0.03, 60, False),
    'longcat-2.0': (0.30, 1.20, 0.006, 60, False),
    'longcat-2.5-preview-free': (0.0, 0.0, 0.0, float('inf'), False),
    'mimo-v2.6-flash': (0.14, 0.28, 0.0028, 60, False),
    'mimo-v2.6-pro': (0.435, 0.87, 0.003625, 15, False),
    'mimo-v2.5': (0.14, 0.28, 0.0028, 60, False),
    'mimo-v2.5-pro': (0.435, 0.87, 0.003625, 15, False),
    'minimax-m3': (0.30, 1.20, 0.06, 60, False),
    'minimax-m2.7': (0.30, 1.20, 0.06, 60, False),
    'muse-spark-1.3-contributor': (0.10, 0.20, 0.002, 60, False),
    'muse-spark-1.2-contributor': (0.10, 0.20, 0.002, 60, False),
    'qwen3.8-flash': (0.15, 0.47, 0.016, 30, False),
    'qwen3.7-plus': (0.40, 1.60, 0.04, 60, False),
    'deepseek-v4.1-flash': (0.15, 0.60, 0.003, 60, True),
    'deepseek-v4-flash': (0.15, 0.60, 0.003, 30, True),
    'deepseek-v4-flash-vision-exp': (0.15, 0.60, 0.003, 15, True),
    'deepseek-v4-pro': (0.66, 1.98, 0.022, 15, True),
    'hy4-preview': (0.834, 2.501, 0.042, 30, False),
    'hy3': (0.14, 0.58, 0.035, 60, False),
    'space-bunny-free': (0.0, 0.0, 0.0, float('inf'), False),
    'gpt-6-luna': (0.10, 0.50, 0.01, 15, False),
}

WINDOWS = {  # ad: (saniye, aylık limitin oranı)
    '5h': (5 * 3600, 0.20),
    'week': (7 * 86400, 0.50),
    'month': (30 * 86400, 1.00),
}


class BudgetExceededError(Exception):
    pass


def is_deepseek_peak(now_utc=None):
    """DeepSeek peak: Pzt-Cum 01:00-04:00 ve 06:00-10:00 UTC."""
    now = now_utc or datetime.now(timezone.utc)
    if now.weekday() >= 5:
        return False
    h = now.hour
    return 1 <= h < 4 or 6 <= h < 10


def compute_cost(model, usage, now_utc=None):
    """`usage` sözlüğünden USD maliyeti hesaplar (önbellekli girdi ayrı fiyatlanır)."""
    if model not in PRICING:
        return 0.0
    inp, out, cached, _, peak_applies = PRICING[model]
    mult = 2.0 if (peak_applies and is_deepseek_peak(now_utc)) else 1.0
    prompt = usage.get('prompt_tokens', 0) or 0
    completion = usage.get('completion_tokens', 0) or 0
    cached_tokens = ((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0)
    fresh = max(0, prompt - cached_tokens)
    return mult * (fresh * inp + cached_tokens * cached + completion * out) / 1_000_000


class BudgetManager:
    def __init__(self, db_path=None, safety_fraction=0.5):
        self.db_path = db_path if db_path is not None else USAGE_DB_PATH
        self.safety_fraction = safety_fraction
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.executescript("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                prompt_tokens INTEGER DEFAULT 0,
                completion_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                status TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_usage_model ON usage_logs(model);
            """)
            cols = [r[1] for r in c.execute("PRAGMA table_info(usage_logs)")]
            if 'cost_usd' not in cols:
                c.execute("ALTER TABLE usage_logs ADD COLUMN cost_usd REAL DEFAULT 0")
            if 'ts_epoch' not in cols:
                c.execute("ALTER TABLE usage_logs ADD COLUMN ts_epoch REAL DEFAULT 0")
            conn.commit()

    # --- sorgular ---------------------------------------------------------
    def spent_in_window(self, model, seconds, now=None):
        now = now or time.time()
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute(
                "SELECT coalesce(sum(cost_usd),0), count(*) FROM usage_logs "
                "WHERE model=? AND status='success' AND ts_epoch>=?", (model, now - seconds)).fetchone()
        return {'cost_usd': r[0], 'requests': r[1]}

    def window_status(self, model, now=None):
        monthly = PRICING.get(model, (0, 0, 0, 1.0, False))[3]
        out = {}
        for name, (secs, frac) in WINDOWS.items():
            cap = monthly * frac
            spent = self.spent_in_window(model, secs, now)
            out[name] = {
                'spent_usd': round(spent['cost_usd'], 4),
                'requests': spent['requests'],
                'cap_usd': cap,
                'safe_cap_usd': cap * self.safety_fraction,
            }
        return out

    def get_model_limit(self, model):
        """Geriye dönük uyumluluk: 5 saatlik pencerenin güvenli dolar tavanı."""
        return self.window_status(model)['5h']['safe_cap_usd']

    def get_current_usage(self, model):
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute("SELECT count(*), coalesce(sum(total_tokens),0), coalesce(sum(cost_usd),0) "
                             "FROM usage_logs WHERE model=? AND status='success'", (model,)).fetchone()
        return {'request_count': r[0], 'total_tokens': r[1], 'cost_usd': r[2]}

    # --- denetim ve kayıt -------------------------------------------------
    def check_and_reserve(self, model):
        if model not in PRICING:
            raise BudgetExceededError(f"[{model}] fiyat tablosunda yok; güvenlik için engellendi.")
        if PRICING[model][3] == float('inf'):
            return True
        for name, st in self.window_status(model).items():
            if st['spent_usd'] >= st['safe_cap_usd']:
                raise BudgetExceededError(
                    f"[{model}] {name} penceresinde güvenli tavan aşıldı: "
                    f"${st['spent_usd']:.4f} / ${st['safe_cap_usd']:.2f} (tam limit ${st['cap_usd']:.2f}).")
        return True

    def record_usage(self, model, prompt_tokens=0, completion_tokens=0, status="success", usage=None):
        """Kullanımı kaydeder ve USD maliyetini döner."""
        if usage is None:
            usage = {'prompt_tokens': prompt_tokens, 'completion_tokens': completion_tokens}
        p = usage.get('prompt_tokens', 0) or 0
        cpl = usage.get('completion_tokens', 0) or 0
        cost = compute_cost(model, usage) if status == 'success' else 0.0
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO usage_logs (model, prompt_tokens, completion_tokens, total_tokens, status, cost_usd, ts_epoch) "
                "VALUES (?,?,?,?,?,?,?)", (model, p, cpl, p + cpl, status, cost, time.time()))
            conn.commit()
        return cost

    def get_full_budget_report(self):
        report = []
        for model, (_, _, _, monthly, _) in PRICING.items():
            st = self.window_status(model)
            total = self.get_current_usage(model)
            report.append({
                'model': model,
                'requests_used': total['request_count'],
                'tokens_used': total['total_tokens'],
                'cost_usd_total': round(total['cost_usd'], 4),
                'monthly_limit_usd': '∞' if monthly == float('inf') else monthly,
                'spent_5h_usd': st['5h']['spent_usd'],
                'cap_5h_usd': '∞' if monthly == float('inf') else round(st['5h']['cap_usd'], 2),
                'usage_percent_5h': 0.0 if monthly == float('inf') or st['5h']['cap_usd'] == 0
                else round(100 * st['5h']['spent_usd'] / st['5h']['cap_usd'], 2),
            })
        return report
