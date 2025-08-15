#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git状況確認ツール
"""

import subprocess
import os
import sys
from pathlib import Path

# Unicode出力対応
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def check_git_status():
    """Git状況を確認"""
    
    project_dir = Path(r"C:\Users\terada\Desktop\apps\体組成管理app")
    os.chdir(project_dir)
    
    print(f"Current directory: {os.getcwd()}")
    
    try:
        # Git status確認
        print("\n=== GIT STATUS ===")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print("Modified files:")
            print(result.stdout)
        else:
            print("No modified files (clean working directory)")
        
        # Git log確認（最新5件）
        print("\n=== RECENT COMMITS ===")
        result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                              capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        
        # リモートとの差異確認
        print("\n=== REMOTE COMPARISON ===")
        result = subprocess.run(['git', 'fetch', 'origin', 'main'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        result = subprocess.run(['git', 'status', '-uno'], 
                              capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        
        # 特定ファイルの最終更新時刻確認
        print("\n=== FILE TIMESTAMPS ===")
        csv_file = project_dir / "reports" / "daily_health_data.csv"
        if csv_file.exists():
            import datetime
            mtime = csv_file.stat().st_mtime
            formatted_time = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"daily_health_data.csv last modified: {formatted_time}")
        else:
            print("daily_health_data.csv not found")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_git_status()
