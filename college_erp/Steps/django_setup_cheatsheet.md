# Django Setup & Project Cheat Sheet - Version 1 (Local)

## 1. Create Virtual Environment

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

## 2. Install Django

pip install django

# Optional: check version
django-admin --version

## 3. Create Project

django-admin startproject college_erp
cd config

## 4. Run Development Server

# Default port
python manage.py runserver

# Specific host/port (for remote access or Docker)
python manage.py runserver 0.0.0.0:8000

## 5. Apply Migrations

python manage.py migrate

## 6. Create Superuser (Admin)

python manage.py createsuperuser
# Follow prompts: username, email, password

## 7. Access Admin Panel

http://127.0.0.1:8000/admin

