function togglePaymentFields(value) {
  document.getElementById("card-fields").style.display = value === "card" ? "block" : "none";
  document.getElementById("transfer-fields").style.display = value === "transfer" ? "block" : "none";
  document.getElementById("loan-fields").style.display = value === "loan" ? "block" : "none";
}

document.addEventListener("DOMContentLoaded", function () {
  const selectedMethod = document.querySelector("select[name='payment_method']").value;
  togglePaymentFields(selectedMethod);

  document.querySelector("select[name='payment_method']").addEventListener("change", function (e) {
    togglePaymentFields(e.target.value);
  });
});
