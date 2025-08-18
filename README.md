# 株価可視化ツール

このリポジトリでは、株価データを取得し、移動平均やグラフで可視化するPythonコードを公開しています。

## 特徴
- 株価データ（終値）の可視化
- 移動平均線の描画
- 土日・祝日などデータが存在しない日は自動的にスキップ

## 必要なライブラリ
以下のPythonライブラリを使用しています。
- pandas
- matplotlib
- yfinance （株価データ取得用）

インストール例：
```bash
pip install pandas matplotlib yfinance
