"""
Health Auto Export データ受信サーバー
Health Auto Export REST API から送信されたデータを受信・保存
"""

from flask import Flask, request, jsonify
import json
import pandas as pd
from datetime import datetime, date
import os
from typing import Dict, List, Any

app = Flask(__name__)

# データ保存ディレクトリ
DATA_DIR = os.path.join(os.path.dirname(__file__), 'health_api_data')
os.makedirs(DATA_DIR, exist_ok=True)

def save_raw_data(data: Dict[str, Any]) -> str:
    """受信した生データをJSONファイルに保存"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"health_data_{timestamp}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    return filename

def process_health_metrics(metrics: List[Dict]) -> pd.DataFrame:
    """ヘルスメトリクスを処理してDataFrameに変換"""
    processed_data = []
    
    for metric in metrics:
        name = metric.get('name', '')
        units = metric.get('units', '')
        data_points = metric.get('data', [])
        
        for point in data_points:
            row = {
                'metric_name': name,
                'units': units,
                'date': point.get('date', ''),
                'qty': point.get('qty', None),
                'source': metric.get('source', ''),
            }
            
            # 特殊なメトリクス（血圧、睡眠など）の追加フィールド処理
            for key, value in point.items():
                if key not in ['date', 'qty']:
                    row[f'{name}_{key}'] = value
            
            processed_data.append(row)
    
    return pd.DataFrame(processed_data) if processed_data else pd.DataFrame()

@app.route('/health-data', methods=['POST'])
def receive_health_data():
    """Health Auto Export からのデータ受信エンドポイント"""
    try:
        # セッションIDをヘッダーから取得
        session_id = request.headers.get('session-id', 'unknown')
        
        # JSONデータを取得
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # 生データを保存
        filename = save_raw_data(data)
        print(f"Data received (Session: {session_id}) - Saved as: {filename}")
        
        # データ構造を確認
        metrics = data.get('data', {}).get('metrics', [])
        workouts = data.get('data', {}).get('workouts', [])
        
        print(f"Received {len(metrics)} metrics, {len(workouts)} workouts")
        
        # メトリクスを処理してCSV保存
        if metrics:
            df_metrics = process_health_metrics(metrics)
            if not df_metrics.empty:
                csv_filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                csv_path = os.path.join(DATA_DIR, csv_filename)
                df_metrics.to_csv(csv_path, index=False, encoding='utf-8-sig')
                print(f"Metrics saved as CSV: {csv_filename}")
        
        return jsonify({
            'status': 'success',
            'message': 'Data received and processed',
            'metrics_count': len(metrics),
            'workouts_count': len(workouts),
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health-data', methods=['GET'])
def health_check():
    """サーバー稼働確認エンドポイント"""
    return jsonify({
        'status': 'Health Auto Export Data Server is running',
        'timestamp': datetime.now().isoformat(),
        'data_directory': DATA_DIR
    })

@app.route('/health-check', methods=['GET'])
def health_check_simple():
    """シンプルなヘルスチェックエンドポイント（監視用）"""
    return jsonify({
        'status': 'OK',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/latest-data', methods=['GET'])
def get_latest_data():
    """最新のデータファイルを確認"""
    try:
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
        if not files:
            return jsonify({'message': 'No data files found'})
        
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(DATA_DIR, x)))
        
        with open(os.path.join(DATA_DIR, latest_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return jsonify({
            'latest_file': latest_file,
            'data_preview': {
                'metrics_count': len(data.get('data', {}).get('metrics', [])),
                'workouts_count': len(data.get('data', {}).get('workouts', [])),
                'first_few_metrics': data.get('data', {}).get('metrics', [])[:3]
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Health Auto Export Data Server Starting...")
    print(f"Data will be saved to: {DATA_DIR}")
    print(f"Health Auto Export should POST data to: http://localhost:{port}/health-data")
    print(f"Server health check: http://localhost:{port}/health-data (GET)")
    
    app.run(host='0.0.0.0', port=port, debug=False)