
import sqlite3

# Database file name
DB_NAME = "employees.db"


# Establish database connection
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database and create employee table
def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add a new employee
def add_employee(name, email, department, salary):
    conn = get_connection()

    try:
        conn.execute("""
            INSERT INTO employees (name, email, department, salary)
            VALUES (?, ?, ?, ?)
        """, (name, email, department, salary))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# View all employees
def view_employees():
    conn = get_connection()

    employees = conn.execute(
        "SELECT * FROM employees"
    ).fetchall()

    conn.close()

    return employees


# Search employee by ID
def search_employee(employee_id):
    conn = get_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    conn.close()

    return employee


# Update employee details
def update_employee(employee_id, name, email, department, salary):
    conn = get_connection()

    try:
        cursor = conn.execute("""
            UPDATE employees
            SET name = ?, email = ?, department = ?, salary = ?
            WHERE id = ?
        """, (name, email, department, salary, employee_id))

        conn.commit()
        return cursor.rowcount > 0

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# Delete employee by ID
def delete_employee(employee_id):
    conn = get_connection()

    cursor = conn.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,)
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted

