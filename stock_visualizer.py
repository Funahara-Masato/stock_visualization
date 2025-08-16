import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc

# ===== 設定 =====
ticker_symbol = "7203.T"  # トヨタ自動車
output_csv = "stock_portfolio.csv"

# ===== 株価データ取得 =====
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="60d")  # 過去60営業日
        if df.empty:
            raise ValueError("yfinanceからデータ取得失敗")
        df.reset_index(inplace=True)
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        return df
    except Exception as e:
        print(f"[警告] yfinance失敗: {e} → ダミーデータを作成します")
        dates = pd.date_range(end=datetime.now(), periods=60)
        return pd.DataFrame({
            "Date": dates.strftime('%Y-%m-%d'),
            "Open": [None]*60,
            "High": [None]*60,
            "Low": [None]*60,
            "Close": [None]*60,
            "Volume": [None]*60
        })

# ===== 実行 =====
try:
    stock_df = get_stock_data(ticker_symbol)

    # 日次変化率（リターン）の計算
    stock_df['Return'] = stock_df['Close'].pct_change() * 100
    stock_df['Return'] = stock_df['Return'].round(2)

    # 移動平均線（5日・25日）
    stock_df['MA5'] = stock_df['Close'].rolling(window=5).mean()
    stock_df['MA25'] = stock_df['Close'].rolling(window=25).mean()

    # CSV保存
    stock_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"\n保存完了: {output_csv}")

    # ===== 説明を表示 =====
    print("\n=== 各列の意味 ===")
    print("Date  : 日付")
    print("Open  : 始値")
    print("High  : 高値")
    print("Low   : 安値")
    print("Close : 終値")
    print("Volume: 出来高（株数）")
    print("Return: 日次変化率（前日比％）")
    print("MA5   : 5日移動平均")
    print("MA25  : 25日移動平均")

    # 取得結果を標準出力
    print("\n=== 株価データ ===")
    print(stock_df)

    # ===== 株価グラフ =====
    # 日付をdatetime型に変換し、ローソク足用に数値化
    stock_df['Date_dt'] = pd.to_datetime(stock_df['Date'])

    # 連続する整数インデックスを作成（X軸用）
    stock_df['Index'] = range(len(stock_df))

    # Figureを2つのサブプロットで作成（上：価格、下：出来高）
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12,8), sharex=True, gridspec_kw={'height_ratios': [3, 1]}
    )

    # ローソク足データの抽出
    ohlc = stock_df[['Index', 'Open', 'High', 'Low', 'Close']].values
        
    # ローソク足を描画
    candlestick_ohlc(ax1, ohlc, width=0.6, colorup='r', colordown='b', alpha=0.8)

    # 終値と移動平均を重ねて描画
    ax1.plot(stock_df['Index'], stock_df['Close'], color='black', label='Close', alpha=0.6)
    ax1.plot(stock_df['Index'], stock_df['MA5'], color='orange', label='MA5')
    ax1.plot(stock_df['Index'], stock_df['MA25'], color='green', label='MA25')

    # 上段（価格）の軸ラベル・タイトル・凡例・グリッド
    ax1.set_ylabel('Price (JPY)')
    ax1.set_title(f'{ticker_symbol} Stock Price & Moving Averages')
    ax1.legend()
    ax1.grid(True)

    # 下段（出来高）の棒グラフを描画
    ax2.bar(stock_df['Index'], stock_df['Volume'], color='purple')
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Date')
    ax2.grid(True)

    # データがある日だけ2日ごとにラベル表示
    date_labels = stock_df['Date_dt'].dt.strftime('%Y-%m-%d').values
    ax2.set_xticks(range(0, len(stock_df), 2))  # 2日ごと
    ax2.set_xticklabels(date_labels[::2], rotation=45)

    # レイアウト調整して表示
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"[エラー] データ処理中に問題が発生しました: {e}")