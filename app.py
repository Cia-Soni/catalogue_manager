from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flasgger import Swagger
import logging

app = Flask(__name__)  #
app.secret_key = 'supersecretkey'
CORS(app)

# 👉 Setup Swagger
swagger = Swagger(app)

# 👉 Setup Logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

USERS = {"admin": "password"}

CATALOGUES = [
    {'id': 1, 'name': 'Electronics', 'description': 'Phones & gadgets', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'active'},
    {'id': 2, 'name': 'Furniture', 'description': 'Home furniture', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'inactive'},
    {'id': 3, 'name': 'Books', 'description': 'Books & stationery', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'active'},
    {'id': 4, 'name': 'Clothing', 'description': 'Men & Women wear', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'active'},
    {'id': 5, 'name': 'Kitchen', 'description': 'Appliances & cookware', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'inactive'},
    {'id': 6, 'name': 'Home Decor', 'description': 'Decor & accessories', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'active'},
    {'id': 7, 'name': 'Gaming', 'description': 'Games & consoles', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'active'},
    {'id': 8, 'name': 'Laptops', 'description': 'Latest laptops', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'inactive'},
    {'id': 9, 'name': 'Automobiles', 'description': 'Cars & accessories', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'active'},
    {'id': 10, 'name': 'Fitness', 'description': 'Gym equipment', 'effective_from': '2025-07-01', 'effective_to': '2025-12-31', 'status': 'active'},
]
ID_COUNTER = 11

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USERS.get(username) == password:
            session['username'] = username
            logging.info(f"User '{username}' logged in successfully.")
            return redirect(url_for('catalogues_page'))
        else:
            logging.warning(f"Failed login attempt for user '{username}'.")
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/catalogues-page')
def catalogues_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('catalogues.html', catalogues=CATALOGUES)


@app.route('/logout')
def logout():
    username = session.pop('username', None)
    logging.info(f"User '{username}' logged out.")
    return redirect(url_for('login'))

@app.route('/catalogues', methods=['GET'])
def get_catalogues():
    """
    Get paginated catalogues
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: per_page
        in: query
        type: integer
        required: false
        default: 5
    responses:
      200:
        description: Paginated list of catalogues
    """
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    start = (page - 1) * per_page
    end = start + per_page
    paginated = CATALOGUES[start:end]
    logging.info(f"Fetched catalogues page {page} with {per_page} per page.")
    return jsonify({
        'status': 'success',
        'data': paginated,
        'page': page,
        'per_page': per_page,
        'total': len(CATALOGUES)
    }), 200

@app.route('/catalogues/<int:catalogue_id>', methods=['GET'])
def get_catalogue_by_id(catalogue_id):
    """
    Get a catalogue by ID
    ---
    parameters:
      - name: catalogue_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Catalogue found
      404:
        description: Catalogue not found
    """
    for cat in CATALOGUES:
        if cat['id'] == catalogue_id:
            logging.info(f"Catalogue ID {catalogue_id} found.")
            return jsonify({'status': 'success', 'data': cat}), 200
    logging.warning(f"Catalogue ID {catalogue_id} not found.")
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.route('/catalogues', methods=['POST'])
def create_catalogue():
    """
    Create a new catalogue
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            effective_from:
              type: string
            effective_to:
              type: string
            status:
              type: string
    responses:
      201:
        description: Catalogue created
    """
    global ID_COUNTER
    data = request.json
    new_cat = {
        'id': ID_COUNTER,
        'name': data.get('name'),
        'description': data.get('description'),
        'effective_from': data.get('effective_from'),
        'effective_to': data.get('effective_to'),
        'status': data.get('status')
    }
    CATALOGUES.append(new_cat)
    ID_COUNTER += 1
    logging.info(f"Created new catalogue: {new_cat}")
    return jsonify({'status': 'success', 'data': new_cat}), 201

@app.route('/catalogues/<int:catalogue_id>', methods=['PUT'])
def update_catalogue(catalogue_id):
    """
    Update a catalogue by ID
    ---
    parameters:
      - name: catalogue_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
    responses:
      200:
        description: Catalogue updated
      404:
        description: Catalogue not found
    """
    data = request.json
    for cat in CATALOGUES:
        if cat['id'] == catalogue_id:
            cat.update({k: v for k, v in data.items() if k in cat})
            logging.info(f"Updated catalogue ID {catalogue_id}: {cat}")
            return jsonify({'status': 'success', 'data': cat}), 200
    logging.warning(f"Catalogue ID {catalogue_id} not found for update.")
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.route('/catalogues/<int:catalogue_id>', methods=['DELETE'])
def delete_catalogue(catalogue_id):
    """
    Delete a catalogue by ID
    ---
    parameters:
      - name: catalogue_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Catalogue deleted
    """
    global CATALOGUES
    CATALOGUES = [c for c in CATALOGUES if c['id'] != catalogue_id]
    logging.info(f"Deleted catalogue ID {catalogue_id}.")
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
