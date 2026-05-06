from flask import Flask, render_template, jsonify
import yfinance as yf

app = Flask(__name__)

# Your Bloomberg-style Watchlist
WATCHLIST = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'META']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    results = []
    for ticker in WATCHLIST:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Use current price or previous close if market is closed
            current_price = info.get('currentPrice', info.get('previousClose', 0))
            market_cap = info.get('marketCap', 0)
            total_debt = info.get('totalDebt', 0)
            
            if market_cap and market_cap > 0:
                debt_ratio = (total_debt / market_cap) * 100
                is_halal = debt_ratio < 30.0
                
                results.append({
                    "ticker": ticker,
                    "price": f"${current_price:,.2f}",
                    "market_cap": f"${market_cap / 1e9:,.2f}B", # Formatted in Billions
                    "debt_ratio": f"{debt_ratio:.2f}%",
                    "status": "HALAL" if is_halal else "HARAM",
                    "status_class": "halal" if is_halal else "haram"
                })
            else:
                # Fallback if data is missing for a ticker
                results.append({"ticker": ticker, "price": "-", "market_cap": "-", "debt_ratio": "-", "status": "NO DATA", "status_class": "error"})
                
        except Exception as e:
            results.append({"ticker": ticker, "price": "-", "market_cap": "-", "debt_ratio": "-", "status": "FETCH ERROR", "status_class": "error"})
            
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
