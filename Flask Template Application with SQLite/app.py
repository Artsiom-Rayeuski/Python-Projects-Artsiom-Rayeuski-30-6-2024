from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('employees.db')
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            employee_id = int(request.form['employee_id'])
            cur.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
            employee_data = cur.fetchone()
            conn.close()
            if employee_data:
                return render_template('index.html', employee_data=employee_data)
            else:
                return render_template('index.html', error="No employee found with that ID.")
        except ValueError:
            conn.close()
            return render_template('index.html', error="Please enter a valid employee ID.")
        except OverflowError:
            conn.close()
            return render_template('index.html', error = "Please enter a valid employee ID.")

    conn.close()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
