const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
}[char]));

async function api(url, options = {}) {
  const response = await fetch(url, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || `Kërkesa dështoi (${response.status})`);
  return body;
}

function setState(prefix, state, message = "") {
  ["Loading", "Error", "Empty"].forEach((name) => {
    $(`#${prefix}${name}`).hidden = name.toLowerCase() !== state;
  });
  if (state === "error") $(`#${prefix}Error`).textContent = message;
}

function toast(message) {
  const element = $("#toast");
  element.textContent = message;
  element.classList.add("show");
  setTimeout(() => element.classList.remove("show"), 2600);
}

async function loadAnimals() {
  setState("animals", "loading");
  $("#animalsGrid").innerHTML = "";
  const params = new URLSearchParams({
    search: $("#searchInput").value,
    status: $("#statusFilter").value,
  });
  try {
    const data = await api(`/api/animals?${params}`);
    setState("animals", data.count ? null : "empty");
    $("#animalsGrid").innerHTML = data.animals.map((animal) => `
      <article class="card">
        <span class="badge">${escapeHtml(animal.status)}</span>
        <h3>${escapeHtml(animal.name)}</h3>
        <p>${escapeHtml(animal.species)} · ${escapeHtml(animal.breed || "Racë e panjohur")}</p>
        <p>${escapeHtml(animal.description || "Pa përshkrim")}</p>
        ${animal.status === "available"
          ? `<div class="actions"><button data-adopt="${animal.id}" data-name="${escapeHtml(animal.name)}">Apliko për birësim</button></div>`
          : ""}
      </article>`).join("");
  } catch (error) {
    setState("animals", "error", error.message);
  }
}

async function loadAdoptions() {
  setState("adoptions", "loading");
  $("#adoptionsGrid").innerHTML = "";
  try {
    const data = await api("/api/adoptions");
    setState("adoptions", data.count ? null : "empty");
    $("#adoptionsGrid").innerHTML = data.applications.map((item) => `
      <article class="card">
        <span class="badge">${escapeHtml(item.status)}</span>
        <h3>${escapeHtml(item.applicant_name)}</h3>
        <p>Kafsha: ${escapeHtml(item.animal_name)}</p>
        <p>${escapeHtml(item.email)}</p>
        ${item.status === "pending" ? `
          <div class="actions">
            <button data-review="${item.id}" data-status="approved">Mirato</button>
            <button data-review="${item.id}" data-status="rejected">Refuzo</button>
          </div>` : ""}
      </article>`).join("");
  } catch (error) {
    setState("adoptions", "error", error.message);
  }
}

async function loadTasks() {
  setState("tasks", "loading");
  $("#tasksGrid").innerHTML = "";
  try {
    const data = await api("/api/tasks");
    setState("tasks", data.count ? null : "empty");
    $("#tasksGrid").innerHTML = data.tasks.map((task) => `
      <article class="card">
        <span class="badge">${escapeHtml(task.status)}</span>
        <h3>${escapeHtml(task.title)}</h3>
        <p>${escapeHtml(task.description || "")}</p>
        ${task.status !== "done" ? `
          <div class="actions">
            <button data-task="${task.id}" data-status="${task.status === "to_do" ? "in_progress" : "done"}">
              ${task.status === "to_do" ? "Fillo" : "Përfundo"}
            </button>
          </div>` : ""}
      </article>`).join("");
  } catch (error) {
    setState("tasks", "error", error.message);
  }
}

document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach((item) => item.classList.remove("active"));
  tab.classList.add("active");
  document.querySelectorAll(".view").forEach((view) => view.hidden = true);
  $(`#${tab.dataset.view}View`).hidden = false;
  if (tab.dataset.view === "animals") loadAnimals();
  if (tab.dataset.view === "adoptions") loadAdoptions();
  if (tab.dataset.view === "tasks") loadTasks();
}));

$("#searchInput").addEventListener("input", loadAnimals);
$("#statusFilter").addEventListener("change", loadAnimals);
$("#refreshButton").addEventListener("click", () => {
  const active = $(".tab.active").dataset.view;
  if (active === "animals") loadAnimals();
  if (active === "adoptions") loadAdoptions();
  if (active === "tasks") loadTasks();
});

$("#openAnimalForm").addEventListener("click", () => $("#animalDialog").showModal());
document.querySelectorAll("[data-close]").forEach((button) => button.addEventListener("click", () => button.closest("dialog").close()));

$("#animalForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.reportValidity()) return;
  const data = Object.fromEntries(new FormData(form));
  data.age_months = data.age_months ? Number(data.age_months) : null;
  $("#animalFormError").hidden = true;
  try {
    await api("/api/animals", { method: "POST", body: JSON.stringify(data) });
    form.reset();
    $("#animalDialog").close();
    toast("Kafsha u regjistrua.");
    loadAnimals();
  } catch (error) {
    $("#animalFormError").textContent = error.message;
    $("#animalFormError").hidden = false;
  }
});

$("#animalsGrid").addEventListener("click", (event) => {
  const button = event.target.closest("[data-adopt]");
  if (!button) return;
  $("#adoptionForm").elements.animal_id.value = button.dataset.adopt;
  $("#adoptionAnimalName").textContent = `Ju po aplikoni për ${button.dataset.name}.`;
  $("#adoptionDialog").showModal();
});

$("#adoptionForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  if (!form.reportValidity()) return;
  const data = Object.fromEntries(new FormData(form));
  data.animal_id = Number(data.animal_id);
  $("#adoptionFormError").hidden = true;
  try {
    await api("/api/adoptions", { method: "POST", body: JSON.stringify(data) });
    form.reset();
    $("#adoptionDialog").close();
    toast("Aplikimi u dërgua me sukses.");
  } catch (error) {
    $("#adoptionFormError").textContent = error.message;
    $("#adoptionFormError").hidden = false;
  }
});

$("#adoptionsGrid").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-review]");
  if (!button) return;
  try {
    await api(`/api/adoptions/${button.dataset.review}`, {
      method: "PATCH",
      body: JSON.stringify({ status: button.dataset.status }),
    });
    toast(button.dataset.status === "approved" ? "Aplikimi u miratua." : "Aplikimi u refuzua.");
    loadAdoptions();
    loadAnimals();
  } catch (error) {
    toast(error.message);
  }
});

$("#tasksGrid").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-task]");
  if (!button) return;
  try {
    await api(`/api/tasks/${button.dataset.task}`, {
      method: "PATCH",
      body: JSON.stringify({ status: button.dataset.status }),
    });
    toast("Detyra u përditësua.");
    loadTasks();
  } catch (error) {
    toast(error.message);
  }
});

loadAnimals();
