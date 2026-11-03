
import re

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    initialize_database,
    add_employee,
    view_employees,
    search_employee,
    update_employee,
    delete_employee
)

app = Flask(__name__)
app.secret_key = "employee-management-secret-key"


# Calculate dashboard statistics
def get_dashboard_stats():
    employees = view_employees()

    total_employees = len(employees)

    total_salary = sum(
        float(employee["salary"]) for employee in employees
    )

    return total_employees, total_salary


# Validate employee details
def validate_employee(name, email, department, salary):

    if not name or not email or not department or not salary:
        return "All fields are required."

    if len(name) < 2:
        return "Employee name must contain at least 2 characters."

    email_pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

    if not re.match(email_pattern, email):
        return "Please enter a valid email address."

    try:
        salary = float(salary)
    except (ValueError, TypeError):
        return "Salary must be a valid number."

    if salary < 0:
        return "Salary cannot be negative."

    return None


# Home page
@app.route("/")
def home():
    employees = view_employees()
    total_employees, total_salary = get_dashboard_stats()

    return render_template(
        "index.html",
        employees=employees,
        total_employees=total_employees,
        total_salary=total_salary
    )


# Search employee
@app.route("/search", methods=["POST"])
def search():

    employee_id = request.form.get("employee_id", "").strip()

    if not employee_id.isdigit():
        flash("Please enter a valid employee ID.")
        return redirect(url_for("home"))

    employee = search_employee(int(employee_id))

    if employee:
        employees = [employee]
    else:
        employees = []
        flash("Employee not found!")

    total_employees, total_salary = get_dashboard_stats()

    return render_template(
        "index.html",
        employees=employees,
        total_employees=total_employees,
        total_salary=total_salary
    )


# Add employee
@app.route("/add", methods=["POST"])
def add():

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()
    salary = request.form.get("salary", "").strip()

    error = validate_employee(name, email, department, salary)

    if error:
        flash(error)
        return redirect(url_for("home"))

    result = add_employee(
        name,
        email,
        department,
        float(salary)
    )

    if result:
        flash("Employee added successfully!")
    else:
        flash("This email address is already registered.")

    return redirect(url_for("home"))


# Edit employee
@app.route("/edit/<int:employee_id>", methods=["GET", "POST"])
def edit(employee_id):

    employee = search_employee(employee_id)

    if employee is None:
        flash("Employee not found!")
        return redirect(url_for("home"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        salary = request.form.get("salary", "").strip()

        error = validate_employee(name, email, department, salary)

        if error:
            flash(error)
            return redirect(url_for("edit", employee_id=employee_id))

        result = update_employee(
            employee_id,
            name,
            email,
            department,
            float(salary)
        )

        if result:
            flash("Employee updated successfully!")
        else:
            flash("Update failed. Email address may already exist.")

        return redirect(url_for("home"))

    return render_template("edit.html", employee=employee)


# Delete employee
@app.route("/delete/<int:employee_id>", methods=["POST"])
def delete(employee_id):

    result = delete_employee(employee_id)

    if result:
        flash("Employee deleted successfully!")
    else:
        flash("Employee not found!")

    return redirect(url_for("home"))


# Run application
if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
