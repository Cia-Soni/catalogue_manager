document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('catalogueForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = {
        name: document.getElementById('name').value,
        description: document.getElementById('description').value,
        effective_from: document.getElementById('effective_from').value,
        effective_to: document.getElementById('effective_to').value,
        status: document.getElementById('status').value
      };
      await fetch('/catalogues', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      form.reset();
      loadCatalogues();
    });
  }
});
async function loadCatalogues() {
  const res = await fetch('/catalogues');
  const result = await res.json();
  const list = document.getElementById('cataloguesList');
  list.innerHTML = '';
  result.data.forEach(cat => {
    const div = document.createElement('div');
    div.className = 'catalogue-card';
    div.innerHTML = `
      <strong>ID:</strong> ${cat.id} <br>
      <input type="text" id="name-${cat.id}" value="${cat.name}">
      <textarea id="desc-${cat.id}">${cat.description}</textarea>
      <input type="date" id="from-${cat.id}" value="${cat.effective_from}">
      <input type="date" id="to-${cat.id}" value="${cat.effective_to}">
      <select id="status-${cat.id}">
        <option value="active" ${cat.status === 'active' ? 'selected' : ''}>Active</option>
        <option value="inactive" ${cat.status === 'inactive' ? 'selected' : ''}>Inactive</option>
      </select><br>
      <button onclick="updateCatalogue(${cat.id})">Update</button>
      <button onclick="deleteCatalogue(${cat.id})">Delete</button>
    `;
    list.appendChild(div);
  });
}

async function deleteCatalogue(id) {
  await fetch(/catalogues/${id}, { method: 'DELETE' });
  loadCatalogues();
}

async function updateCatalogue(id) {
  const data = {
    name: document.getElementById(name-${id}).value,
    description: document.getElementById(desc-${id}).value,
    effective_from: document.getElementById(from-${id}).value,
    effective_to: document.getElementById(to-${id}).value,
    status: document.getElementById(status-${id}).value
  };
  await fetch(/catalogues/${id}, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  alert('Updated!');
  loadCatalogues();
}