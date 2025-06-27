const API_URL = '/api/catalogues';

async function createCatalogue() {
  const name = document.getElementById('name').value;
  const description = document.getElementById('description').value;

  await fetch(API_URL, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ name, description })
  });

  document.getElementById('name').value = '';
  document.getElementById('description').value = '';
  fetchCatalogues();
}

async function fetchCatalogues() {
  const res = await fetch(API_URL);
  const catalogues = await res.json();
  const list = document.getElementById('catalogue-list');
  list.innerHTML = '';

  catalogues.forEach(cat => {
    const li = document.createElement('li');
    li.innerHTML = `
      <b>${cat.name}</b> - ${cat.description}
      <button onclick="deleteCatalogue(${cat.id})">Delete</button>
      <button onclick="showUpdate(${cat.id}, '${cat.name}', '${cat.description}')">Update</button>
    `;
    list.appendChild(li);
  });
}

async function deleteCatalogue(id) {
  await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
  fetchCatalogues();
}

function showUpdate(id, name, description) {
  const newName = prompt('New Name:', name);
  const newDesc = prompt('New Description:', description);
  if (newName && newDesc) {
    updateCatalogue(id, newName, newDesc);
  }
}

async function updateCatalogue(id, name, description) {
  await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ name, description })
  });
  fetchCatalogues();
}

fetchCatalogues();
