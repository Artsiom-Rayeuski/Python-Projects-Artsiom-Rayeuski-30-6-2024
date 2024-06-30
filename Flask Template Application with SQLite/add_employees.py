import sqlite3

def add_employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()

    # Dodanie danych do tabeli
    employees_data = [
        ('Johnny Dollar', 'Manager', 50000.0),
        ('Jon Smon', 'Developer', 60000.0),
        ('Alex Jackinson', 'Sales Representative', 45000.0),
        ('Peggy Brown', 'Marketing Specialist', 55000.0),
        ('Ezachiel Watson', 'HR Manager', 58000.0)
    ]

    cursor.executemany('''INSERT INTO employees (name, position, salary)
                          VALUES (?, ?, ?)''', employees_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_employees()
