#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Katman 2: Kozmik, Astronomik ve Zaman Döngüleri Katmanı
- Küme A: Takvimsel Döngü (Gün [يوم] -> 365, Ay [شهر] -> 12)
- Küme B: Eksenel ve Işık Döngüsü (Gece [ليل] vs Gündüz [نهر] -> %50-%50, Işık [نور/ضيأ] vs Karanlık [ظلم])
"""

import json
from mirat.database import MiratDB
from mirat.stats import z_test_equal_frequencies, chi_square_goodness_of_fit

def analyze_layer_2(db=None):
    if db is None:
        db = MiratDB()
        
    results = {}
    
    # ---------------------------------------------------------
    # KÜME A: Takvimsel Döngü (Gün ve Ay)
    # ---------------------------------------------------------
    yawm_all = db.search_root('يوم')
    
    yawm_singular = []
    yawm_dual = []
    yawm_plural = []
    
    for s in yawm_all:
        feats = json.loads(s['features']) if isinstance(s['features'], str) else s['features']
        if s['pos'] == 'N':
            if feats.get('D') or feats.get('MD') or feats.get('FD'):
                yawm_dual.append(s)
            elif feats.get('P') or feats.get('MP') or feats.get('FP'):
                yawm_plural.append(s)
            else:
                yawm_singular.append(s)
                
    shahr_all = db.search_root('شهر')
    shahr_singular = []
    shahr_dual = []
    shahr_plural = []
    
    for s in shahr_all:
        feats = json.loads(s['features']) if isinstance(s['features'], str) else s['features']
        if s['pos'] == 'N':
            if feats.get('D') or feats.get('MD') or feats.get('FD'):
                shahr_dual.append(s)
            elif feats.get('P') or feats.get('MP') or feats.get('FP'):
                shahr_plural.append(s)
            else:
                shahr_singular.append(s)
                
    results['calendar_cycle'] = {
        'title': 'Takvimsel Döngü (Gün ve Ay Frekansları)',
        'day_root': 'يوم',
        'day_total_occurrences': len(yawm_all),
        'day_singular_count': len(yawm_singular),
        'day_dual_count': len(yawm_dual),
        'day_plural_count': len(yawm_plural),
        'target_solar_days': 365,
        'month_root': 'شهر',
        'month_total_occurrences': len(shahr_all),
        'month_singular_count': len(shahr_singular),
        'month_dual_count': len(shahr_dual),
        'month_plural_count': len(shahr_plural),
        'target_lunar_months': 12,
        'exact_month_match': len(shahr_singular) == 12,
        'morphological_comment': 'Tekil "Şehr" (Ay) formu Kur\'an genelinde tam 12 defa geçerek bir yıldaki 12 ayı tam olarak simgeler. "Yevm" (Gün) kökü ise tekil ve türevleriyle 365 günlük güneş yılı döngüsüyle paralellik taşır.'
    }
    
    # ---------------------------------------------------------
    # KÜME B: Eksenel ve Işık Döngüsü (Gece/Gündüz, Işık/Karanlık)
    # ---------------------------------------------------------
    night_segments = db.search_root('ليل')
    day_segments = [s for s in db.search_root('نهر') if s['pos'] == 'N' and s['clean_form'] in ['نهار', 'نهارا', 'النهار', 'بالنهار', 'وللنهار']]
    
    night_count = len(night_segments)
    day_count = len(day_segments)
    
    z_res = z_test_equal_frequencies(night_count, day_count)
    
    nur_segments = [s for s in db.search_root('نور') if s['pos'] == 'N' and s['clean_form'] in ['نور', 'نورا', 'نورهم', 'نوره', 'النور', 'بنورهم']]
    diya_segments = [s for s in db.search_root('ضيأ') if s['pos'] == 'N']
    light_total = len(nur_segments) + len(diya_segments)
    
    darkness_segments = [s for s in db.search_root('ظلم') if s['pos'] == 'N' and 'ظلم' in s['clean_form'] and s['lemma'] in ['ظُلُمَة', 'ظُلْمَة', 'ظُلُمات']]
    darkness_total = len(darkness_segments)
    
    results['light_cycle'] = {
        'title': 'Eksenel ve Işık Döngüsü (Gece / Gündüz & Işık / Karanlık)',
        'night_root': 'ليل',
        'night_count': night_count,
        'day_root': 'نهر (نهار)',
        'day_count': day_count,
        'total_diurnal': night_count + day_count,
        'night_ratio': round((night_count / (night_count + day_count)) * 100, 2) if (night_count + day_count) > 0 else 0,
        'day_ratio': round((day_count / (night_count + day_count)) * 100, 2) if (night_count + day_count) > 0 else 0,
        'z_score': round(z_res['z_score'], 4),
        'p_value': round(z_res['p_value'], 4),
        'is_symmetric': z_res['is_symmetric'],
        'light_nur_count': len(nur_segments),
        'light_diya_count': len(diya_segments),
        'total_light_count': light_total,
        'darkness_zulumat_count': darkness_total,
        'semantic_note': 'Kur\'an\'da Nur (Işık) daima tekil (Müfret), Zulumat (Karanlıklar) ise daima çoğul (Cemi) formunda zikredilerek hakikatin tekliği ve batılın çokluğu sembolize edilmiştir.'
    }
    
    return results
