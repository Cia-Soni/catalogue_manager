const BASE_URL = "http://127.0.0.1:5000";

async function createCatalogue() {
  const data = {
    name: document.getElementById("name").value,
    description: document.getElementById("description").value,
    start_date: document.getElementById("start_date").value,
    end_date: document.getElementById("end_date").value
  };
  const res = await fetch(`${BASE_URL}/catalogue`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const json = await res.json();
  alert(JSON.stringify(json));
}

async function updateCatalogue() {
  const id = document.getElementById("update_id").value;
  const data = {
    name: document.getElementById("update_name").value,
    description: document.getElementById("update_description").value,
    start_date: document.getElementById("update_start_date").value,
    end_date: document.getElementById("update_end_date").value
  };
  const res = await fetch(`${BASE_URL}/catalogue/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const json = await res.json();
  alert(JSON.stringify(json));
}

async function deleteCatalogue() {
  const id = document.getElementById("delete_id").value;
  const res = await fetch(`${BASE_URL}/catalogue/${id}`, {
    method: "DELETE"
  });
  const json = await res.json();
  alert(JSON.stringify(json));
}

async function getAllCatalogues() {
  const res = await fetch(`${BASE_URL}/catalogue`);
  const json = await res.json();
  document.getElementById("result").innerText = JSON.stringify(json, null, 2);
}
