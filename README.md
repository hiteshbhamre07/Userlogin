# 🔐 Flask User Authentication with Admin Panel

This is a simple Flask web application implementing user registration, login, and an admin panel using Flask-Admin and MySQL as the database.

---



## 🧰 Tech Stack

- **Flask** – Micro web framework
- **Flask-WTF** – Form handling and CSRF protection
- **Flask-Login** – User session management
- **Flask-Admin** – Admin dashboard
- **SQLAlchemy** – ORM for database interaction
- **MySQL** – Relational database

---

## ⚙️ Setup Instructions

### ✅ 1. Clone the repository

```bash
git clone https://github.com/hiteshbhamre07/DIP_3.git
cd DIP_3


🐍** 2. Create and activate virtual environment**

python -m venv venv
venv\Scripts\activate  # On Windows

**📦 3. Install dependencies**
pip install -r requirements.txt

**🔧 4. Configure database**
Make sure MySQL is running and update your database URI in the script:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flaskapp_db'

🚀 Running the App

  python app.py


