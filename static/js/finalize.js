function togglePaymentFields(value) {
  document.getElementById("card-fields").style.display = value === "card" ? "block" : "none";
  document.getElementById("loan-fields").style.display = value === "loan" ? "block" : "none";
}

document.addEventListener("DOMContentLoaded", function () {
  const methodSelect = document.querySelector("select[name='payment_method']");
  if (methodSelect) {
    togglePaymentFields(methodSelect.value);
    methodSelect.addEventListener("change", function () {
      togglePaymentFields(this.value);
    });
  }
});
