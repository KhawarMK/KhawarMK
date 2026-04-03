const BASE_URL = "http://localhost:5000";

// Show Sections
function showSection(section) {
    document.querySelectorAll(".section").forEach(sec => sec.style.display = "none");
    document.getElementById(`${section}-section`).style.display = "block";
}

// Create Account (Regular or Savings)
async function createAccount() {
    const accountNumber = document.getElementById("account-number").value;
    const holderName = document.getElementById("holder-name").value;
    const password = document.getElementById("password").value;
    const accountType = document.getElementById("account-type").value;

    if (!accountNumber || !holderName || !password) {
        showMessage("Please fill in all fields.");
        return;
    }

    const response = await fetch(`${BASE_URL}/create_account`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            account_number: accountNumber,
            holder_name: holderName,
            password: password,
            account_type: accountType
        })
    });

    const data = await response.json();
    showMessage(data.message);
}

// Check Balance (with Authentication)
async function checkBalance() {
    const accountNumber = document.getElementById("login-account-number").value;
    const password = document.getElementById("login-password").value;

    if (!accountNumber || !password) {
        showMessage("Please enter account number and password.");
        return;
    }

    const response = await fetch(`${BASE_URL}/check_balance`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ account_number: accountNumber, password: password })
    });

    const data = await response.json();
    showMessage(data.balance ? `Balance: $${data.balance}` : data.message);
}

// Deposit Money
async function depositMoney() {
    const accountNumber = document.getElementById("transaction-account").value;
    const password = document.getElementById("transaction-password").value;
    const amount = parseFloat(document.getElementById("amount").value);

    if (!accountNumber || !password || !amount) {
        showMessage("Please enter all details.");
        return;
    }

    const response = await fetch(`${BASE_URL}/deposit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ account_number: accountNumber, amount: amount })
    });

    const data = await response.json();
    showMessage(data.message);
}

// Withdraw Money (Regular Accounts Only)
async function withdrawMoney() {
    const accountNumber = document.getElementById("transaction-account").value;
    const password = document.getElementById("transaction-password").value;
    const amount = parseFloat(document.getElementById("amount").value);

    if (!accountNumber || !password || !amount) {
        showMessage("Please enter all details.");
        return;
    }

    const response = await fetch(`${BASE_URL}/withdraw`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ account_number: accountNumber, amount: amount })
    });

    const data = await response.json();
    showMessage(data.message);
}

// Take Loan
async function takeLoan() {
    const accountNumber = document.getElementById("loan-account").value;
    const password = document.getElementById("loan-password").value;
    const amount = parseFloat(document.getElementById("loan-amount").value);
    const term = parseInt(document.getElementById("loan-term").value);

    if (!accountNumber || !password || !amount || !term) {
        showMessage("Please enter all loan details.");
        return;
    }

    const response = await fetch(`${BASE_URL}/take_loan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ account_number: accountNumber, amount: amount, term: term })
    });

    const data = await response.json();
    showMessage(data.message);
}

// Pay Loan
async function payLoan() {
    const accountNumber = document.getElementById("loan-account").value;
    const password = document.getElementById("loan-password").value;
    const amount = parseFloat(prompt("Enter repayment amount:"));

    if (!accountNumber || !password || !amount) {
        showMessage("Please enter all loan payment details.");
        return;
    }

    const response = await fetch(`${BASE_URL}/pay_loan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ account_number: accountNumber, amount: amount })
    });

    const data = await response.json();
    showMessage(data.message);
}

// Calculate Savings Interest (Only for Savings Accounts)
async function calculateSavings() {
    const accountNumber = document.getElementById("savings-account").value;
    const password = document.getElementById("savings-password").value;
    const years = parseInt(document.getElementById("savings-years").value);

    if (!accountNumber || !password || !years) {
        showMessage("Please enter all savings details.");
        return;
    }

    const response = await fetch(`${BASE_URL}/calculate_savings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ account_number: accountNumber, years: years })
    });

    const data = await response.json();
    showMessage(data.message);
}

// Utility: Show Messages
function showMessage(message) {
    const responseDiv = document.getElementById("response");
    responseDiv.innerText = message;
    responseDiv.style.display = "block";
    setTimeout(() => responseDiv.style.display = "none", 4000);
}
