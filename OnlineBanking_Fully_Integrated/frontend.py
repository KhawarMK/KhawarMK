from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from Banking_System_SQLite import BankDatabase
import os

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Initialize Database
db = BankDatabase()

# Serve the Frontend (HTML, CSS, JS)
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

# Serve Static Files (CSS, JS)
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('frontend', filename)

# API Route: Create Account (Regular or Savings)
@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    account_number = data.get('account_number')
    holder_name = data.get('holder_name')
    password = data.get('password')
    account_type = data.get('account_type')

    if not account_number or not holder_name or not password:
        return jsonify({'message': 'All fields are required.', 'error': True}), 400

    # Check if account already exists
    existing_account = db.get_account(account_number)
    if existing_account:
        return jsonify({'message': 'Account number already exists.', 'error': True}), 400

    # Create the new account
    db.create_account(account_number, holder_name, password, 0.0, account_type, 0.05 if account_type == "savings" else 0.0)
    return jsonify({'message': f'{account_type.capitalize()} Account {account_number} created successfully.'})

# API Route: Check Balance (With Authentication)
@app.route('/check_balance', methods=['POST'])
def check_balance():
    data = request.json
    account_number = data.get('account_number')
    password = data.get('password')

    account = db.get_account(account_number)
    if not account:
        return jsonify({'message': 'Account not found.', 'error': True}), 404

    # Authenticate User
    hashed_password = db.hash_password(password)
    if account[2] == hashed_password:
        return jsonify({'balance': account[3]})
    else:
        return jsonify({'message': 'Incorrect password.', 'error': True}), 401

# API Route: Deposit Money
@app.route('/deposit', methods=['POST'])
def deposit_money():
    data = request.json
    account_number = data.get('account_number')
    amount = float(data.get('amount'))

    account = db.get_account(account_number)
    if not account:
        return jsonify({'message': 'Account not found.', 'error': True}), 404

    new_balance = account[3] + amount
    db.update_balance(account_number, new_balance)
    return jsonify({'message': f'Deposit successful. New balance: ${new_balance:.2f}'})

# API Route: Withdraw Money (Regular Accounts Only)
@app.route('/withdraw', methods=['POST'])
def withdraw_money():
    data = request.json
    account_number = data.get('account_number')
    amount = float(data.get('amount'))

    account = db.get_account(account_number)
    if not account:
        return jsonify({'message': 'Account not found.', 'error': True}), 404

    if account[4] == "savings":
        return jsonify({'message': 'Withdrawals are not allowed from savings accounts.', 'error': True}), 403

    if account[3] < amount:
        return jsonify({'message': 'Insufficient funds.', 'error': True}), 400

    new_balance = account[3] - amount
    db.update_balance(account_number, new_balance)
    return jsonify({'message': f'Withdrawal successful. New balance: ${new_balance:.2f}'})

# API Route: Calculate Savings Interest (Only for Savings Accounts)
@app.route('/calculate_savings', methods=['POST'])
def calculate_savings():
    data = request.json
    account_number = data.get('account_number')
    years = int(data.get('years'))

    account = db.get_account(account_number)
    if not account or account[4] != "savings":
        return jsonify({'message': 'Savings account not found.', 'error': True}), 404

    final_amount = db.calculate_savings_interest(account_number, years)
    return jsonify({'message': f'Projected Savings Balance after {years} years: ${final_amount:.2f}'})

# API Route: Take Loan
@app.route('/take_loan', methods=['POST'])
def take_loan():
    data = request.json
    account_number = data.get('account_number')
    amount = float(data.get('amount'))
    term = int(data.get('term'))

    db.take_loan(account_number, amount, 0.03, term)
    return jsonify({'message': f'Loan of ${amount:.2f} taken for {term} months.'})

# API Route: Pay Loan
@app.route('/pay_loan', methods=['POST'])
def pay_loan():
    data = request.json
    account_number = data.get('account_number')
    amount = float(data.get('amount'))

    db.repay_loan(account_number, amount)
    return jsonify({'message': f'Loan payment of ${amount:.2f} successful.'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
