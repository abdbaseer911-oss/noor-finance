from flask import Flask, render_template, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/screen', methods=['POST'])
def screen_stock():
    data = request.json
    ticker_symbol = data.get('ticker', '').upper()
    
    if not ticker_symbol:
        return jsonify({"error": "Please enter a ticker symbol."})

    try:
        # Fetch live data from Yahoo Finance
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        
        company_name = info.get('shortName', ticker_symbol)
        market_cap = info.get('marketCap', 0)
        total_debt = info.get('totalDebt', 0)
        
        if market_cap == 0:
            return jsonify({"error": f"Could not find market data for {ticker_symbol}."})
            
        # Sharia Check (Debt / Market Cap < 30%)
        debt_ratio = (total_debt / market_cap) * 100
        is_halal = debt_ratio < 30.0
        
        result = {
            "company": company_name,
            "ticker": ticker_symbol,
            "market_cap": f"${market_cap:,.0f}",
            "total_debt": f"${total_debt:,.0f}",
            "debt_ratio": round(debt_ratio, 2),
            "status": "Sharia Compliant (Halal)" if is_halal else "Non-Compliant (Haram)",
            "message": f"Debt to Market Cap ratio is {round(debt_ratio, 2)}% (Threshold is 30%)"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to fetch data. Check the ticker symbol."})

if __name__ == '__main__':
    app.run(debug=True)
