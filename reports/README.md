# 健康分析結果・CSVデータ保存ディレクトリ

このディレクトリには、処理済み健康データと分析結果が保存されます。

## 生成ファイル一覧

### CSVデータファイル
- `daily_health_data.csv` - 日次健康データ（24カラム）
- `health_data_with_ma.csv` - 移動平均データ（7日/14日/28日）
- `health_data_index.csv` - インデックス付きデータ

### 分析結果ファイル
- `analysis_report_*.json` - 健康分析レポート（LINE通知内容）

## 自動更新
GitHub Actions により、HAEデータ受信時に自動的に更新・Git保存されます。
