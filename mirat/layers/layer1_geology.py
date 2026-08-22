#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Katman 1: Coğrafi ve Jeolojik Durumlar Katmanı
- Küme A: Yüzey Alanı Dengesi (Deniz [بحر] vs Kara [برر/يبس]) -> %71 - %29 Oranı ve Ki-Kare Testi
- Küme B: İzostazi ve Yerkabuğu Dengesi (Dağ [جبل] vs Kazık [وتد]) -> Co-occurrence Matrisi
"""

from mirat.database import MiratDB
from mirat.stats import chi_square_goodness_of_fit, co_occurrence_metrics

def analyze_layer_1(db=None):
    if db is None:
        db = MiratDB()
        
    results = {}
    
    # ---------------------------------------------------------
    # KÜME A: Yüzey Alanı Dengesi (Deniz vs Kara)
    # ---------------------------------------------------------
    # Deniz: Kök 'بحر'
    sea_segments = db.search_root('بحر')
    # İsim ve ilgili formları filtrele
    sea_ayahs = set((s['surah'], s['ayah']) for s in sea_segments)
    sea_count = len(sea_segments)
    
    # Kara: Kök 'برر' (İsim/Kara anlamındaki 'بَرّ' formları)
    land_barr_segments = [s for s in db.search_root('برر') if s['pos'] == 'N' and s['clean_form'] in ['بر', 'برا', 'بركم', 'بريه', 'البر']]
    # Kuru toprak: Kök 'يبس'
    land_yabs_segments = [s for s in db.search_root('يبس') if s['pos'] == 'N']
    
    land_all_segments = land_barr_segments + land_yabs_segments
    land_ayahs = set((s['surah'], s['ayah']) for s in land_all_segments)
    
    barr_count = len(land_barr_segments)
    yabs_count = len(land_yabs_segments)
    total_land_count = len(land_all_segments)
    
    total_water_land = sea_count + total_land_count
    
    # Dünya Bilimsel Su/Kara Oranı: %71.11 Deniz, %28.89 Kara
    earth_water_prop = 0.7111
    earth_land_prop = 0.2889
    
    observed_props = [sea_count / total_water_land, total_land_count / total_water_land] if total_water_land > 0 else [0, 0]
    
    chi2_res = chi_square_goodness_of_fit(
        [sea_count, total_land_count],
        [earth_water_prop, earth_land_prop]
    )
    
    results['surface_balance'] = {
        'title': 'Yüzey Alanı Dengesi (Deniz / Kara Oranı)',
        'sea_root': 'بحر',
        'sea_count': sea_count,
        'sea_ayah_count': len(sea_ayahs),
        'land_barr_count': barr_count,
        'land_yabs_count': yabs_count,
        'total_land_count': total_land_count,
        'land_ayah_count': len(land_ayahs),
        'total_tokens': total_water_land,
        'observed_ratio_sea': round(observed_props[0] * 100, 2),
        'observed_ratio_land': round(observed_props[1] * 100, 2),
        'expected_ratio_sea': round(earth_water_prop * 100, 2),
        'expected_ratio_land': round(earth_land_prop * 100, 2),
        'chi2_stat': round(chi2_res['chi2'], 4),
        'p_value': round(chi2_res['p_value'], 4),
        'is_fit_significant': chi2_res['p_value'] >= 0.05, # p >= 0.05 means NO significant difference from reality!
        'details': chi2_res
    }
    
    # ---------------------------------------------------------
    # KÜME B: İzostazi ve Yerkabuğu Dengesi (Dağ [جبل] vs Kazık [وتد])
    # ---------------------------------------------------------
    mountain_segments = db.search_root('جبل')
    peg_segments = db.search_root('وتد')
    
    mountain_ayahs = set((s['surah'], s['ayah']) for s in mountain_segments)
    peg_ayahs = set((s['surah'], s['ayah']) for s in peg_segments)
    
    cooccur = co_occurrence_metrics(mountain_ayahs, peg_ayahs)
    
    results['isostasy'] = {
        'title': 'İzostazi ve Yerkabuğu Dengesi (Dağ / Kazık)',
        'mountain_root': 'جبل',
        'mountain_count': len(mountain_segments),
        'mountain_ayahs_count': len(mountain_ayahs),
        'peg_root': 'وتد',
        'peg_count': len(peg_segments),
        'peg_ayahs_count': len(peg_ayahs),
        'co_occurring_ayahs_count': cooccur['count_both'],
        'co_occurring_ayahs': cooccur['co_occurring_ayahs'],
        'pmi': round(cooccur['pmi'], 3),
        'jaccard': round(cooccur['jaccard_similarity'], 4),
        'odds_ratio': round(cooccur['odds_ratio'], 2) if cooccur['odds_ratio'] != float('inf') else 'inf',
        'key_verse': '78:6-7 (Nebe Suresi: "Yeryüzünü bir beşik, dağları da birer kazık (وتد) yapmadık mı?")'
    }
    
    return results

if __name__ == "__main__":
    import json
    res = analyze_layer_1()
    print(json.dumps(res, indent=2, ensure_ascii=False))
