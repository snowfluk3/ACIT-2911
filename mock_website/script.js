const snackForm = document.getElementById("snackForm");
const snackList = document.getElementById("snackList");
const totalSnacks = document.getElementById("totalSnacks");

let snackCount = 1;

snackForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const name = document.getElementById("snackName").value;
  const category = document.getElementById("snackCategory").value;
  const quantity = document.getElementById("snackQuantity").value;
  const expiry = document.getElementById("snackExpiry").value;

  const snackCard = document.createElement("div");
  snackCard.classList.add("snack-card");

  snackCard.innerHTML = `
    <div class="snack-icon">🍿</div>
    <div>
      <h3>${name}</h3>
      <p>Category: ${category}</p>
      <p>Quantity: ${quantity}</p>
      <p>Expiry Date: ${expiry}</p>
    </div>
  `;

  snackList.appendChild(snackCard);

  snackCount++;
  totalSnacks.textContent = snackCount;

  snackForm.reset();
});
