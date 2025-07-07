from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flasgger import Swagger
import pymysql
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)
swagger = Swagger(app)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Ciaannsoni@1',
    'database': 'catalogue_db'
}

#  LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            logging.info(f"Login success for {username}")
            return redirect(url_for('catalogues_page'))
        else:
            logging.warning(f"Login failed for {username}")
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    user = session.pop('username', None)
    logging.info(f"Logout by {user}")
    return redirect(url_for('login'))

#  SHOW CATALOGUES PAGE
@app.route('/catalogues-page')
def catalogues_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM catalogues")
        catalogues = cursor.fetchall()
    conn.close()
    return render_template('catalogues.html', catalogues=catalogues)

#  GET ALL (API)
@app.route('/catalogues', methods=['GET'])
def get_catalogues():
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM catalogues")
        catalogues = cursor.fetchall()
    conn.close()
    return jsonify({'status': 'success', 'data': catalogues})

#  GET BY ID
@app.route('/catalogues/<int:catalogue_id>', methods=['GET'])
def get_by_id(catalogue_id):
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM catalogues WHERE id=%s", (catalogue_id,))
        cat = cursor.fetchone()
    conn.close()
    if cat:
        return jsonify({'status': 'success', 'data': cat})
    else:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

#  CREATE
@app.route('/catalogues', methods=['POST'])
def create_cat():
    data = request.json
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO catalogues (name, description, effective_from, effective_to, status) "
            "VALUES (%s, %s, %s, %s, %s)",
            (data['name'], data['description'], data['effective_from'], data['effective_to'], data['status'])
        )
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({'status': 'success', 'id': new_id}), 201

# UPDATE
@app.route('/catalogues/<int:catalogue_id>', methods=['PUT'])
def update_cat(catalogue_id):
    data = request.json
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE catalogues SET name=%s, description=%s, effective_from=%s, effective_to=%s, status=%s WHERE id=%s",
            (data['name'], data['description'], data['effective_from'],
             data['effective_to'], data['status'], catalogue_id)
        )
        conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

# DELETE
@app.route('/catalogues/<int:catalogue_id>', methods=['DELETE'])
def delete_cat(catalogue_id):
    conn = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM catalogues WHERE id=%s", (catalogue_id,))
        conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

