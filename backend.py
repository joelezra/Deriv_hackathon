from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Mock database
users = {'user1': {'balance': 10000, 'portfolio': {}}}

@app.route('/login', methods=['POST'])
def login():
    # Simplified login logic
    username = request.json.get('username')
    if username in users:
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/balance', methods=['GET'])
def get_balance():
    username = request.args.get('username')
    if username in users:
        return jsonify({'balance': users[username]['balance']}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/buy', methods=['POST'])
def buy_stock():
    username = request.json.get('username')
    stock = request.json.get('stock')
    amount = request.json.get('amount')
    # Simplified buy logic
    if username in users:
        users[username]['portfolio'][stock] = users[username]['portfolio'].get(stock, 0) + amount
        return jsonify({'message': f'Bought {amount} of {stock}'}), 200
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
