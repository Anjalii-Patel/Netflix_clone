// frontend/js/subscribe.js
const AUTH_API = "http://localhost:8000/api/auth/";

async function loadPlans() {
  checkAuth();
  renderNav();
  const res = await apiFetch(`${AUTH_API}plans/`);
  const container = document.getElementById("plans");
  container.innerHTML = "";
  if (!res.ok) {
    container.innerHTML = "<p>Failed to load plans.</p>";
    return;
  }
  const plans = await res.json();
  plans.forEach(p => {
    const card = document.createElement("div");
    card.className = "plan-card";
    card.innerHTML = `
      <h3>${p.name}</h3>
      <p>${p.description || ""}</p>
      <p><strong>$${p.price}</strong> / ${p.duration_days} days</p>
      <button data-id="${p.id}">Subscribe</button>
    `;
    card.querySelector("button").onclick = () => subscribe(p.id);
    container.appendChild(card);
  });
}

async function subscribe(planId) {
  const res = await apiFetch(`${AUTH_API}subscribe/checkout/`, {
    method: "POST",
    body: JSON.stringify({ plan_id: planId })
  });
  if (!res.ok) {
    alert("Subscription failed");
    return;
  }
  const next = new URLSearchParams(window.location.search).get("next");
  alert("Subscription active!");
  window.location.href = next || "index.html";
}

document.addEventListener("DOMContentLoaded", loadPlans);
