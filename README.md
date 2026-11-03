<img width="1917" height="1038" alt="image" src="https://github.com/user-attachments/assets/b5a419b1-7dbb-4afa-9576-e8017da77389" />


# Employee Management System

A web-based Employee Management System developed using Python, Flask, and SQLite. This application allows users to manage employee records through a simple and responsive web interface.

## Features

- Add new employee records
- View all employee records
- Search employees by ID
- Update employee information
- Delete employee records with confirmation
- Validate employee details
- Prevent duplicate email addresses
- Dashboard displaying total employees
- Calculate total salary expenditure
- Responsive user interface
- Unit testing using Python unittest

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Delete confirmation |
| unittest | Unit testing |
| Git & GitHub | Version control |

## Project Structure

```text
EmployeeManagementSystem/
│
├── app.py
├── database.py
├── test_employee.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   └── edit.html
│
├── static/
│   └── style.css
│
└── employees.db
```

Note: The SQLite database is generated automatically when the application starts. It is excluded from GitHub.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd EmployeeManagementSystem
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5000
```

## Running Unit Tests

Execute the following command:

```bash
python -m unittest test_employee -v
```

The test suite covers:

- Adding employees
- Adding multiple employees
- Duplicate email prevention
- Viewing employee records
- Searching existing and missing employees
- Updating employee records
- Preventing duplicate emails during updates
- Deleting existing and missing employees

## Database Design

The application uses an SQLite database with an `employees` table.

| Column | Data Type | Constraint |
|---|---|---|
| id | INTEGER | Primary Key, Auto Increment |
| name | TEXT | NOT NULL |
| email | TEXT | UNIQUE, NOT NULL |
| department | TEXT | NOT NULL |
| salary | REAL | NOT NULL |

## Application Screenshots

Add screenshots of the application interface here.

## Future Improvements

- User authentication and authorization
- Employee profile management
- Department-wise employee filtering
- Pagination and sorting
- Export employee records to CSV or Excel
- Improved form and server-side validation

## Author

**Vijay Simha**

B.Tech – Electronics and Communication Engineering

