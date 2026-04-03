from Banking_System_SQLite import authenticate, BankDatabase

def main():
    db = BankDatabase()

    while True:
        print("\n--- Welcome to Online Bank Management System ---")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Take Loan (with Interest Information)")
        print("6. Pay Loan")
        print("7. Savings Interest Information")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':  # Create Account
            acc_num = input("Enter account number (8 digits only): ").strip()
            name = input("Enter holder name: ").strip()
            password = input("Set a password: ").strip()
            acc_type = input("Enter account type (regular/savings): ").strip().lower()
            balance = float(input("Enter initial deposit: "))
            interest_rate = 0.05 if acc_type == "savings" else 0.0
            db.create_account(acc_num, name, password, balance, acc_type, interest_rate)
            print("Account created successfully.")

        elif choice == '2':  # Deposit Money
            acc_num = input("Enter account number: ").strip()
            account = authenticate(db, acc_num)
            if account:
                amount = float(input("Enter deposit amount: "))
                db.update_balance(acc_num, account[3] + amount)
                print(f"Deposit successful. New balance: {account[3] + amount}")

        elif choice == '3':  # Withdraw Money
            acc_num = input("Enter account number: ").strip()
            account = authenticate(db, acc_num)
            if account:
                if account[4] == "savings":
                    print("Cannot withdraw from savings account within the first year.")
                else:
                    amount = float(input("Enter withdrawal amount: "))
                    if amount <= account[3]:
                        db.update_balance(acc_num, account[3] - amount)
                        print(f"Withdrawal successful. New balance: {account[3] - amount}")
                    else:
                        print("Insufficient funds.")

        elif choice == '4':  # Check Balance
            acc_num = input("Enter account number: ").strip()
            account = authenticate(db, acc_num)
            if account:
                print(f"\n--- Account Details ---")
                print(f"Account Number: {account[0]}")
                print(f"Holder Name: {account[1]}")
                print(f"Account Type: {account[4]}")
                print(f"Balance: {account[3]}")
                print(f"Interest Rate (Savings Only): {account[5]}\n")

        elif choice == '5':  # Take Loan (with Interest Information)
            acc_num = input("Enter account number: ").strip()
            account = authenticate(db, acc_num)
            if account:
                amount = float(input("Enter loan amount (positive): "))
                term = int(input("Enter loan term in months: "))
                interest_rate = 0.03  # Default interest rate for loans

                # Calculating Loan Interest Information
                interest = amount * interest_rate * (term / 12)
                total_payment = amount + interest

                print(f"\n--- Loan Information ---")
                print(f"Loan Amount: {amount}")
                print(f"Interest Rate: {interest_rate * 100:.2f}%")
                print(f"Loan Term: {term} months")
                print(f"Interest to Pay: {interest:.2f}")
                print(f"Total Payment (Principal + Interest): {total_payment:.2f}")

                confirm = input("\nDo you want to proceed with this loan? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    db.take_loan(acc_num, amount, interest_rate, term)
                else:
                    print("Loan request cancelled.")

        elif choice == '6':  # Pay Loan (with Authentication and Loan Information)
            acc_num = input("Enter account number: ").strip()
            account = authenticate(db, acc_num)
            if account:
                # Displaying current loan information
                db.cursor.execute("SELECT loan_amount FROM loans WHERE account_number = ?", (acc_num,))
                loan = db.cursor.fetchone()

                if loan and loan[0] > 0:
                    print(f"\nYou currently owe: {loan[0]:.2f}")
                    amount = float(input("Enter repayment amount: "))

                    if amount > loan[0]:
                        print(f"Error: You can only repay up to {loan[0]:.2f}.")
                    else:
                        db.repay_loan(acc_num, amount)
                else:
                    print("No active loan to repay.")

        elif choice == '7':  # Savings Interest Information
            acc_num = input("Enter account number: ").strip()
            account = authenticate(db, acc_num)
            if account and account[4] == "savings":
                years = int(input("Enter the number of years you want to keep your money: "))
                savings_final = db.calculate_savings_interest(acc_num, years)
                print(f"\n--- Savings Summary ---")
                print(f"Initial Balance: {account[3]}")
                print(f"Interest Rate: {account[5] * 100:.2f}%")
                print(f"Time Period: {years} years")
                print(f"Projected Balance after {years} Years: {savings_final:.2f}")
            else:
                print("Savings account not found or not a savings account.")

        elif choice == '8':  # Exit
            db.close()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


