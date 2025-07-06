from util.db_get_connection import get_connection

class AuthService:
    def __init__(self):
        self.init_user_table()

    def init_user_table(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def register(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, password)
            )
            conn.commit()
            return {'success': True, 'message': 'User registered'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()

    def login(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id FROM users WHERE username = %s AND password = %s',
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            return {'success': True, 'user_id': user[0]}
        else:
            return {'success': False, 'message': 'Invalid credentials'}
