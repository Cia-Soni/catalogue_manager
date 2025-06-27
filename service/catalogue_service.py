from util.db_get_connection import get_connection
from dto.catalogue_dto import CatalogueDTO
from util.validators import validate_catalogue_data
from exceptions.exceptions import CatalogueNotFoundError

class CatalogueService:
    def create_catalogue(self, name, description):
        validate_catalogue_data({'name': name, 'description': description})
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO catalogue (name, description) VALUES (%s, %s)",
            (name, description)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {'id': new_id, 'name': name, 'description': description}

    def get_all_catalogues(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM catalogue")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def update_catalogue(self, catalogue_id, name, description):
        validate_catalogue_data({'name': name, 'description': description})
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE catalogue SET name=%s, description=%s WHERE id=%s",
            (name, description, catalogue_id)
        )
        if cursor.rowcount == 0:
            raise CatalogueNotFoundError(f"Catalogue ID {catalogue_id} not found.")
        conn.commit()
        cursor.close()
        conn.close()
        return {'id': catalogue_id, 'name': name, 'description': description}

    def delete_catalogue(self, catalogue_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM catalogue WHERE id=%s",
            (catalogue_id,)
        )
        if cursor.rowcount == 0:
            raise CatalogueNotFoundError(f"Catalogue ID {catalogue_id} not found.")
        conn.commit()
        cursor.close()
        conn.close()
        return {'status': 'deleted', 'id': catalogue_id}
