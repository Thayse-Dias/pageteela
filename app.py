from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# Criar banco de dados e tabela se não existir
def init_db():
    connection = sqlite3.connect('teela.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opening_date TEXT NOT NULL,
            location TEXT NOT NULL,
            service_description TEXT NOT NULL,
            status TEXT NOT NULL,
            sector TEXT NOT NULL,
            observations TEXT
        )
    ''')
    connection.commit()
    connection.close()

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = sqlite3.connect('teela.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            return "Login bem-sucedido!"
        else:
            return "E-mail ou senha incorretos."

    return render_template_string(open('template.html').read(), active_page='login')

# Página de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        connection = sqlite3.connect('teela.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        connection.commit()
        connection.close()
        
        return redirect(url_for('login'))

    return render_template_string(open('template.html').read(), active_page='register')

# Página de Ordem de Serviço
@app.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'POST':
        opening_date = request.form['opening_date']
        location = request.form['location']
        service_description = request.form['service_description']
        status = request.form['status']
        sector = request.form['sector']
        observations = request.form['observations']

        connection = sqlite3.connect('teela.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO service_orders (opening_date, location, service_description, status, sector, observations) VALUES (?, ?, ?, ?, ?, ?)', 
                       (opening_date, location, service_description, status, sector, observations))
        connection.commit()
        connection.close()

        return "Ordem de serviço cadastrada com sucesso!"

    return render_template_string(open('template.html').read(), active_page='service')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

