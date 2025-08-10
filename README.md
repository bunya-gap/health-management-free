# 体組成管理アプリ - Railway クラウド版

## 概要

Health Auto Export iOS アプリから送信される体組成データを受信し、処理するRailway.app用Webサーバーです。

## 特徴

- ✅ **クラウドネイティブ**: Railway.app完全対応
- ✅ **24時間稼働**: PC不要の安定稼働
- ✅ **HTTPS対応**: セキュアな通信
- ✅ **自動スケーリング**: トラフィックに応じた拡張
- ✅ **ログ監視**: Railway標準監視機能

## 技術スタック

- **Web Framework**: Flask 2.0+
- **WSGI Server**: Gunicorn
- **Platform**: Railway.app
- **Runtime**: Python 3.9+
- **Data Format**: JSON/CSV

## エンドポイント

### POST /health-data
Health Auto Export アプリからのデータ受信

### GET /health-data  
サーバー稼働確認

### GET /health-check
シンプルなヘルスチェック

### GET /latest-data
最新データファイルの確認

## デプロイ方法

1. **Railway.app**でプロジェクト作成
2. **このリポジトリを接続**
3. **環境変数設定**：
   - `LINE_BOT_CHANNEL_ACCESS_TOKEN`
   - `LINE_USER_ID`  
   - `OURA_ACCESS_TOKEN`
4. **自動デプロイ実行**

## ローカル開発

```bash
pip install -r requirements.txt
python health_data_server.py
```

サーバーは `http://localhost:5000` で起動します。

## 環境変数

```bash
PORT=5000  # Railway自動設定
LINE_BOT_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_USER_ID=your_user_id_here  
OURA_ACCESS_TOKEN=your_oura_token_here
```

## ファイル構成

```
.
├── Procfile                 # Railway起動設定
├── requirements.txt         # Python依存関係
├── health_data_server.py    # メインアプリケーション
├── .gitignore              # Git除外設定
└── README.md               # このファイル
```

## モニタリング

Railway.appの標準監視機能で以下を確認可能：

- アプリケーションログ
- CPU/メモリ使用率
- レスポンス時間
- エラー率

## サポート

技術的な問題や質問については、Issueを作成してください。