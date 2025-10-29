# Django Setup & Project Cheat Sheet - Version 2 (Docker)

## 1. Create Virtual Environment (Optional)

# Only if you need local Python packages
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

## 2. Install Django in venv (Optional)

pip install django

## 3. Docker Compose Setup

# docker-compose.yml example

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_DB: college_erp_db
      POSTGRES_USER: college_erp_user
      POSTGRES_PASSWORD: Ilikecoding@884d
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

## 4. Run Migrations
docker-compose exec web python manage.py makemigrations 
docker-compose exec web python manage.py migrate

## 5. Create Superuser

docker-compose exec web python manage.py createsuperuser

## Start Docker Desktop  (Open aaplication)
cd .\config\
docker-compose up --build 

## 6. Run Development Server
docker-compose exec web python manage.py runserver 0.0.0.0:8000

## 7. Access Admin Panel

http://127.0.0.1:8000/admin

