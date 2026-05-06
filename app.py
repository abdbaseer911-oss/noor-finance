from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/screen', methods=['POST'])
def screen_stock():
    data = request.json
    company_name = data.get('company')
    debt = float(data.get('debt', 0))
    market_cap = float(data.get('market_cap', 1)) # Prevent division by zero
    
    # Basic Sharia Compliance Check (Debt / Market Cap < 30%)
    debt_ratio = (debt / market_cap) * 100
    
    is_halal = debt_ratio < 30.0
    
    result = {
        "company": company_name,
        "debt_ratio": round(debt_ratio, 2),
        "status": "Sharia Compliant (Halal)" if is_halal else "Non-Compliant (Haram)",
        "message": f"Debt ratio is {round(debt_ratio, 2)}% (Threshold is 30%)"
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
