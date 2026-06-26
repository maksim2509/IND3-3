// ⬇️ ЗАМІНИТИ після деплою на Render
const API_URL = "https://YOUR-APP.onrender.com";

let cart = new Map();
let allDishes = [];
let spinning = false;

const dishGrid     = document.getElementById("dish-grid");
const categoryList = document.getElementById("category-list");
const cartItems    = document.getElementById("cart-items");
const cartTotalNum = document.getElementById("cart-total");
const orderBtn     = document.getElementById("order-btn");
const randomBtn    = document.getElementById("random-btn");
const roulette     = document.getElementById("roulette-display");
const orderHistory = document.getElementById("order-history");
const toast        = document.getElementById("toast");

async function init() {
  await Promise.all([loadCategories(), loadDishes(), loadOrders()]);
}

async function loadCategories() {
  try {
    const res  = await fetch(`${API_URL}/categories`);
    const cats = await res.json();
    categoryList.innerHTML =
      `<button class="cat-btn active" onclick="filterCat(null, this)">Всі</button>` +
      cats.map(c => `<button class="cat-btn" onclick="filterCat('${c}', this)">${c}</button>`).join("");
  } catch {
    showToast("Не вдалося завантажити категорії", "err");
  }
}

async function loadDishes(category = null) {
  dishGrid.innerHTML = skeletons(4);
  try {
    const url = category
      ? `${API_URL}/dishes?category=${encodeURIComponent(category)}`
      : `${API_URL}/dishes`;
    const res = await fetch(url);
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail); }
    allDishes = await res.json();
    renderDishes();
  } catch (e) {
    dishGrid.innerHTML = `<div class="grid-empty">⚠️ ${e.message}</div>`;
  }
}

function renderDishes() {
  if (!allDishes.length) {
    dishGrid.innerHTML = `<div class="grid-empty">Страв не знайдено</div>`;
    return;
  }
  dishGrid.innerHTML = allDishes.map(d => `
    <div class="dish-card ${cart.has(d.id) ? "selected" : ""}"
         id="dish-${d.id}" onclick="toggleCart(${d.id})">
      <span class="dish-emoji">${d.emoji}</span>
      <div class="dish-name">${d.name}</div>
      <div class="dish-cat">${d.category}</div>
      <div class="dish-price">${d.price} грн</div>
      <div class="dish-check">✓</div>
    </div>
  `).join("");
}

function toggleCart(id) {
  const dish = allDishes.find(d => d.id === id);
  if (!dish) return;
  if (cart.has(id)) { cart.delete(id); } else { cart.set(id, dish); }
  const card = document.getElementById(`dish-${id}`);
  if (card) card.classList.toggle("selected", cart.has(id));
  renderCart();
}

function renderCart() {
  const items = [...cart.values()];
  if (!items.length) {
    cartItems.innerHTML = `<div class="cart-empty">Нічого не обрано</div>`;
    cartTotalNum.textContent = "0 грн";
    orderBtn.disabled = true;
    return;
  }
  cartItems.innerHTML = items.map(d => `
    <div class="cart-row">
      <span class="cart-row-emoji">${d.emoji}</span>
      <span class="cart-row-name">${d.name}</span>
      <span class="cart-row-price">${d.price} грн</span>
      <button class="cart-row-remove" onclick="toggleCart(${d.id})">✕</button>
    </div>
  `).join("");
  const total = items.reduce((s, d) => s + d.price, 0);
  cartTotalNum.textContent = `${total} грн`;
  orderBtn.disabled = false;
}

function filterCat(cat, btn) {
  document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  loadDishes(cat);
}

async function spinRandom() {
  if (spinning) return;
  spinning = true;
  randomBtn.disabled = true;
  roulette.innerHTML = `<div class="roulette-spinning">🎲</div>`;
  try {
    const res  = await fetch(`${API_URL}/dishes/random`);
    const dish = await res.json();
    roulette.innerHTML = `
      <div class="roulette-result">
        <span class="r-emoji">${dish.emoji}</span>
        <span class="r-name">${dish.name}</span>
        <span class="r-price">${dish.price} грн</span>
      </div>`;
    if (!cart.has(dish.id)) {
      cart.set(dish.id, dish);
      const card = document.getElementById(`dish-${dish.id}`);
      if (card) {
        card.classList.add("selected", "highlight");
        card.scrollIntoView({ behavior: "smooth", block: "center" });
        setTimeout(() => card.classList.remove("highlight"), 700);
      }
      renderCart();
    }
    showToast(`Додано: ${dish.name} 🎲`, "ok");
  } catch {
    roulette.innerHTML = `<div class="roulette-idle">🎲</div>`;
    showToast("Помилка з'єднання з сервером", "err");
  } finally {
    spinning = false;
    randomBtn.disabled = false;
  }
}

async function submitOrder() {
  if (!cart.size) return;
  orderBtn.disabled = true;
  orderBtn.textContent = "Надсилаємо...";
  try {
    const res = await fetch(`${API_URL}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dish_ids: [...cart.keys()] }),
    });
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail); }
    const order = await res.json();
    showToast(`Замовлення #${order.id} на ${order.total} грн прийнято 🎉`, "ok");
    cart.clear();
    renderCart();
    renderDishes();
    await loadOrders();
  } catch (e) {
    showToast(e.message, "err");
  } finally {
    orderBtn.disabled = false;
    orderBtn.textContent = "Замовити";
  }
}

async function loadOrders() {
  try {
    const res    = await fetch(`${API_URL}/orders`);
    const orders = await res.json();
    if (!orders.length) {
      orderHistory.innerHTML = `<div class="cart-empty">Ще немає замовлень</div>`;
      return;
    }
    orderHistory.innerHTML = [...orders].reverse().map(o => `
      <div class="order-card" id="order-${o.id}">
        <div class="order-card-head">
          <span class="order-id">#${o.id} · ${fmtDate(o.created_at)}</span>
          <span class="order-sum">${o.total} грн</span>
          <button class="order-del" onclick="deleteOrder(${o.id})">✕</button>
        </div>
        <div class="order-dishes-list">
          ${o.dishes.map(d => `${d.emoji} ${d.name}`).join(" · ")}
        </div>
      </div>
    `).join("");
  } catch {
    orderHistory.innerHTML = `<div class="cart-empty">Не вдалося завантажити</div>`;
  }
}

async function deleteOrder(id) {
  try {
    const res = await fetch(`${API_URL}/orders/${id}`, { method: "DELETE" });
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail); }
    showToast(`Замовлення #${id} видалено`, "ok");
    await loadOrders();
  } catch (e) {
    showToast(e.message, "err");
  }
}

function showToast(msg, type = "ok") {
  toast.textContent = msg;
  toast.className = `toast show ${type}`;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => toast.classList.remove("show"), 3000);
}

function fmtDate(iso) {
  return new Date(iso).toLocaleString("uk-UA", {
    day: "2-digit", month: "2-digit",
    hour: "2-digit", minute: "2-digit",
  });
}

function skeletons(n) {
  return Array(n).fill(`<div class="skeleton"></div>`).join("");
}

init();
