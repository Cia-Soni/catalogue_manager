from flask import Flask, request, jsonify, send_from_directory
from service.catalogue_service import CatalogueService
from exceptions.exceptions import CatalogueNotFoundError, InvalidInputError

#Initialize Flask app
app = Flask(__name__, static_folder='static')

catalogue_service = CatalogueService()


@app.route('/')
def index():

    return send_from_directory('static', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# API: Create a new catalogue
@app.route('/api/catalogues', methods=['POST'])
def create_catalogue():
    data = request.get_json()
    try:
        #  1. Validate input & call service method
        result = catalogue_service.create_catalogue(data['name'], data['description'])

        # 2. Return created catalogue with 201 status
        return jsonify(result), 201
    except InvalidInputError as e:
        #  Return validation error
        return jsonify({'error': str(e)}), 400
    except Exception as e:

        return jsonify({'error': 'Internal Server Error'}), 500


# API: Get all catalogues
@app.route('/api/catalogues', methods=['GET'])
def get_catalogues():
    try:
        #  Call service to get all records
        result = catalogue_service.get_all_catalogues()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

# API: Update a catalogue
@app.route('/api/catalogues/<int:catalogue_id>', methods=['PUT'])
def update_catalogue(catalogue_id):
    data = request.get_json()
    try:
        # Validate input & call update
        result = catalogue_service.update_catalogue(catalogue_id, data['name'], data['description'])
        return jsonify(result)
    except CatalogueNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except InvalidInputError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500


# API: Delete a catalogue
@app.route('/api/catalogues/<int:catalogue_id>', methods=['DELETE'])
def delete_catalogue(catalogue_id):
    try:
        #Call delete service method
        result = catalogue_service.delete_catalogue(catalogue_id)
        return jsonify(result)
    except CatalogueNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
 
    app.run(debug=True)
