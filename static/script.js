function goApply() {
  window.location.href = "apply.html";
}


function calculateEMI() {
    let P = document.getElementById("loanAmount").value;
    let R = document.getElementById("interestRate").value;
    let N = document.getElementById("loanMonths").value;

    if (P === "" || R === "" || N === "") {
        document.getElementById("emiResult").innerHTML = "⚠ Please fill all fields";
        return;
    }

    P = parseFloat(P);
    R = parseFloat(R) / 12 / 100;
    N = parseInt(N);

    let EMI;

    if (R === 0) {
        EMI = P / N;
    } else {
        EMI = (P * R * Math.pow(1 + R, N)) / (Math.pow(1 + R, N) - 1);
    }

    document.getElementById("emiResult").innerHTML = "Monthly EMI: ₹" + EMI.toFixed(2);
}


function trackLoan() {
  const id = document.getElementById("trackId").value.trim();
  if (id === "") {
    alert("Enter Application ID");
    return;
  }
  document.getElementById("trackResult").innerHTML =
    `Application <b>${id}</b> Status: <span class="badge">Under Verification</span>`;
}
