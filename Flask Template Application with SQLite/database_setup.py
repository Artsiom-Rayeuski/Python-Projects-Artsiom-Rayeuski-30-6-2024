import sqlite3


def create_database():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Modyfikacja tabeli, dodanie kolumny 'position'
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        position TEXT,
                        salary REAL
                    )''')

    # Dodanie danych do tabeli
    employees_data = [
        ('John Doe', 'Manager', 50000.0),
        ('Jane Smith', 'Developer', 60000.0),
        ('Alice Johnson', 'Sales Representative', 45000.0),
        ('Bob Brown', 'Marketing Specialist', 55000.0),
        ('Emma Wilson', 'HR Manager', 58000.0)
    ]

    cursor.executemany('''INSERT INTO employees (name, position, salary)
                          VALUES (?, ?, ?)''', employees_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
