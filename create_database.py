# create_db.py
import sqlite3

def create_database():
    connection = sqlite3.connect('teela.db')
    cursor = connection.cursor()

    # Cria uma tabela para armazenar usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_database()
