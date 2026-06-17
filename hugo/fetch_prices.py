import yfinance as yf

tickers = ["BA", "AMZN", "TSLA", "GOOGL", "META"]
start = "2024-03-01"
end = "2025-02-15"

data = yf.download(tickers, start=start, end=end)["Close"]
data.to_csv("hugo/stock_prices.csv")
print(data.tail())
print(f"Saved {len(data)} rows to hugo/stock_prices.csv")