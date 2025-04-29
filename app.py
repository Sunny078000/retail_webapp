from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Azure SQL Database connection settings
server = '<your-server-name>.database.windows.net'
database = 'retaildb'
username = '<your-username>'
password = '<your-password>'
driver = '{ODBC Driver 17 for SQL Server}'

# Connection string
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST':
        hshd_num = request.form.get('hshd_num')

        # Connect to the database
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            query = '''
                SELECT t.HSHD_NUM, t.BASKET_NUM, t.PURCHASE_DATE, 
                       p.PRODUCT_NUM, p.DEPARTMENT, p.COMMODITY
                FROM dbo.transactions t
                JOIN dbo.products p ON t.PRODUCT_NUM = p.PRODUCT_NUM
                WHERE t.HSHD_NUM = ?
                ORDER BY t.HSHD_NUM, t.BASKET_NUM, t.PURCHASE_DATE, p.PRODUCT_NUM, p.DEPARTMENT, p.COMMODITY
            '''
            cursor.execute(query, (hshd_num,))
            results = cursor.fetchall()

        except Exception as e:
            print("Database connection error:", e)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
