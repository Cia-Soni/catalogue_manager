from util.db_get_connection import get_connection
from dto.catalogue_dto import Catalogue

class CatalogueService:
    def __init__(self):
        self.init_table()

    def init_table(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS catalogues (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def create(self, data):
        name = data.get('name')
        description = data.get('description')
        status = data.get('status')

        if not name:
            return {'success': False, 'message': 'Name is required'}

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO catalogues (name, description, status) VALUES (?, ?, ?)',
                       (name, description, status))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return {'success': True, 'message': 'Catalogue created', 'data': {'id': new_id}}

    def update(self, catalogue_id, data):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM catalogues WHERE id = ?', (catalogue_id,))
        if not cursor.fetchone():
            conn.close()
            return {'success': False, 'message': 'Catalogue not found'}

        cursor.execute('''
            UPDATE catalogues 
            SET name = ?, description = ?, status = ?
            WHERE id = ?
        ''', (data.get('name'), data.get('description'), data.get('status'), catalogue_id))

        conn.commit()
        conn.close()
        return {'success': True, 'message': 'Catalogue updated'}

    def delete(self, catalogue_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM catalogues WHERE id = ?', (catalogue_id,))
        if not cursor.fetchone():
            conn.close()
            return {'success': False, 'message': 'Catalogue not found'}

        cursor.execute('DELETE FROM catalogues WHERE id = ?', (catalogue_id,))
        conn.commit()
        conn.close()

        return {'success': True, 'message': 'Catalogue deleted'}

    def get_all(self, status=None, page=1, per_page=5):
        offset = (page - 1) * per_page

        conn = get_connection()
        cursor = conn.cursor()

        if status:
            cursor.execute('SELECT * FROM catalogues WHERE status = ? LIMIT ? OFFSET ?', (status, per_page, offset))
            rows = cursor.fetchall()
            cursor.execute('SELECT COUNT(*) FROM catalogues WHERE status = ?', (status,))
            total = cursor.fetchone()[0]
        else:
            cursor.execute('SELECT * FROM catalogues LIMIT ? OFFSET ?', (per_page, offset))
            rows = cursor.fetchall()
            cursor.execute('SELECT COUNT(*) FROM catalogues')
            total = cursor.fetchone()[0]

        conn.close()

        items = []
        for row in rows:
            item = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'status': row[3]
            }
            items.append(item)

        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total // per_page) + (1 if total % per_page else 0)
        }
