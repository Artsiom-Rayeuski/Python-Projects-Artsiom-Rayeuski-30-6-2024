from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

# Połączenie z bazą danych MySQL
db = pymysql.connect(
    host="nazwa_hosta",
    user="nazwa_uzytkownika",
    password="haslo",
    database="nazwa_bazy_danych"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employee', methods=['POST'])
def get_employee():
    employee_id = request.form['employee_id']
    query = "SELECT * FROM employees WHERE id = %s"
    cursor.execute(query, (employee_id,))
    employee = cursor.fetchone()

    if employee:
        # Tutaj możesz zwrócić dane pracownika w dowolny sposób
        return f"Dane pracownika: {employee}"
    else:
        return "Pracownik o podanym ID nie istnieje."

if __name__ == '__main__':
    app.run(debug=True)
