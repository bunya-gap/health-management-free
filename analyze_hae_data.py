#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HAEデータ分析ツール - 受信メトリクス確認
"""

import json
import sys
from pathlib import Path

# Unicode出力対応
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def analyze_hae_data():
    """最新HAEデータのメトリクス分析"""
    
    # 最新HAEファイルを取得
    data_dir = Path(r"C:\Users\terada\Desktop\apps\体組成管理app\health_api_data")
    json_files = list(data_dir.glob("health_data_2025-08-15*.json"))
    
    if not json_files:
        print("ERROR: HAE JSONファイルが見つかりません")
        return
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"Latest HAE file: {latest_file.name}")
    
    # JSONデータ読み込み
    with open(latest_file, 'r', encoding='utf-8') as f:
        hae_data = json.load(f)
    
    # メトリクス分析
    data = hae_data.get('data', {})
    metrics = data.get('metrics', [])
    
    print(f"\nTotal metrics: {len(metrics)}")
    print("\n=== RECEIVED METRICS ===")
    
    # メトリクス名とソース分析
    metric_sources = {}
    for metric in metrics:
        name = metric.get('name', 'unknown')
        data_points = metric.get('data', [])
        sources = set()
        
        for point in data_points:
            source = point.get('source', 'unknown')
            sources.add(source)
        
        metric_sources[name] = list(sources)
        print(f"- {name}: {list(sources)}")
    
    # 体組成関連メトリクス確認
    print(f"\n=== BODY COMPOSITION CHECK ===")
    body_metrics = ['weight_body_mass', 'body_fat_percentage', 'lean_body_mass']
    for metric in body_metrics:
        if metric in metric_sources:
            print(f"✅ {metric}: FOUND - {metric_sources[metric]}")
        else:
            print(f"❌ {metric}: MISSING")
    
    # ソース別メトリクス数
    print(f"\n=== SOURCE SUMMARY ===")
    source_counts = {}
    for name, sources in metric_sources.items():
        for source in sources:
            source_counts[source] = source_counts.get(source, 0) + 1
    
    for source, count in sorted(source_counts.items()):
        print(f"- {source}: {count} metrics")

if __name__ == "__main__":
    analyze_hae_data()
