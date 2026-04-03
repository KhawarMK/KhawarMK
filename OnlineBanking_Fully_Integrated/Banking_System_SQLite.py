import sqlite3
import hashlib

class BankDatabase:
    def __init__(self, db_path="bank_system.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)  # Thread-safe
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            holder_name TEXT,
            password TEXT,
            balance REAL,
            account_type TEXT,
            interest_rate REAL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            account_number TEXT PRIMARY KEY,
            loan_amount REAL,
            loan_interest REAL,
            loan_term_months INTEGER,
            FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        )
        """)
        self.connection.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self, account_number, holder_name, password, balance=0, account_type='regular', interest_rate=0.0):
        hashed_password = self.hash_password(password)
        self.cursor.execute("""
        INSERT INTO accounts (account_number, holder_name, password, balance, account_type, interest_rate)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (account_number, holder_name, hashed_password, balance, account_type, interest_rate))
        self.connection.commit()

    def get_account(self, account_number):
        self.cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
        return self.cursor.fetchone()

    def update_balance(self, account_number, new_balance):
        self.cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
        self.connection.commit()

    def take_loan(self, account_number, amount, interest_rate=0.03, term_months=12):
        self.cursor.execute("""
        INSERT OR REPLACE INTO loans (account_number, loan_amount, loan_interest, loan_term_months)
        VALUES (?, ?, ?, ?)
        """, (account_number, amount, interest_rate, term_months))
        self.connection.commit()

        # Automatically add loan amount to account balance
        account = self.get_account(account_number)
        if account:
            new_balance = account[3] + amount
            self.update_balance(account_number, new_balance)
            print(f"Loan of {amount} added to account. New balance: {new_balance}")

    def repay_loan(self, account_number, amount):
        self.cursor.execute("SELECT loan_amount FROM loans WHERE account_number = ?", (account_number,))
        loan = self.cursor.fetchone()

        if loan and loan[0] > 0:
            current_loan_amount = loan[0]
            if amount > current_loan_amount:
                print(f"Error: You can only repay up to {current_loan_amount:.2f}.")
                return

            new_loan_amount = current_loan_amount - amount
            self.cursor.execute("UPDATE loans SET loan_amount = ? WHERE account_number = ?", (new_loan_amount, account_number))
            self.connection.commit()
            print(f"Loan repayment of {amount} successful. Remaining loan: {new_loan_amount:.2f}")
        else:
            print("No active loan to repay.")

    def calculate_loan_interest(self, account_number):
        self.cursor.execute("SELECT loan_amount, loan_interest, loan_term_months FROM loans WHERE account_number = ?", (account_number,))
        loan = self.cursor.fetchone()
        if loan:
            loan_amount, interest_rate, term_months = loan
            interest = loan_amount * interest_rate * (term_months / 12)
            print(f"Loan interest: {interest:.2f}")
            return interest
        print("No active loan found.")
        return 0.0

    def calculate_savings_interest(self, account_number, years):
        self.cursor.execute(
            "SELECT balance, interest_rate FROM accounts WHERE account_number = ? AND account_type = 'savings'",
            (account_number,))
        account = self.cursor.fetchone()
        if account:
            balance, interest_rate = account
            final_amount = balance * ((1 + interest_rate) ** years)
            return final_amount
        else:
            return 0.0

    def close(self):
        self.connection.close()


def authenticate(db, account_number):
    account = db.get_account(account_number)
    if not account:
        print("Account not found.")
        return None

    password = input("Enter your password: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if account[2] == hashed_password:
        return account
    else:
        print("Incorrect password.")
        return None
