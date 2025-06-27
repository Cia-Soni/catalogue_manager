from exceptions.exceptions import InvalidInputError

def validate_catalogue_data(data):
    if not data.get('name') or not data.get('description'):
        raise InvalidInputError("Both name and description are required.")
    if len(data['name']) > 100:
        raise InvalidInputError("Name must be under 100 characters.")
