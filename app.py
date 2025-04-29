from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import os

app = Flask(__name__)

DB_SERVER = os.environ.get('DB_SERVER')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD}'

def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        hshd_num = request.form['hshd_num']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM transactions WHERE HSHD_NUM = ?"
            cursor.execute(query, (hshd_num,))
            results = cursor.fetchall()
            conn.close()
    return render_template('search.html', results=results)

@app.route('/datapull')
def datapull():
    results = []
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM transactions WHERE HSHD_NUM = 10"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
    return render_template('datapull.html', results=results)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
