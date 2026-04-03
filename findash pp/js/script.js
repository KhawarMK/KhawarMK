//2632657
document.addEventListener("DOMContentLoaded", () => {
  initModals();
  initFormValidation();
  initChartSimulation();
  revealSectionsOnScroll();
});


function initModals() {
  const modals = document.querySelectorAll(".modal");
  const closeButtons = document.querySelectorAll(".close-btn");

  
  modals.forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.style.display = "none";
    });
  });

  closeButtons.forEach((btn) =>
    btn.addEventListener("click", () => {
      modals.forEach((modal) => (modal.style.display = "none"));
    })
  );
}


function showPopup(popupId) {
  const popup = document.getElementById(popupId);
  if (popup) popup.style.display = "flex";
}


function initFormValidation() {
  const form = document.getElementById("registerForm");
  if (!form) return;

  const password = document.getElementById("password");
  const confirm = document.getElementById("confirm");
  const strengthMeter = document.createElement("div");
  strengthMeter.id = "passStrength";
  password?.insertAdjacentElement("afterend", strengthMeter);

  password?.addEventListener("input", () => {
    const value = password.value;
    const strength = getPasswordStrength(value);
    strengthMeter.textContent = `Strength: ${strength.label}`;
    strengthMeter.style.color = strength.color;
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (password.value !== confirm.value) {
      alert("Passwords do not match.");
      return;
    }
    showPopup("signupSuccess");
    form.reset();
    strengthMeter.textContent = "";
  });
}


function getPasswordStrength(password) {
  if (password.length >= 8 && /[A-Z]/.test(password) && /\d/.test(password)) {
    return { label: "Strong", color: "green" };
  } else if (password.length >= 6) {
    return { label: "Medium", color: "orange" };
  }
  return { label: "Weak", color: "red" };
}


function revealSectionsOnScroll() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.1 }
  );

  document.querySelectorAll(".fade-section").forEach((section) => {
    observer.observe(section);
  });
}


function initChartSimulation() {
  if (!document.getElementById("revenueChart")) return;

  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"];
  let revenue = [12000, 14000, 16000, 18000, 20000, 22000];
  let expenses = [6000, 7000, 8000, 9500, 11000, 12500];
  let profit = revenue.map((rev, i) => rev - expenses[i]);

 
function renderChart(id, label, data, color) {
  return new Chart(document.getElementById(id), {
    type: "line",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [{
        label,
        data,
        fill: true,
        backgroundColor: color + "33",
        borderColor: color,
        tension: 0.4,
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 25000 
        },
        x: {
          grid: {
            display: false
          }
        }
      },
      plugins: {
        legend: {
          position: "top"
        }
      }
    }
  });
}


  // Create three charts (Revenue, Expenses, Profit)
  const revenueChart = renderChart("revenueChart", "Revenue ($)", revenue, "#00a3e0");
  const expensesChart = renderChart("expensesChart", "Expenses ($)", expenses, "#e53935");
  const profitChart = renderChart("profitChart", "Profit ($)", profit, "#43a047");

  // Update Charts Automatically Every 6 Seconds
  setInterval(() => {
    updateCharts(revenueChart, expensesChart, profitChart);
  }, 6000);
}

// Update Chart Data Efficiently
function updateCharts(revenueChart, expensesChart, profitChart) {
  const newRevenue = Math.round(14000 + Math.random() * 10000);
  const newExpenses = Math.round(7000 + Math.random() * 5000);
  const newProfit = newRevenue - newExpenses;

  // Add new data to all charts
  [revenueChart, expensesChart, profitChart].forEach((chart, index) => {
    chart.data.labels.push("New");
    if (chart.data.labels.length > 6) chart.data.labels.shift();
  });

  // Update data for each chart
  revenueChart.data.datasets[0].data.push(newRevenue);
  expensesChart.data.datasets[0].data.push(newExpenses);
  profitChart.data.datasets[0].data.push(newProfit);

  [revenueChart, expensesChart, profitChart].forEach((chart) => {
    if (chart.data.datasets[0].data.length > 6) chart.data.datasets[0].data.shift();
    chart.update();
  });
}
